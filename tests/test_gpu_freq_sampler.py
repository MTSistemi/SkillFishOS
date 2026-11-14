"""skillfish-gpu-freq-sampler: one gpu_metrics reader, and no SMU mailbox of its own.

Until 26.11.2 the sampler sent messages on the SMU's queue 0 through the SMN
window, which is the mailbox amdgpu itself uses: it raced the driver and caused
"Failed to export SMU metrics table!". These tests keep it from coming back and
check the values it publishes from a gpu_metrics table.
"""
import importlib.machinery
import importlib.util
import pathlib
import struct

SAMPLER = (pathlib.Path(__file__).resolve().parents[1]
           / "system" / "usr" / "local" / "bin" / "skillfish-gpu-freq-sampler")


def _load():
    loader = importlib.machinery.SourceFileLoader("sampler_mod", str(SAMPLER))
    spec = importlib.util.spec_from_loader("sampler_mod", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)         # main() only runs under __main__
    return mod


def _table(gfxclk=1850, apu=29500, cpu=150, gpu=4060, fmt=2):
    d = bytearray(128)
    d[2], d[3] = fmt, 2
    struct.pack_into("<H", d, 40, apu)
    struct.pack_into("<H", d, 44, cpu)
    struct.pack_into("<H", d, 46, gpu)
    struct.pack_into("<H", d, 76, gfxclk)
    return bytes(d)


def _code():
    """The source without comments: the history in the header names the old
    registers on purpose."""
    lines = SAMPLER.read_text(encoding="utf-8").splitlines()
    return "\n".join(l.split("#", 1)[0] for l in lines)


def test_it_never_touches_the_smn_window_or_the_driver_mailbox():
    code = _code()
    assert "0000:00:00.0/config" not in code
    assert "0xB8" not in code and "0xBC" not in code
    assert "03B10A" not in code.upper()
    assert "pwrite" not in code


def test_power_line_reads_the_measured_offsets_in_watts():
    m = _load()
    assert m.power_line(_table()) == "29.5 0.1 4.1"


def test_unreported_power_is_a_dash_not_65_watts():
    m = _load()
    assert m.power_line(_table(cpu=0xFFFF)) == "29.5 - 4.1"


def test_gfxclk_comes_from_offset_76():
    m = _load()
    assert m.u16(_table(gfxclk=2114), m.GFXCLK_OFFSET) == 2114


def test_a_table_of_another_format_is_not_trusted(tmp_path, monkeypatch):
    m = _load()
    f = tmp_path / "gpu_metrics"
    f.write_bytes(_table(fmt=1))
    monkeypatch.setattr(m, "METRICS", str(f))
    assert m.read_metrics() is None
    f.write_bytes(_table())
    assert m.read_metrics() is not None

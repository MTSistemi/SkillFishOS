"""Tests for the pure logic of skillfish-tuner-helper (no root, no SMU, no Qt).

These guard the GPU-governor config writer: the multi-point voltage curve and
the Balanced/Performance mode switch. A wrong curve here can hard-freeze a
BC-250 (see docs/OPTIMIZATIONS.md), so this is the most safety-critical pure
logic in the repo.
"""
import importlib.machinery
import importlib.util
import pathlib
import types

import pytest

HELPER = pathlib.Path(__file__).resolve().parents[1] / "apps" / "tuner" / "skillfish-tuner-helper"


@pytest.fixture()
def helper(tmp_path, monkeypatch):
    loader = importlib.machinery.SourceFileLoader("tuner_helper", str(HELPER))
    spec = importlib.util.spec_from_loader("tuner_helper", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    # never touch the real system from tests
    conf = tmp_path / "config.toml"
    monkeypatch.setattr(mod, "GOV_CONF", str(conf))
    calls = []
    monkeypatch.setattr(mod, "sh", lambda cmd, timeout=30: (calls.append(cmd), types.SimpleNamespace(returncode=0, stdout=""))[1])
    mod._test_calls = calls
    mod._test_conf = conf
    return mod


# ---------- _gpu_curve: the multi-point voltage ladder ----------

def test_curve_full_range_inserts_midpoints(helper):
    assert helper._gpu_curve(350, 700, 2200, 1000) == [(350, 700), (1500, 900), (2000, 1000), (2200, 1000)]


def test_curve_low_max_has_no_midpoints_above_it(helper):
    assert helper._gpu_curve(350, 700, 1500, 900) == [(350, 700), (1500, 900)]


def test_curve_dedup_when_max_is_a_midpoint(helper):
    pts = helper._gpu_curve(350, 700, 2000, 1000)
    assert pts == [(350, 700), (1500, 900), (2000, 1000)]
    freqs = [f for f, _ in pts]
    assert len(freqs) == len(set(freqs)), "no duplicate frequencies"


def test_curve_is_ascending(helper):
    pts = helper._gpu_curve(350, 700, 2200, 1000)
    assert pts == sorted(pts)


def test_curve_clamps_undervolted_2230(helper):
    # 2230 @ <=1000 mV is the reproduced hard-freeze combo: must clamp to 2200
    pts = helper._gpu_curve(350, 700, 2230, 1000)
    assert max(f for f, _ in pts) == 2200


def test_curve_allows_2230_with_proper_voltage(helper):
    pts = helper._gpu_curve(350, 700, 2230, 1060)
    assert (2230, 1060) in pts


# ---------- apply_gpu: writes the curve, replaces old safe-points ----------

def test_apply_gpu_writes_multipoint_curve(helper):
    helper._test_conf.write_text("[load-target]\nupper = 0.95\nlower = 0.7\n"
                                 "[[safe-points]]\nfrequency = 350\nvoltage = 700\n"
                                 "[[safe-points]]\nfrequency = 2230\nvoltage = 1000\n")
    assert helper.apply_gpu(350, 700, 2200, 1000)
    txt = helper._test_conf.read_text()
    assert "2230" not in txt, "the dangerous 2230 point must be gone"
    assert txt.count("[[safe-points]]") == 4
    assert "frequency = 1500" in txt and "frequency = 2000" in txt


def test_apply_gpu_strips_commented_safepoints(helper):
    helper._test_conf.write_text("[load-target]\nupper = 0.95\nlower = 0.7\n"
                                 "[[safe-points]]\nfrequency = 350        # MHz\nvoltage = 700          # mV\n")
    assert helper.apply_gpu(350, 700, 2200, 1000)
    txt = helper._test_conf.read_text()
    assert txt.count("[[safe-points]]") == 4


def test_apply_gpu_reloads_governor_gently(helper):
    helper._test_conf.write_text("[[safe-points]]\nfrequency = 350\nvoltage = 700\n"
                                 "[[safe-points]]\nfrequency = 2000\nvoltage = 1000\n")
    helper.apply_gpu(350, 700, 2000, 1000)
    joined = " | ".join(helper._test_calls)
    assert "stop cyan-skillfish-governor" in joined and "start cyan-skillfish-governor" in joined
    assert "restart" not in joined, "must use stop -> settle -> start, not an abrupt restart"


# ---------- gov_mode: Balanced / Performance switch ----------

def _stock(helper):
    helper._test_conf.write_text("[timing.intervals]\nsample = 2000\nadjust = 20_000\nfinetune = 1_000_000_000\n"
                                 "[timing.ramp-rates]\nnormal = 1\nburst = 200\n[timing]\nburst-samples = 48\n"
                                 "[frequency-thresholds]\nadjust = 100\nfinetune = 10\n"
                                 "[load-target]\nupper = 0.95\nlower = 0.7\n"
                                 "[[safe-points]]\nfrequency = 350\nvoltage = 700\n"
                                 "[[safe-points]]\nfrequency = 1500\nvoltage = 900\n"
                                 "[[safe-points]]\nfrequency = 2000\nvoltage = 1000\n"
                                 "[[safe-points]]\nfrequency = 2200\nvoltage = 1000\n")


def test_mode_roundtrip_preserves_safepoints(helper):
    _stock(helper)
    assert helper.current_gov_mode() == "balanced"
    assert helper.gov_mode("performance")
    txt = helper._test_conf.read_text()
    assert "upper = 0.20" in txt and helper.current_gov_mode() == "performance"
    assert txt.count("[[safe-points]]") == 4, "performance keeps the user's curve"
    assert helper.gov_mode("balanced")
    txt = helper._test_conf.read_text()
    assert "upper = 0.95" in txt and helper.current_gov_mode() == "balanced"
    assert txt.count("[[safe-points]]") == 4


# ---------- test_cpu: crash-safe persistence ----------

def _cpu_fixture(helper, tmp_path, monkeypatch):
    conf = tmp_path / "bc250-smu-oc.conf"
    conf.write_text("[overclock]\nfrequency = 3700\nscale = -16\nmax_temperature = 85\n")
    monkeypatch.setattr(helper, "OC_CONF", str(conf))
    monkeypatch.setattr(helper, "get", lambda: {"cpu": {"frequency": 3700, "scale": -16, "max_temperature": 85}})
    return conf


def test_cpu_bench_runs_with_last_known_good_on_disk(helper, tmp_path, monkeypatch):
    """A hard freeze mid-bench must reboot into the OLD config, not the candidate."""
    conf = _cpu_fixture(helper, tmp_path, monkeypatch)
    seen = {}
    def fake_bench(*a, **k):
        seen["conf_during_bench"] = conf.read_text()
        return {"ok": True, "min_mhz": 3900, "score": 1, "unit": "x", "temp": 60}
    monkeypatch.setattr(helper, "bench_cpu", fake_bench)
    r = helper.test_cpu(3900, -24, 85)
    assert r["ok"]
    assert "frequency = 3700" in seen["conf_during_bench"], "candidate must NOT be persisted during the bench"
    assert "frequency = 3900" in conf.read_text(), "candidate persisted only after passing"


def test_cpu_failed_bench_keeps_old_config(helper, tmp_path, monkeypatch):
    conf = _cpu_fixture(helper, tmp_path, monkeypatch)
    monkeypatch.setattr(helper, "bench_cpu", lambda *a, **k: {"ok": True, "min_mhz": 3000})
    r = helper.test_cpu(4000, -36, 85)
    assert not r["ok"]
    assert "frequency = 3700" in conf.read_text()


def test_safepoints_fallback_is_the_safe_curve(helper):
    helper._test_conf.write_text("")  # unreadable / empty config
    pts = helper._gov_safepoints()
    assert pts == [(350, 700), (1500, 900), (2000, 1000), (2200, 1000)]
    assert max(f for f, _ in pts) <= 2200, "fallback must never exceed the validated 2200 MHz"

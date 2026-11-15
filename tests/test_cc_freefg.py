"""Control Center, FreeFG: the launcher-entry edits that keep GE-Proton's own
OptiScaler out of a FreeFG game, and the pinned release.

GE-Proton reads PROTON_USE_OPTISCALER / PROTON_FSR4_UPGRADE with nonzero(): 0
switches its placement off, and the game's entry wins over the launcher-wide
flatpak override our FSR 4 switch writes. These are the pure parts of
sfcc/freefg.py; the parts that call FreeFG were tried on bc250-dev.
"""
import importlib.util
import json
import pathlib

FREEFG = (pathlib.Path(__file__).resolve().parents[1]
          / "apps" / "control-center" / "sfcc" / "freefg.py")


def _m():
    spec = importlib.util.spec_from_file_location("cc_freefg", FREEFG)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ZEROS = [{"key": "PROTON_USE_OPTISCALER", "value": "0"}, {"key": "PROTON_FSR4_UPGRADE", "value": "0"}]


def test_heroic_empty_gets_the_two_zeros():
    assert _m().heroic_neutral([]) == ZEROS
    assert _m().heroic_neutral(None) == ZEROS


def test_heroic_existing_ge_values_are_replaced_others_kept_in_order():
    m = _m()
    env = [{"key": "A", "value": "1"}, {"key": "PROTON_FSR4_UPGRADE", "value": "1"}, {"key": "B", "value": "x"}]
    assert m.heroic_neutral(env) == [{"key": "A", "value": "1"}, {"key": "B", "value": "x"}] + ZEROS


def test_heroic_restore_puts_back_what_was_there():
    m = _m()
    original = [{"key": "PROTON_FSR4_UPGRADE", "value": "1"}]
    now = [{"key": "WINEDLLOVERRIDES", "value": "dxgi=n,b"}] + ZEROS
    assert m.heroic_restored(now, original) == [{"key": "WINEDLLOVERRIDES", "value": "dxgi=n,b"},
                                                {"key": "PROTON_FSR4_UPGRADE", "value": "1"}]
    assert m.heroic_restored(ZEROS, []) == []


def test_steam_empty_options():
    assert _m().steam_neutral("") == "PROTON_USE_OPTISCALER=0 PROTON_FSR4_UPGRADE=0 %command%"
    assert _m().steam_neutral(None) == "PROTON_USE_OPTISCALER=0 PROTON_FSR4_UPGRADE=0 %command%"


def test_steam_game_arguments_only_go_after_command():
    assert _m().steam_neutral("-dx12") == "PROTON_USE_OPTISCALER=0 PROTON_FSR4_UPGRADE=0 %command% -dx12"


def test_steam_existing_assignments_are_replaced_others_kept():
    got = _m().steam_neutral("DXVK_HUD=1 PROTON_FSR4_UPGRADE=1 %command% -skipintro")
    assert got == "DXVK_HUD=1 PROTON_USE_OPTISCALER=0 PROTON_FSR4_UPGRADE=0 %command% -skipintro"


def test_steam_neutral_is_stable():
    m = _m()
    once = m.steam_neutral("%command%")
    assert m.steam_neutral(once) == once


def test_installed_reads_the_state_file(tmp_path):
    m = _m()
    exe = tmp_path / "Game.exe"
    exe.write_text("")
    assert not m.installed(exe)
    st = tmp_path / ".bc250-xefg-experimental"
    st.mkdir()
    (st / "state.json").write_text(json.dumps({"status": "installed"}))
    assert m.installed(exe)
    (st / "state.json").write_text(json.dumps({"status": "restored"}))
    assert not m.installed(exe)


def test_the_release_is_pinned_with_its_hash():
    m = _m()
    assert m.VERSION == "1.4.0"
    assert len(m.SHA256) == 64 and int(m.SHA256, 16) >= 0
    assert m.URL.endswith("/v1.4.0/freefg-1.4.0.zip")
    # never NVIDIA's DLL, never HelixSR's upscalers (they crash at load on our Proton)
    assert m.INSTALL_ARGS[:4] == ["--upscaler", "fsr4", "--dlss-helper", "no"]


def test_verdict_short():
    m = _m()
    assert m.verdict_short("Automatic (no recipe): detected DLSS → OptiFG input") == "Automatic (no recipe)"
    assert m.verdict_short("Not supported: This game has no upscaler") == "Not supported"
    assert m.verdict_short("Verified on BC-250: Cyberpunk 2077 (2.5 benchmark)") == "Verified on BC-250"


def _archive(root, name, record):
    d = root / name
    d.mkdir()
    (d / "state.json").write_text(json.dumps(record))
    (d / "backup.bin").write_text("x")
    return d


def test_prune_deletes_only_archives_that_hold_nothing_more(tmp_path):
    m = _m()
    exe = tmp_path / "Game.exe"
    exe.write_text("")
    cur = tmp_path / ".bc250-xefg-experimental"
    cur.mkdir()
    (cur / "state.json").write_text(json.dumps({"status": "restored"}))
    done = _archive(tmp_path, ".bc250-xefg-experimental-restored-0123456789ab",
                    {"status": "restored", "game_settings": [{"status": "restored"}]})
    left = _archive(tmp_path, ".bc250-xefg-experimental-restored-aaaaaaaaaaaa",
                    {"status": "restored", "game_settings": [{"status": "left", "left": {"k": "kept"}}]})
    damaged = _archive(tmp_path, ".bc250-xefg-experimental-restored-bbbbbbbbbbbb",
                       {"status": "restored", "left_installed": [{"path": "a.dll", "sha256": "0"}]})
    unreadable = tmp_path / ".bc250-xefg-experimental-restored-cccccccccccc"
    unreadable.mkdir()
    other = _archive(tmp_path, ".bc250-xefg-experimental-restored-mine", {"status": "restored"})
    deleted, kept = m.prune_archives(exe)
    assert deleted == [done.name] and not done.exists()
    assert kept == [left.name, damaged.name, unreadable.name]
    assert left.exists() and damaged.exists() and unreadable.exists()
    assert other.exists() and cur.exists()          # not an archive name / the live record


def test_archive_done_with():
    m = _m()
    assert m.archive_done_with({"status": "restored"})
    assert not m.archive_done_with({"status": "installed"})
    assert not m.archive_done_with({"status": "restored", "kept_changed": ["a.ini"]})
    assert not m.archive_done_with({"status": "restored", "game_settings": [{"status": "pending"}]})
    assert not m.archive_done_with(None)

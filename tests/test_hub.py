"""Tests for the Hub's pure logic (no display needed — nothing is instantiated)."""
import importlib.machinery
import importlib.util
import pathlib

import pytest

HUB = pathlib.Path(__file__).resolve().parents[1] / "apps" / "hub" / "skillfish-hub"


@pytest.fixture(scope="module")
def hub():
    pytest.importorskip("PyQt6.QtWidgets")  # import-only; no QApplication created
    loader = importlib.machinery.SourceFileLoader("hub_mod", str(HUB))
    spec = importlib.util.spec_from_loader("hub_mod", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


def test_top_category_routing(hub):
    assert hub.top_category_of(["ActionGame", "Game"]) == "Game"
    assert hub.top_category_of(["IDE", "Development"]) == "Development"
    # routing keys off the top-level freedesktop category (AppStream always
    # includes it); a bare sub-category falls back to Utility
    assert hub.top_category_of(["IDE"]) == "Utility"
    assert hub.top_category_of([]) == "Utility"
    assert hub.top_category_of(["NoSuchCategory"]) == "Utility"


def test_subcats_are_unique_per_category(hub):
    for cat, subs in hub.SUBCATS.items():
        ids = [s for s, _n in subs]
        assert len(ids) == len(set(ids)), f"duplicate sub-category id in {cat}"


def test_app_defaults_are_safe(hub):
    a = hub.App("apt", "x.y", "pkg", "Name")
    assert a.rating == 0.0 and a.rating_n == 0
    assert a.screens == [] and a.cats == []
    assert a.odrs_id == "x.y"  # falls back to the appid for ratings lookup


# --------------------------------------------------------------------------
# The detached transaction, firmware, and the rules that must not drift back.
# --------------------------------------------------------------------------
HELPER_SRC = pathlib.Path(__file__).resolve().parents[1] / "apps" / "hub" / "skillfish-hub-helper"


def test_updates_always_have_five_fields(hub, monkeypatch):
    """The page unpacks five fields. Four would raise on the first row.

    This is the contract between Catalog.updates() and the updates page: the
    fifth field is the firmware device id, empty for everything else. It is
    cheap to break by adding a source and forgetting the fifth value, and the
    breakage shows up as an empty page rather than as an error.
    """
    monkeypatch.setattr(hub, "have", lambda b: b == "apt-get")
    monkeypatch.setattr(hub, "run", lambda cmd, t=120: (
        0, "Inst libnss3 [2:3.126-1] (2:3.127-1 Debian:unstable)\n", ""))
    righe = hub.Catalog().updates()
    assert righe and all(len(r) == 5 for r in righe)
    assert righe[0][0] == "apt" and righe[0][4] == ""


def test_firmware_carries_the_device_id(hub, monkeypatch):
    """Without the id fwupd would not know which device to update."""
    payload = ('{"Devices":[{"Name":"System Firmware","DeviceId":"abc123",'
               '"Version":"1.0","Releases":[{"Version":"1.1"}]}]}')
    monkeypatch.setattr(hub, "have", lambda b: b == "fwupdmgr")
    monkeypatch.setattr(hub, "run", lambda cmd, t=120: (0, payload, ""))
    (sorgente, nome, vecchia, nuova, ident), = hub.Catalog.firmware()
    assert sorgente == "firmware" and ident == "abc123"
    assert (vecchia, nuova) == ("1.0", "1.1")


def test_firmware_survives_rubbish(hub, monkeypatch):
    """fwupdmgr exits non-zero when there is nothing to do: not an error.

    It also prints nothing useful in that case, and a JSON parser handed an
    empty string raises. A software centre that refuses to open its updates
    page because a firmware daemon had nothing to say would be worse than one
    without firmware support at all.
    """
    monkeypatch.setattr(hub, "have", lambda b: b == "fwupdmgr")
    for uscita in ("", "not json at all", "{}", '{"Devices":null}'):
        monkeypatch.setattr(hub, "run", lambda cmd, t=120, u=uscita: (2, u, ""))
        assert hub.Catalog.firmware() == []


def test_update_all_leaves_firmware_alone(hub):
    """«Update all» must never carry firmware with it.

    A wrong package is reinstalled; a wrong firmware is carried to a repair
    shop. Firmware goes one device at a time, from its own button, after an
    explicit yes.
    """
    import inspect
    sorgente = inspect.getsource(hub.Hub.update_all)
    assert '"aggiorna"' in sorgente
    assert "firmware" not in sorgente


def test_transaction_state_is_readable_without_root(hub, tmp_path, monkeypatch):
    """The window is not root: it must be able to read the state, and cope
    with the file not being there at all (no transaction has ever run)."""
    monkeypatch.setattr(hub, "TX_JSON", str(tmp_path / "assente.json"))
    assert hub.tx_stato() == {} and hub.tx_in_corso() is False
    p = tmp_path / "tx.json"
    p.write_text('{"stato":"in-corso","rc":null,"azione":"aggiorna"}')
    monkeypatch.setattr(hub, "TX_JSON", str(p))
    assert hub.tx_in_corso() is True
    p.write_text('{"stato":"in-co')            # caught mid-write: must not raise
    assert hub.tx_stato() == {}


def test_helper_starts_the_work_detached():
    """The whole point: the work must not be a child of the window.

    If this ever goes back to running apt as a child process, the first upgrade
    that replaces Qt kills it halfway and leaves dpkg to be repaired by hand.
    """
    testo = HELPER_SRC.read_text(encoding="utf-8")
    assert "systemd-run" in testo
    assert "setsid nohup" in testo          # il ripiego senza systemd
    assert "--force-confold" in testo       # apt non deve fermarsi a chiedere
    assert "Dpkg::Use-Pty=0" in testo


def test_counting_stands_down_while_a_transaction_runs():
    """The daily count must not fight the real transaction for apt's lock."""
    testo = HELPER_SRC.read_text(encoding="utf-8")
    conta = testo.split("\n  conta)", 1)[1]
    assert "tx_attiva" in conta.split("apt-get update", 1)[0]

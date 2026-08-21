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


# --------------------------------------------------------------------------
# Opening a file the way Discover did: .deb, Flatpak refs, appstream:// links.
# --------------------------------------------------------------------------
def test_target_needs_a_real_file(hub, tmp_path):
    """A path that is not a real file must never reach the root helper.

    The helper runs as root through pkexec. A directory, a device node or a
    made-up path has no business being handed to apt, and the cheapest place to
    stop it is before it is even offered to the user.
    """
    finto = tmp_path / "inventato.deb"
    assert hub.bersaglio([str(finto)]) is None
    cartella = tmp_path / "cartella.deb"
    cartella.mkdir()
    assert hub.bersaglio([str(cartella)]) is None
    vero = tmp_path / "vero.deb"
    vero.write_bytes(b"!<arch>\n")
    assert hub.bersaglio([str(vero)]) == ("deb", str(vero))


def test_target_understands_what_kde_actually_passes(hub, tmp_path):
    """KDE hands over a file:// URL, and percent-encodes the spaces in it."""
    f = tmp_path / "un pacchetto.flatpakref"
    f.write_text("[Flatpak Ref]\nName=org.example.App\n")
    url = "file://" + str(f).replace(" ", "%20")
    assert hub.bersaglio([url]) == ("flatpakref", str(f))


def test_target_reads_the_two_schemes_discover_owned(hub):
    """appstream:// and apt:// were Discover's; nothing else answers them."""
    assert hub.bersaglio(["appstream://org.kde.kate"]) == ("app", "org.kde.kate")
    assert hub.bersaglio(["apt://vlc"]) == ("app", "vlc")
    # ⚠️ Options are not targets. Passed one, the Hub must open normally rather
    # than treat "--something" as a package name.
    assert hub.bersaglio(["--qwindowgeometry"]) is None
    assert hub.bersaglio([]) is None


def test_target_ignores_files_we_do_not_handle(hub, tmp_path):
    """A .txt is not ours: no dialog, no transaction, just a normal start."""
    f = tmp_path / "note.txt"
    f.write_text("ciao")
    assert hub.bersaglio([str(f)]) is None


def test_flatpakref_description_names_the_app_and_its_origin(hub, tmp_path):
    """The question 'do you want to install this?' needs a real answer.

    Asking over a file name is not asking: it is making the user press Yes.
    """
    f = tmp_path / "app.flatpakref"
    f.write_text("[Flatpak Ref]\nName=org.example.App\nUrl=https://example.org/repo\n")
    nome, righe = hub.descrivi("flatpakref", str(f))
    assert nome == "org.example.App"
    assert any("example.org" in str(v) for _k, v in righe)


def test_the_warning_says_it_is_unsigned():
    """A file from outside is not a package from our repositories.

    None of our keys signed it, and the person installing it is trusting
    whoever gave it to them. That sentence is the whole difference between
    installing from the Hub and installing something found lying around.
    """
    import pathlib
    hubsrc = (pathlib.Path(__file__).resolve().parents[1]
              / "apps" / "hub" / "skillfish-hub").read_text(encoding="utf-8")
    assert "def avviso_bersaglio" in hubsrc
    assert "avviso_bersaglio(tipo)" in hubsrc          # e viene mostrato davvero


def test_helper_checks_every_path_it_is_given():
    """Each file action must validate the path before touching it."""
    testo = HELPER_SRC.read_text(encoding="utf-8")
    corpo = testo.split("  tx-run)", 1)[1].split("  conta)", 1)[0]
    for azione in ("deb)", "flatpakref)", "flatpakrepo)", "flatpakbundle)"):
        pezzo = corpo.split("      " + azione, 1)[1].split(";;", 1)[0]
        assert "percorso_sicuro" in pezzo, azione

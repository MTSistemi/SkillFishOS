"""Tests for the fan daemon's decisions. No hardware, no root, no PWM written.

This is the most safety-critical pure logic in the project after the GPU
governor: get it wrong and a board cooks. The tests are therefore written the
way the code is -- around the ways it can be wrong, not the ways it works.

The four that matter:

* emergency must not go through the curve at all. A curve whose last point is
  70% would otherwise cap the fan at 70% while the chip passes 90 C.
* the minimum must survive everything. Many 3-wire fans stop below a threshold
  and do not restart until the PWM climbs well past it, so "0% because it is
  cold" is a trap that ends with a stopped fan and no tachometer.
* anticipation must only ever add. A falling temperature is not a reason to
  slow down right now; that is the curve's job, with hysteresis.
* an unknown game must be treated as heavy. Being wrong upwards costs one
  minute of fan noise once; being wrong downwards costs heat exactly when the
  most heat is arriving.
"""
import importlib.machinery
import importlib.util
import pathlib
import sys
import time

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
DAEMON = ROOT / "apps" / "fan" / "skillfish-fand"
SHARED = ROOT / "system" / "usr" / "share" / "skillfish"

# The daemon does sys.path.insert(0, "/usr/share/skillfish") and imports hwmon
# from there. On a CI runner that directory does not exist -- and it should not
# have to: a test that only passes on a machine with the package installed is
# testing the machine, not the code. sys.path.insert only prepends, so adding
# the repo copy here lets the import fall through to it.
if str(SHARED) not in sys.path:
    sys.path.append(str(SHARED))


@pytest.fixture()
def fand(tmp_path, monkeypatch):
    loader = importlib.machinery.SourceFileLoader("skillfish_fand", str(DAEMON))
    spec = importlib.util.spec_from_loader("skillfish_fand", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    # nothing in the tests may touch the real system
    monkeypatch.setattr(mod, "CONF", str(tmp_path / "ventola.json"))
    monkeypatch.setattr(mod, "STATO", str(tmp_path / "stato.json"))
    monkeypatch.setattr(mod, "ORIGINALE", str(tmp_path / "originale.json"))
    monkeypatch.setattr(mod, "APPRESI", str(tmp_path / "appresi.json"))
    monkeypatch.setattr(mod, "CATALOGO", str(tmp_path / "catalogo.json"))
    return mod


CURVE = [(40, 30), (55, 40), (65, 60), (75, 85), (85, 100)]


def test_curve_interpolates_between_points(fand):
    assert fand.interpola(CURVE, 40) == 30
    assert fand.interpola(CURVE, 55) == 40
    assert fand.interpola(CURVE, 60) == 50      # halfway between 40 and 60
    assert fand.interpola(CURVE, 85) == 100


def test_curve_is_never_extrapolated(fand):
    """Below the first point and above the last, the curve holds.

    Extrapolating downwards would invent fan speeds slower than anything the
    user drew.
    """
    assert fand.interpola(CURVE, -20) == 30
    assert fand.interpola(CURVE, 200) == 100


def test_empty_curve_means_full_speed(fand):
    assert fand.interpola([], 30) == 100


def demone(fand, **conf):
    import io as _io
    import json as _json
    base = {"attivo": True, "pwm": "test:pwm1", "sorgente": ["test:temp1"],
            "curva": [list(p) for p in CURVE], "minimo": 30, "isteresi": 3,
            "emergenza": 88}
    base.update(conf)
    with _io.open(fand.CONF, "w", encoding="utf-8") as f:
        f.write(_json.dumps(base))
    return fand.Demone()


def test_emergency_ignores_the_curve(fand):
    """A curve that tops out at 70% must not cap the fan during an emergency."""
    d = demone(fand, curva=[[40, 30], [80, 70]], emergenza=88)
    assert d.decidi(90.0, time.time(), False) == 100.0
    assert "emergency" in d.motivo


def test_no_temperature_means_full_speed(fand):
    """The chip vanished, or every source went implausible.

    Without this the fan would sit on the last value written, forever.
    """
    d = demone(fand)
    assert d.decidi(None, time.time(), False) == 100.0


def test_minimum_wins_over_a_cold_curve(fand):
    d = demone(fand, curva=[[40, 0], [80, 100]], minimo=35)
    assert d.decidi(20.0, time.time(), False) == 35


def test_minimum_cannot_be_configured_below_the_floor(fand):
    """A fan that stops does not restart on its own. 0% is not an option."""
    d = demone(fand, minimo=0)
    assert d.conf["minimo"] == fand.SOGLIA_MINIMA


def test_anticipation_raises_the_fan_before_the_heat(fand):
    d = demone(fand)
    now = time.time()
    # two degrees per second for six seconds: a game just started
    d.storia_t = [(now - 6 + i, 50.0 + 2.0 * i) for i in range(7)]
    calmo = fand.interpola(CURVE, 62.0)
    assert d.decidi(62.0, now, False) > calmo
    assert "anticipating" in d.motivo


def test_anticipation_never_lowers_the_fan(fand):
    """Falling fast is not a reason to slow down now."""
    d = demone(fand, isteresi=0)
    now = time.time()
    d.storia_t = [(now - 6 + i, 80.0 - 3.0 * i) for i in range(7)]
    assert d.decidi(62.0, now, False) == pytest.approx(fand.interpola(CURVE, 62.0))


def test_power_slope_adds_anticipation_on_its_own(fand):
    """Watts rise before degrees do: they are the cause, not the effect."""
    d = demone(fand)
    now = time.time()
    d.storia_t = [(now - 6 + i, 62.0) for i in range(7)]        # flat
    d.storia_w = [(now - 6 + i, 20.0 + 8.0 * i) for i in range(7)]  # 8 W/s
    assert d.decidi(62.0, now, False) > fand.interpola(CURVE, 62.0)


def test_hysteresis_holds_the_fan_through_sensor_jitter(fand):
    d = demone(fand, isteresi=5)
    now = time.time()
    d.ultimo_duty = fand.interpola(CURVE, 70.0)
    # half a degree down is jitter, not cooling
    assert d.decidi(69.5, now, False) == d.ultimo_duty
    # ten degrees down is real
    assert d.decidi(60.0, now, False) < d.ultimo_duty


def test_precooling_lifts_the_floor_but_emergency_still_wins(fand):
    d = demone(fand)
    now = time.time()
    duty = d.decidi(45.0, now, True)
    assert duty >= d.conf["predittivo"]["preraffredda"]
    assert d.decidi(95.0, now, True) == 100.0


def test_a_broken_config_falls_back_instead_of_dying(fand):
    """The daemon is also the emergency: refusing to start is the worst option."""
    import io as _io
    with _io.open(fand.CONF, "w", encoding="utf-8") as f:
        f.write("{ this is not json")
    c = fand.carica_conf()
    assert c["attivo"] is False          # hands the fan back to the chip
    assert c["curva"]


def test_unknown_game_is_treated_as_heavy(fand):
    g = fand.Giochi(fand.CONF_PREDEFINITA)
    assert g.peso("Some Game Nobody Measured Yet") is True


def test_a_measured_light_game_stops_pre_cooling(fand):
    """This is the Cyberpunk / Roblox distinction, and it is measured, not guessed."""
    g = fand.Giochi(fand.CONF_PREDEFINITA)
    g.appresi = {"Roblox": {"picco_watt": 18.0},
                 "Cyberpunk 2077": {"picco_watt": 62.0}}
    assert g.peso("Roblox") is False
    assert g.peso("Cyberpunk 2077") is True


def test_measurement_beats_the_shipped_catalogue(fand):
    """What this machine actually did outranks what we guessed for everyone."""
    g = fand.Giochi(fand.CONF_PREDEFINITA)
    g.catalogo = {"Some Title": {"pesante": True}}
    g.appresi = {"Some Title": {"picco_watt": 12.0}}
    assert g.peso("Some Title") is False


def _fake_pwm(fand, tmp_path, monkeypatch, value=94, mode=1):
    """A pwm/pwm_enable pair on disk, standing in for /sys."""
    pwm = tmp_path / "pwm2"
    pwm.write_text(str(value))
    (tmp_path / "pwm2_enable").write_text(str(mode))

    class FakePwm:
        chiave = "test.0:pwm2"
        percorso = str(pwm)

    # patched on the module object, not by dotted name: the daemon is loaded
    # with exec_module and never lands in sys.modules, so a string target
    # cannot find it.
    monkeypatch.setattr(fand.hwmon, "elenca", lambda: ([], [FakePwm()]))
    return pwm


def test_the_firmware_value_is_captured_once_per_boot(fand, tmp_path, monkeypatch):
    """Found by testing, not by reading: this one bit for real.

    After a SIGKILL systemd restarts the daemon, which re-reads the PWM and
    finds OUR value in it -- and records that as "the original". Restart after
    restart the firmware's value is lost, and "put things back" comes to mean
    "put our own value back". Worse for the MODE: the chip may have been
    governing the fan itself (mode 2), and we would leave it on mode 1 with
    nobody in charge, which is a fan nailed to a fixed number forever.
    """
    _fake_pwm(fand, tmp_path, monkeypatch, value=94, mode=2)

    primo = fand.Uscita("test.0:pwm2")
    assert primo.prendi()
    assert primo.originale["valore"] == 94
    assert primo.originale["modo"] == 2
    primo.scrivi(100)                       # now the file holds 255, not 94

    # the daemon is killed and restarted: a second Uscita over the same output
    secondo = fand.Uscita("test.0:pwm2")
    assert secondo.prendi()
    assert secondo.originale["valore"] == 94, "recorded our own value as the original"
    assert secondo.originale["modo"] == 2

    secondo.rilascia()
    assert (tmp_path / "pwm2").read_text() == "94"
    assert (tmp_path / "pwm2_enable").read_text() == "2"


def test_restore_from_outside_survives_a_dead_process(fand, tmp_path, monkeypatch):
    """ExecStopPost is the only path that runs after a SIGKILL."""
    _fake_pwm(fand, tmp_path, monkeypatch, value=94, mode=2)
    u = fand.Uscita("test.0:pwm2")
    u.prendi()
    u.scrivi(100)
    assert (tmp_path / "pwm2").read_text() == "255"

    # the process is gone; only the file is left
    fand.ripristina_da_fuori()
    assert (tmp_path / "pwm2").read_text() == "94"
    assert (tmp_path / "pwm2_enable").read_text() == "2"


def test_value_is_restored_before_the_mode(fand, tmp_path, monkeypatch):
    """Order matters: mode first would let the chip apply OUR value for an instant."""
    _fake_pwm(fand, tmp_path, monkeypatch, value=94, mode=2)
    u = fand.Uscita("test.0:pwm2")
    u.prendi()
    u.scrivi(100)
    ordine = []
    vero = fand.Uscita._scrivi

    def spia(percorso, valore):
        ordine.append(percorso.split("/")[-1])
        return vero(percorso, valore)

    monkeypatch.setattr(fand.Uscita, "_scrivi", staticmethod(spia))
    u.rilascia()
    assert ordine == ["pwm2", "pwm2_enable"]


@pytest.mark.parametrize("cmdline,expected", [
    ("/home/u/.local/share/Steam/steamapps/common/Cyberpunk 2077/bin/x64/game.exe",
     "Cyberpunk 2077"),
    # the Flatpak Steam, which is what SkillFishOS actually ships
    ("/home/u/.var/app/com.valvesoftware.Steam/.local/share/Steam/steamapps/"
     "common/Black Myth Wukong Benchmark Tool/b1.exe",
     "Black Myth Wukong Benchmark Tool"),
    # Proton and the runtimes live in the same folder and are not games
    ("/x/steamapps/common/Proton - Experimental/proton waitforexitandrun", ""),
    ("/x/steamapps/common/SteamLinuxRuntime_sniper/_v2-entry-point", ""),
    ("/usr/bin/firefox", ""),
])
def test_game_name_from_command_line(fand, cmdline, expected):
    assert fand.Giochi._nome_gioco(cmdline) == expected

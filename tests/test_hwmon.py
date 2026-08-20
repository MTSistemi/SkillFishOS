"""Tests for sensor discovery: telling real hwmon channels from invented ones.

Why this matters more than it looks. On the two machines we own, most of what
the Super-I/O chip declares is not real:

* BC-250 (nct6686): 8 fan channels, one reads. 14 voltages, three read --
  +12V and +5V are hardwired to 0.00 there. 7 temperatures, three read.
* Fujitsu D3521-A1 (nct6792): CPUTIN reports 127.5 C while coretemp reports 47.
  AUXTIN1/2/3 report -128. Both are what the chip returns for a pin with
  nothing attached.

A panel that shows those numbers is not merely untidy. If someone attaches a
fan curve to a channel that is a constant, the curve is driven by a number that
never moves: the fan either never spins up or sits at full speed forever.

The hard case is the suspicion rule, and the hard part of it is staying quiet.
A genuinely hot component under load looks a lot like a disconnected pin --
except that it moves. These tests therefore include three cases where the rule
MUST say nothing, because an alarm that cries wolf is one people learn to skip.
"""
import importlib.machinery
import importlib.util
import pathlib

import pytest

MODULE = (pathlib.Path(__file__).resolve().parents[1]
          / "system" / "usr" / "share" / "skillfish" / "hwmon.py")


@pytest.fixture(scope="module")
def hwmon():
    loader = importlib.machinery.SourceFileLoader("skillfish_hwmon", str(MODULE))
    spec = importlib.util.spec_from_loader("skillfish_hwmon", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


def chan(hwmon, label, readings):
    c = hwmon.Canale("test", "test.0", "temp", 1, "/dev/null", label)
    c.campioni = list(readings)
    c.cambia = len(set(c.campioni)) > 1
    c.vero = True
    return c


COOL = [
    ("Core 0", [37.0, 38.0, 37.0, 38.0, 37.0]),
    ("Core 1", [36.0, 37.0, 36.0, 37.0, 36.0]),
    ("GPU", [37.0, 37.0, 38.0, 37.0, 37.0]),
]


@pytest.mark.parametrize("name,extra,expected", [
    # A disconnected pin: hot and perfectly still among cool sensors.
    ("disconnected pin",
     [("SYSTIN", [80.0] * 5)],
     {"SYSTIN"}),

    # The one that must NOT fire: a VRM genuinely under load. Same temperature
    # range as the broken pin above, but it moves.
    ("hot but moving",
     [("VRM", [78.0, 79.0, 81.0, 80.0, 82.0])],
     set()),

    # Still, but only ten degrees above the rest: a saturated passive
    # heatsink is a real thing and must not be flagged.
    ("still but close",
     [("Chipset", [48.0] * 5)],
     set()),

    # Two broken pins at once: the rule uses the median precisely so that a
    # second bad channel cannot drag the reference up and hide the first.
    ("two broken pins",
     [("SYSTIN", [80.0] * 5), ("AUXTIN0", [75.0] * 5)],
     {"SYSTIN", "AUXTIN0"}),
])
def test_suspicion_rule(hwmon, name, extra, expected):
    channels = [chan(hwmon, n, r) for n, r in extra + COOL]
    hwmon._segna_sospetti(channels)
    assert {c.etichetta_driver for c in channels if c.motivo} == expected


def test_real_bc250_readings_are_all_accepted(hwmon):
    """The BC-250's real temperatures sit within a few degrees of each other.

    This is the negative test that the live run on the board cannot provide:
    there, the rule could not fire even if it were wrong.
    """
    channels = [chan(hwmon, n, r) for n, r in [
        ("Composite", [51.9] * 5),
        ("edge", [47.0, 48.0, 47.0, 49.0, 48.0]),
        ("CPU", [51.0, 51.0, 50.0, 51.0, 51.0]),
        ("System", [49.5] * 5),
        ("VRM MOS", [49.5] * 5),
        ("Tctl", [51.0, 51.1, 51.0, 51.2, 51.0]),
    ]]
    hwmon._segna_sospetti(channels)
    assert [c.etichetta_driver for c in channels if c.motivo] == []


def test_too_few_sensors_to_have_an_opinion(hwmon):
    """With two temperatures there is no "rest of the field" to compare against."""
    channels = [chan(hwmon, "SYSTIN", [80.0] * 5),
                chan(hwmon, "Core 0", [37.0, 38.0, 37.0, 38.0, 37.0])]
    hwmon._segna_sospetti(channels)
    assert [c.etichetta_driver for c in channels if c.motivo] == []


def test_channel_key_is_stable_across_reboots(hwmon):
    """hwmon3 can be the Nuvoton today and the NVMe tomorrow.

    User-written labels are stored against the key, so it has to come from the
    device link (nct6687.2592, 0000:01:00.0) and not from the hwmon number.
    """
    c = hwmon.Canale("nct6686", "nct6687.2592", "fan", 2, "/dev/null", "Pump Fan")
    assert c.chiave == "nct6687.2592:fan2"


def test_label_never_falls_back_to_nothing(hwmon):
    """The Fujitsu's voltages have no driver label at all: in0..in14 and that is it.

    An unnamed row in a panel is worse than an ugly name, so the fallback chain
    is user label, then driver label, then the raw channel name.
    """
    unnamed = hwmon.Canale("nct6792", "nct6775.2576", "in", 0, "/dev/null", "")
    assert unnamed.etichetta({}) == "in0"
    assert unnamed.etichetta({"nct6775.2576:in0": "+3.3V standby"}) == "+3.3V standby"

    named = hwmon.Canale("nct6686", "nct6687.2592", "in", 2, "/dev/null", "+3.3V")
    assert named.etichetta({}) == "+3.3V"
    assert named.etichetta({"nct6687.2592:in2": "Rail 3V3"}) == "Rail 3V3"

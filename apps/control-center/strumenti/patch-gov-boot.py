#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Issue #79: the Governor checkbox showed the session and never the boot state.

Runs ON the build VM, inside ~/sfx-src.

    python3 patch-gov-boot.py [--prova]

⚠️ THE BOOT STATE IS NOT ASKED OF THE DAEMON. The page ticks once a second and
the daemon runs behind pkexec, so gov-get on every frame would mean two
systemctl processes a second for a value that only changes when somebody
clicks the box. It is read directly, unprivileged, and cached for a few
seconds.

⚠️ `systemctl is-enabled` EXITS 1 WHEN THE UNIT IS DISABLED. Deciding on the
exit code would call every disabled unit an error, which is how a campaign
setup died earlier this month under `set -e`. The word it prints decides.

The anchors are exact and the patch refuses to write anything if one of them
does not match.
"""
import io
import os
import sys

PROVA = "--prova" in sys.argv
TUNER = os.path.expanduser("~/sfx-src/apps/control-center/sfcc/pagine/tuner.py")

CAMBI = []


def cambia(vecchio, nuovo, etichetta):
    CAMBI.append((vecchio, nuovo, etichetta))


# ---- the unit name, next to the other module constants
cambia(
    "MV_PER_SCALINO = 6.25          # the SMU voltage step of the CPU undervolt\n",
    "MV_PER_SCALINO = 6.25          # the SMU voltage step of the CPU undervolt\n"
    "GOV_UNIT = \"skillfish-vf-governor.service\"\n",
    "il nome dell'unita' fra le costanti")

# ---- the checkbox learns there is a second state
cambia(
    '''        self.interruttore = QCheckBox("Governor")
        self.interruttore.setToolTip(L("Spento: il clock torna al governor di serie.",
                                       "Off: the clock goes back to the stock governor."))
        self.interruttore.clicked.connect(self._governor_on_off)
''',
    '''        self.interruttore = QCheckBox("Governor")
        self.interruttore.setToolTip(L("Spento: il clock torna al governor di serie.",
                                       "Off: the clock goes back to the stock governor."))
        self.interruttore.clicked.connect(self._governor_on_off)
        # the boot state is re-read on a timer of its own, see _gov_al_boot
        self._gov_boot = None
        self._gov_boot_letto = 0.0
''',
    "la casella tiene anche lo stato al boot")

# ---- how the boot state is read
cambia(
    '''    def _governor_on_off(self, on):
        r = self.demone.cmd(cmd="gov-attiva", on=bool(on))
        if not r.get("ok"):
            self.toast(r.get("err", "?"))
            self.interruttore.setChecked(not on)
''',
    '''    # systemctl is-enabled is a process and this page ticks every second, so
    # the boot state is re-read every few seconds instead of every frame.
    INTERVALLO_BOOT = 5.0

    def _gov_al_boot(self):
        """Whether the governor comes back at the next boot.

        ⚠️ is-enabled exits 1 when the unit is disabled, so the word it prints
        decides and not the return code."""
        adesso = time.time()
        if self._gov_boot is None or adesso - self._gov_boot_letto > self.INTERVALLO_BOOT:
            _, out, _ = sh("systemctl is-enabled " + GOV_UNIT, 10)
            self._gov_boot = out.strip() == "enabled"
            self._gov_boot_letto = adesso
        return self._gov_boot

    def _governor_on_off(self, on):
        r = self.demone.cmd(cmd="gov-attiva", on=bool(on))
        self._gov_boot = None          # the click just changed it: read it again
        if not r.get("ok"):
            self.toast(r.get("err", "?"))
            self.interruttore.setChecked(not on)
''',
    "_gov_al_boot, e il click invalida la cache")

# ---- the box says both states
cambia(
    '''        self.interruttore.blockSignals(True)
        self.interruttore.setChecked(vivo)
        self.interruttore.blockSignals(False)
''',
    '''        al_boot = self._gov_al_boot()
        # ticked only when both halves agree: running now AND coming back. A box
        # that only knew the first half read as "on and staying on" to a user
        # whose governor was about to disappear at the next boot.
        self.interruttore.blockSignals(True)
        self.interruttore.setChecked(vivo and al_boot)
        self.interruttore.blockSignals(False)
        self.interruttore.setToolTip("%s %s" % (
            L("Ora e' acceso.", "It is on now.") if vivo
            else L("Ora e' spento.", "It is off now."),
            L("Al prossimo avvio riparte.", "It comes back at the next boot.") if al_boot
            else L("Al prossimo avvio non riparte.", "It does not come back at the next boot.")))
''',
    "la casella si spunta solo se valgono tutte e due")

testo = io.open(TUNER, encoding="utf-8").read()

esito = 0
for vecchio, nuovo, etichetta in CAMBI:
    quante = testo.count(vecchio)
    stato = "ok" if quante == 1 else "NON TROVATO" if quante == 0 else "%d VOLTE" % quante
    print("[%-11s] %s" % (stato, etichetta))
    if quante != 1:
        esito = 1
        continue
    testo = testo.replace(vecchio, nuovo)

if esito:
    sys.exit("\nqualche ancoraggio non combacia: non ho scritto niente")
if PROVA:
    sys.exit("\n--prova: non ho scritto niente")

io.open(TUNER, "w", encoding="utf-8", newline="\n").write(testo)
import py_compile
py_compile.compile(TUNER, cfile="/tmp/sfx-gov-check.pyc", doraise=True)
os.remove("/tmp/sfx-gov-check.pyc")
print("scritto e compila: %s" % TUNER)

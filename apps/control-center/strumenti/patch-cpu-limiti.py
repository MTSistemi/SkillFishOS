#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Issue #78: the CPU panel offered settings the backend refuses, said nothing,
and left the refused value in the file the boot service reads.

Runs ON the build VM, inside ~/sfx-src.

    python3 patch-cpu-limiti.py [--prova]

⚠️ WHY apply_cpu KEEPS RETURNING A BOOL. Six places call it, and four of them
only branch on success:

    if not apply_cpu(mhz, scale, tmp):

A tuple is always truthy, so changing the signature would send every one of
those down the wrong branch without an error anywhere. The reason travels
through a new apply_cpu_esito(); apply_cpu() stays a thin bool wrapper.

⚠️ WHY THE UNDERVOLT IS CAPPED BELOW THE BACKEND'S OWN FLOOR. bc250_limits.py
allows scale -50. Sent at the stock 3500 MHz it froze the dev board within
seconds and the watchdog had to reboot it. The suggestion sweep in the panel
already stops at -40. The ten steps in between buy nothing and cost a power
cycle, so cpu_limiti() clamps them off.

Every replacement is anchored on exact text and fails loudly if it is not
found, so a half-applied patch is not possible.
"""
import io
import os
import sys

PROVA = "--prova" in sys.argv
RADICE = os.path.expanduser("~/sfx-src")
DEMONE = os.path.join(RADICE, "apps/control-center/skillfish-cc-helper")
TUNER = os.path.join(RADICE, "apps/control-center/sfcc/pagine/tuner.py")


def leggi(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def scrivi(p, testo):
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(testo)


CAMBI = []


def cambia(percorso, vecchio, nuovo, etichetta):
    CAMBI.append((percorso, vecchio, nuovo, etichetta))


# ------------------------------------------------------------------ daemon

D_VECCHIO_APPLY = '''def apply_cpu(mhz, scale, tmp):
    mhz, scale, tmp = int(mhz), int(scale), int(tmp)
    if not (2000 <= mhz <= 4500 and -60 <= scale <= 10 and 50 <= tmp <= 100):
        return False
    _log("CPU: %d MHz, scale %d, limite %d C" % (mhz, scale, tmp))
    _write_cpu_conf(mhz, scale, tmp)
    r = sh("python3 %s/bc250_apply.py --apply %s" % (OC_DIR, OC_CONF))
    return r.returncode == 0
'''

D_NUOVO_APPLY = r'''# The backend is the only authority on what can be applied. bc250_limits.py is
# a plain list of integers next to bc250_apply.py, so it gets read instead of
# guessed: we used to accept 2000-4500 MHz against a floor of 3500, and every
# value below it was offered to the user and then refused without a word.
CPU_LIMITI_RIPIEGO = {"freq_min": 3500, "freq_max": 4500,
                      "scale_min": -50, "scale_max": 0,
                      "temp_min": 0, "temp_max": 100}

# The deepest undervolt we let anything reach. The backend allows -50, but -50
# at the stock clock froze the dev board outright and the suggestion sweep
# already stops at -40. Those ten steps buy nothing and cost a power cycle.
CPU_UV_SICURO = -40

_CPU_LIMITI = None


def cpu_limiti():
    """What bc250_apply.py will actually accept, read once and kept."""
    global _CPU_LIMITI
    if _CPU_LIMITI is not None:
        return _CPU_LIMITI
    lim = dict(CPU_LIMITI_RIPIEGO)
    try:
        for nome, val in re.findall(r"(\w+)\s*=\s*(-?\d+)",
                                    _rd("%s/bc250_limits.py" % OC_DIR)):
            if nome in lim:
                lim[nome] = int(val)
    except OSError:
        # no backend installed: the fallback above is what it shipped with
        pass
    lim["scale_min"] = max(lim["scale_min"], CPU_UV_SICURO)
    _CPU_LIMITI = lim
    return lim


def _cpu_fuori(mhz, scale, tmp):
    """Which knob sits outside the limits, as a code the panel can translate.
    None when everything fits."""
    lim = cpu_limiti()
    for campo, val, lo, hi in (
            ("frequency", mhz, lim["freq_min"], lim["freq_max"]),
            ("scale", scale, lim["scale_min"], lim["scale_max"]),
            ("max_temperature", tmp, lim["temp_min"], lim["temp_max"])):
        if not lo <= val <= hi:
            return {"campo": campo, "min": lo, "max": hi}
    return None


def _ultima_riga(testo):
    righe = [r.strip() for r in (testo or "").splitlines() if r.strip()]
    return righe[-1] if righe else ""


def apply_cpu_esito(mhz, scale, tmp):
    """Apply a CPU setting and say why if it did not go in.

    Returns (ok, reason). The reason is either a dict naming the knob that is
    out of range, which the panel turns into a sentence, or the backend's own
    last line. Plain False told the user nothing and read like a control that
    was not wired up.

    On refusal the previous configuration goes back on disk. This file is what
    bc250-smu-oc.service reads at boot, so a value the backend rejected would
    otherwise arm the next boot to fail as well, silently."""
    mhz, scale, tmp = int(mhz), int(scale), int(tmp)
    fuori = _cpu_fuori(mhz, scale, tmp)
    if fuori:
        return False, fuori
    _log("CPU: %d MHz, scale %d, limite %d C" % (mhz, scale, tmp))
    prima = _cpu_conf()
    _write_cpu_conf(mhz, scale, tmp)
    r = sh("python3 %s/bc250_apply.py --apply %s" % (OC_DIR, OC_CONF))
    if r.returncode == 0:
        return True, ""
    _write_cpu_conf(prima["frequency"], prima["scale"], prima["max_temperature"])
    return False, (_ultima_riga(r.stderr) or _ultima_riga(r.stdout)
                   or "bc250_apply.py failed")


def apply_cpu(mhz, scale, tmp):
    """Bool-only wrapper. Four callers branch on `if not apply_cpu(...)` and a
    tuple is always truthy, so the reason never travels through this name."""
    return apply_cpu_esito(mhz, scale, tmp)[0]


def _esito_cpu(ok, perche):
    """One shape for every CPU reply, so the panel always has something to say."""
    if ok:
        return {"ok": True}
    if isinstance(perche, dict):
        return {"ok": False, "fuori": perche}
    return {"ok": False, "err": perche}
'''

cambia(DEMONE, D_VECCHIO_APPLY, D_NUOVO_APPLY, "limiti veri + motivo + niente conf sporca")

D_VECCHIO_VOL = '''    prev = _cpu_conf()
    ok = apply_cpu(mhz, scale, tmp)
    _write_cpu_conf(prev["frequency"], prev["scale"], prev["max_temperature"])
    return {"ok": ok}
'''

D_NUOVO_VOL = '''    prev = _cpu_conf()
    ok, perche = apply_cpu_esito(mhz, scale, tmp)
    _write_cpu_conf(prev["frequency"], prev["scale"], prev["max_temperature"])
    return _esito_cpu(ok, perche)
'''

cambia(DEMONE, D_VECCHIO_VOL, D_NUOVO_VOL, "cpu_volatile porta il motivo")

D_VECCHIO_CMD = '''    if c == "apply-cpu":
        return {"ok": apply_cpu(req["mhz"], req["scale"], req["temp"])}
    if c == "persist-cpu":
        ok = apply_cpu(req["mhz"], req["scale"], req["temp"])
        persist_cpu()
        return {"ok": ok}
'''

D_NUOVO_CMD = '''    if c == "apply-cpu":
        return _esito_cpu(*apply_cpu_esito(req["mhz"], req["scale"], req["temp"]))
    if c == "cpu-limits":
        return {"ok": True, "data": cpu_limiti()}
    if c == "persist-cpu":
        ok, perche = apply_cpu_esito(req["mhz"], req["scale"], req["temp"])
        # a setting the backend refused must not be armed for the next boot
        if ok:
            persist_cpu()
        return _esito_cpu(ok, perche)
'''

cambia(DEMONE, D_VECCHIO_CMD, D_NUOVO_CMD, "apply/persist rispondono col motivo, e cpu-limits")

# ------------------------------------------------------------------- panel

T_VECCHIO_MANOPOLE = '''        self.cf = Manopola(2000, 4500, cfg.get("frequency", 3500), "MHz")
        self.cs = Manopola(-60, 0, cfg.get("scale", 0), "", mostra=lambda s: ("−%.0f mV" % (-s * MV_PER_SCALINO)) if s else "0 mV")
        self.ct = Manopola(60, 95, cfg.get("max_temperature", 85), "°C")
'''

T_NUOVO_MANOPOLE = '''        lim = self._limiti_cpu()
        self.cf = Manopola(lim["freq_min"], lim["freq_max"], cfg.get("frequency", 3500), "MHz")
        self.cs = Manopola(lim["scale_min"], lim["scale_max"], cfg.get("scale", 0), "", mostra=lambda s: ("−%.0f mV" % (-s * MV_PER_SCALINO)) if s else "0 mV")
        self.ct = Manopola(max(60, lim["temp_min"]), min(95, lim["temp_max"]), cfg.get("max_temperature", 85), "°C")
'''

cambia(TUNER, T_VECCHIO_MANOPOLE, T_NUOVO_MANOPOLE, "le manopole si fermano dove si ferma il backend")

T_VECCHIO_APPLICA = '''    def _applica_cpu(self):
        m, s, t = self._valori_cpu()
        r = self.demone.cmd(cmd="apply-cpu", mhz=m, scale=s, temp=t)
        self.demone.cmd(cmd="thermal-guard", limit=t)
        self.et_cpu.setText(L("CPU applicata", "CPU applied") if r.get("ok") else r.get("err", L("non applicata", "not applied")))
'''

T_NUOVO_APPLICA = '''    # What the panel offers when the daemon cannot be asked. Deliberately the
    # narrow range: offering more than the backend accepts is the bug itself.
    RIPIEGO_LIMITI = {"freq_min": 3500, "freq_max": 4500, "scale_min": -40,
                      "scale_max": 0, "temp_min": 0, "temp_max": 100}

    def _limiti_cpu(self):
        """What the backend will really accept. Asked, never assumed: the panel
        used to offer 2000-4500 MHz against a floor of 3500, and everything
        below it failed without a word."""
        r = self.demone.cmd(cmd="cpu-limits") or {}
        lim = dict(self.RIPIEGO_LIMITI)
        if r.get("ok"):
            lim.update(r.get("data") or {})
        return lim

    def _motivo_cpu(self, r):
        """Why the setting did not go in, in words the user can act on."""
        f = r.get("fuori") or {}
        frase = {
            "frequency": L("La frequenza accettata va da %d a %d MHz.",
                           "The accepted clock runs from %d to %d MHz."),
            "scale": L("L'undervolt accettato va da %d a %d scalini.",
                       "The accepted undervolt runs from %d to %d steps."),
            "max_temperature": L("Il limite gradi accettato va da %d a %d.",
                                 "The accepted degree limit runs from %d to %d."),
        }.get(f.get("campo"))
        if frase:
            return frase % (f.get("min", 0), f.get("max", 0))
        return r.get("err") or L("non applicata", "not applied")

    def _applica_cpu(self):
        m, s, t = self._valori_cpu()
        r = self.demone.cmd(cmd="apply-cpu", mhz=m, scale=s, temp=t)
        self.demone.cmd(cmd="thermal-guard", limit=t)
        self.et_cpu.setText(L("CPU applicata", "CPU applied") if r.get("ok") else self._motivo_cpu(r))
'''

cambia(TUNER, T_VECCHIO_APPLICA, T_NUOVO_APPLICA, "Applica dice perche' non e' andata")

T_VECCHIO_SALVA = '''        r = self.demone.cmd(cmd="persist-cpu", mhz=m, scale=s, temp=t)
        self.et_cpu.setText(L("CPU salvata: vale anche al prossimo avvio", "CPU saved: applies at next boot too") if r.get("ok") else r.get("err", "?"))
'''

T_NUOVO_SALVA = '''        r = self.demone.cmd(cmd="persist-cpu", mhz=m, scale=s, temp=t)
        self.et_cpu.setText(L("CPU salvata: vale anche al prossimo avvio", "CPU saved: applies at next boot too") if r.get("ok") else self._motivo_cpu(r))
'''

cambia(TUNER, T_VECCHIO_SALVA, T_NUOVO_SALVA, "Salva al boot dice perche' non e' andata")

# --------------------------------------------------------------- applica

testi = {}
for percorso, vecchio, nuovo, etichetta in CAMBI:
    testi.setdefault(percorso, leggi(percorso))

esito = 0
for percorso, vecchio, nuovo, etichetta in CAMBI:
    quante = testi[percorso].count(vecchio)
    stato = "ok" if quante == 1 else "NON TROVATO" if quante == 0 else "%d VOLTE" % quante
    print("[%-11s] %-52s %s" % (stato, etichetta, os.path.basename(percorso)))
    if quante != 1:
        esito = 1
        continue
    testi[percorso] = testi[percorso].replace(vecchio, nuovo)

if esito:
    sys.exit("\nqualche ancoraggio non combacia: non ho scritto niente")

if PROVA:
    print("\n--prova: non ho scritto niente")
    sys.exit(0)

for percorso, testo in testi.items():
    scrivi(percorso, testo)
    print("scritto %s" % percorso)

# the daemon must still parse: a syntax error here is a dead Control Center
for percorso in testi:
    import py_compile
    py_compile.compile(percorso, cfile="/tmp/sfx-compile-check.pyc", doraise=True)
    print("compila: %s" % os.path.basename(percorso))
os.remove("/tmp/sfx-compile-check.pyc")
print("fatto")

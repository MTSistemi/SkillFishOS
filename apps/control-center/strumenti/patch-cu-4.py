#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Issue #77, the daemon: no floor, a mapping that can be kept at boot, and a
CU test that can finally look at the first three pairs.

Runs ON the build VM, inside ~/sfx-src.

    python3 patch-cu-4.py [--prova]

⚠️ cu_test USED TO RE-IMPOSE THE FLOOR IT WAS SUPPOSED TO HELP ESCAPE. It set
every row to 0x07 as its baseline and only ever added WGP3 and WGP4 on top, so
the three pairs a user most needs to check, the ones that could not be switched
off, were also the three the test never looked at. The baseline is now the real
minimum and the sweep covers all five positions.

⚠️ WHAT THE SWEEP CANNOT DO, so nobody reads more into it than is there: the
other rows have to be running on something while one row is under test, and
that something is their lowest pair. A pair that is defective there taints
every reading. The test finds a bad pair among the rest; it cannot clear the
floor pair of every row at once.

⚠️ TWENTY STEPS INSTEAD OF EIGHT, and they have to fit in the time the window
promises. Measured on the dev board: vkpeak prints fp32-scalar within 8
seconds, so the per-step bench comes down from 22 to 12 with margin to spare.

The row validation and the check that what was asked is what landed come from
tom lima's PR #80.
"""
import io
import os
import sys

PROVA = "--prova" in sys.argv
D = os.path.expanduser("~/sfx-src/apps/control-center/skillfish-cc-helper")

CAMBI = []


def cambia(vecchio, nuovo, etichetta):
    CAMBI.append((vecchio, nuovo, etichetta))


cambia('''def cu_get():
    try:
        return json.loads(sh("/usr/local/bin/skillfish-cu get", 30).stdout)
    except Exception:
        return {}
''', '''def cu_get():
    try:
        j = json.loads(sh("/usr/local/bin/skillfish-cu get", 30).stdout)
    except Exception:
        return {}
    # Whether a mapping is kept for the next boot is asked of the tool, which
    # owns the file, rather than by looking for the file from here.
    try:
        b = json.loads(sh("/usr/local/bin/skillfish-cu boot-get", 30).stdout)
        j["keep_boot"] = bool(b.get("keep"))
        j["boot_rows"] = b.get("rows") or []
    except Exception:
        j["keep_boot"] = False
        j["boot_rows"] = []
    return j


ORDINE_CU = ("0.0", "0.1", "1.0", "1.1")


def _cu_righe_valide(rows):
    """Four masks, each one a real one and none of them empty.

    A row with no WGP has nothing to run on, and the tool would quietly raise
    it to one pair. Saying no here means the window can explain it instead of
    showing a number the user did not choose."""
    if not isinstance(rows, list) or len(rows) != 4:
        return "maschere-storte"
    for x in rows:
        if not isinstance(x, int) or isinstance(x, bool) or not 0 <= x <= 31:
            return "maschere-storte"
    if any(x == 0 for x in rows):
        return "riga-vuota"
    return None
''', "cu_get sa del boot, e le righe si validano")

cambia('''        r = [int(x) & 0x1f for x in rows][:4]
        while len(r) < 4:
            r.append(0x07)
        _log("CU: maschere %s" % r)
        p = sh("/usr/local/bin/skillfish-cu set-rows %s" % (" ".join(str(x) for x in r)))
        j = cu_get()
        if p.returncode != 0:
            motivo = (getattr(p, "stderr", "") or "").strip() or (p.stdout or "").strip()
            return {"ok": False, "err": motivo or "skillfish-cu e' uscito con %d" % p.returncode,
                    "active": j.get("active_cu"), "rows": j.get("rows")}
        return {"ok": True, "active": j.get("active_cu"), "rows": j.get("rows")}
''', '''        storto = _cu_righe_valide(rows)
        if storto:
            # a missing fourth row used to be filled in with 0x07, which is the
            # floor that turned out not to exist: better to refuse than to
            # invent a mapping nobody asked for
            return {"ok": False, "motivo": storto}
        r = list(rows)
        _log("CU: maschere %s" % r)
        p = sh("/usr/local/bin/skillfish-cu set-rows %s" % (" ".join(str(x) for x in r)))
        j = cu_get()
        atteso = dict(zip(ORDINE_CU, r))
        if p.returncode != 0 or j.get("rows") != atteso:
            # the card is the authority, not the exit code: a write that went
            # nowhere used to come back as success. From PR #80.
            motivo = (getattr(p, "stderr", "") or "").strip() or (p.stdout or "").strip()
            return {"ok": False, "err": motivo or "skillfish-cu e' uscito con %d" % p.returncode,
                    "active": j.get("active_cu"), "rows": j.get("rows")}
        return {"ok": True, "active": j.get("active_cu"), "rows": j.get("rows")}
''', "cu_apply non inventa righe e controlla cosa e' atterrato")

cambia('''    def vk():
        r = sh("cd %s && stdbuf -oL -eL timeout 22 ./vkpeak" % vdir, t=35)
''', '''    def vk():
        # 12 and not 22: fp32-scalar is on screen within 8 seconds, measured on
        # the dev board, and the sweep now has twenty steps to get through.
        r = sh("cd %s && stdbuf -oL -eL timeout 12 ./vkpeak" % vdir, t=25)
''', "il banco per passo scende a 12 s")

cambia('''    cur = cu_get().get("rows", {})
    order = ["0.0", "0.1", "1.0", "1.1"]
    res = []
    sh("/usr/local/bin/skillfish-cu set-rows 7 7 7 7")
    time.sleep(1)
    base, _ = vk()
    for rk in order:
        for wgp in (3, 4):
            rows = {k: 7 for k in order}
            rows[rk] = 7 | (1 << wgp)
''', '''    stato = cu_get()
    cur = stato.get("rows", {})
    order = list(ORDINE_CU)
    # The lowest pair is what the other rows run on while one row is under
    # test. It used to be 0x07, three pairs, which is exactly the range the
    # test could never examine.
    fondo = 1 << 0
    res = []
    sh("/usr/local/bin/skillfish-cu set-rows %d %d %d %d" % (fondo, fondo, fondo, fondo))
    time.sleep(1)
    base, _ = vk()
    for rk in order:
        for wgp in range(5):
            rows = {k: fondo for k in order}
            rows[rk] = (1 << wgp)
''', "il test guarda tutte e cinque le posizioni, dal minimo vero")

cambia('''    if c == "cu-test":
''', '''    if c == "cu-keep-boot":
        return cu_keep_boot(req.get("on"), req.get("rows"))
    if c == "cu-test":
''', "il comando cu-keep-boot")

cambia('''def cu_test():
    if not VKPEAK:
''', '''def cu_keep_boot(on, rows):
    """Keep this mapping at the next boot, or stop keeping one.

    Only a mapping that is actually on the card can be kept: saving something
    that was never applied would arm the next boot with a routing nobody has
    seen work. The idea, and the check, are from tom lima\'s PR #80."""
    if not on:
        p = sh("/usr/local/bin/skillfish-cu boot-clear", 30)
        return {"ok": p.returncode == 0, **{k: v for k, v in cu_get().items() if k != "ok"}}
    storto = _cu_righe_valide(rows)
    if storto:
        return {"ok": False, "motivo": storto}
    viva = cu_get().get("rows")
    if viva != dict(zip(ORDINE_CU, rows)):
        return {"ok": False, "motivo": "non-applicata"}
    p = sh("/usr/local/bin/skillfish-cu boot-save %s" % " ".join(str(x) for x in rows), 30)
    _log("CU: tenute al boot %s" % rows)
    return {"ok": p.returncode == 0, **{k: v for k, v in cu_get().items() if k != "ok"}}


def cu_test():
    if not VKPEAK:
''', "cu_keep_boot")

testo = io.open(D, encoding="utf-8").read()
esito = 0
for vecchio, nuovo, etichetta in CAMBI:
    n = testo.count(vecchio)
    stato = "ok" if n == 1 else "NON TROVATO" if n == 0 else "%d VOLTE" % n
    print("[%-11s] %s" % (stato, etichetta))
    if n != 1:
        esito = 1
        continue
    testo = testo.replace(vecchio, nuovo)

if esito:
    sys.exit("\nqualche ancoraggio non combacia: non ho scritto niente")
if PROVA:
    sys.exit("\n--prova: non ho scritto niente")

io.open(D, "w", encoding="utf-8", newline="\n").write(testo)
import py_compile
py_compile.compile(D, cfile="/tmp/sfx-cu4.pyc", doraise=True)
os.remove("/tmp/sfx-cu4.pyc")
print("scritto e compila: %s" % D)

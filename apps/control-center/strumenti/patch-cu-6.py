#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Issue #77: the CU test puts the card back whatever happens, and stops
leaving a benchmark running behind it.

Runs ON the build VM, inside ~/sfx-src, after patch-cu-4.py.

    python3 patch-cu-6.py [--prova]

Three things, all found by running the thing instead of reading it.

⚠️ 1. IT DID NOT PUT THE CARD BACK IF IT DID NOT FINISH. The restore was the
last statement of the function, so anything that raised in the middle of twenty
steps left the board on one pair per row, eight CU out of forty, with nothing on
screen to say why. Measured: interrupted at row 1.1 the card sat at 8 CU. It is
a try/finally now.

⚠️ 2. THE FINAL BENCH HAD NO `timeout`, unlike every other call in here. With
shell=True a subprocess timeout kills the shell and leaves ./vkpeak running as
an orphan, pinning the GPU at 100% for as long as it likes. Seen on the board:
a vkpeak with no deadline still grinding after the caller was gone. Capped like
the others, and 20 seconds is plenty because fp32-scalar is printed within 8.

⚠️ 3. IT TOOK 425 SECONDS, not the five minutes the window promises. The waits
between steps were 1 s and 1.5 s for twenty steps, and the final bench ran to
completion when it only needs its first line. Trimmed to fit what we say.
"""
import io
import os
import sys

PROVA = "--prova" in sys.argv
D = os.path.expanduser("~/sfx-src/apps/control-center/skillfish-cc-helper")

VECCHIO = '''    res = []
    sh("/usr/local/bin/skillfish-cu set-rows %d %d %d %d" % (fondo, fondo, fondo, fondo))
    time.sleep(1)
    base, _ = vk()
    for rk in order:
        for wgp in range(5):
            rows = {k: fondo for k in order}
            rows[rk] = (1 << wgp)
            sh("/usr/local/bin/skillfish-cu set-rows %d %d %d %d" % (rows["0.0"], rows["0.1"], rows["1.0"], rows["1.1"]))
            time.sleep(1)
            g, rc = vk()
            e = errs()
            al = alive()
            verdict = "FAIL" if (not al or e > 0) else ("N/A" if g <= 0 else "OK")
            res.append({"row": rk, "wgp": wgp, "cu": "%d-%d" % (wgp * 2, wgp * 2 + 1),
                        "gflops": round(g), "errors": e, "verdict": verdict})
            time.sleep(1.5)
    sh("/usr/local/bin/skillfish-cu max")
    time.sleep(1)
    rf = sh("cd %s && ./vkpeak" % vdir, t=120)
    mf = re.search(r'fp32-scalar\\s*=\\s*([\\d.]+)', rf.stdout)
    full = round(float(mf.group(1)) if mf else 0.0)
    full_err = errs()
    g0 = lambda k: int(cur.get(k, 31))  # noqa: E731
    sh("/usr/local/bin/skillfish-cu set-rows %d %d %d %d" % (g0("0.0"), g0("0.1"), g0("1.0"), g0("1.1")))
    return {"ok": True, "baseline": round(base), "results": res,
'''

NUOVO = '''    res = []

    def rimetti():
        """The mapping the user had before any of this started.

        ⚠️ In a finally, because it used to be the last statement of the
        function: anything that raised part way through twenty steps left the
        board on one pair per row, eight CU out of forty, and said nothing."""
        g0 = int  # keeps the lambda-free shape readable
        sh("/usr/local/bin/skillfish-cu set-rows %d %d %d %d"
           % tuple(g0(cur.get(k, 31)) for k in order))

    try:
        sh("/usr/local/bin/skillfish-cu set-rows %d %d %d %d" % (fondo, fondo, fondo, fondo))
        time.sleep(0.5)
        base, _ = vk()
        for rk in order:
            for wgp in range(5):
                rows = {k: fondo for k in order}
                rows[rk] = (1 << wgp)
                sh("/usr/local/bin/skillfish-cu set-rows %d %d %d %d" % (rows["0.0"], rows["0.1"], rows["1.0"], rows["1.1"]))
                time.sleep(0.5)
                g, rc = vk()
                e = errs()
                al = alive()
                verdict = "FAIL" if (not al or e > 0) else ("N/A" if g <= 0 else "OK")
                res.append({"row": rk, "wgp": wgp, "cu": "%d-%d" % (wgp * 2, wgp * 2 + 1),
                            "gflops": round(g), "errors": e, "verdict": verdict})
                time.sleep(1)
        sh("/usr/local/bin/skillfish-cu max")
        time.sleep(0.5)
        # ⚠️ timeout, like every other bench here. Without one, a subprocess
        # deadline kills the shell and leaves ./vkpeak orphaned on the GPU.
        rf = sh("cd %s && stdbuf -oL -eL timeout 20 ./vkpeak" % vdir, t=35)
        mf = re.search(r'fp32-scalar\\s*=\\s*([\\d.]+)', rf.stdout)
        full = round(float(mf.group(1)) if mf else 0.0)
        full_err = errs()
    finally:
        rimetti()
    return {"ok": True, "baseline": round(base), "results": res,
'''

testo = io.open(D, encoding="utf-8").read()
n = testo.count(VECCHIO)
print("[%s] il corpo del test" % ("ok" if n == 1 else "NON TROVATO"))
if n != 1:
    sys.exit("l'ancoraggio non combacia: non ho scritto niente")
testo = testo.replace(VECCHIO, NUOVO)

if PROVA:
    sys.exit("\n--prova: non ho scritto niente")

io.open(D, "w", encoding="utf-8", newline="\n").write(testo)
import py_compile
py_compile.compile(D, cfile="/tmp/sfx-cu6.pyc", doraise=True)
os.remove("/tmp/sfx-cu6.pyc")
print("scritto e compila")

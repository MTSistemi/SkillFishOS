#!/usr/bin/env python3
"""Second pass on the dashboard daemon (2026-09-12): what the web Tuner needs
to match the native one.

    patch-dashboardd-2.py <repo>

- a CPU test runner with countdown and Stop (steps applied through the helper's
  cpu-volatile, the load run here, polled by the page): GET/POST
  /api/tuner/cpu-prova
- the 8-core unlock and the EFI program: GET/POST /api/tuner/coreunlock
Idempotent.
"""
import os
import sys

p = os.path.join(sys.argv[1], "apps", "dashboard", "skillfish-dashboardd")
t = open(p, encoding="utf-8").read()

if "class ProvaCpuWeb" not in t:
    a = "\ndef cc_gov():\n"
    assert a in t
    blocco = r'''
# ---- the CPU test with countdown and Stop (web side) ----------------------------
# The helper's own test-cpu/suggest-uv block for a minute or two and the page
# could only wait. Here the steps are run in a thread: the helper applies the
# values WITHOUT writing them to disk (cpu-volatile), sysbench loads every
# thread, the lowest clock is watched, and the page polls the state once a
# second. Stop kills the load; whatever happens the applied values come back.
def _cpu_min_mhz():
    try:
        with open("/proc/cpuinfo") as fh:
            fs = [float(ln.split(":")[1]) for ln in fh if ln.lower().startswith("cpu mhz")]
        return min(fs) if fs else None
    except Exception:
        return None


class ProvaCpuWeb:
    TOLLERANZA = 200

    def __init__(self):
        self.lock = threading.Lock()
        self.attiva = False
        self.stop = False
        self.etichetta = ""
        self.resto = 0
        self.esiti = []
        self.migliore = None
        self.finita = False
        self.fermata = False
        self.proc = None
        self.temp = 85

    def stato(self):
        with self.lock:
            return {"ok": True, "attiva": self.attiva, "etichetta": self.etichetta, "resto": self.resto,
                    "esiti": list(self.esiti), "migliore": self.migliore, "finita": self.finita,
                    "fermata": self.fermata}

    def avvia(self, passi, temp):
        with self.lock:
            if self.attiva:
                return {"ok": False, "err": "prova in corso"}
            self.attiva, self.stop, self.finita, self.fermata = True, False, False, False
            self.esiti, self.migliore, self.etichetta, self.resto = [], None, "", 0
            self.temp = int(temp)
        th = threading.Thread(target=self._giro, args=(list(passi),), daemon=True)
        th.start()
        return {"ok": True}

    def ferma(self):
        with self.lock:
            self.stop = True
            p = self.proc
        if p is not None:
            try:
                p.terminate()
            except OSError:
                pass
        return {"ok": True}

    def _giro(self, passi):
        nth = os.cpu_count() or 8
        for mhz, scale, secs in passi:
            if self.stop:
                break
            with self.lock:
                self.etichetta, self.resto = "%d MHz  ·  UV %d" % (mhz, scale), secs
            r = tuner_cmd([{"cmd": "cpu-volatile", "mhz": int(mhz), "scale": int(scale), "temp": self.temp}])
            if not r.get("ok"):
                with self.lock:
                    self.esiti.append({"mhz": mhz, "scale": scale, "tenuto": False, "min": 0, "err": r.get("err", "apply")})
                break
            try:
                proc = subprocess.Popen(["sysbench", "cpu", "--threads=%d" % nth, "--time=%d" % int(secs),
                                         "--cpu-max-prime=20000", "run"],
                                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except OSError as e:
                with self.lock:
                    self.esiti.append({"mhz": mhz, "scale": scale, "tenuto": False, "min": 0, "err": str(e)})
                break
            with self.lock:
                self.proc = proc
            minimo, t0 = None, time.monotonic()
            while proc.poll() is None and not self.stop:
                passati = time.monotonic() - t0
                if passati > 5:
                    m = _cpu_min_mhz()
                    if m is not None and (minimo is None or m < minimo):
                        minimo = m
                with self.lock:
                    self.resto = max(0, int(secs - passati))
                time.sleep(0.5)
            rc = proc.wait() if proc.poll() is not None else -1
            with self.lock:
                self.proc = None
            if self.stop:
                break
            tenuto = rc == 0 and minimo is not None and minimo >= mhz - self.TOLLERANZA
            with self.lock:
                self.esiti.append({"mhz": mhz, "scale": scale, "tenuto": tenuto, "min": int(minimo or 0)})
                if tenuto:
                    self.migliore = [mhz, scale]
            if not tenuto:
                break
        # back to the applied values, whatever happened
        try:
            cfg = (tuner_cmd([{"cmd": "get"}]).get("data") or {}).get("cpu") or {}
            tuner_cmd([{"cmd": "apply-cpu", "mhz": int(cfg.get("frequency", 3500)),
                        "scale": int(cfg.get("scale", 0)), "temp": int(cfg.get("max_temperature", 85))}])
        except Exception:
            pass
        with self.lock:
            self.fermata = self.stop
            self.attiva, self.finita, self.etichetta, self.resto = False, True, "", 0


PROVA_CPU = ProvaCpuWeb()


def cc_prova_cpu_post(data):
    az = data.get("azione", "avvia")
    if az == "stop":
        return PROVA_CPU.ferma()
    try:
        temp = int(data.get("temp", 85))
        if az == "uv":
            mhz = int(data.get("mhz", 3500))
            passi = [(mhz, s, 12) for s in range(0, -41, -2)]
        elif az == "max":
            passi = [(3600, -8, 30), (3700, -16, 30), (3800, -20, 30), (3900, -24, 30), (4000, -36, 30)]
        else:
            passi = [(int(data.get("mhz", 3500)), int(data.get("scale", 0)), 60)]
    except (TypeError, ValueError):
        return {"ok": False, "err": "valori non validi"}
    return PROVA_CPU.avvia(passi, temp)


def cc_coreunlock():
    r = tuner_cmd([{"cmd": "core-unlock"}])
    e = tuner_cmd([{"cmd": "coreunlock-efi"}])
    return {"ok": True, "abilitato": bool(r.get("abilitato")), "supportato": bool(r.get("supportato")),
            "efi": e if e.get("ok") else {"supportato": False}}


def cc_coreunlock_post(data):
    if "efi" in data:
        return tuner_cmd([{"cmd": "coreunlock-efi-set", "on": bool(data.get("efi"))}])
    return tuner_cmd([{"cmd": "core-unlock-set", "on": bool(data.get("on"))}])

'''
    t = t.replace(a, blocco + a, 1)
    print("classe ProvaCpuWeb")

if '"/api/tuner/cpu-prova"' not in t:
    a = '''        if path == "/api/tuner/gov":
            if not self._guard("tuner"):
                return
            return self._json(200, cc_gov())
'''
    assert a in t
    t = t.replace(a, '''        if path == "/api/tuner/cpu-prova":
            if not self._guard("tuner"):
                return
            return self._json(200, PROVA_CPU.stato())
        if path == "/api/tuner/coreunlock":
            if not self._guard("tuner"):
                return
            return self._json(200, cc_coreunlock())
''' + a, 1)
    b = '''        if path == "/api/tuner/test-cpu":
            if not self._guard("tuner"):
                return
'''
    assert b in t
    t = t.replace(b, '''        if path == "/api/tuner/cpu-prova":
            if not self._guard("tuner"):
                return
            return self._json(200, cc_prova_cpu_post(data))
        if path == "/api/tuner/coreunlock":
            if not self._guard("tuner"):
                return
            return self._json(200, cc_coreunlock_post(data))
''' + b, 1)
    print("rotte cpu-prova e coreunlock")

open(p, "w", encoding="utf-8").write(t)
print("fatto")

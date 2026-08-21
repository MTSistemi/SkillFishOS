# -*- coding: utf-8 -*-
u"""I dati del HUD, letti una volta sola per tutti.

CHI LO USA
  - skillfish-hud-editor, la finestra sulla scrivania
  - skillfish-dashboardd, che serve la stessa pagina da remoto

⚠️ PERCHE' STA QUI E NON DENTRO ALL'APPLICAZIONE.
Le due strade devono dire la STESSA cosa. Se il configuratore sul desktop e
quello via web calcolassero per conto proprio quali voci la macchina puo' dare,
al primo sensore nuovo una delle due direbbe di si' e l'altra di no — e l'utente
non avrebbe modo di capire quale delle due ha ragione. Una copia della logica e'
una copia che diverge; e' solo questione di quando.

⚠️ QUI NON SI TRADUCE NIENTE. Le etichette restano a chi disegna: la finestra ha
il suo L(), la pagina web il suo dizionario. Questo modulo maneggia chiavi, che
sono le stesse per tutti e in tutte le lingue.
"""
from __future__ import unicode_literals

import glob
import io
import json
import os
import subprocess

VAL = "/usr/local/bin/skillfish-hud-val"
GEN = "/usr/local/bin/skillfish-hud-config"

# Le voci che skillfish-hud-config sa scrivere. ⚠️ Le chiavi sono le stesse la',
# qui e nel file delle preferenze: cambiarne una in un posto solo vuol dire un
# ordine scritto che nessuno capisce.
CHIAVI = ["titolo", "kernel", "cpu", "barre", "gpu", "gpubar", "volt", "vram",
          "ram", "fan", "disco", "rete", "uptime", "bluetooth"]

ORDINE_PREDEFINITO = ["titolo", "kernel", "cpu", "barre", "gpu", "gpubar",
                      "volt", "vram", "ram", "fan", "disco", "bluetooth"]

POSIZIONI = ["top_right", "top_left", "bottom_right", "bottom_left",
             "middle_right", "middle_left"]

# Le voci che ci sono sempre: non dipendono da un sensore.
SEMPRE = ("titolo", "cpu", "barre", "ram", "disco", "uptime")


def val(chiave):
    u"""Un valore letto da skillfish-hud-val, o stringa vuota se non c'e'."""
    try:
        p = subprocess.run([VAL, chiave], capture_output=True, text=True, timeout=6)
        v = (p.stdout or "").strip()
        return v if v and v not in ("?", "0") else ""
    except Exception:
        return ""


def c_e_util():
    u"""Il carico della GPU esiste come DATO anche quando vale zero.

    ⚠️ `val()` scarta lo zero, perche' per quasi tutte le chiavi zero vuol dire
    «non lo so». Per il carico no: una macchina ferma sta davvero allo zero per
    cento. Guardando il valore, l'anteprima nascondeva la barra della GPU su una
    scheda a riposo mentre il HUD vero la mostrava — cioe' l'anteprima diceva una
    cosa e lo schermo un'altra, che e' il difetto peggiore che possa avere
    un'anteprima. Si guarda la FONTE, esattamente come fa skillfish-hud-config.
    """
    if os.path.exists("/run/skillfish-gpu-util"):
        return True
    return bool(glob.glob("/sys/class/drm/card[0-9]/device/gpu_busy_percent"))


def dati():
    u"""I valori veri di questa macchina, adesso."""
    d = {}
    for k in ("kernel", "cpu_temp", "gpu_freq", "gpu_temp", "gpu_util",
              "gpu_mv", "gpu_power", "vram", "vram_tot", "fan", "fan_all"):
        v = val(k)
        if v:
            d[k] = v
    try:
        with io.open("/proc/cpuinfo", encoding="utf-8") as f:
            mhz = [float(r.split(":")[1]) for r in f if r.startswith("cpu MHz")]
        d["cpu_mhz_g"] = "%.2f" % (max(mhz) / 1000.0) if mhz else "—"
        d["thread"] = len(mhz) or os.cpu_count() or 8
    except Exception:
        d["thread"] = os.cpu_count() or 8
    try:
        with io.open("/proc/loadavg", encoding="utf-8") as f:
            carico = float(f.read().split()[0])
        d["cpu_use"] = "%d" % min(100, carico / max(1, d["thread"]) * 100)
    except Exception:
        pass
    try:
        with io.open("/proc/meminfo", encoding="utf-8") as f:
            m = {}
            for r in f:
                p = r.split()
                if p[0][:-1] in ("MemTotal", "MemAvailable"):
                    m[p[0][:-1]] = int(p[1])
        tot, disp = m.get("MemTotal", 0), m.get("MemAvailable", 0)
        if tot:
            d["ram"] = "%.1f / %.1f GiB   %d%%" % ((tot - disp) / 1048576.0,
                                                   tot / 1048576.0,
                                                   (tot - disp) * 100 // tot)
    except Exception:
        pass
    try:
        s = os.statvfs("/")
        usati = (s.f_blocks - s.f_bfree) * s.f_frsize / 1073741824.0
        tot = s.f_blocks * s.f_frsize / 1073741824.0
        d["disco"] = "%.0f / %.0f GiB   %d%%" % (usati, tot, usati * 100 // max(1, tot))
    except Exception:
        pass
    try:
        with io.open("/proc/uptime", encoding="utf-8") as f:
            sec = float(f.read().split()[0])
        d["uptime"] = "%dg %dh" % (sec // 86400, (sec % 86400) // 3600)
    except Exception:
        pass
    d["gpu_util_c_e"] = c_e_util()
    d["rete"] = "0,0 ↓  0,0 ↑" if os.path.isdir("/sys/class/net") else ""
    d["bluetooth"] = bool(os.path.isdir("/sys/class/bluetooth")
                          and os.listdir("/sys/class/bluetooth"))
    return d


def disponibili(d=None):
    u"""Quali voci questa macchina puo' dare davvero.

    ⚠️ Le altre restano SCEGLIIBILI, solo in grigio. Sono spente perche' il dato
    non c'e' adesso — le ventole non si vedono finche' non e' caricato il driver
    del Super-I/O, e una scheda video la si puo' infilare domani. Toglierle
    dall'elenco farebbe sembrare il sistema piu' povero di quello che e', e non
    ci sarebbe modo di capire dove cercare quando il dato compare.
    """
    if d is None:
        d = dati()
    c_e = {
        "kernel": bool(d.get("kernel")),
        "gpu": bool(d.get("gpu_freq") or d.get("gpu_temp") or d.get("gpu_util_c_e")),
        "gpubar": bool(d.get("gpu_util_c_e")),
        "volt": bool(d.get("gpu_mv") or d.get("gpu_power")),
        "vram": bool(d.get("vram") or d.get("vram_tot")),
        "fan": bool(d.get("fan") or d.get("fan_all")),
        "rete": bool(d.get("rete")),
        "bluetooth": bool(d.get("bluetooth")),
    }
    return dict((k, bool(c_e.get(k, True))) for k in CHIAVI)


# ------------------------------------------------------------- le preferenze
def percorso_pref(home):
    return os.path.join(home, ".config", "skillfish", "hud.json")


def percorso_autostart(home):
    return os.path.join(home, ".config", "autostart", "skillfish-conky.desktop")


def leggi_pref(percorso):
    try:
        with io.open(percorso, encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except (IOError, OSError, ValueError):
        return {}


def acceso(percorso_auto):
    u"""Il HUD si accendera' al prossimo accesso?

    Si guarda l'avvio automatico, non se conky sta girando adesso: chi lo spegne
    vuole che resti spento anche dopo un riavvio, e chi lo accende vuole
    ritrovarlo. `Hidden=true` e' il modo previsto dallo standard per disattivare
    un avvio automatico senza cancellare il file — cancellarlo vorrebbe dire non
    sapere piu' come rimetterlo.
    """
    try:
        with io.open(percorso_auto, encoding="utf-8") as f:
            return "hidden=true" not in f.read().lower()
    except (IOError, OSError):
        return False


def normalizza(pref):
    u"""Rende sicure le preferenze che arrivano da fuori.

    ⚠️ Dalla pagina web arriva quello che arriva. Chiavi inventate, una posizione
    che non esiste, una larghezza di tre pixel: qui si tiene solo cio' che
    skillfish-hud-config sa scrivere, e il resto si butta. Il generatore esegue
    soltanto nomi che corrispondono a una sua funzione, ma fidarsi di un solo
    controllo quando ce ne possono essere due e' una scelta strana da fare.
    """
    voci = [v for v in (pref.get("voci") or []) if v in CHIAVI]
    pos = pref.get("posizione")
    def _int(chiave, minimo, massimo, quando_manca):
        try:
            return max(minimo, min(massimo, int(pref.get(chiave, quando_manca))))
        except (TypeError, ValueError):
            return quando_manca
    return {
        "versione": 1,
        "mostra": bool(pref.get("mostra", True)),
        # ⚠️ Elenco VUOTO e chiave assente sono due cose diverse: vuoto vuol dire
        # «non voglio niente», assente vuol dire «non ho scelto». Appiattirle
        # rimetteva il HUD intero a chi lo aveva svuotato apposta.
        "voci": voci,
        "posizione": pos if pos in POSIZIONI else "top_right",
        "larghezza": _int("larghezza", 160, 800, 240),
        "opacita": _int("opacita", 0, 255, 165),
        "font": _int("font", 6, 20, 9),
        "intervallo": _int("intervallo", 1, 60, 2),
    }

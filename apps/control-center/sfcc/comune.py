# -*- coding: utf-8 -*-
"""Things every page needs: the language, the help button, small file helpers.

The translation rule of the project: Italian is written in the code as the
first argument of L(), English is the second and is also the key of the shared
dictionary in /usr/share/skillfish/i18n/<lang>.json. Anything not translated
falls back to English, never to Italian.
"""
import io
import json
import os
import subprocess
import sys

sys.path.insert(0, "/usr/share/skillfish")


def _lingua():
    val = (os.environ.get("LC_ALL") or os.environ.get("LC_MESSAGES")
           or os.environ.get("LANG") or os.environ.get("LANGUAGE") or "")
    v = val.lower()
    if v.startswith("it"):
        return "it"
    # "uk" is Ukrainian; "ua" is the country and turns up in hand-written locales.
    if v.startswith("ua"):
        return "uk"
    codice = v.replace("-", "_").split(".")[0].split("@")[0].split("_")[0].strip()
    if len(codice) == 2 and codice.isalpha():
        return codice
    return "en"


LANG = _lingua()

# The shared dictionary must never keep the window from opening.
try:
    from i18n import traduttore as _traduttore
    _TR = _traduttore(LANG)
except Exception:
    def _TR(en):
        return en


def L(it, en):
    """Italian from the code, anything else through the shared dictionary.

    Both strings must be constants: format AFTER translating, or the key
    looked up already contains the value and is never found.
    """
    return it if LANG == "it" else _TR(en)


# The "?" button shared by every SkillFishOS application. base and this package
# are different .debs, so the import is guarded: without it the explanation is
# shown as a tooltip and nothing else changes.
try:
    from aiuto import Aiuto
except Exception:
    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import QToolButton, QMessageBox

    class Aiuto(QToolButton):
        def __init__(self, testo, titolo="", parent=None):
            super().__init__(parent)
            self.setText("?")
            self.setToolTip(testo)
            self.setCursor(Qt.CursorShape.WhatsThisCursor)
            self._t, self._ti = testo, titolo
            self.clicked.connect(lambda: QMessageBox.information(
                self.window(), self._ti or L("Aiuto", "Help"), self._t))


# ---------------------------------------------------------------- paths
E_BC250 = "/usr/local/bin/skillfish-is-bc250"
ICONE = "/usr/share/icons/hicolor/256x256/apps"
ICONA = ICONE + "/skillfish-control-center.png"
HELPER = "/usr/local/bin/skillfish-cc-helper"
GOV_CONF = "/etc/skillfish-vf-governor.json"
GOV_BATTITO = "/run/skillfish-vf-governor.battito"
VENTOLA_STATO = "/run/skillfish/ventola.json"
VENTOLA_CONF = "/etc/skillfish/ventola.json"
FREEZE_LOG = "/var/log/skillfish-freeze.log"
FREEZE_FLAG = "/run/skillfish-freeze-detected"
CU_STATO = "/run/skillfish/cu_active.json"
PROFILI_UTENTE = os.path.expanduser("~/.config/skillfish/profili.json")
PROFILI_SISTEMA = "/usr/share/skillfish/profili.json"
IMPOSTAZIONI = os.path.expanduser("~/.config/skillfish/control-center.json")


def e_bc250():
    """True on the board. The tools that talk to the SMU must not run elsewhere."""
    try:
        return subprocess.run([E_BC250], capture_output=True, timeout=5).returncode == 0
    except Exception:
        return False


def sh(cmd, t=30, **kw):
    """(rc, stdout, stderr) of a shell command that must never raise."""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=t, **kw)
        return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()
    except Exception as e:
        return 1, "", str(e)


def leggi_json(percorso, ripiego=None):
    try:
        with io.open(percorso, encoding="utf-8") as f:
            d = json.load(f)
        return d if d is not None else ripiego
    except (IOError, OSError, ValueError):
        return ripiego


def scrivi_json(percorso, dati):
    """Write a user-owned JSON file atomically (the settings, the profiles)."""
    os.makedirs(os.path.dirname(percorso), exist_ok=True)
    tmp = percorso + ".tmp"
    with io.open(tmp, "w", encoding="utf-8") as f:
        json.dump(dati, f, indent=1, ensure_ascii=False)
    os.replace(tmp, percorso)


def leggi_testo(percorso):
    try:
        with io.open(percorso, encoding="utf-8") as f:
            return f.read().strip()
    except (IOError, OSError):
        return ""


def battito():
    """The governor heartbeat: (epoch, MHz, ceiling, degrees, watts, load) or None."""
    t = leggi_testo(GOV_BATTITO)
    try:
        p = t.split()
        return {"quando": float(p[0]), "mhz": int(p[1]), "tetto": int(p[2]),
                "gradi": int(p[3]), "watt": int(p[4]), "carico": int(p[5])}
    except (IndexError, ValueError):
        return None


def hwmon_valore(nome_chip, voce):
    """One hwmon reading by chip name, or None."""
    base = "/sys/class/hwmon"
    try:
        for h in sorted(os.listdir(base)):
            p = os.path.join(base, h)
            if leggi_testo(p + "/name") == nome_chip:
                v = leggi_testo(os.path.join(p, voce))
                return int(v) if v.lstrip("-").isdigit() else None
    except OSError:
        pass
    return None


def versione_pacchetto(nome):
    rc, out, _ = sh("dpkg-query -W -f='${Version}' %s 2>/dev/null" % nome, 10)
    return out if rc == 0 else ""

# -*- coding: utf-8 -*-
"""Console: Steam Big Picture inside gamescope, like a SteamOS session.

Two ways in: the session picked at the login screen, and this button, which
starts gamescope over the running desktop. Quitting Steam, or "Return to
desktop" inside it, brings the desktop back with every window where it was.
"""
import os
import subprocess

from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QMessageBox, QVBoxLayout, QWidget

from ..comune import IMPOSTAZIONI, L, leggi_json, scrivi_json, sh
from ..finestra import PaginaBase
from ..stile import Scheda, Stato, griglia_schede, intestazione

GAMING_MODE = "/usr/local/bin/skillfish-gaming-mode"
SESSIONE = "/usr/share/wayland-sessions/skillfish-gaming.desktop"


class Pagina(PaginaBase):
    def __init__(self, finestra):
        super().__init__(finestra)
        self.intervallo_ms = 3000

    def costruisci(self):
        v = self.corpo_scorrevole()
        v.addWidget(intestazione("Console", L(
            "Steam Big Picture a tutto schermo dentro gamescope, con il controller: la scheda come una "
            "console. Si esce da Steam, e il desktop e' ancora li'.",
            "Steam Big Picture full screen inside gamescope, with the controller: the board as a console. "
            "Quit Steam, and the desktop is still there.")))
        self.c_avvia = Scheda(L("Adesso", "Now"), L("Parte sopra al desktop: gamescope prende lo schermo e Steam si apre in modalita' console.",
            "Starts on top of the desktop: gamescope takes the screen and Steam opens in console mode."))
        self.b_stato = Stato("", "quieto")
        self.c_avvia.testa.insertWidget(self.c_avvia.testa.count() - 1, self.b_stato)
        imp = leggi_json(IMPOSTAZIONI, {}) or {}
        cons = imp.get("console", {})
        r = QHBoxLayout()
        r.addWidget(QLabel(L("Risoluzione", "Resolution")))
        self.ris = QComboBox()
        for w, h in ((1920, 1080), (2560, 1440), (3840, 2160), (1280, 720)):
            self.ris.addItem("%d×%d" % (w, h), (w, h))
        i = self.ris.findText("%d×%d" % (cons.get("w", 1920), cons.get("h", 1080)))
        self.ris.setCurrentIndex(i if i >= 0 else 0)
        r.addWidget(self.ris)
        r.addWidget(QLabel("Hz"))
        self.hz = QComboBox()
        for hz in (60, 120, 144, 50):
            self.hz.addItem(str(hz), hz)
        i = self.hz.findData(cons.get("r", 60))
        self.hz.setCurrentIndex(i if i >= 0 else 0)
        r.addWidget(self.hz)
        r.addStretch(1)
        self.c_avvia.aggiungi(r)
        self.c_avvia.bottoni((L("Avvia la console", "Start the console"), self._avvia, True),
                             (L("Torna al desktop", "Back to the desktop"), self._desktop, False))

        self.c_sessione = Scheda(L("Dalla schermata di accesso", "From the login screen"), L("Nella schermata di accesso scegli la sessione «SkillFishOS Console»: la scheda parte in Steam senza desktop.",
            "On the login screen pick the «SkillFishOS Console» session: the board starts into Steam, no desktop."))
        self.r_sess = self.c_sessione.riga(L("Sessione installata", "Session installed"))
        self.r_gs = self.c_sessione.riga("gamescope")
        self.r_steam = self.c_sessione.riga("Steam")
        v.addWidget(griglia_schede(self.c_avvia, self.c_sessione, colonne=2))
        v.addStretch(1)
        self.r_sess.setText(L("si'", "yes") if os.path.exists(SESSIONE) else L("no", "no"))
        rc, out, _ = sh("/usr/games/gamescope --version 2>&1 | sed 's/\\x1b\\[[0-9;]*m//g' | grep -oE '[0-9]+\\.[0-9]+[0-9a-z.-]*' | head -1", 5)
        self.r_gs.setText(out.strip() or L("presente", "present") if os.path.exists("/usr/games/gamescope") else L("manca", "missing"))
        rc, out, _ = sh("flatpak info com.valvesoftware.Steam --show-ref 2>/dev/null", 10)
        self.r_steam.setText(L("flatpak", "flatpak") if rc == 0 else L("manca", "missing"))

    def aggiorna(self):
        rc, out, _ = sh("pgrep -x gamescope >/dev/null && echo si", 5)
        on = out.strip() == "si"
        self.b_stato.setText(L("in corso", "running") if on else L("ferma", "stopped"))
        self.b_stato.tono("bene" if on else "quieto")

    def _avvia(self):
        if not os.path.exists(GAMING_MODE):
            self.toast(L("manca skillfish-console", "skillfish-console is missing"))
            return
        w, h = self.ris.currentData()
        r = self.hz.currentData()
        imp = leggi_json(IMPOSTAZIONI, {}) or {}
        imp["console"] = {"w": w, "h": h, "r": r}
        scrivi_json(IMPOSTAZIONI, imp)
        env = dict(os.environ, GAMESCOPE_W=str(w), GAMESCOPE_H=str(h), GAMESCOPE_R=str(r))
        subprocess.Popen([GAMING_MODE], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def _desktop(self):
        sh("/usr/local/bin/steamos-session-select desktop", 20)

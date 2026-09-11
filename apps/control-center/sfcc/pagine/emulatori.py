# -*- coding: utf-8 -*-
"""Emulators: EmuDeck, or pick them one by one from Flathub.

They are not in the ISO on purpose (several GB, not for everyone). EmuDeck
installs into the user's home, so it has to be done on every machine; the
list of single emulators comes from install-emulators.sh, which is the
authority on what runs well on this GPU.
"""
import os
import subprocess

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (QCheckBox, QHBoxLayout, QLabel, QPlainTextEdit, QPushButton,
                             QVBoxLayout, QWidget)

from .. import stile
from ..comune import L, leggi_testo, sh
from ..finestra import PaginaBase
from ..stile import Scheda, Stato, griglia_schede, intestazione

EMUDECK_SH = "/usr/local/share/skillfish/install-emudeck.sh"
EMU_SH = "/usr/local/share/skillfish/install-emulators.sh"
EMUDECK_APP = os.path.expanduser("~/Applications/EmuDeck.AppImage")


def elenco_emulatori():
    """key|flatpak id|name|description|recommended, parsed from the script itself."""
    out = []
    dentro = False
    for riga in leggi_testo(EMU_SH).splitlines():
        if riga.startswith('EMU="'):
            dentro = True
            continue
        if dentro:
            if riga.strip() == '"':
                break
            p = riga.strip().split("|")
            if len(p) >= 5 and p[0]:
                out.append({"chiave": p[0], "id": p[1], "nome": p[2], "desc": p[3], "consigliato": p[4] == "si"})
    return out


def flatpak_installati():
    rc, out, _ = sh("flatpak list --app --columns=application 2>/dev/null", 20)
    return set(out.split())


class Lavoro(QThread):
    riga = pyqtSignal(str)
    fine = pyqtSignal(int)

    def __init__(self, cmd, parent=None):
        super().__init__(parent)
        self.cmd = cmd

    def run(self):
        try:
            p = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            for ln in iter(p.stdout.readline, ""):
                if ln:
                    self.riga.emit(ln.rstrip())
            p.wait()
            self.fine.emit(p.returncode)
        except Exception as e:
            self.riga.emit(str(e))
            self.fine.emit(1)


class Pagina(PaginaBase):
    def __init__(self, finestra):
        super().__init__(finestra)
        self.intervallo_ms = 0
        self._lavoro = None
        self.caselle = {}

    def costruisci(self):
        v = self.corpo_scorrevole()
        v.addWidget(intestazione(L("Emulatori", "Emulators"), L(
            "Non sono nella ISO: pesano diversi gigabyte e non servono a tutti. Due strade: EmuDeck, "
            "che configura tutto da solo, o la scelta uno per uno da Flathub.",
            "Not in the ISO: they weigh several gigabytes and not everyone wants them. Two ways: "
            "EmuDeck, which sets everything up by itself, or picking them one by one from Flathub.")))
        self.c_emudeck = Scheda("EmuDeck", L("Installa e configura emulatori, cartelle ROM, BIOS e controlli, tutto nella tua home.",
            "Installs and configures emulators, ROM folders, BIOS files and controls, all in your home."))
        self.b_emudeck = Stato("", "quieto")
        self.c_emudeck.testa.insertWidget(self.c_emudeck.testa.count() - 1, self.b_emudeck)
        self.c_emudeck.aggiungi(QLabel(L("Scarica l'AppImage ufficiale e lo avvia: da li' scegli tu.", "Downloads the official AppImage and starts it: you choose from there.")))
        self.c_emudeck.bottoni((L("Installa / Avvia", "Install / Start"), self._emudeck, True))

        self.c_lista = Scheda(L("Uno per uno", "One by one"), L("Flatpak da Flathub: i pacchetti Debian sono vecchi e su questa GPU rendono male. Spuntati i consigliati.",
            "Flatpaks from Flathub: the Debian packages are old and run badly on this GPU. The recommended ones are ticked."))
        inst = flatpak_installati()
        for e in elenco_emulatori():
            r = QHBoxLayout()
            c = QCheckBox("%s" % e["nome"])
            c.setChecked(e["consigliato"] and e["id"] not in inst)
            c.setToolTip(e["desc"])
            self.caselle[e["id"]] = c
            r.addWidget(c)
            d = QLabel(e["desc"])
            d.setObjectName("quieto")
            d.setWordWrap(True)
            r.addWidget(d, 1)
            st = Stato(L("installato", "installed") if e["id"] in inst else "", "bene")
            if e["id"] in inst:
                r.addWidget(st)
                b = QPushButton(L("Avvia", "Launch"))
                b.clicked.connect(lambda _c=False, i=e["id"]: subprocess.Popen(["flatpak", "run", i]))
                r.addWidget(b)
            self.c_lista.aggiungi(r)
        self.c_lista.bottoni((L("Installa i selezionati", "Install the selected"), self._installa, True))
        v.addWidget(griglia_schede(self.c_emudeck, self.c_lista, colonne=2))
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(200)
        self.log.hide()
        v.addWidget(self.log)
        v.addStretch(1)
        self.aggiorna()

    def aggiorna(self):
        c = os.path.exists(EMUDECK_APP)
        self.b_emudeck.setText(L("installato", "installed") if c else L("non installato", "not installed"))
        self.b_emudeck.tono("bene" if c else "quieto")

    def _emudeck(self):
        if os.path.exists(EMUDECK_APP):
            subprocess.Popen([EMUDECK_APP], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return
        self._avvia(["bash", EMUDECK_SH])

    def _installa(self):
        scelti = [i for i, c in self.caselle.items() if c.isChecked()]
        if not scelti:
            self.toast(L("Niente selezionato.", "Nothing selected."))
            return
        self._avvia(["flatpak", "install", "--user", "-y", "flathub"] + scelti)

    def _avvia(self, cmd):
        if self._lavoro is not None:
            return
        self.log.clear()
        self.log.show()
        self.log.appendPlainText("$ " + " ".join(cmd))
        self._lavoro = Lavoro(cmd, self)
        self._lavoro.riga.connect(self.log.appendPlainText)
        self._lavoro.fine.connect(self._finito)
        self._lavoro.start()

    def _finito(self, rc):
        self._lavoro = None
        self.log.appendPlainText(L("Fatto.", "Done.") if rc == 0 else L("Uscita %d.", "Exit %d.") % rc)
        sh("kbuildsycoca6 --noincremental >/dev/null 2>&1 &", 5)
        self.costruita = False
        self.attiva()

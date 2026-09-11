# -*- coding: utf-8 -*-
"""ISO: disk images mounted through udisks2, the way the Dolphin menu does it."""
import json
import os
import subprocess

from PyQt6.QtWidgets import QFileDialog, QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from ..comune import L, sh
from ..finestra import PaginaBase
from ..stile import Scheda, intestazione

MONTA = "/usr/local/bin/skillfish-iso-mount"


def montate():
    """[(iso file, loop device, mountpoint)] for every image on a loop device."""
    out = []
    rc, txt, _ = sh("losetup -J 2>/dev/null", 10)
    try:
        dev = json.loads(txt or "{}").get("loopdevices", [])
    except ValueError:
        dev = []
    for d in dev:
        nome, back = d.get("name", ""), d.get("back-file", "") or ""
        if not back or back.startswith("/var/lib/snapd"):
            continue
        rc, mp, _ = sh("findmnt -nro TARGET %s 2>/dev/null | head -1" % nome, 5)
        out.append((back, nome, mp.replace("\\x20", " ")))
    return out


class Pagina(PaginaBase):
    def __init__(self, finestra):
        super().__init__(finestra)
        self.intervallo_ms = 3000

    def costruisci(self):
        v = self.corpo_scorrevole()
        v.addWidget(intestazione("ISO", L(
            "Immagini disco montate come dischi, senza terminale e senza GNOME: dal menu di Dolphin o da "
            "qui.", "Disk images mounted as disks, no terminal and no GNOME: from the Dolphin menu or "
            "from here.")))
        self.scheda = Scheda(L("Immagini montate", "Mounted images"))
        self.lista = QVBoxLayout()
        self.lista.setSpacing(4)
        self.scheda.aggiungi(self.lista)
        self.scheda.bottoni((L("Monta un'immagine…", "Mount an image…"), self._monta, True))
        v.addWidget(self.scheda)
        v.addStretch(1)

    def aggiorna(self):
        while self.lista.count():
            it = self.lista.takeAt(0)
            if it.widget():
                it.widget().deleteLater()
        voci = montate()
        if not voci:
            e = QLabel(L("Nessuna immagine montata.", "No image mounted."))
            e.setObjectName("quieto")
            self.lista.addWidget(e)
            return
        for iso, dev, mp in voci:
            riga = QFrame()
            riga.setObjectName("riga")
            r = QHBoxLayout(riga)
            r.setContentsMargins(4, 4, 4, 6)
            col = QVBoxLayout()
            col.setSpacing(0)
            n = QLabel(os.path.basename(iso))
            n.setStyleSheet("font-weight:700;")
            m = QLabel("%s   ·   %s" % (dev, mp or L("non montata", "not mounted")))
            m.setObjectName("quieto")
            col.addWidget(n)
            col.addWidget(m)
            r.addLayout(col, 1)
            if mp:
                b = QPushButton(L("Apri", "Open"))
                b.clicked.connect(lambda _c=False, p=mp: subprocess.Popen(["xdg-open", p]))
                r.addWidget(b)
            b = QPushButton(L("Smonta", "Unmount"))
            b.clicked.connect(lambda _c=False, f=iso: self._smonta(f))
            r.addWidget(b)
            self.lista.addWidget(riga)

    def _monta(self):
        f, _ = QFileDialog.getOpenFileName(self, L("Immagine disco", "Disk image"), os.path.expanduser("~"), "ISO (*.iso *.img *.udf);;*")
        if f:
            subprocess.Popen([MONTA, f])
            self.toast(L("Monto %s…", "Mounting %s…") % os.path.basename(f))

    def _smonta(self, f):
        subprocess.Popen([MONTA, "-u", f])
        self.toast(L("Smonto %s…", "Unmounting %s…") % os.path.basename(f))

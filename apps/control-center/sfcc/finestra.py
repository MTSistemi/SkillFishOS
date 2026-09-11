# -*- coding: utf-8 -*-
"""The window: a column of sections on the left, one page at a time on the right.

Sections are one word each. A page is built the first time it is opened and
told when it is shown and hidden, so only the visible one polls the machine.
"""
import importlib
import os

from PyQt6.QtCore import QRect, QSize, Qt, QTimer
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (QApplication, QButtonGroup, QFrame, QHBoxLayout, QLabel,
                             QMainWindow, QPushButton, QScrollArea, QStackedWidget,
                             QVBoxLayout, QWidget)

from . import VERSIONE, stile
from .comune import ICONA, ICONE, L, e_bc250
from .demone import Demone
from .pad import Pad, invia_tasto

# key, Italian, English, icon file, module under pagine/
SEZIONI = [
    ("stato",     "Stato",      "Status",    "skillfish-control-center", "stato"),
    ("tuner",     "Tuner",      "Tuner",     "skillfish-tuner",          "tuner"),
    ("ventola",   "Ventola",    "Fan",       "skillfish-fan",            "ventola"),
    ("monitor",   "Monitor",    "Monitor",   "skillfish-monitor",        "monitor"),
    ("giochi",    "Giochi",     "Games",     "skillfish-giochi",         "giochi"),
    ("profili",   "Profili",    "Profiles",  "skillfish-profili",        "profili"),
    ("kernel",    "Kernel",     "Kernel",    "skillfish-kernel",         "kernel"),
    ("snapshots", "Snapshot",   "Snapshots", "skillfish-snapshots",      "snapshots"),
    ("ai",        "AI",         "AI",        "skillfish-ai",             "ai"),
    ("emulatori", "Emulatori",  "Emulators", "skillfish-emulators",      "emulatori"),
    ("console",   "Console",    "Console",   "skillfish-console",        "console"),
    ("iso",       "ISO",        "ISO",       "skillfish-iso-mount",      "iso"),
]


class PaginaBase(QWidget):
    """What every page inherits: the window, the helper, a scrolling body."""

    def __init__(self, finestra):
        super().__init__()
        self.finestra = finestra
        self.demone = finestra.demone
        self.costruita = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.aggiorna)
        self.intervallo_ms = 1000
        self._v = QVBoxLayout(self)
        self._v.setContentsMargins(0, 0, 0, 0)

    def corpo_scorrevole(self):
        """A vertical layout inside a scroll area, for pages taller than the window."""
        area = QScrollArea()
        area.setWidgetResizable(True)
        area.setFrameShape(QFrame.Shape.NoFrame)
        area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        dentro = QWidget()
        v = QVBoxLayout(dentro)
        v.setContentsMargins(22, 18, 22, 18)
        v.setSpacing(14)
        area.setWidget(dentro)
        self._v.addWidget(area)
        return v

    def corpo_pieno(self):
        """A layout that fills the page: for the sections with a chart."""
        v = QVBoxLayout()
        v.setContentsMargins(22, 18, 22, 18)
        v.setSpacing(10)
        self._v.addLayout(v)
        return v

    def costruisci(self):
        pass

    def aggiorna(self):
        pass

    def attiva(self):
        if not self.costruita:
            self.costruisci()
            self.costruita = True
        self.aggiorna()
        if self.intervallo_ms:
            self.timer.start(self.intervallo_ms)

    def disattiva(self):
        self.timer.stop()

    def toast(self, testo, secondi=4):
        self.finestra.toast(testo, secondi)


class Finestra(QMainWindow):
    def __init__(self, pagina_iniziale="stato"):
        super().__init__()
        self.setWindowTitle("SkillFishOS Control Center")
        if os.path.exists(ICONA):
            self.setWindowIcon(QIcon(ICONA))
        self.demone = Demone()
        self.bc250 = e_bc250()
        self.pagine = {}
        self.attuale = None

        centro = QWidget()
        centro.setObjectName("centro")
        self.setCentralWidget(centro)
        fuori = QHBoxLayout(centro)
        fuori.setContentsMargins(0, 0, 0, 0)
        fuori.setSpacing(0)

        # --- the column of sections
        lato = QFrame()
        lato.setFixedWidth(168)
        lato.setStyleSheet("QFrame{background:#110d09;border-right:1px solid %s;}" % stile.SCHEDA_BORDO)
        lv = QVBoxLayout(lato)
        lv.setContentsMargins(10, 14, 10, 12)
        lv.setSpacing(2)
        testa = QHBoxLayout()
        logo = QLabel()
        pm = QPixmap(ICONA)
        if not pm.isNull():
            logo.setPixmap(pm.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio,
                                     Qt.TransformationMode.SmoothTransformation))
        testa.addWidget(logo)
        nome = QLabel("<b>SkillFishOS</b><br><span style='color:%s;font-size:10px;'>Control Center</span>"
                      % stile.TESTO_2)
        testa.addWidget(nome)
        testa.addStretch(1)
        lv.addLayout(testa)
        lv.addSpacing(10)
        self.gruppo = QButtonGroup(self)
        self.bottoni = {}
        for chiave, it, en, icona, _mod in SEZIONI:
            b = QPushButton(L(it, en))
            b.setObjectName("lato")
            b.setCheckable(True)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            png = os.path.join(ICONE, icona + ".png")
            if os.path.exists(png):
                b.setIcon(QIcon(png))
                b.setIconSize(QSize(20, 20))
            b.clicked.connect(lambda _c=False, k=chiave: self.mostra(k))
            self.gruppo.addButton(b)
            self.bottoni[chiave] = b
            lv.addWidget(b)
        lv.addStretch(1)
        self.et_versione = QLabel("v%s" % VERSIONE)
        self.et_versione.setStyleSheet("color:%s;font-size:10px;" % stile.TESTO_3)
        lv.addWidget(self.et_versione)
        fuori.addWidget(lato)

        # --- the page
        destra = QVBoxLayout()
        destra.setContentsMargins(0, 0, 0, 0)
        destra.setSpacing(0)
        self.pila = QStackedWidget()
        destra.addWidget(self.pila, 1)
        self.et_toast = QLabel("")
        self.et_toast.setStyleSheet("QLabel{background:#2c2318;color:%s;padding:6px 14px;"
                                    "border-top:1px solid %s;}" % (stile.OTTONE, stile.SCHEDA_BORDO))
        self.et_toast.setWordWrap(True)
        self.et_toast.hide()
        destra.addWidget(self.et_toast)
        fuori.addLayout(destra, 1)
        self._toast_timer = QTimer(self)
        self._toast_timer.setSingleShot(True)
        self._toast_timer.timeout.connect(self.et_toast.hide)

        self._adatta_allo_schermo()
        self.mostra(pagina_iniziale if pagina_iniziale in self.bottoni else "stato")

        # --- a controller drives the window too (D-pad/stick, A, B, LB/RB, Start)
        self.pad = Pad(self)
        self.pad.tasto.connect(self._dal_pad)
        self.pad.collegato.connect(self._pad_collegato)

    def _pad_collegato(self, si):
        if si:
            self.toast(L("Controller: %s. Croce o levetta per muoversi, A conferma, B indietro, LB/RB cambiano sezione.",
                         "Controller: %s. D-pad or stick to move, A confirms, B goes back, LB/RB switch section.")
                       % self.pad.nome, 6)

    def _dal_pad(self, nome):
        chiavi = [k for k, _i, _e, _c, _m in SEZIONI]
        if nome in ("sezione-prec", "sezione-succ"):
            i = chiavi.index(self.attuale) if self.attuale in chiavi else 0
            i = (i + (1 if nome == "sezione-succ" else -1)) % len(chiavi)
            self.mostra(chiavi[i])
            self.bottoni[chiavi[i]].setFocus()
        elif nome == "stato":
            self.mostra("stato")
        elif nome == "ok" and QApplication.focusWidget() is None:
            self.bottoni[self.attuale].setFocus()
        else:
            if QApplication.focusWidget() is None:
                self.bottoni[self.attuale].setFocus()
            invia_tasto(nome)

    def _adatta_allo_schermo(self):
        sc = QApplication.primaryScreen()
        d = sc.availableGeometry() if sc else QRect(0, 0, 1280, 800)
        larg = min(1760, max(1000, int(d.width() * 0.86)))
        alt = min(1080, max(640, int(d.height() * 0.88)))
        self.resize(larg, alt)
        self.move(d.left() + max(0, (d.width() - larg) // 2), d.top() + max(0, (d.height() - alt) // 2))

    def _pagina(self, chiave):
        p = self.pagine.get(chiave)
        if p is None:
            modulo = dict((s[0], s[4]) for s in SEZIONI)[chiave]
            try:
                m = importlib.import_module("sfcc.pagine." + modulo)
                p = m.Pagina(self)
            except Exception as e:
                p = PaginaErrore(self, chiave, e)
            self.pagine[chiave] = p
            self.pila.addWidget(p)
        return p

    def mostra(self, chiave):
        if self.attuale is not None and self.attuale != chiave:
            self.pagine[self.attuale].disattiva()
        p = self._pagina(chiave)
        self.pila.setCurrentWidget(p)
        self.bottoni[chiave].setChecked(True)
        self.attuale = chiave
        p.attiva()

    def toast(self, testo, secondi=4):
        self.et_toast.setText(testo)
        self.et_toast.show()
        self._toast_timer.start(int(secondi * 1000))

    def closeEvent(self, ev):
        self.pad.ferma()
        for p in self.pagine.values():
            try:
                p.disattiva()
                if hasattr(p, "chiudi"):
                    p.chiudi()
            except Exception:
                pass
        self.demone.chiudi()
        super().closeEvent(ev)


class PaginaErrore(PaginaBase):
    """Shown when a page module fails to import: the window still opens."""

    def __init__(self, finestra, chiave, errore):
        super().__init__(finestra)
        self.chiave, self.errore = chiave, errore
        self.intervallo_ms = 0

    def costruisci(self):
        v = self.corpo_scorrevole()
        v.addWidget(stile.intestazione(self.chiave, L(
            "Questa sezione non si e' aperta. L'errore e' qui sotto: e' un guasto nostro, "
            "segnalalo su GitHub.", "This section did not open. The error is below: it is our "
            "fault, please report it on GitHub.")))
        e = QLabel(str(self.errore))
        e.setObjectName("male")
        e.setWordWrap(True)
        v.addWidget(e)
        v.addStretch(1)

# -*- coding: utf-8 -*-
"""The look: brass on dark, uniform background, cards with one big number.

The reference is bc250-control-center by movacx (clean cards, a small caption
and a large value, wide buttons at the bottom of each card). The palette is the
SkillFishSteampunk one already used by the theme and by every other window, so
the Control Center does not look like a different program.
"""
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                             QVBoxLayout, QWidget)

from .comune import Aiuto, L

# --- the palette -----------------------------------------------------------
FONDO = "#15110d"          # the window
SCHEDA = "#1f1913"         # a card
SCHEDA_BORDO = "#33291f"
SCHEDA_ALTA = "#261f18"    # a card that is hovered or selected
TESTO = "#ece0c8"
TESTO_2 = "#b9a27a"        # captions
TESTO_3 = "#7f6f55"        # even quieter
OTTONE = "#d8a849"
OTTONE_SCURO = "#8a6a2a"
ARANCIO = "#e8703a"
ROSSO = "#d85a5a"
VERDE = "#8fbf6a"
AZZURRO = "#7fd4ff"
VIOLA = "#b98cff"
GRIGLIA = "#3a322a"

# chart colours, same as Fan Control so the two read the same
COL_TEMP = ["#e8703a", "#d85a5a", "#c78be0", "#7fd4ff", "#8fbf6a", "#e0d05a", "#b06a3a", "#5a8fd8"]
COL_DUTY = OTTONE
COL_RPM = "#5ad0c0"
COL_WATT = VIOLA
COL_VOLT = "#6a9fd8"
COL_MHZ = OTTONE
COL_CARICO = VERDE

QSS = """
QMainWindow, QWidget#centro { background: %(fondo)s; }
QWidget { color: %(testo)s; font-size: 13px; }
QLabel { background: transparent; }
QLabel#didascalia { color: %(testo2)s; font-size: 11px; letter-spacing: 1px; }
QLabel#numerone { color: %(testo)s; font-size: 40px; font-weight: 800; }
QLabel#unita { color: %(testo2)s; font-size: 15px; font-weight: 600; padding-top: 14px; }
QLabel#titolo_pagina { color: %(ottone)s; font-size: 20px; font-weight: 800; }
QLabel#sotto_pagina { color: %(testo2)s; font-size: 12px; }
QLabel#titolo_scheda { color: %(testo)s; font-size: 14px; font-weight: 700; }
QLabel#quieto { color: %(testo2)s; }
QLabel#bene { color: %(verde)s; font-weight: 600; }
QLabel#male { color: %(arancio)s; font-weight: 600; }
QFrame#scheda { background: %(scheda)s; border: 1px solid %(bordo)s; border-radius: 10px; }
QFrame#scheda:hover { border-color: #4a3d2e; }
QFrame#riga { border-bottom: 1px solid %(bordo)s; }
QPushButton {
  background: #2a2119; color: %(testo)s; border: 1px solid #3f3327;
  border-radius: 8px; padding: 7px 14px; font-weight: 600; min-height: 18px;
}
QPushButton:hover { background: #352a1f; border-color: %(ottone_s)s; }
QPushButton:pressed { background: #201912; }
QPushButton:disabled { color: %(testo3)s; border-color: #2c241b; }
QPushButton#primario { background: #3d2f1c; border-color: %(ottone_s)s; color: #f4e2b8; }
QPushButton#primario:hover { background: #4d3b22; border-color: %(ottone)s; }
QPushButton#pericolo { color: #f0b0a0; }
QPushButton#pericolo:hover { border-color: %(rosso)s; }
QPushButton#lato {
  background: transparent; border: none; border-radius: 8px; text-align: left;
  padding: 8px 12px; color: %(testo2)s; font-weight: 600;
}
QPushButton#lato:hover { background: %(scheda)s; color: %(testo)s; }
QPushButton#lato:checked { background: #2c2318; color: %(ottone)s; border-left: 3px solid %(ottone)s; }
QToolButton { background: transparent; border: none; color: %(testo2)s; }
QToolButton:hover { color: %(testo)s; }
QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit {
  background: #120e0a; color: %(testo)s; border: 1px solid #3f3327; border-radius: 6px; padding: 4px 8px;
}
QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover { border-color: %(ottone_s)s; }
QComboBox QAbstractItemView { background: #1a140e; color: %(testo)s; selection-background-color: #3d2f1c; }
QCheckBox, QRadioButton { spacing: 8px; }
QCheckBox::indicator, QRadioButton::indicator { width: 16px; height: 16px; }
QGroupBox { border: 1px solid %(bordo)s; border-radius: 8px; margin-top: 10px; padding-top: 8px; }
QGroupBox::title { subcontrol-origin: margin; left: 10px; color: %(testo2)s; }
QScrollArea { border: none; background: transparent; }
QScrollBar:vertical { background: transparent; width: 8px; }
QScrollBar::handle:vertical { background: #3f3327; border-radius: 4px; min-height: 24px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background: transparent; height: 8px; }
QScrollBar::handle:horizontal { background: #3f3327; border-radius: 4px; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QSlider::groove:horizontal { height: 4px; background: %(griglia)s; border-radius: 2px; }
QSlider::handle:horizontal { width: 14px; margin: -6px 0; background: %(ottone)s; border-radius: 7px; }
QProgressBar { background: #120e0a; border: 1px solid #3f3327; border-radius: 6px; text-align: center; height: 14px; }
QProgressBar::chunk { background: %(ottone_s)s; border-radius: 5px; }
QTabWidget::pane { border: 1px solid %(bordo)s; border-radius: 8px; }
QTabBar::tab { background: transparent; color: %(testo2)s; padding: 6px 14px; }
QTabBar::tab:selected { color: %(ottone)s; border-bottom: 2px solid %(ottone)s; }
QToolTip { background: #2a2119; color: %(testo)s; border: 1px solid %(ottone_s)s; padding: 4px; }
QMessageBox, QDialog { background: %(fondo)s; }
QTextEdit, QPlainTextEdit { background: #120e0a; color: %(testo)s; border: 1px solid #3f3327; border-radius: 6px; }
QListWidget, QTreeWidget, QTableWidget { background: #120e0a; border: 1px solid #3f3327; border-radius: 6px; }
QListWidget::item:selected, QTreeWidget::item:selected { background: #3d2f1c; }
QHeaderView::section { background: %(scheda)s; color: %(testo2)s; border: none; padding: 4px; }
""" % {"fondo": FONDO, "scheda": SCHEDA, "bordo": SCHEDA_BORDO, "testo": TESTO,
       "testo2": TESTO_2, "testo3": TESTO_3, "ottone": OTTONE, "ottone_s": OTTONE_SCURO,
       "verde": VERDE, "arancio": ARANCIO, "rosso": ROSSO, "griglia": GRIGLIA}


# --- the building blocks ---------------------------------------------------
class Scheda(QFrame):
    """A card: a title with an optional "?", then whatever the page puts in."""
    cliccata = pyqtSignal()

    def __init__(self, titolo="", aiuto="", parent=None):
        super().__init__(parent)
        self.setObjectName("scheda")
        self.v = QVBoxLayout(self)
        self.v.setContentsMargins(16, 12, 16, 14)
        self.v.setSpacing(8)
        if titolo:
            testa = QHBoxLayout()
            testa.setSpacing(6)
            self.titolo = QLabel(titolo)
            self.titolo.setObjectName("titolo_scheda")
            testa.addWidget(self.titolo)
            if aiuto:
                testa.addWidget(Aiuto(aiuto, titolo))
            testa.addStretch(1)
            self.testa = testa
            self.v.addLayout(testa)

    def aggiungi(self, w, peso=0):
        if isinstance(w, QWidget):
            self.v.addWidget(w, peso)
        else:
            self.v.addLayout(w, peso)
        return w

    def riga(self, etichetta, valore="", aiuto=""):
        """A caption on the left and a value on the right; returns the value label."""
        r = QHBoxLayout()
        e = QLabel(etichetta)
        e.setObjectName("quieto")
        r.addWidget(e)
        if aiuto:
            r.addWidget(Aiuto(aiuto, etichetta))
        r.addStretch(1)
        v = QLabel(valore)
        v.setStyleSheet("font-weight:600;")
        v.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        r.addWidget(v)
        self.v.addLayout(r)
        return v

    def bottoni(self, *voci):
        """(text, slot, primary) tuples in one row at the bottom of the card.

        The first row of buttons pushes itself to the bottom: cards in a grid
        share the height of the tallest, and the buttons belong at the foot.
        """
        if not getattr(self, "_spinta", False):
            self.v.addStretch(1)
            self._spinta = True
        r = QHBoxLayout()
        r.setSpacing(8)
        out = []
        for testo, slot, primario in voci:
            b = QPushButton(testo)
            if primario:
                b.setObjectName("primario")
            if slot:
                b.clicked.connect(slot)
            b.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            r.addWidget(b)
            out.append(b)
        self.v.addLayout(r)
        return out

    def mousePressEvent(self, ev):
        self.cliccata.emit()
        super().mousePressEvent(ev)


class Numerone(QWidget):
    """A caption, a large number and its unit: the thing a card is about."""

    def __init__(self, didascalia, unita="", parent=None):
        super().__init__(parent)
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)
        self.didascalia = QLabel(didascalia.upper())
        self.didascalia.setObjectName("didascalia")
        v.addWidget(self.didascalia)
        r = QHBoxLayout()
        r.setSpacing(6)
        self.valore = QLabel("—")
        self.valore.setObjectName("numerone")
        r.addWidget(self.valore)
        self.unita = QLabel(unita)
        self.unita.setObjectName("unita")
        r.addWidget(self.unita)
        r.addStretch(1)
        v.addLayout(r)

    def imposta(self, valore, unita=None, colore=None):
        self.valore.setText("—" if valore is None else str(valore))
        if unita is not None:
            self.unita.setText(unita)
        self.valore.setStyleSheet("color:%s;" % (colore or TESTO))


class Tessera(QFrame):
    """A small value tile: dot of the line colour, name, number with the unit.

    The tiles ARE the legend of the chart next to them: click to show or hide
    the line, double-click to rename it. Nothing is listed twice.
    """
    premuta = pyqtSignal(str)
    rinominata = pyqtSignal(str)

    def __init__(self, chiave, parent=None):
        super().__init__(parent)
        self.chiave = chiave
        # ⚠️ QLabel is a QFrame: a bare "QFrame{border}" rule would box the two
        # labels too. The rule is bound to this object's name instead.
        self.setObjectName("tessera")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        g = QVBoxLayout(self)
        g.setContentsMargins(8, 4, 8, 4)
        g.setSpacing(0)
        self.nome = QLabel("")
        self.valore = QLabel("")
        g.addWidget(self.nome)
        g.addWidget(self.valore)

    def aggiorna(self, s):
        col = s["colore"].name() if isinstance(s["colore"], QColor) else s["colore"]
        acceso = s["visibile"]
        self.nome.setText(s["etichetta"])
        v = s["punti"][-1][1] if s["punti"] else None
        dec = {"C": 1, "%": 0, "rpm": 0, "W": 1, "V": 3, "MHz": 0, "mV": 0}.get(s["unita"], 1)
        unita = {"C": "°C"}.get(s["unita"], s["unita"])
        self.valore.setText("—" if v is None else ("%." + str(dec) + "f %s") % (v, unita))
        self.nome.setStyleSheet("font-size:10px; color:%s; border:none;" % (col if acceso else TESTO_3))
        self.valore.setStyleSheet("font-size:15px; font-weight:bold; color:%s; border:none;"
                                  % (col if acceso else "#8a7c68"))
        self.setStyleSheet("QFrame#tessera { border:1px solid %s; border-radius:5px; background:%s; }"
                           % (col if acceso else GRIGLIA, SCHEDA if acceso else FONDO))

    def mousePressEvent(self, ev):
        self.premuta.emit(self.chiave)

    def mouseDoubleClickEvent(self, ev):
        self.rinominata.emit(self.chiave)


class Stato(QLabel):
    """A coloured badge: good / warning / quiet."""

    def __init__(self, testo="", tono="quieto", parent=None):
        super().__init__(testo, parent)
        # a badge never grows with the row it sits in
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.tono(tono)

    def tono(self, t):
        col = {"bene": VERDE, "male": ARANCIO, "quieto": TESTO_2, "ottone": OTTONE}.get(t, TESTO_2)
        self.setStyleSheet("QLabel{color:%s;border:1px solid %s;border-radius:9px;padding:1px 8px;"
                           "font-size:11px;font-weight:600;}" % (col, col))


LINGUE_SITO = ("it", "en", "pl", "uk", "ru", "es", "pt", "de", "fr")


def url_doc(ancora=""):
    """The documentation page of the Control Center on the site, in the
    language of the system (English when the site does not have it)."""
    from .comune import LANG
    lingua = LANG if LANG in LINGUE_SITO else "en"
    # Italian is the default language of the site: no prefix in the path
    prefisso = "" if lingua == "it" else lingua + "/"
    return "https://skillfishos.com/%sdocs/control-center/%s" % (prefisso, ("#" + ancora) if ancora else "")


def link_doc(ancora=""):
    """The one place the long explanations live: a link to the documentation.
    Short help stays behind the "?" buttons; anything longer goes to the docs."""
    u = url_doc(ancora)
    e = QLabel('<a href="%s" style="color:%s;">%s ↗</a>' % (u, OTTONE, L("Documentazione", "Documentation")))
    e.setOpenExternalLinks(True)
    e.setToolTip(u)
    e.setStyleSheet("font-size:11px;")
    return e


def intestazione(titolo, sotto="", aiuto="", doc=None):
    """The title block at the top of every page. doc: anchor in the docs page."""
    w = QWidget()
    v = QVBoxLayout(w)
    v.setContentsMargins(0, 0, 0, 0)
    v.setSpacing(2)
    r = QHBoxLayout()
    r.setSpacing(8)
    t = QLabel(titolo)
    t.setObjectName("titolo_pagina")
    r.addWidget(t)
    if aiuto:
        r.addWidget(Aiuto(aiuto, titolo))
    if doc is not None:
        r.addWidget(link_doc(doc))
    r.addStretch(1)
    v.addLayout(r)
    if sotto:
        s = QLabel(sotto)
        s.setObjectName("sotto_pagina")
        s.setWordWrap(True)
        v.addWidget(s)
    return w


class GrigliaSchede(QWidget):
    """Cards in equal columns that REFLOW with the width: as many columns as
    fit at LARGHEZZA_SCHEDA each, up to the maximum asked, never less than
    one. A window made narrow stacks the cards instead of squeezing them."""
    LARGHEZZA_SCHEDA = 330

    def __init__(self, schede, colonne=3, parent=None):
        super().__init__(parent)
        from PyQt6.QtWidgets import QGridLayout
        self.schede = list(schede)
        self.massimo = max(1, colonne)
        self.colonne = 0
        self.g = QGridLayout(self)
        self.g.setContentsMargins(0, 0, 0, 0)
        self.g.setHorizontalSpacing(12)
        self.g.setVerticalSpacing(12)
        self._disponi(self.massimo)

    def _disponi(self, n):
        if n == self.colonne:
            return
        for s in self.schede:
            self.g.removeWidget(s)
        for c in range(max(self.colonne, n)):
            self.g.setColumnStretch(c, 0)
        for i, s in enumerate(self.schede):
            self.g.addWidget(s, i // n, i % n)
        for c in range(n):
            self.g.setColumnStretch(c, 1)
        self.colonne = n

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        n = max(1, min(self.massimo, (self.width() + 12) // (self.LARGHEZZA_SCHEDA + 12)))
        self._disponi(n)


def griglia_schede(*schede, colonne=3):
    """Cards laid out in equal columns, wrapping to the next row, reflowing
    to fewer columns when the window gets narrow."""
    return GrigliaSchede(schede, colonne)

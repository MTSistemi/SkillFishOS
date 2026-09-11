# -*- coding: utf-8 -*-
"""The one chart, and the curve editors that live inside it.

One chart per page, scrolling in time, with every reading in it; the thing you
EDIT (a curve) sits in a movable, resizable box in a corner of the same chart.
That is the scheme Fan Control settled on and the Control Center keeps it for
every section: whoever learned one page knows the others.

Five or six units share the chart, so each series is mapped to its own 0-100
scale; the real number is read on the tile, under the pointer (one line at a
time, large) or by clicking a line, which opens it alone with true axes.
"""
from PyQt6.QtCore import QPointF, QRect, Qt, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QFont, QLinearGradient, QPainter, QPainterPath, QPen
from PyQt6.QtWidgets import QSizePolicy, QToolButton, QWidget

from . import stile
from .comune import L

FONDO = QColor(stile.FONDO)
FONDO_INSERTO = QColor("#120e0a")
OTTONE = QColor(stile.OTTONE)
OTTONE_SCURO = QColor(stile.OTTONE_SCURO)
GRIGLIA = QColor(stile.GRIGLIA)
VIVO = QColor(stile.AZZURRO)

DECIMALI = {"C": 1, "%": 0, "rpm": 0, "W": 1, "V": 3, "MHz": 0, "mV": 0}


def _fmt(v, unita):
    return ("%." + str(DECIMALI.get(unita, 1)) + "f %s") % (v, unita)


class Grafico(QWidget):
    """The last minutes, scrolling. Series are fed with carica() or campiona()."""

    FINESTRA = 300

    def __init__(self, inserto=None, parent=None):
        super().__init__(parent)
        self.serie = {}
        self.ordine = []
        self.nuova_serie = None
        self.apri_serie = None
        self.cursore = None
        self.sotto = None
        self._inizio = self._fine = 0.0
        self._n_temp = 0
        self.inserto = inserto
        self._inserto_aperto = True
        self._inserto_pos = None
        self._inserto_dim = None
        if inserto is not None:
            inserto.setParent(self)
            inserto.spostata = self._sposta_inserto
            inserto.ridimensionata = self._ridimensiona_inserto
            self.bottone_inserto = QToolButton(self)
            self.bottone_inserto.setText("▾")
            self.bottone_inserto.setAutoRaise(True)
            self.bottone_inserto.clicked.connect(self._apri_chiudi)
        self.setMinimumHeight(240)
        self.setMinimumWidth(360)
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    # ---- the box in the corner --------------------------------------------
    INS_L, INS_H = 470, 300
    INS_MIN_L, INS_MIN_H = 260, 170

    def _apri_chiudi(self):
        self._inserto_aperto = not self._inserto_aperto
        self.inserto.setVisible(self._inserto_aperto)
        self.bottone_inserto.setText("▾" if self._inserto_aperto else "▸")
        self.update()

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        self._posiziona_inserto()

    def _posiziona_inserto(self):
        if self.inserto is None:
            return
        a = self._area()
        l, h = self._inserto_dim or (self.INS_L, self.INS_H)
        l = max(self.INS_MIN_L, min(a.width(), l))
        h = max(self.INS_MIN_H, min(a.height(), h))
        if self._inserto_pos is None:
            x, y = a.left(), a.bottom() - h
        else:
            x, y = self._inserto_pos
        x = max(a.left(), min(a.right() - l, x))
        y = max(a.top(), min(a.bottom() - h, y))
        self.inserto.setGeometry(QRect(int(x), int(y), int(l), int(h)))
        self.bottone_inserto.setGeometry(QRect(int(x) + int(l) - 21, int(y) + 1, 19, 15))

    def _ridimensiona_inserto(self, l, h):
        if self._inserto_pos is None:
            g = self.inserto.geometry()
            self._inserto_pos = (g.x(), g.y())
        self._inserto_dim = (l, h)
        self._posiziona_inserto()

    def _sposta_inserto(self, punto):
        p = self.mapFromGlobal(punto)
        self._inserto_pos = (p.x(), p.y())
        self._posiziona_inserto()

    # ---- geometry ----------------------------------------------------------
    def _area(self):
        return QRect(42, 10, max(1, self.width() - 54), max(1, self.height() - 34))

    def _y(self, q):
        a = self._area()
        return a.bottom() - max(0.0, min(1.0, q)) * a.height()

    def _colore(self, unita):
        if unita == "C":
            c = stile.COL_TEMP[self._n_temp % len(stile.COL_TEMP)]
            self._n_temp += 1
            return QColor(c)
        return QColor({"%": stile.COL_DUTY, "rpm": stile.COL_RPM, "W": stile.COL_WATT,
                       "V": stile.COL_VOLT, "MHz": stile.COL_MHZ, "mV": stile.COL_VOLT}
                      .get(unita, "#999999"))

    def _nuova(self, chiave, etichetta, unita, colore=None, visibile=None):
        s = {"etichetta": etichetta, "unita": unita, "punti": [],
             "visibile": (unita in ("C", "%", "rpm", "W", "MHz")) if visibile is None else visibile,
             "colore": QColor(colore) if colore else self._colore(unita)}
        self.serie[chiave] = s
        self.ordine.append(chiave)
        return s

    # ---- feeding -----------------------------------------------------------
    def carica(self, storia, meta):
        """History kept by a daemon: {key: {"t0": s, "v": [...]}} plus names."""
        nuove = False
        for chiave, punti in (storia or {}).items():
            etichetta, unita = meta.get(chiave, (chiave, ""))[:2]
            s = self.serie.get(chiave)
            if s is None:
                s = self._nuova(chiave, etichetta, unita)
                nuove = True
            s["etichetta"] = etichetta
            t0 = punti.get("t0") or 0
            s["punti"] = [(t0 + i, v) for i, v in enumerate(punti.get("v") or []) if v is not None]
        if nuove and self.nuova_serie:
            self.nuova_serie()
        self.update()

    def campiona(self, adesso, letture):
        """A sample taken by the page itself: [(key, label, unit, value, colour?)]."""
        nuove = False
        for voce in letture:
            chiave, etichetta, unita, v = voce[:4]
            colore = voce[4] if len(voce) > 4 else None
            if v is None:
                continue
            s = self.serie.get(chiave)
            if s is None:
                s = self._nuova(chiave, etichetta, unita, colore)
                nuove = True
            s["punti"].append((adesso, float(v)))
            taglio = adesso - self.FINESTRA - 5
            while s["punti"] and s["punti"][0][0] < taglio:
                s["punti"].pop(0)
        if nuove and self.nuova_serie:
            self.nuova_serie()
        self.update()

    @staticmethod
    def _scala(unita, valori):
        if unita == "C":
            return 20.0, 100.0
        if unita == "%":
            return 0.0, 100.0
        if unita == "rpm":
            m = max(valori) if valori else 1
            return 0.0, max(500.0, (int(m / 500) + 1) * 500.0)
        if unita == "W":
            m = max(valori) if valori else 1
            return 0.0, max(10.0, (int(m / 10) + 1) * 10.0)
        if unita == "MHz":
            return 0.0, 2400.0
        if unita == "mV":
            return 650.0, 1150.0
        if unita == "V":
            o = sorted(valori)
            med = o[len(o) // 2] if o else 1.0
            return (0.0, 1.0) if med <= 0 else (med * 0.9, med * 1.1)
        return (min(valori) if valori else 0.0), (max(valori) if valori else 1.0)

    def elenco(self):
        return [(k, self.serie[k]) for k in self.ordine if k in self.serie]

    def _visibili(self):
        return [(k, s) for k, s in self.elenco() if s["visibile"] and s["punti"]]

    @staticmethod
    def valore_a(s, quando):
        if not s["punti"]:
            return None
        migliore, dist = None, None
        for tempo, v in s["punti"]:
            d = abs(tempo - quando)
            if dist is None or d < dist:
                migliore, dist = v, d
        return migliore

    # ---- painting ----------------------------------------------------------
    def paintEvent(self, ev):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), FONDO)
        a = self._area()
        p.setFont(QFont(self.font().family(), 8))
        for q in range(0, 101, 20):
            y = self._y(q / 100.0)
            p.setPen(QPen(GRIGLIA, 1))
            p.drawLine(a.left(), int(y), a.right(), int(y))
            p.setPen(QPen(OTTONE_SCURO, 1))
            p.drawText(8, int(y) + 4, "%d%%" % q)
        for i in range(0, 6):
            x = a.left() + a.width() * i / 5.0
            p.setPen(QPen(GRIGLIA, 1))
            p.drawLine(int(x), a.top(), int(x), a.bottom())
            p.setPen(QPen(OTTONE_SCURO, 1))
            sec = int(self.FINESTRA * (5 - i) / 5.0)
            p.drawText(int(x) - (16 if sec else 22), a.bottom() + 16,
                       L("adesso", "now") if sec == 0 else "-%d s" % sec)
        serie = self._visibili()
        if not serie:
            p.setPen(QPen(OTTONE_SCURO, 1))
            p.drawText(a.left() + 12, a.center().y(), L("niente da mostrare", "nothing to show"))
            return
        self._fine = max(s["punti"][-1][0] for _, s in serie)
        self._inizio = self._fine - self.FINESTRA
        for chiave, s in serie:
            valori = [v for _, v in s["punti"]]
            basso, alto = self._scala(s["unita"], valori)
            campo = (alto - basso) or 1.0
            cam = QPainterPath()
            primo = True
            for tempo, v in s["punti"]:
                if tempo < self._inizio:
                    continue
                x = a.left() + (tempo - self._inizio) / float(self.FINESTRA) * a.width()
                y = self._y((v - basso) / campo)
                if primo:
                    cam.moveTo(x, y)
                    primo = False
                else:
                    cam.lineTo(x, y)
            if primo:
                continue
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.setPen(QPen(s["colore"], 2.4 if s["unita"] in ("%", "MHz") else 1.5))
            p.drawPath(cam)
        self._disegna_cursore(p)

    def _disegna_cursore(self, p):
        if self.cursore is None or self.sotto is None:
            return
        s = self.serie.get(self.sotto)
        if not s or not s["punti"]:
            return
        a = self._area()
        x = max(a.left(), min(a.right(), self.cursore.x()))
        quando = self._inizio + (x - a.left()) / float(max(1, a.width())) * self.FINESTRA
        v = self.valore_a(s, quando)
        if v is None:
            return
        basso, alto = self._scala(s["unita"], [y for _, y in s["punti"]])
        y = self._y((v - basso) / ((alto - basso) or 1.0))
        p.setPen(QPen(QColor(216, 168, 73, 130), 1, Qt.PenStyle.DashLine))
        p.drawLine(int(x), a.top(), int(x), a.bottom())
        p.setBrush(QBrush(s["colore"]))
        p.setPen(QPen(FONDO, 2))
        p.drawEllipse(QPointF(x, y), 5.5, 5.5)
        grosso = _fmt(v, s["unita"])
        sec = int(round(self._fine - quando))
        piccolo = "%s  ·  %s" % (s["etichetta"], L("adesso", "now") if sec <= 0 else "-%d s" % sec)
        fg = QFont(self.font().family(), 20, QFont.Weight.Bold)
        fp = QFont(self.font().family(), 9)
        p.setFont(fg)
        fmg = p.fontMetrics()
        lg = fmg.horizontalAdvance(grosso)
        p.setFont(fp)
        fmp = p.fontMetrics()
        lp = fmp.horizontalAdvance(piccolo)
        larg = max(lg, lp) + 22
        alt = fmg.height() + fmp.height() + 18
        bx = x + 16 if x + 16 + larg < a.right() else x - 16 - larg
        by = max(a.top() + 2, min(a.bottom() - alt - 2, y - alt / 2.0))
        p.setBrush(QBrush(QColor(21, 17, 13, 240)))
        p.setPen(QPen(s["colore"], 1))
        p.drawRoundedRect(QRect(int(bx), int(by), int(larg), int(alt)), 5, 5)
        p.setPen(QPen(QColor("#9a8a70"), 1))
        p.setFont(fp)
        p.drawText(int(bx) + 11, int(by) + 6 + fmp.ascent(), piccolo)
        p.setPen(QPen(s["colore"], 1))
        p.setFont(fg)
        p.drawText(int(bx) + 11, int(by) + 10 + fmp.height() + fmg.ascent(), grosso)

    # ---- interaction -------------------------------------------------------
    def mouseMoveEvent(self, ev):
        self.cursore = ev.position()
        self.sotto = self._serie_vicina(self.cursore)
        self.setCursor(Qt.CursorShape.PointingHandCursor if self.sotto else Qt.CursorShape.ArrowCursor)
        self.update()

    def leaveEvent(self, ev):
        self.cursore = None
        self.sotto = None
        self.update()

    def _serie_vicina(self, pos):
        a = self._area()
        if not a.contains(pos.toPoint()):
            return None
        if self.inserto is not None and self._inserto_aperto and self.inserto.geometry().contains(pos.toPoint()):
            return None
        quando = self._inizio + (pos.x() - a.left()) / float(max(1, a.width())) * self.FINESTRA
        migliore, dist = None, None
        for chiave, s in self._visibili():
            v = self.valore_a(s, quando)
            if v is None:
                continue
            basso, alto = self._scala(s["unita"], [x for _, x in s["punti"]])
            y = self._y((v - basso) / ((alto - basso) or 1.0))
            d = abs(y - pos.y())
            if dist is None or d < dist:
                migliore, dist = chiave, d
        return migliore if dist is not None and dist < 40 else None

    def mousePressEvent(self, ev):
        chiave = self._serie_vicina(ev.position())
        if chiave and self.apri_serie:
            self.apri_serie(chiave)


class GraficoSingolo(QWidget):
    """One series alone, with the real numbers on the axes."""

    def __init__(self, grafico, chiave, parent=None):
        super().__init__(parent)
        self.grafico = grafico
        self.chiave = chiave
        self.setMinimumSize(560, 320)
        self.setMouseTracking(True)
        self.cursore = None

    def _area(self):
        return QRect(66, 12, max(1, self.width() - 80), max(1, self.height() - 42))

    def paintEvent(self, ev):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), FONDO)
        a = self._area()
        s = self.grafico.serie.get(self.chiave)
        p.setFont(QFont(self.font().family(), 8))
        if not s or not s["punti"]:
            p.setPen(QPen(OTTONE_SCURO, 1))
            p.drawText(a.left() + 10, a.center().y(), L("ancora nessuna lettura", "no readings yet"))
            return
        valori = [v for _, v in s["punti"]]
        basso, alto = min(valori), max(valori)
        if alto - basso < 1e-9:
            basso, alto = basso - 1.0, alto + 1.0
        margine = (alto - basso) * 0.1
        basso, alto = basso - margine, alto + margine
        campo = alto - basso
        dec = DECIMALI.get(s["unita"], 1)
        for i in range(0, 5):
            y = a.bottom() - a.height() * i / 4.0
            p.setPen(QPen(GRIGLIA, 1))
            p.drawLine(a.left(), int(y), a.right(), int(y))
            p.setPen(QPen(OTTONE_SCURO, 1))
            p.drawText(4, int(y) + 4, ("%." + str(dec) + "f") % (basso + campo * i / 4.0))
        fine = s["punti"][-1][0]
        inizio = fine - self.grafico.FINESTRA
        for i in range(0, 6):
            x = a.left() + a.width() * i / 5.0
            p.setPen(QPen(GRIGLIA, 1))
            p.drawLine(int(x), a.top(), int(x), a.bottom())
            p.setPen(QPen(OTTONE_SCURO, 1))
            sec = int(self.grafico.FINESTRA * (5 - i) / 5.0)
            p.drawText(int(x) - (16 if sec else 22), a.bottom() + 18,
                       L("adesso", "now") if sec == 0 else "-%d s" % sec)
        p.setPen(QPen(OTTONE, 1))
        p.setFont(QFont(self.font().family(), 13, QFont.Weight.Bold))
        p.drawText(6, self.height() - 8, s["unita"])
        p.setFont(QFont(self.font().family(), 8))
        cam = QPainterPath()
        primo = True
        for tempo, v in s["punti"]:
            if tempo < inizio:
                continue
            x = a.left() + (tempo - inizio) / float(self.grafico.FINESTRA) * a.width()
            y = a.bottom() - (v - basso) / campo * a.height()
            if primo:
                cam.moveTo(x, y)
                primo = False
            else:
                cam.lineTo(x, y)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(s["colore"], 2))
        p.drawPath(cam)
        if self.cursore is not None and a.left() <= self.cursore <= a.right():
            quando = inizio + (self.cursore - a.left()) / float(max(1, a.width())) * self.grafico.FINESTRA
            v = self.grafico.valore_a(s, quando)
            if v is not None:
                y = a.bottom() - (v - basso) / campo * a.height()
                p.setPen(QPen(QColor(216, 168, 73, 140), 1, Qt.PenStyle.DashLine))
                p.drawLine(int(self.cursore), a.top(), int(self.cursore), a.bottom())
                p.setBrush(QBrush(s["colore"]))
                p.setPen(QPen(FONDO, 1.5))
                p.drawEllipse(QPointF(self.cursore, y), 4, 4)
                p.setPen(QPen(s["colore"], 1))
                p.setFont(QFont(self.font().family(), 9, QFont.Weight.Bold))
                sec = int(round(fine - quando))
                p.drawText(int(self.cursore) + 8, int(y) - 8, "%s  (%s)" % (
                    _fmt(v, s["unita"]), L("adesso", "now") if sec <= 0 else "-%d s" % sec))

    def mouseMoveEvent(self, ev):
        self.cursore = ev.position().x()
        self.update()

    def leaveEvent(self, ev):
        self.cursore = None
        self.update()


class Inserto(QWidget):
    """The movable, resizable box inside the chart. Subclasses draw the curve.

    Points are [x, y] pairs in the curve's own units; X_MIN/X_MAX and
    Y_MIN/Y_MAX are fixed on purpose: an axis that follows the data makes two
    different curves look the same.
    """
    X_MIN, X_MAX = 0.0, 100.0
    Y_MIN, Y_MAX = 0.0, 100.0
    X_PASSO_ETICHETTA = 20
    Y_PASSO = 10
    X_FMT = "%d"
    Y_FMT = "%d"
    TITOLO = "Curve"
    RAGGIO = 5
    MANIGLIA = 17
    ANGOLO = 15
    MONOTONA = True             # y may not go down as x goes up
    X_FISSA = False             # points may only move vertically
    cambiata = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.punti = []
        self.vivo = None
        self.spostata = None
        self.ridimensionata = None
        self.bloccata = False
        self._trascinato = -1
        self._presa = None
        self._tira = None
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def _area(self):
        return QRect(40, self.MANIGLIA + 6, max(1, self.width() - 52),
                     max(30, self.height() - self.MANIGLIA - 28))

    def _px(self, x, y):
        a = self._area()
        return QPointF(a.left() + (x - self.X_MIN) / (self.X_MAX - self.X_MIN) * a.width(),
                       a.bottom() - (y - self.Y_MIN) / (self.Y_MAX - self.Y_MIN) * a.height())

    def _val(self, pos):
        a = self._area()
        x = self.X_MIN + (pos.x() - a.left()) / max(1, a.width()) * (self.X_MAX - self.X_MIN)
        y = self.Y_MIN + (a.bottom() - pos.y()) / max(1, a.height()) * (self.Y_MAX - self.Y_MIN)
        return (max(self.X_MIN, min(self.X_MAX, x)), max(self.Y_MIN, min(self.Y_MAX, y)))

    def _etichetta_punto(self, x, y):
        return self.Y_FMT % y

    def _clampa(self, x, y):
        return x, y

    def paintEvent(self, ev):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        a = self._area()
        p.fillRect(self.rect(), FONDO_INSERTO)
        p.setPen(QPen(OTTONE_SCURO, 1))
        p.drawRect(0, 0, self.width() - 1, self.height() - 1)
        p.fillRect(QRect(1, 1, self.width() - 2, self.MANIGLIA), QColor("#241f19"))
        p.setPen(QPen(OTTONE, 1))
        p.setFont(QFont(self.font().family(), 8, QFont.Weight.Bold))
        p.drawText(7, self.MANIGLIA - 4, self.TITOLO)
        p.setPen(QPen(OTTONE_SCURO, 1))
        cx = self.width() // 2
        for i in range(-3, 4):
            p.drawLine(cx + i * 4, 5, cx + i * 4, self.MANIGLIA - 5)
        for i in range(3):
            d = 4 + i * 4
            p.drawLine(self.width() - 3, self.height() - 3 - d, self.width() - 3 - d, self.height() - 3)
        p.setFont(QFont(self.font().family(), 7))
        self._griglia(p, a)
        if not self.punti:
            return
        cam = QPainterPath()
        cam.moveTo(a.left(), self._px(self.X_MIN, self.punti[0][1]).y())
        for x, y in self.punti:
            cam.lineTo(self._px(max(self.X_MIN, min(self.X_MAX, x)), y))
        cam.lineTo(a.right(), self._px(self.X_MAX, self.punti[-1][1]).y())
        sotto = QPainterPath(cam)
        sotto.lineTo(a.right(), a.bottom())
        sotto.lineTo(a.left(), a.bottom())
        sotto.closeSubpath()
        sf = QLinearGradient(0, a.top(), 0, a.bottom())
        sf.setColorAt(0.0, QColor(216, 168, 73, 80))
        sf.setColorAt(1.0, QColor(216, 168, 73, 12))
        p.fillPath(sotto, QBrush(sf))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(OTTONE, 2))
        p.drawPath(cam)
        p.setFont(QFont(self.font().family(), 7))
        for x, y in self.punti:
            c = self._px(max(self.X_MIN, min(self.X_MAX, x)), y)
            p.setPen(QPen(QColor("#2b241c"), 2))
            p.setBrush(QBrush(OTTONE))
            p.drawEllipse(c, self.RAGGIO, self.RAGGIO)
            p.setPen(QPen(QColor("#c9b184"), 1))
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawText(int(c.x()) + 7, int(c.y()) - 6, self._etichetta_punto(x, y))
        if self.vivo:
            c = self._px(max(self.X_MIN, min(self.X_MAX, self.vivo[0])),
                         max(self.Y_MIN, min(self.Y_MAX, self.vivo[1])))
            p.setBrush(QBrush(VIVO))
            p.setPen(QPen(QColor("#0d1a20"), 2))
            p.drawEllipse(c, 4.5, 4.5)
        self._extra(p, a)

    def _griglia(self, p, a):
        x = self.X_MIN
        while x <= self.X_MAX + 1e-9:
            xx = self._px(x, self.Y_MIN).x()
            p.setPen(QPen(GRIGLIA, 1))
            p.drawLine(int(xx), a.top(), int(xx), a.bottom())
            p.setPen(QPen(OTTONE_SCURO, 1))
            p.drawText(int(xx) - 10, a.bottom() + 13, self.X_FMT % x)
            x += self.X_PASSO_ETICHETTA
        y = self.Y_MIN
        i = 0
        while y <= self.Y_MAX + 1e-9:
            yy = self._px(self.X_MIN, y).y()
            p.setPen(QPen(GRIGLIA if i % 2 else QColor("#4a4036"), 1))
            p.drawLine(a.left(), int(yy), a.right(), int(yy))
            if i % 2 == 0:
                p.setPen(QPen(OTTONE_SCURO, 1))
                p.drawText(3, int(yy) + 4, self.Y_FMT % y)
            y += self.Y_PASSO
            i += 1

    def _extra(self, p, a):
        pass

    def _vicino(self, pos):
        for i, (x, y) in enumerate(self.punti):
            c = self._px(max(self.X_MIN, min(self.X_MAX, x)), y)
            if (c.x() - pos.x()) ** 2 + (c.y() - pos.y()) ** 2 <= (self.RAGGIO + 7) ** 2:
                return i
        return -1

    def _nell_angolo(self, pos):
        return pos.x() >= self.width() - self.ANGOLO and pos.y() >= self.height() - self.ANGOLO

    def mousePressEvent(self, ev):
        if self._nell_angolo(ev.position()):
            self._tira = (ev.globalPosition().toPoint(), self.width(), self.height())
            return
        if ev.position().y() <= self.MANIGLIA:
            self._presa = ev.globalPosition().toPoint() - self.pos()
            return
        if self.bloccata:
            return
        i = self._vicino(ev.position())
        if ev.button() == Qt.MouseButton.RightButton:
            if i >= 0 and len(self.punti) > 2 and not self.X_FISSA:
                del self.punti[i]
                self._fatto()
            return
        self._trascinato = i

    def mouseDoubleClickEvent(self, ev):
        if (self.bloccata or self.X_FISSA or ev.position().y() <= self.MANIGLIA
                or self._nell_angolo(ev.position()) or self._vicino(ev.position()) >= 0):
            return
        x, y = self._val(ev.position())
        x, y = self._clampa(x, y)
        self.punti.append([x, y])
        self._fatto()

    def mouseMoveEvent(self, ev):
        if self._tira is not None:
            partenza, l0, h0 = self._tira
            d = ev.globalPosition().toPoint() - partenza
            if self.ridimensionata:
                self.ridimensionata(l0 + d.x(), h0 + d.y())
            return
        if self._presa is not None:
            if self.spostata:
                self.spostata(ev.globalPosition().toPoint() - self._presa)
            return
        if self._trascinato < 0:
            if self._nell_angolo(ev.position()):
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif ev.position().y() <= self.MANIGLIA:
                self.setCursor(Qt.CursorShape.SizeAllCursor)
            elif self._vicino(ev.position()) >= 0 and not self.bloccata:
                self.setCursor(Qt.CursorShape.OpenHandCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)
            return
        x, y = self._val(ev.position())
        i = self._trascinato
        if self.X_FISSA:
            x = self.punti[i][0]
        else:
            if i > 0:
                x = max(x, self.punti[i - 1][0] + 0.5)
            if i < len(self.punti) - 1:
                x = min(x, self.punti[i + 1][0] - 0.5)
        x, y = self._clampa(x, y)
        self.punti[i] = [x, y]
        self.update()

    def mouseReleaseEvent(self, ev):
        self._presa = None
        self._tira = None
        if self._trascinato >= 0:
            self._trascinato = -1
            self._fatto()

    def _fatto(self):
        self.punti.sort()
        if self.MONOTONA:
            for i in range(1, len(self.punti)):
                if self.punti[i][1] < self.punti[i - 1][1]:
                    self.punti[i][1] = self.punti[i - 1][1]
        self.update()
        self.cambiata.emit()

    def imposta(self, punti):
        self.punti = [list(p) for p in punti]
        self.update()

    def aggiorna_vivo(self, x, y):
        self.vivo = None if x is None or y is None else (x, y)
        self.update()


class CurvaVentola(Inserto):
    """Temperature to fan percent, 20-100 C and 0-100 %."""
    X_MIN, X_MAX = 20.0, 100.0
    Y_MIN, Y_MAX = 0.0, 100.0
    X_PASSO_ETICHETTA = 20
    Y_PASSO = 10
    X_FMT = "%d°"
    Y_FMT = "%d%%"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.TITOLO = L("Curva", "Curve")

    def _clampa(self, x, y):
        return round(x, 1), round(y)


class CurvaVF(Inserto):
    """The GPU voltage/frequency curve of the governor: MHz along, mV up.

    ⚠️ The hard limits of the chip are drawn AND enforced: 700-1129 mV is the
    OD_RANGE the driver declares for this ASIC and the governor clamps to it as
    well; a point cannot be dragged outside. The ceiling (freq_max) is drawn
    as a vertical brass line: the curve beyond it exists but is never used.
    Points snap to 5 MHz and 5 mV: finer than that is noise on this rail.
    """
    X_MIN, X_MAX = 300.0, 2300.0
    Y_MIN, Y_MAX = 650.0, 1150.0
    X_PASSO_ETICHETTA = 500
    Y_PASSO = 50
    X_FMT = "%d"
    Y_FMT = "%d"
    MV_MIN, MV_MAX = 700, 1129
    MHZ_MIN, MHZ_MAX = 350, 2300

    def __init__(self, parent=None):
        super().__init__(parent)
        self.TITOLO = L("Curva V/F", "V/F curve")
        self.tetto = 2100

    def _clampa(self, x, y):
        x = max(self.MHZ_MIN, min(self.MHZ_MAX, round(x / 5.0) * 5))
        y = max(self.MV_MIN, min(self.MV_MAX, round(y / 5.0) * 5))
        return int(x), int(y)

    def _etichetta_punto(self, x, y):
        # Fifteen knots 50 MHz apart would pile their labels on top of each
        # other: only the knot being dragged and the last one say their value.
        i = next((n for n, p in enumerate(self.punti) if p[0] == x and p[1] == y), -1)
        if i == self._trascinato or i == len(self.punti) - 1:
            return "%d MHz  %d mV" % (x, y) if i == self._trascinato else "%d" % y
        return ""

    def _griglia(self, p, a):
        # a line every 250 MHz, a number every 500: the labels were colliding
        x = self.X_MIN + 200
        while x <= self.X_MAX + 1e-9:
            xx = self._px(x, self.Y_MIN).x()
            p.setPen(QPen(GRIGLIA, 1))
            p.drawLine(int(xx), a.top(), int(xx), a.bottom())
            if int(x) % 500 == 0:
                p.setPen(QPen(OTTONE_SCURO, 1))
                p.drawText(int(xx) - 10, a.bottom() + 13, "%d" % x)
            x += 250
        y = self.Y_MIN + 50
        while y <= self.Y_MAX - 1e-9:
            yy = self._px(self.X_MIN, y).y()
            p.setPen(QPen(GRIGLIA if int(y) % 100 else QColor("#4a4036"), 1))
            p.drawLine(a.left(), int(yy), a.right(), int(yy))
            if int(y) % 100 == 0:
                p.setPen(QPen(OTTONE_SCURO, 1))
                p.drawText(3, int(yy) + 4, "%d" % y)
            y += 50

    def _extra(self, p, a):
        # the two rails of the chip, and the ceiling
        for mv in (self.MV_MIN, self.MV_MAX):
            yy = self._px(self.X_MIN, mv).y()
            p.setPen(QPen(QColor(216, 90, 90, 120), 1, Qt.PenStyle.DashLine))
            p.drawLine(a.left(), int(yy), a.right(), int(yy))
        xx = self._px(self.tetto, self.Y_MIN).x()
        p.setPen(QPen(OTTONE, 1.5, Qt.PenStyle.DashLine))
        p.drawLine(int(xx), a.top(), int(xx), a.bottom())
        p.setFont(QFont(self.font().family(), 7, QFont.Weight.Bold))
        p.setPen(QPen(OTTONE, 1))
        p.drawText(int(xx) + 4, a.top() + 10, L("tetto %d", "ceiling %d") % self.tetto)
        p.setPen(QPen(OTTONE_SCURO, 1))
        p.setFont(QFont(self.font().family(), 7))
        p.drawText(a.right() - 26, a.bottom() + 13, "MHz")
        p.drawText(3, a.top() + 8, "mV")

    def mv_a(self, mhz):
        """The voltage the curve gives at a clock, interpolated like the governor."""
        pts = self.punti
        if not pts:
            return None
        if mhz <= pts[0][0]:
            return pts[0][1]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            if x0 <= mhz <= x1:
                return y0 + (y1 - y0) * (mhz - x0) / float(max(1, x1 - x0))
        return pts[-1][1]

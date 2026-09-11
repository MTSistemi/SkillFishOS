# -*- coding: utf-8 -*-
"""One unit per chart, real numbers on the axes: what the Monitor uses since
26.09.2. Several series share a chart only when they share the unit, so the Y
axis is always true (degrees, MHz, watts...) and the X axis is time.

The first Monitor mapped every unit onto one 0-100 chart: readable as a
picture, useless as a number. Mattia's verdict: "on the axes there are only
percentages and seconds". Hence this.
"""
import math

from PyQt6.QtCore import QPointF, QRect, Qt, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter, QPainterPath, QPen
from PyQt6.QtWidgets import QSizePolicy, QWidget

from . import stile
from .comune import L

DECIMALI = {"°C": 1, "%": 0, "rpm": 0, "W": 1, "V": 3, "MHz": 0, "mV": 0, "MB": 0}


def _passo_bello(campo, tacche=5):
    """A tick step from the 1-2-5 family so about `tacche` ticks fit."""
    if campo <= 0:
        return 1.0
    grezzo = campo / float(max(1, tacche))
    e = 10 ** math.floor(math.log10(grezzo))
    for m in (1, 2, 5, 10):
        if m * e >= grezzo:
            return m * e
    return 10 * e


class GraficoUnita(QWidget):
    """Several series of ONE unit, drawn with the true scale.

    campiona(t, valori) appends the values whose key is a series of this
    chart; carica(righe) replaces everything (the viewer). The legend is drawn
    in the header: name and current value, click to show or hide a line. The
    hover cursor is shared: the page pushes the time to every chart.
    """
    cursore_mosso = pyqtSignal(object)   # float seconds, or None
    FINESTRA = 300

    def __init__(self, titolo, unita, serie, y_min=None, y_max=None, parent=None):
        super().__init__(parent)
        self.titolo, self.unita = titolo, unita
        self.serie = [(k, e, QColor(c)) for k, e, c in serie]
        self.punti = dict((k, []) for k, _e, _c in self.serie)
        self.visibile = dict((k, True) for k, _e, _c in self.serie)
        self.y_min, self.y_max = y_min, y_max
        self.finestra = self.FINESTRA
        self.cursore_t = None
        self._legenda = {}
        self.setMinimumHeight(190)
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    # ---- data ------------------------------------------------------------------
    def campiona(self, t, valori):
        limite = t - self.finestra - 5
        for k, _e, _c in self.serie:
            v = valori.get(k)
            if v is not None:
                self.punti[k].append((t, float(v)))
            pts = self.punti[k]
            while pts and pts[0][0] < limite:
                pts.pop(0)
        self.update()

    def carica(self, righe):
        """righe: list of (t, dict). The window becomes the whole span."""
        for k in self.punti:
            self.punti[k] = []
        for t, d in righe:
            for k, _e, _c in self.serie:
                v = d.get(k)
                if v is not None:
                    self.punti[k].append((t, float(v)))
        tempi = [t for t, _d in righe]
        self.finestra = max(10.0, float(tempi[-1] - tempi[0])) if tempi else self.FINESTRA
        self.update()

    def azzera(self):
        for k in self.punti:
            self.punti[k] = []
        self.finestra = self.FINESTRA
        self.update()

    def imposta_cursore(self, t):
        self.cursore_t = t
        self.update()

    def ultimo(self, k):
        pts = self.punti.get(k) or []
        return pts[-1][1] if pts else None

    def ha_dati(self):
        return any(self.punti[k] for k, _e, _c in self.serie)

    def _fine(self):
        fine = None
        for pts in self.punti.values():
            if pts:
                fine = pts[-1][0] if fine is None else max(fine, pts[-1][0])
        return fine

    def valore_a(self, k, quando):
        pts = self.punti.get(k) or []
        if not pts or quando < pts[0][0] - 2 or quando > pts[-1][0] + 2:
            return None
        return min(pts, key=lambda p: abs(p[0] - quando))[1]

    # ---- geometry --------------------------------------------------------------
    def _area(self):
        return QRect(58, 30, max(1, self.width() - 68), max(1, self.height() - 52))

    def _scala(self):
        valori = []
        for k, _e, _c in self.serie:
            if self.visibile[k]:
                valori += [v for _t, v in self.punti[k]]
        if self.y_min is not None and self.y_max is not None:
            return float(self.y_min), float(self.y_max)
        if not valori:
            return 0.0, 1.0
        basso, alto = min(valori), max(valori)
        if self.y_min is not None:
            basso = float(self.y_min)
        if alto - basso < 1e-9:
            alto = basso + (abs(basso) * 0.1 or 1.0)
        passo = _passo_bello(alto - basso, 4)
        basso = math.floor(basso / passo) * passo
        alto = (math.floor(alto / passo) + 1) * passo
        return basso, alto

    # ---- painting --------------------------------------------------------------
    def paintEvent(self, ev):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor(stile.SCHEDA))
        p.setPen(QPen(QColor(stile.SCHEDA_BORDO), 1))
        p.drawRect(0, 0, self.width() - 1, self.height() - 1)
        a = self._area()
        ottone, scuro, griglia = QColor(stile.OTTONE), QColor(stile.OTTONE_SCURO), QColor(stile.GRIGLIA)
        dec = DECIMALI.get(self.unita, 1)
        # header: title with the unit, then the legend with the values
        p.setPen(QPen(ottone, 1))
        p.setFont(QFont(self.font().family(), 10, QFont.Weight.Bold))
        capo = "%s  (%s)" % (self.titolo, self.unita)
        p.drawText(10, 19, capo)
        x = 10 + p.fontMetrics().horizontalAdvance(capo) + 18
        p.setFont(QFont(self.font().family(), 8))
        self._legenda = {}
        for k, e, c in self.serie:
            v = self.valore_a(k, self.cursore_t) if self.cursore_t is not None else self.ultimo(k)
            testo = "%s %s" % (e, "—" if v is None else ("%." + str(dec) + "f") % v)
            larg = p.fontMetrics().horizontalAdvance(testo) + 16
            self._legenda[k] = QRect(x, 4, larg, 18)
            col = c if self.visibile[k] else QColor(stile.TESTO_3)
            p.setBrush(QBrush(col))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(QPointF(x + 5, 13), 3.5, 3.5)
            p.setPen(QPen(col, 1))
            p.drawText(x + 12, 17, testo)
            x += larg + 6
        # grid, Y labels with the true numbers
        basso, alto = self._scala()
        campo = (alto - basso) or 1.0
        passo = _passo_bello(campo, 4)
        y = basso
        p.setFont(QFont(self.font().family(), 8))
        while y <= alto + 1e-9:
            yy = a.bottom() - (y - basso) / campo * a.height()
            p.setPen(QPen(griglia, 1))
            p.drawLine(a.left(), int(yy), a.right(), int(yy))
            p.setPen(QPen(scuro, 1))
            testo = ("%." + str(dec) + "f") % y
            p.drawText(a.left() - 6 - p.fontMetrics().horizontalAdvance(testo), int(yy) + 4, testo)
            y += passo
        fine = self._fine()
        inizio = (fine - self.finestra) if fine is not None else 0.0
        for i in range(0, 6):
            xx = a.left() + a.width() * i / 5.0
            p.setPen(QPen(griglia, 1))
            p.drawLine(int(xx), a.top(), int(xx), a.bottom())
            sec = int(round(self.finestra * (5 - i) / 5.0))
            p.setPen(QPen(scuro, 1))
            if sec == 0:
                testo = L("adesso", "now")
            elif sec < 120:
                testo = "-%d s" % sec
            else:
                testo = "-%d min" % (sec // 60)
            p.drawText(int(xx) - p.fontMetrics().horizontalAdvance(testo) // 2, a.bottom() + 16, testo)
        if fine is None:
            p.setPen(QPen(scuro, 1))
            p.drawText(a.left() + 10, a.center().y(), L("ancora nessuna lettura", "no readings yet"))
            return
        # the lines
        for k, _e, c in self.serie:
            if not self.visibile[k]:
                continue
            cam = QPainterPath()
            primo = True
            for t, v in self.punti[k]:
                if t < inizio:
                    continue
                xv = a.left() + (t - inizio) / float(self.finestra) * a.width()
                yv = a.bottom() - (v - basso) / campo * a.height()
                if primo:
                    cam.moveTo(xv, yv)
                    primo = False
                else:
                    cam.lineTo(xv, yv)
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.setPen(QPen(c, 1.6))
            p.drawPath(cam)
        # the shared cursor
        if self.cursore_t is not None and inizio <= self.cursore_t <= fine + 1:
            xv = a.left() + (self.cursore_t - inizio) / float(self.finestra) * a.width()
            p.setPen(QPen(QColor(216, 168, 73, 140), 1, Qt.PenStyle.DashLine))
            p.drawLine(int(xv), a.top(), int(xv), a.bottom())
            for k, _e, c in self.serie:
                if not self.visibile[k]:
                    continue
                v = self.valore_a(k, self.cursore_t)
                if v is None:
                    continue
                yv = a.bottom() - (v - basso) / campo * a.height()
                p.setBrush(QBrush(c))
                p.setPen(QPen(QColor(stile.SCHEDA), 1.5))
                p.drawEllipse(QPointF(xv, yv), 3.5, 3.5)

    # ---- mouse -----------------------------------------------------------------
    def mouseMoveEvent(self, ev):
        a = self._area()
        fine = self._fine()
        if fine is None or not (a.left() <= ev.position().x() <= a.right()):
            self.cursore_mosso.emit(None)
            return
        inizio = fine - self.finestra
        self.cursore_mosso.emit(inizio + (ev.position().x() - a.left()) / float(max(1, a.width())) * self.finestra)

    def leaveEvent(self, ev):
        self.cursore_mosso.emit(None)

    def mousePressEvent(self, ev):
        for k, r in self._legenda.items():
            if r.contains(ev.position().toPoint()):
                self.visibile[k] = not self.visibile[k]
                self.update()
                return

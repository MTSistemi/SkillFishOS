# -*- coding: utf-8 -*-
"""The cluster, drawn: one row per board, memory, load, watts.

Why not a table: the number that matters is how much memory the cluster has
altogether, and a table of figures does not show it. One bar per board, stacked,
with the total across the top — you see at a glance whether the next model fits.

⚠️ MEMORY HERE MEANS VRAM + GTT. On a BC-250 they are the same chip: the GPU
gets half a gigabyte of "VRAM" and everything else through GTT, so showing VRAM
alone would say 0.5 GB on a board that can hold a 13 GB model.

⚠️ AND THE LOAD CAN BE UNKNOWN. On gfx1013 the SMU does not report GPU activity
(it returns 0xFFFF, which is where MangoHud's famous 655% comes from):
skillfish-gpu-util samples it with radeontop instead. If that service is not
running the figure is -1, and -1 is drawn as "?" rather than as zero, because
zero would be a lie.
"""
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QFont, QLinearGradient, QPainter, QPen
from PyQt6.QtWidgets import QSizePolicy, QWidget

FONDO = "#15110d"
SCHEDA = "#1f1913"
BORDO = "#33291f"
TESTO = "#ece0c8"
TESTO_2 = "#b9a27a"
TESTO_3 = "#7f6f55"
OTTONE = "#d8a849"
OTTONE_SC = "#8a6a2a"
VERDE = "#8fbf6a"
ROSSO = "#d85a5a"
AZZURRO = "#7fd4ff"
VIOLA = "#b98cff"


def _gb(b):
    return (b or 0) / (1024.0 ** 3)


class Cluster(QWidget):
    """Una riga per scheda: memoria, carico, watt, gradi."""

    def __init__(self):
        super().__init__()
        self.dati = {"schede": [], "memoria_totale": 0, "memoria_usata": 0,
                     "watt_totali": 0}
        self.setMinimumHeight(150)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def aggiorna(self, dati):
        if isinstance(dati, dict) and dati.get("schede") is not None:
            self.dati = dati
            n = max(1, len(dati["schede"]))
            # 46 px a scheda piu' l'intestazione: cosi' la finestra non si
            # allarga da sola quando qualcuno aggiunge la terza.
            self.setMinimumHeight(58 + n * 52)
            self.updateGeometry()
            self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        W = self.width()
        y = 0

        schede = self.dati.get("schede") or []
        tot = _gb(self.dati.get("memoria_totale"))
        uso = _gb(self.dati.get("memoria_usata"))
        libera = max(0.0, tot - uso)

        # --- l'intestazione: il numero per cui si accende un cluster ---------
        f = QFont()
        f.setPointSize(20)
        f.setBold(True)
        p.setFont(f)
        p.setPen(QColor(OTTONE))
        p.drawText(QRectF(0, y, W, 30), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                   "%.1f GB" % libera)
        f.setPointSize(10)
        f.setBold(False)
        p.setFont(f)
        p.setPen(QColor(TESTO_2))
        larg = p.fontMetrics().horizontalAdvance("%.1f GB " % libera) + 66
        p.drawText(QRectF(larg, y, W - larg, 30),
                   Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                   "liberi su %.1f GB · %d schede · %d W"
                   % (tot, len(schede), self.dati.get("watt_totali", 0)))
        y += 34

        if not schede:
            p.setPen(QColor(TESTO_3))
            p.drawText(QRectF(0, y, W, 40), Qt.AlignmentFlag.AlignCenter,
                       "nessuna scheda")
            return

        for s in schede:
            self._riga(p, s, y, W)
            y += 52

    def _riga(self, p, s, y, W):
        f = QFont()
        f.setPointSize(10)
        p.setFont(f)

        # il nome, e un pallino che dice se il nodo risponde
        col = VERDE if s.get("nodo") else (TESTO_3 if s.get("locale") else ROSSO)
        p.setBrush(QColor(col))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QRectF(2, y + 9, 8, 8))

        p.setPen(QColor(TESTO))
        nome = s.get("nome") or s.get("ip") or "?"
        if s.get("locale"):
            nome += "  (questa)"
        p.drawText(QRectF(16, y + 2, 190, 16),
                   Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, nome)

        if s.get("errore"):
            p.setPen(QColor(ROSSO))
            p.drawText(QRectF(210, y + 2, W - 210, 16),
                       Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                       s["errore"])
            return

        # --- i numeri, a destra ---------------------------------------------
        carico = s.get("carico", -1)
        testo = "%s   %d W   %d MHz   %d °C" % (
            ("%d%%" % carico) if carico >= 0 else "?",
            s.get("watt", 0), s.get("clock", 0), s.get("temp", 0))
        p.setPen(QColor(TESTO_2))
        p.drawText(QRectF(W - 230, y + 2, 228, 16),
                   Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, testo)

        # --- la barra della memoria -----------------------------------------
        tot = _gb(s.get("vram_totale")) + _gb(s.get("gtt_totale"))
        uso = _gb(s.get("vram_usata")) + _gb(s.get("gtt_usata"))
        frazione = min(1.0, uso / tot) if tot else 0.0

        bx, bh = 16, 18
        by = y + 21
        bw = W - bx - 2
        p.setPen(QPen(QColor(BORDO), 1))
        p.setBrush(QColor("#0e0b08"))
        p.drawRoundedRect(QRectF(bx, by, bw, bh), 3, 3)

        if frazione > 0:
            g = QLinearGradient(bx, 0, bx + bw * frazione, 0)
            # Sopra l'85% il colore vira: e' il punto oltre il quale il modello
            # dopo non ci sta piu', e va visto senza leggere i numeri.
            g.setColorAt(0.0, QColor(OTTONE_SC))
            g.setColorAt(1.0, QColor(ROSSO if frazione > 0.85 else OTTONE))
            p.setBrush(g)
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(QRectF(bx + 1, by + 1, max(2.0, (bw - 2) * frazione),
                                     bh - 2), 2, 2)

        # e il carico, come tacca sopra la barra: due informazioni diverse,
        # due segni diversi, mai la stessa barra che dice due cose.
        # ⚠️ Solo con carico VERO: a zero la tacca finirebbe appiccicata al
        # bordo sinistro e sembrerebbe un difetto del disegno.
        if carico > 0:
            x = bx + 1 + (bw - 2) * min(1.0, carico / 100.0)
            p.setPen(QPen(QColor(AZZURRO), 2))
            p.drawLine(QRectF(x, by - 3, x, by + bh + 3).topLeft().toPoint(),
                       QRectF(x, by - 3, x, by + bh + 3).bottomLeft().toPoint())

        # ⚠️ Il testo va a DESTRA dentro la barra, non a sinistra: a sinistra
        # finisce sopra il riempimento in ottone e non si legge piu'. A destra
        # lo sfondo e' scuro finche' la scheda non e' quasi piena, e quando lo
        # e' il numero non serve piu' perche' lo dice il colore.
        f.setPointSize(9)
        p.setFont(f)
        p.setPen(QColor(TESTO_2))
        p.drawText(QRectF(bx + 6, by, bw - 12, bh),
                   Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                   "%.1f / %.1f GB" % (uso, tot))

# -*- coding: utf-8 -*-
"""Monitor: every reading in one chart, the per-thread bars, and the recorder.

Same scheme as the other sections: tiles on the left are the legend, one chart
in the middle. Press REC and the session goes to a .sfmon file (CSV) that this
page reopens with a scrubber, second by second. Sensors come from
skillfish-hud-val, the same source the HUD reads.
"""
import csv
import datetime
import math
import os
import re
import shutil
import subprocess
import time

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QFont, QLinearGradient, QPainter, QPen
from PyQt6.QtWidgets import (QComboBox, QFileDialog, QFrame, QHBoxLayout, QLabel, QMessageBox,
                             QPushButton, QScrollArea, QSlider, QVBoxLayout, QWidget)

from .. import stile
from ..comune import L, Aiuto
from ..finestra import PaginaBase
from ..grafico import Grafico, GraficoSingolo
from ..stile import Tessera, intestazione
from .tuner import Pannello

REC_DIR = os.path.expanduser("~/SkillFishOS-benchmarks")
SFMON_EXT = ".sfmon"
HUD = shutil.which("skillfish-hud-val") or "/usr/local/bin/skillfish-hud-val"

# key, label (it, en), unit, colour
SERIE = [
    ("cpu_temp", ("CPU °C", "CPU °C"), "C", "#e8c878"),
    ("gpu_temp", ("GPU °C", "GPU °C"), "C", stile.ARANCIO),
    ("cpu_load", ("Carico CPU", "CPU load"), "%", "#5fd24f"),
    ("gpu_util", ("Carico GPU", "GPU load"), "%", "#49b6e0"),
    ("cpu_mhz", ("CPU MHz", "CPU MHz"), "MHz", "#9bd24f"),
    ("gpu_freq", ("GPU MHz", "GPU MHz"), "MHz", stile.OTTONE),
    ("gpu_power", ("GPU W", "GPU W"), "W", stile.VIOLA),
    ("gpu_mv", ("GPU mV", "GPU mV"), "mV", stile.COL_VOLT),
    ("cpu_mv", ("CPU mV", "CPU mV"), "mV", "#e8a878"),
    ("fan", ("Ventola", "Fan"), "rpm", stile.COL_RPM),
]
REC_KEYS = ["cpu_temp", "gpu_temp", "cpu_load", "gpu_util", "cpu_mhz", "gpu_freq",
            "gpu_power", "gpu_mv", "cpu_mv", "fan", "vram"]


def _num(s):
    if s is None:
        return None
    m = re.search(r'-?\d+(?:\.\d+)?', str(s))
    return float(m.group()) if m else None


def read_all():
    out = {}
    try:
        txt = subprocess.run([HUD, "all"], capture_output=True, text=True, timeout=1.2).stdout
        for line in txt.splitlines():
            parts = line.split(None, 1)
            if len(parts) == 2:
                out[parts[0]] = _num(parts[1])
    except Exception:
        pass
    return out


def cpu_load_pct(prev):
    try:
        with open("/proc/stat") as fh:
            f = fh.readline().split()[1:]
        vals = [int(x) for x in f]
        idle = vals[3] + (vals[4] if len(vals) > 4 else 0)
        total = sum(vals)
        if prev is None:
            return None, (total, idle)
        dt, di = total - prev[0], idle - prev[1]
        pct = (100.0 * (dt - di) / dt) if dt > 0 else None
        return (max(0.0, min(100.0, pct)) if pct is not None else None), (total, idle)
    except Exception:
        return None, prev


_TOPO = {}


def cpu_threads():
    base = "/sys/devices/system/cpu"
    try:
        cpus = sorted(int(d[3:]) for d in os.listdir(base) if re.match(r"cpu\d+$", d))
    except Exception:
        return []
    mhz = {}
    try:
        cur = None
        with open("/proc/cpuinfo") as fh:
            for ln in fh:
                if ln.startswith("processor"):
                    cur = int(ln.split(":")[1])
                elif ln.lower().startswith("cpu mhz") and cur is not None:
                    mhz[cur] = float(ln.split(":")[1])
    except Exception:
        pass
    out = []
    for c in cpus:
        try:
            with open("%s/cpu%d/online" % (base, c)) as fh:
                on = fh.read().strip() == "1"
        except Exception:
            on = True
        try:
            with open("%s/cpu%d/topology/core_id" % (base, c)) as fh:
                _TOPO[c] = int(fh.read().strip())
        except Exception:
            pass
        out.append((c, _TOPO.get(c, c // 2), mhz.get(c) if on else None))
    return out


class BarreCore(QWidget):
    """One bar per logical CPU, grouped by core, brass to ember as it climbs."""

    def __init__(self):
        super().__init__()
        self.threads = []
        self.setMinimumHeight(140)
        self.setMaximumHeight(170)

    def push(self, threads):
        self.threads = threads or []
        self.update()

    def _colore(self, t):
        a, b = ((0x6b, 0x5a, 0x34), (0xd8, 0xa8, 0x49)) if t < 0.5 else ((0xd8, 0xa8, 0x49), (0xe0, 0x6b, 0x39))
        k = (t / 0.5) if t < 0.5 else ((t - 0.5) / 0.5)
        return QColor(*[int(a[i] + (b[i] - a[i]) * k) for i in range(3)])

    def paintEvent(self, _e):
        w, h = self.width(), self.height()
        if w <= 2 or h <= 2:
            return
        p = QPainter(self)
        try:
            p.setRenderHint(QPainter.RenderHint.Antialiasing)
            p.fillRect(self.rect(), QColor(stile.FONDO))
            live = [m for (_c, _k, m) in self.threads if m is not None]
            f = QFont(self.font().family(), 9, QFont.Weight.Bold)
            p.setFont(f)
            p.setPen(QColor(stile.OTTONE))
            p.drawText(8, 16, L("Frequenza per thread (MHz)", "Per-thread clock (MHz)"))
            if live:
                p.setPen(QColor(stile.TESTO_2))
                s = "min %d  ·  %s %d  ·  max %d  ·  %d/%d" % (round(min(live)), L("media", "avg"), round(sum(live) / len(live)), round(max(live)), len(live), len(self.threads))
                p.drawText(w - 8 - p.fontMetrics().horizontalAdvance(s), 16, s)
            if not self.threads:
                return
            gx0, gy0, gx1, gy1 = 44, 26, w - 8, h - 18
            gw, gh = gx1 - gx0, gy1 - gy0
            hi = max(1000.0, max(live) if live else 0.0)
            hi = math.ceil(hi / 500.0) * 500.0
            ft = QFont(self.font().family(), 7)
            p.setFont(ft)
            for i in range(5):
                yy = int(gy0 + gh * i / 4)
                p.setPen(QPen(QColor(stile.GRIGLIA), 1))
                p.drawLine(gx0, yy, gx1, yy)
                txt = "%d" % round(hi - hi * i / 4.0)
                p.setPen(QColor(stile.OTTONE_SCURO))
                p.drawText(gx0 - 4 - p.fontMetrics().horizontalAdvance(txt), yy + 3, txt)
            n = len(self.threads)
            slot = gw / float(n)
            bw = max(4.0, slot * 0.62)
            for i, (cpu, core, mhz) in enumerate(self.threads):
                shift = (slot * 0.10) * (1 if (i % 2) else -1) if n > 4 else 0.0
                x = gx0 + slot * i + (slot - bw) / 2.0 + shift
                if mhz is None:
                    p.setBrush(Qt.BrushStyle.NoBrush)
                    p.setPen(QPen(QColor(216, 168, 73, 55), 1, Qt.PenStyle.DashLine))
                    p.drawRoundedRect(int(x), gy1 - 14, int(bw), 14, 3, 3)
                else:
                    t = max(0.0, min(1.0, mhz / hi))
                    bh = max(2.0, gh * t)
                    col = self._colore(t)
                    grad = QLinearGradient(0, gy1 - bh, 0, gy1)
                    c0, c1 = QColor(col), QColor(col)
                    c0.setAlpha(235)
                    c1.setAlpha(110)
                    grad.setColorAt(0, c0)
                    grad.setColorAt(1, c1)
                    p.setPen(Qt.PenStyle.NoPen)
                    p.setBrush(QBrush(grad))
                    p.drawRoundedRect(int(x), int(gy1 - bh), int(bw), int(bh), 3, 3)
                    if bw >= 26:
                        p.setPen(QColor("#e8c878"))
                        v = "%d" % round(mhz)
                        p.drawText(int(x + (bw - p.fontMetrics().horizontalAdvance(v)) / 2), int(max(gy0 + 9, gy1 - bh - 3)), v)
                lab = "%d" % cpu if bw < 26 else "%d·%d" % (core, cpu)
                p.setPen(QColor(stile.TESTO_3))
                p.drawText(int(x + (bw - p.fontMetrics().horizontalAdvance(lab)) / 2), gy1 + 12, lab)
        finally:
            p.end()


class Campionatore(QThread):
    campione = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._intervallo = 0.75
        self._stop = False
        self._prev = None

    def imposta_ms(self, ms):
        self._intervallo = max(0.1, float(ms) / 1000.0)

    def ferma(self):
        self._stop = True

    def run(self):
        while not self._stop:
            vals = read_all()
            pct, self._prev = cpu_load_pct(self._prev)
            vals["cpu_load"] = pct
            vals["_threads"] = cpu_threads()
            vals["_t"] = time.time()
            if self._stop:
                break
            self.campione.emit(vals)
            t = 0.0
            while t < self._intervallo and not self._stop:
                self.msleep(50)
                t += 0.05


class Pagina(PaginaBase):
    def __init__(self, finestra):
        super().__init__(finestra)
        self.intervallo_ms = 0            # the sampler thread paces this page
        self.tessere = {}
        self.pannelli_serie = {}
        self.campionatore = None
        self._rec = None
        self._viewer = None

    def costruisci(self):
        v = self.corpo_pieno()
        testa = QHBoxLayout()
        testa.addWidget(intestazione("Monitor", "", L(
            "Tutte le letture in un grafico solo: temperature, carichi, frequenze, watt, tensioni, "
            "ventola. Le tessere accendono e spengono le linee; un clic su una linea la apre da "
            "sola con i numeri veri. REC scrive la sessione in un file .sfmon che si riapre da qui "
            "e si scorre secondo per secondo.",
            "Every reading in one chart: temperatures, loads, clocks, watts, voltages, fan. The "
            "tiles switch lines on and off; clicking a line opens it alone with real numbers. REC "
            "writes the session to a .sfmon file that reopens here and scrubs second by second.")))
        testa.addStretch(1)
        self.b_apri = QPushButton(L("Apri", "Open"))
        self.b_apri.clicked.connect(self._apri)
        testa.addWidget(self.b_apri)
        self.b_csv = QPushButton("CSV")
        self.b_csv.setToolTip(L("Esporta la registrazione aperta o l'ultima fatta come CSV",
                                "Export the open recording, or the last one made, as CSV"))
        self.b_csv.clicked.connect(self._esporta_csv)
        testa.addWidget(self.b_csv)
        self.b_rec = QPushButton("● REC")
        self.b_rec.setCheckable(True)
        self.b_rec.setStyleSheet("QPushButton:checked{background:#7a2a1f;border-color:#e05540;color:#fff;}")
        self.b_rec.toggled.connect(self._rec_toggle)
        testa.addWidget(self.b_rec)
        testa.addWidget(QLabel(L("Aggiornamento", "Refresh")))
        self.iv = QComboBox()
        for ms, lab in ((300, "0.3 s"), (500, "0.5 s"), (750, "0.75 s"), (1000, "1 s"), (2000, "2 s")):
            self.iv.addItem(lab, ms)
        self.iv.setCurrentIndex(2)
        self.iv.currentIndexChanged.connect(lambda: self.campionatore and self.campionatore.imposta_ms(self.iv.currentData()))
        testa.addWidget(self.iv)
        v.addLayout(testa)

        corpo = QHBoxLayout()
        corpo.setSpacing(10)
        v.addLayout(corpo, 1)
        lato = QScrollArea()
        lato.setWidgetResizable(True)
        lato.setFrameShape(QFrame.Shape.NoFrame)
        lato.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        lato.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        lato.setFixedWidth(168)
        gabbia = QWidget()
        self.colonna = QVBoxLayout(gabbia)
        self.colonna.setContentsMargins(0, 0, 4, 0)
        self.colonna.setSpacing(5)
        self.colonna.addStretch(1)
        lato.setWidget(gabbia)
        corpo.addWidget(lato, 0)
        destra = QVBoxLayout()
        destra.setSpacing(8)
        corpo.addLayout(destra, 1)
        self.grafico = Grafico()
        self.grafico.nuova_serie = self._rifai_tessere
        self.grafico.apri_serie = self._apri_serie
        destra.addWidget(self.grafico, 1)
        self.barre = BarreCore()
        destra.addWidget(self.barre)
        # the scrubber, shown only with a recording open
        self.riga_scrub = QHBoxLayout()
        self.et_scrub = QLabel("")
        self.et_scrub.setObjectName("quieto")
        self.scrub = QSlider(Qt.Orientation.Horizontal)
        self.scrub.valueChanged.connect(self._scorri)
        self.b_chiudi = QPushButton(L("Torna al vivo", "Back to live"))
        self.b_chiudi.clicked.connect(self._chiudi_registrazione)
        self.riga_scrub.addWidget(self.et_scrub)
        self.riga_scrub.addWidget(self.scrub, 1)
        self.riga_scrub.addWidget(self.b_chiudi)
        destra.addLayout(self.riga_scrub)
        self._mostra_scrub(False)
        file = getattr(self.finestra, "file_da_aprire", None)
        if file:
            self.finestra.file_da_aprire = None
            self._carica(file)

    def _mostra_scrub(self, si):
        for w in (self.et_scrub, self.scrub, self.b_chiudi):
            w.setVisible(si)

    # ---- live -----------------------------------------------------------------------
    def attiva(self):
        super().attiva()
        if self.campionatore is None and self._viewer is None:
            self.campionatore = Campionatore()
            self.campionatore.imposta_ms(self.iv.currentData())
            self.campionatore.campione.connect(self._campione)
            self.campionatore.start()

    def disattiva(self):
        super().disattiva()
        # keep sampling while recording, stop otherwise: the page is not visible
        if self.campionatore is not None and not self._rec:
            self.campionatore.ferma()
            self.campionatore.wait(1500)
            self.campionatore = None

    def chiudi(self):
        if self._rec:
            self.b_rec.setChecked(False)
        self.disattiva()

    def _campione(self, vals):
        if self._viewer is not None:
            return
        self.barre.push(vals.get("_threads"))
        adesso = vals.get("_t") or time.time()
        letture = [(k, L(*lab), unita, vals.get(k), col) for k, lab, unita, col in SERIE]
        self.grafico.campiona(adesso, letture)
        for chiave, serie in self.grafico.elenco():
            w = self.tessere.get(chiave)
            if w is not None:
                w.aggiorna(serie)
        if self._rec:
            wtr, fh, rows, t0 = self._rec
            row = [round(adesso - t0, 2)] + [vals.get(k) for k in REC_KEYS]
            wtr.writerow(row)
            rows.append(row)

    def _rifai_tessere(self):
        while self.colonna.count():
            it = self.colonna.takeAt(0)
            if it.widget():
                it.widget().setParent(None)
        for k, s in self.grafico.elenco():
            t = self.tessere.get(k)
            if t is None:
                t = Tessera(k)
                t.premuta.connect(self._accendi_serie)
                self.tessere[k] = t
            self.colonna.addWidget(t)
        self.colonna.addStretch(1)

    def _accendi_serie(self, k):
        s = self.grafico.serie.get(k)
        if s:
            s["visibile"] = not s["visibile"]
            self.grafico.update()
            self.tessere[k].aggiorna(s)

    def _apri_serie(self, k):
        s = self.grafico.serie.get(k)
        if not s:
            return
        p = self.pannelli_serie.get(k)
        if p is None:
            p = Pannello(s["etichetta"], GraficoSingolo(self.grafico, k), self)
            p.resize(700, 400)
            self.pannelli_serie[k] = p
        p.mostra()

    # ---- recorder -------------------------------------------------------------------
    def _rec_toggle(self, on):
        if on:
            os.makedirs(REC_DIR, exist_ok=True)
            path = os.path.join(REC_DIR, datetime.datetime.now().strftime("rec-%Y%m%d-%H%M%S") + SFMON_EXT)
            fh = open(path, "w", newline="")
            fh.write("# SkillFishOS Monitor recording v1\n")
            fh.write("# started=%s interval_ms=%s\n" % (datetime.datetime.now().isoformat(timespec="seconds"), self.iv.currentData()))
            wtr = csv.writer(fh)
            wtr.writerow(["t_sec"] + REC_KEYS)
            self._rec = (wtr, fh, [], time.time())
            self._rec_path = path
            self.b_rec.setText("■ STOP")
            self.toast(L("Registro in %s", "Recording to %s") % path, 5)
        else:
            rec, self._rec = self._rec, None
            self.b_rec.setText("● REC")
            if not rec:
                return
            _w, fh, rows, _t0 = rec
            fh.close()
            if not rows:
                return
            nomi = dict((k, L(*lab)) for k, lab, _u, _c in SERIE)
            nomi["vram"] = "VRAM MB"
            righe = [L("Registrazione: %.0f s, %d campioni", "Recording: %.0f s, %d samples") % (rows[-1][0], len(rows)), ""]
            for i, k in enumerate(REC_KEYS, start=1):
                serie = [r[i] for r in rows if isinstance(r[i], (int, float))]
                if serie:
                    righe.append("%-12s min %.0f · %s %.0f · max %.0f" % (nomi.get(k, k), min(serie), L("media", "avg"), sum(serie) / len(serie), max(serie)))
            righe += ["", self._rec_path]
            QMessageBox.information(self, L("Riepilogo", "Summary"), "\n".join(righe))

    def _esporta_csv(self):
        """A .sfmon is already CSV with two comment lines on top: the export
        drops the comments, names the columns in the user's language and lets
        the file be opened by any spreadsheet."""
        sorg = getattr(self, "_vista_path", None) or getattr(self, "_rec_path", None)
        if not sorg or not os.path.exists(sorg):
            self.toast(L("Prima registra o apri una registrazione.", "Record or open a recording first."))
            return
        dest, _ = QFileDialog.getSaveFileName(self, L("Esporta CSV", "Export CSV"),
                                              os.path.splitext(sorg)[0] + ".csv", "CSV (*.csv)")
        if not dest:
            return
        nomi = dict((k, L(*lab)) for k, lab, _u, _c in SERIE)
        nomi["vram"] = "VRAM MB"
        try:
            with open(sorg, newline="") as f, open(dest, "w", newline="") as g:
                wtr = csv.writer(g)
                for i, row in enumerate(csv.reader(l for l in f if not l.startswith("#"))):
                    if i == 0:
                        row = [L("secondi", "seconds")] + [nomi.get(k, k) for k in row[1:]]
                    wtr.writerow(row)
        except OSError as e:
            self.toast(str(e))
            return
        self.toast(L("Esportato in %s", "Exported to %s") % dest, 5)

    # ---- viewer ---------------------------------------------------------------------
    def _apri(self):
        path, _ = QFileDialog.getOpenFileName(self, L("Apri registrazione", "Open recording"), REC_DIR, "SkillFishOS Monitor (*.sfmon *.csv)")
        if path:
            self._carica(path)

    def _carica(self, path):
        self._vista_path = path
        times, cols = [], {}
        header, rows = None, []
        try:
            with open(path, newline="") as fh:
                for line in fh:
                    s = line.strip()
                    if not s or s.startswith("#"):
                        continue
                    parts = next(csv.reader([line]))
                    if header is None:
                        header = parts
                        continue
                    rows.append(parts)
        except Exception as e:
            self.toast(str(e))
            return
        if not header or not rows:
            self.toast(L("file vuoto", "empty file"))
            return
        idx = {h: i for i, h in enumerate(header)}
        for r in rows:
            try:
                times.append(float(r[idx["t_sec"]]))
            except Exception:
                times.append(len(times) * 1.0)
        for k in REC_KEYS:
            if k in idx:
                cols[k] = []
                for r in rows:
                    try:
                        cols[k].append(float(r[idx[k]]))
                    except Exception:
                        cols[k].append(None)
        # stop the live feed and show the whole recording in the chart
        if self.campionatore is not None:
            self.campionatore.ferma()
            self.campionatore.wait(1500)
            self.campionatore = None
        self._viewer = (times, cols)
        self.grafico.serie = {}
        self.grafico.ordine = []
        self.grafico._n_temp = 0
        self.grafico.FINESTRA = max(30, int(times[-1]) + 1)
        for k, lab, unita, col in SERIE:
            if k in cols:
                for t, val in zip(times, cols[k]):
                    if val is not None:
                        self.grafico.campiona(t, [(k, L(*lab), unita, val, col)])
        self._rifai_tessere()
        for chiave, serie in self.grafico.elenco():
            self.tessere[chiave].aggiorna(serie)
        self.scrub.blockSignals(True)
        self.scrub.setRange(0, len(times) - 1)
        self.scrub.setValue(len(times) - 1)
        self.scrub.blockSignals(False)
        self._mostra_scrub(True)
        self._scorri(len(times) - 1)
        self.finestra.toast(L("Registrazione: %s", "Recording: %s") % os.path.basename(path), 4)

    def _scorri(self, i):
        if not self._viewer:
            return
        times, cols = self._viewer
        if not (0 <= i < len(times)):
            return
        self.et_scrub.setText("t = %.1f s / %.1f s" % (times[i], times[-1]))
        for k, lab, unita, col in SERIE:
            s = self.grafico.serie.get(k)
            if s is None or k not in cols:
                continue
            v = cols[k][i]
            t = self.tessere.get(k)
            if t and v is not None:
                t.valore.setText(("%." + str({"C": 1, "W": 1}.get(unita, 0)) + "f %s") % (v, unita))

    def _chiudi_registrazione(self):
        self._viewer = None
        self._mostra_scrub(False)
        self.grafico.serie = {}
        self.grafico.ordine = []
        self.grafico._n_temp = 0
        self.grafico.FINESTRA = 300
        self._rifai_tessere()
        self.attiva()

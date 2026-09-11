# -*- coding: utf-8 -*-
"""Monitor: every reading of the board, one chart per unit, real axes.

Temperatures, clocks, load, power, voltages, fan, memory: seven charts, each
with its own true scale, plus the per-thread clock bars. REC writes the
session to a .sfmon (CSV with two comment lines) that reopens here and scrubs
second by second; CSV exports it for a spreadsheet.

Readings come straight from sysfs/hwmon and the governor heartbeat: no helper,
no root, nothing to install.
"""
import csv
import datetime
import os
import re
import time

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QFont, QLinearGradient, QPainter, QPen
from PyQt6.QtWidgets import (QComboBox, QFileDialog, QFrame, QGridLayout, QHBoxLayout, QLabel,
                             QMessageBox, QPushButton, QScrollArea, QSlider, QVBoxLayout, QWidget)

from .. import stile
from ..comune import L, battito, hwmon_valore, leggi_json, VENTOLA_STATO
from ..finestra import PaginaBase
from ..grafico_unita import GraficoUnita
from ..stile import intestazione

REC_DIR = os.path.expanduser("~/SkillFishOS-benchmarks")
SFMON_EXT = ".sfmon"

# the charts: (key, title, unit, [(series key, label, colour)], y_min, y_max)
GRAFICI = [
    ("temp", ("Temperature", "Temperatures"), "°C", [
        ("cpu_temp", "CPU", "#e8c878"), ("gpu_temp", "GPU", stile.ARANCIO),
        ("vrm_temp", "VRM", "#c78be0"), ("sys_temp", ("Sistema", "System"), "#8fbf6a"),
        ("nvme_temp", "NVMe", "#7fd4ff")], None, None),
    ("clock", ("Frequenze", "Clocks"), "MHz", [
        ("cpu_mhz", ("CPU media", "CPU avg"), "#9bd24f"), ("cpu_min", "CPU min", "#5a8f3a"),
        ("cpu_max", "CPU max", "#d4f0a0"), ("gpu_mhz", "GPU", stile.OTTONE),
        ("tetto", ("Tetto GPU", "GPU ceiling"), "#9a7a3a")], 0, None),
    ("load", ("Carico", "Load"), "%", [
        ("cpu_load", "CPU", "#5fd24f"), ("gpu_load", "GPU", "#49b6e0")], 0, 100),
    ("power", ("Potenza", "Power"), "W", [("gpu_w", "GPU", stile.VIOLA)], 0, None),
    ("volt", ("Tensioni", "Voltages"), "mV", [
        ("gpu_mv", "GPU", stile.COL_VOLT), ("soc_mv", "SoC", "#e8a878")], None, None),
    ("fan", ("Ventola", "Fan"), "rpm", [("fan", ("Giri", "Speed"), stile.COL_RPM)], 0, None),
    ("mem", ("Memoria", "Memory"), "MB", [
        ("ram_used", "RAM", "#e0d05a"), ("vram_used", "VRAM", stile.OTTONE),
        ("gtt_used", "GTT", "#b06a3a")], 0, None),
]
REC_KEYS = [k for _g, _t, _u, serie, _lo, _hi in GRAFICI for k, _e, _c in serie]
# names the first Monitor used in its .sfmon files
VECCHI_NOMI = {"gpu_util": "gpu_load", "gpu_freq": "gpu_mhz", "gpu_power": "gpu_w", "vram": "vram_used"}
_TOPO = {}


def _mb(path):
    try:
        with open(path) as fh:
            return int(fh.read().strip()) / 1048576.0
    except Exception:
        return None


def _card():
    for c in ("card0", "card1"):
        if os.path.exists("/sys/class/drm/%s/device/gpu_busy_percent" % c):
            return "/sys/class/drm/%s/device" % c
    return None


def cpu_load_pct(prev):
    try:
        with open("/proc/stat") as fh:
            f = fh.readline().split()[1:]
        vals = [int(x) for x in f]
        idle = vals[3] + (vals[4] if len(vals) > 4 else 0)
        tot = sum(vals)
        if prev:
            di, dt = idle - prev[0], tot - prev[1]
            pct = (1.0 - di / float(dt)) * 100.0 if dt > 0 else None
        else:
            pct = None
        return pct, (idle, tot)
    except Exception:
        return None, prev


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
        if c not in _TOPO:
            try:
                with open("%s/cpu%d/topology/core_id" % (base, c)) as fh:
                    _TOPO[c] = int(fh.read().strip())
            except Exception:
                _TOPO[c] = c // 2
        out.append((c, _TOPO[c], mhz.get(c) if on else None))
    return out


def leggi_tutto():
    """Every reading, straight from the kernel."""
    v = {}
    t = hwmon_valore("k10temp", "temp1_input")
    v["cpu_temp"] = t / 1000.0 if t else None
    for k, n in (("sys_temp", 2), ("vrm_temp", 3)):
        t = hwmon_valore("nct6686", "temp%d_input" % n)
        v[k] = t / 1000.0 if t else None
    t = hwmon_valore("nvme", "temp1_input")
    v["nvme_temp"] = t / 1000.0 if t else None
    b = battito()
    if b and time.time() - b["quando"] < 5:
        v["gpu_mhz"], v["tetto"], v["gpu_temp"], v["gpu_w"], v["gpu_load"] = b["mhz"], b["tetto"], b["gradi"], b["watt"], b["carico"]
    else:
        f = hwmon_valore("amdgpu", "freq1_input")
        v["gpu_mhz"] = f / 1e6 if f else None
        t = hwmon_valore("amdgpu", "temp1_input")
        v["gpu_temp"] = t / 1000.0 if t else None
        w = hwmon_valore("amdgpu", "power1_average") or hwmon_valore("amdgpu", "power1_input")
        v["gpu_w"] = w / 1e6 if w else None
        c = _card()
        try:
            with open(c + "/gpu_busy_percent") as fh:
                v["gpu_load"] = float(fh.read().strip())
        except Exception:
            v["gpu_load"] = None
    v["gpu_mv"] = hwmon_valore("amdgpu", "in0_input")
    v["soc_mv"] = hwmon_valore("amdgpu", "in1_input")
    # the one real fan: the first that turns
    v["fan"] = None
    for n in range(1, 9):
        r = hwmon_valore("nct6686", "fan%d_input" % n)
        if r:
            v["fan"] = r
            break
    if v["fan"] is None:
        st = leggi_json(VENTOLA_STATO, {}) or {}
        v["fan"] = st.get("rpm")
    try:
        with open("/proc/meminfo") as fh:
            m = dict((ln.split(":")[0], int(ln.split()[1])) for ln in fh if ":" in ln)
        v["ram_used"] = (m.get("MemTotal", 0) - m.get("MemAvailable", 0)) / 1024.0
    except Exception:
        v["ram_used"] = None
    c = _card()
    v["vram_used"] = _mb(c + "/mem_info_vram_used") if c else None
    v["gtt_used"] = _mb(c + "/mem_info_gtt_used") if c else None
    return v


class BarreCore(QWidget):
    """One bar per logical CPU, grouped by core, brass to ember as it climbs."""

    def __init__(self):
        super().__init__()
        self.threads = []
        self.setMinimumHeight(150)
        self.setMaximumHeight(180)

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
            p.fillRect(self.rect(), QColor(stile.SCHEDA))
            p.setPen(QPen(QColor(stile.SCHEDA_BORDO), 1))
            p.drawRect(0, 0, w - 1, h - 1)
            live = [m for (_c, _k, m) in self.threads if m is not None]
            p.setFont(QFont(self.font().family(), 10, QFont.Weight.Bold))
            p.setPen(QColor(stile.OTTONE))
            p.drawText(10, 19, L("Frequenza per thread  (MHz)", "Per-thread clock  (MHz)"))
            if live:
                p.setFont(QFont(self.font().family(), 8))
                p.setPen(QColor(stile.TESTO_2))
                s = "min %d  ·  %s %d  ·  max %d  ·  %d/%d" % (round(min(live)), L("media", "avg"), round(sum(live) / len(live)), round(max(live)), len(live), len(self.threads))
                p.drawText(w - 10 - p.fontMetrics().horizontalAdvance(s), 19, s)
            if not self.threads:
                return
            gx0, gy0, gx1, gy1 = 58, 30, w - 10, h - 20
            gw, gh = gx1 - gx0, gy1 - gy0
            hi = max(1000.0, max(live) if live else 0.0)
            hi = float(((hi + 499) // 500) * 500)
            p.setFont(QFont(self.font().family(), 8))
            for i in range(5):
                yy = int(gy0 + gh * i / 4)
                p.setPen(QPen(QColor(stile.GRIGLIA), 1))
                p.drawLine(gx0, yy, gx1, yy)
                txt = "%d" % round(hi - hi * i / 4.0)
                p.setPen(QColor(stile.OTTONE_SCURO))
                p.drawText(gx0 - 6 - p.fontMetrics().horizontalAdvance(txt), yy + 4, txt)
            n = len(self.threads)
            slot = gw / float(n)
            bw = max(4.0, slot * 0.62)
            p.setFont(QFont(self.font().family(), 7))
            for i, (cpu, core, mhz) in enumerate(self.threads):
                x = gx0 + slot * i + (slot - bw) / 2.0
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
                p.drawText(int(x + (bw - p.fontMetrics().horizontalAdvance(lab)) / 2), gy1 + 13, lab)
        finally:
            p.end()


class Campionatore(QThread):
    campione = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._intervallo = 1.0
        self._stop = False
        self._prev = None

    def imposta_ms(self, ms):
        self._intervallo = max(0.2, float(ms) / 1000.0)

    def ferma(self):
        self._stop = True

    def run(self):
        while not self._stop:
            vals = leggi_tutto()
            pct, self._prev = cpu_load_pct(self._prev)
            vals["cpu_load"] = pct
            thr = cpu_threads()
            vivi = [m for _c, _k, m in thr if m is not None]
            vals["cpu_mhz"] = (sum(vivi) / len(vivi)) if vivi else None
            vals["cpu_min"] = min(vivi) if vivi else None
            vals["cpu_max"] = max(vivi) if vivi else None
            vals["_threads"] = thr
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
        self.campionatore = None
        self.grafici = {}
        self._rec = None
        self._rec_path = None
        self._vista = None          # (times, rows) when a recording is open
        self._vista_path = None

    # ---- build -------------------------------------------------------------------
    def costruisci(self):
        v = self.corpo_pieno()
        testa = QHBoxLayout()
        testa.addWidget(intestazione("Monitor", "", L(
            "Un grafico per grandezza, con i numeri veri sugli assi. Clic su una voce della "
            "legenda per nasconderla. REC registra, Apri riapre, CSV esporta.",
            "One chart per quantity, real numbers on the axes. Click a legend entry to hide it. "
            "REC records, Open reopens, CSV exports."), doc="monitor"))
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
        for ms, lab in ((500, "0.5 s"), (1000, "1 s"), (2000, "2 s"), (5000, "5 s")):
            self.iv.addItem(lab, ms)
        self.iv.setCurrentIndex(1)
        self.iv.currentIndexChanged.connect(lambda: self.campionatore and self.campionatore.imposta_ms(self.iv.currentData()))
        testa.addWidget(self.iv)
        v.addLayout(testa)

        # the viewer strip: hidden until a recording is open
        self.riga_vista = QFrame()
        rv = QHBoxLayout(self.riga_vista)
        rv.setContentsMargins(0, 0, 0, 0)
        self.et_vista = QLabel("")
        self.et_vista.setStyleSheet("color:%s;" % stile.OTTONE)
        rv.addWidget(self.et_vista)
        self.scrub = QSlider(Qt.Orientation.Horizontal)
        self.scrub.valueChanged.connect(self._scorri)
        rv.addWidget(self.scrub, 1)
        b = QPushButton(L("Chiudi registrazione", "Close recording"))
        b.clicked.connect(self._chiudi_registrazione)
        rv.addWidget(b)
        self.riga_vista.hide()
        v.addWidget(self.riga_vista)

        scorri = QScrollArea()
        scorri.setWidgetResizable(True)
        scorri.setFrameShape(QFrame.Shape.NoFrame)
        gabbia = QWidget()
        self.g = QGridLayout(gabbia)
        self.g.setContentsMargins(0, 0, 6, 0)
        self.g.setSpacing(8)
        for chiave, titolo, unita, serie, lo, hi in GRAFICI:
            ser = [(k, (L(*e) if isinstance(e, tuple) else e), c) for k, e, c in serie]
            gr = GraficoUnita(L(*titolo), unita, ser, lo, hi)
            gr.cursore_mosso.connect(self._cursore)
            self.grafici[chiave] = gr
        self.barre = BarreCore()
        self.colonne = 0
        self._disponi(2)
        scorri.setWidget(gabbia)
        v.addWidget(scorri, 1)

    def _disponi(self, n):
        """The charts in n columns (two when wide, one when narrow)."""
        if n == self.colonne:
            return
        grafici = [self.grafici[k] for k, *_r in GRAFICI]
        for w in grafici + [self.barre]:
            self.g.removeWidget(w)
        for c in range(2):
            self.g.setColumnStretch(c, 0)
        for i, gr in enumerate(grafici):
            self.g.addWidget(gr, i // n, i % n)
        self.g.addWidget(self.barre, (len(grafici) + n - 1) // n, 0, 1, n)
        for c in range(n):
            self.g.setColumnStretch(c, 1)
        self.colonne = n

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        if self.grafici:
            self._disponi(1 if self.width() < 1150 else 2)

    # ---- live -------------------------------------------------------------------
    def attiva(self):
        super().attiva()            # builds the page the first time
        if self._vista is not None:
            return
        if self.campionatore is None:
            self.campionatore = Campionatore()
            self.campionatore.imposta_ms(self.iv.currentData())
            self.campionatore.campione.connect(self._campione)
            self.campionatore.start()

    def disattiva(self):
        super().disattiva()
        if self.campionatore is not None and self._rec is None:
            self.campionatore.ferma()
            self.campionatore.wait(1500)
            self.campionatore = None

    def chiudi(self):
        self._rec_toggle(False)
        self.disattiva()

    def _campione(self, vals):
        if self._vista is not None:
            return
        t = vals["_t"]
        for gr in self.grafici.values():
            gr.campiona(t, vals)
        self.barre.push(vals.get("_threads"))
        if self._rec:
            wtr, _fh, rows, t0 = self._rec
            row = [round(t - t0, 2)] + [(None if vals.get(k) is None else round(vals[k], 2)) for k in REC_KEYS]
            wtr.writerow(row)
            rows.append(row)

    def _cursore(self, t):
        for gr in self.grafici.values():
            gr.imposta_cursore(t)

    # ---- recording ----------------------------------------------------------------
    def _rec_toggle(self, on):
        if on:
            os.makedirs(REC_DIR, exist_ok=True)
            path = os.path.join(REC_DIR, datetime.datetime.now().strftime("rec-%Y%m%d-%H%M%S") + SFMON_EXT)
            fh = open(path, "w", newline="")
            fh.write("# SkillFishOS Monitor recording v2\n")
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
            nomi = self._nomi()
            righe = [L("Registrazione: %.0f s, %d campioni", "Recording: %.0f s, %d samples") % (rows[-1][0], len(rows)), ""]
            for i, k in enumerate(REC_KEYS, start=1):
                serie = [r[i] for r in rows if isinstance(r[i], (int, float))]
                if serie:
                    righe.append("%-14s min %.0f · %s %.0f · max %.0f" % (nomi.get(k, k), min(serie), L("media", "avg"), sum(serie) / len(serie), max(serie)))
            righe += ["", self._rec_path]
            QMessageBox.information(self, L("Riepilogo", "Summary"), "\n".join(righe))

    def _nomi(self):
        out = {}
        for _g, titolo, unita, serie, _lo, _hi in GRAFICI:
            for k, e, _c in serie:
                out[k] = "%s %s (%s)" % (L(*titolo), L(*e) if isinstance(e, tuple) else e, unita)
        return out

    def _esporta_csv(self):
        sorg = self._vista_path or self._rec_path
        if not sorg or not os.path.exists(sorg):
            self.toast(L("Prima registra o apri una registrazione.", "Record or open a recording first."))
            return
        dest, _ = QFileDialog.getSaveFileName(self, L("Esporta CSV", "Export CSV"),
                                              os.path.splitext(sorg)[0] + ".csv", "CSV (*.csv)")
        if not dest:
            return
        nomi = self._nomi()
        try:
            with open(sorg, newline="") as f, open(dest, "w", newline="") as g:
                wtr = csv.writer(g)
                for i, row in enumerate(csv.reader(l for l in f if not l.startswith("#"))):
                    if i == 0:
                        row = [L("secondi", "seconds")] + [nomi.get(VECCHI_NOMI.get(k, k), k) for k in row[1:]]
                    wtr.writerow(row)
        except OSError as e:
            self.toast(str(e))
            return
        self.toast(L("Esportato in %s", "Exported to %s") % dest, 5)

    # ---- viewer -------------------------------------------------------------------
    def _apri(self):
        path, _ = QFileDialog.getOpenFileName(self, L("Apri registrazione", "Open recording"), REC_DIR, "SkillFishOS Monitor (*.sfmon *.csv)")
        if path:
            self._carica(path)

    def _carica(self, path):
        righe = []
        try:
            with open(path, newline="") as f:
                rd = csv.reader(l for l in f if not l.startswith("#"))
                header = next(rd)
                chiavi = [VECCHI_NOMI.get(k, k) for k in header[1:]]
                for row in rd:
                    if not row:
                        continue
                    try:
                        t = float(row[0])
                    except ValueError:
                        continue
                    d = {}
                    for k, val in zip(chiavi, row[1:]):
                        try:
                            d[k] = float(val)
                        except ValueError:
                            pass
                    righe.append((t, d))
        except Exception as e:
            self.toast(L("Non riesco a leggere %s: %s", "Cannot read %s: %s") % (path, e))
            return
        if not righe:
            self.toast(L("Registrazione vuota.", "Empty recording."))
            return
        self.disattiva()
        self._vista = righe
        self._vista_path = path
        for gr in self.grafici.values():
            gr.carica(righe)
        self.scrub.blockSignals(True)
        self.scrub.setRange(0, len(righe) - 1)
        self.scrub.setValue(len(righe) - 1)
        self.scrub.blockSignals(False)
        self.et_vista.setText("%s  ·  %.0f s  ·  %d %s" % (os.path.basename(path), righe[-1][0], len(righe), L("campioni", "samples")))
        self.riga_vista.show()
        self._scorri(len(righe) - 1)

    def _scorri(self, i):
        if self._vista is None or not (0 <= i < len(self._vista)):
            return
        t = self._vista[i][0]
        self._cursore(t)

    def _chiudi_registrazione(self):
        self._vista = None
        self._vista_path = None
        self.riga_vista.hide()
        for gr in self.grafici.values():
            gr.azzera()
            gr.imposta_cursore(None)
        self.attiva()

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
import json
import math
import os
import re
import subprocess
import time

from PyQt6.QtCore import Qt, QRectF, QThread, QTimer, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QFont, QLinearGradient, QPainter, QPen
from PyQt6.QtWidgets import (QComboBox, QFileDialog, QFrame, QGridLayout, QHBoxLayout, QLabel,
                             QMessageBox, QPushButton, QScrollArea, QSlider, QVBoxLayout,
                             QWidget)

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
    except (OSError, ValueError, IndexError):
        # per-thread MHz is a nicety: without it the bars just stay at zero
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


# ---- GDDR6 memory temperature ------------------------------------------------
# Eight JEDEC sensors, one inside each memory chip, reached through the SMU.
#
# ⚠️ IT IS A CAPPED SESSION AND NOT A SENSOR. Polling those sensors wedges the
# SMU, which is the chip the V/F governor talks to several times a second:
# measured 31 min 39 s at one second and 55 min 15 s at three, and only a reboot
# comes back from it. How often it is patched counts separately from how long it
# runs - three sessions inside four minutes ended with "queue 3 msg 0x05 rejected
# (status 0xFF)". skillfish-gddr6-helper owns the ten minute ceiling and the
# sixty second cooldown; this page only asks it to start and stop.
#
# Reading needs nothing: the collector publishes its snapshot world-readable, so
# the page never asks for a password to SHOW anything. Only the button goes
# through the privileged helper, which is the rule the fan page already follows.
GDDR6_HELPER = "/usr/local/bin/skillfish-gddr6-helper"
GDDR6_SNAPSHOT = "/run/bc250-memory/telemetry"
GDDR6_CHIP = 8


def gddr6_disponibile():
    """True only where the reading can exist, so the card is absent elsewhere."""
    if not os.path.exists(GDDR6_HELPER):
        return False
    try:
        with open("/sys/class/dmi/id/product_name") as fh:
            return "BC-250" in fh.read()
    except OSError:
        return False


def gddr6_gradi():
    """(status, [temperature per chip]) from the collector's snapshot.

    Five lines: marker, boot time, status, eight raw words, error. Degrees come
    out of the JEDEC code in the low byte: code * 2 - 40.
    """
    try:
        with open(GDDR6_SNAPSHOT, encoding="utf-8", errors="replace") as fh:
            righe = fh.read().splitlines()
    except OSError:
        return "assente", []
    if len(righe) < 4 or righe[0] != "BC250_MEMORY_V1":
        return "assente", []
    if righe[2] != "ok":
        return righe[2], []
    gradi = [(int(w) & 0xFF) * 2 - 40 for w in righe[3].split() if w.isdigit()]
    return ("ok", gradi) if len(gradi) == GDDR6_CHIP else (righe[2], [])


def gddr6_stato():
    """The helper's own account of the session. No privileges: it is a read."""
    try:
        p = subprocess.run([GDDR6_HELPER, "stato"], capture_output=True,
                           text=True, timeout=25)
        return json.loads((p.stdout or "{}").strip().splitlines()[-1])
    except Exception:
        return {}


def colore_temp(c):
    """Cool blue to ember, over the range these chips actually live in.

    25 to 85 °C and not 0 to 100: idle sits near 44 and a loaded board near 50,
    so a scale starting at zero would paint every honest reading the same shade
    and the card would tell nobody anything.
    """
    if c is None:
        return QColor(stile.GRIGLIA)
    fermate = [(25, "#5a8fd8"), (40, "#7fd4ff"), (52, "#8fbf6a"),
               (64, stile.OTTONE), (75, stile.ARANCIO), (85, stile.ROSSO)]
    if c <= fermate[0][0]:
        return QColor(fermate[0][1])
    for (c0, col0), (c1, col1) in zip(fermate, fermate[1:]):
        if c <= c1:
            k = (c - c0) / float(c1 - c0)
            a, b = QColor(col0), QColor(col1)
            return QColor(*[int(x + (y - x) * k) for x, y in
                            ((a.red(), b.red()), (a.green(), b.green()), (a.blue(), b.blue()))])
    return QColor(fermate[-1][1])


class TesseraChip(QFrame):
    """One memory chip: its number, its temperature, a bar in its own colour."""

    def __init__(self, indice, parent=None):
        super().__init__(parent)
        self.indice = indice
        self.gradi = None
        self.caldo = False
        self.setObjectName("tessera")
        self.setMinimumWidth(78)
        v = QVBoxLayout(self)
        v.setContentsMargins(8, 4, 8, 5)
        v.setSpacing(1)
        r = QHBoxLayout()
        r.setSpacing(5)
        self.nome = QLabel("%d" % indice)
        self.valore = QLabel("—")
        r.addWidget(self.nome)
        r.addStretch(1)
        r.addWidget(self.valore)
        v.addLayout(r)
        self.barra = QFrame()
        self.barra.setFixedHeight(3)
        v.addWidget(self.barra)
        self.aggiorna(None, False)

    def aggiorna(self, gradi, caldo):
        self.gradi, self.caldo = gradi, caldo
        col = colore_temp(gradi)
        self.nome.setText("%d" % self.indice)
        self.nome.setStyleSheet("font-size:10px;color:%s;border:none;" % stile.TESTO_2)
        self.valore.setText("—" if gradi is None else "%d °C" % gradi)
        self.valore.setStyleSheet("font-size:14px;font-weight:bold;border:none;color:%s;"
                                  % (col.name() if gradi is not None else stile.TESTO_2))
        # The bar is the whole legend: no colour key anywhere, because the number
        # and its colour sit in the same tile.
        self.barra.setStyleSheet("background:%s;border:none;border-radius:2px;"
                                 % (col.name() if gradi is not None else stile.GRIGLIA))
        self.setStyleSheet(
            "QFrame#tessera{border:1px solid %s;border-radius:6px;background:%s;}"
            % (col.name() if caldo else stile.SCHEDA_BORDO,
               stile.SCHEDA_ALTA if caldo else stile.SCHEDA))


class DisegnoScheda(QWidget):
    """The BC-250 seen from above, drawn from the board's own CAD.

    Every position below is measured, not sketched. They come from
    ASRock_AMD_BC-250_ISL_X5R_r1.00.cad, the GenCAD 1.4 boardview of the real
    board published on bc-250.com, whose 2163 components are placed on a PCB of
    304.66 x 139.98 mm. Millimetres here are that file's millimetres.

    ⚠️ GenCAD puts its origin bottom left with y growing upwards and Qt grows y
    downwards, so every y below is already 139.98 - y. Using the raw value would
    draw a mirrored board: the same picture of a part that does not exist.

    ⚠️ U27, U33, U37 and U43 sit at 45 degrees. The CAD gives that away by their
    pin field coming out square at 15.9 mm while the four straight ones measure
    9.8 x 12.7, and (9.8 + 12.7) / sqrt(2) is 15.9 exactly. They are drawn turned
    because on this board they are turned.

    ⚠️ WHICH SENSOR IS WHICH CHIP IS STILL UNKNOWN. The eight positions are real;
    the order the SMU reports them in is not documented anywhere, here or
    upstream. The chip numbered 0 in this drawing is the first sensor the SMU
    answers with, and nothing yet proves it is the part silkscreened U27. Until
    someone heats one chip and watches which number moves, this says WHICH chip
    is hot and only guesses where. The help text says so.
    """

    LARGO, ALTO = 304.66, 139.98

    # the eight GDDR6, in the order the SMU reports them (see the caveat above)
    MEMORIA = [
        (135.24, 90.33, 8.78, 11.25, True),    # U27
        (159.89, 105.83, 9.75, 12.75, False),  # U29
        (184.59, 105.83, 9.75, 12.75, False),  # U31
        (209.24, 90.33, 8.78, 11.25, True),    # U33
        (135.24, 29.33, 8.78, 11.25, True),    # U37
        (159.89, 13.83, 9.75, 12.75, False),   # U39
        (184.59, 13.83, 9.75, 12.75, False),   # U41
        (209.24, 29.33, 8.78, 11.25, True),    # U43
    ]

    APU = (172.20, 59.80, 42.4, 42.4)          # U25, BGA2197
    FCH = (60.50, 82.20, 23.1, 23.1)           # SU1, 656 balls
    SIO = (96.50, 104.20, 15.7, 15.7)          # UIO1

    BUCHI = [(7.5, 11.1, 2.5), (7.5, 111.1, 2.5),
             (298.8, 17.3, 2.9), (298.8, 27.3, 2.9)]

    # connectors, with the ones that open onto the outside world marked dark
    CONNETTORI = [
        (7.8, 56.1, 10.3, 16.5, True, "DP"),       # J4002, DisplayPort
        (12.0, 96.1, 13.5, 15.6, True, "LAN"),     # LAN1
        (12.0, 75.1, 6.7, 13.1, True, ""),         # USB_3_4
        (11.5, 37.1, 5.7, 13.1, True, ""),         # USB1
        (9.4, 21.1, 8.1, 8.0, False, ""),          # PANEL1
        (31.2, 8.1, 20.7, 7.5, False, "M.2"),      # M2_1
        (233.8, 130.6, 12.6, 11.5, True, ""),      # J1000, 8 pin PCIe
        (255.8, 131.0, 9.0, 11.5, True, ""),       # J2000, Micro-Fit
        (275.8, 131.0, 9.0, 11.5, True, ""),       # J2001, Micro-Fit
    ]

    # the VRM that feeds the APU: six power stages in a column, plus two strays
    STADI = [(257.0, y) for y in (33.4, 43.1, 52.8, 62.6, 72.4, 82.2)] + \
            [(288.2, 69.5), (273.2, 99.8), (246.6, 13.3)]

    # small parts, so the board reads as a board and not as a diagram
    MINUTERIA = [
        (11.5, 75.1, 5.7, 13.1), (54.7, 6.2, 11.4, 4.1), (299.1, 128.6, 2.5, 17.8),
        (61.2, 32.7, 5.8, 5.8), (24.0, 114.8, 16.0, 2.0), (111.1, 106.7, 6.7, 4.6),
        (50.1, 103.8, 6.7, 4.6), (44.2, 112.1, 8.0, 3.8), (38.3, 51.9, 6.3, 4.6),
        (36.1, 24.0, 8.7, 3.2), (114.5, 114.0, 7.3, 3.8), (94.8, 86.0, 5.7, 3.8),
        (299.0, 46.4, 3.8, 5.7), (24.9, 89.7, 3.8, 5.7), (37.1, 41.0, 5.7, 3.8),
        (36.3, 80.0, 5.7, 3.8), (60.3, 114.1, 7.6, 2.5), (298.6, 83.2, 3.6, 5.1),
        (71.6, 99.6, 5.7, 3.8), (89.4, 60.3, 5.8, 5.8), (31.6, 101.2, 3.8, 3.8),
        (105.0, 60.0, 4.2, 4.2), (120.0, 72.0, 3.4, 3.4), (120.0, 98.0, 3.4, 3.4),
        (228.0, 60.0, 4.6, 3.2), (228.0, 80.0, 4.6, 3.2), (240.0, 95.0, 3.6, 3.6),
        (150.0, 5.5, 3.0, 3.0), (200.0, 5.5, 3.0, 3.0), (170.0, 134.0, 3.0, 3.0),
    ]

    PCB = "#17241a"
    PCB_BORDO = "#3a5740"
    SERIGRAFIA = "#6d8f74"
    RAME = "#1a2a1d"
    METALLO = "#4a5158"

    # past this the board eats the page: it is 2.18 times wider than it is tall,
    # so a card 800 wide would otherwise want 370 pixels of height for it alone.
    ALTEZZA_MAX = 300

    def __init__(self, parent=None):
        super().__init__(parent)
        self.gradi = []
        self.setMinimumHeight(150)

    def heightForWidth(self, larghezza):
        return min(self.ALTEZZA_MAX,
                   int(max(0, larghezza - 8) * self.ALTO / self.LARGO) + 8)

    def resizeEvent(self, e):
        """Keep the widget the shape of the board it draws.

        ⚠️ A QVBoxLayout only honours heightForWidth for a widget whose size
        policy declares it, and setting that policy here made the card lay out at
        the minimum height anyway: the board came out a third of the width it had
        room for. Taking the height itself, from the width we were actually
        given, is one line and always works.
        """
        super().resizeEvent(e)
        voluta = self.heightForWidth(self.width())
        if voluta > 0 and self.height() != voluta:
            self.setFixedHeight(voluta)

    def aggiorna(self, gradi):
        self.gradi = gradi or []
        self.update()

    def paintEvent(self, _e):
        w, h = self.width(), self.height()
        if w <= 24 or h <= 16:
            return
        p = QPainter()
        if not p.begin(self):
            return
        try:
            p.setRenderHint(QPainter.RenderHint.Antialiasing)
            k = min((w - 8) / self.LARGO, (h - 8) / self.ALTO)
            x0 = (w - self.LARGO * k) / 2.0
            y0 = (h - self.ALTO * k) / 2.0

            def rett(mx, my, mw, mh):
                """A part's box, from its centre in millimetres to pixels."""
                return QRectF(x0 + (mx - mw / 2.0) * k, y0 + (my - mh / 2.0) * k,
                              mw * k, mh * k)

            def penna(colore, spessore=1.0):
                q = QPen(QColor(colore), spessore)
                q.setCosmetic(True)
                return q

            self._pcb(p, rett, penna, k, x0, y0)
            self._minuteria(p, rett, penna, k)
            self._chip_grossi(p, rett, penna, k)
            self._memoria(p, rett, penna, k)
        except Exception:
            pass
        finally:
            if p.isActive():
                p.end()

    # ------------------------------------------------------------------ pieces

    def _pcb(self, p, rett, penna, k, x0, y0):
        p.setPen(penna(self.PCB_BORDO, 1.4))
        p.setBrush(QColor(self.PCB))
        p.drawRoundedRect(QRectF(x0, y0, self.LARGO * k, self.ALTO * k),
                          2.5 * k, 2.5 * k)

        # the ground pour under the memory and the APU, barely a shade lighter
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(self.RAME))
        p.drawRoundedRect(rett(172.0, 60.0, 112.0, 112.0), 10 * k, 10 * k)

        # the silkscreen name, where the board has room for it
        f = QFont()
        f.setPointSizeF(max(4.5, 2.8 * k))
        f.setBold(True)
        p.setFont(f)
        p.setPen(QColor(self.SERIGRAFIA))
        p.drawText(rett(250.0, 110.0, 40.0, 8.0),
                   Qt.AlignmentFlag.AlignCenter, "BC-250")

        p.setPen(penna(self.PCB_BORDO, 1.0))
        p.setBrush(QColor("#0d140f"))
        for mx, my, r in self.BUCHI:
            p.drawEllipse(rett(mx, my, r * 2, r * 2))

        for mx, my, mw, mh, fuori, etichetta in self.CONNETTORI:
            p.setPen(penna(self.METALLO, 1.0))
            p.setBrush(QColor("#0a0d0b") if fuori else QColor("#25332a"))
            p.drawRoundedRect(rett(mx, my, mw, mh), 1.0 * k, 1.0 * k)

        # the M.2 card itself, lying over its slot towards the board centre
        p.setPen(penna(self.PCB_BORDO, 1.0))
        p.setBrush(QColor("#1b2b20"))
        p.drawRoundedRect(rett(53.0, 8.1, 60.0, 11.0), 0.8 * k, 0.8 * k)

        # power stages
        p.setPen(penna(self.METALLO, 1.0))
        p.setBrush(QColor("#232c25"))
        for mx, my in self.STADI:
            p.drawRoundedRect(rett(mx, my, 4.7, 4.7), 0.6 * k, 0.6 * k)

    def _minuteria(self, p, rett, penna, k):
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor("#25352a"))
        for mx, my, mw, mh in self.MINUTERIA:
            p.drawRect(rett(mx, my, mw, mh))

    def _chip_grossi(self, p, rett, penna, k):
        for (mx, my, mw, mh), corpo in ((self.APU, "#2c3239"),
                                        (self.FCH, "#242c26"),
                                        (self.SIO, "#242c26")):
            p.setPen(penna("#586a5d", 1.0))
            p.setBrush(QColor(corpo))
            p.drawRoundedRect(rett(mx, my, mw, mh), 0.8 * k, 0.8 * k)

        # the APU's metal lid, and its name
        mx, my, mw, mh = self.APU
        p.setPen(penna("#6d7883", 1.0))
        p.setBrush(QColor("#454d57"))
        p.drawRoundedRect(rett(mx, my, mw * 0.72, mh * 0.72), 0.6 * k, 0.6 * k)
        f = QFont()
        f.setPointSizeF(max(5.5, 3.4 * k))
        f.setBold(True)
        p.setFont(f)
        p.setPen(QColor("#c8d2c9"))
        p.drawText(rett(mx, my, mw, mh), Qt.AlignmentFlag.AlignCenter, "APU")

        f.setPointSizeF(max(4.5, 2.4 * k))
        f.setBold(False)
        p.setFont(f)
        p.setPen(QColor(self.SERIGRAFIA))
        for mx, my, mw, mh, _fuori, etichetta in self.CONNETTORI:
            if etichetta:
                p.drawText(rett(mx, my, max(mw, 16.0), mh),
                           Qt.AlignmentFlag.AlignCenter, etichetta)

    def _memoria(self, p, rett, penna, k):
        f = QFont()
        f.setPointSizeF(max(5.0, 3.0 * k))
        f.setBold(True)
        for i, (mx, my, mw, mh, girato) in enumerate(self.MEMORIA):
            gradi = self.gradi[i] if i < len(self.gradi) else None
            col = colore_temp(gradi)
            riempi = QColor(col)
            riempi.setAlpha(150 if gradi is not None else 40)
            p.save()
            p.translate(rett(mx, my, 0, 0).center())
            if girato:
                p.rotate(45)
            corpo = QRectF(-mw * k / 2.0, -mh * k / 2.0, mw * k, mh * k)
            p.setPen(penna(col.name(), 1.4))
            p.setBrush(riempi)
            p.drawRoundedRect(corpo, 0.7 * k, 0.7 * k)
            p.restore()
            # the number stays upright even where the chip is turned
            p.setFont(f)
            p.setPen(QColor(stile.TESTO if gradi is not None else stile.TESTO_2))
            p.drawText(rett(mx, my, mw, mh), Qt.AlignmentFlag.AlignCenter, str(i))


class SchedaGddr6(stile.Scheda):
    """The memory card: the board, the two numbers that matter, the eight chips."""

    def __init__(self, demone, parent=None):
        super().__init__(L("GDDR6 · Memoria", "GDDR6 · Memory"), L(
            "La temperatura la misurano otto sensori dentro i chip di memoria, e si "
            "leggono passando dalla SMU. Per questo non è un sensore sempre acceso: "
            "interrogarla a lungo la pianta, e la SMU è la stessa che regge frequenze "
            "e tensioni. La lettura si accende quando serve, dura al massimo dieci "
            "minuti e si chiude da sola. Il disegno della scheda è schematico: dice "
            "QUALE chip è caldo, non dove si trova fisicamente.",
            "Eight sensors inside the memory chips measure this, and they answer only "
            "through the SMU. That is why it is not a sensor that stays on: polling it "
            "for long wedges the SMU, which is also the chip that holds clocks and "
            "voltages. The reading starts when needed, lasts ten minutes at most and "
            "closes itself. The board drawing is schematic: it tells you WHICH chip is "
            "hot, not where it sits."), parent)
        self.demone = demone
        self._attiva = False
        self._in_corso = False

        testa = QHBoxLayout()
        testa.setSpacing(18)
        self.n_caldo = stile.Numerone(L("Punto caldo", "Hotspot"), "°C")
        self.n_media = stile.Numerone(L("Media", "Average"), "°C")
        testa.addWidget(self.n_caldo)
        testa.addWidget(self.n_media)
        testa.addStretch(1)
        self.badge = stile.Stato(L("spenta", "off"), "quieto")
        testa.addWidget(self.badge)
        self.aggiungi(testa)

        self.disegno = DisegnoScheda()
        self.aggiungi(self.disegno)

        griglia = QGridLayout()
        griglia.setSpacing(6)
        self.tessere = []
        for i in range(GDDR6_CHIP):
            t = TesseraChip(i)
            griglia.addWidget(t, i // 4, i % 4)
            self.tessere.append(t)
        self.aggiungi(griglia)

        basso = QHBoxLayout()
        self.b = QPushButton("")
        self.b.clicked.connect(self._premuto)
        basso.addWidget(self.b)
        self.nota = QLabel("")
        self.nota.setWordWrap(True)
        self.nota.setStyleSheet("color:%s;font-size:11px;" % stile.TESTO_2)
        basso.addWidget(self.nota, 1)
        self.aggiungi(basso)
        self.aggiorna()

    def _premuto(self):
        if self._in_corso:
            return
        self._in_corso = True
        try:
            r = self.demone.cmd(cmd="gddr6",
                                azione="ferma" if self._attiva else "avvia") or {}
            if not r.get("ok"):
                self.nota.setText(str(r.get("errore") or L("non riuscito", "failed")))
        finally:
            self._in_corso = False
        self.aggiorna()

    def aggiorna(self):
        st = gddr6_stato()
        self._attiva = bool(st.get("attiva"))
        rimasti, pausa = st.get("rimasti"), st.get("pausa") or 0
        motivo = st.get("perche_no")

        self.b.setText("■ " + L("Ferma la lettura", "Stop reading") if self._attiva
                       else "◉ " + L("Leggi la memoria", "Read the memory"))
        self.b.setEnabled(not motivo and (self._attiva or not pausa))
        self.badge.setText(L("in lettura", "reading") if self._attiva else L("spenta", "off"))
        self.badge.tono("bene" if self._attiva else "quieto")

        if motivo:
            self.nota.setText(str(motivo))
        elif self._attiva and rimasti is not None:
            self.nota.setText(L("si chiude da sola fra %s", "closes itself in %s")
                              % ("%d:%02d" % (rimasti // 60, rimasti % 60)))
        elif pausa:
            self.nota.setText(L("pausa fra una lettura e l'altra: ancora %s s",
                                "cooldown between readings: %s s left") % pausa)
        else:
            self.nota.setText(L("si accende quando serve, al massimo %s minuti",
                                "started when needed, %s minutes at most")
                              % int(st.get("minuti_max") or 10))

        stato, gradi = gddr6_gradi()
        if not (self._attiva and stato == "ok" and gradi):
            gradi = []
        caldo = max(gradi) if gradi else None
        self.n_caldo.imposta(caldo, colore=colore_temp(caldo).name() if gradi else None)
        self.n_media.imposta(round(sum(gradi) / float(len(gradi)), 1) if gradi else None)
        self.disegno.aggiorna(gradi)
        for i, t in enumerate(self.tessere):
            v = gradi[i] if i < len(gradi) else None
            t.aggiorna(v, bool(gradi) and v == caldo)


class Pagina(PaginaBase):
    def __init__(self, finestra):
        super().__init__(finestra)
        self.campionatore = None
        self.grafici = {}
        self._rec = None
        self._rec_path = None
        self._vista = None          # (times, rows) when a recording is open
        self.scheda_mem = None      # the GDDR6 card, only where there is one
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
        if gddr6_disponibile():
            self.scheda_mem = SchedaGddr6(self.demone)
            # three seconds: the collector publishes no faster, and every tick
            # of this timer costs a subprocess.
            self._giro_mem = QTimer(self)
            self._giro_mem.timeout.connect(self.scheda_mem.aggiorna)
            self._giro_mem.start(3000)
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
        for w in grafici + [self.barre] + ([self.scheda_mem] if self.scheda_mem else []):
            self.g.removeWidget(w)
        for c in range(2):
            self.g.setColumnStretch(c, 0)
        riga0 = 0
        if self.scheda_mem is not None:
            # first and full width: it is the only card here that is not a chart,
            # and tucking it between two charts would read as one.
            self.g.addWidget(self.scheda_mem, 0, 0, 1, n)
            riga0 = 1
        for i, gr in enumerate(grafici):
            self.g.addWidget(gr, riga0 + i // n, i % n)
        self.g.addWidget(self.barre, riga0 + (len(grafici) + n - 1) // n, 0, 1, n)
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
                            # not a number: leave this reading out of the row instead of a fake zero
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

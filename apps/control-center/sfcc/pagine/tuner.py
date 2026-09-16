# -*- coding: utf-8 -*-
"""Tuner: the GPU voltage/frequency curve, the CPU, the cores, the compute units.

THE CURVE IS THE CHART. MHz across, millivolts up, the fifteen knots drag, the
same knots sit in a table beside it where every value can be typed. The live
dot is the GPU right now. What you see is what the governor runs.

APPLY IS A TRIAL. A curve that asks too little voltage hangs the board, and
on the BC-250 a hang means pulling the plug. So Apply starts the candidate
with the last known good curve still on disk and counts down: unless you
press Keep, the good curve is what boots.

EVERY TEST COUNTS DOWN AND CAN BE STOPPED. The CPU load runs here, as the
user, in its own thread; the helper only applies the values (without leaving
them on disk) so the window never freezes and a hang boots the old values.
"""
import os
import re
import subprocess
import time

from PyQt6.QtCore import Qt, QThread, QTimer, pyqtSignal
from PyQt6.QtWidgets import (QAbstractItemView, QButtonGroup, QCheckBox, QDialog, QGridLayout,
                             QHBoxLayout, QHeaderView, QLabel, QMessageBox, QPushButton,
                             QRadioButton, QSlider, QSpinBox, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QWidget)

from .. import stile
from ..comune import GOV_CONF, L, Aiuto, battito, hwmon_valore, leggi_json, leggi_testo, sh
from ..demone import in_sfondo
from ..finestra import PaginaBase
from ..grafico import CurvaVF
from ..stile import Stato, Tessera, intestazione, link_doc

CURVA_PREDEFINITA = "/usr/share/skillfish/vf-curva-predefinita.json"
MV_PER_SCALINO = 6.25          # the SMU voltage step of the CPU undervolt
GOV_UNIT = "skillfish-vf-governor.service"
SECONDI_PROVA = 25
CPU_TOLLERANZA = 200           # MHz under the target that still count as "holds"


def cpu_media_mhz():
    fs = [float(x) for x in re.findall(r'cpu MHz\s*:\s*([\d.]+)', leggi_testo("/proc/cpuinfo"))]
    return sum(fs) / len(fs) if fs else None


def cpu_min_mhz():
    fs = [float(x) for x in re.findall(r'cpu MHz\s*:\s*([\d.]+)', leggi_testo("/proc/cpuinfo"))]
    return min(fs) if fs else None


class Pannello(QDialog):
    """A panel that opens when needed and lives, hidden, the rest of the time."""

    def __init__(self, titolo, contenuto, parent=None):
        super().__init__(parent)
        self.setWindowTitle(titolo)
        self.setModal(False)
        v = QVBoxLayout(self)
        v.setContentsMargins(12, 12, 12, 12)
        v.addWidget(contenuto)
        r = QHBoxLayout()
        r.addStretch(1)
        b = QPushButton(L("Chiudi", "Close"))
        b.clicked.connect(self.hide)
        r.addWidget(b)
        v.addLayout(r)

    def mostra(self):
        self.show()
        self.raise_()
        self.activateWindow()


class Manopola(QWidget):
    """A slider and a number box that agree: drag for the rough value, type
    the exact one. Step 1, always."""
    cambiata = pyqtSignal(int)

    def __init__(self, lo, hi, val, unita="", mostra=None, parent=None):
        super().__init__(parent)
        h = QHBoxLayout(self)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(8)
        self.s = QSlider(Qt.Orientation.Horizontal)
        self.s.setRange(lo, hi)
        self.s.setSingleStep(1)
        self.s.setPageStep(10)
        self.n = QSpinBox()
        self.n.setRange(lo, hi)
        self.n.setSingleStep(1)
        self.n.setSuffix((" " + unita) if unita else "")
        self.n.setMinimumWidth(100)
        self.et = QLabel("")
        self.et.setMinimumWidth(84)
        self.et.setStyleSheet("color:%s;" % stile.TESTO_2)
        self.mostra = mostra
        self.s.valueChanged.connect(self._dal_cursore)
        self.n.valueChanged.connect(self._dalla_casella)
        h.addWidget(self.s, 1)
        h.addWidget(self.n)
        h.addWidget(self.et)
        self.setValue(val)

    def _dal_cursore(self, v):
        self.n.blockSignals(True)
        self.n.setValue(v)
        self.n.blockSignals(False)
        self._agg(v)

    def _dalla_casella(self, v):
        self.s.blockSignals(True)
        self.s.setValue(v)
        self.s.blockSignals(False)
        self._agg(v)

    def _agg(self, v):
        self.et.setText(self.mostra(v) if self.mostra else "")
        self.cambiata.emit(v)

    def value(self):
        return self.n.value()

    def setValue(self, v):
        self.n.setValue(int(v))


class ProvaCpu(QThread):
    """Steps of (MHz, undervolt step, seconds): each is applied through the
    helper WITHOUT touching the boot values, then sysbench loads every thread
    for the given seconds while the lowest clock is watched. Stop kills the
    load and the thread reports what it had."""
    tick = pyqtSignal(str, int)                 # label, seconds left
    passo = pyqtSignal(int, int, bool, int)     # mhz, scale, held, min mhz
    finito = pyqtSignal(object)                 # (mhz, scale) of the best, or None

    def __init__(self, demone, passi, temp, parent=None):
        super().__init__(parent)
        self.demone, self.passi, self.temp = demone, list(passi), int(temp)
        self._stop = False
        self._proc = None
        self.migliore = None

    def ferma(self):
        self._stop = True
        p = self._proc
        if p is not None:
            try:
                p.terminate()
            except OSError:
                # already exited: nothing left to stop
                pass

    def run(self):
        nth = os.cpu_count() or 8
        for mhz, scale, secs in self.passi:
            if self._stop:
                break
            etichetta = "%d MHz  ·  UV %d" % (mhz, scale)
            self.tick.emit(etichetta, secs)
            r = self.demone.cmd(cmd="cpu-volatile", mhz=mhz, scale=scale, temp=self.temp)
            if not r.get("ok"):
                self.passo.emit(mhz, scale, False, 0)
                break
            try:
                self._proc = subprocess.Popen(
                    ["sysbench", "cpu", "--threads=%d" % nth, "--time=%d" % secs, "--cpu-max-prime=20000", "run"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except OSError:
                self.passo.emit(mhz, scale, False, 0)
                break
            minimo = None
            t0 = time.monotonic()
            while self._proc.poll() is None:
                if self._stop:
                    break
                passati = time.monotonic() - t0
                if passati > 5:
                    m = cpu_min_mhz()
                    if m is not None and (minimo is None or m < minimo):
                        minimo = m
                self.tick.emit(etichetta, max(0, int(secs - passati)))
                time.sleep(0.5)
            rc = self._proc.wait() if self._proc.poll() is not None else -1
            self._proc = None
            if self._stop:
                break
            tenuto = rc == 0 and minimo is not None and minimo >= mhz - CPU_TOLLERANZA
            self.passo.emit(mhz, scale, tenuto, int(minimo or 0))
            if tenuto:
                self.migliore = (mhz, scale)
            else:
                break
        self.finito.emit(self.migliore)


class ProvaCurva(QDialog):
    """The countdown after Apply: keep, or go back before the time runs out."""

    def __init__(self, secondi, parent=None):
        super().__init__(parent)
        self.setWindowTitle(L("Curva in prova", "Curve on trial"))
        self.setModal(True)
        self.tenuta = False
        self.resto = secondi
        v = QVBoxLayout(self)
        v.setContentsMargins(20, 18, 20, 18)
        t = QLabel(L("La curva nuova sta girando. Su disco c'e' ancora quella di prima: "
                     "se la scheda si pianta e riparte, torna quella.",
                     "The new curve is running. The old one is still on disk: if the board "
                     "hangs and comes back, that is the one that boots."))
        t.setWordWrap(True)
        v.addWidget(t)
        self.et = QLabel("")
        self.et.setObjectName("numerone")
        self.et.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v.addWidget(self.et)
        self.vivo = QLabel("")
        self.vivo.setObjectName("quieto")
        self.vivo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v.addWidget(self.vivo)
        r = QHBoxLayout()
        b1 = QPushButton(L("Torna indietro", "Go back"))
        b1.clicked.connect(self.reject)
        b2 = QPushButton(L("Tieni", "Keep"))
        b2.setObjectName("primario")
        b2.clicked.connect(self._tieni)
        r.addWidget(b1)
        r.addWidget(b2)
        v.addLayout(r)
        self.t = QTimer(self)
        self.t.timeout.connect(self._tick)
        self.t.start(1000)
        self._tick(primo=True)

    def _tick(self, primo=False):
        if not primo:
            self.resto -= 1
        b = battito()
        if b:
            self.vivo.setText("%d MHz  ·  %d °C  ·  %d W  ·  %s %d%%" % (
                b["mhz"], b["gradi"], b["watt"], L("carico", "load"), b["carico"]))
        self.et.setText("%d s" % max(0, self.resto))
        if self.resto <= 0:
            self.reject()

    def _tieni(self):
        self.tenuta = True
        self.accept()


# the readouts beside the curve: key, label, unit, colour
LETTURE = [
    ("gpu_mhz", "GPU MHz", "MHz", stile.OTTONE),
    ("tetto", ("Tetto", "Ceiling"), "MHz", "#9a7a3a"),
    ("gpu_mv", "GPU mV", "mV", stile.COL_VOLT),
    ("gpu_c", "GPU °C", "C", stile.ARANCIO),
    ("gpu_w", "GPU W", "W", stile.VIOLA),
    ("carico", ("Carico GPU", "GPU load"), "%", stile.VERDE),
    ("cpu_mhz", "CPU MHz", "MHz", "#9bd24f"),
    ("cpu_c", "CPU °C", "C", "#e8c878"),
]


class Pagina(PaginaBase):
    def __init__(self, finestra):
        super().__init__(finestra)
        self.intervallo_ms = 1000
        self.conf = {}
        self.tessere = {}
        self.cfg = {}
        self._occupato = False
        self._prova = None
        self._tabella_muta = False

    # ============================================================ build
    def costruisci(self):
        v = self.corpo_pieno()
        testa = QHBoxLayout()
        testa.addWidget(intestazione("Tuner", "", L(
            "La curva tensione/frequenza del governor: trascina un punto o scrivi il numero "
            "nella tabella. Applica la prova per %d secondi e tiene la vecchia su disco.",
            "The governor's voltage/frequency curve: drag a knot or type the number in the "
            "table. Apply runs it on trial for %d seconds with the old one kept on disk.") % SECONDI_PROVA,
            doc="tuner"))
        testa.addStretch(1)
        self.b_stato = Stato("", "quieto")
        testa.addWidget(self.b_stato)
        self.interruttore = QCheckBox("Governor")
        self.interruttore.setToolTip(L("Spento: il clock torna al governor di serie.",
                                       "Off: the clock goes back to the stock governor."))
        self.interruttore.clicked.connect(self._governor_on_off)
        # the boot state is re-read on a timer of its own, see _gov_al_boot
        self._gov_boot = None
        self._gov_boot_letto = 0.0
        testa.addWidget(self.interruttore)
        testa.addWidget(Aiuto(L("Il nostro governor forza il clock e si prende la protezione: il tetto scende quando la scheda scalda o tira troppo.",
                                "Our governor forces the clock and takes on the protection: the ceiling drops when the board gets hot or draws too much."), "Governor"))
        v.addLayout(testa)

        # --- the readouts: a column on the left when the window is wide, a
        # strip above the curve when it is narrow (both exist, one is shown)
        self.striscia = QWidget()
        sr = QHBoxLayout(self.striscia)
        sr.setContentsMargins(0, 0, 0, 0)
        sr.setSpacing(5)
        colonna = QVBoxLayout()
        colonna.setSpacing(5)
        for chiave, etichetta, unita, colore in LETTURE:
            nome = L(*etichetta) if isinstance(etichetta, tuple) else etichetta
            t1, t2 = Tessera(chiave), Tessera(chiave)
            for t in (t1, t2):
                t.setCursor(Qt.CursorShape.ArrowCursor)
            self.tessere[chiave] = ((t1, t2), nome, unita, colore)
            colonna.addWidget(t1)
            sr.addWidget(t2)
        colonna.addStretch(1)
        self.striscia.hide()
        v.addWidget(self.striscia)

        corpo = QHBoxLayout()
        corpo.setSpacing(10)
        v.addLayout(corpo, 1)
        self.gab = QWidget()
        self.gab.setLayout(colonna)
        self.gab.setFixedWidth(150)
        corpo.addWidget(self.gab, 0)

        # --- centre: the curve, full size
        self.curva = CurvaVF(autonomo=True)
        self.curva.cambiata.connect(self._curva_toccata)
        corpo.addWidget(self.curva, 1)

        # --- right: the knots as numbers, the ceiling, the presets
        destra = QVBoxLayout()
        destra.setSpacing(6)
        r = QHBoxLayout()
        r.addWidget(QLabel("<b>%s</b>" % L("Punti della curva", "Curve knots")))
        r.addWidget(Aiuto(L("Ogni riga e' un punto: MHz e mV si scrivono. + aggiunge un punto dopo quello scelto, − lo toglie.",
                            "Every row is a knot: type MHz and mV. + adds a knot after the selected one, − removes it."), L("Punti", "Knots")))
        r.addStretch(1)
        # the global button padding ate the glyph at 30 px: no padding here
        for testo, slot, suggerimento in (("+", self._aggiungi_punto, L("Aggiungi un punto dopo quello scelto", "Add a knot after the selected one")),
                                          ("−", self._togli_punto, L("Togli il punto scelto", "Remove the selected knot"))):
            b = QPushButton(testo)
            b.setFixedSize(34, 30)
            b.setStyleSheet("QPushButton{padding:0;min-width:0;font-size:16px;font-weight:700;}")
            b.setToolTip(suggerimento)
            b.clicked.connect(slot)
            r.addWidget(b)
        destra.addLayout(r)
        self.tabella = QTableWidget(0, 2)
        self.tabella.setHorizontalHeaderLabels(["MHz", "mV"])
        self.tabella.verticalHeader().setVisible(False)
        self.tabella.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabella.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabella.setFixedWidth(226)
        self.tabella.itemChanged.connect(self._tabella_cambiata)
        destra.addWidget(self.tabella, 1)
        r = QHBoxLayout()
        r.addWidget(QLabel("<b>%s</b>" % L("Tetto", "Ceiling")))
        self.tetto = QSpinBox()
        self.tetto.setRange(350, 2300)
        self.tetto.setSingleStep(1)
        self.tetto.setSuffix(" MHz")
        self.tetto.valueChanged.connect(self._tetto_cambiato)
        r.addWidget(self.tetto)
        r.addWidget(Aiuto(L("Fin dove il governor puo' spingere il clock. 2100 tiene sulla scheda di sviluppo; sali di 50 alla volta e prova Cyberpunk.",
                            "How far the governor may push the clock. 2100 holds on the development board; go up 50 at a time and try Cyberpunk."), L("Tetto", "Ceiling")))
        destra.addLayout(r)
        pr = QVBoxLayout()
        pr.setSpacing(2)
        self.gruppo_preset = QButtonGroup(self)
        for chiave, testo, aiuto in (
                # the preset names stay English in every language (Mattia, 2026-09-12)
                ("prudente", "Cautious 1850", L("Il punto dolce col dissipatore di serie: quasi gli stessi fotogrammi, dieci gradi in meno.", "The sweet spot with the stock heatsink: nearly the same frames, ten degrees less.")),
                ("equilibrato", "Balanced 2000", L("Tetto a 2000 MHz.", "Ceiling at 2000 MHz.")),
                ("misurato", "Performance 2100", L("La curva a quindici punti misurata sulla scheda di sviluppo: quella che spediamo.", "The fifteen-point curve measured on the development board: the one we ship."))):
            rr = QHBoxLayout()
            b = QRadioButton(testo)
            b.chiave = chiave
            self.gruppo_preset.addButton(b)
            rr.addWidget(b)
            rr.addWidget(Aiuto(aiuto, testo))
            rr.addStretch(1)
            pr.addLayout(rr)
        self.gruppo_preset.buttonClicked.connect(self._preset)
        destra.addLayout(pr)
        self.et_salva = QLabel("")
        self.et_salva.setObjectName("quieto")
        self.et_salva.setWordWrap(True)
        destra.addWidget(self.et_salva)
        rr = QHBoxLayout()
        b = QPushButton(L("Annulla", "Discard"))
        b.setToolTip(L("Torna alla curva che sta girando.", "Back to the curve that is running."))
        b.clicked.connect(self._ricarica_curva)
        rr.addWidget(b)
        self.b_applica = QPushButton(L("Applica", "Apply"))
        self.b_applica.setObjectName("primario")
        self.b_applica.setMinimumHeight(34)
        self.b_applica.clicked.connect(self._applica)
        rr.addWidget(self.b_applica)
        destra.addLayout(rr)
        gd = QWidget()
        gd.setLayout(destra)
        gd.setFixedWidth(246)
        corpo.addWidget(gd, 0)

        # --- bottom: the panels
        basso = QHBoxLayout()
        basso.setSpacing(6)
        basso.addWidget(QLabel(L("Pannelli:", "Panels:")))
        self.pannelli = {}
        for nome, titolo, costruisci in (
                ("cpu", "CPU", self._pan_cpu),
                ("core", L("Core", "Cores"), self._pan_core),
                ("cu", "CU", self._pan_cu),
                ("vram", "VRAM", self._pan_vram),
                ("avanzate", L("Avanzate", "Advanced"), self._pan_avanzate),
                ("test", "Test", self._pan_test)):
            b = QPushButton(titolo)
            b.clicked.connect(lambda _c=False, k=nome, t=titolo, f=costruisci: self._apri_pannello(k, t, f))
            basso.addWidget(b)
        basso.addStretch(1)
        v.addLayout(basso, 0)
        self._ricarica_curva()

    # ============================================================ curve
    def _ricarica_curva(self):
        self.conf = leggi_json(GOV_CONF, {})
        pts = self.conf.get("curva") or [[350, 700], [2100, 1050]]
        self.curva.imposta(pts)
        self.curva.tetto = int(self.conf.get("freq_max", pts[-1][0]))
        self.tetto.blockSignals(True)
        self.tetto.setValue(self.curva.tetto)
        self.tetto.blockSignals(False)
        self.curva.update()
        self._riempi_tabella()
        self.et_salva.setText(L("curva in uso", "curve in use"))
        self._segna_preset()

    def _riempi_tabella(self):
        self._tabella_muta = True
        self.tabella.setRowCount(len(self.curva.punti))
        for i, (x, y) in enumerate(self.curva.punti):
            for col, val in ((0, x), (1, y)):
                it = QTableWidgetItem("%d" % val)
                it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabella.setItem(i, col, it)
        self._tabella_muta = False

    def _tabella_cambiata(self, item):
        if self._tabella_muta:
            return
        try:
            val = int(item.text())
        except ValueError:
            self._riempi_tabella()
            return
        i, col = item.row(), item.column()
        if not (0 <= i < len(self.curva.punti)):
            return
        x, y = self.curva.punti[i]
        if col == 0:
            x = max(self.curva.MHZ_MIN, min(self.curva.MHZ_MAX, val))
        else:
            y = max(self.curva.MV_MIN, min(self.curva.MV_MAX, val))
        self.curva.punti[i] = [int(x), int(y)]
        self.curva._fatto()          # sorts, keeps it monotonic, emits cambiata

    def _aggiungi_punto(self):
        pts = self.curva.punti
        i = self.tabella.currentRow()
        if i < 0 or i >= len(pts) - 1:
            i = len(pts) - 1
            nuovo = [min(self.curva.MHZ_MAX, pts[i][0] + 50), pts[i][1]] if pts else [1000, 800]
        else:
            nuovo = [(pts[i][0] + pts[i + 1][0]) // 2, (pts[i][1] + pts[i + 1][1]) // 2]
        pts.append(nuovo)
        self.curva._fatto()

    def _togli_punto(self):
        i = self.tabella.currentRow()
        if 0 <= i < len(self.curva.punti) and len(self.curva.punti) > 2:
            del self.curva.punti[i]
            self.curva._fatto()

    def _segna_preset(self):
        for b in self.gruppo_preset.buttons():
            self.gruppo_preset.setExclusive(False)
            b.setChecked({"prudente": 1850, "equilibrato": 2000, "misurato": 2100}.get(b.chiave) == self.curva.tetto
                         and (b.chiave != "misurato" or len(self.curva.punti) >= 10))
            self.gruppo_preset.setExclusive(True)

    def _curva_toccata(self):
        pts = self.curva.punti
        if pts:
            self.tetto.blockSignals(True)
            self.tetto.setValue(max(pts[0][0], min(pts[-1][0], self.tetto.value())))
            self.tetto.blockSignals(False)
            self.curva.tetto = self.tetto.value()
        self._riempi_tabella()
        self.et_salva.setText(L("modificata, non applicata", "changed, not applied"))
        self._segna_preset()

    def _tetto_cambiato(self, v):
        pts = self.curva.punti
        if pts:
            v = max(pts[0][0], min(pts[-1][0], v))
            if v != self.tetto.value():
                self.tetto.blockSignals(True)
                self.tetto.setValue(v)
                self.tetto.blockSignals(False)
        self.curva.tetto = v
        self.curva.update()
        self.et_salva.setText(L("modificata, non applicata", "changed, not applied"))
        self._segna_preset()

    def _preset(self, bottone):
        tetto = {"prudente": 1850, "equilibrato": 2000, "misurato": 2100}[bottone.chiave]
        if bottone.chiave == "misurato":
            pred = leggi_json(CURVA_PREDEFINITA, {})
            if pred.get("curva"):
                self.curva.imposta(pred["curva"])
                self._riempi_tabella()
        pts = self.curva.punti
        if pts and tetto > pts[-1][0]:
            tetto = pts[-1][0]
        self.tetto.setValue(tetto)
        self.et_salva.setText(L("%s: premi Applica", "%s: press Apply") % bottone.text())

    def _conf_candidata(self):
        c = dict(self.conf)
        c["curva"] = [[int(x), int(y)] for x, y in self.curva.punti]
        c["freq_max"] = int(self.tetto.value())
        return c

    def _applica(self):
        if self._occupato:
            return
        cand = self._conf_candidata()
        self._occupato = True
        self.b_applica.setEnabled(False)
        self.et_salva.setText(L("metto in prova…", "starting the trial…"))
        in_sfondo(lambda: self.demone.cmd(cmd="gov-prova", conf=cand), self._provata, self)

    def _provata(self, r):
        self._occupato = False
        self.b_applica.setEnabled(True)
        if not r.get("ok"):
            self.et_salva.setText(r.get("err", L("non applicata", "not applied")))
            if r.get("err") and "prova in corso" in r.get("err", ""):
                self.demone.cmd(cmd="gov-annulla")
            return
        d = ProvaCurva(SECONDI_PROVA, self)
        d.exec()
        if d.tenuta:
            r2 = self.demone.cmd(cmd="gov-conferma")
            self.et_salva.setText(L("applicata", "applied") if r2.get("ok") else r2.get("err", "?"))
        else:
            self.demone.cmd(cmd="gov-annulla")
            self.et_salva.setText(L("annullata: torna la curva di prima", "cancelled: the previous curve is back"))
        self._ricarica_curva()

    # systemctl is-enabled is a process and this page ticks every second, so
    # the boot state is re-read every few seconds instead of every frame.
    INTERVALLO_BOOT = 5.0

    def _gov_al_boot(self):
        """Whether the governor comes back at the next boot.

        ⚠️ is-enabled exits 1 when the unit is disabled, so the word it prints
        decides and not the return code."""
        adesso = time.time()
        if self._gov_boot is None or adesso - self._gov_boot_letto > self.INTERVALLO_BOOT:
            _, out, _ = sh("systemctl is-enabled " + GOV_UNIT, 10)
            self._gov_boot = out.strip() == "enabled"
            self._gov_boot_letto = adesso
        return self._gov_boot

    def _governor_on_off(self, on):
        r = self.demone.cmd(cmd="gov-attiva", on=bool(on))
        self._gov_boot = None          # the click just changed it: read it again
        if not r.get("ok"):
            self.toast(r.get("err", "?"))
            self.interruttore.setChecked(not on)

    # ============================================================ readings
    def aggiorna(self):
        adesso = time.time()
        b = battito()
        vivo = bool(b) and adesso - b["quando"] < 5
        val = {}
        if b:
            val.update(gpu_mhz=b["mhz"], tetto=b["tetto"], gpu_c=b["gradi"], gpu_w=b["watt"], carico=b["carico"])
        else:
            mhz = hwmon_valore("amdgpu", "freq1_input")
            t = hwmon_valore("amdgpu", "temp1_input")
            w = hwmon_valore("amdgpu", "power1_average") or hwmon_valore("amdgpu", "power1_input")
            val.update(gpu_mhz=mhz // 1000000 if mhz else None, gpu_c=t / 1000.0 if t else None,
                       gpu_w=w / 1e6 if w else None)
        mv = hwmon_valore("amdgpu", "in0_input")
        val["gpu_mv"] = mv
        val["cpu_mhz"] = cpu_media_mhz()
        tc = hwmon_valore("k10temp", "temp1_input")
        val["cpu_c"] = tc / 1000.0 if tc else None
        for chiave, (coppia, etichetta, unita, colore) in self.tessere.items():
            v = val.get(chiave)
            for t in coppia:
                t.aggiorna({"etichetta": etichetta, "unita": unita, "colore": colore, "visibile": True,
                            "punti": [(adesso, v)] if v is not None else []})
        self.curva.aggiorna_vivo(val.get("gpu_mhz"), mv)
        self.b_stato.setText(L("governor attivo", "governor running") if vivo else L("governor fermo", "governor stopped"))
        self.b_stato.tono("bene" if vivo else "male")
        al_boot = self._gov_al_boot()
        # ticked only when both halves agree: running now AND coming back. A box
        # that only knew the first half read as "on and staying on" to a user
        # whose governor was about to disappear at the next boot.
        self.interruttore.blockSignals(True)
        self.interruttore.setChecked(vivo and al_boot)
        self.interruttore.blockSignals(False)
        self.interruttore.setToolTip("%s %s" % (
            L("Ora e' acceso.", "It is on now.") if vivo
            else L("Ora e' spento.", "It is off now."),
            L("Al prossimo avvio riparte.", "It comes back at the next boot.") if al_boot
            else L("Al prossimo avvio non riparte.", "It does not come back at the next boot.")))
        if os.path.exists("/run/skillfish/gov-prova.json") and not self._occupato:
            self.b_stato.setText(L("prova in corso", "trial running"))
            self.b_stato.tono("ottone")

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        if not self.costruita:
            return
        stretto = self.width() < 1250
        self.gab.setVisible(not stretto)
        self.striscia.setVisible(stretto)

    # ============================================================ panels
    def _apri_pannello(self, nome, titolo, costruisci):
        p = self.pannelli.get(nome)
        if p is None:
            p = Pannello(titolo, costruisci(), self)
            self.pannelli[nome] = p
        p.mostra()

    def _cfg(self):
        r = self.demone.cmd(cmd="get")
        self.cfg = r.get("data", {}) if r.get("ok") else {}
        return self.cfg

    # ---- CPU
    def _pan_cpu(self):
        cfg = self._cfg().get("cpu", {})
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(8)
        lim = self._limiti_cpu()
        self.cf = Manopola(lim["freq_min"], lim["freq_max"], cfg.get("frequency", 3500), "MHz")
        self.cs = Manopola(lim["scale_min"], lim["scale_max"], cfg.get("scale", 0), "", mostra=lambda s: ("−%.0f mV" % (-s * MV_PER_SCALINO)) if s else "0 mV")
        self.ct = Manopola(max(60, lim["temp_min"]), min(95, lim["temp_max"]), cfg.get("max_temperature", 85), "°C")
        for testo, cur, aiuto in (
                (L("Frequenza", "Clock"), self.cf, L("Il clock sotto carico. Sopra 3500 con otto core comanda il calore.", "The clock under load. Above 3500 with eight cores heat is in charge.")),
                (L("Undervolt", "Undervolt"), self.cs, L("Scalini di 6,25 mV tolti alla CPU: meno calore, stessa frequenza, fin dove regge.", "Steps of 6.25 mV taken off the CPU: less heat, same clock, as far as it holds.")),
                (L("Limite gradi", "Degree limit"), self.ct, L("Sopra, la guardia termica rallenta di 100 MHz alla volta e poi rialza.", "Above it the thermal guard slows by 100 MHz at a time, then raises again."))):
            r = QHBoxLayout()
            e = QLabel(testo)
            e.setMinimumWidth(100)
            r.addWidget(e)
            r.addWidget(Aiuto(aiuto, testo))
            r.addWidget(cur, 1)
            v.addLayout(r)
        r = QHBoxLayout()
        self.b_cpu = {}
        for chiave, testo, slot, primario in (
                ("uv", L("Suggerisci UV", "Suggest UV"), self._suggerisci_uv, False),
                ("max", L("Trova il massimo", "Find my max"), self._cpu_wizard, False),
                ("test", "Test 60 s", self._test_cpu, False),
                ("stop", "Stop", self._ferma_prova, False),
                ("applica", L("Applica", "Apply"), self._applica_cpu, True),
                ("salva", L("Salva al boot", "Save at boot"), self._salva_cpu, False)):
            b = QPushButton(testo)
            if primario:
                b.setObjectName("primario")
            b.clicked.connect(slot)
            self.b_cpu[chiave] = b
            r.addWidget(b)
        self.b_cpu["stop"].setEnabled(False)
        v.addLayout(r)
        self.et_cpu = QLabel("")
        self.et_cpu.setObjectName("quieto")
        self.et_cpu.setWordWrap(True)
        v.addWidget(self.et_cpu)
        self.et_conto = QLabel("")
        self.et_conto.setObjectName("numerone")
        self.et_conto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.et_conto.hide()
        v.addWidget(self.et_conto)
        return w

    def _valori_cpu(self):
        return self.cf.value(), self.cs.value(), self.ct.value()

    # What the panel offers when the daemon cannot be asked. Deliberately the
    # narrow range: offering more than the backend accepts is the bug itself.
    RIPIEGO_LIMITI = {"freq_min": 3500, "freq_max": 4500, "scale_min": -40,
                      "scale_max": 0, "temp_min": 0, "temp_max": 100}

    def _limiti_cpu(self):
        """What the backend will really accept. Asked, never assumed: the panel
        used to offer 2000-4500 MHz against a floor of 3500, and everything
        below it failed without a word."""
        r = self.demone.cmd(cmd="cpu-limits") or {}
        lim = dict(self.RIPIEGO_LIMITI)
        if r.get("ok"):
            lim.update(r.get("data") or {})
        return lim

    def _motivo_cpu(self, r):
        """Why the setting did not go in, in words the user can act on."""
        f = r.get("fuori") or {}
        frase = {
            "frequency": L("La frequenza accettata va da %d a %d MHz.",
                           "The accepted clock runs from %d to %d MHz."),
            "scale": L("L'undervolt accettato va da %d a %d scalini.",
                       "The accepted undervolt runs from %d to %d steps."),
            "max_temperature": L("Il limite gradi accettato va da %d a %d.",
                                 "The accepted degree limit runs from %d to %d."),
        }.get(f.get("campo"))
        if frase:
            return frase % (f.get("min", 0), f.get("max", 0))
        return r.get("err") or L("non applicata", "not applied")

    def _applica_cpu(self):
        m, s, t = self._valori_cpu()
        r = self.demone.cmd(cmd="apply-cpu", mhz=m, scale=s, temp=t)
        self.demone.cmd(cmd="thermal-guard", limit=t)
        self.et_cpu.setText(L("CPU applicata", "CPU applied") if r.get("ok") else self._motivo_cpu(r))

    def _salva_cpu(self):
        m, s, t = self._valori_cpu()
        r = self.demone.cmd(cmd="persist-cpu", mhz=m, scale=s, temp=t)
        self.et_cpu.setText(L("CPU salvata: vale anche al prossimo avvio", "CPU saved: applies at next boot too") if r.get("ok") else self._motivo_cpu(r))

    # every CPU test goes through one machinery: steps, countdown, Stop
    def _avvia_prova(self, passi, testo, fine):
        if self._prova is not None:
            return
        self._prova = ProvaCpu(self.demone, passi, self.ct.value(), self)
        self._prova_fine = fine
        self._prova_esiti = []
        self._prova.tick.connect(self._prova_tick)
        self._prova.passo.connect(self._prova_passo)
        self._prova.finito.connect(self._prova_finita)
        for k, b in self.b_cpu.items():
            b.setEnabled(k == "stop")
        self.et_cpu.setText(testo)
        self.et_conto.show()
        self._prova.start()

    def _prova_tick(self, etichetta, resto):
        self.et_conto.setText("%s   %d s" % (etichetta, resto))

    def _prova_passo(self, mhz, scale, tenuto, minimo):
        self._prova_esiti.append((mhz, scale, tenuto, minimo))
        self.et_cpu.setText(L("%d MHz @ %d: %s (min %d MHz)", "%d MHz @ %d: %s (min %d MHz)") % (
            mhz, scale, L("regge", "holds") if tenuto else L("NON regge", "does NOT hold"), minimo))

    def _prova_finita(self, migliore):
        fermata = self._prova is not None and self._prova._stop
        self._prova = None
        self.et_conto.hide()
        for k, b in self.b_cpu.items():
            b.setEnabled(k != "stop")
        # whatever happened, the CPU goes back to the applied values
        cfg = self._cfg().get("cpu", {})
        self.demone.cmd(cmd="apply-cpu", mhz=cfg.get("frequency", 3500), scale=cfg.get("scale", 0), temp=cfg.get("max_temperature", 85))
        if fermata:
            self.et_cpu.setText(L("Fermato. Valori di prima rimessi.", "Stopped. Previous values are back."))
            return
        self._prova_fine(migliore)

    def _ferma_prova(self):
        if self._prova is not None:
            self._prova.ferma()

    def _test_cpu(self):
        m, s, _t = self._valori_cpu()
        self._avvia_prova([(m, s, 60)], L("Test: un minuto di carico su tutti i thread…", "Test: a minute of load on every thread…"),
                          lambda best: (self.et_cpu.setText(L("Regge. Premi Applica per tenerlo.", "Holds. Press Apply to keep it.") if best else L("Non regge: valori di prima rimessi.", "Does not hold: previous values are back."))))

    def _suggerisci_uv(self):
        m = self.cf.value()
        passi = [(m, s, 12) for s in range(0, -41, -2)]
        self._avvia_prova(passi, L("Cerco l'undervolt per %d MHz: dodici secondi a scalino, mi fermo al primo che non regge.",
                                   "Looking for the undervolt at %d MHz: twelve seconds a step, stopping at the first that does not hold.") % m,
                          self._uv_trovato)

    def _uv_trovato(self, best):
        if not best:
            self.et_cpu.setText(L("Nemmeno lo scalino 0 regge a questa frequenza.", "Not even step 0 holds at this clock."))
            return
        self.cs.setValue(best[1])
        self.et_cpu.setText(L("Suggerito: scalino %d (−%.0f mV). Premi Applica.", "Suggested: step %d (−%.0f mV). Press Apply.") % (best[1], -best[1] * MV_PER_SCALINO))

    CPU_WIZ = [(3600, -8), (3700, -16), (3800, -20), (3900, -24), (4000, -36)]

    def _cpu_wizard(self):
        if QMessageBox.question(self, L("Trova il massimo", "Find my max"), L(
                "Da 3600 a 4000 MHz con undervolt crescente, trenta secondi a scalino, si ferma al primo che non regge. "
                "L'ultimo scalino puo' piantare alcune schede: il watchdog riavvia e tornano i valori buoni. Procedere?",
                "From 3600 to 4000 MHz with growing undervolt, thirty seconds a step, stops at the first that does not hold. "
                "The last step can hang some boards: the watchdog reboots and the good values are back. Proceed?")) != QMessageBox.StandardButton.Yes:
            return
        self._avvia_prova([(f, s, 30) for f, s in self.CPU_WIZ], L("Cerco il massimo…", "Looking for the maximum…"), self._wiz_fine)

    def _wiz_fine(self, best):
        if not best:
            self.et_cpu.setText(L("Nemmeno 3600 regge: resta com'era.", "Not even 3600 holds: left as it was."))
            return
        f, s = best
        self.cf.setValue(f)
        self.cs.setValue(s)
        self.et_cpu.setText(L("Massimo che regge: %d MHz @ %d. Premi Applica.", "Highest that holds: %d MHz @ %d. Press Apply.") % (f, s))

    # ---- cores
    def _pan_core(self):
        st = self.demone.cmd(cmd="cpu-cores") or {}
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(8)
        self.core_stato = st.get("cores", [])
        self.core_voluti = {c["core"]: c["online"] for c in self.core_stato}
        g = QGridLayout()
        g.setSpacing(6)
        self.core_bottoni = {}
        for i, c in enumerate(self.core_stato):
            b = QPushButton("%d" % c["core"])
            b.setCheckable(True)
            b.setChecked(c["online"])
            b.setEnabled(c.get("removable", True))
            b.setFixedWidth(44)
            b.toggled.connect(lambda on, k=c["core"]: self._core_toggle(k, on))
            self.core_bottoni[c["core"]] = b
            g.addWidget(b, i // 8, i % 8)
        v.addLayout(g)
        self.et_core = QLabel("")
        self.et_core.setStyleSheet("color:%s;" % stile.OTTONE)
        v.addWidget(self.et_core)
        r = QHBoxLayout()
        for testo, n in ((L("Tutti", "All"), 99), ("6", 6), ("4", 4)):
            b = QPushButton(testo)
            b.clicked.connect(lambda _c=False, k=n: self._core_preset(k))
            r.addWidget(b)
        self.smt = QCheckBox("SMT")
        self.smt.setChecked((st.get("smt") or "on") == "on")
        self.smt.setEnabled(bool(st.get("smt")))
        self.smt.toggled.connect(self._smt)
        r.addWidget(self.smt)
        r.addWidget(Aiuto(L("Due thread per core. Spento, uno.", "Two threads per core. Off, one."), "SMT"))
        r.addStretch(1)
        b = QPushButton(L("Applica", "Apply"))
        b.setObjectName("primario")
        b.clicked.connect(self._applica_core)
        r.addWidget(b)
        v.addLayout(r)
        # the two hidden cores
        cu = self.demone.cmd(cmd="core-unlock") or {}
        efi = self.demone.cmd(cmd="coreunlock-efi") or {}
        r = QHBoxLayout()
        self.core8 = QCheckBox(L("Sblocca gli 8 core", "Unlock the 8 cores"))
        self.core8.setChecked(bool(cu.get("abilitato")))
        self.core8.setEnabled(bool(cu.get("supportato")))
        self.core8.toggled.connect(self._core8)
        r.addWidget(self.core8)
        r.addWidget(Aiuto(L(
            "I due core che la BC-250 tiene spenti: 6c/12t diventa 8c/16t, +20% misurato. "
            "Con lo sblocco EFI avviene prima di GRUB in un avvio solo; senza, il servizio "
            "lo fa con un riavvio in piu' a ogni accensione da spenta.",
            "The two cores the BC-250 keeps off: 6c/12t becomes 8c/16t, +20% measured. "
            "With the EFI unlock it happens before GRUB in a single boot; without it the "
            "service does it with one extra reboot on every cold start."), L("8 core", "8 cores")))
        self.efi8 = QCheckBox(L("Prima dell'avvio (EFI)", "Before boot (EFI)"))
        self.efi8.setChecked(bool(efi.get("installato")) and bool(efi.get("primo")))
        self.efi8.setEnabled(bool(efi.get("supportato")) and bool(cu.get("supportato")))
        self.efi8.toggled.connect(self._efi8)
        r.addWidget(self.efi8)
        r.addWidget(Aiuto(L("Il programma EFI di Hexxeh, primo nell'ordine di avvio: sblocca e fa un reset caldo prima del sistema. Provato: un avvio solo.",
                            "Hexxeh's EFI program, first in the boot order: unlocks and warm-resets before the system. Verified: one boot only."), "EFI"))
        r.addStretch(1)
        v.addLayout(r)
        self._core_conta()
        return w

    def _core_toggle(self, k, on):
        self.core_voluti[k] = on
        self._core_conta()

    def _core_conta(self):
        n = sum(1 for x in self.core_voluti.values() if x)
        thr = n * (2 if self.smt.isChecked() else 1)
        self.et_core.setText(L("Core attivi: %d / %d  ·  %d thread", "Active cores: %d / %d  ·  %d threads") % (n, len(self.core_voluti) or 8, thr))

    def _core_preset(self, tieni):
        for c in self.core_stato:
            want = True if tieni >= len(self.core_stato) else c["core"] < tieni
            if not c.get("removable", True):
                want = True
            b = self.core_bottoni.get(c["core"])
            if b:
                b.setChecked(want)

    def _smt(self, on):
        r = self.demone.cmd(cmd="cpu-smt", on=bool(on))
        self.toast(L("SMT %s", "SMT %s") % (L("acceso", "on") if on else L("spento", "off")) if r.get("ok") else r.get("err", "?"))
        self._core_conta()

    def _core8(self, on):
        r = self.demone.cmd(cmd="core-unlock-set", on=bool(on))
        self.toast(L("Sblocco 8 core %s: vale dal prossimo avvio.", "8-core unlock %s: from the next boot.") % (L("acceso", "on") if on else L("spento", "off")) if r.get("ok") else r.get("err", "?"), 6)

    def _efi8(self, on):
        r = self.demone.cmd(cmd="coreunlock-efi-set", on=bool(on))
        if r.get("ok"):
            self.toast(L("Sblocco EFI %s.", "EFI unlock %s.") % (L("installato, primo all'avvio", "installed, first at boot") if on else L("tolto", "removed")), 6)
        else:
            self.toast(r.get("out") or r.get("err", "?"), 8)
            self.efi8.blockSignals(True)
            self.efi8.setChecked(not on)
            self.efi8.blockSignals(False)

    def _applica_core(self):
        r = self.demone.cmd(cmd="cpu-cores-set", cores=[{"core": k, "online": bool(v)} for k, v in self.core_voluti.items()])
        self.toast(L("Core applicati: %d thread", "Cores applied: %d threads") % r.get("nproc", 0) if r.get("ok") else r.get("err", "?"))

    # ---- compute units
    CU_VERDE = "QPushButton{background:#2e5a2a;border:1px solid #8fbf6a;color:#d4f0a0;font-weight:700;}"
    CU_ROSSO = "QPushButton{background:#5a2a2a;border:1px solid #d85a5a;color:#f0b0b0;}"

    def _pan_cu(self):
        cu = (self.demone.cmd(cmd="cu-get") or {})
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(8)
        # One pair per row, and the daemon says so rather than this file
        # guessing. There used to be a floor of three here, greyed out and
        # OR-ed into everything, and it was not real.
        self.cu_min = int(cu.get("min_wgp", 1)) or 1
        self.cu_ordine = ["0.0", "0.1", "1.0", "1.1"]
        righe = cu.get("rows") or {k: 31 for k in self.cu_ordine}
        self.cu_righe = {k: int(righe.get(k, 31)) or self.cu_min for k in self.cu_ordine}
        e = QLabel(L("Verde acceso, rosso spento. Ogni casella e' una coppia di CU. Almeno una per riga deve restare accesa.",
                     "Green on, red off. Every cell is a pair of CUs. At least one per row has to stay on."))
        e.setWordWrap(True)
        e.setObjectName("quieto")
        v.addWidget(e)
        g = QGridLayout()
        g.setSpacing(6)
        for c in range(5):
            et = QLabel("WGP %d" % c)
            et.setObjectName("didascalia")
            et.setAlignment(Qt.AlignmentFlag.AlignCenter)
            g.addWidget(et, 0, c + 1)
        self.cu_celle = {}
        for r, rk in enumerate(self.cu_ordine):
            et = QLabel("SE%s SH%s" % (rk[0], rk[2]))
            et.setObjectName("quieto")
            g.addWidget(et, r + 1, 0)
            for wgp in range(5):
                b = QPushButton("CU %d-%d" % (r * 10 + wgp * 2, r * 10 + wgp * 2 + 1))
                b.setCheckable(True)
                b.setFixedSize(80, 30)
                b.setChecked(bool(self.cu_righe[rk] & (1 << wgp)))
                b.toggled.connect(lambda on, rk=rk, wgp=wgp: self._cu_toggle(rk, wgp, on))
                self.cu_celle[(rk, wgp)] = b
                g.addWidget(b, r + 1, wgp + 1)
        v.addLayout(g)
        r = QHBoxLayout()
        r.addWidget(QLabel("<b>%s</b>" % L("CU attive", "Active CUs")))
        self.cu_n = QSpinBox()
        self.cu_n.setRange(len(self.cu_ordine) * 2, 40)
        self.cu_n.setSingleStep(2)
        self.cu_n.valueChanged.connect(self._cu_da_numero)
        r.addWidget(self.cu_n)
        r.addWidget(Aiuto(L("Scrivi quante CU vuoi, a coppie: le caselle si accendono da sole, prima una colonna poi l'altra. Oppure clicca le caselle.",
                            "Type how many CUs you want, in pairs: the cells light up by themselves, one column then the other. Or click the cells."), "CU"))
        for n in (24, 32, 36, 40):
            b = QPushButton("%d" % n)
            b.setFixedWidth(44)
            b.clicked.connect(lambda _c=False, k=n: self.cu_n.setValue(k))
            r.addWidget(b)
        r.addStretch(1)
        self.et_cu = QLabel("")
        self.et_cu.setStyleSheet("color:%s;font-weight:700;" % stile.OTTONE)
        r.addWidget(self.et_cu)
        v.addLayout(r)
        r = QHBoxLayout()
        r.addStretch(1)
        b = QPushButton("Test CU")
        b.setToolTip(L("Prova una coppia alla volta sotto vkpeak, tutte e cinque le posizioni, e guarda se la GPU fa errori. Cinque minuti circa.",
                       "Tries one pair at a time under vkpeak, all five positions, and watches for GPU errors. About five minutes."))
        b.clicked.connect(self._test_cu)
        r.addWidget(b)
        b = QPushButton(L("Applica", "Apply"))
        b.setObjectName("primario")
        b.clicked.connect(self._applica_cu)
        r.addWidget(b)
        v.addLayout(r)
        r = QHBoxLayout()
        self.cu_al_boot = QCheckBox(L("Mantieni all'avvio", "Keep at boot"))
        self.cu_al_boot.setToolTip(L(
            "La scheda riparte con questa mappatura invece che con tutte le CU accese. Applica prima, poi spunta.",
            "The board comes back with this mapping instead of every CU on. Apply first, then tick."))
        self.cu_al_boot.setChecked(bool(cu.get("keep_boot")))
        self.cu_al_boot.clicked.connect(self._cu_boot_switch)
        r.addWidget(self.cu_al_boot)
        r.addWidget(Aiuto(L(
            "Senza la spunta la scheda accende tutte le CU a ogni avvio, che e' quello che serve quasi sempre. "
            "Con la spunta riparte con le coppie scelte qui: serve quando una coppia e' guasta e va lasciata spenta.",
            "Unticked, the board turns every CU on at each boot, which is what almost everyone wants. Ticked, it "
            "comes back with the pairs chosen here: that is what you need when a pair is faulty and has to stay off."),
            L("Mantieni all'avvio", "Keep at boot")))
        r.addStretch(1)
        v.addLayout(r)
        self._cu_colora()
        return w

    def _cu_motivo(self, r):
        """Why a CU change did not go through, in words the user can act on."""
        return {
            "riga-vuota": L("Ogni riga deve avere almeno una coppia accesa.",
                            "Every row needs at least one pair on."),
            "maschere-storte": L("Le quattro righe non sono valide.",
                                 "The four rows are not valid."),
            "non-applicata": L("Applica la scelta prima di tenerla all'avvio.",
                               "Apply the selection before keeping it at boot."),
        }.get(r.get("motivo")) or r.get("err") or "?"

    def _cu_boot_switch(self, on):
        r = self.demone.cmd(cmd="cu-keep-boot", on=bool(on),
                            rows=[self.cu_righe[rk] for rk in self.cu_ordine]) or {}
        if not r.get("ok"):
            self.toast(self._cu_motivo(r), 6)
            self.cu_al_boot.blockSignals(True)
            self.cu_al_boot.setChecked(not on)
            self.cu_al_boot.blockSignals(False)
            return
        self.toast(L("La scheda ripartira' con questa mappatura", "The board will come back with this mapping")
                   if on else L("Al prossimo avvio tornano tutte accese", "Every CU comes back on at the next boot"), 5)

    def _cu_toggle(self, rk, wgp, on):
        m = self.cu_righe.get(rk, 31)
        nuova = (m | (1 << wgp)) if on else (m & ~(1 << wgp))
        if nuova == 0:
            # the last pair of a row: refused, and said out loud. Disabling the
            # button instead is what the old floor did, and it left the user
            # with no idea why the cell would not move.
            self.cu_celle[(rk, wgp)].blockSignals(True)
            self.cu_celle[(rk, wgp)].setChecked(True)
            self.cu_celle[(rk, wgp)].blockSignals(False)
            self.et_cu.setText(L("Almeno una coppia per riga", "At least one pair per row"))
            return
        self.cu_righe[rk] = nuova
        self._cu_colora()

    def _cu_conta(self):
        return sum(bin(self.cu_righe.get(rk, 31)).count("1") * 2 for rk in self.cu_ordine)

    def _cu_colora(self):
        for (rk, wgp), b in self.cu_celle.items():
            acceso = bool(self.cu_righe.get(rk, 31) & (1 << wgp))
            b.setStyleSheet(self.CU_VERDE if acceso else self.CU_ROSSO)
        n = self._cu_conta()
        self.et_cu.setText("%d / 40" % n)
        self.cu_n.blockSignals(True)
        self.cu_n.setValue(n)
        self.cu_n.blockSignals(False)

    def _cu_da_numero(self, n):
        """n CUs into pairs: one per row first, then a column at a time."""
        coppie = max(len(self.cu_ordine), n // 2)
        for rk in self.cu_ordine:
            self.cu_righe[rk] = 1 << 0
        coppie -= len(self.cu_ordine)
        for wgp in range(1, 5):
            for rk in self.cu_ordine:
                if coppie <= 0:
                    break
                self.cu_righe[rk] |= (1 << wgp)
                coppie -= 1
        for (rk, wgp), b in self.cu_celle.items():
            b.blockSignals(True)
            b.setChecked(bool(self.cu_righe[rk] & (1 << wgp)))
            b.blockSignals(False)
        self._cu_colora()

    def _applica_cu(self):
        r = self.demone.cmd(cmd="cu-apply",
                            rows=[self.cu_righe.get(rk, 31) for rk in self.cu_ordine]) or {}
        if not r.get("ok"):
            self.toast(self._cu_motivo(r), 6)
            return
        self.toast(L("CU applicate: %s/40", "CUs applied: %s/40") % r.get("active", "?"), 6)
        # a mapping kept for boot and then changed is no longer what was kept
        if self.cu_al_boot.isChecked():
            self._cu_boot_switch(True)

    def _test_cu(self):
        if QMessageBox.question(self, "Test CU", L(
                "Prova una coppia di CU alla volta sotto vkpeak, in tutte e cinque le posizioni, e guarda se la GPU fa errori. "
                "Circa cinque minuti, e alla fine rimette la scelta di adesso. Procedere?",
                "Tries one CU pair at a time under vkpeak, in all five positions, and watches for GPU errors. "
                "About five minutes, and it puts the current selection back at the end. Proceed?")) != QMessageBox.StandardButton.Yes:
            return
        self.et_cu.setText(L("test…", "testing…"))
        in_sfondo(lambda: self.demone.cmd(cmd="cu-test"), self._cu_testate, self)

    def _cu_testate(self, r):
        self._cu_colora()
        if not r.get("ok"):
            QMessageBox.warning(self, "Test CU", r.get("err", "?"))
            return
        righe = [L("40 CU sotto sforzo: %s GFLOPS", "40 CU under load: %s GFLOPS") % r.get("full40", "?"),
                 L("24 CU: %s GFLOPS", "24 CU: %s GFLOPS") % r.get("baseline", "?"), ""]
        for x in r.get("results", []):
            righe.append("SE%s SH%s WGP%d: %s%s" % (x["row"][0], x["row"][2], x["wgp"], x["verdict"],
                                                    (" · %d err" % x["errors"]) if x["errors"] else ""))
        righe.append("")
        righe.append(L("Difetti trovati: possibile CU rotta, tienine meno.", "Problems found: a CU may be bad, keep fewer.")
                     if (r.get("bad") or r.get("full40_err")) else L("Nessun difetto.", "No defects."))
        QMessageBox.information(self, "Test CU", "\n".join(righe))

    # ---- VRAM
    def _pan_vram(self):
        cur = self._cfg().get("vram", {}).get("uma_mb", 0)
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(8)
        r = QHBoxLayout()
        e = QLabel(L("Adesso: %d MB (%.1f GB)", "Now: %d MB (%.1f GB)") % (cur, cur / 1024.0))
        e.setStyleSheet("color:%s;font-weight:700;" % stile.OTTONE)
        r.addWidget(e)
        r.addWidget(Aiuto(L(
            "Memoria riservata alla GPU nel CMOS, vale dal prossimo avvio. Con 512 MB dinamici "
            "alcuni giochi scelgono texture basse: se sono sfocate, prova 4 o 6 GB fissi.",
            "Memory set aside for the GPU in the CMOS, in force from the next boot. With the "
            "512 MB dynamic split some games pick low textures: if blurry, try 4 or 6 GB fixed."), "VRAM"))
        r.addStretch(1)
        v.addLayout(r)
        r = QHBoxLayout()
        self.vram = QSpinBox()
        self.vram.setRange(512, 12288)
        self.vram.setSingleStep(256)
        self.vram.setSuffix(" MB")
        self.vram.setValue(cur if cur else 8192)
        r.addWidget(self.vram)
        for mb, testo in ((512, "512 MB"), (1024, "1 GB"), (2048, "2 GB"), (4096, "4 GB"), (6144, "6 GB"), (8192, "8 GB")):
            b = QPushButton(testo)
            b.clicked.connect(lambda _c=False, k=mb: self.vram.setValue(k))
            r.addWidget(b)
        r.addStretch(1)
        v.addLayout(r)
        b = QPushButton(L("Imposta (riavvio)", "Set (reboot)"))
        b.setObjectName("primario")
        b.clicked.connect(self._set_vram)
        v.addWidget(b)
        return w

    def _set_vram(self):
        mb = self.vram.value()
        if QMessageBox.question(self, "VRAM", L("VRAM a %d MB? Serve un riavvio.", "VRAM to %d MB? A reboot is needed.") % mb) != QMessageBox.StandardButton.Yes:
            return
        r = self.demone.cmd(cmd="set-vram", mb=mb)
        self.toast(L("VRAM %d MB: riavvia per applicare", "VRAM %d MB: reboot to apply") % mb if r.get("ok") else r.get("err", L("non scritta", "not written")), 6)

    # ---- advanced
    def _pan_avanzate(self):
        c = leggi_json(GOV_CONF, {})
        w = QWidget()
        g = QGridLayout(w)
        g.setContentsMargins(0, 0, 0, 0)
        g.setHorizontalSpacing(10)
        self.av = {}
        voci = (
            ("margine_salita", L("Margine in salita", "Ascent margin"), "mV", 0, 80, L("Millivolt aggiunti solo mentre si sale. Spedito: 10.", "Millivolts added only while climbing. Shipped: 10.")),
            ("gradino", L("Gradino", "Step"), "MHz", 10, 300, L("Di quanto scende la frequenza a ogni passo quando il carico cala.", "How much the clock drops per step when the load falls.")),
            ("conferme_giu", L("Conferme in discesa", "Descent confirmations"), "", 1, 20, L("Giri di carico basso prima di scendere di un gradino.", "Low-load ticks before stepping down.")),
            ("gradi_ok", L("Gradi ok", "Degrees ok"), "°C", 60, 95, L("Sotto, il tetto puo' risalire.", "Below, the ceiling may climb back.")),
            ("gradi_max", L("Gradi max", "Degrees max"), "°C", 65, 97, L("Sopra, il tetto scende di 50 MHz per volta.", "Above, the ceiling walks down 50 MHz at a time.")),
            ("gradi_rottura", L("Gradi di rottura", "Degrees of breaking"), "°C", 70, 99, L("Sopra, il tetto crolla di 200 MHz in un colpo.", "Above, the ceiling drops 200 MHz in one go.")),
            ("watt_max", L("Watt max", "Watts max"), "W", 60, 220, L("Il nostro limite di potenza.", "Our own power limit.")),
            ("watt_ok", L("Watt ok", "Watts ok"), "W", 40, 200, L("Sotto, il tetto puo' risalire.", "Below, the ceiling may climb back.")),
        )
        for i, (k, testo, unita, lo, hi, aiuto) in enumerate(voci):
            g.addWidget(QLabel(testo), i, 0)
            g.addWidget(Aiuto(aiuto, testo), i, 1)
            s = QSpinBox()
            s.setRange(lo, hi)
            s.setSuffix((" " + unita) if unita else "")
            s.setValue(int(c.get(k, lo)))
            self.av[k] = s
            g.addWidget(s, i, 2)
        self.av_droop = QCheckBox(L("Insegui il rail (droop)", "Chase the rail (droop)"))
        self.av_droop.setChecked(bool(c.get("droop_attivo")))
        g.addWidget(self.av_droop, len(voci), 0, 1, 2)
        g.addWidget(Aiuto(L("Alza la tensione quando il sensore la vede cadere sotto la curva. Spento di serie.", "Raises the voltage when the sensor sees it sag below the curve. Off by default."), "droop"), len(voci), 2)
        b = QPushButton(L("Applica", "Apply"))
        b.setObjectName("primario")
        b.clicked.connect(self._applica_avanzate)
        g.addWidget(b, len(voci) + 1, 0, 1, 3)
        return w

    def _applica_avanzate(self):
        c = dict(leggi_json(GOV_CONF, {}))
        for k, s in self.av.items():
            c[k] = s.value()
        c["droop_attivo"] = self.av_droop.isChecked()
        r = self.demone.cmd(cmd="gov-set", conf=c)
        self.toast(L("Impostazioni applicate, governor riavviato", "Settings applied, governor restarted") if r.get("ok") else r.get("err", "?"), 6)
        self._ricarica_curva()

    # ---- tests
    def _pan_test(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(8)
        e = QLabel(L("vkpeak misura i GFLOPS della GPU con la curva in uso. Non prova la stabilita' di un gioco.",
                     "vkpeak measures the GPU GFLOPS with the curve in use. It does not prove a game stable."))
        e.setWordWrap(True)
        v.addWidget(e)
        r = QHBoxLayout()
        b = QPushButton("vkpeak")
        b.clicked.connect(self._bench_gpu)
        r.addWidget(b)
        b = QPushButton(L("Registro", "Log"))
        b.clicked.connect(self._giornale)
        r.addWidget(b)
        r.addWidget(link_doc("tuner"))
        r.addStretch(1)
        v.addLayout(r)
        self.et_test = QLabel("")
        self.et_test.setObjectName("quieto")
        self.et_test.setWordWrap(True)
        v.addWidget(self.et_test)
        return w

    def _bench_gpu(self):
        self.et_test.setText(L("vkpeak in corso…", "vkpeak running…"))
        in_sfondo(lambda: self.demone.cmd(cmd="bench-gpu"),
                  lambda r: self.et_test.setText(("%s %s · %s °C" % (r.get("score"), r.get("unit"), r.get("temp"))) if r.get("ok") else r.get("err", "?")), self)

    def _giornale(self):
        rc, out, _ = sh("journalctl -t skillfish-cc-helper -t skillfish-tuner-helper -t skillfish-vf-governor --no-pager -n 60 2>/dev/null", 10)
        QMessageBox.information(self, L("Registro", "Log"), out or L("(vuoto)", "(empty)"))

    def disattiva(self):
        super().disattiva()
        if self._prova is not None:
            self._prova.ferma()

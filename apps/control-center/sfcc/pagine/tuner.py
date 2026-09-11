# -*- coding: utf-8 -*-
"""Tuner: the GPU voltage/frequency curve, the CPU, the cores, the compute units.

THE CURVE IS THE THING. The governor holds one point at a time (MHz, mV) and
reads which mV from a curve of knots; the ceiling says how high it may go.
Here the curve is drawn inside the chart, its knots drag, and the live dot
shows where the GPU is right now. What you drag is what the governor runs.

APPLY IS A TRIAL. A curve that asks too little voltage hangs the board, and
on the BC-250 a hang means pulling the plug. So Apply starts the candidate
with the last known good curve still on disk, and counts down: if you do not
press Keep within the time, or the board dies and comes back, the good curve
is what boots. The tuner-helper did the same for the CPU; now the GPU has it.
"""
import os
import re
import time

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (QButtonGroup, QCheckBox, QComboBox, QDialog, QFrame, QGridLayout,
                             QHBoxLayout, QLabel, QMessageBox, QPushButton, QRadioButton,
                             QScrollArea, QSizePolicy, QSlider, QSpinBox, QVBoxLayout, QWidget)

from .. import stile
from ..comune import GOV_CONF, L, Aiuto, battito, hwmon_valore, leggi_json, leggi_testo, sh
from ..demone import in_sfondo
from ..finestra import PaginaBase
from ..grafico import CurvaVF, Grafico, GraficoSingolo
from ..stile import Scheda, Stato, Tessera, intestazione

CURVA_PREDEFINITA = "/usr/share/skillfish/vf-curva-predefinita.json"
MV_PER_SCALINO = 6.25          # the SMU voltage step of the CPU undervolt
SECONDI_PROVA = 25


def cpu_media_mhz():
    fs = [float(x) for x in re.findall(r'cpu MHz\s*:\s*([\d.]+)', leggi_testo("/proc/cpuinfo"))]
    return sum(fs) / len(fs) if fs else None


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


class Cursore(QWidget):
    """A slider with its value written next to it."""

    def __init__(self, lo, hi, val, unita="", passo=1, mostra=None, parent=None):
        super().__init__(parent)
        h = QHBoxLayout(self)
        h.setContentsMargins(0, 0, 0, 0)
        self.s = QSlider(Qt.Orientation.Horizontal)
        self.s.setRange(lo, hi)
        self.s.setSingleStep(passo)
        self.s.setPageStep(passo * 5)
        self.s.setValue(int(val))
        self.et = QLabel("")
        self.et.setMinimumWidth(96)
        self.et.setStyleSheet("font-weight:700;color:%s;" % stile.OTTONE)
        self.unita, self.mostra = unita, mostra
        self.s.valueChanged.connect(self._agg)
        h.addWidget(self.s, 1)
        h.addWidget(self.et)
        self._agg(self.s.value())

    def _agg(self, v):
        self.et.setText(self.mostra(v) if self.mostra else "%d %s" % (v, self.unita))

    def value(self):
        return self.s.value()

    def setValue(self, v):
        self.s.setValue(int(v))


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


class Pagina(PaginaBase):
    def __init__(self, finestra):
        super().__init__(finestra)
        self.intervallo_ms = 1000
        self.conf = {}
        self.tessere = {}
        self.pannelli_serie = {}
        self.cfg = {}
        self._occupato = False

    # ============================================================ build
    def costruisci(self):
        v = self.corpo_pieno()
        testa = QHBoxLayout()
        testa.addWidget(intestazione("Tuner", "", L(
            "Il grafico mostra gli ultimi cinque minuti: frequenza e tensione della GPU, "
            "il tetto, gradi, watt, carico, e la CPU. Le tessere a sinistra sono la legenda: "
            "clic per accendere o spegnere una linea, clic sulla linea per aprirla da sola "
            "con i numeri veri sugli assi.\n\n"
            "Nel riquadro c'e' la curva del governor: MHz in orizzontale, millivolt in "
            "verticale. Trascina un punto, doppio clic per aggiungerne uno, tasto destro "
            "per toglierlo. La riga tratteggiata e' il tetto: oltre non si va. Il pallino "
            "azzurro e' la GPU adesso.\n\n"
            "Applica mette la curva in prova con un conto alla rovescia: la curva vecchia "
            "resta su disco finche' non premi Tieni.",
            "The chart shows the last five minutes: GPU clock and voltage, the ceiling, "
            "degrees, watts, load, and the CPU. The tiles on the left are the legend: click "
            "to show or hide a line, click a line to open it alone with real axes.\n\n"
            "The box holds the governor's curve: MHz across, millivolts up. Drag a point, "
            "double-click to add one, right-click to remove it. The dashed line is the "
            "ceiling: it never goes beyond. The blue dot is the GPU right now.\n\n"
            "Apply runs the curve on trial with a countdown: the old curve stays on disk "
            "until you press Keep.")))
        testa.addStretch(1)
        self.b_stato = Stato("", "quieto")
        testa.addWidget(self.b_stato)
        self.interruttore = QCheckBox(L("Governor", "Governor"))
        self.interruttore.setToolTip(L("Spento: il clock torna al governor di serie.",
                                       "Off: the clock goes back to the stock governor."))
        self.interruttore.clicked.connect(self._governor_on_off)
        testa.addWidget(self.interruttore)
        testa.addWidget(Aiuto(L(
            "Il nostro governor forza il clock attraverso il firmware e si prende la protezione "
            "che forzare toglie: il tetto scende quando la scheda scalda o tira troppo. Spento, "
            "comanda il governor di serie di Cyan Skillfish, che chiede il clock invece di "
            "forzarlo e sopra i 2200 MHz viene rifiutato.",
            "Our governor forces the clock through the firmware and takes on the protection "
            "that forcing gives up: the ceiling drops when the board gets hot or draws too much. "
            "Off, the stock Cyan Skillfish governor is in charge: it asks for the clock instead "
            "of forcing it, and is refused above 2200 MHz."), "Governor"))
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

        self.curva = CurvaVF()
        self.curva.cambiata.connect(self._curva_toccata)
        self.grafico = Grafico(self.curva)
        self.grafico.nuova_serie = self._rifai_tessere
        self.grafico.apri_serie = self._apri_serie
        corpo.addWidget(self.grafico, 1)

        # --- the strip at the bottom: ceiling, presets, panels, apply
        basso = QHBoxLayout()
        basso.setSpacing(12)
        v.addLayout(basso, 0)

        gc = QVBoxLayout()
        gc.setSpacing(4)
        r = QHBoxLayout()
        r.addWidget(QLabel("<b>%s</b>" % L("Tetto", "Ceiling")))
        self.tetto = QSpinBox()
        self.tetto.setRange(350, 2300)
        self.tetto.setSingleStep(50)
        self.tetto.setSuffix(" MHz")
        self.tetto.valueChanged.connect(self._tetto_cambiato)
        r.addWidget(self.tetto)
        r.addWidget(Aiuto(L(
            "Fin dove il governor puo' spingere il clock. Misurato sulla scheda di sviluppo: "
            "2100 tiene, 2150 regge una sera e poi cade, 2230 pianta Cyberpunk in tre minuti. "
            "Ogni scheda e' diversa: sali di 50 alla volta e gioca a Cyberpunk, che e' l'unico "
            "a caricare CPU e GPU insieme.",
            "How far the governor may push the clock. Measured on the development board: 2100 "
            "holds, 2150 lasts an evening and then falls, 2230 hangs Cyberpunk in three minutes. "
            "Every board differs: go up 50 at a time and play Cyberpunk, the only game that "
            "loads CPU and GPU together."), L("Tetto", "Ceiling")))
        r.addStretch(1)
        gc.addLayout(r)
        pr = QHBoxLayout()
        pr.setSpacing(6)
        self.gruppo_preset = QButtonGroup(self)
        for chiave, testo, aiuto in (
                ("prudente", L("Prudente", "Cautious"), L("Tetto a 1850 MHz: il punto dolce di una scheda con il dissipatore di serie. Quasi gli stessi fotogrammi, dieci gradi in meno.", "Ceiling at 1850 MHz: the sweet spot of a board with the stock heatsink. Nearly the same frames, ten degrees less.")),
                ("equilibrato", L("Equilibrato", "Balanced"), L("Tetto a 2000 MHz.", "Ceiling at 2000 MHz.")),
                ("misurato", L("Misurato", "Measured"), L("Tetto a 2100 MHz con la curva a quindici punti misurata sulla scheda di sviluppo: e' quella che spediamo.", "Ceiling at 2100 MHz with the fifteen-point curve measured on the development board: the one we ship."))):
            b = QRadioButton(testo)
            b.chiave = chiave
            self.gruppo_preset.addButton(b)
            pr.addWidget(b)
            pr.addWidget(Aiuto(aiuto, testo))
        self.gruppo_preset.buttonClicked.connect(self._preset)
        pr.addStretch(1)
        gc.addLayout(pr)
        basso.addLayout(gc)

        pann = QGridLayout()
        pann.setSpacing(6)
        self.pannelli = {}
        for i, (nome, titolo, costruisci) in enumerate((
                ("cpu", "CPU", self._pan_cpu),
                ("core", L("Core", "Cores"), self._pan_core),
                ("cu", "CU", self._pan_cu),
                ("vram", "VRAM", self._pan_vram),
                ("avanzate", L("Avanzate", "Advanced"), self._pan_avanzate),
                ("test", "Test", self._pan_test))):
            b = QPushButton(titolo)
            b.clicked.connect(lambda _c=False, k=nome, t=titolo, f=costruisci: self._apri_pannello(k, t, f))
            pann.addWidget(b, i // 3, i % 3)
        basso.addLayout(pann)
        basso.addStretch(1)

        fine = QVBoxLayout()
        fine.setSpacing(4)
        self.et_salva = QLabel("")
        self.et_salva.setObjectName("quieto")
        self.et_salva.setWordWrap(True)
        fine.addWidget(self.et_salva)
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
        fine.addLayout(rr)
        basso.addLayout(fine)

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
        self.et_salva.setText(L("curva in uso", "curve in use"))
        self._segna_preset()

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
            self.et_salva.setObjectName("male")
            self.et_salva.style().polish(self.et_salva)
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
        self.et_salva.setObjectName("quieto")
        self.et_salva.style().polish(self.et_salva)
        self._ricarica_curva()

    def _governor_on_off(self, on):
        r = self.demone.cmd(cmd="gov-attiva", on=bool(on))
        if not r.get("ok"):
            self.toast(r.get("err", "?"))
            self.interruttore.setChecked(not on)

    # ============================================================ readings
    def aggiorna(self):
        adesso = time.time()
        letture = []
        b = battito()
        vivo = bool(b) and adesso - b["quando"] < 5
        if b:
            letture += [("gpu_mhz", "GPU MHz", "MHz", b["mhz"], stile.OTTONE),
                        ("tetto", L("Tetto", "Ceiling"), "MHz", b["tetto"], "#9a7a3a"),
                        ("gpu_c", "GPU °C", "C", b["gradi"], stile.ARANCIO),
                        ("gpu_w", "GPU W", "W", b["watt"], stile.VIOLA),
                        ("carico", L("Carico GPU", "GPU load"), "%", b["carico"], stile.VERDE)]
        else:
            mhz = hwmon_valore("amdgpu", "freq1_input")
            t = hwmon_valore("amdgpu", "temp1_input")
            w = hwmon_valore("amdgpu", "power1_average") or hwmon_valore("amdgpu", "power1_input")
            letture += [("gpu_mhz", "GPU MHz", "MHz", mhz // 1000000 if mhz else None, stile.OTTONE),
                        ("gpu_c", "GPU °C", "C", t // 1000 if t else None, stile.ARANCIO),
                        ("gpu_w", "GPU W", "W", w / 1e6 if w else None, stile.VIOLA)]
        mv = hwmon_valore("amdgpu", "in0_input")
        letture.append(("gpu_mv", "GPU mV", "mV", mv, stile.COL_VOLT))
        letture.append(("cpu_mhz", "CPU MHz", "MHz", cpu_media_mhz(), "#9bd24f"))
        tc = hwmon_valore("k10temp", "temp1_input")
        letture.append(("cpu_c", "CPU °C", "C", tc / 1000.0 if tc else None, "#e8c878"))
        self.grafico.campiona(adesso, letture)
        for chiave, serie in self.grafico.elenco():
            w = self.tessere.get(chiave)
            if w is not None:
                w.aggiorna(serie)
        self.curva.aggiorna_vivo(b["mhz"] if b else None, mv)
        # the badge and the switch
        self.b_stato.setText(L("governor attivo", "governor running") if vivo else L("governor fermo", "governor stopped"))
        self.b_stato.tono("bene" if vivo else "male")
        self.interruttore.blockSignals(True)
        self.interruttore.setChecked(vivo)
        self.interruttore.blockSignals(False)
        if os.path.exists("/run/skillfish/gov-prova.json") and not self._occupato:
            self.b_stato.setText(L("prova in corso", "trial running"))
            self.b_stato.tono("ottone")

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

    def _accendi_serie(self, chiave):
        s = self.grafico.serie.get(chiave)
        if s:
            s["visibile"] = not s["visibile"]
            self.grafico.update()
            self.tessere[chiave].aggiorna(s)

    def _apri_serie(self, chiave):
        s = self.grafico.serie.get(chiave)
        if not s:
            return
        p = self.pannelli_serie.get(chiave)
        if p is None:
            p = Pannello(s["etichetta"], GraficoSingolo(self.grafico, chiave), self)
            p.resize(700, 400)
            self.pannelli_serie[chiave] = p
        p.mostra()

    # ============================================================ panels
    def _apri_pannello(self, nome, titolo, costruisci):
        p = self.pannelli.get(nome)
        if p is None:
            p = Pannello(titolo, costruisci(), self)
            self.pannelli[nome] = p
        p.mostra()

    def _cfg(self):
        """The old-style snapshot of everything (through the helper, once)."""
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
        self.cf = Cursore(3000, 4500, cfg.get("frequency", 3500), "MHz", 50)
        self.cs = Cursore(-50, 0, cfg.get("scale", 0), "", 1,
                          mostra=lambda s: ("%d (−%.0f mV)" % (s, -s * MV_PER_SCALINO)) if s else "0")
        self.ct = Cursore(60, 95, cfg.get("max_temperature", 85), "°C")
        for testo, cur, aiuto in (
                (L("Frequenza", "Clock"), self.cf, L("La frequenza a cui la CPU sale sotto carico. Misurato: oltre 3500 con otto core il guadagno e' zero, perche' comanda il calore.", "The clock the CPU climbs to under load. Measured: above 3500 with eight cores the gain is nil, because heat is in charge.")),
                (L("Undervolt", "Undervolt"), self.cs, L("Scalini di 6,25 mV tolti alla tensione della CPU. Meno tensione, meno calore, stessa frequenza: fino a dove regge.", "Steps of 6.25 mV taken off the CPU voltage. Less voltage, less heat, same clock: as far as it holds.")),
                (L("Limite gradi", "Degree limit"), self.ct, L("Sopra questa temperatura la guardia termica rallenta la CPU di 100 MHz alla volta, e la rialza quando si raffredda.", "Above this temperature the thermal guard slows the CPU by 100 MHz at a time, and raises it again when it cools."))):
            r = QHBoxLayout()
            e = QLabel(testo)
            e.setMinimumWidth(110)
            r.addWidget(e)
            r.addWidget(Aiuto(aiuto, testo))
            r.addWidget(cur, 1)
            v.addLayout(r)
        r = QHBoxLayout()
        for testo, slot, primario in (
                (L("Trova il massimo", "Find my max"), self._cpu_wizard, False),
                (L("Suggerisci UV", "Suggest UV"), self._suggerisci_uv, False),
                ("Test", self._test_cpu, False),
                (L("Applica", "Apply"), self._applica_cpu, True),
                (L("Salva al boot", "Save at boot"), self._salva_cpu, False)):
            b = QPushButton(testo)
            if primario:
                b.setObjectName("primario")
            b.clicked.connect(slot)
            r.addWidget(b)
        v.addLayout(r)
        self.et_cpu = QLabel("")
        self.et_cpu.setObjectName("quieto")
        self.et_cpu.setWordWrap(True)
        v.addWidget(self.et_cpu)
        return w

    def _valori_cpu(self):
        return self.cf.value(), self.cs.value(), self.ct.value()

    def _applica_cpu(self):
        m, s, t = self._valori_cpu()
        r = self.demone.cmd(cmd="apply-cpu", mhz=m, scale=s, temp=t)
        self.demone.cmd(cmd="thermal-guard", limit=t)
        self.et_cpu.setText(L("CPU applicata", "CPU applied") if r.get("ok") else r.get("err", L("non applicata", "not applied")))

    def _salva_cpu(self):
        m, s, t = self._valori_cpu()
        r = self.demone.cmd(cmd="persist-cpu", mhz=m, scale=s, temp=t)
        self.et_cpu.setText(L("CPU salvata: vale anche al prossimo avvio", "CPU saved: applies at next boot too") if r.get("ok") else r.get("err", "?"))

    def _lavoro_cpu(self, fn, testo, poi):
        self.et_cpu.setText(testo)
        in_sfondo(fn, poi, self)

    def _test_cpu(self):
        m, s, t = self._valori_cpu()
        self._lavoro_cpu(lambda: self.demone.cmd(cmd="test-cpu", mhz=m, scale=s, temp=t),
                         L("Test: applico e faccio un minuto di carico…", "Test: applying and loading for a minute…"), self._cpu_fatto)

    def _cpu_fatto(self, r):
        if r.get("ok"):
            b = r.get("bench", {})
            self.et_cpu.setText(L("Regge: %s %s, %s °C. Applicata.", "Holds: %s %s, %s °C. Applied.") % (b.get("score"), b.get("unit"), b.get("temp")))
        else:
            self.et_cpu.setText(r.get("err", L("test fallito", "test failed")))

    def _suggerisci_uv(self):
        m = self.cf.value()
        self._lavoro_cpu(lambda: self.demone.cmd(cmd="suggest-uv", mhz=m),
                         L("Cerco l'undervolt per %d MHz (circa un minuto)…", "Looking for the undervolt at %d MHz (about a minute)…") % m,
                         lambda r: (self.cs.setValue(r.get("suggested_scale", 0)),
                                    self.et_cpu.setText(L("Suggerito: scalino %s. Premi Applica.", "Suggested: step %s. Press Apply.") % r.get("suggested_scale", 0))))

    CPU_WIZ = [(3600, -8), (3700, -16), (3800, -20), (3900, -24), (4000, -36)]

    def _cpu_wizard(self):
        if QMessageBox.question(self, L("Trova il massimo", "Find my max"), L(
                "Prova la CPU a scalini crescenti, 3600 → 4000 MHz con undervolt progressivo, "
                "un minuto di carico per scalino, e si ferma al primo che non regge.\n\n"
                "L'ultimo scalino puo' piantare alcune schede: in quel caso il watchdog riavvia "
                "e al boot torna l'ultimo valore buono. Procedere?",
                "Steps the CPU up, 3600 → 4000 MHz with progressive undervolt, a minute of load "
                "per step, and stops at the first that does not hold.\n\n"
                "The last step can hang some boards: the watchdog then reboots and the last good "
                "value is back at boot. Proceed?")) != QMessageBox.StandardButton.Yes:
            return
        self._wiz = list(self.CPU_WIZ)
        self._wiz_buono = None
        self._wiz_avanti()

    def _wiz_avanti(self):
        if not self._wiz:
            self._wiz_fine()
            return
        f, s = self._wiz.pop(0)
        self._lavoro_cpu(lambda: self.demone.cmd(cmd="test-cpu", mhz=f, scale=s, temp=85),
                         L("Provo %d MHz @ %d…", "Trying %d MHz @ %d…") % (f, s),
                         lambda r, f=f, s=s: self._wiz_passo(f, s, r))

    def _wiz_passo(self, f, s, r):
        if r.get("ok"):
            self._wiz_buono = (f, s)
            self._wiz_avanti()
        else:
            self._wiz_fine((f, s))

    def _wiz_fine(self, caduto=None):
        if not self._wiz_buono:
            self.et_cpu.setText(L("Nemmeno 3600 regge: resta com'era.", "Not even 3600 holds: left as it was."))
            return
        f, s = self._wiz_buono
        self.cf.setValue(f)
        self.cs.setValue(s)
        t = L("Massimo che regge: %d MHz @ %d (gia' applicato).", "Highest that holds: %d MHz @ %d (already applied).") % (f, s)
        if caduto:
            t += " " + L("(%d @ %d non ha retto.)", "(%d @ %d did not hold.)") % caduto
        self.et_cpu.setText(t)

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
        cu = self.demone.cmd(cmd="core-unlock") or {}
        self.core8 = QCheckBox(L("8 core", "8 cores"))
        self.core8.setChecked(bool(cu.get("abilitato")))
        self.core8.setEnabled(bool(cu.get("supportato")))
        self.core8.toggled.connect(self._core8)
        r.addWidget(self.core8)
        r.addWidget(Aiuto(L(
            "Sblocca i due core che la BC-250 tiene spenti: 6c/12t diventa 8c/16t, +20% misurato. "
            "Costa un riavvio in piu' a ogni accensione da spenta, perche' la scheda rilegge "
            "quanti core ha. Vale dal prossimo avvio.",
            "Unlocks the two cores the BC-250 keeps off: 6c/12t becomes 8c/16t, +20% measured. "
            "Costs one extra reboot on every cold start, because the board re-reads how many "
            "cores it has. Takes effect from the next boot."), L("8 core", "8 cores")))
        r.addStretch(1)
        b = QPushButton(L("Applica", "Apply"))
        b.setObjectName("primario")
        b.clicked.connect(self._applica_core)
        r.addWidget(b)
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

    def _applica_core(self):
        r = self.demone.cmd(cmd="cpu-cores-set", cores=[{"core": k, "online": bool(v)} for k, v in self.core_voluti.items()])
        self.toast(L("Core applicati: %d thread", "Cores applied: %d threads") % r.get("nproc", 0) if r.get("ok") else r.get("err", "?"))

    # ---- compute units
    def _pan_cu(self):
        cu = (self.demone.cmd(cmd="cu-get") or {})
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(8)
        self.cu_floor = int(cu.get("floor", 7))
        self.cu_ordine = ["0.0", "0.1", "1.0", "1.1"]
        righe = cu.get("rows") or {k: 7 for k in self.cu_ordine}
        self.cu_righe = {k: int(righe.get(k, 7)) | self.cu_floor for k in self.cu_ordine}
        g = QGridLayout()
        g.setSpacing(6)
        for c in range(5):
            e = QLabel("WGP%d" % c)
            e.setObjectName("didascalia")
            g.addWidget(e, 0, c + 1)
        self.cu_celle = {}
        for r, rk in enumerate(self.cu_ordine):
            e = QLabel("SE%s.SH%s" % (rk[0], rk[2]))
            e.setObjectName("quieto")
            g.addWidget(e, r + 1, 0)
            for wgp in range(5):
                b = QPushButton("")
                b.setCheckable(True)
                b.setFixedSize(40, 26)
                b.setChecked(bool(self.cu_righe[rk] & (1 << wgp)))
                b.setEnabled(not bool(self.cu_floor & (1 << wgp)))
                b.toggled.connect(lambda on, rk=rk, wgp=wgp: self._cu_toggle(rk, wgp, on))
                self.cu_celle[(rk, wgp)] = b
                g.addWidget(b, r + 1, wgp + 1)
        v.addLayout(g)
        self.et_cu = QLabel("")
        self.et_cu.setStyleSheet("color:%s;" % stile.OTTONE)
        v.addWidget(self.et_cu)
        r = QHBoxLayout()
        for testo, m in (("24", 0x07), ("32", 0x0f), ("40", 0x1f)):
            b = QPushButton(testo + " CU")
            b.clicked.connect(lambda _c=False, k=m: self._cu_preset(k))
            r.addWidget(b)
        r.addWidget(Aiuto(L(
            "Ogni casella e' un WGP, cioe' due unita' di calcolo. Le prime tre di ogni riga le "
            "tiene accese il driver. Le altre due per riga sono le sedici che il firmware "
            "lascia spente e che noi accendiamo: misurato, valgono +26% nei giochi.",
            "Each cell is a WGP, that is two compute units. The first three of every row are "
            "kept on by the driver. The other two per row are the sixteen the firmware leaves "
            "off and we turn on: measured, they are worth +26% in games."), "CU"))
        r.addStretch(1)
        b = QPushButton("Test CU")
        b.clicked.connect(self._test_cu)
        r.addWidget(b)
        b = QPushButton(L("Applica", "Apply"))
        b.setObjectName("primario")
        b.clicked.connect(self._applica_cu)
        r.addWidget(b)
        v.addLayout(r)
        self._cu_conta()
        return w

    def _cu_toggle(self, rk, wgp, on):
        m = self.cu_righe.get(rk, 7)
        m = (m | (1 << wgp)) if on else (m & ~(1 << wgp))
        self.cu_righe[rk] = m | self.cu_floor
        self._cu_conta()

    def _cu_conta(self):
        n = sum(bin(self.cu_righe.get(rk, 7) | self.cu_floor).count("1") * 2 for rk in self.cu_ordine)
        self.et_cu.setText(L("CU attive: %d / 40", "Active CUs: %d / 40") % n)

    def _cu_preset(self, m):
        m |= self.cu_floor
        for rk in self.cu_ordine:
            for wgp in range(5):
                b = self.cu_celle.get((rk, wgp))
                if b and b.isEnabled():
                    b.setChecked(bool(m & (1 << wgp)))

    def _applica_cu(self):
        r = self.demone.cmd(cmd="cu-apply", rows=[self.cu_righe.get(rk, 7) | self.cu_floor for rk in self.cu_ordine])
        self.toast(L("CU applicate: %s/40", "CUs applied: %s/40") % r.get("active", "?") if r.get("ok") else r.get("err", "?"), 6)

    def _test_cu(self):
        if QMessageBox.question(self, "Test CU", L(
                "Accende una coppia di CU extra alla volta, la mette sotto sforzo con vkpeak e guarda "
                "se la GPU fa errori. Dura due o tre minuti. Procedere?",
                "Turns on one extra CU pair at a time, loads it with vkpeak and watches for GPU "
                "errors. Takes two or three minutes. Proceed?")) != QMessageBox.StandardButton.Yes:
            return
        self.et_cu.setText(L("Test in corso…", "Testing…"))
        in_sfondo(lambda: self.demone.cmd(cmd="cu-test"), self._cu_testate, self)

    def _cu_testate(self, r):
        self._cu_conta()
        if not r.get("ok"):
            QMessageBox.warning(self, "Test CU", r.get("err", "?"))
            return
        righe = [L("40 CU sotto sforzo: %s GFLOPS", "40 CU under load: %s GFLOPS") % r.get("full40", "?"),
                 L("24 CU: %s GFLOPS", "24 CU: %s GFLOPS") % r.get("baseline", "?"), ""]
        for x in r.get("results", []):
            righe.append("SE%s.SH%s WGP%d: %s%s" % (x["row"][0], x["row"][2], x["wgp"], x["verdict"],
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
            "Quanta memoria il firmware riserva alla GPU. Si scrive nel CMOS e vale dal "
            "prossimo avvio. Il resto e' condiviso lo stesso attraverso il GTT. Con 512 MB "
            "dinamici alcuni giochi misurano la VRAM all'avvio e scelgono texture di "
            "qualita' bassa: se le texture sono sfocate, prova 4 o 6 GB fissi.",
            "How much memory the firmware sets aside for the GPU. Written to the CMOS, in "
            "force from the next boot. The rest is shared anyway through the GTT. With the "
            "512 MB dynamic split some games measure the VRAM at start and pick low texture "
            "quality: if textures look blurry, try 4 or 6 GB fixed."), "VRAM"))
        r.addStretch(1)
        v.addLayout(r)
        self.vram_valori = [2048, 3072, 4096, 6144, 8192, 10240, 12288]
        self.vram = QComboBox()
        for mb in self.vram_valori:
            self.vram.addItem("%d MB (%.0f GB)" % (mb, mb / 1024.0))
        self.vram.setCurrentIndex(self.vram_valori.index(cur) if cur in self.vram_valori else 4)
        v.addWidget(self.vram)
        b = QPushButton(L("Imposta (riavvio)", "Set (reboot)"))
        b.clicked.connect(self._set_vram)
        v.addWidget(b)
        return w

    def _set_vram(self):
        mb = self.vram_valori[self.vram.currentIndex()]
        if QMessageBox.question(self, "VRAM", L("VRAM a %d MB? Serve un riavvio.", "VRAM to %d MB? A reboot is needed.") % mb) != QMessageBox.StandardButton.Yes:
            return
        r = self.demone.cmd(cmd="set-vram", mb=mb)
        self.toast(L("VRAM %d MB: riavvia per applicare", "VRAM %d MB: reboot to apply") % mb if r.get("ok") else L("non scritta", "not written"), 6)

    # ---- advanced governor knobs
    def _pan_avanzate(self):
        c = leggi_json(GOV_CONF, {})
        w = QWidget()
        g = QGridLayout(w)
        g.setContentsMargins(0, 0, 0, 0)
        g.setHorizontalSpacing(10)
        self.av = {}
        voci = (
            ("margine_salita", L("Margine in salita", "Ascent margin"), "mV", 0, 80, L("Millivolt aggiunti alla curva solo mentre si sale. Misurato: 40 toglievano gli errori di calcolo di una scheda sfortunata; 10 e' il valore spedito con la curva a quindici punti.", "Millivolts added to the curve only while climbing. Measured: 40 removed the arithmetic errors of an unlucky board; 10 is the value shipped with the fifteen-point curve.")),
            ("gradino", L("Gradino", "Step"), "MHz", 10, 300, L("Di quanto scende la frequenza a ogni passo quando il carico cala.", "How much the clock drops per step when the load falls.")),
            ("conferme_giu", L("Conferme in discesa", "Descent confirmations"), "", 1, 20, L("Quanti giri di carico basso servono prima di scendere di un gradino. Evita di scendere durante un fotogramma leggero in mezzo a una scena pesante.", "How many low-load ticks before stepping down. Keeps the clock from dropping on a light frame inside a heavy scene.")),
            ("gradi_ok", L("Gradi ok", "Degrees ok"), "°C", 60, 95, L("Sotto questa temperatura il tetto puo' risalire.", "Below this temperature the ceiling may climb back.")),
            ("gradi_max", L("Gradi max", "Degrees max"), "°C", 65, 97, L("Sopra, il tetto scende di 50 MHz per volta.", "Above, the ceiling walks down 50 MHz at a time.")),
            ("gradi_rottura", L("Gradi di rottura", "Degrees of breaking"), "°C", 70, 99, L("Sopra, il tetto crolla di 200 MHz in un colpo.", "Above, the ceiling drops 200 MHz in one go.")),
            ("watt_max", L("Watt max", "Watts max"), "W", 60, 220, L("Il nostro limite di potenza: quello del firmware e' aggirato dal forzare.", "Our own power limit: the firmware's is bypassed by forcing.")),
            ("watt_ok", L("Watt ok", "Watts ok"), "W", 40, 200, L("Sotto, il tetto puo' risalire.", "Below, the ceiling may climb back.")),
        )
        for i, (k, testo, unita, lo, hi, aiuto) in enumerate(voci):
            e = QLabel(testo)
            g.addWidget(e, i, 0)
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
        g.addWidget(Aiuto(L("Alza la tensione quando il sensore la vede cadere sotto il pavimento della curva. Spento di serie: con i quindici punti non serve.", "Raises the voltage when the sensor sees it sag below the curve's floor. Off by default: with the fifteen points it is not needed."), "droop"), len(voci), 2)
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
        e = QLabel(L(
            "Un giro di vkpeak sulla GPU con la curva che sta girando. Non prova la stabilita' "
            "di un gioco: quella la prova Cyberpunk. Serve per vedere i GFLOPS delle CU.",
            "One vkpeak run on the GPU with the curve that is running. It does not prove a game "
            "stable: Cyberpunk does that. It is for seeing the GFLOPS of the CUs."))
        e.setWordWrap(True)
        v.addWidget(e)
        r = QHBoxLayout()
        b = QPushButton("vkpeak")
        b.clicked.connect(self._bench_gpu)
        r.addWidget(b)
        b = QPushButton(L("Carico CPU 60 s", "CPU load 60 s"))
        b.clicked.connect(self._bench_cpu)
        r.addWidget(b)
        b = QPushButton(L("Registro", "Log"))
        b.clicked.connect(self._giornale)
        r.addWidget(b)
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

    def _bench_cpu(self):
        self.et_test.setText(L("carico CPU in corso…", "CPU load running…"))
        in_sfondo(lambda: self.demone.cmd(cmd="bench-cpu", secs=60),
                  lambda r: self.et_test.setText(("%s %s · min %s MHz · %s °C" % (r.get("score"), r.get("unit"), r.get("min_mhz"), r.get("temp"))) if r.get("ok") else r.get("err", "?")), self)

    def _giornale(self):
        rc, out, _ = sh("journalctl -t skillfish-cc-helper -t skillfish-tuner-helper -t skillfish-vf-governor --no-pager -n 60 2>/dev/null", 10)
        QMessageBox.information(self, L("Registro", "Log"), out or L("niente nel registro", "nothing in the log"))

    def disattiva(self):
        super().disattiva()

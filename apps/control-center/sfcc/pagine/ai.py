# -*- coding: utf-8 -*-
"""AI: the local LLM engine (Unsloth Studio on Vulkan), on and off in one click.

Off before gaming: the engine keeps the GPU memory. The models live inside
Unsloth's own interface; here there is the switch, the hardware, and the
shared-memory (GTT) limit, which is a kernel parameter and needs a reboot.
"""
import glob
import os
import subprocess

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (QCheckBox, QHBoxLayout, QLabel, QMessageBox, QPlainTextEdit,
                             QProgressBar, QPushButton, QSlider, QVBoxLayout, QWidget)
from PyQt6.QtCore import Qt

from .. import stile
from ..comune import L, Aiuto, leggi_testo, sh
from ..finestra import PaginaBase
from ..stile import Numerone, Scheda, Stato, griglia_schede, intestazione

UNSLOTH_BIN = "/usr/local/bin/skillfish-unsloth"
UNSLOTH_SVC = "skillfish-unsloth.service"
UNSLOTH_URL = "http://localhost:8888"
UNSLOTH_INSTALLER = "/usr/local/share/skillfish/install-unsloth.sh"


def _int(path):
    try:
        return int(leggi_testo(path))
    except ValueError:
        return None


def _drm():
    for p in sorted(glob.glob("/sys/class/drm/card[0-9]/device")):
        if os.path.exists(os.path.join(p, "mem_info_vram_total")):
            return p
    return None


def gb(n):
    return "?" if n is None else "%.1f GB" % (n / 1e9)


def gtt_richiesto():
    tok = {}
    for pezzo in leggi_testo("/proc/cmdline").split():
        if "=" in pezzo:
            k, v = pezzo.split("=", 1)
            tok[k] = v
    if tok.get("amdgpu.gttsize", "").isdigit():
        return int(tok["amdgpu.gttsize"]), "amdgpu.gttsize"
    if tok.get("ttm.pages_limit", "").isdigit():
        return int(tok["ttm.pages_limit"]) // 256, "ttm.pages_limit"
    return None, None


def ram():
    tot = disp = None
    for line in leggi_testo("/proc/meminfo").splitlines():
        if line.startswith("MemTotal"):
            tot = int(line.split()[1]) * 1024
        elif line.startswith("MemAvailable"):
            disp = int(line.split()[1]) * 1024
    return tot, disp


class Installatore(QThread):
    riga = pyqtSignal(str)
    fine = pyqtSignal(int)

    def run(self):
        try:
            p = subprocess.Popen("pkexec sh -c 'UNSLOTH_FORCE_VULKAN=1 bash %s'" % UNSLOTH_INSTALLER, shell=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            for ln in iter(p.stdout.readline, ""):
                if ln:
                    self.riga.emit(ln.rstrip())
            p.wait(3600)
            self.fine.emit(p.returncode)
        except Exception as e:
            self.riga.emit(str(e))
            self.fine.emit(1)


class Pagina(PaginaBase):
    def __init__(self, finestra):
        super().__init__(finestra)
        self.intervallo_ms = 5000
        self.occupato = False
        self._inst = None

    def costruisci(self):
        v = self.corpo_scorrevole()
        v.addWidget(intestazione("AI", L(
            "Un modello linguistico che gira qui, sulla GPU integrata, circa cinque volte piu' veloce "
            "che sul processore. Domande e risposte restano su questa macchina.",
            "A language model that runs here, on the integrated GPU, about five times faster than on "
            "the processor. Questions and answers stay on this machine.")))
        self.c_motore = Scheda(L("Motore", "Engine"), L(
            "Unsloth Studio con llama.cpp su Vulkan. Acceso tiene la memoria della GPU: spegnilo prima "
            "di giocare. Al primo accesso ti chiede di scegliere una password; i modelli si scaricano "
            "dalla sua interfaccia.",
            "Unsloth Studio with llama.cpp on Vulkan. While on it holds GPU memory: turn it off before "
            "gaming. On first sign-in it asks you to choose a password; models are downloaded from its "
            "own interface."))
        self.b_stato = Stato("", "quieto")
        self.c_motore.testa.insertWidget(self.c_motore.testa.count() - 1, self.b_stato)
        self.acceso = QCheckBox(L("Acceso", "On"))
        self.acceso.clicked.connect(self._accendi)
        self.c_motore.aggiungi(self.acceso)
        self.r_api = self.c_motore.riga("API", UNSLOTH_URL + "/v1")
        self.c_motore.bottoni((L("Apri la chat", "Open the chat"), lambda: sh("xdg-open %s &" % UNSLOTH_URL, 5), True),
                              (L("Installa", "Install"), self._installa, False))

        self.c_hw = Scheda("Hardware")
        self.r_gpu = self.c_hw.riga("GPU")
        self.r_cpu = self.c_hw.riga("CPU")
        self.r_vram = self.c_hw.riga("VRAM")
        self.r_ram = self.c_hw.riga("RAM")
        self.r_budget = self.c_hw.riga(L("Budget del modello", "Model budget"))

        self.c_gtt = Scheda(L("Memoria condivisa (GTT)", "Shared memory (GTT)"), L(
            "Sulla BC-250 la memoria e' condivisa fra GPU e CPU: questo alza la quota di RAM che il "
            "modello puo' usare oltre alla VRAM, cosi' entrano modelli piu' grandi. E' un parametro del "
            "kernel: serve un riavvio.",
            "On the BC-250 memory is shared between GPU and CPU: this raises the share of RAM the model "
            "may use on top of VRAM, so larger models fit. It is a kernel parameter: a reboot is needed."))
        self.n_gtt = Numerone("GTT", "GB")
        self.c_gtt.aggiungi(self.n_gtt)
        r = QHBoxLayout()
        self.gtt = QSlider(Qt.Orientation.Horizontal)
        self.gtt.setRange(2, 14)
        self.gtt_et = QLabel("— GB")
        self.gtt_et.setMinimumWidth(56)
        self.gtt.valueChanged.connect(lambda x: self.gtt_et.setText("%d GB" % x))
        r.addWidget(self.gtt, 1)
        r.addWidget(self.gtt_et)
        self.c_gtt.aggiungi(r)
        self.r_gtt_leva = self.c_gtt.riga(L("Richiesto", "Requested"))
        self.c_gtt.bottoni((L("Applica e riavvia", "Apply and reboot"), self._gtt, True))
        v.addWidget(griglia_schede(self.c_motore, self.c_hw, self.c_gtt, colonne=3))

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(220)
        self.log.hide()
        v.addWidget(self.log)
        v.addStretch(1)
        self._hw()

    def _hw(self):
        rc, out, _ = sh("lspci -nn 2>/dev/null | grep -E 'VGA|3D|Display' | head -1", 8)
        gpu = out.split(":", 2)[-1].strip() if out else "?"
        if "]" in gpu:
            gpu = gpu.split("]", 1)[1].strip()          # drop the vendor prefix
        self.r_gpu.setText(gpu[:44])
        for line in leggi_testo("/proc/cpuinfo").splitlines():
            if line.startswith("model name"):
                self.r_cpu.setText(line.split(":", 1)[1].strip()[:40])
                break
        d = _drm()
        vt = _int(os.path.join(d, "mem_info_vram_total")) if d else None
        vu = _int(os.path.join(d, "mem_info_vram_used")) if d else None
        gt = _int(os.path.join(d, "mem_info_gtt_total")) if d else None
        self.r_vram.setText("%s %s / %s" % (gb((vt or 0) - (vu or 0)), L("libera", "free"), gb(vt)) if vt else L("n/d", "n/a"))
        rt, ra = ram()
        self.r_ram.setText("%s %s / %s" % (gb(ra), L("libera", "free"), gb(rt)))
        self.r_budget.setText(gb((vt or 0) + (gt or 0)) if (vt and gt) else "—")
        cur, leva = gtt_richiesto()
        ram_gb = int(rt / 1e9) if rt else 14
        self.gtt.setMaximum(max(4, min(60, ram_gb - 1)))
        self.n_gtt.imposta("%.1f" % (gt / 1e9) if gt else None)
        if cur is not None:
            self.gtt.blockSignals(True)
            self.gtt.setValue(max(2, min(self.gtt.maximum(), round(cur / 1024))))
            self.gtt.blockSignals(False)
            self.gtt_et.setText("%d GB" % self.gtt.value())
            self.r_gtt_leva.setText("%d MB (%s)" % (cur, leva))
        else:
            self.gtt.setEnabled(False)
            self.r_gtt_leva.setText(L("non impostato", "not set"))

    def aggiorna(self):
        if self.occupato:
            return
        inst = os.path.exists(UNSLOTH_BIN)
        rc, out, _ = sh("systemctl is-active %s" % UNSLOTH_SVC, 8)
        on = out == "active"
        self.acceso.blockSignals(True)
        self.acceso.setChecked(on)
        self.acceso.setEnabled(inst)
        self.acceso.blockSignals(False)
        if not inst:
            self.b_stato.setText(L("non installato", "not installed"))
            self.b_stato.tono("quieto")
        else:
            self.b_stato.setText(L("acceso", "on") if on else L("spento: GPU libera per i giochi", "off: GPU free for games"))
            self.b_stato.tono("bene" if on else "quieto")

    def _accendi(self, on):
        self.occupato = True
        r = self.demone.cmd(cmd="servizio", azione="start" if on else "stop", unit=UNSLOTH_SVC)
        self.occupato = False
        if not r.get("ok"):
            self.toast(r.get("err") or L("non riuscito", "failed"))
        self.aggiorna()

    def _installa(self):
        if os.path.exists(UNSLOTH_BIN):
            if QMessageBox.question(self, "AI", L("Il motore e' gia' installato. Rilanciare l'installazione per aggiornarlo?", "The engine is already installed. Run the installer again to update it?")) != QMessageBox.StandardButton.Yes:
                return
        if self._inst is not None:
            return
        self.log.clear()
        self.log.show()
        self.log.appendPlainText(L("Scarico e configuro Unsloth Studio (circa 2 GB)…", "Downloading and setting up Unsloth Studio (about 2 GB)…"))
        self._inst = Installatore(self)
        self._inst.riga.connect(self.log.appendPlainText)
        self._inst.fine.connect(self._installato)
        self._inst.start()

    def _installato(self, rc):
        self._inst = None
        self.log.appendPlainText(L("Fatto.", "Done.") if rc == 0 else L("Non riuscito (uscita %d).", "Failed (exit %d).") % rc)
        self.aggiorna()

    def _gtt(self):
        mb = self.gtt.value() * 1024
        if QMessageBox.question(self, "GTT", L("Imposto %d GB e riavvio?", "Set %d GB and reboot?") % self.gtt.value()) != QMessageBox.StandardButton.Yes:
            return
        r = self.demone.cmd(cmd="gtt", mb=mb)
        if r.get("ok"):
            self.demone.cmd(cmd="riavvia")
        else:
            self.toast(r.get("out") or r.get("err") or "?")

# -*- coding: utf-8 -*-
"""Status: what the machine is doing right now, on one screen, nothing to set.

Four cards with one big number each (GPU, CPU, compute units, fan), then the
system card (kernel, governor, Mesa, scheduler) and the card that says whether
the last boot was clean. Everything here is read from files anyone can read:
opening this page never asks for a password.
"""
import os
import re
import subprocess

from PyQt6.QtWidgets import QLabel, QMessageBox

from .. import stile
from ..comune import (CU_STATO, FREEZE_FLAG, FREEZE_LOG, GOV_CONF, L, VENTOLA_STATO, battito,
                      hwmon_valore, leggi_json, leggi_testo, sh, versione_pacchetto)
from ..demone import in_sfondo
from ..finestra import PaginaBase
from ..stile import Numerone, Scheda, Stato, griglia_schede, intestazione


def cpu_media_mhz():
    fs = [float(x) for x in re.findall(r'cpu MHz\s*:\s*([\d.]+)', leggi_testo("/proc/cpuinfo"))]
    return (sum(fs) / len(fs), len(fs)) if fs else (None, 0)


def os_release():
    d = {}
    for riga in leggi_testo("/etc/os-release").splitlines():
        if "=" in riga:
            k, v = riga.split("=", 1)
            d[k] = v.strip().strip('"')
    return d


class Pagina(PaginaBase):
    def __init__(self, finestra):
        super().__init__(finestra)
        self.intervallo_ms = 1500
        self._mesa_sistema = None
        self._mesa_giochi = None

    def costruisci(self):
        v = self.corpo_scorrevole()
        v.addWidget(intestazione(L("Stato", "Status"), L(
            "Cosa sta facendo la macchina adesso. Qui non si imposta niente: si guarda.",
            "What the machine is doing right now. Nothing is set here: you look.")))

        # --- the four numbers
        self.c_gpu = Scheda("GPU", L("Frequenza forzata dal governor e tetto: sotto carico sale al tetto, che scende se la scheda scalda o tira troppo.",
            "Clock forced by the governor and its ceiling: under load it jumps to the ceiling, which drops when the board gets hot or draws too much."))
        self.n_gpu = Numerone(L("Frequenza", "Clock"), "MHz")
        self.c_gpu.aggiungi(self.n_gpu)
        self.r_tetto = self.c_gpu.riga(L("Tetto", "Ceiling"))
        self.r_gpu_mv = self.c_gpu.riga(L("Tensione", "Voltage"))
        self.r_gpu_c = self.c_gpu.riga(L("Temperatura", "Temperature"))
        self.r_gpu_w = self.c_gpu.riga("Watt")
        self.r_gpu_carico = self.c_gpu.riga(L("Carico", "Load"))
        self.b_gov = Stato("", "quieto")
        self.c_gpu.testa.insertWidget(self.c_gpu.testa.count() - 1, self.b_gov)

        self.c_cpu = Scheda("CPU")
        self.n_cpu = Numerone(L("Frequenza media", "Average clock"), "MHz")
        self.c_cpu.aggiungi(self.n_cpu)
        self.r_cpu_thread = self.c_cpu.riga("Thread")
        self.r_cpu_c = self.c_cpu.riga(L("Temperatura", "Temperature"))
        self.r_cpu_oc = self.c_cpu.riga(L("Impostata", "Set to"))

        self.c_cu = Scheda(L("Unita' di calcolo", "Compute units"), L("24 unita' attive di serie: le altre 16 le accendiamo noi all'avvio.",
            "24 units on by default: we turn the other 16 on at boot."))
        self.n_cu = Numerone("CU", "/ 40")
        self.c_cu.aggiungi(self.n_cu)
        self.r_cu_boot = self.c_cu.riga(L("All'avvio", "At boot"))
        self.r_cu_righe = self.c_cu.riga(L("Maschere", "Masks"))

        self.c_ventola = Scheda(L("Ventola", "Fan"))
        self.n_ventola = Numerone(L("Giri", "Speed"), "rpm")
        self.c_ventola.aggiungi(self.n_ventola)
        self.r_duty = self.c_ventola.riga("PWM")
        self.r_ventola_chi = self.c_ventola.riga(L("Comanda", "In charge"))
        self.r_ventola_t = self.c_ventola.riga(L("Sorgente", "Source"))
        v.addWidget(griglia_schede(self.c_gpu, self.c_cpu, self.c_cu, self.c_ventola, colonne=4))

        # --- the system
        self.c_sys = Scheda(L("Sistema", "System"))
        self.r_versione = self.c_sys.riga("SkillFishOS")
        self.r_kernel = self.c_sys.riga("Kernel")
        self.r_governor = self.c_sys.riga("Governor")
        self.r_mesa_sys = self.c_sys.riga(L("Driver Vulkan di sistema", "System Vulkan driver"))
        self.r_mesa_giochi = self.c_sys.riga(L("Driver nei giochi", "Driver in games"))
        self.r_scx = self.c_sys.riga(L("Schedulatore", "Scheduler"))
        self.r_cc = self.c_sys.riga("Control Center")

        self.c_boot = Scheda(L("Ultimo avvio", "Last boot"), L("Se manca il segno dello spegnimento in ordine, l'ultima volta e' andato giu' da solo: con l'overclock e' il sintomo che conta.",
            "If the orderly-shutdown mark is missing, the last time it went down on its own: with an overclock that is the symptom that counts."))
        self.e_boot = QLabel("")
        self.e_boot.setWordWrap(True)
        self.c_boot.aggiungi(self.e_boot)
        self.r_boot_n = self.c_boot.riga(L("Cadute registrate", "Recorded crashes"))
        self.r_boot_ultima = self.c_boot.riga(L("Ultima", "Last"))
        self.c_boot.bottoni((L("Vai al Tuner", "Open the Tuner"), lambda: self.finestra.mostra("tuner"), False))

        self.c_azioni = Scheda(L("Azioni", "Actions"))
        self.c_azioni.aggiungi(QLabel(L("Le altre finestre di SkillFishOS e lo spegnimento.",
                                        "The other SkillFishOS windows, and power.")))
        self.c_azioni.bottoni((L("Hub", "Hub"), lambda: self._lancia("skillfish-hub"), False),
                              (L("Remote Manager", "Remote Manager"),
                               lambda: self._lancia("skillfish-remote-manager"), False))
        self.c_azioni.bottoni((L("HUD", "HUD"), lambda: self._lancia("skillfish-hud-editor"), False),
                              (L("Terminale", "Terminal"), lambda: self._lancia("konsole"), False))
        self.c_azioni.bottoni((L("Riavvia", "Reboot"), lambda: self._spegni("riavvia"), False),
                              (L("Spegni", "Shut down"), lambda: self._spegni("spegni"), False))
        v.addWidget(griglia_schede(self.c_sys, self.c_boot, self.c_azioni, colonne=3))
        v.addStretch(1)
        self._statico()
        in_sfondo(self._leggi_mesa, self._mesa_letta, self)

    # ---- readings ------------------------------------------------------------
    def _statico(self):
        osr = os_release()
        self.r_versione.setText(("%s %s" % (osr.get("VERSION", ""), osr.get("VERSION_CODENAME", ""))).strip() or osr.get("PRETTY_NAME", "?"))
        k = os.uname().release
        self.r_kernel.setText(k)
        self.r_kernel.setStyleSheet("font-weight:600;color:%s;" % (stile.VERDE if "skillfishos" in k else stile.ARANCIO))
        self.r_governor.setText(("skillfish-vf-governor %s" % versione_pacchetto("skillfish-vf-governor")).strip())
        self.r_cc.setText(versione_pacchetto("skillfish-control-center") or "?")
        rc, out, _ = sh("systemctl is-enabled skillfish-cu.service 2>/dev/null", 5)
        self.r_cu_boot.setText(L("40 CU (sblocco attivo)", "40 CU (unlock on)") if out == "enabled" else L("come da firmware", "as the firmware leaves them"))
        rc, out, _ = sh("systemctl is-enabled skillfish-scx.path 2>/dev/null", 5)
        self.r_scx.setText(L("bpfland nei giochi", "bpfland while gaming") if out == "enabled" else L("di serie (EEVDF)", "stock (EEVDF)"))
        # last boot
        caduto = os.path.exists(FREEZE_FLAG)
        righe = [r for r in leggi_testo(FREEZE_LOG).splitlines() if r.strip()]
        self.r_boot_n.setText(str(len(righe)))
        self.r_boot_ultima.setText(righe[-1].split(" ")[0].replace("T", " ")[:16] if righe else "—")
        if caduto:
            self.e_boot.setText(L("Questo avvio segue uno spegnimento non pulito.",
                                  "This boot follows an unclean shutdown."))
            self.e_boot.setObjectName("male")
        else:
            self.e_boot.setText(L("Spegnimento precedente in ordine.", "Previous shutdown was orderly."))
            self.e_boot.setObjectName("bene")
        self.e_boot.setStyleSheet("")
        self.e_boot.style().polish(self.e_boot)

    def _leggi_mesa(self):
        out = {"sistema": "?", "giochi": "?"}
        try:
            r = subprocess.run("timeout 10 vulkaninfo --summary 2>/dev/null | grep -m1 driverInfo",
                               shell=True, capture_output=True, text=True, timeout=15)
            m = re.search(r"driverInfo\s*=\s*(.+)", r.stdout)
            if m:
                info = m.group(1).strip()
                out["sistema"] = (L("nostra", "ours") + " (%s)" % info) if "git-" in info else info
        except (OSError, subprocess.SubprocessError):
            # vulkaninfo missing or timed out: leave the "?" placeholder set above
            out["sistema"] = "?"
        try:
            r = subprocess.run(["/usr/bin/skillfish-mesa", "stato"], capture_output=True, text=True, timeout=10)
            nomi = {"com.valvesoftware.Steam": "Steam", "com.heroicgameslauncher.hgl": "Heroic"}
            nostro = [nomi.get(ln.split()[0], ln.split()[0]) for ln in r.stdout.splitlines() if "NOSTRO" in ln]
            out["giochi"] = (L("nostra in %s", "ours in %s") % ", ".join(nostro)) if nostro else L("di serie", "stock")
        except Exception:
            out["giochi"] = L("di serie", "stock")
        return out

    def _mesa_letta(self, d):
        self.r_mesa_sys.setText(d.get("sistema", "?"))
        self.r_mesa_giochi.setText(d.get("giochi", "?"))

    def aggiorna(self):
        b = battito()
        if b:
            self.n_gpu.imposta(b["mhz"])
            self.r_tetto.setText("%d MHz" % b["tetto"])
            self.r_gpu_c.setText("%d °C" % b["gradi"])
            self.r_gpu_w.setText("%d W" % b["watt"])
            self.r_gpu_carico.setText("%d %%" % b["carico"])
            import time
            vivo = time.time() - b["quando"] < 5
            self.b_gov.setText(L("governor attivo", "governor running") if vivo else L("governor fermo", "governor stopped"))
            self.b_gov.tono("bene" if vivo else "male")
        else:
            mhz = hwmon_valore("amdgpu", "freq1_input")
            self.n_gpu.imposta(mhz // 1000000 if mhz else None)
            t = hwmon_valore("amdgpu", "temp1_input")
            self.r_gpu_c.setText("%d °C" % (t // 1000) if t else "—")
            w = hwmon_valore("amdgpu", "power1_average") or hwmon_valore("amdgpu", "power1_input")
            self.r_gpu_w.setText("%.0f W" % (w / 1e6) if w else "—")
            self.b_gov.setText(L("governor assente", "no governor"))
            self.b_gov.tono("quieto")
            conf = leggi_json(GOV_CONF, {})
            self.r_tetto.setText("%s MHz" % conf.get("freq_max", "—"))
        mv = hwmon_valore("amdgpu", "in0_input")
        self.r_gpu_mv.setText("%d mV" % mv if mv else "—")

        media, n = cpu_media_mhz()
        self.n_cpu.imposta(int(media) if media else None)
        self.r_cpu_thread.setText("%d %s" % (n, L("attivi", "online")))
        t = hwmon_valore("k10temp", "temp1_input")
        self.r_cpu_c.setText("%.0f °C" % (t / 1000.0) if t else "—")
        m = re.search(r"frequency\s*=\s*(\d+)", leggi_testo("/etc/bc250-smu-oc.conf"))
        self.r_cpu_oc.setText("%s MHz" % m.group(1) if m else "—")

        cu = leggi_json(CU_STATO, {})
        self.n_cu.imposta(cu.get("active_cu") if cu else None)
        righe = cu.get("rows") or {}
        self.r_cu_righe.setText(" ".join("%x" % righe[k] for k in sorted(righe)) if righe else "—")

        s = leggi_json(VENTOLA_STATO, {})
        if s:
            giri = next((x.get("value") for x in s.get("sensori", []) if x.get("type") == "fan" and x.get("value")), None)
            self.n_ventola.imposta(int(giri) if giri else None)
            self.r_duty.setText("%.0f %%" % float(s.get("duty") or 0))
            self.r_ventola_chi.setText(L("la curva", "the curve") if s.get("in_controllo") else L("il firmware", "the firmware"))
            t = s.get("temperatura")
            self.r_ventola_t.setText("%.1f °C" % t if t is not None else "—")
        else:
            rpm = hwmon_valore("nct6686", "fan2_input")
            self.n_ventola.imposta(rpm)
            self.r_ventola_chi.setText(L("controllo non attivo", "controller not running"))

    # ---- actions ---------------------------------------------------------------
    def _lancia(self, cmd):
        try:
            subprocess.Popen([cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            self.toast(L("%s non e' installato", "%s is not installed") % cmd)

    def _spegni(self, cosa):
        titolo = L("Riavviare?", "Reboot?") if cosa == "riavvia" else L("Spegnere?", "Shut down?")
        if QMessageBox.question(self, titolo, L("Chiudi prima quello che stai facendo.",
                                                "Close what you are doing first.")) != QMessageBox.StandardButton.Yes:
            return
        r = self.demone.cmd(cmd=cosa)
        if not r.get("ok"):
            self.toast(r.get("err", "?"))

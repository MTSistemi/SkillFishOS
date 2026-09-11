# -*- coding: utf-8 -*-
"""Games: our Mesa, the scheduler, Proton, FSR 4.

Everything a game runs through, in one place. Our Mesa is switched per launcher
(a flatpak override) or for the whole system (a divert of the 64-bit driver);
the scheduler is armed through GameMode; Proton versions are fetched from
GitHub and installed into Steam and Heroic, the way ProtonUp-Qt would if it
started on this board.
"""
import configparser
import importlib.machinery
import importlib.util
import json
import os
import re
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (QCheckBox, QComboBox, QHBoxLayout, QLabel, QListWidget,
                             QListWidgetItem, QMessageBox, QProgressBar, QPushButton, QVBoxLayout,
                             QWidget)

from .. import stile
from ..comune import L, Aiuto, sh
from ..demone import in_sfondo
from ..finestra import PaginaBase
from ..stile import Scheda, Stato, griglia_schede, intestazione

MESA_CLI = "/usr/bin/skillfish-mesa"
STEAM_APP = "com.valvesoftware.Steam"
HEROIC_APP = "com.heroicgameslauncher.hgl"
CASA = os.path.expanduser("~")
STEAM_TOOLS = os.path.join(CASA, ".var/app/%s/data/Steam/compatibilitytools.d" % STEAM_APP)
STEAM_CONFIG = os.path.join(CASA, ".var/app/%s/data/Steam/config/config.vdf" % STEAM_APP)
HEROIC_TOOLS = os.path.join(CASA, ".var/app/%s/config/heroic/tools/proton" % HEROIC_APP)
HEROIC_CONFIG = os.path.join(CASA, ".var/app/%s/config/heroic/config.json" % HEROIC_APP)
OVERRIDES = os.path.join(CASA, ".local/share/flatpak/overrides")
GE_API = "https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases?per_page=15"
FSR4_ENV = ("PROTON_USE_OPTISCALER", "PROTON_FSR4_UPGRADE")


def _mesa_modulo():
    """The switch script, loaded as a module (it has no .py extension)."""
    if not os.path.exists(MESA_CLI):
        return None
    try:
        loader = importlib.machinery.SourceFileLoader("skillfish_mesa", MESA_CLI)
        spec = importlib.util.spec_from_loader("skillfish_mesa", loader)
        m = importlib.util.module_from_spec(spec)
        loader.exec_module(m)
        return m
    except Exception:
        return None


def _override(app):
    c = configparser.RawConfigParser()
    c.optionxform = str
    c.read(os.path.join(OVERRIDES, app))
    for s in ("Context", "Environment"):
        if not c.has_section(s):
            c.add_section(s)
    return c


def _scrivi_override(app, c):
    os.makedirs(OVERRIDES, exist_ok=True)
    with open(os.path.join(OVERRIDES, app), "w", encoding="utf-8", newline="\n") as fh:
        c.write(fh, space_around_delimiters=False)


def _mesa_stato(app):
    m = _mesa_modulo()
    if m is None:
        return None
    c = _override(app)
    icd = c.get("Environment", "VK_DRIVER_FILES", fallback=None)
    unset = c.get("Context", "unset-environment", fallback="")
    return icd == m.ICD and "VK_DRIVER_FILES" not in unset


def _fsr4_stato(app):
    c = _override(app)
    return all(c.get("Environment", k, fallback="") == "1" for k in FSR4_ENV)


def _fsr4_set(app, on):
    c = _override(app)
    v = c.get("Context", "unset-environment", fallback="")
    resto = [x for x in v.split(";") if x and x not in FSR4_ENV]
    if resto:
        c.set("Context", "unset-environment", ";".join(resto) + ";")
    elif c.has_option("Context", "unset-environment"):
        c.remove_option("Context", "unset-environment")
    for k in FSR4_ENV:
        if on:
            c.set("Environment", k, "1")
        elif c.has_option("Environment", k):
            c.remove_option("Environment", k)
    _scrivi_override(app, c)


def proton_installati():
    out = {}
    for nome, cartella in (("steam", STEAM_TOOLS), ("heroic", HEROIC_TOOLS)):
        try:
            out[nome] = sorted(d for d in os.listdir(cartella) if os.path.isdir(os.path.join(cartella, d)))
        except OSError:
            out[nome] = []
    return out


def heroic_default():
    try:
        with open(HEROIC_CONFIG) as f:
            d = json.load(f)
        return (d.get("defaultSettings", {}).get("wineVersion") or {}).get("name", "")
    except Exception:
        return ""


def steam_default():
    try:
        with open(STEAM_CONFIG, encoding="utf-8", errors="replace") as f:
            t = f.read()
        m = re.search(r'"CompatToolMapping"\s*\{(.*?)\n\t{4}\}', t, re.S)
        if m:
            z = re.search(r'"0"\s*\{[^}]*?"name"\s*"([^"]*)"', m.group(1), re.S)
            if z:
                return z.group(1)
    except Exception:
        pass
    return ""


def steam_aperto():
    rc, out, _ = sh("flatpak ps --columns=application 2>/dev/null", 10)
    return STEAM_APP in out


class Scarica(QThread):
    """Download a GE-Proton tarball and unpack it into the chosen folders."""
    avanzamento = pyqtSignal(int, str)
    finito = pyqtSignal(bool, str)

    def __init__(self, url, nome, cartelle, parent=None):
        super().__init__(parent)
        self.url, self.nome, self.cartelle = url, nome, cartelle

    def run(self):
        tmp = None
        try:
            tmp = tempfile.NamedTemporaryFile(prefix="ge-proton-", suffix=".tar.gz", delete=False)
            req = urllib.request.Request(self.url, headers={"User-Agent": "SkillFishOS-Control-Center"})
            with urllib.request.urlopen(req, timeout=60) as r:
                tot = int(r.headers.get("Content-Length") or 0)
                letti = 0
                while True:
                    b = r.read(1 << 20)
                    if not b:
                        break
                    tmp.write(b)
                    letti += len(b)
                    self.avanzamento.emit(int(letti * 100 / tot) if tot else 0, "%d MB" % (letti >> 20))
            tmp.close()
            for cartella in self.cartelle:
                os.makedirs(cartella, exist_ok=True)
                self.avanzamento.emit(100, L("estraggo in %s", "unpacking into %s") % cartella)
                with tarfile.open(tmp.name, "r:gz") as tf:
                    # refuse anything that would land outside the folder
                    for m in tf.getmembers():
                        if m.name.startswith("/") or ".." in m.name.split("/"):
                            raise ValueError("archivio sospetto: %s" % m.name)
                    tf.extractall(cartella)
            self.finito.emit(True, self.nome)
        except Exception as e:
            self.finito.emit(False, str(e))
        finally:
            if tmp is not None:
                try:
                    os.unlink(tmp.name)
                except OSError:
                    pass


class Pagina(PaginaBase):
    def __init__(self, finestra):
        super().__init__(finestra)
        self.intervallo_ms = 5000
        self.versioni = []
        self._scarica = None

    def costruisci(self):
        v = self.corpo_scorrevole()
        v.addWidget(intestazione(L("Giochi", "Games"), L(
            "Il driver, lo schedulatore e Proton: quello che un gioco attraversa prima di arrivare "
            "allo schermo.", "The driver, the scheduler and Proton: what a game goes through on its "
            "way to the screen.")))

        # --- Mesa
        self.c_mesa = Scheda(L("Driver Vulkan", "Vulkan driver"), L(
            "La nostra Mesa apre le code compute che il driver di serie tiene chiuse su questa GPU: "
            "+4% in Cyberpunk, e +12% con FSR 4 acceso. Si accende per lanciatore, con un override "
            "flatpak, o per tutto il sistema.\n\n"
            "SERVE IL NOSTRO KERNEL. Su un kernel senza le due patch delle code compute quelle code "
            "piantano la GPU, e sulla BC-250 un aggancio si risolve staccando la corrente. Il modo "
            "«sistema» si rifiuta di partire su un altro kernel; quello per lanciatore no, sta a te.",
            "Our Mesa opens the compute queues the stock driver keeps closed on this GPU: +4% in "
            "Cyberpunk, and +12% with FSR 4 on. It is switched per launcher, through a flatpak "
            "override, or for the whole system.\n\n"
            "IT NEEDS OUR KERNEL. On a kernel without the two compute-queue patches those queues "
            "wedge the GPU, and on the BC-250 a wedge is fixed by pulling the plug. The «system» "
            "mode refuses to start on another kernel; the per-launcher one does not, that is on you."))
        self.b_mesa = Stato("", "quieto")
        self.c_mesa.testa.insertWidget(self.c_mesa.testa.count() - 1, self.b_mesa)
        self.m_steam = QCheckBox("Steam")
        self.m_heroic = QCheckBox("Heroic")
        self.m_sistema = QCheckBox(L("Tutto il sistema", "Whole system"))
        for cb in (self.m_steam, self.m_heroic):
            cb.clicked.connect(self._mesa_lanciatore)
        self.m_sistema.clicked.connect(self._mesa_sistema)
        self.c_mesa.aggiungi(self.m_steam)
        self.c_mesa.aggiungi(self.m_heroic)
        self.c_mesa.aggiungi(self.m_sistema)
        self.r_mesa_ver = self.c_mesa.riga(L("Pacchetto", "Package"))
        self.r_mesa_kernel = self.c_mesa.riga("Kernel")
        self.e_mesa = QLabel("")
        self.e_mesa.setObjectName("quieto")
        self.e_mesa.setWordWrap(True)
        self.c_mesa.aggiungi(self.e_mesa)

        # --- scheduler
        self.c_scx = Scheda(L("Schedulatore", "Scheduler"), L(
            "scx_bpfland, lo schedulatore di CachyOS, caricato SOLO mentre gira un gioco: lo alza "
            "GameMode all'avvio e lo toglie alla chiusura. Misurato: +1,5-2% in Cyberpunk e "
            "fotogrammi piu' regolari. Se il kernel lo espelle due volte (la malattia di lavd su "
            "questa scheda) il servizio si rifiuta di partire finche' non azzeri il contatore.",
            "scx_bpfland, the CachyOS scheduler, loaded ONLY while a game runs: GameMode raises it "
            "at launch and drops it at exit. Measured: +1.5-2% in Cyberpunk and steadier frames. If "
            "the kernel ejects it twice (lavd's disease on this board) the service refuses to start "
            "until you reset the counter."))
        self.b_scx = Stato("", "quieto")
        self.c_scx.testa.insertWidget(self.c_scx.testa.count() - 1, self.b_scx)
        self.s_armato = QCheckBox(L("Nei giochi", "While gaming"))
        self.s_armato.clicked.connect(self._scx_set)
        self.c_scx.aggiungi(self.s_armato)
        self.r_scx_nome = self.c_scx.riga(L("Adesso", "Now"))
        self.r_scx_esp = self.c_scx.riga(L("Espulsioni", "Ejections"))
        self.c_scx.bottoni((L("Azzera contatore", "Reset counter"), self._scx_azzera, False))

        # --- FSR 4
        self.c_fsr = Scheda("FSR 4", L(
            "FSR 4 gira sulla BC-250 attraverso OptiScaler, sul percorso DLSS del gioco: GE-Proton "
            "11 scarica OptiScaler da solo quando trova PROTON_USE_OPTISCALER=1, e il gioco va "
            "messo su DLSS. Serve anche la libreria FSR 4 di AMD (amdxcffx64.dll), che non "
            "possiamo distribuire: la trovi nel driver Windows di AMD, e va copiata accanto al "
            "gioco. Con la nostra Mesa vale +12%.",
            "FSR 4 runs on the BC-250 through OptiScaler, on the game's DLSS path: GE-Proton 11 "
            "downloads OptiScaler by itself when it finds PROTON_USE_OPTISCALER=1, and the game "
            "must be set to DLSS. AMD's FSR 4 library (amdxcffx64.dll) is needed too and we cannot "
            "ship it: it is in AMD's Windows driver, and goes next to the game. With our Mesa it is "
            "worth +12%."))
        self.f_steam = QCheckBox("Steam")
        self.f_heroic = QCheckBox("Heroic")
        for cb in (self.f_steam, self.f_heroic):
            cb.clicked.connect(self._fsr4)
        self.c_fsr.aggiungi(self.f_steam)
        self.c_fsr.aggiungi(self.f_heroic)
        self.c_fsr.bottoni((L("Guida", "Guide"), lambda: sh("xdg-open https://github.com/MTSistemi/SkillFishOS/wiki &", 5), False))
        v.addWidget(griglia_schede(self.c_mesa, self.c_scx, self.c_fsr, colonne=3))

        # --- Proton
        self.c_proton = Scheda("Proton", L(
            "Le versioni GE-Proton 11 pubblicate da GloriousEggroll. «Installa» le scarica (circa "
            "500 MB) e le mette nelle cartelle di Steam e di Heroic; «Predefinita» le sceglie come "
            "default. Per Steam serve che Steam sia chiuso: il file di configurazione lo riscrive "
            "lui all'uscita.",
            "The GE-Proton 11 versions published by GloriousEggroll. «Install» downloads them "
            "(about 500 MB) and puts them in the Steam and Heroic folders; «Default» picks one as "
            "the default. For Steam, Steam must be closed: it rewrites its configuration on exit."))
        self.lista = QListWidget()
        self.lista.setMinimumHeight(200)
        self.c_proton.aggiungi(self.lista, 1)
        r = QHBoxLayout()
        self.p_steam = QCheckBox("Steam")
        self.p_steam.setChecked(os.path.isdir(os.path.dirname(STEAM_TOOLS)))
        self.p_heroic = QCheckBox("Heroic")
        self.p_heroic.setChecked(os.path.isdir(os.path.dirname(HEROIC_TOOLS)))
        r.addWidget(QLabel(L("Per:", "For:")))
        r.addWidget(self.p_steam)
        r.addWidget(self.p_heroic)
        r.addStretch(1)
        self.c_proton.aggiungi(r)
        self.barra = QProgressBar()
        self.barra.hide()
        self.c_proton.aggiungi(self.barra)
        self.e_proton = QLabel("")
        self.e_proton.setObjectName("quieto")
        self.e_proton.setWordWrap(True)
        self.c_proton.aggiungi(self.e_proton)
        self.b_installa, self.b_rimuovi, self.b_def_steam, self.b_def_heroic = self.c_proton.bottoni(
            (L("Installa", "Install"), self._installa, True),
            (L("Rimuovi", "Remove"), self._rimuovi, False),
            (L("Predefinita in Steam", "Default in Steam"), lambda: self._default("steam"), False),
            (L("Predefinita in Heroic", "Default in Heroic"), lambda: self._default("heroic"), False))
        v.addWidget(self.c_proton)
        v.addStretch(1)
        self._proton_elenca()
        in_sfondo(self._scarica_elenco, self._elenco_pronto, self)

    # ---- Mesa ---------------------------------------------------------------------
    def aggiorna(self):
        m = _mesa_modulo()
        if m is None:
            self.b_mesa.setText(L("non installata", "not installed"))
            self.b_mesa.tono("quieto")
            for cb in (self.m_steam, self.m_heroic, self.m_sistema):
                cb.setEnabled(False)
        else:
            for cb, app in ((self.m_steam, STEAM_APP), (self.m_heroic, HEROIC_APP)):
                cb.blockSignals(True)
                cb.setChecked(bool(_mesa_stato(app)))
                cb.blockSignals(False)
            st = self.demone.cmd(cmd="mesa-sistema") if self.demone.attivo() else self._mesa_sistema_senza_root()
            self.m_sistema.blockSignals(True)
            self.m_sistema.setChecked(bool(st.get("attivo")))
            self.m_sistema.blockSignals(False)
            self.r_mesa_ver.setText(st.get("versione") or "?")
            self.r_mesa_kernel.setText(L("nostro", "ours") if st.get("kernel_nostro") else L("NON nostro", "NOT ours"))
            self.r_mesa_kernel.setStyleSheet("font-weight:600;color:%s;" % (stile.VERDE if st.get("kernel_nostro") else stile.ARANCIO))
            dove = [n for n, on in (("Steam", self.m_steam.isChecked()), ("Heroic", self.m_heroic.isChecked()), (L("sistema", "system"), self.m_sistema.isChecked())) if on]
            self.b_mesa.setText(L("nostra: %s", "ours: %s") % ", ".join(dove) if dove else L("di serie", "stock"))
            self.b_mesa.tono("bene" if dove else "quieto")
        for cb, app in ((self.f_steam, STEAM_APP), (self.f_heroic, HEROIC_APP)):
            cb.blockSignals(True)
            cb.setChecked(_fsr4_stato(app))
            cb.blockSignals(False)
        self._scx_aggiorna()

    def _mesa_sistema_senza_root(self):
        """What can be known without the helper: is the divert there?"""
        rc, out, _ = sh("dpkg-divert --list /usr/lib/x86_64-linux-gnu/libvulkan_radeon.so 2>/dev/null", 10)
        return {"attivo": bool(out), "kernel_nostro": "skillfishos" in os.uname().release,
                "versione": sh("dpkg-query -W -f='${Version}' skillfish-mesa-gfx1013 2>/dev/null", 5)[1]}

    def _mesa_lanciatore(self):
        m = _mesa_modulo()
        if m is None:
            return
        for cb, app in ((self.m_steam, STEAM_APP), (self.m_heroic, HEROIC_APP)):
            try:
                (m.accendi if cb.isChecked() else m.spegni)(app)
            except Exception as e:
                self.toast(str(e))
        self.e_mesa.setText(L("Vale dal prossimo avvio del lanciatore.", "Takes effect the next time the launcher starts."))
        self.aggiorna()

    def _mesa_sistema(self, on):
        if on and QMessageBox.question(self, L("Driver di sistema", "System driver"), L(
                "Da adesso TUTTO quello che usa Vulkan passa dalla nostra Mesa, desktop compreso. "
                "Il 32 bit resta al driver di serie. Procedere?",
                "From now on EVERYTHING that uses Vulkan goes through our Mesa, desktop included. "
                "32-bit stays on the stock driver. Proceed?")) != QMessageBox.StandardButton.Yes:
            self.m_sistema.setChecked(False)
            return
        r = self.demone.cmd(cmd="mesa-sistema-set", on=bool(on))
        if not r.get("ok"):
            self.toast(r.get("err", "?"), 8)
            self.m_sistema.setChecked(not on)
        else:
            self.e_mesa.setText(L("Vale per i programmi avviati da adesso.", "Applies to programs started from now on."))
        self.aggiorna()

    # ---- scheduler --------------------------------------------------------------
    def _scx_aggiorna(self):
        st = self.demone.cmd(cmd="scx") if self.demone.attivo() else self._scx_senza_root()
        self.s_armato.blockSignals(True)
        self.s_armato.setChecked(bool(st.get("abilitato")))
        self.s_armato.setEnabled(bool(st.get("kernel")) and bool(st.get("installato")))
        self.s_armato.blockSignals(False)
        if not st.get("kernel"):
            self.b_scx.setText(L("kernel senza sched_ext", "kernel without sched_ext"))
            self.b_scx.tono("quieto")
        elif not st.get("installato"):
            self.b_scx.setText(L("skillfish-scx non installato", "skillfish-scx not installed"))
            self.b_scx.tono("quieto")
        elif st.get("caricato"):
            self.b_scx.setText(L("caricato adesso", "loaded now"))
            self.b_scx.tono("bene")
        else:
            self.b_scx.setText(L("armato", "armed") if st.get("abilitato") else L("spento", "off"))
            self.b_scx.tono("ottone" if st.get("abilitato") else "quieto")
        self.r_scx_nome.setText(st.get("nome") or L("di serie", "stock"))
        self.r_scx_esp.setText("%d / 2" % int(st.get("espulsioni", 0)))

    def _scx_senza_root(self):
        rc, en, _ = sh("systemctl is-enabled skillfish-scx.path 2>/dev/null", 5)
        conta = ""
        try:
            conta = open("/var/lib/skillfish/scx-espulsioni").read().strip()
        except OSError:
            pass
        ops = ""
        try:
            ops = open("/sys/kernel/sched_ext/root/ops").read().strip()
        except OSError:
            pass
        stato = ""
        try:
            stato = open("/sys/kernel/sched_ext/state").read().strip()
        except OSError:
            pass
        return {"kernel": os.path.isdir("/sys/kernel/sched_ext"), "installato": os.path.exists("/usr/lib/skillfish-scx/scx_bpfland"),
                "abilitato": en == "enabled", "caricato": stato == "enabled", "nome": ops,
                "espulsioni": int(conta) if conta.isdigit() else 0}

    def _scx_set(self, on):
        r = self.demone.cmd(cmd="scx-set", on=bool(on))
        if not r.get("ok"):
            self.toast(r.get("err", "?"))
        self._scx_aggiorna()

    def _scx_azzera(self):
        r = self.demone.cmd(cmd="scx-azzera")
        self.toast(L("contatore azzerato", "counter reset") if r.get("ok") else r.get("err", "?"))
        self._scx_aggiorna()

    # ---- FSR 4 -----------------------------------------------------------------------
    def _fsr4(self):
        for cb, app in ((self.f_steam, STEAM_APP), (self.f_heroic, HEROIC_APP)):
            try:
                _fsr4_set(app, cb.isChecked())
            except Exception as e:
                self.toast(str(e))
        self.toast(L("Vale dal prossimo avvio del lanciatore. Nel gioco scegli DLSS.",
                     "Takes effect the next time the launcher starts. In the game pick DLSS."), 6)

    # ---- Proton ----------------------------------------------------------------------
    def _scarica_elenco(self):
        try:
            req = urllib.request.Request(GE_API, headers={"User-Agent": "SkillFishOS-Control-Center"})
            with urllib.request.urlopen(req, timeout=20) as r:
                dati = json.load(r)
            out = []
            for rel in dati:
                nome = rel.get("tag_name", "")
                asset = next((a for a in rel.get("assets", []) if a["name"].endswith(".tar.gz") and "aarch64" not in a["name"]), None)
                if asset and nome:
                    out.append({"nome": nome, "url": asset["browser_download_url"], "mb": asset["size"] >> 20,
                                "data": (rel.get("published_at") or "")[:10]})
            return {"ok": True, "versioni": out}
        except Exception as e:
            return {"ok": False, "err": str(e)}

    def _elenco_pronto(self, r):
        if r.get("ok"):
            self.versioni = r["versioni"]
        else:
            self.e_proton.setText(L("Elenco da GitHub non disponibile: %s", "GitHub list unavailable: %s") % r.get("err", "?"))
        self._proton_elenca()

    def _proton_elenca(self):
        inst = proton_installati()
        ds, dh = steam_default(), heroic_default()
        scelto = self.lista.currentItem().data(32) if self.lista.currentItem() else None
        self.lista.clear()
        nomi = []
        for v in self.versioni:
            nomi.append(v["nome"])
        for n in inst["steam"] + inst["heroic"]:
            if n not in nomi:
                nomi.append(n)
        for n in nomi:
            dove = []
            if n in inst["steam"]:
                dove.append("Steam" + (" ★" if n == ds else ""))
            if n in inst["heroic"]:
                dove.append("Heroic" + (" ★" if n == dh else ""))
            v = next((x for x in self.versioni if x["nome"] == n), None)
            testo = n
            if v:
                testo += "   ·   %s   ·   %d MB" % (v["data"], v["mb"])
            testo += ("   ·   " + L("installata in ", "installed in ") + ", ".join(dove)) if dove else ("   ·   " + L("non installata", "not installed"))
            it = QListWidgetItem(testo)
            it.setData(32, n)
            if dove:
                it.setForeground(__import__("PyQt6.QtGui", fromlist=["QColor"]).QColor(stile.VERDE))
            self.lista.addItem(it)
            if n == scelto:
                self.lista.setCurrentItem(it)
        if not self.lista.count():
            self.lista.addItem(L("nessuna versione trovata", "no version found"))
        self.r_default = (ds, dh)

    def _scelta(self):
        it = self.lista.currentItem()
        return it.data(32) if it else None

    def _cartelle_scelte(self):
        out = []
        if self.p_steam.isChecked():
            out.append(STEAM_TOOLS)
        if self.p_heroic.isChecked():
            out.append(HEROIC_TOOLS)
        return out

    def _installa(self):
        n = self._scelta()
        v = next((x for x in self.versioni if x["nome"] == n), None)
        if not v:
            self.toast(L("Scegli una versione dell'elenco di GitHub.", "Pick a version from the GitHub list."))
            return
        cartelle = self._cartelle_scelte()
        if not cartelle:
            self.toast(L("Scegli almeno un lanciatore.", "Pick at least one launcher."))
            return
        if self._scarica is not None:
            return
        self.b_installa.setEnabled(False)
        self.barra.setValue(0)
        self.barra.show()
        self.e_proton.setText(L("Scarico %s (%d MB)…", "Downloading %s (%d MB)…") % (n, v["mb"]))
        self._scarica = Scarica(v["url"], n, cartelle, self)
        self._scarica.avanzamento.connect(self._avanza)
        self._scarica.finito.connect(self._scaricato)
        self._scarica.start()

    def _avanza(self, pct, testo):
        self.barra.setValue(pct)
        self.e_proton.setText(testo)

    def _scaricato(self, ok, msg):
        self._scarica = None
        self.b_installa.setEnabled(True)
        self.barra.hide()
        self.e_proton.setText(L("Installata %s.", "Installed %s.") % msg if ok else L("Non riuscito: %s", "Failed: %s") % msg)
        self._proton_elenca()

    def _rimuovi(self):
        n = self._scelta()
        if not n:
            return
        inst = proton_installati()
        dove = [(STEAM_TOOLS, "Steam") for _ in [0] if n in inst["steam"]] + [(HEROIC_TOOLS, "Heroic") for _ in [0] if n in inst["heroic"]]
        if not dove:
            self.toast(L("Non e' installata.", "It is not installed."))
            return
        if QMessageBox.question(self, L("Rimuovere?", "Remove?"), L("Tolgo %s da %s?", "Remove %s from %s?") % (n, ", ".join(d for _, d in dove))) != QMessageBox.StandardButton.Yes:
            return
        for cartella, _ in dove:
            shutil.rmtree(os.path.join(cartella, n), ignore_errors=True)
        self._proton_elenca()

    def _default(self, dove):
        n = self._scelta()
        if not n:
            return
        inst = proton_installati()
        if n not in inst[dove]:
            self.toast(L("Prima installala in %s.", "Install it in %s first.") % dove.capitalize())
            return
        if dove == "heroic":
            try:
                with open(HEROIC_CONFIG) as f:
                    d = json.load(f)
                d.setdefault("defaultSettings", {})["wineVersion"] = {
                    "bin": os.path.join(HEROIC_TOOLS, n, "proton"), "name": n, "type": "proton"}
                with open(HEROIC_CONFIG, "w") as f:
                    json.dump(d, f, indent=2)
                self.e_proton.setText(L("%s e' la predefinita di Heroic.", "%s is Heroic's default.") % n)
            except Exception as e:
                self.toast(str(e))
        else:
            if steam_aperto():
                self.toast(L("Chiudi Steam prima: riscrive la configurazione all'uscita.", "Close Steam first: it rewrites its configuration on exit."), 7)
                return
            if not self._steam_default(n):
                self.toast(L("Non sono riuscito a scrivere config.vdf.", "Could not write config.vdf."))
            else:
                self.e_proton.setText(L("%s e' la predefinita di Steam.", "%s is Steam's default.") % n)
        self._proton_elenca()

    def _steam_default(self, n):
        """Write CompatToolMapping "0" in config.vdf: the global default tool."""
        try:
            with open(STEAM_CONFIG, encoding="utf-8", errors="replace") as f:
                t = f.read()
        except OSError:
            return False
        blocco = ('"CompatToolMapping"\n\t\t\t\t{\n\t\t\t\t\t"0"\n\t\t\t\t\t{\n'
                  '\t\t\t\t\t\t"name"\t\t"%s"\n\t\t\t\t\t\t"config"\t\t""\n\t\t\t\t\t\t"priority"\t\t"75"\n'
                  '\t\t\t\t\t}\n' % n)
        m = re.search(r'"CompatToolMapping"\s*\{', t)
        if m:
            # replace or insert the "0" entry inside the existing block
            inizio = m.end()
            z = re.search(r'"0"\s*\{[^}]*\}', t[inizio:], re.S)
            voce = '"0"\n\t\t\t\t\t{\n\t\t\t\t\t\t"name"\t\t"%s"\n\t\t\t\t\t\t"config"\t\t""\n\t\t\t\t\t\t"priority"\t\t"75"\n\t\t\t\t\t}' % n
            if z and z.start() < 400:
                t = t[:inizio + z.start()] + voce + t[inizio + z.end():]
            else:
                t = t[:inizio] + "\n\t\t\t\t\t" + voce + t[inizio:]
        else:
            s = re.search(r'"Steam"\s*\{', t)
            if not s:
                return False
            t = t[:s.end()] + "\n\t\t\t\t" + blocco + "\t\t\t\t}" + t[s.end():]
        shutil.copy2(STEAM_CONFIG, STEAM_CONFIG + ".skillfish.bak")
        with open(STEAM_CONFIG, "w", encoding="utf-8") as f:
            f.write(t)
        return True

# -*- coding: utf-8 -*-
"""AI: Unsloth Studio on Vulkan, driven from here.

The engine is a service; Studio is its web interface on port 8888. This page
talks to Studio's own API with an API key, so it can do what the old panel
could not: show the version and update it, list the models on disk and
download new ones from the Hub, run a quick chat with a measured speed, open
the engine to the local network, and walk the user through the first sign-in
(Unsloth generates a random password at install and shuts itself down after an
hour if it is not changed).

What needs root goes through the helper: service on/off and autostart, the
bind address and parallel slots in /etc/default/skillfish-unsloth, the copy of
the key the Remote Manager reads, the GTT limit (a kernel parameter, reboot).
"""
import glob
import json
import os
import re
import subprocess
import time
import urllib.error
import urllib.request

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import (QDialog, QDialogButtonBox, QApplication, QCheckBox, QComboBox, QHBoxLayout, QLabel, QLineEdit, QMessageBox,
                             QPlainTextEdit, QProgressBar, QPushButton, QSlider, QSpinBox,
                             QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView,
                             QAbstractItemView)

from ..cluster import Cluster
from ..comune import L, leggi_testo, sh
from ..demone import in_sfondo
from ..finestra import PaginaBase
from ..stile import Scheda, Stato, griglia_schede, intestazione, TESTO_3

UNSLOTH_BIN = "/usr/local/bin/skillfish-unsloth"
UNSLOTH_UPDATE = "/usr/local/bin/skillfish-unsloth-update"
UNSLOTH_SVC = "skillfish-unsloth.service"
PORTA = 8888
UNSLOTH_URL = "http://127.0.0.1:%d" % PORTA
# Lo scrive skillfish-cluster.service: leggibile da tutti, niente pkexec.
CLUSTER_STATO = "/run/skillfish/cluster.json"
CASA = os.path.expanduser("~")
BIN_UTENTE = os.path.join(CASA, ".unsloth", "studio", "unsloth_studio", "bin", "unsloth")
BOOTSTRAP = os.path.join(CASA, ".unsloth", "studio", "auth", ".bootstrap_password")
CHIAVE_F = os.path.join(CASA, ".config", "skillfish", "unsloth.key")
DEFAULT_F = "/etc/default/skillfish-unsloth"
# Repositories on Hugging Face that fit the shared memory of the board; the
# box is editable, any repo id works.
SUGGERITI = ("unsloth/Qwen3-1.7B-GGUF", "unsloth/Qwen3-4B-GGUF", "unsloth/Qwen3-8B-GGUF",
             "unsloth/gemma-3-4b-it-GGUF", "unsloth/Qwen2.5-Coder-7B-Instruct-GGUF")


# ---------------------------------------------------------------- readings
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


def meminfo():
    out = {}
    for line in leggi_testo("/proc/meminfo").splitlines():
        k = line.split(":")[0]
        if k in ("MemTotal", "MemAvailable", "SwapTotal", "SwapFree"):
            out[k] = int(line.split()[1]) * 1024
    return out


def chiave():
    try:
        with open(CHIAVE_F) as f:
            return f.read().strip()
    except OSError:
        return ""


def salva_chiave(valore):
    os.makedirs(os.path.dirname(CHIAVE_F), mode=0o700, exist_ok=True)
    if not valore:
        try:
            os.remove(CHIAVE_F)
        except OSError:
            # already gone, or not readable: either way there is nothing left to remove
            pass
        return
    fd = os.open(CHIAVE_F, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(valore.strip() + "\n")


def bootstrap_password():
    try:
        with open(BOOTSTRAP) as f:
            return f.read().strip()
    except OSError:
        return ""


def studio(path, dati=None, key=None, t=8, metodo=None):
    """One call to Studio's API; JSON in, JSON out, None on any failure."""
    testa = {"Accept": "application/json"}
    if key:
        testa["Authorization"] = "Bearer " + key
    corpo = None
    if dati is not None:
        corpo = json.dumps(dati).encode()
        testa["Content-Type"] = "application/json"
    req = urllib.request.Request(UNSLOTH_URL + path, data=corpo, headers=testa,
                                 method=metodo or ("POST" if dati is not None else "GET"))
    try:
        with urllib.request.urlopen(req, timeout=t) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            return {"_errore": e.code, **json.loads(e.read().decode())}
        except Exception:
            return {"_errore": e.code}
    except Exception:
        return None


def dim_n(n):
    """12862655 -> 12,9M. Un numero a sette cifre non lo legge nessuno."""
    try:
        n = int(n)
    except (TypeError, ValueError):
        return "?"
    for soglia, suff in ((1000000000, "G"), (1000000, "M"), (1000, "k")):
        if n >= soglia:
            return ("%.1f%s" % (n / soglia, suff)).replace(".0", "")
    return str(n)


CARTELLE_MODELLI = ("modelli", "models", ".unsloth/models", ".cache/unsloth/models")


def quant_dal_nome(nome):
    """La quantizzazione, letta dalla coda del nome: Q4_K_M, UD-Q6_K, IQ3_XXS.

    ⚠️ Non la chiediamo a Studio perche' Studio non ce l'ha: /v1/models
    restituisce id, loaded e display_name e basta.
    """
    m = re.search(r"((?:UD-)?(?:IQ|Q)\d+(?:_[A-Za-z0-9]+)*)$", nome or "")
    return m.group(1) if m else ""


_GGUF = {}


def _gguf_sul_disco(rinfresca=False):
    """Nome del file (senza .gguf) -> quanto occupa.

    ⚠️ Si guardano le cartelle dove i modelli finiscono davvero, non l'Hub:
    /api/hub/cached-gguf conosce solo quelli scaricati da li', e chi si copia
    un .gguf a mano - che e' il caso normale su una scheda di prova - non
    comparirebbe mai.
    """
    if _GGUF and not rinfresca:
        return _GGUF
    _GGUF.clear()
    viste = set()
    for base in CARTELLE_MODELLI:
        d = os.path.join(CASA, base)
        if not os.path.isdir(d) or d in viste:
            continue
        viste.add(d)
        # ⚠️ Due livelli, non di piu': dentro .unsloth c'e' la cache di uv con
        # decine di migliaia di file, e scandagliarla a ogni apertura della
        # pagina si sentirebbe.
        for radice, cartelle, file in os.walk(d):
            if radice[len(d):].count(os.sep) >= 2:
                cartelle[:] = []
            for n in file:
                if not n.endswith(".gguf"):
                    continue
                try:
                    _GGUF[n[:-5]] = os.path.getsize(os.path.join(radice, n))
                except OSError:
                    # sparito fra la lettura e lo stat: non e' un guasto
                    pass
    return _GGUF


def cerca_hf(q, limite=40):
    """I GGUF di Hugging Face che somigliano a quello che uno ha scritto.

    Restituisce (elenco, errore). Ogni voce e' (repo_id, scaricamenti, like).

    ⚠️ Niente chiave: questa API risponde in chiaro a chiunque, ed e' un bene,
    perche' vuol dire che la ricerca funziona anche su una scheda dove Studio
    non e' ancora configurato.

    ⚠️ filter=gguf, sempre. Altrimenti escono i modelli in safetensors, che
    llama.cpp non apre: si vedrebbero nell'elenco, si scaricherebbero decine di
    gigabyte e si scoprirebbe dopo.
    """
    q = (q or "").strip()
    if not q:
        return [], L("scrivi qualcosa da cercare", "type something to look for")
    url = ("https://huggingface.co/api/models?search=%s&filter=gguf"
           "&sort=downloads&direction=-1&limit=%d"
           % (urllib.request.quote(q), max(1, min(100, limite))))
    try:
        with urllib.request.urlopen(url, timeout=25) as r:
            dati = json.loads(r.read().decode("utf-8"))
    except Exception as e:                       # rete assente, HF giu', ...
        return [], str(e)
    fuori = []
    for m in dati:
        rid = m.get("id") or m.get("modelId")
        if rid:
            fuori.append((rid, m.get("downloads") or 0, m.get("likes") or 0))
    if not fuori:
        return [], L("nessun modello trovato", "no model found")
    return fuori, None


def crea_chiave(password):
    """Sign in with the Studio password and mint an API key for this machine."""
    r = studio("/api/auth/login", {"username": "unsloth", "password": password})
    if not r or not r.get("access_token"):
        return None, L("password di Studio non accettata", "Studio password not accepted")
    tok = r["access_token"]
    r = studio("/api/auth/api-keys", {"name": "SkillFishOS Control Center"}, key=tok)
    if not r or not r.get("key"):
        return None, L("Studio non ha rilasciato la chiave", "Studio did not issue the key")
    # Without this, a request for a model that is not loaded gets "No model
    # loaded" from the API: with it, Studio loads the model that is asked for.
    studio("/api/settings/openai-auto-switch", {"enabled": True}, key=tok, metodo="PUT")
    return r["key"], ""


def primo_accesso(nuova):
    """The first sign-in done for the user: bootstrap password in, their
    password set, an API key minted. Returns (key, error)."""
    vecchia = bootstrap_password()
    if not vecchia:
        return None, L("password iniziale non trovata", "initial password not found")
    r = studio("/api/auth/login", {"username": "unsloth", "password": vecchia})
    if not r or not r.get("access_token"):
        return None, L("la password iniziale non e' piu' valida: entra in Studio", "the initial password is no longer valid: sign in to Studio")
    r2 = studio("/api/auth/change-password", {"current_password": vecchia, "new_password": nuova}, key=r["access_token"])
    if not r2 or r2.get("_errore"):
        return None, (r2 or {}).get("detail") or L("cambio password rifiutato", "password change refused")
    return crea_chiave(nuova)


def leggi_default():
    out = {"bind": "127.0.0.1", "parallel": 4}
    for line in leggi_testo(DEFAULT_F).splitlines():
        line = line.strip()
        if line.startswith("UNSLOTH_BIND="):
            out["bind"] = line.split("=", 1)[1].strip().strip('"')
        elif line.startswith("UNSLOTH_PARALLEL="):
            try:
                out["parallel"] = int(line.split("=", 1)[1].strip().strip('"'))
            except ValueError:
                # malformed value: fall back to the default set above
                out["parallel"] = 4
    return out


def ip_locale():
    rc, out, _ = sh("hostname -I", 5)
    return (out.split() or ["?"])[0]


def dim(n):
    try:
        n = float(n)
    except (TypeError, ValueError):
        return "?"
    return "%.1f GB" % (n / 1e9) if n >= 1e9 else "%.0f MB" % (n / 1e6)


class Aggiornatore(QThread):
    """skillfish-unsloth-update through pkexec, one line at a time."""
    riga = pyqtSignal(str)
    fine = pyqtSignal(int)

    def run(self):
        try:
            p = subprocess.Popen(["pkexec", UNSLOTH_UPDATE], stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, text=True, bufsize=1)
            for ln in iter(p.stdout.readline, ""):
                if ln:
                    self.riga.emit(ln.rstrip())
            p.wait(3600)
            self.fine.emit(p.returncode)
        except Exception as e:
            self.riga.emit(str(e))
            self.fine.emit(1)


# ---------------------------------------------------------------- the page
class Pagina(PaginaBase):
    def __init__(self, finestra):
        super().__init__(finestra)
        self.intervallo_ms = 5000
        self.occupato = False
        self._agg = None
        self._giro = 0
        self.attivo = False
        self.chiave = chiave()
        self.msgs = []
        self.modelli = []
        self._chiave_morta = False
        self.varianti = []

    # ---- build
    def costruisci(self):
        v = self.corpo_scorrevole()
        v.addWidget(intestazione("AI", L(
            "Unsloth Studio sulla GPU, con llama.cpp su Vulkan: modelli, chat e API restano su questa macchina.",
            "Unsloth Studio on the GPU, llama.cpp on Vulkan: models, chat and API stay on this machine."),
            doc="ai"))

        # -- engine
        self.c_motore = Scheda(L("Motore", "Engine"), L(
            "Acceso tiene la memoria della GPU: spegnilo prima di giocare. L'aggiornamento e' l'installatore ufficiale, rilanciato.",
            "On, it holds GPU memory: turn it off before gaming. Update reruns the official installer."))
        self.b_stato = Stato("", "quieto")
        self.c_motore.testa.insertWidget(self.c_motore.testa.count() - 1, self.b_stato)
        r = QHBoxLayout()
        self.acceso = QCheckBox(L("Acceso", "On"))
        self.acceso.clicked.connect(self._accendi)
        r.addWidget(self.acceso)
        self.autostart = QCheckBox(L("All'avvio", "At boot"))
        self.autostart.clicked.connect(self._autostart)
        r.addWidget(self.autostart)
        r.addStretch(1)
        self.c_motore.aggiungi(r)
        self.r_versione = self.c_motore.riga(L("Versione", "Version"), "—")
        self.r_backend = self.c_motore.riga("Backend", "—")
        self.r_api = self.c_motore.riga("API", UNSLOTH_URL + "/v1")
        self.b_apri, self.b_aggiorna = self.c_motore.bottoni(
            (L("Apri Studio", "Open Studio"), lambda: sh("xdg-open %s &" % UNSLOTH_URL, 5), True),
            (L("Aggiorna", "Update"), self._aggiorna, False))

        # -- access: first sign-in, then the key
        self.c_accesso = Scheda(L("Accesso", "Access"), L(
            "Studio ha un suo utente. La chiave API serve a questa finestra e al Remote Manager per parlare col motore.",
            "Studio has its own user. The API key is how this window and the Remote Manager talk to the engine."))
        self.r_utente = self.c_accesso.riga(L("Utente", "User"), "unsloth")
        self.r_chiave = self.c_accesso.riga(L("Chiave API", "API key"), "—")
        self.w_primo = QWidget()
        pv = QVBoxLayout(self.w_primo)
        pv.setContentsMargins(0, 0, 0, 0)
        pv.setSpacing(6)
        e = QLabel(L("Primo accesso: scegli la password di Studio. La chiave API viene creata insieme.",
                     "First sign-in: choose the Studio password. The API key is created with it."))
        e.setWordWrap(True)
        e.setObjectName("quieto")
        pv.addWidget(e)
        self.pw1 = QLineEdit()
        self.pw1.setEchoMode(QLineEdit.EchoMode.Password)
        self.pw1.setPlaceholderText(L("nuova password", "new password"))
        self.pw2 = QLineEdit()
        self.pw2.setEchoMode(QLineEdit.EchoMode.Password)
        self.pw2.setPlaceholderText(L("ripeti", "repeat"))
        pv.addWidget(self.pw1)
        pv.addWidget(self.pw2)
        b = QPushButton(L("Imposta e crea la chiave", "Set and create the key"))
        b.setObjectName("primario")
        b.clicked.connect(self._primo_accesso)
        pv.addWidget(b)
        self.w_primo.hide()
        self.c_accesso.aggiungi(self.w_primo)
        self.w_chiave = QWidget()
        kv = QVBoxLayout(self.w_chiave)
        kv.setContentsMargins(0, 0, 0, 0)
        kv.setSpacing(6)
        r = QHBoxLayout()
        self.pw_studio = QLineEdit()
        self.pw_studio.setEchoMode(QLineEdit.EchoMode.Password)
        self.pw_studio.setPlaceholderText(L("password di Studio", "Studio password"))
        r.addWidget(self.pw_studio, 1)
        b = QPushButton(L("Crea la chiave", "Create the key"))
        b.clicked.connect(self._crea_chiave)
        r.addWidget(b)
        kv.addLayout(r)
        r = QHBoxLayout()
        self.chiave_in = QLineEdit()
        self.chiave_in.setPlaceholderText(L("oppure incolla una chiave sk-unsloth-…", "or paste a key sk-unsloth-…"))
        r.addWidget(self.chiave_in, 1)
        b = QPushButton(L("Salva", "Save"))
        b.clicked.connect(self._salva_chiave)
        r.addWidget(b)
        kv.addLayout(r)
        self.w_chiave.hide()
        self.c_accesso.aggiungi(self.w_chiave)
        bottoni = self.c_accesso.bottoni(
            (L("Dimentica la chiave", "Forget the key"), self._togli_chiave, False),
            (L("Reimposta la password", "Reset the password"), self._reset_password, False))
        self.b_togli_chiave = bottoni[0]
        self.b_reset = bottoni[1]

        # -- memory
        self.c_mem = Scheda(L("Memoria", "Memory"), L(
            "Sul BC-250 VRAM e RAM sono lo stesso chip: il GTT e' la quota di RAM che il modello puo' usare oltre alla VRAM. Parametro del kernel: serve un riavvio.",
            "On the BC-250 VRAM and RAM are the same chip: the GTT is the share of RAM the model may use on top of VRAM. Kernel parameter: a reboot is needed."))
        self.r_vram = self.c_mem.riga("VRAM")
        # ⚠️ Con la modalita' accesa questa finestra non c'e' piu': il desktop
        # si spegne. Per tornare indietro c'e' il Remote Manager da un altro
        # computer, oppure ssh. Il testo lo dice prima di farlo.
        self.r_ai_mode = self.c_mem.riga(
            L("Modalita' AI", "AI mode"), L("desktop acceso", "desktop running"))
        self.b_ai_mode = self.c_mem.bottoni(
            (L("Spegni il desktop per l'AI", "Shut the desktop down for AI"),
             self._ai_mode, False))[0]
        self.r_gtt = self.c_mem.riga("GTT")
        self.r_ram = self.c_mem.riga("RAM")
        self.r_swap = self.c_mem.riga("Swap")
        self.r_budget = self.c_mem.riga(L("Budget del modello", "Model budget"))
        r = QHBoxLayout()
        self.gtt = QSlider(Qt.Orientation.Horizontal)
        self.gtt.setRange(2, 14)
        self.gtt_et = QLabel("— GB")
        self.gtt_et.setMinimumWidth(56)
        self.gtt.valueChanged.connect(lambda x: self.gtt_et.setText("%d GB" % x))
        r.addWidget(QLabel(L("Limite GTT", "GTT limit")))
        r.addWidget(self.gtt, 1)
        r.addWidget(self.gtt_et)
        self.c_mem.aggiungi(r)
        self.c_mem.bottoni((L("Massimo", "Maximum"), lambda: self.gtt.setValue(self.gtt.maximum()), False),
                           (L("Applica e riavvia", "Apply and reboot"), self._gtt, True))
        v.addWidget(griglia_schede(self.c_motore, self.c_accesso, self.c_mem, colonne=3))

        # -- models
        self.c_modelli = Scheda(L("Modelli", "Models"), L(
            "I GGUF scaricati dall'Hub di Hugging Face. Fino a circa 11 GB di pesi ci stanno; oltre, il resto del sistema soffre.",
            "The GGUFs downloaded from the Hugging Face Hub. Up to about 11 GB of weights fit; past that the rest of the system suffers."))
        self.tab = QTableWidget(0, 3)
        self.tab.setHorizontalHeaderLabels([L("Modello", "Model"), L("Quantizzazione", "Quantization"), L("Dimensione", "Size")])
        self.tab.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tab.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.tab.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.tab.verticalHeader().hide()
        self.tab.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tab.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tab.setMinimumHeight(120)
        self.tab.setMaximumHeight(180)
        self.c_modelli.aggiungi(self.tab)
        # La ricerca su Hugging Face: sopra la tendina, perche' e' da li' che
        # si parte quando non si sa gia' come si chiama il modello.
        r = QHBoxLayout()
        self.cerca_txt = QLineEdit()
        self.cerca_txt.setPlaceholderText(
            L("cerca su Hugging Face: qwen, llama, gemma, coder...",
              "search Hugging Face: qwen, llama, gemma, coder..."))
        self.cerca_txt.returnPressed.connect(self._cerca_hf)
        r.addWidget(self.cerca_txt, 2)
        b = QPushButton(L("Cerca modelli", "Search models"))
        b.clicked.connect(self._cerca_hf)
        r.addWidget(b)
        self.c_modelli.aggiungi(r)
        self.r_trovati = self.c_modelli.riga(L("Trovati", "Found"), "—")

        r = QHBoxLayout()
        self.repo = QComboBox()
        self.repo.setEditable(True)
        self.repo.addItems(SUGGERITI)
        self.repo.lineEdit().setPlaceholderText("utente/Modello-GGUF")
        r.addWidget(self.repo, 2)
        b = QPushButton(L("Cerca", "Look up"))
        b.clicked.connect(self._cerca_varianti)
        r.addWidget(b)
        self.c_modelli.aggiungi(r)
        r = QHBoxLayout()
        self.variante = QComboBox()
        r.addWidget(self.variante, 2)
        self.b_scarica = QPushButton(L("Scarica", "Download"))
        self.b_scarica.setObjectName("primario")
        self.b_scarica.clicked.connect(self._scarica)
        self.b_scarica.setEnabled(False)
        r.addWidget(self.b_scarica)
        self.c_modelli.aggiungi(r)
        self.barra = QProgressBar()
        self.barra.setRange(0, 100)
        self.barra.setTextVisible(True)
        self.barra.hide()
        self.c_modelli.aggiungi(self.barra)
        self.c_modelli.bottoni((L("Apri l'Hub", "Open the Hub"), lambda: sh("xdg-open %s/hub &" % UNSLOTH_URL, 5), False),
                               (L("Aggiorna l'elenco", "Refresh the list"), lambda: self._modelli(True), False))

        # -- chat
        self.c_chat = Scheda("Chat", L(
            "Una prova rapida sull'API: la risposta arriva con i token al secondo misurati. La chat completa, con file e ricerca, e' dentro Studio.",
            "A quick run over the API: the reply comes with the measured tokens per second. The full chat, with files and search, is inside Studio."))
        r = QHBoxLayout()
        self.modello = QComboBox()
        r.addWidget(self.modello, 1)
        b = QPushButton(L("Nuova", "New"))
        b.clicked.connect(self._nuova_chat)
        r.addWidget(b)
        self.c_chat.aggiungi(r)
        self.risposta = QPlainTextEdit()
        self.risposta.setReadOnly(True)
        self.risposta.setMinimumHeight(120)
        self.risposta.setMaximumHeight(220)
        self.risposta.setPlaceholderText(L("La risposta compare qui.", "The reply appears here."))
        self.c_chat.aggiungi(self.risposta, 1)
        r = QHBoxLayout()
        self.domanda = QLineEdit()
        self.domanda.setPlaceholderText(L("Scrivi e premi Invio", "Type and press Enter"))
        self.domanda.returnPressed.connect(self._invia)
        r.addWidget(self.domanda, 1)
        self.b_invia = QPushButton(L("Invia", "Send"))
        self.b_invia.setObjectName("primario")
        self.b_invia.clicked.connect(self._invia)
        r.addWidget(self.b_invia)
        self.c_chat.aggiungi(r)
        self.r_velocita = self.c_chat.riga(L("Velocita'", "Speed"), "—")

        # -- network
        self.c_rete = Scheda(L("Rete", "Network"), L(
            "Aperto sulla rete locale, Studio risponde anche agli altri dispositivi di casa, con il suo utente e la sua password. Le chat in parallelo sono i posti di llama-server.",
            "Open on the local network, Studio answers the other devices at home too, with its own user and password. Parallel chats are llama-server's slots."))
        self.lan = QCheckBox(L("Raggiungibile dalla rete locale", "Reachable from the local network"))
        self.c_rete.aggiungi(self.lan)
        self.r_indirizzo = self.c_rete.riga(L("Indirizzo", "Address"), "—")
        r = QHBoxLayout()
        r.addWidget(QLabel(L("Chat in parallelo", "Parallel chats")))
        self.slot = QSpinBox()
        self.slot.setRange(1, 16)
        r.addWidget(self.slot)
        r.addStretch(1)
        self.c_rete.aggiungi(r)
        self.c_rete.bottoni((L("Applica", "Apply"), self._rete, True))
        # --- il cluster ------------------------------------------------
        # ⚠️ IL CLUSTER NON FA ANDARE PIU' VELOCE. Misurato fra .32 e .40 il
        # 12/09/2026: un modello che entra in una scheda sola perde il 35%
        # quando lo si divide (35,7 contro 23,3 token al secondo), perche' ogni
        # confine fra strati e' un viaggio sulla rete. Serve a far girare quello
        # che da solo non gira: il 27B a Q6 su una scheda non si carica
        # nemmeno, su due fa 7,6 token al secondo. Il testo della scheda lo
        # dice, perche' e' la prima cosa che uno deve sapere prima di
        # accenderlo.
        self.c_cluster = Scheda(L("Cluster", "Cluster"), L(
            "Piu' schede BC-250 che si dividono un modello troppo grande per una "
            "sola. NON va piu' veloce: la rete costa. Serve per i modelli che "
            "su una scheda non entrano.",
            "Several BC-250 boards sharing a model too large for one. It is NOT "
            "faster: the network costs. It is for models that do not fit on a "
            "single board."))
        self.cluster = Cluster()
        self.c_cluster.aggiungi(self.cluster)

        # il pannello per aggiungerne una, chiuso finche' non serve
        self.w_agg = QWidget()
        ag = QVBoxLayout(self.w_agg)
        ag.setContentsMargins(0, 6, 0, 0)
        ag.setSpacing(6)
        r = QHBoxLayout()
        self.cl_ip = QLineEdit()
        self.cl_ip.setPlaceholderText(L("indirizzo, es. 192.168.1.40", "address, e.g. 192.168.1.40"))
        r.addWidget(self.cl_ip, 2)
        self.cl_utente = QLineEdit("root")
        self.cl_utente.setPlaceholderText(L("utente", "user"))
        r.addWidget(self.cl_utente, 1)
        ag.addLayout(r)
        r = QHBoxLayout()
        self.cl_pw = QLineEdit()
        self.cl_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.cl_pw.setPlaceholderText(L("password (serve una volta sola)",
                                        "password (needed once)"))
        r.addWidget(self.cl_pw, 2)
        b = QPushButton(L("Aggiungi", "Add"))
        b.setObjectName("primario")
        b.clicked.connect(self._cluster_aggiungi)
        r.addWidget(b)
        ag.addLayout(r)
        self.cl_esito = QLabel("")
        self.cl_esito.setWordWrap(True)
        self.cl_esito.setStyleSheet("color: %s;" % TESTO_3)
        ag.addWidget(self.cl_esito)
        self.w_agg.hide()
        self.c_cluster.aggiungi(self.w_agg)

        self.c_cluster.bottoni(
            (L("Aggiungi una scheda", "Add a board"),
             lambda: self.w_agg.setVisible(not self.w_agg.isVisible()), False),
            (L("Accendi i nodi", "Start the nodes"), self._cluster_avvia, False),
            (L("Spegni i nodi", "Stop the nodes"), self._cluster_ferma, False))
        v.addWidget(self.c_cluster)

        v.addWidget(griglia_schede(self.c_modelli, self.c_chat, self.c_rete, colonne=3))

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(200)
        self.log.hide()
        v.addWidget(self.log)
        v.addStretch(1)
        self._hw()
        self._rete_leggi()

    def attiva(self):
        super().attiva()
        self._giro = 0

    # ---- readings
    def _hw(self):
        d = _drm()
        vt = _int(os.path.join(d, "mem_info_vram_total")) if d else None
        vu = _int(os.path.join(d, "mem_info_vram_used")) if d else None
        gt = _int(os.path.join(d, "mem_info_gtt_total")) if d else None
        gu = _int(os.path.join(d, "mem_info_gtt_used")) if d else None
        m = meminfo()
        self.r_vram.setText("%s %s / %s" % (gb((vt or 0) - (vu or 0)), L("libera", "free"), gb(vt)) if vt else L("n/d", "n/a"))
        self.r_gtt.setText("%s %s / %s" % (gb(gu), L("usato", "used"), gb(gt)) if gt else L("n/d", "n/a"))
        self.r_ram.setText("%s %s / %s" % (gb(m.get("MemAvailable")), L("libera", "free"), gb(m.get("MemTotal"))))
        self.r_swap.setText("%s / %s" % (gb(m.get("SwapFree")), gb(m.get("SwapTotal"))) if m.get("SwapTotal") else L("nessuno", "none"))
        self.r_budget.setText(gb((vt or 0) + (gt or 0)) if (vt and gt) else "—")
        if not getattr(self, "_gtt_pronto", False):
            cur, leva = gtt_richiesto()
            ram_gb = int(m.get("MemTotal", 14e9) / 1e9)
            self.gtt.setMaximum(max(4, min(60, ram_gb - 1)))
            if cur is not None:
                self.gtt.setValue(max(2, min(self.gtt.maximum(), round(cur / 1024))))
                self.gtt_et.setText("%d GB" % self.gtt.value())
            else:
                self.gtt.setEnabled(False)
            self._gtt_pronto = True

    def _rete_leggi(self):
        d = leggi_default()
        self.lan.setChecked(d["bind"] not in ("127.0.0.1", "localhost", "::1"))
        self.slot.setValue(d["parallel"])
        self.r_indirizzo.setText("http://%s:%d" % (ip_locale() if self.lan.isChecked() else "127.0.0.1", PORTA))

    def aggiorna(self):
        if self.occupato:
            return
        self._hw()
        inst = os.path.exists(UNSLOTH_BIN) and os.path.exists(BIN_UTENTE)
        rc, out, _ = sh("systemctl is-active %s; systemctl is-enabled %s" % (UNSLOTH_SVC, UNSLOTH_SVC), 8)
        righe = out.split()
        on = bool(righe) and righe[0] == "active"
        self.acceso.blockSignals(True)
        self.acceso.setChecked(on)
        self.acceso.setEnabled(inst)
        self.acceso.blockSignals(False)
        self.autostart.blockSignals(True)
        self.autostart.setChecked(len(righe) > 1 and righe[1] == "enabled")
        self.autostart.setEnabled(inst)
        self.autostart.blockSignals(False)
        self.b_aggiorna.setText(L("Aggiorna", "Update") if inst else L("Installa", "Install"))
        if not inst:
            self.b_stato.setText(L("non installato", "not installed"))
            self.b_stato.tono("quieto")
            self.r_versione.setText("—")
        elif on:
            self.b_stato.setText(L("acceso", "on"))
            self.b_stato.tono("bene")
        else:
            self.b_stato.setText(L("spento: GPU libera per i giochi", "off: GPU free for games"))
            self.b_stato.tono("quieto")
        self.attivo = on
        self._accesso(on)
        # Studio's own API, off the GUI thread and not on every tick
        if on and self._giro % 6 == 0:
            in_sfondo(self._leggi_studio, self._studio_letto, self)
        if on and self.barra.isVisible() and self._giro % 1 == 0:
            in_sfondo(self._leggi_download, self._download_letto, self)
        # ⚠️ Il cluster si rilegge nel giro, non solo all'apertura. La prima
        # stesura lo leggeva una volta sola nel costruttore: a quel punto
        # l'helper non e' ancora autenticato (pkexec deve ancora chiedere la
        # password), la risposta e' un errore e il grafico restava a zero
        # schede per sempre.
        # Ogni cinque giri: la telemetria passa da ssh e una scheda spenta
        # costa otto secondi di attesa, che non si vogliono ogni secondo.
        if self._giro % 5 == 0:
            self._cluster_leggi()
        self._giro += 1

    def _accesso(self, on):
        st = studio("/api/auth/status", t=3) if on else None
        primo = bool(st and st.get("requires_password_change"))
        self.w_primo.setVisible(on and primo and bool(bootstrap_password()))
        self.w_chiave.setVisible(on and not primo and not self.chiave)
        self.b_togli_chiave.setVisible(bool(self.chiave))
        if self.chiave:
            self.r_chiave.setText(L("impostata", "set") + " (%s…)" % self.chiave[:14])
        elif on and primo:
            self.r_chiave.setText(L("dopo il primo accesso", "after the first sign-in"))
        elif getattr(self, "_chiave_morta", False):
            self.r_chiave.setText(L("non vale piu'", "no longer valid"))
        else:
            self.r_chiave.setText(L("manca", "missing"))
        if st:
            self.r_utente.setText(st.get("default_username") or "unsloth")

    def _leggi_studio(self):
        k = self.chiave
        out = {"agg": studio("/api/studio/update-status", key=k, t=6) if k else None,
               "backend": studio("/api/llama/backend", key=k, t=6) if k else None,
               "v1": studio("/v1/models", key=k, t=6) if k else None,
               "cache": studio("/api/hub/cached-gguf", key=k, t=8) if k else None}
        if not k or not out["agg"] or out["agg"].get("_errore"):
            rc, ver, _ = sh("%s --version" % BIN_UTENTE, 20) if os.path.exists(BIN_UTENTE) else (1, "", "")
            out["ver"] = ver.split()[-1] if ver else ""
        return out

    def _studio_letto(self, r):
        agg = r.get("agg") or {}
        if agg.get("current_version"):
            v = agg["current_version"]
            if agg.get("update_available") and agg.get("latest_version"):
                v += "  →  %s %s" % (agg["latest_version"], L("disponibile", "available"))
            self.r_versione.setText(v)
        elif r.get("ver"):
            self.r_versione.setText(r["ver"])
        elif not self.chiave:
            self.r_versione.setText(L("serve la chiave", "needs the key"))
        be = r.get("backend") or {}
        if be.get("backend"):
            self.r_backend.setText("llama.cpp %s (%s)" % (be["backend"], be.get("installed_tag") or ""))
        v1 = r.get("v1") or {}
        # ⚠️ 401 = la chiave e' stata revocata (di solito da un reset della
        # password, anche fatto da un'altra parte). Senza questo controllo la
        # pagina resta muta: schede vuote, "nessun modello scaricato" con i
        # modelli sul disco, e la riga della chiave che dice "impostata".
        if isinstance(v1, dict) and v1.get("_errore") in (401, 403):
            self.chiave = ""
            salva_chiave("")
            self._chiave_morta = True
            self.r_backend.setText("—")
            self.modelli = []
            self.modello.clear()
            self._riempi_modelli([], [])
            return
        # ⚠️ Solo una lettura andata a buon fine con una chiave in mano
        # cancella il segno. Azzerarlo sempre lo faceva sparire al giro dopo,
        # quando la chiave revocata era gia' stata tolta e il 401 non arrivava
        # piu': il messaggio durava sei secondi e poi tornava un innocuo
        # "nessun modello scaricato".
        if self.chiave:
            self._chiave_morta = False
        dati = [m for m in v1.get("data", []) if m.get("id")]
        ids = sorted(m["id"] for m in dati)
        if ids != self.modelli:
            self.modelli = ids
            cur = self.modello.currentText()
            self.modello.clear()
            self.modello.addItems(ids)
            if cur in ids:
                self.modello.setCurrentText(cur)
        cache = r.get("cache") or {}
        self._riempi_modelli(dati, cache.get("cached") or [])

    def _riempi_modelli(self, dati, repos):
        """/v1/models says what can be served (and what is loaded), the Hub
        cache says how big each repository is on disk."""
        dimensioni = {rp.get("repo_id"): rp.get("size_bytes") for rp in repos}
        # Quello che l'Hub non sa lo sa il disco.
        sul_disco = _gguf_sul_disco(rinfresca=True)
        righe = []
        for m in sorted(dati, key=lambda x: x["id"]):
            q = m.get("quant") or quant_dal_nome(m["id"])
            if m.get("loaded"):
                q += ("  ·  " if q else "") + L("in memoria", "loaded")
            peso = dimensioni.get(m["id"]) or sul_disco.get(m["id"])
            righe.append((m["id"], q, dim(peso)))
        self.tab.setRowCount(len(righe))
        for i, (a, b, c) in enumerate(righe):
            for j, t in enumerate((a, b, c)):
                it = QTableWidgetItem(t)
                if j:
                    it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tab.setItem(i, j, it)
        if not righe:
            self.tab.setRowCount(1)
            if getattr(self, "_chiave_morta", False):
                vuoto = L("la chiave API non vale piu': rientra con la password",
                          "the API key is no longer valid: sign in again")
            elif not self.chiave:
                vuoto = L("serve la chiave API: entra qui sopra",
                          "the API key is missing: sign in above")
            else:
                vuoto = L("nessun modello scaricato", "no model downloaded")
            self.tab.setItem(0, 0, QTableWidgetItem(vuoto))
            self.tab.setSpan(0, 0, 1, 3)
        else:
            self.tab.clearSpans()

    def _modelli(self, ora=False):
        if self.attivo:
            in_sfondo(self._leggi_studio, self._studio_letto, self)

    # ---- engine
    def _accendi(self, on):
        self.occupato = True
        r = self.demone.cmd(cmd="servizio", azione="start" if on else "stop", unit=UNSLOTH_SVC)
        self.occupato = False
        if not r.get("ok"):
            self.toast(r.get("err") or L("non riuscito", "failed"))
        self.aggiorna()

    def _autostart(self, on):
        r = self.demone.cmd(cmd="servizio", azione="enable" if on else "disable", unit=UNSLOTH_SVC)
        if not r.get("ok"):
            self.toast(r.get("err") or L("non riuscito", "failed"))
        self.aggiorna()

    def _aggiorna(self):
        if self._agg is not None:
            return
        if os.path.exists(BIN_UTENTE):
            if QMessageBox.question(self, "AI", L("Rilancio l'installatore ufficiale di Unsloth (qualche GB, il motore si riavvia)?",
                                                  "Rerun the official Unsloth installer (a few GB, the engine restarts)?")) != QMessageBox.StandardButton.Yes:
                return
        self.log.clear()
        self.log.show()
        self.log.appendPlainText(L("Scarico Unsloth Studio (backend Vulkan)…", "Downloading Unsloth Studio (Vulkan backend)…"))
        self._agg = Aggiornatore(self)
        self._agg.riga.connect(self.log.appendPlainText)
        self._agg.fine.connect(self._aggiornato)
        self._agg.start()

    def _aggiornato(self, rc):
        self._agg = None
        self.log.appendPlainText(L("Fatto.", "Done.") if rc == 0 else L("Non riuscito (uscita %d).", "Failed (exit %d).") % rc)
        self._giro = 0
        self.aggiorna()

    # ---- access
    def _primo_accesso(self):
        p1, p2 = self.pw1.text(), self.pw2.text()
        if len(p1) < 8:
            self.toast(L("Almeno 8 caratteri.", "At least 8 characters."))
            return
        if p1 != p2:
            self.toast(L("Le due password non coincidono.", "The two passwords do not match."))
            return
        self.occupato = True
        in_sfondo(lambda: primo_accesso(p1), self._chiave_arrivata, self)

    def _crea_chiave(self):
        pw = self.pw_studio.text()
        if not pw:
            return
        self.occupato = True
        in_sfondo(lambda: crea_chiave(pw), self._chiave_arrivata, self)

    def _chiave_arrivata(self, r):
        self.occupato = False
        k, err = r if isinstance(r, tuple) else (None, str(r))
        if not k:
            self.toast(err or L("non riuscito", "failed"), 6)
            return
        self.pw1.clear()
        self.pw2.clear()
        self.pw_studio.clear()
        self._imposta_chiave(k)
        self.toast(L("Chiave creata e salvata.", "Key created and saved."))

    def _salva_chiave(self):
        k = self.chiave_in.text().strip()
        if not k.startswith("sk-"):
            self.toast(L("Una chiave di Studio comincia con sk-.", "A Studio key starts with sk-."))
            return
        self.chiave_in.clear()
        self._imposta_chiave(k)
        self.toast(L("Chiave salvata.", "Key saved."))

    def _imposta_chiave(self, k):
        salva_chiave(k)
        self.chiave = k
        # the Remote Manager reads its own copy, written by root
        self.demone.cmd(cmd="unsloth-key-set", key=k)
        self._giro = 0
        self.aggiorna()

    def _ai_mode(self):
        """Spegne il desktop per lasciare la memoria al modello.

        ⚠️ Da qui si puo' solo ACCENDERE. Per spegnerla servirebbe una finestra
        che, un secondo dopo, non esiste piu': il ritorno si fa dal Remote
        Manager di un altro computer, o da ssh. Dirlo prima e' l'unica cosa
        onesta da fare.
        """
        if QMessageBox.question(
                self, L("Modalita' AI", "AI mode"),
                L("Spengo il desktop?\n\n"
                  "Si chiude tutto quello che hai aperto, senza salvare, e "
                  "liberi circa mezzo giga per il modello. Lo schermo diventa "
                  "nero.\n\n"
                  "Per tornare al desktop: dal Remote Manager di un altro "
                  "computer, oppure `skillfish-ai-mode off` da ssh.",
                  "Shut the desktop down?\n\n"
                  "Everything you have open closes without saving, and about "
                  "half a gigabyte goes to the model. The screen goes "
                  "black.\n\n"
                  "To come back: from the Remote Manager on another computer, "
                  "or `skillfish-ai-mode off` over ssh.")
        ) != QMessageBox.StandardButton.Yes:
            return
        # ⚠️ La risposta si guarda. Prima si buttava via: se l'helper non
        # partiva (password annullata) il pulsante non faceva niente e non
        # diceva niente, ed e' esattamente cosi' che il guasto e' arrivato in
        # mano a chi usa la macchina.
        r = self.demone.cmd(cmd="ai-mode", azione="on", insisti=True)
        if not r.get("ok"):
            QMessageBox.warning(self, L("Modalita' AI", "AI mode"),
                                r.get("errore") or r.get("err") or L(
                                    "non ci sono riuscito", "could not do it"))
            return
        # Se il desktop e' ancora in piedi dopo la risposta, qualcosa non ha
        # funzionato: meglio dirlo che lasciare un pulsante che sembra inerte.
        if not r.get("attiva"):
            QMessageBox.warning(self, L("Modalita' AI", "AI mode"), L(
                "La modalita' AI non si e' accesa. Da ssh: "
                "`skillfish-ai-mode on` dice perche'.",
                "AI mode did not come on. Over ssh, `skillfish-ai-mode on` "
                "says why."))

    def _cluster_leggi(self):
        """La telemetria di tutte le schede, letta da /run.

        ⚠️ NON si passa dall'helper. Chiedere la telemetria a root vuol dire
        pkexec, cioe' una password: il riquadro restava vuoto finche' l'utente
        non la digitava per qualche altro motivo, e diceva "0 schede" con due
        schede accese e funzionanti (visto sulla .32 il 12/09/2026). La
        raccolta la fa skillfish-cluster.service e lascia il risultato in un
        file che leggono tutti.
        """
        try:
            with open(CLUSTER_STATO, encoding="utf-8") as f:
                self.cluster.aggiorna(json.load(f))
        except (OSError, ValueError):
            # Il servizio puo' essere spento: non e' un errore da mostrare,
            # il riquadro dice gia' "nessuna scheda".
            pass

    def _cluster_aggiungi(self):
        ip = self.cl_ip.text().strip()
        if not ip:
            return
        self.cl_esito.setText(L("controllo...", "checking..."))
        ut = self.cl_utente.text().strip() or "root"
        pw = self.cl_pw.text()
        in_sfondo(lambda: self.demone.cmd(cmd="cluster", azione="aggiungi", insisti=True,
                                          ip=ip, utente=ut, password=pw),
                  self._cluster_aggiunta, self)

    def _cluster_aggiunta(self, r):
        # ⚠️ La password si cancella SUBITO dal campo: e' servita per mettere
        # la chiave, da adesso in poi non serve piu' a niente e non deve
        # restare a schermo.
        self.cl_pw.clear()
        passi = r.get("passi") or []
        righe = []
        for x in passi:
            segno = "ok" if x.get("ok") else "no"
            nota = (" - " + x["nota"]) if x.get("nota") else ""
            righe.append("%s  %s%s" % (segno, x.get("passo", ""), nota))
        if not r.get("ok"):
            righe.append(r.get("errore", ""))
        elif not r.get("ha_nodo"):
            righe.append(L(
                "La scheda e' nell'elenco, ma il nodo RPC non c'e' ancora: va "
                "installato su quella macchina in /opt/skillfish-rpc.",
                "The board is in the list, but the RPC node is not there yet: "
                "it has to be installed on that machine in /opt/skillfish-rpc."))
        self.cl_esito.setText("\n".join(x for x in righe if x))
        if r.get("ok"):
            self.cl_ip.clear()
        self._cluster_leggi()

    def _cluster_avvia(self):
        in_sfondo(lambda: self.demone.cmd(cmd="cluster", azione="avvia", insisti=True),
                  lambda r: self._cluster_esito(r, True), self)

    def _cluster_ferma(self):
        in_sfondo(lambda: self.demone.cmd(cmd="cluster", azione="ferma", insisti=True),
                  lambda r: self._cluster_esito(r, False), self)

    def _cluster_esito(self, r, acceso):
        quante = len(r.get("schede") or [])
        self.cl_esito.setText(
            (L("nodi accesi su %d schede", "nodes started on %d boards")
             if acceso else
             L("nodi spenti su %d schede", "nodes stopped on %d boards")) % quante)
        self._cluster_leggi()

    def _reset_password(self):
        """Ruota la password di Studio e la mostra una volta sola.

        ⚠️ Si chiede conferma prima: ruotarla butta fuori chi era dentro, e i
        collegamenti di anteprima gia' condivisi restano validi (vanno
        rigenerati dalle impostazioni di Studio).
        """
        # La password la sceglie chi usa la macchina. Lasciando vuoto si
        # prende quella casuale che genera Studio, e la si copia.
        d = QDialog(self)
        d.setWindowTitle(L("Password di Studio", "Studio password"))
        g = QVBoxLayout(d)
        t = QLabel(L("Scegli la password nuova per Unsloth Studio (utente "
                     "unsloth).\n\nQuella di adesso smette di funzionare "
                     "subito e chi sta usando Studio viene scollegato.\n"
                     "Lascia vuoto per farne generare una a caso.",
                     "Choose the new password for Unsloth Studio (user "
                     "unsloth).\n\nThe current one stops working right away "
                     "and anyone using Studio is signed out.\n"
                     "Leave empty to have a random one generated."))
        t.setWordWrap(True)
        g.addWidget(t)
        p1 = QLineEdit(); p1.setEchoMode(QLineEdit.EchoMode.Password)
        p1.setPlaceholderText(L("password nuova", "new password"))
        p2 = QLineEdit(); p2.setEchoMode(QLineEdit.EchoMode.Password)
        p2.setPlaceholderText(L("ripetila", "repeat it"))
        g.addWidget(p1); g.addWidget(p2)
        bb = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok
                              | QDialogButtonBox.StandardButton.Cancel)
        bb.accepted.connect(d.accept); bb.rejected.connect(d.reject)
        g.addWidget(bb)
        if d.exec() != QDialog.DialogCode.Accepted:
            return
        scelta = p1.text()
        if scelta and scelta != p2.text():
            QMessageBox.warning(self, "AI", L("le due password non coincidono",
                                              "the two passwords do not match"))
            return
        # ⚠️ In sottofondo: fra il reset, i tentativi di rientro e la chiave
        # nuova si arriva a piu' di un minuto, e una finestra che non ridisegna
        # per un minuto la si chiude credendo che sia piantata.
        self.b_reset.setEnabled(False)
        self.b_reset.setText(L("Cambio la password…", "Changing the password…"))
        in_sfondo(lambda: self.demone.cmd(cmd="unsloth-password-reset", scelta=scelta, insisti=True),
                  lambda r: self._reset_fatto(r, scelta), self)

    def _reset_fatto(self, r, scelta):
        self.b_reset.setEnabled(True)
        self.b_reset.setText(L("Reimposta la password", "Reset the password"))
        if r.get("chiave"):
            self.chiave = r["chiave"]
            salva_chiave(self.chiave)
            self._chiave_morta = False
        if not r.get("ok"):
            # ⚠️ `errore` lo mette la nostra funzione, `err` il demone quando e'
            # lui a non partire (pkexec annullato, nessun agente polkit). Senza
            # il secondo si vedeva un "non ci sono riuscito" muto.
            QMessageBox.warning(self, "AI", r.get("errore") or r.get("err") or L(
                "non ci sono riuscito", "could not do it"))
            return
        nuova = r.get("password") or ""
        if r.get("scelta"):
            QMessageBox.information(self, "AI", L(
                "Fatto. Entra in Studio con l'utente unsloth e la password che "
                "hai scelto.",
                "Done. Sign in to Studio with user unsloth and the password "
                "you chose."))
            return
        if nuova and r.get("errore"):
            # La casuale e' valida, la scelta no: si dice come stanno le cose
            # invece di far credere che sia andata.
            QMessageBox.warning(self, "AI", L(
                "La password e' stata cambiata, ma NON in quella che hai "
                "scelto:\n\n%s\n\nUsa quella qui sotto.",
                "The password was changed, but NOT to the one you chose:"
                "\n\n%s\n\nUse the one below.") % r["errore"])
        if nuova:
            m = QMessageBox(self)
            m.setWindowTitle(L("Password di Studio", "Studio password"))
            m.setText(L("La password nuova e':\n\n%s\n\nUtente: unsloth",
                        "The new password is:\n\n%s\n\nUser: unsloth") % nuova)
            m.setInformativeText(L("Non la salviamo da nessuna parte.",
                                   "We do not store it anywhere."))
            # Un pulsante per copiarla: nessuno ricopia a mano trenta caratteri.
            copia = m.addButton(L("Copia", "Copy"), QMessageBox.ButtonRole.ActionRole)
            m.addButton(QMessageBox.StandardButton.Ok)
            m.exec()
            if m.clickedButton() is copia:
                QApplication.clipboard().setText(nuova)
        else:
            QMessageBox.information(self, "AI", L(
                "Password cambiata, ma non sono riuscito a leggerla "
                "dall'uscita del comando:\n\n%s",
                "Password changed, but I could not read it from the command "
                "output:\n\n%s") % (r.get("uscita") or ""))

    def _togli_chiave(self):
        if QMessageBox.question(self, "AI", L("Dimentico la chiave qui e nel Remote Manager? In Studio resta valida.",
                                              "Forget the key here and in the Remote Manager? It stays valid in Studio.")) != QMessageBox.StandardButton.Yes:
            return
        salva_chiave("")
        self.chiave = ""
        self.demone.cmd(cmd="unsloth-key-set", key="")
        self.modelli = []
        self.modello.clear()
        self.aggiorna()

    # ---- memory
    def _gtt(self):
        mb = self.gtt.value() * 1024
        if QMessageBox.question(self, "GTT", L("Imposto %d GB e riavvio?", "Set %d GB and reboot?") % self.gtt.value()) != QMessageBox.StandardButton.Yes:
            return
        r = self.demone.cmd(cmd="gtt", mb=mb)
        if r.get("ok"):
            self.demone.cmd(cmd="riavvia")
        else:
            self.toast(r.get("out") or r.get("err") or "?")

    # ---- models
    def _cerca_hf(self):
        """Cerca su Hugging Face e riempie la tendina con quello che esce."""
        q = self.cerca_txt.text().strip()
        if not q:
            return
        self.r_trovati.setText(L("cerco...", "searching..."))
        in_sfondo(lambda: cerca_hf(q), self._trovati_hf, self)

    def _trovati_hf(self, r):
        elenco, errore = r
        if errore:
            self.r_trovati.setText(errore)
            return
        # ⚠️ Dopo una ricerca si mostra il PRIMO RISULTATO, non quello che
        # c'era prima. La prima stesura conservava il valore precedente per non
        # cancellare quello che uno stava scrivendo: provata sulla scheda, il
        # risultato era che la tendina non cambiava e la ricerca sembrava non
        # aver fatto niente.
        self.repo.clear()
        for rid, scar, like in elenco:
            # Gli scaricamenti sono l'unico indizio utile per capire, fra dieci
            # repository con lo stesso nome, quale usa la gente.
            self.repo.addItem("%s   (%s ↓)" % (rid, dim_n(scar)), rid)
        self.r_trovati.setText(L("%d modelli", "%d models") % len(elenco))
        self.repo.setCurrentIndex(0)
        # e si guardano subito le quantizzazioni del primo: e' il passo dopo,
        # e farlo fare a mano sarebbe un clic in piu' per nessun motivo.
        self._cerca_varianti()

    def _cerca_varianti(self):
        # ⚠️ L'etichetta della tendina ha appeso il numero di scaricamenti:
        # a Unsloth va l'id nudo, che sta nel dato della voce.
        repo = (self.repo.currentData() or self.repo.currentText().split("   ")[0]).strip()
        if not repo or "/" not in repo:
            self.toast(L("Indica il repository come utente/nome.", "Give the repository as user/name."))
            return
        if not self.chiave or not self.attivo:
            self.toast(L("Serve il motore acceso e la chiave.", "Needs the engine on and the key."))
            return
        self.variante.clear()
        self.variante.addItem(L("cerco…", "looking up…"))
        self.b_scarica.setEnabled(False)
        in_sfondo(lambda: studio("/api/hub/gguf-variants?repo_id=" + urllib.request.quote(repo, safe=""), key=self.chiave, t=40),
                  self._varianti_lette, self)

    def _varianti_lette(self, r):
        self.variante.clear()
        vs = (r or {}).get("variants") or []
        self.varianti = vs
        if not vs:
            self.variante.addItem((r or {}).get("detail") or L("nessun GGUF trovato", "no GGUF found"))
            return
        for v in vs:
            self.variante.addItem("%s  ·  %s%s" % (v.get("quant") or v.get("filename"), dim(v.get("size_bytes")),
                                                   ("  ·  " + L("gia' scaricato", "already downloaded")) if v.get("downloaded") else ""))
        # the first Unsloth Dynamic 4-bit, or the first one that fits, is a sensible default
        for i, v in enumerate(vs):
            if (v.get("quant") or "").upper().startswith(("UD-Q4", "Q4_K_M")):
                self.variante.setCurrentIndex(i)
                break
        self.b_scarica.setEnabled(True)

    def _scarica(self):
        i = self.variante.currentIndex()
        if i < 0 or i >= len(self.varianti):
            return
        v = self.varianti[i]
        # ⚠️ L'etichetta della tendina ha appeso il numero di scaricamenti:
        # a Unsloth va l'id nudo, che sta nel dato della voce.
        repo = (self.repo.currentData() or self.repo.currentText().split("   ")[0]).strip()
        self._dl_repo = repo
        self.b_scarica.setEnabled(False)
        self.barra.setValue(0)
        self.barra.setFormat("%s · %s" % (repo, v.get("quant") or ""))
        self.barra.show()
        in_sfondo(lambda: studio("/api/hub/download", {"repo_id": repo, "gguf_variant": v.get("quant")}, key=self.chiave, t=40),
                  self._scaricamento_avviato, self)

    def _scaricamento_avviato(self, r):
        if not r or not r.get("accepted", r.get("state") == "running"):
            self.barra.hide()
            self.b_scarica.setEnabled(True)
            self.toast((r or {}).get("detail") or L("Studio non ha accettato il download", "Studio did not accept the download"), 6)
            return
        self.toast(L("Download avviato.", "Download started."))
        self.timer.setInterval(2000)

    def _leggi_download(self):
        repo = getattr(self, "_dl_repo", "")
        return {"attivi": studio("/api/hub/active-downloads", key=self.chiave, t=6),
                "prog": studio("/api/hub/download-progress?repo_id=" + urllib.request.quote(repo, safe=""), key=self.chiave, t=6) if repo else None}

    def _download_letto(self, r):
        attivi = (r.get("attivi") or {}).get("downloads") or []
        prog = r.get("prog") or {}
        pct = None
        tot = prog.get("expected_bytes") or prog.get("total_bytes")
        if prog.get("downloaded_bytes") and tot:
            pct = 100.0 * prog["downloaded_bytes"] / tot
        elif isinstance(prog.get("progress"), (int, float)):
            pct = float(prog["progress"]) * (100.0 if prog["progress"] <= 1 else 1.0)
        if pct is not None:
            self.barra.setValue(max(0, min(100, int(pct))))
        if not attivi:
            self.barra.setValue(100)
            self.barra.hide()
            self.b_scarica.setEnabled(True)
            self.timer.setInterval(self.intervallo_ms)
            self.toast(L("Download finito.", "Download finished."))
            self._giro = 0
            self._modelli(True)

    # ---- chat
    def _nuova_chat(self):
        self.msgs = []
        self.risposta.clear()
        self.r_velocita.setText("—")

    def _invia(self):
        q = self.domanda.text().strip()
        if not q:
            return
        if not self.attivo or not self.chiave:
            self.toast(L("Serve il motore acceso e la chiave.", "Needs the engine on and the key."))
            return
        modello = self.modello.currentText().strip()
        if not modello:
            self.toast(L("Scarica un modello prima.", "Download a model first."))
            return
        self.domanda.clear()
        self.msgs.append({"role": "user", "content": q})
        self.risposta.appendPlainText("> " + q)
        self.risposta.appendPlainText("…")
        self.b_invia.setEnabled(False)
        msgs = list(self.msgs)
        t0 = time.time()

        def chiama():
            # thinking off: a quick test wants the answer, not the reasoning
            r = studio("/v1/chat/completions", {"model": modello, "messages": msgs, "max_tokens": 512, "stream": False,
                                                "chat_template_kwargs": {"enable_thinking": False}},
                       key=self.chiave, t=600)
            return {"r": r, "s": time.time() - t0}
        in_sfondo(chiama, self._risposta_arrivata, self)

    def _risposta_arrivata(self, out):
        self.b_invia.setEnabled(True)
        r = out.get("r") or {}
        testo = ""
        try:
            msg = r["choices"][0]["message"]
            testo = msg.get("content") or msg.get("reasoning_content") or ""
        except (KeyError, IndexError, TypeError):
            testo = (r.get("error") or {}).get("message") if isinstance(r.get("error"), dict) else (r.get("detail") or L("nessuna risposta", "no reply"))
            self.msgs.pop()
        else:
            self.msgs.append({"role": "assistant", "content": testo})
        # replace the waiting marker with the reply
        cur = self.risposta.textCursor()
        cur.movePosition(QTextCursor.MoveOperation.End)
        cur.select(QTextCursor.SelectionType.LineUnderCursor)
        cur.removeSelectedText()
        cur.insertText(testo.strip())
        self.risposta.appendPlainText("")
        uso = r.get("usage") or {}
        n = uso.get("completion_tokens")
        s = out.get("s") or 0
        if n and s:
            self.r_velocita.setText("%d token · %.0f tok/s · %.1f s" % (n, n / s, s))
        elif s:
            self.r_velocita.setText("%.1f s" % s)

    # ---- network
    def _rete(self):
        r = self.demone.cmd(cmd="unsloth-conf-set", lan=self.lan.isChecked(), parallel=self.slot.value())
        if not r.get("ok"):
            self.toast(r.get("err") or L("non riuscito", "failed"))
            return
        self._rete_leggi()
        self.toast(L("Applicato; il motore e' stato riavviato se era acceso.", "Applied; the engine was restarted if it was on."))

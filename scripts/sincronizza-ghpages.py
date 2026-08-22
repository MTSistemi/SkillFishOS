# -*- coding: utf-8 -*-
"""Porta l'archivio apt del container sul ramo gh-pages di GitHub.

PERCHE' SERVE
skillfish-rilascio pubblica su skillfishos.com/apt, ma NON su GitHub Pages, e
la sorgente apt dentro le ISO punta proprio a mtsistemi.github.io. Senza questo
passaggio si costruirebbero immagini che scaricano ancora i pacchetti vecchi:
verificato oggi, skillfishos.com era a 26.08.24 e Pages fermo a 26.08.23.

⚠️ NIENTE TAR. La nota in memoria dice che pubblicare i .deb passando dal tar
di Git Bash rompe i percorsi e ha gia' svuotato gh-pages una volta. Qui i file
si copiano uno per uno con SFTP e si committano con git: l'archivio e' di 36
file per 25 MB, non vale la pena rischiare per risparmiare qualche secondo.
"""
import io
import re
import os
import shutil
import stat
import tempfile
import subprocess
import sys

import paramiko


# --- le credenziali del container, da FUORI il repository -------------------
# ⚠️ Qui c'era la password scritta in chiaro, ed e' finita su un repository
# PUBBLICO (16/08/2026, commit 1655aa3). Adesso si legge da
# ~/.skillfishos/deploy.env, che e' lo stesso posto delle credenziali OVH e non
# e' mai stato dentro al repository.
#
# Non si mette un valore predefinito: un ripiego silenzioso qui vorrebbe dire
# rimettere una password nel codice fra sei mesi, quando qualcuno lo trovera'
# comodo.
def _credenziali():
    percorso = os.path.join(os.path.expanduser("~"), ".skillfishos", "deploy.env")
    valori = {}
    try:
        with io.open(percorso, encoding="utf-8") as f:
            for riga in f:
                riga = riga.strip()
                if not riga or riga.startswith("#") or "=" not in riga:
                    continue
                k, _, v = riga.partition("=")
                valori[k.strip()] = v.strip().strip('"').strip("'")
    except IOError:
        pass
    manca = [k for k in ("APT_HOST", "APT_USER", "APT_PASS") if not valori.get(k)]
    if manca:
        sys.exit(
            "manca %s in %s\n"
            "   Aggiungi queste righe (il file NON sta nel repository):\n"
            "      APT_HOST=192.168.5.103\n"
            "      APT_USER=root\n"
            "      APT_PASS=<la password del container>"
            % (", ".join(manca), percorso))
    return valori["APT_HOST"], valori["APT_USER"], valori["APT_PASS"]


APT_HOST, APT_USER, APT_PASS = _credenziali()

QUI = os.path.dirname(os.path.abspath(__file__))

# ⚠️ SI LAVORA FUORI DA DROPBOX. Questo script sta dentro una cartella
# sincronizzata, e Dropbox tiene aperti i file mentre li indicizza: la
# cancellazione dell'albero fallisce, `ignore_errors=True` la fa fallire in
# SILENZIO, e la copia successiva muore con "il file esiste gia'". E' lo stesso
# motivo per cui il sito si costruisce in C:\sfweb e non nel repository.
LAVORO = os.path.join(tempfile.gettempdir(), "skillfishos-ghpages")
SCARICO = os.path.join(LAVORO, "apt-nuovo")
CLONE = os.path.join(LAVORO, "gh-pages")
REPO = "https://github.com/MTSistemi/SkillFishOS.git"


def butta(percorso):
    """Cancella un albero anche quando Windows fa i capricci.

    git lascia gli oggetti in sola lettura e Windows si rifiuta di cancellarli;
    `shutil.rmtree(ignore_errors=True)` non protesta e lascia mezzo albero al
    suo posto. Qui si toglie la sola lettura e si riprova, e se proprio non si
    riesce lo si dice invece di andare avanti su una cartella sporca.
    """
    def riprova(funzione, p, _):
        os.chmod(p, stat.S_IWRITE)
        funzione(p)
    if not os.path.exists(percorso):
        return
    shutil.rmtree(percorso, onerror=riprova)
    if os.path.exists(percorso):
        sys.exit("   non riesco a cancellare %s: chiudi i programmi che lo tengono aperto" % percorso)

# ⚠️ La versione si passa da fuori. Prima era scritta dentro, in due punti: il
# controllo di sicurezza e il messaggio di commit. Al rilascio dopo il controllo
# fermava tutto per la versione sbagliata, e il messaggio avrebbe raccontato la
# storia del rilascio precedente.
#     python sincronizza-ghpages.py 26.08.26
if len(sys.argv) < 2:
    sys.exit("uso: sincronizza-ghpages.py <versione>   (esempio: 26.08.26)")
VERSIONE = sys.argv[1]
# ⚠️ Due forme, ed e' giusto cosi': le nostre applicazioni si numerano
# 26.08.51, il meta-pacchetto del kernel usa la forma Debian 7.2.0-1. Prima
# passava solo la prima, e per pubblicare il kernel bisognava scavalcare questo
# controllo — cioe' togliere la rete di sicurezza nel rilascio piu' delicato.
if not re.match(r"^\d+\.\d+\.\d+(-\d+)?$", VERSIONE):
    sys.exit("versione non riconosciuta: %r (attesa tipo 26.08.26 oppure 7.2.0-1)" % VERSIONE)
print("   allineo GitHub Pages alla %s" % VERSIONE)


def scarica_ricorsivo(sftp, remoto, locale):
    """Copia una cartella remota intera, contando i file."""
    n = 0
    os.makedirs(locale, exist_ok=True)
    for voce in sftp.listdir_attr(remoto):
        r = remoto + "/" + voce.filename
        l = os.path.join(locale, voce.filename)
        if voce.st_mode is not None and (voce.st_mode & 0o40000):
            n += scarica_ricorsivo(sftp, r, l)
        else:
            sftp.get(r, l)
            n += 1
    return n


def git(*args, cwd=CLONE):
    r = subprocess.run(["git"] + list(args), cwd=cwd,
                       capture_output=True, text=True)
    if r.returncode != 0 and "nothing to commit" not in (r.stdout + r.stderr):
        print("   git %s -> %s" % (" ".join(args[:2]), (r.stderr or r.stdout).strip()[:200]))
    return r


# --- 1. l'archivio dal container --------------------------------------------
butta(SCARICO)
c = paramiko.SSHClient()
# Qui dentro viaggia la password del container. Accettare qualunque chiave
# dell'host significa consegnarla al primo che si mette in mezzo sulla rete:
# si controlla che sia quella conosciuta, e se non lo e' ci si ferma.
c.load_system_host_keys()
c.set_missing_host_key_policy(paramiko.RejectPolicy())
try:
    c.connect(APT_HOST, username=APT_USER, password=APT_PASS, timeout=40)
except paramiko.SSHException as e:
    sys.exit("   FERMO: la chiave host di %s non e' fra quelle conosciute (%s).\n"
             "   Collegati una volta a mano con «ssh %s@%s» per registrarla."
             % (APT_HOST, e, APT_USER, APT_HOST))
sf = c.open_sftp()
tot = 0
for cartella in ("dists", "pool"):
    tot += scarica_ricorsivo(sf, "/srv/apt/" + cartella,
                             os.path.join(SCARICO, cartella))
for chiave in ("skillfishos-archive-keyring.asc", "skillfishos-archive-keyring.gpg"):
    try:
        sf.get("/srv/apt/" + chiave, os.path.join(SCARICO, chiave))
        tot += 1
    except IOError:
        pass
sf.close()
c.close()
print("   scaricati dal container: %d file" % tot)

# --- 2. il ramo gh-pages ----------------------------------------------------
butta(CLONE)
tok = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()
if not tok:
    sys.exit("   niente token: non posso pubblicare")
url = REPO.replace("https://", "https://MTSistemi:%s@" % tok)
r = subprocess.run(["git", "clone", "--depth", "1", "--branch", "gh-pages", url, CLONE],
                   capture_output=True, text=True)
if r.returncode != 0:
    sys.exit("   clone fallito: " + (r.stderr or "")[:300])
print("   ramo gh-pages clonato")

# --- 3. sostituzione ---------------------------------------------------------
# Si sostituiscono SOLO dists e pool: index.html, .nojekyll e .gitattributes
# sono del sito, non dell'archivio, e vanno lasciati stare. (.nojekyll in
# particolare: senza, GitHub Pages ignora le cartelle che iniziano per underscore
# e l'archivio smetterebbe di funzionare.)
for cartella in ("dists", "pool"):
    butta(os.path.join(CLONE, cartella))
    shutil.copytree(os.path.join(SCARICO, cartella), os.path.join(CLONE, cartella))
for chiave in ("skillfishos-archive-keyring.asc", "skillfishos-archive-keyring.gpg"):
    s = os.path.join(SCARICO, chiave)
    if os.path.exists(s):
        shutil.copy2(s, os.path.join(CLONE, chiave))

rimasti = [n for n in (".nojekyll", "index.html", ".gitattributes")
           if os.path.exists(os.path.join(CLONE, n))]
print("   file del sito lasciati intatti: %s" % ", ".join(rimasti))

# --- 4. controllo PRIMA di pubblicare ---------------------------------------
pacchetti = []
for radice, _, files in os.walk(os.path.join(CLONE, "pool")):
    pacchetti += [f for f in files if f.endswith(".deb")]
# ⚠️ NON si cerca la versione in skillfish-base: da quando si pubblica solo
# cio' che cambia davvero, un rilascio puo' non toccarlo affatto (la 26.08.45
# ha cambiato il solo skillfish-hub). Si controlla invece che la versione ci
# sia in QUALCUNO dei nostri pacchetti e che l'albero non sia monco.
base = [p for p in pacchetti if p.startswith("skillfish-base_")]
con_versione = [p for p in pacchetti if ("_%s_" % VERSIONE) in p]
print("   pacchetti nell'albero: %d, alla %s: %s"
      % (len(pacchetti), VERSIONE, ", ".join(sorted(con_versione)) or "NESSUNO"))
if not base:
    sys.exit("   FERMO: nell'albero non c'e' skillfish-base, e' monco: non pubblico")
if len(pacchetti) < 10:
    sys.exit("   FERMO: solo %d pacchetti nell'albero, sembra monco: non pubblico"
             % len(pacchetti))
if not con_versione:
    sys.exit("   FERMO: nell'albero non c'e' nessun pacchetto alla %s.\n"
             "   Hai gia' fatto «skillfish-rilascio --pubblica» sul container?"
             % VERSIONE)

git("add", "-A")
git("-c", "user.name=SkillFishOS", "-c", "user.email=tadini@poloinformatico.it",
    "commit", "-m",
    "apt archive %s\n\n"
        "Brings GitHub Pages level with skillfishos.com/apt. Installed images\n"
        "point their apt source at this branch, so while it lags behind, users\n"
        "silently stop receiving fixes and new images are built with stale\n"
        "packages." % VERSIONE)
r = git("push", "origin", "gh-pages")
print("   " + ((r.stderr or r.stdout).strip().splitlines() or ["push eseguito"])[-1])

butta(SCARICO)
butta(CLONE)
print("   copie locali rimosse")

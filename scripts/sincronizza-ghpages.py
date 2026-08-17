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
import os
import shutil
import subprocess
import sys

import paramiko

QUI = os.path.dirname(os.path.abspath(__file__))
SCARICO = os.path.join(QUI, "apt-nuovo")
CLONE = os.path.join(QUI, "gh-pages")
REPO = "https://github.com/MTSistemi/SkillFishOS.git"

# ⚠️ La versione si passa da fuori. Prima era scritta dentro, in due punti: il
# controllo di sicurezza e il messaggio di commit. Al rilascio dopo il controllo
# fermava tutto per la versione sbagliata, e il messaggio avrebbe raccontato la
# storia del rilascio precedente.
#     python sincronizza-ghpages.py 26.08.26
if len(sys.argv) < 2:
    sys.exit("uso: sincronizza-ghpages.py <versione>   (esempio: 26.08.26)")
VERSIONE = sys.argv[1]
if not all(p.isdigit() for p in VERSIONE.split(".")) or VERSIONE.count(".") != 2:
    sys.exit("versione non riconosciuta: %r (attesa tipo 26.08.26)" % VERSIONE)
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
shutil.rmtree(SCARICO, ignore_errors=True)
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("192.168.5.103", username="root", password="47yk2d8r6c", timeout=40)
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
shutil.rmtree(CLONE, ignore_errors=True)
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
    shutil.rmtree(os.path.join(CLONE, cartella), ignore_errors=True)
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
base = [p for p in pacchetti if p.startswith("skillfish-base_")]
print("   pacchetti nell'albero: %d, fra cui %s" % (len(pacchetti), base or "NESSUN skillfish-base"))
if not base:
    sys.exit("   FERMO: nell'albero non c'e' skillfish-base, non pubblico")
if VERSIONE not in base[0]:
    sys.exit("   FERMO: mi aspettavo la %s e trovo %s, non pubblico"
             % (VERSIONE, base[0]))

git("add", "-A")
r = git("-c", "user.name=SkillFishOS", "-c", "user.email=tadini@poloinformatico.it",
        "commit", "-m",
        "apt archive %s\n\n"
        "Brings GitHub Pages level with skillfishos.com/apt. Installed images\n"
        "point their apt source at this branch, so while it lags behind, users\n"
        "silently stop receiving fixes and new images are built with stale\n"
        "packages." % VERSIONE)
r = git("push", "origin", "gh-pages")
print("   " + ((r.stderr or r.stdout).strip().splitlines() or ["push eseguito"])[-1])

shutil.rmtree(SCARICO, ignore_errors=True)
shutil.rmtree(CLONE, ignore_errors=True)
print("   copie locali rimosse")

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
import re
import shutil
import subprocess
import sys

import paramiko

QUI = os.path.dirname(os.path.abspath(__file__))
SCARICO = os.path.join(QUI, "apt-nuovo")
CLONE = os.path.join(QUI, "gh-pages")
REPO = "https://github.com/MTSistemi/SkillFishOS.git"


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


def versione_attesa(nomi, richiesta):
    """Quale versione ci aspettiamo di pubblicare, e perche' la si controlla.

    Il numero non sta piu' scritto dentro allo script: o lo si passa come
    argomento, o lo si deduce dai nomi dei .deb. In tutti e due i casi si
    pretende che nell'archivio ci sia UNA sola versione dei nostri pacchetti:
    due versioni mescolate vogliono dire un rilascio a meta', ed e' esattamente
    il caso da cui questa guardia deve proteggere.
    """
    viste = set()
    for n in nomi:
        m = re.match(r"skillfish[a-z-]*_([0-9][0-9.]*)_", n)
        if m and not m.group(1).startswith("7."):   # il kernel ha una sua numerazione
            viste.add(m.group(1))
    if not viste:
        sys.exit("   FERMO: nell'archivio non c'e' nessun pacchetto nostro")
    if len(viste) > 1:
        sys.exit("   FERMO: nell'archivio convivono piu' versioni (%s): rilascio a meta'"
                 % ", ".join(sorted(viste)))
    trovata = viste.pop()
    if richiesta and trovata != richiesta:
        sys.exit("   FERMO: chiesto %s ma nell'archivio c'e' %s" % (richiesta, trovata))
    return trovata


VER = versione_attesa(pacchetti, sys.argv[1] if len(sys.argv) > 1 else None)
if not base:
    sys.exit("   FERMO: manca skillfish-base, non pubblico")
print("   versione da pubblicare: %s" % VER)

git("add", "-A")
r = git("-c", "user.name=SkillFishOS", "-c", "user.email=tadini@poloinformatico.it",
        "commit", "-m",
        "Archivio apt %s\n\n"
        "Allinea GitHub Pages a skillfishos.com/apt. Le ISO scaricano da qui,\n"
        "quindi finche' questo ramo resta indietro si costruiscono immagini\n"
        "con i pacchetti vecchi." % VER)
r = git("push", "origin", "gh-pages")
print("   " + ((r.stderr or r.stdout).strip().splitlines() or ["push eseguito"])[-1])

shutil.rmtree(SCARICO, ignore_errors=True)
shutil.rmtree(CLONE, ignore_errors=True)
print("   copie locali rimosse")

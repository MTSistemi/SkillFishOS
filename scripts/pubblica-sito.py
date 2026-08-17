# -*- coding: utf-8 -*-
u"""Pubblica il sito costruito su OVH, via SFTP.

⚠️ PRIMA di questo va lanciato C:\\sfweb\\build.ps1, non "npm run build" a mano:
dentro Dropbox il filtro dei file mangia parte della cartella prodotta e il sito
finisce online senza CSS. build.ps1 costruisce fuori da Dropbox
(%TEMP%\\skillfishos-website-dist) proprio per questo.

⚠️ QUESTO SCRIPT NON CANCELLA NIENTE sul server. Caricare e' sicuro, cancellare
no: un errore di percorso qui svuoterebbe il sito. Quando qualcosa va tolto
davvero, lo si toglie a mano sapendo cosa si sta facendo.

Alla fine si controlla quello che vede un visitatore: la pagina, il CSS e una
pagina per ogni lingua. Un caricamento andato a buon fine non e' la stessa cosa
di un sito che funziona.
"""
import os
import pathlib
import posixpath
import sys
import urllib.request

import paramiko

DIST = pathlib.Path(os.environ.get("TEMP", "/tmp")) / "skillfishos-website-dist"
CRED = pathlib.Path(os.path.expanduser("~")) / ".skillfishos" / "deploy.env"

if not DIST.is_dir():
    sys.exit("non trovo la cartella costruita: %s\nlancia prima C:\\sfweb\\build.ps1" % DIST)

# controllo di sanita': se il CSS non c'e', la costruzione e' monca e caricarla
# vorrebbe dire mettere online un sito senza grafica.
css = list((DIST / "_astro").glob("*.css")) if (DIST / "_astro").is_dir() else []
html = list(DIST.rglob("*.html"))
print("   da caricare: %d pagine, %d fogli di stile" % (len(html), len(css)))
if not css or len(html) < 50:
    sys.exit("   costruzione incompleta: non pubblico")

dati = {}
for riga in CRED.read_text(encoding="utf-8").splitlines():
    riga = riga.strip()
    if "=" in riga and not riga.startswith("#"):
        k, v = riga.split("=", 1)
        dati[k.strip()] = v.strip()

host = dati.get("OVH_SFTP_HOST", "ssh.cluster129.hosting.ovh.net")
base = dati.get("OVH_FTP_DIR", "www").rstrip("/")
t = paramiko.Transport((host, 22))
t.connect(username=dati["OVH_FTP_USER"], password=dati["OVH_FTP_PASS"])
s = paramiko.SFTPClient.from_transport(t)
print("   collegato a %s, cartella %s" % (host, base))

fatte = set()


def assicura(d):
    """mkdir -p, ma via SFTP e senza chiedere due volte la stessa cartella"""
    if d in fatte or d in ("", ".", "/"):
        return
    assicura(posixpath.dirname(d))
    try:
        s.stat(d)
    except IOError:
        try:
            s.mkdir(d)
        except IOError:
            pass
    fatte.add(d)


caricati = saltati = 0
byte = 0
for p in sorted(DIST.rglob("*")):
    if p.is_dir():
        continue
    rel = p.relative_to(DIST).as_posix()
    remoto = base + "/" + rel
    dim = p.stat().st_size
    # se e' identico per dimensione e non piu' vecchio, si salta: sono oltre
    # duecento file e la linea verso OVH non e' veloce
    try:
        st = s.stat(remoto)
        if st.st_size == dim and st.st_mtime >= p.stat().st_mtime:
            saltati += 1
            continue
    except IOError:
        pass
    assicura(posixpath.dirname(remoto))
    s.put(str(p), remoto)
    caricati += 1
    byte += dim

print("   caricati %d file (%.1f MB), gia' aggiornati %d" % (caricati, byte / 1e6, saltati))
s.close()
t.close()

# --- e adesso quello che vede un visitatore ---------------------------------
print("\n   controllo dal vivo:")
prove = ["https://skillfishos.com/",
         "https://skillfishos.com/news",
         "https://skillfishos.com/en/news",
         "https://skillfishos.com/pl/news",
         "https://skillfishos.com/uk/news",
         "https://skillfishos.com/gallery",
         "https://skillfishos.com/download"]
prove += ["https://skillfishos.com/_astro/" + c.name for c in css]
guasti = 0
for u in prove:
    try:
        r = urllib.request.urlopen(urllib.request.Request(
            u, headers={"User-Agent": "SkillFishOS-deploy"}), timeout=20)
        code, n = r.getcode(), len(r.read())
    except Exception as e:
        code, n = getattr(e, "code", 0), 0
    if code != 200:
        guasti += 1
    print("     %-3s %8d  %s" % (code or "err", n, u.replace("https://skillfishos.com", "")or "/"))
sys.exit(1 if guasti else 0)

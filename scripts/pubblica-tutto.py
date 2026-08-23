# -*- coding: utf-8 -*-
u"""Pubblica su TUTTI i mirror con un comando solo, e verifica che siano pari.

PERCHE' ESISTE. I mirror erano due e si pubblicavano con due comandi diversi:
`skillfish-rilascio --pubblica` sul container per OVH, e
`scripts/sincronizza-ghpages.py` da Windows per GitHub Pages. Finche' i client
usavano un mirror solo, dimenticarne uno era disordine. Da quando apt prova
tutti i mirror a turno, la divergenza diventa un ERRORE IN FACCIA ALL'UTENTE:
se un mirror serve un Release piu' vecchio di quello gia' in cache, apt lo
rifiuta e l'aggiornamento si pianta.

PERCHE' GIRA DA WINDOWS E NON SUL CONTAINER. Il container ha la chiave di firma
dell'archivio; il token di GitHub ce l'ha solo questa macchina. Mettere il token
anche sul container vorrebbe dire una credenziale in piu' da custodire, per non
guadagnare niente: da qui si raggiungono tutti e due i pezzi.

⚠️ NON DICE «FATTO» SENZA AVER GUARDATO. Alla fine scarica il Release da tutti i
mirror e confronta l'impronta. Se non combaciano lo dice e esce male: un
comando che dichiara successo senza verificare e' esattamente come ci siamo
ritrovati con due mirror disallineati.
"""
from __future__ import unicode_literals, print_function
import hashlib
import io
import os
import subprocess
import sys
import time
import urllib.request

CONTAINER = "192.168.5.210"
IMPRONTA = "SHA256:+jpokXzLD6d6Stn/FPyuStdtZWOrcS3gS3XkpEWvqA4"
PW = "47yk2d8r6c"
QUI = os.path.dirname(os.path.abspath(__file__))

# ⚠️ L'ORDINE E' QUELLO CHE VEDONO I CLIENT: OVH per primo, che e' nostro.
MIRROR = [
    ("OVH", "https://skillfishos.com/apt"),
    ("GitHub Pages", "https://mtsistemi.github.io/SkillFishOS"),
    ("casa", "https://deb.skillfishos.com"),
]


def sul_container(comando):
    return subprocess.run(["plink", "-batch", "-hostkey", IMPRONTA, "-pw", PW,
                           "root@" + CONTAINER, comando],
                          capture_output=True, text=True)


def impronta_release(base):
    u"""Il Release di un mirror, in impronta. None se non risponde."""
    try:
        with urllib.request.urlopen(base + "/dists/aetherium/Release", timeout=25) as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        print("      %s: %s" % (base, e))
        return None


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: pubblica-tutto.py <versione>   (esempio: 26.08.55)")
    versione = sys.argv[1]

    print("=== 1. OVH, dal container ===")
    r = sul_container("skillfish-rilascio --pubblica")
    coda = (r.stdout or r.stderr).strip().split("\n")
    for riga in coda[-6:]:
        print("   " + riga)
    if r.returncode != 0:
        sys.exit("   !! il rilascio su OVH e' fallito, non proseguo")

    print()
    print("=== 2. GitHub Pages, da qui ===")
    sinc = os.path.join(QUI, "sincronizza-ghpages.py")
    if not os.path.exists(sinc):
        sys.exit("   !! manca %s" % sinc)
    r = subprocess.run([sys.executable, "-u", sinc, versione], capture_output=True, text=True)
    for riga in (r.stdout or r.stderr).strip().split("\n")[-8:]:
        print("   " + riga)
    if r.returncode != 0:
        sys.exit("   !! la sincronizzazione con Pages e' fallita")

    print()
    print("=== 3. sono davvero pari? ===")
    # Pages ci mette un momento a servire il commit nuovo: si aspetta, ma non
    # all'infinito. Meglio dire «non combaciano» che dire «fatto» sperandoci.
    for tentativo in range(6):
        if tentativo:
            time.sleep(20)
        impronte = [(nome, impronta_release(url)) for nome, url in MIRROR]
        for nome, imp in impronte:
            print("   %-14s %s" % (nome, (imp or "non risponde")[:16]))
        valori = set(i for _, i in impronte if i)
        if len(valori) == 1 and all(i for _, i in impronte):
            print()
            print("   TUTTI PARI: %d mirror, stesso Release." % len(MIRROR))
            return 0
        if tentativo < 5:
            print("   ...non ancora, riprovo fra 20 secondi")
    print()
    print("   !! I MIRROR NON COMBACIANO.")
    print("      Con il ripiego attivo un client puo' prendere il Release vecchio")
    print("      da un mirror e vedersi rifiutare l'aggiornamento. Va sistemato")
    print("      prima di considerare pubblicata questa versione.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

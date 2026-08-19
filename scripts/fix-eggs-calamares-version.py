#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Fa mostrare a Calamares la VERSIONE DEL RILASCIO invece della data di build.
Corregge anche il nome della voce del bootloader.

   fix-eggs-calamares-version.py 26.06.5

⚠️ LA VERSIONE SI PASSA DA FUORI. Prima stava scritta dentro in due posti - qui
come '26.06' e nei branding.desc come '26.06.4' - e nessuno dei due era legato
alla ISO che si stava costruendo. Risultato: la 26.06.5 prodotta il 19/08/2026
presentava l'installatore come "SkillFishOS 26.06.4 Aetherium". Un utente che
prova l'immagine nuova legge il numero vecchio e non ha modo di accorgersi che
sta guardando la cosa giusta.

Adesso build-iso.sh ricava il numero dal nome del file .iso e lo passa qui, cosi'
non c'e' un secondo posto da ricordarsi di aggiornare.
"""
import os
import re
import shutil
import sys

if len(sys.argv) < 2:
    sys.exit("uso: fix-eggs-calamares-version.py <versione>   (esempio: 26.06.5)")
VER = sys.argv[1]
if not re.match(r"^\d+\.\d+(\.\d+)?$", VER):
    sys.exit("versione non riconosciuta: %r (attesa tipo 26.06.5)" % VER)
NOME = "SkillFishOS %s Aetherium" % VER
print("   versione da mostrare: %s" % NOME)

# --- 1. il generatore di eggs ------------------------------------------------
f = "/usr/lib/penguins-eggs/dist/classes/incubation/branding.js"
if os.path.exists(f):
    with open(f, encoding="utf-8") as _f:
        s = _f.read()
    if not os.path.exists(f + ".skfbak"):
        shutil.copy(f, f + ".skfbak")
    # si riparte SEMPRE dall'originale: applicare la toppa su una gia' toppata
    # lascerebbe dentro la versione del rilascio precedente.
    with open(f + ".skfbak", encoding="utf-8") as _f:
        s = _f.read()
    reps = [
        ("const version = today.toISOString().split('T')[0]; // 2021-09-30",
         "const version = '%s'; // SkillFishOS release (was build date)" % VER),
        ("const shortVersion = version.split('-').join('.'); // 2021.09.30",
         "const shortVersion = '%s';" % VER),
        ("const versionedName = remix.fullname + ' (' + shortVersion + ')';",
         "const versionedName = remix.fullname + ' %s Aetherium';" % VER),
        ("const shortVersionedName = remix.versionName + ' ' + version;",
         "const shortVersionedName = remix.fullname + ' %s Aetherium';" % VER),
        ("bootloaderEntryName = 'Skillfishos';",
         "bootloaderEntryName = 'SkillFishOS';"),
    ]
    ok = True
    for a, b in reps:
        if a in s:
            s = s.replace(a, b)
        else:
            print("   MANCA nel sorgente di eggs: %s" % a[:55])
            ok = False
    with open(f, "w", encoding="utf-8") as _f:
        _f.write(s)
    print("   branding.js aggiornato (tutte le sostituzioni: %s)" % ok)
else:
    print("   ATTENZIONE: non trovo branding.js di eggs")

# --- 2. i branding.desc gia' generati ----------------------------------------
# eggs li scrive prima che questo script giri, quindi contengono ancora il
# numero del rilascio precedente. Si riscrivono qui, altrimenti l'installatore
# mostra il vecchio anche con branding.js corretto.
campi = {
    "shortVersion": VER,
    "version": VER,
    "shortVersionedName": NOME,
    "versionedName": NOME,
}
tocchi = 0
for radice, _, files in os.walk("/etc/calamares/branding"):
    for nome in files:
        if nome != "branding.desc":
            continue
        p = os.path.join(radice, nome)
        with open(p, encoding="utf-8") as _f:
            righe = _f.read().split("\n")
        cambiato = False
        for i, r in enumerate(righe):
            m = re.match(r"^(\s*)([A-Za-z]+):\s*(.*)$", r)
            if m and m.group(2) in campi:
                nuovo = "%s%s: %s" % (m.group(1), m.group(2), campi[m.group(2)])
                if righe[i] != nuovo:
                    righe[i] = nuovo
                    cambiato = True
        if cambiato:
            with open(p, "w", encoding="utf-8", newline="\n") as _f:
                _f.write("\n".join(righe))
            tocchi += 1
            print("   aggiornato %s" % p)
print("   branding.desc aggiornati: %d" % tocchi)

# -*- coding: utf-8 -*-
u"""I pulsanti di download offrono la stessa release che la pagina annuncia?

PERCHE' ESISTE. Il 15/09/2026 Mattia: «sul sito i link di download puntano
ancora alla 26.06.4 e abbiamo rilasciato la 26.06.5». Aveva ragione, ed erano
tre giorni che era cosi'.

Il giro di aggiornamento aveva spostato tutto quello che si LEGGE: i testi nelle
nove lingue, le tre URL in i18n.ts, la dimensione, le nove installazione.md, i
torrent, i magnet, la voce di news. Non aveva spostato quello che si CLICCA.
Ogni pulsante passa da /go.php?f=..., e li' dentro c'erano ancora gli indirizzi
della release precedente.

⚠️ Il punto da ricordare: cercare il numero di versione nei sorgenti risponde
alla domanda «lo diciamo?», non alla domanda «lo consegniamo?». Sono due
domande diverse e quel giorno avevano due risposte diverse.

COSA CONTROLLA. Solo coerenza interna, senza rete, cosi' gira in un secondo su
ogni pull request:
  1. go.php offre la stessa versione che i18n.ts annuncia;
  2. dentro go.php non ci sono due versioni diverse mescolate;
  3. i .torrent che go.php offre esistono davvero in public/torrent;
  4. in .htaccess il collegamento breve SENZA numero (che vuol dire «quella di
     adesso») porta alla versione corrente.

⚠️ NON controlla i collegamenti brevi che SCRIVONO un numero di versione:
quelli devono continuare a consegnare la versione che nominano, anche vecchia.
Sostituirla di nascosto sarebbe peggio di un link datato.

Uso:
    python3 scripts/controlla-pulsanti.py
"""
from __future__ import unicode_literals, print_function

import io
import os
import re
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITO = os.path.join(RADICE, "website")

VERSIONE = re.compile(r"files/(\d+\.\d+\.\d+)-Aetherium")


def leggi(*pezzi):
    p = os.path.join(SITO, *pezzi)
    if not os.path.isfile(p):
        return None
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def controlla():
    guai = []

    i18n = leggi("src", "i18n.ts")
    go = leggi("public", "go.php")
    htaccess = leggi("public", ".htaccess")

    if i18n is None or go is None:
        return ["Non trovo website/src/i18n.ts o website/public/go.php: "
                "controllo saltato, non fallito."]

    # --- 1. la versione annunciata e quella consegnata ----------------------
    annunciate = VERSIONE.findall(i18n)
    if not annunciate:
        return ["i18n.ts non nomina nessuna release su SourceForge: "
                "controllo saltato, non fallito."]
    if len(set(annunciate)) > 1:
        guai.append("**i18n.ts** nomina piu' di una release: %s."
                    % ", ".join(sorted(set(annunciate))))
    annunciata = annunciate[0]

    consegnate = set(VERSIONE.findall(go))
    if not consegnate:
        guai.append("**go.php** non nomina nessuna release su SourceForge.")
    elif consegnate != {annunciata}:
        guai.append("**go.php** manda alla %s, ma la pagina annuncia la %s. "
                    "I pulsanti passano tutti da go.php, quindi il sito "
                    "annuncia una release e ne consegna un'altra."
                    % (", ".join(sorted(consegnate)), annunciata))

    # --- 2. dentro go.php una versione sola --------------------------------
    nei_nomi = set(re.findall(r"SkillFishOS-(\d+\.\d+\.\d+)-Aetherium", go))
    nelle_note = set(re.findall(r"RELEASE-NOTES-(\d+\.\d+\.\d+)\.md", go))
    mescolate = (nei_nomi | nelle_note) - {annunciata}
    if mescolate:
        guai.append("**go.php** contiene ancora nomi di file della %s mentre "
                    "annuncia la %s." % (", ".join(sorted(mescolate)), annunciata))

    # --- 3. i torrent che offriamo devono esistere -------------------------
    # ⚠️ Il 15/09/2026 i .torrent della 26.06.5 stavano sul server ma NON nel
    # repository: chi avesse ripubblicato da un clone pulito avrebbe messo
    # online due link a file inesistenti, e il sito non se ne sarebbe accorto.
    for nome in re.findall(r"/torrent/([A-Za-z0-9._-]+\.torrent)", go):
        if not os.path.isfile(os.path.join(SITO, "public", "torrent", nome)):
            guai.append("**go.php** offre `%s`, che non esiste in "
                        "website/public/torrent." % nome)

    # --- 4. il collegamento breve senza numero -----------------------------
    if htaccess:
        for riga in htaccess.split("\n"):
            if "dl/SkillFishOS-26" in riga and "RewriteRule" in riga:
                # il collegamento SENZA numero di versione: ^dl/SkillFishOS-26\.06-Aetherium
                sinistra = riga.split()[1] if len(riga.split()) > 1 else ""
                if re.search(r"SkillFishOS-26\\\.06-Aetherium", sinistra):
                    dove = VERSIONE.search(riga)
                    if dove and dove.group(1) != annunciata:
                        guai.append("**.htaccess**: il collegamento breve senza "
                                    "numero porta alla %s, ma quella corrente "
                                    "e' la %s." % (dove.group(1), annunciata))

    return guai


def main():
    guai = controlla()
    if not guai:
        print("I pulsanti consegnano la release che la pagina annuncia.")
        return 0
    print("Trovate %d incoerenze fra quello che il sito dice e quello che da':\n"
          % len(guai))
    for g in guai:
        print(" - " + g.replace("**", ""))
    return 1


if __name__ == "__main__":
    sys.exit(main())

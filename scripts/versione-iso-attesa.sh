#!/bin/bash
# Which number the next image must carry.
#
#     versione-iso-attesa.sh          stampa il numero atteso, es. 26.06.5
#     versione-iso-attesa.sh --ultima stampa l'ultima pubblicata, es. 26.06.4
#
# ⚠️ LA FONTE E' SOURCEFORGE, NON IL DISCO. Il numero di una ISO e' +1
# sull'ultima PUBBLICATA, non sull'ultima costruita: sul disco di sviluppo
# restano immagini di prova con numeri alti, e scegliere il primo nome libero
# fa saltare una versione a chi scarica e lascia noi con due immagini diverse
# che si chiamano uguale.
#
# Il commento in iso/build.sh diceva gia' questa regola e non e' bastato: nel
# settembre 2026 sono uscite due immagini 26.06.6 mentre su SourceForge c'era
# la 26.06.4. Per questo adesso e' un controllo e non una frase.
set -u

RSS="${SKILLFISH_SF_RSS:-https://sourceforge.net/projects/skillfishos/rss?path=/}"

ultima() {
    curl -sfL --max-time 25 "$RSS" \
        | grep -oE 'SkillFishOS-[0-9]+\.[0-9]+\.[0-9]+-Aetherium-' \
        | sed -E 's/^SkillFishOS-//; s/-Aetherium-$//' \
        | sort -V | tail -1
}

U=$(ultima)
if [ -z "$U" ]; then
    echo "non riesco a leggere le versioni pubblicate da $RSS" >&2
    exit 1
fi

if [ "${1:-}" = "--ultima" ]; then
    printf '%s\n' "$U"
    exit 0
fi

# +1 sull'ultima cifra. Il resto del numero non si tocca: 26.06 e' il nome del
# rilascio, non una data da aggiornare.
TESTA="${U%.*}"
CODA="${U##*.}"
printf '%s.%s\n' "$TESTA" "$((CODA + 1))"

#!/bin/bash
# Prova il blocco che ritira le righe del vecchio rilevatore, sui tre casi che
# capitano davvero. Gira in una cartella temporanea: non tocca il sistema.
#
# ⚠️ Il caso che conta e' il secondo. Se il filtro fosse sbagliato, a chi ha
# avuto una piantata VERA gliela porteremmo via insieme a quelle finte, e non
# se ne accorgerebbe nessuno: il numero scende, e un numero che scende sembra
# sempre una buona notizia.
set -u
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT

VECCHIA1='2026-07-14T10:54:52+02:00 unclean-shutdown cpu=frequency=3500 gpu_max=1500MHz'
VECCHIA2='2026-07-30T11:12:41+02:00 unclean-shutdown cpu=frequency=3500 gpu_max=1500MHz'
NUOVA='2026-08-25T09:01:00+02:00 unclean-shutdown profile=bc250 cpu=3700 gpu_max=2230MHz'

ritira() {   # la stessa logica del postinst, con i percorsi nella cartella di prova
    FRZLOG="$T/freeze.log"
    FRZOLD="$T/freeze.log.vecchio"
    FRZMARK="$T/marca"
    if [ ! -e "$FRZMARK" ]; then
        if [ -f "$FRZLOG" ] && grep -q "unclean-shutdown cpu=" "$FRZLOG" 2>/dev/null; then
            grep "unclean-shutdown cpu=" "$FRZLOG" >> "$FRZOLD" 2>/dev/null || true
            grep -v "unclean-shutdown cpu=" "$FRZLOG" > "$FRZLOG.nuovo" 2>/dev/null || true
            mv "$FRZLOG.nuovo" "$FRZLOG" 2>/dev/null || true
        fi
        : > "$FRZMARK"
    fi
}

esito() {  # esito <atteso-nel-log> <atteso-da-parte> <nome>
    a=$( { wc -l < "$T/freeze.log"; } 2>/dev/null | tr -d ' '); a=${a:-0}
    b=$( { wc -l < "$T/freeze.log.vecchio"; } 2>/dev/null | tr -d ' '); b=${b:-0}
    if [ "$a" = "$1" ] && [ "$b" = "$2" ]; then
        echo "  OK   $3  (nel log $a, da parte $b)"
    else
        echo "  FAIL $3  (nel log $a atteso $1, da parte $b atteso $2)"
        ESITO=1
    fi
}

ESITO=0

echo "1. solo righe vecchie: devono sparire tutte dal log"
rm -f "$T"/freeze.log* "$T/marca"
printf '%s\n%s\n' "$VECCHIA1" "$VECCHIA2" > "$T/freeze.log"
ritira
esito 0 2 "tutte e due spostate, log vuoto"

echo "2. vecchie E una vera: la vera DEVE restare"
rm -f "$T"/freeze.log* "$T/marca"
printf '%s\n%s\n%s\n' "$VECCHIA1" "$NUOVA" "$VECCHIA2" > "$T/freeze.log"
ritira
esito 1 2 "resta solo quella del rilevatore nuovo"
grep -q 'profile=bc250' "$T/freeze.log" \
    && echo "  OK   la riga rimasta e' proprio quella vera" \
    || { echo "  FAIL la riga rimasta non e' quella vera"; ESITO=1; }

echo "3. gia' fatto una volta: non si tocca piu' niente"
rm -f "$T"/freeze.log* ; : > "$T/marca"
printf '%s\n%s\n' "$VECCHIA1" "$VECCHIA2" > "$T/freeze.log"
ritira
esito 2 0 "il log resta com'era"

echo "4. nessun registro: non deve dare errore"
rm -f "$T"/freeze.log* "$T/marca"
ritira
[ -e "$T/marca" ] && echo "  OK   segno scritto lo stesso, non si ritenta a ogni aggiornamento" \
                  || { echo "  FAIL segno non scritto"; ESITO=1; }

exit $ESITO

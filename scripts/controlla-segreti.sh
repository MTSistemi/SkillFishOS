#!/bin/bash
# Cerca credenziali nei file che stanno per uscire di casa.
#
# PERCHE' ESISTE
# Il 16/08/2026 la password di root del container e' finita su GitHub, che e'
# un repository PUBBLICO, dentro a scripts/sincronizza-ghpages.py. Ci e' restata
# quattro giorni. Non l'ha vista nessuno perche' non guardava nessuno: CodeQL
# cerca difetti nel codice, e il rilevamento automatico di GitHub riconosce i
# FORMATI noti dei token (ghp_, chiavi AWS) — una password qualunque no.
#
# ⚠️ QUESTO FILE NON CONTIENE NESSUN SEGRETO, e non deve mai contenerne.
# Il rilevatore che c'era in slim-iso.sh cercava la password vera, quindi la
# conteneva: era lui stesso una fuga, e per giunta non avrebbe trovato uno
# script con una password DIVERSA. Qui si cerca la FORMA di una credenziale.
#
#   uso:  scripts/controlla-segreti.sh            tutto l'albero tracciato
#         scripts/controlla-segreti.sh --da-spedire   solo cio' che non e' su origin
set -u
cd "$(dirname "$0")/.."

# Le forme. Niente valori, solo strutture.
#   password="…"            una password scritta a mano (con le virgolette:
#                           password=VARIABILE non ha virgolette e va bene)
#                           ⚠️ nell'esempio qui sopra i puntini sono UN carattere
#                           apposta: la forma vuole almeno sei caratteri fra le
#                           virgolette, quindi questa riga non segnala se stessa.
#                           Con «qualcosa» al posto dei puntini, l'hook bloccava
#                           il push per colpa della propria documentazione.
#   sshpass                 il modo classico di passare una password a ssh
#   BEGIN ... PRIVATE KEY   una chiave privata
#   ghp_ / github_pat_      i token di GitHub
#   AKIA...                 le chiavi AWS
# ⚠️ Il valore deve essere un LETTERALE: subito dopo l'uguale una virgoletta,
# poi caratteri che NON sono ne' $ (una variabile) ne' / (un percorso) ne' <
# (un segnaposto). `password=VARIABILE` non ha virgolette e va benissimo — e'
# esattamente cio' che vogliamo che il codice faccia.
FORME='(password|passwd|passphrase)[[:space:]]*=[[:space:]]*["'"'"'][^"'"'"'$/<][^"'"'"']{5,}["'"'"']|sshpass[[:space:]]+-p|BEGIN [A-Z ]*PRIVATE KEY|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}'

# Cosa NON e' un segreto anche se ci assomiglia: i segnaposto nei messaggi di
# aiuto, e gli esempi nella documentazione.
# Cosa NON e' un segreto anche se ci assomiglia:
#   - i segnaposto nei messaggi di aiuto
#   - le righe che CERCANO le password (questo file, e il filtro di slim-iso):
#     un rilevatore che segnala gli altri rilevatori non serve a niente
#   - /etc/passwd, che e' un file
#   - le stringhe CONCATENATE: `"...&password=" + variabile` costruisce un URL,
#     e il valore non e' nel file. Si riconoscono dal + attaccato a una
#     virgoletta (visto in apps/dashboard/web/app.js, che compone l'indirizzo
#     del KVM).
INNOCUI='<la password|<password>|LA-TUA-PASSWORD|esempio|example|xxxxx|\*\*\*\*|grep|etc/passwd|FORME=|INNOCUI=|"[[:space:]]*\+|\+[[:space:]]*"'

# ⚠️ iso/chroot e iso/cache sono copie del sistema costruito, non roba nostra:
# contengono migliaia di file di terze parti e non finiscono nel repository.
ESCLUSI=(':!iso/chroot' ':!iso/cache' ':!*.iso' ':!*.deb' ':!*.png' ':!*.jpg' ':!*.woff2')

if [ "${1:-}" = "--da-spedire" ]; then
    BASE=$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || echo "")
    if [ -z "$BASE" ]; then
        echo "nessun ramo remoto: controllo tutto l'albero"
        TROVATE=$(git grep -nEI "$FORME" -- . "${ESCLUSI[@]}" 2>/dev/null || true)
    else
        echo "controllo solo cio' che non e' ancora su $BASE"
        TROVATE=$(git diff -U0 "$BASE"..HEAD -- . "${ESCLUSI[@]}" 2>/dev/null \
                  | grep '^+' | grep -vE '^\+\+\+' | grep -nEI "$FORME" || true)
    fi
else
    TROVATE=$(git grep -nEI "$FORME" -- . "${ESCLUSI[@]}" 2>/dev/null || true)
fi

# via i segnaposto
TROVATE=$(printf '%s\n' "$TROVATE" | grep -vEi "$INNOCUI" | grep -v '^$' || true)

if [ -n "$TROVATE" ]; then
    echo
    echo "⚠️  CREDENZIALI TROVATE — non spedire:"
    printf '%s\n' "$TROVATE" | cut -c1-140 | sed 's/^/   /'
    echo
    echo "   Le credenziali vanno in ~/.skillfishos/deploy.env, che sta FUORI dal"
    echo "   repository, e si leggono da li' (vedi scripts/sincronizza-ghpages.py)."
    exit 1
fi

echo "nessuna credenziale nei file: si puo' spedire"
exit 0

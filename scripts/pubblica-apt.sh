#!/bin/bash
# Send .deb files to the archive container, sign them into the archive and
# publish, without going through anybody's laptop.
#
#     pubblica-apt.sh <file.deb> [altri.deb ...]
#     pubblica-apt.sh --solo-locale <file.deb ...>   mette in archivio e si ferma
#
# ⚠️ LE DUE META' SONO SEPARATE APPOSTA. `skillfish-rilascio <deb>` firma e
# indicizza ma tiene tutto nel container; `--pubblica` e' il gesto che lo manda
# fuori, su skillfishos.com e sul mirror. Chi vuole guardare prima di spedire
# usa --solo-locale.
#
# ⚠️ E GITHUB PAGES NON LO AGGIORNA QUESTO. Le ISO e i sistemi installati
# scaricano da mtsistemi.github.io: dopo questo si lancia
# scripts/sincronizza-ghpages.py <versione>.
set -u
CONTAINER="${SKILLFISH_APT:-root@192.168.5.210}"
SOLO_LOCALE=0
if [ "${1:-}" = "--solo-locale" ]; then SOLO_LOCALE=1; shift; fi
[ $# -gt 0 ] || { echo "uso: $0 [--solo-locale] <file.deb> [...]" >&2; exit 2; }

for f in "$@"; do
    [ -f "$f" ] || { echo "non trovo $f" >&2; exit 1; }
done

echo ">>> copio $# pacchetti in /srv/incoming"
scp -q -o StrictHostKeyChecking=accept-new "$@" "$CONTAINER:/srv/incoming/" || exit 1

# il confronto delle impronte: un pacchetto che arriva mezzo non deve entrare
IMPRONTE=$(md5sum "$@" | sed 's|[^ ]*/||')
REMOTI=$(ssh -o StrictHostKeyChecking=accept-new "$CONTAINER" "cd /srv/incoming && md5sum $(for f in "$@"; do printf '%q ' "$(basename "$f")"; done)")
if [ "$(printf '%s\n' "$IMPRONTE" | sort)" != "$(printf '%s\n' "$REMOTI" | sort)" ]; then
    echo "le impronte non coincidono: non pubblico" >&2
    exit 1
fi
echo "    impronte uguali"

NOMI=$(for f in "$@"; do printf '/srv/incoming/%s ' "$(basename "$f")"; done)
ssh "$CONTAINER" "skillfish-rilascio $NOMI" | grep -E "messo|errore|ERRORE" || true

if [ "$SOLO_LOCALE" = 1 ]; then
    echo ">>> resta nel container: http://192.168.5.210/apt"
    exit 0
fi
ssh "$CONTAINER" "skillfish-rilascio --pubblica" | grep -E "FATTO|mirror|errore|ERRORE" || true
echo ">>> ricorda GitHub Pages: scripts/sincronizza-ghpages.py <versione>"

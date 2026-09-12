#!/bin/bash
# Send the built website to OVH.
#
#     pubblica-sito.sh
#
# ⚠️ La stessa TMPDIR di costruisci-sito.sh, o si pubblica una cartella vuota:
# pubblica-sito.py cerca in os.tmpdir()/skillfishos-website-dist e su questa
# macchina il temporaneo sta nella home, non in /tmp (vedi costruisci-sito.sh).
set -u
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export TMPDIR="${SKILLFISH_TMPDIR:-$HOME/tmp}"
D="$TMPDIR/skillfishos-website-dist"
[ -d "$D" ] || { echo "non c'e' niente da pubblicare in $D: prima costruisci-sito.sh" >&2; exit 1; }
N=$(find "$D" -name '*.html' | wc -l)
[ "$N" -ge 50 ] || { echo "solo $N pagine in $D: non pubblico" >&2; exit 1; }
exec python3 "$SRC/scripts/pubblica-sito.py" "$@"

#!/bin/bash
# Build the website, and refuse to hand over a broken one.
#
#     costruisci-sito.sh            costruisce e conta cosa e' uscito
#     pubblica-sito.sh              lo manda su OVH (stessa TMPDIR, vedi sotto)
#
# ⚠️ PERCHE' CONTA I FILE. Una build che finisce con "Complete!" puo' lasciare
# un sito senza un solo foglio di stile: e' successo costruendo dalla copia
# Dropbox, dove i fine riga erano stati riscritti. Il numero di CSS e di
# immagini e' il controllo piu' economico che distingue un sito vero da uno
# monco, e sta qui e non nella testa di chi pubblica.
#
# ⚠️ TMPDIR NON E' UN DETTAGLIO. astro.config.mjs scrive in
# os.tmpdir()/skillfishos-website-dist. Sulla VM /tmp e' tmpfs, cioe' un altro
# filesystem rispetto a /home: Astro a fine build sposta i file con rename() e
# fra due filesystem rename() non funziona ("EXDEV: cross-device link not
# permitted"). Quindi qui TMPDIR viene portato dentro la home, e chi pubblica
# deve usare la stessa: lo fa pubblica-sito.sh, che sta accanto a questo.
set -u
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export TMPDIR="${SKILLFISH_TMPDIR:-$HOME/tmp}"
mkdir -p "$TMPDIR"
DIST="$TMPDIR/skillfishos-website-dist"

cd "$SRC/website" || exit 1
if [ ! -d node_modules ]; then
    echo ">>> npm ci"
    npm ci --no-audit --no-fund || npm install --no-audit --no-fund || exit 1
fi

rm -rf "$DIST"
echo ">>> astro build (TMPDIR=$TMPDIR)"
npx astro build || exit 1

HTML=$(find "$DIST" -name '*.html' | wc -l)
CSS=$(find "$DIST" -name '*.css' | wc -l)
IMG=$(find "$DIST" \( -name '*.png' -o -name '*.jpg' -o -name '*.svg' -o -name '*.webp' \) | wc -l)
printf '[costruisci-sito] %s HTML, %s CSS, %s immagini in %s\n' "$HTML" "$CSS" "$IMG" "$DIST"
if [ "$HTML" -lt 50 ] || [ "$CSS" -lt 1 ] || [ "$IMG" -lt 1 ]; then
    echo "[costruisci-sito] NON pubblicare: il sito e' monco" >&2
    exit 1
fi
echo "[costruisci-sito] ok, si pubblica con scripts/pubblica-sito.sh"

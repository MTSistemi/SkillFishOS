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
# ⚠️ node_modules BEING THERE DOES NOT MEAN IT IS THE RIGHT ONE. This used to
# run npm ci only when the folder was missing, so on the VM, where it always
# exists, a Dependabot bump merged into package-lock.json never reached the
# build: on 21/09/2026, after PR #88 (astro 7.3.2 -> 7.3.3), the site was built
# and published with astro 7.3.1. The build said "Complete!" all the same.
#
# So the checksum of the lockfile that node_modules was installed from is kept
# inside node_modules, and npm ci runs again whenever it differs.
#
# No fallback to npm install: npm ci fails only when package-lock.json does not
# match package.json, and npm install would then quietly rewrite the lockfile
# and build something the repository does not describe.
LOCKSUM=$(sha256sum package-lock.json | cut -d' ' -f1)
if [ "$(cat node_modules/.skillfish-lock.sha256 2>/dev/null)" != "$LOCKSUM" ]; then
    echo ">>> npm ci (node_modules missing or installed from another package-lock.json)"
    npm ci --no-audit --no-fund || exit 1
    echo "$LOCKSUM" > node_modules/.skillfish-lock.sha256
fi
echo ">>> astro $(node -p 'require("astro/package.json").version')"

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

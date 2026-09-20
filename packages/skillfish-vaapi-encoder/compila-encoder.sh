#!/bin/bash
# Build the BC-250 VA-API encoder from our fork.
#
#     compila-encoder.sh [ramo]
#         esempio: compila-encoder.sh fix/hevc-rate-control
#
# The driver encodes H.264 and HEVC with Vulkan compute shaders on the 40 CUs,
# because the BC-250 has no usable video engine. Upstream is simpmix's
# bc250-encoding-decoding-fix (GPL-3.0-only); we build our fork, which carries
# nine fixes sent back as pull requests 21 and 22 - without them HEVC segfaults
# on the first frame and, once it stops crashing, produces a picture no decoder
# reproduces.
#
# ⚠️ IL PREFISSO NON E' UN DETTAGLIO. Gli shader vengono cercati a un percorso
# compilato dentro la libreria, che CMake ricava da CMAKE_INSTALL_PREFIX. Con
# il valore di serie finirebbero in /usr/local/share, e un pacchetto Debian li'
# non ci scrive: si compila con prefisso /usr e gli shader vanno in
# /usr/share/bc250/shaders, dove la libreria li trova da sola.
#
# ⚠️ I test non si compilano di proposito: su alcune versioni mancano degli
# include e fanno fallire tutta la build, mentre la libreria sta benissimo.
set -eu
RAMO="${1:-fix/hevc-rate-control}"
ORIGINE=https://github.com/MTSistemi/bc250-encoding-decoding-fix.git
LAVORO=~/encoder-bc250
ALBERO=$LAVORO/costruito

for c in cmake glslangValidator pkg-config; do
    command -v "$c" >/dev/null || { echo "manca $c" >&2; exit 1; }
done
for l in libva libdrm vulkan; do
    pkg-config --exists "$l" || { echo "manca il pacchetto di sviluppo $l" >&2; exit 1; }
done

if [ -d "$LAVORO/sorgente/.git" ]; then
    git -C "$LAVORO/sorgente" fetch --depth 1 origin "$RAMO"
    git -C "$LAVORO/sorgente" checkout -q FETCH_HEAD
else
    rm -rf "$LAVORO/sorgente"
    mkdir -p "$LAVORO"
    git clone --depth 1 --branch "$RAMO" "$ORIGINE" "$LAVORO/sorgente"
fi

COMMIT=$(git -C "$LAVORO/sorgente" rev-parse --short HEAD)
echo ">>> ramo $RAMO, commit $COMMIT"

rm -rf "$ALBERO"
cmake -S "$LAVORO/sorgente/approach1-compute-encoder" -B "$ALBERO" \
      -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr >/dev/null
cmake --build "$ALBERO" -j"$(nproc)" --target bc250_drv_video compile_shaders

[ -f "$ALBERO/bc250_drv_video.so" ] || { echo "la libreria non e' uscita" >&2; exit 1; }
N=$(ls "$ALBERO"/*.spv 2>/dev/null | wc -l)
[ "$N" -ge 9 ] || { echo "solo $N shader compilati, ne servono 9" >&2; exit 1; }

echo "$COMMIT" > "$LAVORO/commit.txt"
echo ">>> pronto: $ALBERO ($(stat -c %s "$ALBERO/bc250_drv_video.so") byte, $N shader)"
echo ">>> adesso: pacchetto-encoder.sh"

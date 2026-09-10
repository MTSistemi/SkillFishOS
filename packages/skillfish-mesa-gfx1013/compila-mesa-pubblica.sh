#!/bin/bash
# Build the RADV we can actually ship: Mesa 26.2.2 + the compute-queue fix.
#
#     compila-mesa-pubblica.sh      log ~/mesa-pub.log, esito ~/mesa-pub.fatto
#
# ⚠️ NIENTE PATCH FSR4 QUI. Il repository bc250-fsr4 (dmorazasanchez) NON HA
# LICENZA: nessun file LICENSE, nessuna riga SPDX, niente nel README. Senza
# licenza non abbiamo il permesso di ridistribuire ne' la patch ne' un binario
# che la contiene, quindi nel pacchetto non ci va. Chi la vuole se la compila
# a casa sua con lo script che pubblichiamo a parte.
#
# ⚠️ QUESTA LIBRERIA VUOLE IL NOSTRO KERNEL. Il fix apre le code compute su
# GFX1013, che il RADV di serie tiene chiuse apposta; senza le patch v33 nel
# kernel (0130/0131) quelle code piantano la GPU. Il pacchetto NON sostituisce
# la Mesa di sistema: si installa in /opt e si accende per singolo gioco.
#
# Il fix e' di DryhoppedIPA (bc250-gfx1013-fix), licenza MIT, ed e' citato nel
# copyright del pacchetto.
set -u
SORG=~/mesa-pub-src
BUILD=~/mesa-pub-build
USCITA=~/mesa-pub
TAG=mesa-26.2.2
exec > >(tee ~/mesa-pub.log) 2>&1
rm -f ~/mesa-pub.fatto

echo "=== $(date +%H:%M:%S) sorgente $TAG"
if [ ! -d "$SORG/.git" ]; then
    rm -rf "$SORG"
    timeout 900 git clone -q --depth 1 --branch "$TAG" \
        https://gitlab.freedesktop.org/mesa/mesa.git "$SORG" || exit 1
fi
cd "$SORG" || exit 1
git checkout -q -- .
echo "    versione: $(git describe --tags 2>/dev/null || echo $TAG)"

echo "=== $(date +%H:%M:%S) fix code compute (DryhoppedIPA, MIT)"
python3 - <<'PY'
f = "src/amd/common/ac_gpu_info.c"
t = open(f).read()
v1 = """      /* GFX1013 is known to have broken compute queue */
      if (ip_type == AMD_IP_COMPUTE && device_info->family == FAMILY_NV &&
          ASICREV_IS(device_info->external_rev, GFX1013))
         return false;
"""
n1 = """      /* GFX1013: le code compute si espongono. ⚠️ Vuole un kernel con la
       * riparazione del ciclo di vita delle code (patch v33 0130/0131): su un
       * kernel di serie vanno lasciate chiuse o la GPU si pianta.
       * Fix originale: DryhoppedIPA/bc250-gfx1013-fix (MIT).
       */
"""
v2 = """   info->has_async_compute_threadgroup_bug = info->family == CHIP_ICELAND ||
                                             info->family == CHIP_TONGA;"""
n2 = """   info->has_async_compute_threadgroup_bug = info->family == CHIP_ICELAND ||
                                             info->family == CHIP_TONGA ||
                                             info->family == CHIP_GFX1013;"""
for v, n, nome in ((v1, n1, "code compute esposte"), (v2, n2, "bug threadgroup")):
    if t.count(v) != 1:
        raise SystemExit("⚠️ «%s»: trovato %d volte" % (nome, t.count(v)))
    t = t.replace(v, n, 1)
    print("    %s: applicato" % nome)
open(f, "w").write(t)
PY
[ $? -eq 0 ] || exit 1

echo "=== $(date +%H:%M:%S) compilo (solo RADV)"
rm -rf "$BUILD"
meson setup "$BUILD" "$SORG" -Dbuildtype=release -Dwrap_mode=nodownload \
    -Dvulkan-drivers=amd -Dgallium-drivers= -Dllvm=disabled \
    -Dplatforms=x11,wayland -Dvideo-codecs= 2>&1 | tail -3
ninja -C "$BUILD" -j 24 2>&1 | tail -3
SO=$(find "$BUILD" -name libvulkan_radeon.so | head -1)
[ -n "$SO" ] || { echo "⚠️ niente libreria"; exit 1; }
mkdir -p "$USCITA"
cp "$SO" "$USCITA/libvulkan_radeon.so"
echo "=== $(date +%H:%M:%S) fatto: $(stat -c%s "$USCITA/libvulkan_radeon.so") byte"
strings "$USCITA/libvulkan_radeon.so" | grep -oE "Mesa 26[^\"]*" | head -1
date > ~/mesa-pub.fatto

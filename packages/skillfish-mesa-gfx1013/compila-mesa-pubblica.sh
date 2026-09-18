#!/bin/bash
# Build the Mesa we ship: the WHOLE driver with our patches, not only RADV.
#
#     compila-mesa-pubblica.sh [versione]     esempio: 26.2.3
#
# Why: until now we shipped one file, libvulkan_radeon.so, and the rest of the
# machine kept Debian's Mesa. Two drivers on one board, and the desktop never
# saw our work. This builds the full stack (OpenGL, EGL, GBM, Vulkan, VA) into
# /opt/skillfish-gfx1013 so the whole 64-bit system can be pointed at it with a
# single ld.so.conf.d line.
#
# ⚠️ THE PREFIX IS PART OF THE BUILD. The DRI search path is compiled in, so
# our libEGL/libGLX/libgbm look for radeonsi_dri.so under our prefix. Moving the
# tree after the build breaks OpenGL in a way that looks like a driver bug.
#
# ⚠️ -Damd-use-llvm=false IS NOT OPTIONAL. Turning LLVM on for radeonsi also
# links RADV against libLLVM.so.21.1, which does not exist inside the flatpak
# sandbox the games run in: the Vulkan loader then drops our ICD IN SILENCE and
# the game starts on the runtime's driver. Same trap as libdisplay-info, and it
# only shows up in a measurement. RADV compiles shaders with ACO; LLVM there is
# dead weight.
#
# ⚠️ libdir MUST stay lib/x86_64-linux-gnu. That directory goes into
# /etc/ld.so.conf.d, and ldconfig tags every entry with its architecture: a
# 32-bit process looking for libvulkan_radeon.so skips ours and keeps finding
# Debian's i386 one. That is what lets 32-bit Proton games keep working.
set -u
VER="${1:-26.2.3}"
CORTO=$(echo "$VER" | tr -d .)
REPO=~/bc250-fsr4
SORG=~/mesa-fsr4-src
BUILD=~/mesa-completa-$CORTO-build
STAGE=~/mesa-completa-$CORTO
PREFISSO=/opt/skillfish-gfx1013
TAG=mesa-$VER
exec > >(tee ~/mesa-completa-$CORTO.log) 2>&1
rm -f ~/mesa-completa-$CORTO.fatto

cd "$SORG" || exit 1
git checkout -q -- .
git checkout -q "$TAG" || { echo "non ho il tag $TAG: serve git fetch --tags"; exit 1; }
echo "=== $(date +%H:%M:%S) sorgente $(git describe --tags 2>/dev/null || echo $TAG), patch FSR4 $(cd $REPO && git log -1 --format=%h)"
git apply --check --exclude=src/amd/common/ac_gpu_info.c "$REPO/bc250-fsr4-v3.patch" || { echo "la patch FSR4 non si applica: mi fermo"; exit 1; }
git apply --exclude=src/amd/common/ac_gpu_info.c "$REPO/bc250-fsr4-v3.patch" && echo "    FSR4 v3 applicata (senza ac_gpu_info.c)"

echo "=== $(date +%H:%M:%S) code compute in ac_gpu_info.c"
python3 - <<'PY'
f = "src/amd/common/ac_gpu_info.c"
t = open(f).read()
v1 = """      /* GFX1013 is known to have broken compute queue */
      if (ip_type == AMD_IP_COMPUTE && device_info->family == FAMILY_NV &&
          ASICREV_IS(device_info->external_rev, GFX1013))
         return false;
"""
n1 = """      /* GFX1013: the compute queues are exposed. Needs a kernel with the
       * queue lifecycle fixes (our patches 0130/0131): on a stock kernel they
       * hang the GPU. Fix by DryhoppedIPA/bc250-gfx1013-fix (MIT).
       */
"""
v2 = """   info->has_async_compute_threadgroup_bug = info->family == CHIP_ICELAND ||
                                             info->family == CHIP_TONGA;"""
n2 = """   info->has_async_compute_threadgroup_bug = info->family == CHIP_ICELAND ||
                                             info->family == CHIP_TONGA ||
                                             info->family == CHIP_GFX1013;"""
v3 = """            ASICREV_IS(device_info->external_rev, NAVI14)))
         info->ip[AMD_IP_GFX].ver_minor = info->ip[AMD_IP_COMPUTE].ver_minor = 1;"""
n3 = """            ASICREV_IS(device_info->external_rev, NAVI14) ||
            ASICREV_IS(device_info->external_rev, GFX1013)))
         info->ip[AMD_IP_GFX].ver_minor = info->ip[AMD_IP_COMPUTE].ver_minor = 1;"""
for v, n, nome in ((v1, n1, "code compute esposte"), (v2, n2, "bug threadgroup"), (v3, n3, "GFX10.1 (ver_minor)")):
    if n in t:
        print("    %s: gia' presente" % nome)
        continue
    if v not in t:
        raise SystemExit("    %s: contesto non trovato, mi fermo" % nome)
    t = t.replace(v, n, 1)
    print("    %s: applicato" % nome)
open(f, "w").write(t)
PY
[ $? -eq 0 ] || exit 1

echo "=== $(date +%H:%M:%S) meson setup"
rm -rf "$BUILD" "$STAGE"
meson setup "$BUILD" "$SORG" \
    -Dprefix=$PREFISSO \
    -Dlibdir=lib/x86_64-linux-gnu \
    -Dbuildtype=release \
    -Dwrap_mode=nodownload \
    -Dplatforms=x11,wayland \
    -Dvulkan-drivers=amd \
    -Dgallium-drivers=radeonsi,zink,softpipe,llvmpipe \
    -Dllvm=enabled -Dshared-llvm=enabled -Damd-use-llvm=false \
    -Dglvnd=enabled \
    -Degl=enabled -Dgbm=enabled -Dglx=dri -Dopengl=true -Dgles2=enabled \
    -Dvideo-codecs=all \
    -Dgallium-va=enabled \
    -Db_ndebug=true || { echo "meson setup fallito"; exit 1; }

echo "=== $(date +%H:%M:%S) compilo"
ninja -C "$BUILD" -j 20 || { echo "compilazione fallita"; exit 1; }

echo "=== $(date +%H:%M:%S) installo nello stage"
DESTDIR="$STAGE" ninja -C "$BUILD" install || exit 1

echo "=== $(date +%H:%M:%S) fatto"
find "$STAGE" -name '*.so*' -printf '%s\t%P\n' | sort -k2 | head -40
echo "--- versione dentro le librerie:"
strings "$STAGE$PREFISSO/lib/x86_64-linux-gnu/libvulkan_radeon.so" | grep -oE 'Mesa 26[^"]*' | head -1
strings "$STAGE$PREFISSO/lib/x86_64-linux-gnu/dri/radeonsi_dri.so" 2>/dev/null | grep -oE 'Mesa 26[^"]*' | head -1
echo "--- totale: $(du -sh "$STAGE" | cut -f1)"
date > ~/mesa-completa-$CORTO.fatto

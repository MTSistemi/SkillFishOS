#!/bin/bash
# Build the RADV we ship: Mesa 26.2.2 + FSR4 v3 (dmorazasanchez, MIT since
# 2026-09-11) + the GFX1013 compute-queue fix (DryhoppedIPA, MIT).
#
#     compila-mesa-pubblica.sh      log ~/mesa-2622.log, esito ~/mesa-2622.fatto
#
# The v3 patch carries the compute-queue hunks in ac_gpu_info.c itself, but
# they are written against Mesa main and do not apply to 26.2.2: that file is
# excluded from the patch and edited here with the same three changes
# (expose the compute queues, GFX1013 in the threadgroup-bug list, GFX1013 in
# the ver_minor = 1 list that marks the chip as GFX10.1).
# ⚠️ THIS LIBRARY WANTS OUR KERNEL: on a stock kernel the compute queues hang.
set -u
REPO=~/bc250-fsr4
SORG=~/mesa-fsr4-src
BUILD=~/mesa-2622-build
USCITA=~/mesa-2622
TAG=mesa-26.2.2
exec > >(tee ~/mesa-2622.log) 2>&1
rm -f ~/mesa-2622.fatto

cd "$SORG" || exit 1
git checkout -q -- .
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

echo "=== $(date +%H:%M:%S) compilo (solo RADV)"
rm -rf "$BUILD"
meson setup "$BUILD" "$SORG" -Dbuildtype=release -Dwrap_mode=nodownload \
    -Dvulkan-drivers=amd -Dgallium-drivers= -Dllvm=disabled \
    -Dplatforms=x11,wayland -Dvideo-codecs= 2>&1 | tail -3
ninja -C "$BUILD" -j 16 2>&1 | tail -3
SO=$(find "$BUILD" -name libvulkan_radeon.so | head -1)
[ -n "$SO" ] || { echo "niente libreria"; exit 1; }
mkdir -p "$USCITA"
cp "$SO" "$USCITA/libvulkan_radeon.so"
echo "=== $(date +%H:%M:%S) fatto: $(stat -c%s "$USCITA/libvulkan_radeon.so") byte, $(strings "$USCITA/libvulkan_radeon.so" | grep -oE "Mesa 26[^\"]*" | head -1)"
date > ~/mesa-2622.fatto

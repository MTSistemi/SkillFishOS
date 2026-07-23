#!/bin/bash
# Build the skillfishos-kernel wrapper for a given kernel version.
# Usage: build_wrapper.sh <kver> <debver> <reltag>
#   e.g. build_wrapper.sh 7.0.11-skillfishos 7.0.11-1 kernel-7.0.11-skillfishos
set -euo pipefail
KVER="$1"; DEBVER="$2"; RELTAG="$3"
OUT=/root/wrap; rm -rf "$OUT"; mkdir -p "$OUT/DEBIAN"
cat > "$OUT/DEBIAN/control" <<EOF
Package: skillfishos-kernel
Version: ${DEBVER}
Architecture: amd64
Maintainer: SkillFishOS <apt@skillfishos.com>
Depends: curl | wget, initramfs-tools
Section: kernel
Priority: optional
Description: SkillFishOS BC-250 kernel (linux-tkg ${KVER})
 Meta-package that downloads and installs the prebuilt linux-tkg ${KVER} kernel
 (image + headers) for the AMD BC-250 from the SkillFishOS GitHub release. The
 ~150 MB kernel image is hosted as a release asset because GitHub's 100 MB/file
 limit prevents shipping it in the APT pool.
EOF
cat > "$OUT/DEBIAN/postinst" <<EOF
#!/bin/sh
set -e
BASE="https://github.com/MTSistemi/SkillFishOS/releases/download/${RELTAG}"
IMG="linux-image-${KVER}_${DEBVER}_amd64.deb"
HDR="linux-headers-${KVER}_${DEBVER}_amd64.deb"
TMP="\$(mktemp -d)"
dl(){ if command -v curl >/dev/null 2>&1; then curl -fSL "\$1" -o "\$2"; else wget -O "\$2" "\$1"; fi; }
if dpkg-query -W -f='\${Status}' linux-image-${KVER} 2>/dev/null | grep -q "install ok installed"; then
  echo "skillfishos-kernel: ${KVER} already installed, skipping download."
else
  echo "skillfishos-kernel: fetching ${KVER} image + headers from GitHub release..."
  dl "\$BASE/\$IMG" "\$TMP/\$IMG"
  dl "\$BASE/\$HDR" "\$TMP/\$HDR"
  dpkg -i "\$TMP/\$IMG" "\$TMP/\$HDR" || apt-get -f install -y
  apt-mark hold linux-image-${KVER} linux-headers-${KVER} 2>/dev/null || true
fi
rm -rf "\$TMP"
command -v update-grub >/dev/null 2>&1 && update-grub || true
exit 0
EOF
chmod 0755 "$OUT/DEBIAN/postinst"
dpkg-deb --root-owner-group --build "$OUT" "/root/skillfishos-kernel_${DEBVER}_amd64.deb"
echo "=== built ==="; dpkg-deb -I "/root/skillfishos-kernel_${DEBVER}_amd64.deb" | grep -E 'Package|Version|Description' | head -3
echo "--- postinst preview ---"; sed -n '1,8p' "$OUT/DEBIAN/postinst"

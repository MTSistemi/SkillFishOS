#!/bin/bash
# Prep the box to build a single-kernel ISO for flavor $1 (version string $2).
# Installs the flavor kernel and excludes all OTHER skillfishos kernels from the
# eggs snapshot so the ISO ships only the target kernel.
set -euo pipefail
FLAVOR="$1"; KVER="$2"   # e.g. generic 7.0.11-skillfishos-generic
DEBDIR="/root/ktkg-${FLAVOR}/DEBS"

echo "### installing kernel $KVER (image+headers)"
dpkg -i "${DEBDIR}/linux-image-${KVER}_7.0.11-1_amd64.deb" \
        "${DEBDIR}/linux-headers-${KVER}_7.0.11-1_amd64.deb"

echo "### verify boot+modules"
ls -la "/boot/vmlinuz-${KVER}" "/boot/initrd.img-${KVER}"
ls -d "/lib/modules/${KVER}"

echo "### GRUB default still pinned to 7.0.10 (no change):"
grep -E '^GRUB_DEFAULT' /etc/default/grub

echo "### rebuild exclude.list: drop every skillfishos kernel except ${KVER}"
BASE=/etc/penguins-eggs.d/exclude.list
[ -f "${BASE}.skfbak" ] || cp "$BASE" "${BASE}.skfbak"
# start from the pristine backup, then append excludes for non-target kernels
cp "${BASE}.skfbak" "$BASE"
{
  echo "# SKF-KERNEL-EXCLUDE-START (flavor ${FLAVOR}, keep ${KVER})"
  for kv in $(ls -1 /lib/modules); do
    case "$kv" in
      *skillfishos*)
        if [ "$kv" != "$KVER" ]; then
          echo "boot/vmlinuz-${kv}"
          echo "boot/initrd.img-${kv}"
          echo "boot/System.map-${kv}"
          echo "boot/config-${kv}"
          echo "lib/modules/${kv}/*"
        fi
        ;;
    esac
  done
  echo "# SKF-KERNEL-EXCLUDE-END"
} >> "$BASE"
echo "### exclude.list tail:"; tail -n 12 "$BASE"
echo "### DONE prep for ${FLAVOR}"

#!/bin/bash
# Build .deb for the 3 new SkillFishOS apps from the installed files on the box.
set -euo pipefail
VER=26.06
OUT=/tmp/newdebs; rm -rf "$OUT"; mkdir -p "$OUT/out"
POST='#!/bin/sh
set -e
gtk-update-icon-cache -q -f /usr/share/icons/hicolor 2>/dev/null || true
update-desktop-database -q 2>/dev/null || true
exit 0'

build() { # build <pkg> <depends> <desc> <file1> [file2...]
  P="$1"; DEPS="$2"; DESC="$3"; shift 3
  D="$OUT/$P"; mkdir -p "$D/DEBIAN"
  for f in "$@"; do install -D -m "$( [ -x "$f" ] && echo 0755 || echo 0644 )" "$f" "$D$f"; done
  cat > "$D/DEBIAN/control" <<EOF
Package: $P
Version: $VER
Architecture: all
Maintainer: SkillFishOS <info@skillfishos.com>
Depends: $DEPS
Section: utils
Priority: optional
Homepage: https://skillfishos.com
Description: $DESC
EOF
  printf '%s\n' "$POST" > "$D/DEBIAN/postinst"; chmod 0755 "$D/DEBIAN/postinst"
  dpkg-deb --root-owner-group --build "$D" "$OUT/out/${P}_${VER}_all.deb" >/dev/null
  echo "built ${P}_${VER}_all.deb"
}

build skillfish-kernel-switch "python3, python3-pyqt6, polkitd | policykit-1, grub2-common" \
  "SkillFishOS Kernel Switch - choose the boot kernel (GRUB default / boot-once)" \
  /usr/local/bin/skillfish-kernel-switch /usr/local/bin/skillfish-grub-helper /usr/share/applications/os.skillfish.kernel.desktop

build skillfish-monitor "python3, python3-pyqt6, skillfish-tuner" \
  "SkillFishOS Monitor - live temperature/frequency/voltage/fan charts" \
  /usr/local/bin/skillfish-monitor /usr/share/applications/os.skillfish.monitor.desktop

build skillfish-hub "python3, python3-pyqt6, polkitd | policykit-1" \
  "SkillFishOS Hub - install and update SkillFishOS software from our repo" \
  /usr/local/bin/skillfish-hub /usr/share/applications/os.skillfish.hub.desktop

echo "=== built debs ==="; ls -l "$OUT/out/"

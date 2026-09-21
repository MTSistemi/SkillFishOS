#!/bin/bash
# Build skillfish-vkpeak from nihui/vkpeak's source, pinned to one commit.
#
#     bash packages/skillfish-vkpeak/build-vkpeak.sh [output-dir]
#
# WHY IT IS A PACKAGE (issue #91). The Control Center's GPU test and CU test
# run vkpeak, and until now they looked for it only in /opt/bench or
# /root/bench. Those folders exist on our development boards and in images
# cloned from them, and nowhere else: no package ever installed vkpeak, so on a
# normal installation the test said "vkpeak assente" and did nothing.
#
# It is built here rather than taken from upstream's release zip so that what
# we ship is what this recipe produces from a known commit.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-$HOME/DEBS-vkpeak}"
COMMIT=b98fe11            # nihui/vkpeak, 2026-08-16
VERSION=20260816-1
WORK="${WORK:-$HOME/build-vkpeak}"

mkdir -p "$WORK" "$OUT"
if [ ! -d "$WORK/vkpeak/.git" ]; then
  git clone -q --recursive https://github.com/nihui/vkpeak.git "$WORK/vkpeak"
fi
cd "$WORK/vkpeak"
git fetch -q --depth 50 origin || true
git checkout -q "$COMMIT"
git submodule update -q --init --recursive
[ "$(git rev-parse --short=7 HEAD)" = "$COMMIT" ] || { echo "not at $COMMIT" >&2; exit 1; }

rm -rf build && mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release .. > cmake.log
make -j"$(nproc)" > make.log
strip vkpeak

PKG="$WORK/pkg"
rm -rf "$PKG"
install -D -m 0755 vkpeak "$PKG/usr/lib/skillfish/vkpeak/vkpeak"
install -D -m 0644 "$HERE/copyright" "$PKG/usr/share/doc/skillfish-vkpeak/copyright"
{
  printf 'skillfish-vkpeak (%s) unstable; urgency=medium\n\n' "$VERSION"
  printf '  * vkpeak %s built from source, for the Control Center GPU and CU tests (#91).\n\n' "$COMMIT"
  printf ' -- SkillFishOS <info@skillfishos.com>  %s\n' "$(date -R)"
} | gzip -9n > "$PKG/usr/share/doc/skillfish-vkpeak/changelog.Debian.gz"
mkdir -p "$PKG/DEBIAN"
cat > "$PKG/DEBIAN/control" <<CTRL
Package: skillfish-vkpeak
Version: $VERSION
Architecture: amd64
Maintainer: SkillFishOS <info@skillfishos.com>
Depends: libc6, libstdc++6, libgcc-s1, libvulkan1
Section: utils
Priority: optional
Homepage: https://github.com/nihui/vkpeak
Description: vkpeak - Vulkan peak compute benchmark, for the SkillFishOS tests
 Measures the peak floating point and integer throughput of the GPU through
 Vulkan. The Control Center runs it for the GPU benchmark and the CU test.
 Built by SkillFishOS from nihui/vkpeak commit $COMMIT (MIT). The binary is
 installed out of PATH, in /usr/lib/skillfish/vkpeak.
 .
 Part of SkillFishOS.
CTRL
dpkg-deb --root-owner-group --build "$PKG" "$OUT/skillfish-vkpeak_${VERSION}_amd64.deb" >/dev/null
echo "$OUT/skillfish-vkpeak_${VERSION}_amd64.deb"

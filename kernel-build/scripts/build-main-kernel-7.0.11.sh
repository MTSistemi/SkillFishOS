#!/bin/bash
# Build 7.0.11-skillfishos (znver2, full config) = the BC-250 "main" kernel,
# bumped from 7.0.10 with the same customizations. Reuses the linux-tkg source
# tree (all BC-250 patches already applied), full generic config + -march=znver2.
set -uo pipefail
SRC=/root/ktkg-generic/linux-src-git
cd "$SRC"
cp -f /root/config-generic.bak .config
./scripts/config --set-str LOCALVERSION ""
yes '' | make olddefconfig > /tmp/main-olddef.log 2>&1
echo "config ready; modules(=m): $(grep -c '=m' .config)"
rm -f /root/maink.done /root/maink-build.log
nohup bash -c "cd '$SRC' && make -j12 bindeb-pkg KCFLAGS='-march=znver2 -mtune=znver2 -O3' KDEB_PKGVERSION='7.0.11-1' LOCALVERSION=-skillfishos > /root/maink-build.log 2>&1; echo \"EXIT \$?\" > /root/maink.done" >/dev/null 2>&1 &
echo "launched pid(bg)=$!"

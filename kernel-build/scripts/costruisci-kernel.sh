#!/bin/bash
# Build both SkillFishOS kernel flavours, one after the other, on the build VM.
#
#     kernel-build/scripts/costruisci-kernel.sh 7.2.6
#
# Output lands in ~/DEBS-<versione>/bc250/ and ~/DEBS-<versione>/x64/, and
# ~/build-<versione>.fatto is written when both are done.
#
# ⚠️ THE VERSION IS AN ARGUMENT NOW. It used to be a constant edited by hand at
# every release, which meant the file said 7.2.5 while it built 7.2.6 and the
# comments at the top were wrong more often than right.
#
# ⚠️ AND IT IS PINNED, not "7.2-latest". With -latest a new point release
# landing between the two builds gives a BC-250 kernel and an x64 kernel at
# different versions. That is not hypothetical: it is what confounded the GFXOFF
# A/B on 2026-09-17 and cost a whole rebuild.
#
# ⚠️ THE TWO FLAVOURS DIFFER IN THREE THINGS, and getting a single one wrong
# produces a package whose name looks right and that does not boot on the
# machine it is for:
#
#            _processor_opt   _kernel_localversion    who needs it
#   BC-250   znver2           skillfishos             the board, Zen 2
#   x64      x86-64           skillfishos-x64         any other x86-64 machine
#
# ⚠️ THE generic-cpu FRAGMENT IS NEEDED BY BOTH, here: this VM runs on a Zen 4
# host, and without the fragment CONFIG_X86_NATIVE_CPU stays on and the
# "BC-250" kernel comes out tuned for Zen 4. It does not boot on a Zen 2: that
# is issue #53.
#
# ⚠️ THE .myfrag FILES LIVE IN THE TREE ROOT and install.sh runs `git clean
# -ffdx`: they are wiped between one flavour and the next. They are copied back
# from the repository before each build.
#
# ⚠️ NOTHING OF OURS MAY SIT INSIDE ~/linux-tkg. linux-tkg globs the tree for
# *.myfrag, subdirectories included, so a folder of set-aside files left in
# there gets its fragments applied a second time, silently. Keep spare copies
# outside the tree.
set -u
V="${1:?uso: costruisci-kernel.sh <versione>   esempio: 7.2.6}"
cd ~/linux-tkg || exit 1
C=customization.cfg
REPO="$HOME/sfx-src/kernel-build"

# The external config silently overrides customization.cfg. It must not exist.
if [ -f ~/.config/frogminer/linux-tkg.cfg ]; then
    echo "!!! ~/.config/frogminer/linux-tkg.cfg esiste e vince su customization.cfg" >&2
    exit 1
fi

# The recipe: the full patch set, straight from the repository.
if ! diff -rq "$REPO/userpatches-350/" ~/linux-tkg/linux72-tkg-userpatches/ >/dev/null; then
    echo "!!! le patch nell'albero non sono la ricetta userpatches-350" >&2
    exit 1
fi
echo "patch: $(ls ~/linux-tkg/linux72-tkg-userpatches/ | wc -l) (ricetta 350, verificata)"

cp -n "$C" "$C.prima-del-$V"
mkdir -p ~/DEBS-$V/bc250 ~/DEBS-$V/x64 ~/frammenti-skillfish
cp -f "$REPO/config-fragments/"*.myfrag ~/frammenti-skillfish/
echo "frammenti: $(ls ~/frammenti-skillfish/*.myfrag | wc -l)"

imposta() {
    sed -i "s|^_version=.*|_version=\"v$V\"|" "$C"
    sed -i "s|^_processor_opt=.*|_processor_opt=\"$1\"|" "$C"
    sed -i "s|^_kernel_localversion=.*|_kernel_localversion=\"$2\"|" "$C"
    sed -i "s|^_install_after_building=.*|_install_after_building=\"no\"|" "$C"
    grep -E '^_version=|^_processor_opt=|^_kernel_localversion=' "$C" | sed 's/^/   /'
}

costruisci() {
    rm -f DEBS/*.deb 2>/dev/null
    cp -f ~/frammenti-skillfish/*.myfrag .
    ls ./*.myfrag | sed 's|^|   frammento |'
    ./install.sh install > ~/build-$V-$1.log 2>&1
    local esito=$?
    cp DEBS/*.deb ~/DEBS-$V/$1/ 2>/dev/null
    echo "$1: uscita $esito, $(ls ~/DEBS-$V/$1/*.deb 2>/dev/null | wc -l) pacchetti"
    grep -iE "hunk.*FAILED|patch failed|^make.*Error" ~/build-$V-$1.log | head -5
}

echo "=== BC-250 (znver2) $(date +%H:%M:%S) ==="
imposta znver2 skillfishos
costruisci bc250

echo "=== x64 (x86-64 generico) $(date +%H:%M:%S) ==="
imposta x86-64 skillfishos-x64
costruisci x64

echo "=== finito $(date +%H:%M:%S) ==="
ls -la ~/DEBS-$V/bc250/ ~/DEBS-$V/x64/ 2>/dev/null | grep -E 'linux-image|linux-headers'
echo
echo "poi si firma, e solo dopo si pubblica:"
echo "  sudo bash kernel-build/scripts/firma-kernel.sh ~/DEBS-$V/*/linux-image-*.deb"
date > ~/build-$V.fatto

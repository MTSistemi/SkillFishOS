#!/bin/bash
# Build both SkillFishOS kernel flavours from the 7.2.5 tree, one after the other.
#
#     costruisci-725.sh
#
# Esce in ~/DEBS-7.2.5/bc250/ e ~/DEBS-7.2.5/x64/, e lascia ~/build-725.fatto
# quando ha finito tutte e due. E' la ricetta del 7.2.4 con la versione nuova:
# il resto non cambia, e le trappole restano quelle.
#
# ⚠️ I DUE SAPORI SI DISTINGUONO PER TRE COSE, e sbagliarne una sola produce un
# pacchetto che sembra giusto dal nome e non parte sulla macchina di destinazione:
#
#            _processor_opt   _kernel_localversion    a chi serve
#   BC-250   znver2           skillfishos             la scheda, Zen 2
#   x64      x86-64           skillfishos-x64         qualunque macchina x86-64
#
# ⚠️ IL FRAMMENTO generic-cpu SERVE A TUTTI E DUE, qui: questa VM gira su un
# Ryzen 7950X (Zen 4), e senza il frammento CONFIG_X86_NATIVE_CPU resta acceso e
# il kernel «BC-250» esce tarato Zen 4. Su una Zen 2 non parte: e' la issue #53.
#
# ⚠️ I .myfrag stanno nella radice dell'albero e install.sh fa `git clean -ffdx`:
# vengono cancellati fra un sapore e l'altro. Qui si tengono da parte e si
# rimettono prima di ogni costruzione.
set -u
cd ~/linux-tkg || exit 1
C=customization.cfg
V=7.2.5
cp -n "$C" "$C.prima-del-725"
mkdir -p ~/DEBS-$V/bc250 ~/DEBS-$V/x64 ~/frammenti-skillfish
cp -f ./*.myfrag ~/frammenti-skillfish/ 2>/dev/null
echo "frammenti messi al sicuro: $(ls ~/frammenti-skillfish/*.myfrag 2>/dev/null | wc -l)"

imposta() {
    sed -i "s|^_version=.*|_version=\"v$V\"|" "$C"
    sed -i "s|^_processor_opt=.*|_processor_opt=\"$1\"|" "$C"
    sed -i "s|^_kernel_localversion=.*|_kernel_localversion=\"$2\"|" "$C"
    sed -i "s|^_install_after_building=.*|_install_after_building=\"no\"|" "$C"
    grep -E '^_version=|^_processor_opt=|^_kernel_localversion=' "$C"
}

costruisci() {
    rm -f DEBS/*.deb 2>/dev/null
    cp -f ~/frammenti-skillfish/*.myfrag . 2>/dev/null
    ls ./*.myfrag 2>/dev/null | sed 's|^|   frammento |'
    ./install.sh install > ~/build-725-$1.log 2>&1
    local esito=$?
    cp DEBS/*.deb ~/DEBS-$V/$1/ 2>/dev/null
    echo "$1: uscita $esito, $(ls ~/DEBS-$V/$1/*.deb 2>/dev/null | wc -l) pacchetti"
    grep -iE "error|fatal|patch failed|hunk.*FAILED" ~/build-725-$1.log | head -5
}

echo "=== BC-250 (znver2) $(date +%H:%M:%S) ==="
imposta znver2 skillfishos
costruisci bc250

echo "=== x64 (x86-64 generico) $(date +%H:%M:%S) ==="
imposta x86-64 skillfishos-x64
costruisci x64

echo "=== finito $(date +%H:%M:%S) ==="
ls -la ~/DEBS-$V/bc250/ ~/DEBS-$V/x64/ 2>/dev/null | grep -E 'linux-image|linux-headers'
date > ~/build-725.fatto

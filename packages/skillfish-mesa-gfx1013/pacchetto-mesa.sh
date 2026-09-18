#!/bin/bash
# Package our Mesa: the whole driver, not only the Vulkan half.
#
#     pacchetto-mesa.sh [versione-pacchetto] [versione-mesa]
#         esempio: pacchetto-mesa.sh 26.09.4 26.2.3
#
# ⚠️ FROM 26.09.4 THIS SHIPS THE WHOLE STACK. Until 26.09.3 the package held one
# file, libvulkan_radeon.so, and the machine kept Debian's Mesa for everything
# else: the desktop, the browsers, every native OpenGL program. Now the tree
# built by compila-mesa-pubblica.sh goes in whole, and /etc/ld.so.conf.d points
# the 64-bit side of the machine at it.
#
# ⚠️ LE DUE VERSIONI SONO DUE COSE DIVERSE: la prima e' il numero del nostro
# pacchetto, la seconda la Mesa che ci mettiamo dentro.
set -u
VER="${1:-$(date +%y.%m).4}"
MESA="${2:-26.2.3}"
CORTO=$(echo "$MESA" | tr -d .)
ALBERO=~/mesa-completa-$CORTO/opt/skillfish-gfx1013
QUI=$(dirname "$0")

[ -d "$ALBERO/lib/x86_64-linux-gnu" ] || {
    echo "non trovo $ALBERO: prima compila-mesa-pubblica.sh $MESA" >&2; exit 1; }

# ⚠️ Si controlla che le librerie dicano davvero quella versione, invece di
# fidarsi del nome della cartella.
for f in libvulkan_radeon.so libgallium-$MESA.so; do
    [ -f "$ALBERO/lib/x86_64-linux-gnu/$f" ] || { echo "manca $f" >&2; exit 1; }
    DENTRO=$(strings "$ALBERO/lib/x86_64-linux-gnu/$f" | grep -oE 'Mesa [0-9]+\.[0-9]+\.[0-9]+' | head -1 | cut -d' ' -f2)
    [ "$DENTRO" = "$MESA" ] || { echo "$f dice Mesa $DENTRO, non $MESA" >&2; exit 1; }
done

# ⚠️ E CHE RADV NON SI SIA PORTATO DIETRO LLVM. Con -Dllvm=enabled per radeonsi,
# anche libvulkan_radeon.so finisce legata a libLLVM.so.21.1, che dentro il
# sandbox flatpak dei giochi non esiste: il caricatore Vulkan scarta il nostro
# ICD in silenzio e il gioco parte con il driver del runtime. Si vede solo
# misurando, quindi si controlla qui.
if objdump -p "$ALBERO/lib/x86_64-linux-gnu/libvulkan_radeon.so" | grep -q LLVM; then
    echo "RADV e' legata a libLLVM: ricompila con -Damd-use-llvm=false" >&2; exit 1
fi
echo "pacchetto $VER, Mesa $MESA (verificata dentro le librerie, RADV senza LLVM)"

P=~/pkg-mesa
rm -rf "$P"
install -d "$P/DEBIAN" "$P/opt" "$P/usr/bin" "$P/usr/lib/systemd/system" \
           "$P/usr/share/doc/skillfish-mesa-gfx1013"
cp -a "$ALBERO" "$P/opt/skillfish-gfx1013"
# the headers and pkgconfig files are for building against Mesa: not our job
rm -rf "$P/opt/skillfish-gfx1013/include" "$P/opt/skillfish-gfx1013/lib/x86_64-linux-gnu/pkgconfig"

# ⚠️ L'ICD DEL SANDBOX HA IL PERCORSO ASSOLUTO, e serve solo ai flatpak: sul
# sistema il file di Debian (percorso relativo) risolve gia' alla nostra
# libreria attraverso la cache di ldconfig, e mettere un secondo file negli
# elenchi del caricatore farebbe comparire la stessa GPU due volte.
cat > "$P/opt/skillfish-gfx1013/share/vulkan/icd.d/radeon_icd.x86_64.json" <<'JSON'
{
    "ICD": {
        "api_version": "1.4.309",
        "library_path": "/opt/skillfish-gfx1013/lib/x86_64-linux-gnu/libvulkan_radeon.so"
    },
    "file_format_version": "1.0.0"
}
JSON

install -m 0755 "$QUI/skillfish-mesa" "$P/usr/bin/skillfish-mesa" || exit 1
install -m 0644 "$QUI/skillfish-mesa.service" "$P/usr/lib/systemd/system/skillfish-mesa.service" || exit 1

cat > "$P/DEBIAN/control" <<CTRL
Package: skillfish-mesa-gfx1013
Version: $VER
Section: libs
Priority: optional
Architecture: amd64
Depends: python3
Recommends: skillfishos-kernel
Maintainer: SkillFishOS <info@skillfishos.com>
Description: SkillFishOS - our Mesa for the BC-250, the whole driver
 Mesa ${MESA} built for the BC-250 with two changes the stock driver does not
 carry: on GFX1013 it exposes the dedicated compute queues, and it lowers FSR 4
 to INT8 so the upscaler runs on a chip AMD never shipped it for. Measured on a
 board: about 4 per cent in Cyberpunk 2077 from the queues, about 12 per cent
 more with FSR 4 on through OptiScaler.
 .
 From 26.09.4 this is the whole driver and not only the Vulkan half: OpenGL,
 EGL, GBM and Vulkan. On a BC-250 running our kernel it becomes the driver of
 the machine at boot, desktop included, through one line in /etc/ld.so.conf.d,
 and the flatpak overrides for Steam and Heroic point the games at it. On
 anything else the boot service leaves Debian's Mesa exactly where it is: the
 machine is recognised by its DMI, and the running kernel is checked at every
 boot rather than once at installation.
 .
 Debian's Mesa stays installed and untouched. The 32-bit side keeps using it on
 purpose, which is what lets 32-bit Proton games keep working.
 .
 WARNING: this driver needs a kernel carrying the BC-250 compute-queue lifecycle
 repair, which ours does. On a stock kernel those queues wedge the GPU, which is
 exactly why the stock driver keeps them closed. That is what the gate is for.
 .
 The compute-queue fix is the work of DryhoppedIPA (bc250-gfx1013-fix) and the
 FSR 4 lowering of dmorazasanchez (bc250-fsr4), both MIT; Mesa is MIT. See
 /usr/share/doc/skillfish-mesa-gfx1013/copyright.
 .
 Part of SkillFishOS.
CTRL

cat > "$P/DEBIAN/postinst" <<'POST'
#!/bin/sh
set -e
# ⚠️ libdisplay-info: la nostra .so e' compilata su sid e la chiede, ma il
# runtime flatpak dei giochi non ce l'ha. Si copia quella del sistema accanto
# alla nostra invece di spedirne una copia nostra: cosi' resta allineata agli
# aggiornamenti e non ridistribuiamo il binario di qualcun altro.
for f in /usr/lib/x86_64-linux-gnu/libdisplay-info.so.*; do
    [ -e "$f" ] || continue
    cp -a "$f" /opt/skillfish-gfx1013/lib/x86_64-linux-gnu/ 2>/dev/null || true
done

if [ -d /run/systemd/system ]; then
    systemctl daemon-reload >/dev/null 2>&1 || true
fi
deb-systemd-helper enable skillfish-mesa.service >/dev/null 2>&1 || true

# The switch decides for itself whether this machine may have our driver: a
# BC-250 on our kernel gets it now, anything else is left alone.
/usr/bin/skillfish-mesa avvio >/dev/null 2>&1 || true
/usr/bin/skillfish-mesa stato || true
exit 0
POST
chmod 755 "$P/DEBIAN/postinst"

cat > "$P/DEBIAN/prerm" <<'PRE'
#!/bin/sh
set -e
# Going away means giving the machine back to Debian's Mesa: the line in
# ld.so.conf.d and the flatpak overrides point at files that are about to
# disappear, and a Vulkan loader with a dangling ICD starts nothing at all.
if [ "$1" = "remove" ] || [ "$1" = "deconfigure" ]; then
    /usr/bin/skillfish-mesa off >/dev/null 2>&1 || true
    deb-systemd-invoke stop skillfish-mesa.service >/dev/null 2>&1 || true
    deb-systemd-helper disable skillfish-mesa.service >/dev/null 2>&1 || true
fi
exit 0
PRE
chmod 755 "$P/DEBIAN/prerm"

cat > "$P/usr/share/doc/skillfish-mesa-gfx1013/copyright" <<'COPY'
Upstream: Mesa (https://gitlab.freedesktop.org/mesa/mesa), tag mesa-@MESA@
License: MIT

The GFX1013 compute-queue change carried on top of it comes from
  DryhoppedIPA, bc250-gfx1013-fix — Copyright (c) 2026 DryhoppedIPA
  https://github.com/DryhoppedIPA/bc250-gfx1013-fix
  License: MIT

The FSR 4 INT8 lowering for GFX1013 (V3) comes from
  David Moraza Sanchez, bc250-fsr4 — Copyright (c) 2026 dmorazasanchez
  https://github.com/dmorazasanchez/bc250-fsr4 (branch v3)
  License: MIT (added upstream on 2026-09-11)
COPY
sed -i "s/@MESA@/$MESA/" "$P/usr/share/doc/skillfish-mesa-gfx1013/copyright"

dpkg-deb --root-owner-group --build "$P" ~/skillfish-mesa-gfx1013_${VER}_amd64.deb
ls -la ~/skillfish-mesa-gfx1013_${VER}_amd64.deb | awk '{print $5, $9}'

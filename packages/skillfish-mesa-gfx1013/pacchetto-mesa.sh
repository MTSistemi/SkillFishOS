#!/bin/bash
# Package our RADV for the BC-250 without touching the system Mesa.
#
#     pacchetto-mesa.sh [versione-pacchetto] [versione-mesa]
#         esempio: pacchetto-mesa.sh 26.09.3 26.2.3
#
# ⚠️ LE DUE VERSIONI ERANO COSTANTI, e non erano nemmeno le stesse cose: una
# e' il numero del nostro pacchetto, l'altra la Mesa che ci mettiamo dentro.
# Il numero del pacchetto usciva da `date`, quindi due rilasci nello stesso
# mese avevano lo stesso numero e il secondo non arrivava a nessuno; e la Mesa
# era scritta a mano in tre punti (la cartella, la descrizione, il copyright),
# quindi bastava dimenticarne uno per spedire un pacchetto che dichiarava una
# versione e ne conteneva un'altra.
set -u
VER="${1:-$(date +%y.%m).3}"
MESA="${2:-26.2.3}"
SORG=~/mesa-$(echo "$MESA" | tr -d .)/libvulkan_radeon.so
[ -f "$SORG" ] || { echo "non trovo $SORG: prima compila-mesa-pubblica.sh $MESA" >&2; exit 1; }
# ⚠️ E si controlla che la libreria dica davvero quella versione, invece di
# fidarsi del nome della cartella.
DENTRO=$(strings "$SORG" | grep -oE 'Mesa [0-9]+\.[0-9]+\.[0-9]+' | head -1 | cut -d' ' -f2)
[ "$DENTRO" = "$MESA" ] || { echo "la libreria dice Mesa $DENTRO, non $MESA" >&2; exit 1; }
echo "pacchetto $VER, Mesa $MESA (verificata dentro la libreria)"
P=~/pkg-mesa
rm -rf "$P"
install -d "$P/DEBIAN" "$P/opt/skillfish-gfx1013/lib/x86_64-linux-gnu" \
           "$P/opt/skillfish-gfx1013/share/vulkan/icd.d" "$P/usr/bin" \
           "$P/usr/share/doc/skillfish-mesa-gfx1013"

cp "$SORG" "$P/opt/skillfish-gfx1013/lib/x86_64-linux-gnu/"
cat > "$P/opt/skillfish-gfx1013/share/vulkan/icd.d/radeon_icd.x86_64.json" <<'JSON'
{
    "ICD": {
        "api_version": "1.4.309",
        "library_path": "/opt/skillfish-gfx1013/lib/x86_64-linux-gnu/libvulkan_radeon.so"
    },
    "file_format_version": "1.0.0"
}
JSON

# the switch: the copy kept in the repository next to this script
install -m 0755 "$(dirname "$0")/skillfish-mesa" "$P/usr/bin/skillfish-mesa" || exit 1

cat > "$P/DEBIAN/control" <<CTRL
Package: skillfish-mesa-gfx1013
Version: $VER
Section: libs
Priority: optional
Architecture: amd64
Depends: python3
Recommends: skillfishos-kernel
Maintainer: SkillFishOS <info@skillfishos.com>
Description: SkillFishOS - RADV for the BC-250 with the compute queues open
 A build of Mesa ${MESA}'s Vulkan driver carrying one change the stock driver
 does not: on GFX1013 it exposes the dedicated compute queues, and adds the chip
 to the async-compute threadgroup workaround list that has covered Iceland and
 Tonga since 2015. Measured on a BC-250: 4.2 per cent on Cyberpunk 2077.
 .
 It does not replace the system Mesa and does not touch it. The driver is
 installed under /opt/skillfish-gfx1013 and is switched on per application with
 "skillfish-mesa on", which writes the flatpak overrides for Steam and Heroic;
 "skillfish-mesa off" puts them back. Anything not switched on keeps using the
 distribution driver.
 .
 WARNING: this driver needs a kernel carrying the BC-250 compute-queue lifecycle
 repair, which ours does. On a stock kernel those queues wedge the GPU, which is
 exactly why the stock driver keeps them closed. Do not point a stock-kernel
 machine at it.
 .
 Since 26.09.2 it also carries the FSR 4 INT8 lowering for GFX1013 (V3) by
 dmorazasanchez (bc250-fsr4, MIT): with FSR 4 on through OptiScaler it is worth
 about +12% in Cyberpunk 2077, and it changes nothing when FSR 4 is off.
 .
 The compute-queue fix is the work of DryhoppedIPA (bc250-gfx1013-fix), MIT
 licensed; Mesa is MIT. See /usr/share/doc/skillfish-mesa-gfx1013/copyright.
 .
 Part of SkillFishOS.
CTRL

cat > "$P/DEBIAN/postinst" <<'POST'
#!/bin/sh
set -e
# ⚠️ libdisplay-info: la .so e' compilata su sid e la chiede, ma il runtime
# flatpak dei giochi non ce l'ha. Si copia quella del sistema accanto alla
# nostra invece di spedirne una copia nostra: cosi' resta allineata agli
# aggiornamenti e non ridistribuiamo il binario di qualcun altro.
for f in /usr/lib/x86_64-linux-gnu/libdisplay-info.so.*; do
    [ -e "$f" ] || continue
    cp -a "$f" /opt/skillfish-gfx1013/lib/x86_64-linux-gnu/ 2>/dev/null || true
done
echo "skillfish-mesa: installato. Si accende con 'skillfish-mesa on' (per gioco, non di sistema)."
exit 0
POST
chmod 755 "$P/DEBIAN/postinst"

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

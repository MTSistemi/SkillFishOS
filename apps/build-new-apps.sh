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
  /usr/local/bin/skillfish-kernel-manager /usr/local/bin/skillfish-kernel-helper /usr/share/applications/os.skillfish.kernel.desktop
# I due file si chiamavano skillfish-kernel-switch e skillfish-grub-helper, sono
# stati rinominati e questo script non era stato aggiornato: la build si fermava
# qui. Il NOME DEL PACCHETTO resta skillfish-kernel-switch di proposito, perche'
# cambiarlo obbligherebbe chi lo ha gia' installato a reinstallarlo a mano.

build skillfish-monitor "python3, python3-pyqt6, skillfish-tuner" \
  "SkillFishOS Monitor - live temperature/frequency/voltage/fan charts" \
  /usr/local/bin/skillfish-monitor /usr/share/applications/os.skillfish.monitor.desktop

# L'icona e' la borsa steampunk del NOSTRO tema — quella che SkillFishSteampunk
# usa per Discover, di cui l'Hub prende il posto nella barra — copiata come
# skillfish-hub invece di puntare al nome "plasmadiscover". Quel nome appartiene
# a plasma-discover-common: se un domani togliamo Discover dalla ISO l'Hub
# resterebbe con un quadrato vuoto.
# Sta in due temi apposta: in SkillFishSteampunk, che e' quello attivo, e in
# hicolor, che e' il ripiego per chi cambia tema — senza la copia in hicolor
# ricadrebbe sulla borsa blu di KDE, che col nostro ottone non c'entra niente.
# I PNG servono perche' nel codice l'icona della finestra e' un PERCORSO passato
# a QPixmap, non un nome di tema.
build skillfish-hub "python3, python3-pyqt6, polkitd | policykit-1" \
  "SkillFishOS Hub - install and update SkillFishOS software from our repo" \
  /usr/local/bin/skillfish-hub /usr/share/applications/os.skillfish.hub.desktop \
  /usr/share/icons/hicolor/48x48/apps/skillfish-hub.png \
  /usr/share/icons/hicolor/128x128/apps/skillfish-hub.png \
  /usr/share/icons/hicolor/256x256/apps/skillfish-hub.png \
  /usr/share/icons/hicolor/scalable/apps/skillfish-hub.svg \
  /usr/share/icons/SkillFishSteampunk/scalable/apps/skillfish-hub.svg

# Gli emulatori NON possono stare nella ISO: EmuDeck installa tutto nella home
# dell'utente (flatpak --user e AppImage in ~/Applications), e la ISO replica
# /etc/skel, non la home di chi ha costruito il sistema. Quindi vanno reinstallati
# su ogni macchina, e servono due voci nel menu Giochi — che e' esattamente dove
# la gente va a cercarli e non trova niente.
# Pacchetto separato e non dentro un altro perche' non c'entra con nessuna delle
# nostre app: sono due script e due voci di menu, pochi KB.
build skillfish-emulators "flatpak, curl" \
  "SkillFishOS Emulators - install emulators after the installation (EmuDeck or one by one)" \
  /usr/local/share/skillfish/install-emudeck.sh \
  /usr/local/share/skillfish/install-emulators.sh \
  /usr/share/applications/os.skillfish.emudeck.desktop \
  /usr/share/applications/os.skillfish.emulators.desktop

echo "=== built debs ==="; ls -l "$OUT/out/"

#!/bin/bash
# install-minecraft.sh — official Minecraft: Java Edition on SkillFishOS (BC-250).
#
# Installs the *official* Mojang launcher (the real Minecraft, not a clone):
# the launcher signs you in with your own Microsoft/Mojang account and
# downloads the game itself. The BC-250's Mesa driver exposes full hardware
# OpenGL 4.6 on gfx1013 (radeonsi/ACO), so Java Edition runs natively — no
# Zink/translation layer needed.
#
# Run as root ON THE BOX:  sudo bash install-minecraft.sh
# Optional: MINECRAFT_DEB=/path/to/Minecraft.deb to install a local file.
set -euo pipefail
USER_NAME="${SKILLFISH_USER:-skillfish}"
DEB_URL="https://launcher.mojang.com/download/Minecraft.deb"

echo ">>> [1/4] Java (runtime di riserva; il launcher porta comunque la sua JRE)"
# Minecraft 1.20.5+ vuole Java 21. Il launcher scarica la JRE giusta da solo,
# ma un JRE di sistema serve per mod-launcher (Prism/Fabric) e non guasta.
JRE=""
for cand in openjdk-21-jre openjdk-22-jre openjdk-23-jre default-jre; do
  if apt-cache show "$cand" >/dev/null 2>&1; then JRE="$cand"; break; fi
done
if [ -n "$JRE" ]; then
  apt-get update -qq || true
  DEBIAN_FRONTEND=noninteractive apt-get install -y "$JRE" || echo "  (Java di sistema non installato: il launcher userà la sua JRE)"
else
  echo "  (nessun pacchetto JRE trovato in apt: il launcher userà la sua JRE)"
fi

echo ">>> [2/4] launcher ufficiale Mojang"
if [ -n "${MINECRAFT_DEB:-}" ]; then
  ORIG="$MINECRAFT_DEB"
else
  TMP="$(mktemp -d)"; ORIG="$TMP/Minecraft.deb"
  echo "    scarico: $DEB_URL"
  curl -L --fail --retry 3 -o "$ORIG" "$DEB_URL"
fi
echo "    dimensione: $(du -h "$ORIG" | cut -f1)"

# Il .deb Mojang (2.1.x) dichiara dipendenze con NOMI LEGACY che su Debian sid
# non esistono più: `libgdk-pixbuf2.0-0` (ora `libgdk-pixbuf-2.0-0`) e
# `default-jre`. Le librerie/JRE reali ci sono — è solo il control a essere
# vecchio — quindi ripacchettizziamo rimappando i nomi ai pacchetti correnti.
echo "    correggo le dipendenze legacy per Debian sid"
WRK="$(mktemp -d)"; dpkg-deb -R "$ORIG" "$WRK"
sed -i -E \
  -e 's/\bdefault-jre\b/openjdk-21-jre | default-jre/' \
  -e 's/\blibgdk-pixbuf2\.0-0\b/libgdk-pixbuf-2.0-0/g' \
  -e 's/^(Version: .*)$/\1+skillfish1/' \
  "$WRK/DEBIAN/control"
DEB="$(dirname "$ORIG")/minecraft-launcher_skillfish.deb"
dpkg-deb --root-owner-group --build "$WRK" "$DEB" >/dev/null

echo ">>> [3/4] installazione (apt risolve il resto delle dipendenze)"
DEBIAN_FRONTEND=noninteractive apt-get install -y "$DEB"

echo ">>> [4/4] verifica"
BIN="$(command -v minecraft-launcher || echo /opt/minecraft-launcher/minecraft-launcher)"
if [ -x "$BIN" ]; then
  echo "    launcher: $BIN"
  # GL sanity (native path, no Zink)
  echo "    OpenGL: $(sudo -u "$USER_NAME" glxinfo -B 2>/dev/null | grep -m1 'OpenGL renderer' || echo 'glxinfo assente')"
else
  echo "FATAL: launcher non installato" >&2; exit 1
fi

cat <<EOF

=========================================================================
 Minecraft: Java Edition (ufficiale) installato.

 Avvialo dal menu (Giochi -> Minecraft Launcher) o con:  minecraft-launcher
 Al primo avvio accedi con il TUO account Microsoft/Mojang: il launcher
 scarica il gioco. La GPU BC-250 espone OpenGL 4.6 nativo, quindi gira
 senza layer di traduzione.

 Suggerimento prestazioni (opzionale, dopo): Fabric + Sodium alzano
 parecchio gli FPS rispetto al Minecraft vanilla.
=========================================================================
EOF

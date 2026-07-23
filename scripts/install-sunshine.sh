#!/bin/bash
# install-sunshine.sh — SkillFishOS game streaming host (Sunshine + Moonlight).
#
# Sunshine is the HOST that streams the desktop/games; the client is Moonlight
# (phone/PC/TV). Sunshine is not in Debian apt, so we fetch the official .deb
# from LizardByte's GitHub releases and let apt resolve its dependencies.
#
# Run as root ON THE BOX:  sudo bash install-sunshine.sh
# Optional: SUNSHINE_DEB=/path/to/sunshine.deb to install a specific file.
set -euo pipefail
USER_NAME="${SKILLFISH_USER:-skillfish}"
API="https://api.github.com/repos/LizardByte/Sunshine/releases/latest"

if [ -n "${SUNSHINE_DEB:-}" ]; then
  DEB="$SUNSHINE_DEB"
else
  echo ">>> [1/4] cerco l'ultima release Sunshine (.deb Debian amd64)"
  ASSETS="$(curl -fsSL "$API" | grep -oE '"browser_download_url":[^,]*\.deb"' | sed -E 's/.*"(https[^"]+)".*/\1/')"
  # preferenza: debian trixie -> bookworm -> qualsiasi debian -> primo .deb amd64
  URL="$(printf '%s\n' "$ASSETS" | grep -iE 'debian.*trixie|trixie.*debian' | grep -iE 'amd64|x86_64' | head -1)"
  [ -n "$URL" ] || URL="$(printf '%s\n' "$ASSETS" | grep -i 'debian' | grep -i 'bookworm' | grep -iE 'amd64|x86_64' | head -1)"
  [ -n "$URL" ] || URL="$(printf '%s\n' "$ASSETS" | grep -i 'debian' | grep -iE 'amd64|x86_64' | head -1)"
  [ -n "$URL" ] || URL="$(printf '%s\n' "$ASSETS" | grep -iE 'amd64|x86_64' | head -1)"
  [ -n "$URL" ] || { echo "FATAL: nessun .deb trovato nella release. Scaricalo a mano: https://github.com/LizardByte/Sunshine/releases" >&2; exit 1; }
  echo "    asset: $URL"
  TMP="$(mktemp -d)"; DEB="$TMP/sunshine.deb"
  curl -L --fail --retry 3 -o "$DEB" "$URL"
fi

echo ">>> [2/4] installazione (apt risolve le dipendenze)"
apt-get update
apt-get install -y "$DEB"

echo ">>> [3/4] permessi cattura schermo + KMS"
# Sunshine usa KMS/uinput per cattura e input virtuale
setcap cap_sys_admin+p "$(readlink -f "$(command -v sunshine)")" 2>/dev/null || true
modprobe uinput 2>/dev/null || true
echo 'uinput' > /etc/modules-load.d/sunshine.conf
# regola udev per /dev/uinput (di solito installata dal pacchetto; la garantiamo)
if [ ! -e /etc/udev/rules.d/85-sunshine.rules ]; then
  echo 'KERNEL=="uinput", SUBSYSTEM=="misc", OPTIONS+="static_node=uinput", TAG+="uaccess"' > /etc/udev/rules.d/85-sunshine.rules
  udevadm control --reload-rules && udevadm trigger --name-match=uinput || true
fi

echo ">>> [4/4] servizio utente"
# Sunshine gira come servizio UTENTE (serve la sessione grafica per catturare)
loginctl enable-linger "$USER_NAME" 2>/dev/null || true
sudo -u "$USER_NAME" XDG_RUNTIME_DIR="/run/user/$(id -u "$USER_NAME")" \
  systemctl --user enable sunshine 2>/dev/null || \
  echo "    (abilita Sunshine dalla sessione desktop: systemctl --user enable --now sunshine)"

echo
echo ">>> FATTO."
echo "    Web UI di pairing:  https://<ip-della-board>:47990  (crea utente/password al 1° accesso)"
echo "    Client: installa **Moonlight** sul dispositivo, aggiungi l'IP della board, inserisci il PIN."
echo "    Porte LAN: 47984-48010 (TCP/UDP). Nella dashboard collegheremo il modulo 'Game streaming'."

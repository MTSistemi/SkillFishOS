#!/usr/bin/env bash
# Skillfish OS setup for AMD BC-250 (Debian Testing "forky" + Cinnamon)
#
# FASE 1:
#   - Scarica e installa kernel+headers custom (.deb) in /tmp via dpkg -i
#   - Prepara continuazione automatica (systemd) + tail -f log visibile all'utente al login
#   - Reboot
#
# FASE 2 (dopo reboot):
#   - Disabilita eventuali repo "trixie" rimasti (per non mischiare suite)
#   - APT base + prerequisiti
#   - Mesa >= 25.3 (con pinning sid SOLO per Mesa se necessario)
#   - Flatpak + Flathub + installazioni di default (Steam, Heroic, Ryujinx)
#   - GameMode (daemon + libs)
#   - CoolerControl (Cloudsmith: fallback trixie se forky non riconosciuto)
#   - bc250_smu_oc
#   - cyan-skillfish-governor + config (safe-points: frequency 2000 -> 2230 se presente)
#   - nct6687 (DKMS precompilato .deb) + autoload
#   - Rimozione dinamica kernel non-target
#   - Shortcut Desktop "Install EmuDeck" (opzionale)
#   - GNOME Software + plugin Flatpak (per vedere Flathub nell'app "Software")

#
# Log:
#   - Unico file: skillfish-os-setup.log nella cartella da cui lanci lo script
#   - Riutilizzato anche dopo il reboot
#
# Uso:
#   chmod +x ./skillfish-os-setup.sh
#   sudo ./skillfish-os-setup.sh
#   (oppure doppio click: verrà chiesta l'autenticazione)
#
set -Eeuo pipefail

# -----------------------------
# Dropbox URLs (override via env)
# -----------------------------
KERNEL_IMAGE_URL_DEFAULT="https://www.dropbox.com/scl/fi/zzca3nb2yo1ap3d2dhetl/linux-image-6.18.5-tkg-amd-bc-250-mt_6.18.5-1_amd64.deb?rlkey=jodt42vu1y55hhtuibrhf7c5j&dl=0"
KERNEL_HEADERS_URL_DEFAULT="https://www.dropbox.com/scl/fi/ofk0bgz3hny30n3ijyqyr/linux-headers-6.18.5-tkg-amd-bc-250-mt_6.18.5-1_amd64.deb?rlkey=sxvw8ajg0h94gbrz8ux29lx15&dl=0"
NCT6687_DKMS_URL_DEFAULT="https://www.dropbox.com/scl/fi/26nh3m2l5jhxc5sk56se3/nct6687d-dkms_20251213-100501_all.deb?rlkey=lf1ifmogfrwlz4jx55btz6d3t&dl=0"

KERNEL_IMAGE_URL="${KERNEL_IMAGE_URL:-$KERNEL_IMAGE_URL_DEFAULT}"
KERNEL_HEADERS_URL="${KERNEL_HEADERS_URL:-$KERNEL_HEADERS_URL_DEFAULT}"
NCT6687_DKMS_URL="${NCT6687_DKMS_URL:-$NCT6687_DKMS_URL_DEFAULT}"

# -----------------------------
# Globals
# -----------------------------
STATE_DIR="/var/lib/skillfish-os-setup"
PHASE_FILE="$STATE_DIR/phase"
LOGPATH_FILE="$STATE_DIR/logpath"
TARGET_USER_FILE="$STATE_DIR/target_user"
COPIED_SCRIPT="/usr/local/sbin/skillfish-os-setup"
TAIL_HELPER="/usr/local/bin/skillfish-tail-log"
AUTOSTART_DESKTOP="/etc/xdg/autostart/skillfish-os-tail-log.desktop"

# -----------------------------
# Logging + errors
# -----------------------------
msg()  { echo -e "\n==> $*\n"; }
warn() { echo -e "\n[WARN] $*\n"; }
die()  { echo -e "\n[ERROR] $*\n" >&2; exit 1; }

trap_err() {
  local rc=$?
  local line=${BASH_LINENO[0]:-?}
  local cmd=${BASH_COMMAND:-?}
  echo -e "\n[ERROR] Script interrotto (rc=$rc) alla riga $line (cmd: $cmd)" >&2
  echo -e "[ERROR] Vedi log: ${LOG_FILE:-<non impostato>}\n" >&2
  exit "$rc"
}
trap trap_err ERR

ensure_root() {
  # If not root, re-exec with an elevation prompt (double click friendly).
  if [[ ${EUID:-$(id -u)} -eq 0 ]]; then
    return 0
  fi

  # Preserve original working dir for logging (pkexec may change cwd)
  export SKILLFISH_START_DIR="${SKILLFISH_START_DIR:-$(pwd -P)}"
  export SKILLFISH_TARGET_USER="${SKILLFISH_TARGET_USER:-${USER}}"

  local script
  script="$(readlink -f "$0")"

  # Graphical elevation (PolicyKit) when running from file manager (X11/Wayland)
  if [[ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]] && command -v pkexec >/dev/null 2>&1; then
    exec pkexec env \
      "DISPLAY=${DISPLAY:-}" \
      "WAYLAND_DISPLAY=${WAYLAND_DISPLAY:-}" \
      "XAUTHORITY=${XAUTHORITY:-${HOME}/.Xauthority}" \
      "SKILLFISH_START_DIR=${SKILLFISH_START_DIR}" \
      "SKILLFISH_TARGET_USER=${SKILLFISH_TARGET_USER}" \
      bash "$script" "$@"
  fi

  # GUI fallback: open a terminal and run sudo (covers double-click when pkexec is missing)
  if [[ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]] && command -v sudo >/dev/null 2>&1; then
    if command -v x-terminal-emulator >/dev/null 2>&1; then
      exec x-terminal-emulator -e sudo -E bash "$script" "$@"
    elif command -v gnome-terminal >/dev/null 2>&1; then
      exec gnome-terminal -- sudo -E bash "$script" "$@"
    elif command -v konsole >/dev/null 2>&1; then
      exec konsole -e sudo -E bash "$script" "$@"
    fi
  fi

  # Terminal fallback (works when already in a terminal)
  if command -v sudo >/dev/null 2>&1; then
    exec sudo -E bash "$script" "$@"
  fi

  die "Permessi insufficienti. Esegui come root o installa pkexec/sudo."
}

# -----------------------------
# Utils
# -----------------------------
have_cmd(){ command -v "$1" >/dev/null 2>&1; }

dropbox_direct() {
  local url="$1"
  if [[ "$url" == *"dropbox.com"* ]]; then
    if [[ "$url" == *"dl=0"* ]]; then
      echo "${url/dl=0/dl=1}"
    elif [[ "$url" == *"dl=1"* ]]; then
      echo "$url"
    else
      if [[ "$url" == *"?"* ]]; then echo "${url}&dl=1"; else echo "${url}?dl=1"; fi
    fi
  else
    echo "$url"
  fi
}

download_to() {
  local url="$1" out="$2"
  local durl; durl="$(dropbox_direct "$url")"
  mkdir -p "$(dirname "$out")"
  rm -f "$out.part"
  if have_cmd wget; then
    wget -q --show-progress --progress=dot:giga --tries=5 --timeout=30 --retry-connrefused --waitretry=2 -O "$out.part" "$durl"
  else
    curl -4fsSL -L -L --retry 5 --retry-all-errors --retry-delay 2 -o "$out.part" "$durl"
  fi
  mv -f "$out.part" "$out"
}

apt_update() { DEBIAN_FRONTEND=noninteractive apt-get update -y; }

apt_install() {
  local pkgs=("$@")
  DEBIAN_FRONTEND=noninteractive apt-get install -y "${pkgs[@]}" || {
    warn "apt install fallito per: ${pkgs[*]} (provo fix deps e ritento)"
    DEBIAN_FRONTEND=noninteractive apt-get -f install -y || true
    DEBIAN_FRONTEND=noninteractive apt-get install -y "${pkgs[@]}"
  }
}

pkg_installed() { dpkg -s "$1" >/dev/null 2>&1; }
pkg_version()   { dpkg-query -W -f='${Version}' "$1" 2>/dev/null || true; }
ver_ge()        { dpkg --compare-versions "$1" ge "$2"; }

detect_codename() {
  . /etc/os-release
  if [[ -n "${VERSION_CODENAME:-}" ]]; then
    echo "$VERSION_CODENAME"
  elif [[ -n "${DEBIAN_CODENAME:-}" ]]; then
    echo "$DEBIAN_CODENAME"
  else
    echo "forky"
  fi
}

get_target_user() {
  # Prefer the user who launched the script (saved in phase1), if available
  if [[ -f "$TARGET_USER_FILE" ]]; then
    local tu; tu="$(cat "$TARGET_USER_FILE" 2>/dev/null || true)"
    if [[ -n "$tu" ]] && getent passwd "$tu" >/dev/null 2>&1; then
      echo "$tu"
      return 0
    fi
  fi

  # If we were launched by double click and elevated via pkexec
  if [[ -n "${SKILLFISH_TARGET_USER:-}" ]] && getent passwd "$SKILLFISH_TARGET_USER" >/dev/null 2>&1; then
    echo "$SKILLFISH_TARGET_USER"
    return 0
  fi


  # If we're running under sudo in an interactive session
  if [[ -n "${SUDO_USER:-}" && "${SUDO_USER}" != "root" ]]; then
    echo "$SUDO_USER"
    return 0
  fi

  # Fallback: first human user
  getent passwd | awk -F: '$3>=1000 && $3<60000 && $1!="nobody" {print $1; exit}'
}

get_desktop_dir() {
  local u="$1"
  local home
  home="$(getent passwd "$u" | cut -d: -f6)"

  # Prefer xdg-user-dir if available (and returns an existing directory)
  if have_cmd xdg-user-dir; then
    local xdg_dir
    xdg_dir="$(su - "$u" -c 'xdg-user-dir DESKTOP' 2>/dev/null || true)"
    if [[ -n "${xdg_dir:-}" && -d "$xdg_dir" ]]; then
      echo "$xdg_dir"
      return 0
    fi
  fi

  if [[ -d "$home/Desktop" ]]; then echo "$home/Desktop"; return 0; fi
  if [[ -d "$home/Scrivania" ]]; then echo "$home/Scrivania"; return 0; fi
  echo "$home/Desktop"
}



ensure_log() {
  mkdir -p "$STATE_DIR"
  if [[ -f "$LOGPATH_FILE" ]]; then
    LOG_FILE="$(cat "$LOGPATH_FILE")"
  else
    local start_dir
    start_dir="${SKILLFISH_START_DIR:-$(pwd -P)}"
    LOG_FILE="$(readlink -f "$start_dir/skillfish-os-setup.log")"
    echo "$LOG_FILE" > "$LOGPATH_FILE"
  fi
  touch "$LOG_FILE"
  chmod 644 "$LOG_FILE" || true

  exec >>"$LOG_FILE" 2>&1
  export PS4='+ [$(date "+%F %T")] ${BASH_SOURCE##*/}:${LINENO}:${FUNCNAME[0]:-main}() '
  set -x
}

# -----------------------------
# Tail -f visible after reboot
# -----------------------------
write_tail_helper() {
  cat >"$TAIL_HELPER" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
STATE_DIR="/var/lib/skillfish-os-setup"
PHASE_FILE="$STATE_DIR/phase"
LOGPATH_FILE="$STATE_DIR/logpath"
TARGET_USER_FILE="$STATE_DIR/target_user"

[[ -f "$PHASE_FILE" ]] || exit 0
phase="$(cat "$PHASE_FILE" || true)"
[[ "$phase" == "2" ]] || exit 0

[[ -f "$LOGPATH_FILE" ]] || exit 0
log="$(cat "$LOGPATH_FILE")"
[[ -n "$log" && -f "$log" ]] || exit 0

pidfile="${XDG_RUNTIME_DIR:-/tmp}/skillfish-os-tail-log.pid"
if [[ -f "$pidfile" ]]; then
  if kill -0 "$(cat "$pidfile" 2>/dev/null)" 2>/dev/null; then exit 0; fi
fi

term=""
for t in x-terminal-emulator gnome-terminal konsole xfce4-terminal mate-terminal xterm; do
  if command -v "$t" >/dev/null 2>&1; then term="$t"; break; fi
done
[[ -n "$term" ]] || exit 0

case "$term" in
  gnome-terminal) gnome-terminal -- bash -lc "echo 'Skillfish OS setup in esecuzione. Log:' \"$log\"; echo; tail -n +1 -f \"$log\"" & ;;
  konsole)        konsole -e bash -lc "echo 'Skillfish OS setup in esecuzione. Log:' \"$log\"; echo; tail -n +1 -f \"$log\"" & ;;
  xfce4-terminal|mate-terminal)
                 "$term" -e bash -lc "echo 'Skillfish OS setup in esecuzione. Log:' \"$log\"; echo; tail -n +1 -f \"$log\"" & ;;
  xterm)          xterm -e bash -lc "echo 'Skillfish OS setup in esecuzione. Log:' \"$log\"; echo; tail -n +1 -f \"$log\"" & ;;
  *)              "$term" -e bash -lc "echo 'Skillfish OS setup in esecuzione. Log:' \"$log\"; echo; tail -n +1 -f \"$log\"" & ;;
esac

echo $! >"$pidfile"
exit 0
EOF
  chmod +x "$TAIL_HELPER"
}

write_autostart_desktop() {
  mkdir -p /etc/xdg/autostart
  cat >"$AUTOSTART_DESKTOP" <<EOF
[Desktop Entry]
Type=Application
Name=Skillfish OS Setup (tail log)
Exec=$TAIL_HELPER
X-GNOME-Autostart-enabled=true
NoDisplay=true
EOF
}


install_continuation_service() {
  cat >/etc/systemd/system/skillfish-os-setup.service <<EOF
[Unit]
Description=Skillfish OS Setup - Phase 2 continuation
Wants=network-online.target
After=network-online.target
ConditionPathExists=$PHASE_FILE

[Service]
Type=oneshot
ExecStart=$COPIED_SCRIPT --phase2
RemainAfterExit=no

[Install]
WantedBy=multi-user.target
EOF
  systemctl daemon-reload
  systemctl enable skillfish-os-setup.service
}

disable_continuation_service() {
  # Do NOT stop the service while we are running inside it (it would kill this script).
  systemctl disable skillfish-os-setup.service 2>/dev/null || true
  rm -f /etc/systemd/system/skillfish-os-setup.service
  systemctl daemon-reload || true
}

# -----------------------------
# Disable leftover trixie sources
# -----------------------------
backup_file_once() {
  local f="$1"
  [[ -f "$f" ]] || return 0
  [[ -f "${f}.bak.skillfish" ]] || cp -a "$f" "${f}.bak.skillfish" || true
}

disable_suite_sources() {
  local suite="$1"
  msg "Disabilito eventuali repo APT che puntano a '$suite' (per evitare mix di suite)…"

  if [[ -f /etc/apt/sources.list ]]; then
    backup_file_once /etc/apt/sources.list
    sed -i -E \
      "s|^([[:space:]]*deb(-src)?[[:space:]].*[[:space:]]${suite}[[:space:]].*)$|# disabled by Skillfish (suite mix): \1|g" \
      /etc/apt/sources.list || true
  fi

  shopt -s nullglob
  for f in /etc/apt/sources.list.d/*.list; do
    [[ "$f" == "/etc/apt/sources.list.d/skillfish-os.list" ]] && continue
    [[ "$f" == "/etc/apt/sources.list.d/skillfish-sid-mesa.list" ]] && continue
    backup_file_once "$f"
    sed -i -E \
      "s|^([[:space:]]*deb(-src)?[[:space:]].*[[:space:]]${suite}[[:space:]].*)$|# disabled by Skillfish (suite mix): \1|g" \
      "$f" || true
  done
  shopt -u nullglob
}

# -----------------------------
# APT sources (NO trixie references)
# -----------------------------
ensure_sources() {
  local codename="$1"
  msg "Configuro APT per Debian $codename (main+contrib+non-free+non-free-firmware)…"
  cat >/etc/apt/sources.list.d/skillfish-os.list <<EOF
deb http://deb.debian.org/debian ${codename} main contrib non-free non-free-firmware
deb http://deb.debian.org/debian ${codename}-updates main contrib non-free non-free-firmware
deb http://security.debian.org/debian-security ${codename}-security main contrib non-free non-free-firmware
deb http://deb.debian.org/debian ${codename}-backports main contrib non-free non-free-firmware
EOF
  apt_update
}

ensure_multiarch_i386() {
  if ! dpkg --print-foreign-architectures | grep -qx i386; then
    dpkg --add-architecture i386
    apt_update
  fi
}

# -----------------------------
# Mesa
# -----------------------------
ensure_mesa_min_version() {
  local min="25.3"
  msg "Mesa >= ${min}…"
  local cur
  cur="$(pkg_version mesa-vulkan-drivers || true)"
  if [[ -n "$cur" ]] && ver_ge "$cur" "$min"; then
    msg "Mesa già OK: mesa-vulkan-drivers=$cur (skip)"
    return 0
  fi

  warn "Mesa è $cur (o non installato). Provo dalle repo correnti."
  apt_install mesa-vulkan-drivers mesa-utils vulkan-tools || true

  cur="$(pkg_version mesa-vulkan-drivers || true)"
  if [[ -n "$cur" ]] && ver_ge "$cur" "$min"; then
    msg "Mesa ora OK: mesa-vulkan-drivers=$cur"
    return 0
  fi

  warn "Mesa ancora < ${min}. Abilito Debian sid SOLO per Mesa (pinning) e riprovo."
  cat >/etc/apt/sources.list.d/skillfish-sid-mesa.list <<'EOF'
deb http://deb.debian.org/debian sid main contrib non-free non-free-firmware
EOF

  cat >/etc/apt/preferences.d/skillfish-mesa-pin <<'EOF'
Package: *
Pin: release a=sid
Pin-Priority: 100

Package: mesa-*
Pin: release a=sid
Pin-Priority: 990

Package: libglx-mesa0 libegl-mesa0 libgbm1 libgl1-mesa-dri mesa-vulkan-drivers mesa-libgallium
Pin: release a=sid
Pin-Priority: 990
EOF

  apt_update
  ensure_multiarch_i386

  local pkgs=(
    "mesa-vulkan-drivers" "mesa-vulkan-drivers:i386"
    "libglx-mesa0" "libglx-mesa0:i386"
    "libegl-mesa0" "libegl-mesa0:i386"
    "libgbm1" "libgbm1:i386"
    "libgl1-mesa-dri" "libgl1-mesa-dri:i386"
    "mesa-libgallium" "mesa-libgallium:i386"
    "mesa-utils" "vulkan-tools"
  )
  DEBIAN_FRONTEND=noninteractive apt-get install -y -t sid "${pkgs[@]}" || true

  cur="$(pkg_version mesa-vulkan-drivers || true)"
  if [[ -n "$cur" ]] && ver_ge "$cur" "$min"; then
    msg "Mesa ora OK (sid pinned): mesa-vulkan-drivers=$cur"
  else
    warn "Non sono riuscito a portare Mesa >= ${min} automaticamente. Versione attuale: ${cur:-<n/d>}"
  fi
}

# -----------------------------
# Flatpak + Flathub + default apps
# -----------------------------
ensure_flathub() {
  msg "Flatpak + Flathub…"
  apt_install flatpak xdg-desktop-portal xdg-desktop-portal-gtk || true
  if ! flatpak remote-list | awk '{print $1}' | grep -qx flathub; then
    flatpak remote-add --if-not-exists --system flathub https://dl.flathub.org/repo/flathub.flatpakrepo
  fi
  flatpak update --appstream --system || true
}

flatpak_install_if_missing() {
  local appid="$1"
  if ! flatpak info "$appid" >/dev/null 2>&1; then
    flatpak install -y flathub "$appid" || true
  else
    msg "Flatpak già presente: $appid (skip)"
  fi
}

install_default_gaming_flatpaks() {
  msg "Installazioni di default da Flathub: Steam, Heroic, Ryujinx…"
  ensure_flathub
  flatpak_install_if_missing "com.valvesoftware.Steam"
  flatpak_install_if_missing "com.heroicgameslauncher.hgl"
  flatpak_install_if_missing "io.github.ryubing.Ryujinx"
  flatpak_install_if_missing "net.davidotek.pupgui2"
}

# -----------------------------
# GNOME Software + plugin Flatpak
# -----------------------------
install_gnome_software_flatpak_plugin() {
  msg "GNOME Software + plugin Flatpak (per mostrare Flathub nell'app 'Software')…"
  apt_install gnome-software gnome-software-plugin-flatpak || true
}

# -----------------------------
# GameMode (APT - forky)
# -----------------------------
install_gamemode() {
  msg "GameMode (APT)…"
  apt_install gamemode gamemode-daemon libgamemode0 libgamemodeauto0 || true
  ensure_multiarch_i386
  DEBIAN_FRONTEND=noninteractive apt-get install -y libgamemode0:i386 libgamemodeauto0:i386 || true

  cat >/usr/local/bin/steam-gamemode <<'EOF'
#!/usr/bin/env bash
exec gamemoderun flatpak run com.valvesoftware.Steam "$@"
EOF
  chmod +x /usr/local/bin/steam-gamemode

  cat >/usr/local/bin/heroic-gamemode <<'EOF'
#!/usr/bin/env bash
exec gamemoderun flatpak run com.heroicgameslauncher.hgl "$@"
EOF
  chmod +x /usr/local/bin/heroic-gamemode
}

# -----------------------------
# CoolerControl (Cloudsmith)
# -----------------------------
install_coolercontrol() {
  msg "CoolerControl…"
  apt_install curl ca-certificates gnupg apt-transport-https debian-keyring || true

  local codename; codename="$(detect_codename)"
  if curl -4fsSL -L -L 'https://dl.cloudsmith.io/public/coolercontrol/coolercontrol/setup.deb.sh' | sudo -E distro=debian codename="$codename" bash; then
    :
  else
    warn "Cloudsmith non ha accettato codename=$codename. Provo fallback: trixie."
    curl -4fsSL -L -L 'https://dl.cloudsmith.io/public/coolercontrol/coolercontrol/setup.deb.sh' | sudo -E distro=debian codename="trixie" bash
  fi

  apt_update
  apt_install coolercontrol || true
  systemctl enable --now coolercontrold || true
}

# -----------------------------
# bc250_smu_oc
# -----------------------------
install_bc250_smu_oc() {
  msg "bc250_smu_oc…"
  apt_install git jq stress python3 python3-pip pipx || true

  export PIPX_HOME="/opt/pipx"
  export PIPX_BIN_DIR="/usr/local/bin"
  mkdir -p "$PIPX_HOME" "$PIPX_BIN_DIR"
  pipx ensurepath || true

  local dir="/opt/skillfish/bc250_smu_oc"
  mkdir -p /opt/skillfish
  if [[ ! -d "$dir/.git" ]]; then
    git clone https://github.com/bc250-collective/bc250_smu_oc.git "$dir"
  else
    (cd "$dir" && git pull --ff-only) || true
  fi

  if have_cmd bc250-detect && have_cmd bc250-apply; then
    msg "bc250_smu_oc già presente (skip)"
    return 0
  fi

  (cd "$dir" && pipx install . --force) || true

  # Istruzioni (testo) per overclock/undervolt CPU via bc250_smu_oc (SMU)
  local u; u="$(get_target_user)"
  if [[ -n "$u" ]]; then
    local home; home="$(getent passwd "$u" | cut -d: -f6)"
    local desktop; desktop="$(get_desktop_dir "$u")"
    mkdir -p "$desktop"
    chown "$u:$u" "$desktop" 2>/dev/null || true
    local doc="$desktop/BC-250_SMU_OC_Istruzioni.txt"

    cat >"$doc" <<'EOF'
BC-250 SMU OC (CPU overclock / undervolt) - ISTRUZIONI RAPIDE

ATTENZIONE (LEGGERE): l’overclock/undervolt è a tuo rischio. Impostazioni errate possono causare instabilità e danni.
- NON superare mai ~1.325V di core voltage (Vid) durante i test.
- Aumentare la frequenza SENZA limitare la tensione può portare a Vid “uncapped” e rischi seri.
- Fai sempre test di stabilità e monitora temperature/voltaggi.

Questo sistema ha installato i tool "bc250-detect" e "bc250-apply" (repo: bc250-collective/bc250_smu_oc).

1) Verifica che i comandi esistano
   bc250-detect --help
   bc250-apply  --help

2) Trova un set stabile (test temporaneo)
   Esempio (OC):
     bc250-detect --frequency 4000 --vid 1275 --keep

   Se crasha:
     - prova ad alzare leggermente il Vid (es. 1300)
     - oppure riduci la frequenza (es. 3900/3800)
   Consiglio prudente: resta sotto ~1300 mV di Vid se possibile.

   Esempio (solo UNDERVOLT a frequenza stock):
     bc250-detect --frequency 3500 --vid 1000 --keep

3) Test stabilità (consigliato)
   - usa "stress" e/o carichi reali (giochi/app pesanti) per almeno 10-30 minuti per step
   - controlla temperature e che non ci siano freeze/reboot

4) Rendi permanente (all’avvio) SOLO quando sei sicuro che sia stabile
   bc250-apply --install overclock.conf
   sudo systemctl enable --now bc250-smu-oc

5) Disabilita / torna stock
   sudo systemctl disable --now bc250-smu-oc

Monitoraggio utile
- Frequenze effettive CPU (per vedere eventuale clock-stretching):
    watch -n 1 "cat /proc/cpuinfo | grep MHz"
- Temperature:
    watch -n 1 sensors

Per dettagli e raccomandazioni aggiornate consulta la pagina ufficiale:
https://github.com/bc250-collective/bc250_smu_oc
EOF

    chmod 644 "$doc" || true
    chown "$u:$u" "$doc" 2>/dev/null || true
  fi
}

# -----------------------------
# cyan-skillfish-governor
# -----------------------------
gh_latest_asset_url() {
  local owner="$1" repo="$2" regex="$3"
  local api="https://api.github.com/repos/${owner}/${repo}/releases/latest"
  local json=""
  if have_cmd wget; then json="$(wget -qO- --tries=3 --timeout=20 "$api" || true)"; fi
  if [[ -z "$json" ]]; then json="$(curl -4fsSL -L -L --retry 3 --retry-all-errors "$api" || true)"; fi
  [[ -n "$json" ]] || return 1
  echo "$json" | jq -r --arg re "$regex" '.assets[] | select(.name|test($re)) | .browser_download_url' | head -n1
}

install_cyan_skillfish_governor() {
  msg "cyan-skillfish-governor…"
  apt_install jq wget ca-certificates || true

  if ! pkg_installed cyan-skillfish-governor; then
    local url
    url="$(gh_latest_asset_url "Magnap" "cyan-skillfish-governor" "amd64\\.deb$" || true)"
    if [[ -z "${url:-}" ]]; then
      warn "Non riesco a determinare l'ultima release da GitHub API. Salto installazione governor."
      return 0
    fi
    local deb="/tmp/cyan-skillfish-governor_latest_amd64.deb"
    download_to "$url" "$deb"
    dpkg -i "$deb" || true
    DEBIAN_FRONTEND=noninteractive apt-get -f install -y || true
  else
    msg "cyan-skillfish-governor già installato (skip)"
  fi

  mkdir -p /etc/cyan-skillfish-governor
  local cfg="/etc/cyan-skillfish-governor/config.toml"
  if [[ -f "$cfg" ]]; then
    cp -a "$cfg" "$cfg.bak.$(date +%Y%m%d_%H%M%S)" || true
  else
    cat >"$cfg" <<'EOF'
# us
[timing.intervals]
sample = 2000
adjust = 20_000
finetune = 1_000_000_000

# MHz/ms
[timing.ramp-rates]
normal = 1
burst = 200

# number of samples
[timing]
burst-samples = 48

# MHz
[frequency-thresholds]
adjust = 100
finetune = 10

[load-target]
upper = 0.95
lower = 0.7

[[safe-points]]
frequency = 350 # MHz
voltage = 700 # mV

[[safe-points]]
frequency = 2230
voltage = 1000
EOF
  fi

  if grep -qE '^[[:space:]]*frequency[[:space:]]*=[[:space:]]*2000([[:space:]]|$)' "$cfg"; then
    sed -i -E 's/^([[:space:]]*frequency[[:space:]]*=[[:space:]]*)2000([[:space:]]|$)/\12230\2/' "$cfg"
  fi

  systemctl enable --now cyan-skillfish-governor.service || true
}

# -----------------------------
# nct6687 DKMS (prebuilt .deb) + autoload
# -----------------------------
install_nct6687_dkms() {
  msg "nct6687 (DKMS) + autoload…"
  if lsmod | awk '{print $1}' | grep -qx nct6687; then
    msg "Modulo nct6687 già caricato (skip install)"
  else
    local deb="/tmp/nct6687d-dkms_all.deb"
    if [[ ! -s "$deb" ]]; then
      download_to "$NCT6687_DKMS_URL" "$deb"
    fi
    dpkg -i "$deb" || true
    DEBIAN_FRONTEND=noninteractive apt-get -f install -y || true
  fi

  modprobe nct6687 || true
  echo "nct6687" >/etc/modules-load.d/nct6687.conf
}

# -----------------------------
# Kernel management
# -----------------------------
current_kernel_target() { uname -r; }

purge_other_kernels() {
  local target="$1"
  msg "Rimozione kernel non-target (dinamico) — target: $target"

  if pkg_installed linux-image-amd64; then DEBIAN_FRONTEND=noninteractive apt-get purge -y linux-image-amd64 || true; fi
  if pkg_installed linux-headers-amd64; then DEBIAN_FRONTEND=noninteractive apt-get purge -y linux-headers-amd64 || true; fi

  mapfile -t imgs < <(dpkg-query -W -f='${Package}\n' 'linux-image-*' 2>/dev/null | sort -u)
  for p in "${imgs[@]}"; do
    [[ "$p" == "linux-image-$target" ]] && continue
    [[ "$p" == *"$target"* ]] && continue
    [[ "$p" == "linux-image-amd64" ]] && continue
    [[ "$p" == linux-image-* ]] && DEBIAN_FRONTEND=noninteractive apt-get purge -y "$p" || true
  done

  mapfile -t hdrs < <(dpkg-query -W -f='${Package}\n' 'linux-headers-*' 2>/dev/null | sort -u)
  for p in "${hdrs[@]}"; do
    [[ "$p" == "linux-headers-$target" ]] && continue
    [[ "$p" == *"$target"* ]] && continue
    [[ "$p" == "linux-headers-amd64" ]] && continue
    [[ "$p" == linux-headers-* ]] && DEBIAN_FRONTEND=noninteractive apt-get purge -y "$p" || true
  done

  DEBIAN_FRONTEND=noninteractive apt-get autoremove -y || true
  update-initramfs -u -k "$target" || true
  update-grub || true
  apt-mark hold linux-image-amd64 linux-headers-amd64 2>/dev/null || true
}

# -----------------------------
# EmuDeck (latest AppImage from GitHub) + launcher menu
# -----------------------------
install_emudeck_latest_appimage() {
  msg "EmuDeck: scarico ultima AppImage da GitHub (senza FUSE2) e creo il launcher nel menu applicazioni…"

  local u; u="$(get_target_user)"
  if [[ -z "$u" ]]; then
    warn "EmuDeck: nessun utente valido trovato, skip."
    return 0
  fi

  local home; home="$(getent passwd "$u" | cut -d: -f6)"
  if [[ -z "$home" || ! -d "$home" ]]; then
    warn "EmuDeck: home non valida per utente '$u' ($home), skip."
    return 0
  fi

  local repo="EmuDeck/emudeck-electron"   # stable
  local install_dir="$home/Applications"
  local dest="$install_dir/EmuDeck.AppImage"
  local wrapper="$install_dir/EmuDeck.sh"

  mkdir -p "$install_dir"
  chown "$u:$u" "$install_dir" 2>/dev/null || true

  # Resolve latest tag via GitHub redirect (no JSON parsing)
  local latest_url="https://github.com/${repo}/releases/latest"
  local final_url tag ver default_asset download_url release_page html href

  final_url="$(curl -fsSL -o /dev/null -w '%{url_effective}' -L "$latest_url")" || {
    warn "EmuDeck: impossibile risolvere l'ultima release (rete/GitHub)."
    return 0
  }

  if [[ "$final_url" != *"/releases/tag/"* ]]; then
    warn "EmuDeck: URL finale inatteso: $final_url"
    return 0
  fi

  tag="${final_url##*/}"   # vX.Y.Z
  ver="${tag#v}"
  default_asset="EmuDeck-${ver}.AppImage"
  download_url="https://github.com/${repo}/releases/download/${tag}/${default_asset}"

  # If default naming doesn't match, scrape the release page for the first .AppImage link
  if ! curl -fsSI "$download_url" >/dev/null 2>&1; then
    release_page="https://github.com/${repo}/releases/tag/${tag}"
    html="$(curl -fsSL "$release_page" || true)"
    href="$(printf '%s' "$html" | grep -oE 'href="[^"]+/releases/download/[^"]+\.AppImage"' | head -n1 | sed -E 's/^href="|"$//g' )" || true

    if [[ -z "${href:-}" ]]; then
      warn "EmuDeck: non trovo un asset .AppImage nella release $tag."
      warn "Pagina: $release_page"
      return 0
    fi

    if [[ "$href" == /* ]]; then
      download_url="https://github.com${href}"
    else
      download_url="$href"
    fi
  fi

  msg "EmuDeck: release $tag — download da: $download_url"

  local tmp
  tmp="$(mktemp "${dest}.tmp.XXXX")"
  curl -fL --retry 3 --retry-delay 2 -o "$tmp" "$download_url"
  chmod +x "$tmp"

  if [[ -f "$dest" ]]; then
    mv -f "$dest" "${dest}.OLD_$(date +%Y%m%d_%H%M%S)" || true
  fi
  mv -f "$tmp" "$dest"
  chmod +x "$dest"
  chown "$u:$u" "$dest" 2>/dev/null || true

  # Wrapper forcing extract-and-run (no libfuse2 needed)
  cat >"$wrapper" <<EOF
#!/usr/bin/env bash
set -euo pipefail
export APPIMAGE_EXTRACT_AND_RUN=1
exec "$dest" "\$@"
EOF
  chmod +x "$wrapper"
  chown "$u:$u" "$wrapper" 2>/dev/null || true

  # Link sul Desktop a EmuDeck.sh
  local desktop
  desktop="$(get_desktop_dir "$u")"
  mkdir -p "$desktop"
  chown "$u:$u" "$desktop" 2>/dev/null || true
  su - "$u" -c "ln -sf \"$wrapper\" \"$desktop/EmuDeck.sh\"" || true

  # Launcher in menu (no Desktop files)
  local app_dir="$home/.local/share/applications"
  local launcher="$app_dir/EmuDeck.desktop"
  mkdir -p "$app_dir"
  chown "$u:$u" "$home/.local" "$home/.local/share" "$app_dir" 2>/dev/null || true

  cat >"$launcher" <<EOF
[Desktop Entry]
Type=Application
Name=EmuDeck
Comment=EmuDeck (AppImage)
Exec=$wrapper
Terminal=false
Categories=Game;
EOF
  chmod 644 "$launcher" || true
  chown "$u:$u" "$launcher" 2>/dev/null || true

  msg "EmuDeck: pronto. Avvio da menu applicazioni o da: $wrapper"
}


# -----------------------------
# Base prerequisites
# -----------------------------
install_tools() {
  msg "Prerequisiti base…"
  apt_update
  apt_install sudo wget curl ca-certificates gnupg jq git unzip zenity rsync \
              build-essential dkms pkg-config \
              mesa-utils vulkan-tools \
              lm-sensors pciutils \
              python3 python3-pip python3-venv pipx \
              steam-devices || true
}

# -----------------------------
# Phase 1
# -----------------------------
phase1_kernel_install() {
  msg "Installo kernel+headers (dpkg -i)…"
  apt_update
  apt_install wget curl ca-certificates || true

  local tmp="/tmp/skillfish-kernel"
  mkdir -p "$tmp"
  local img="$tmp/linux-image-6.18.5-tkg-amd-bc-250-mt.deb"
  local hdr="$tmp/linux-headers-6.18.5-tkg-amd-bc-250-mt.deb"

  download_to "$KERNEL_IMAGE_URL" "$img"
  download_to "$KERNEL_HEADERS_URL" "$hdr"

  dpkg -i "$img" "$hdr" || true
  DEBIAN_FRONTEND=noninteractive apt-get -f install -y || true
  update-grub || true
}

already_on_target_kernel() {
  [[ "$(uname -r)" == "6.18.5-tkg-amd-bc-250-mt" ]]
}

prepare_phase2() {
  msg "Preparo continuazione (fase 2) dopo reboot…"
  mkdir -p "$STATE_DIR"

  # Save the interactive user who launched the script
  if [[ -n "${SUDO_USER:-}" && "${SUDO_USER}" != "root" ]]; then
    echo "${SUDO_USER}" >"$TARGET_USER_FILE"
  fi

  install -m 0755 "$(readlink -f "$0")" "$COPIED_SCRIPT"
  write_tail_helper
  write_autostart_desktop
  install_continuation_service
  echo "2" >"$PHASE_FILE"
}

# -----------------------------
# Phase 2
# -----------------------------
phase2_main() {
  msg "Skillfish OS setup — FASE 2"

  local codename; codename="$(detect_codename)"
  if [[ "$codename" == "forky" ]]; then
    disable_suite_sources "trixie"
  fi
  ensure_sources "$codename"

  install_tools
  ensure_mesa_min_version
  install_default_gaming_flatpaks
  install_gamemode
  install_coolercontrol
  install_bc250_smu_oc
  install_cyan_skillfish_governor
  install_nct6687_dkms

  local target; target="$(current_kernel_target)"
  purge_other_kernels "$target"
  install_emudeck_latest_appimage
  install_gnome_software_flatpak_plugin

  msg "Verifica Mesa in uso (comandi utili):"
  echo "  glxinfo -B | egrep 'OpenGL vendor|OpenGL renderer|OpenGL version'"
  echo "  vulkaninfo --summary | egrep -i 'driver|apiVersion|deviceName'"

  msg "Setup completato."
  echo "done" >"$PHASE_FILE"
  disable_continuation_service || true

  msg "Installazione completata: RIAVVIA MANUALMENTE il sistema per applicare tutte le modifiche."
  msg "Puoi riavviare dal menu o con: sudo reboot"
}

# -----------------------------
# Main
# -----------------------------
main() {
  ensure_root "$@"
  ensure_log
  mkdir -p "$STATE_DIR"

  if [[ "${1:-}" == "--phase2" ]]; then
    if [[ -f "$PHASE_FILE" && "$(cat "$PHASE_FILE")" == "2" ]]; then
      phase2_main
    else
      msg "Nessuna fase2 pendente. Esco."
    fi
    exit 0
  fi

  if already_on_target_kernel; then
    msg "Kernel target già in uso ($(uname -r)). Avvio direttamente fase 2."
    echo "2" >"$PHASE_FILE"
    phase2_main
    exit 0
  fi

  echo "1" >"$PHASE_FILE"
  phase1_kernel_install
  prepare_phase2

  msg "FASE 1 completata. Riavvio per avviare il kernel custom…"
  msg "Dopo il login, vedrai un terminale con: tail -f $LOG_FILE"
  sync || true
  systemctl reboot --force --no-block --ignore-inhibitors || shutdown -r now || reboot -f || true
}

main "$@"

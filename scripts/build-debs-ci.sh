#!/bin/bash
# Build the SkillFishOS app .debs from the repo sources (CI / clean machine).
# Unlike the on-box builders, every input comes from git — this catches the
# "stale binary packaged into a new version" failure mode before publishing.
set -euo pipefail
cd "$(dirname "$0")/.."
VER="${1:-0.0~ci$(date +%Y%m%d)}"
OUT="${OUT:-/tmp/sfx-debs}"
rm -rf "$OUT"; mkdir -p "$OUT/out"

put() { # put <pkg> <mode> <src> <dest-rel>
  [ -f "$3" ] || { echo "FATAL: missing source file $3" >&2; exit 1; }
  install -D -m "$2" "$3" "$OUT/$1/$4"
}
opt() { # like put, but optional
  [ -f "$3" ] && install -D -m "$2" "$3" "$OUT/$1/$4" || echo "  (optional, skipped: $3)"
}
putdir() { # putdir <pkg> <src-dir> <dest-rel-dir>: install a whole tree (0644)
  [ -d "$2" ] || { echo "FATAL: missing source dir $2" >&2; exit 1; }
  local f
  while IFS= read -r f; do
    install -D -m 0644 "$2/$f" "$OUT/$1/$3/$f"
  done < <(cd "$2" && find . -type f ! -name 'icon-theme.cache' -printf '%P\n')
}
ctrl() { # ctrl <pkg> <depends> <desc-first-line>
  mkdir -p "$OUT/$1/DEBIAN"
  printf 'Package: %s\nVersion: %s\nArchitecture: all\nMaintainer: SkillFishOS <info@skillfishos.com>\nDepends: %s\nSection: utils\nPriority: optional\nHomepage: https://skillfishos.com\nDescription: %s\n built from git by CI.\n' \
    "$1" "$VER" "$2" "$3" > "$OUT/$1/DEBIAN/control"
  printf '#!/bin/sh\nset -e\nupdate-desktop-database -q 2>/dev/null || true\ngtk-update-icon-cache -q -f /usr/share/icons/hicolor 2>/dev/null || true\nappstreamcli refresh-cache --force >/dev/null 2>&1 || true\nexit 0\n' > "$OUT/$1/DEBIAN/postinst"
  chmod 0755 "$OUT/$1/DEBIAN/postinst"
}
shot() { # shot <pkg> <metainfo-path>: install metainfo + its referenced screenshots
  put "$1" 0644 "$2" "usr/share/metainfo/$(basename "$2")"
  for s in $(grep -oE 'screenshots/[A-Za-z0-9._-]+' "$2" | sed 's#screenshots/##' | sort -u); do
    opt "$1" 0644 "screenshots/$s" "usr/share/skillfish/screenshots/$s"
  done
}

P=skillfish-tuner
put $P 0755 apps/tuner/skillfish-tuner            usr/local/bin/skillfish-tuner
put $P 0755 apps/tuner/skillfish-tuner-helper     usr/local/bin/skillfish-tuner-helper
put $P 0755 system/usr/local/bin/skillfish-cu     usr/local/bin/skillfish-cu
put $P 0755 system/usr/local/bin/skillfish-hud-val usr/local/bin/skillfish-hud-val
put $P 0755 system/usr/local/bin/skillfish-hud-bt usr/local/bin/skillfish-hud-bt
# Il lanciatore del HUD sta qui e non in un pacchetto suo perche' legge i due
# helper qui sopra: separarli permetterebbe di installarlo senza i sensori che
# gli servono. Deve essere un file eseguibile e non un comando dentro il
# .desktop: KDE converte l'autostart in un servizio systemd e in quel passaggio
# $HOME resta letterale, quindi conky non trovava la configurazione.
put $P 0755 system/usr/local/bin/skillfish-hud     usr/local/bin/skillfish-hud
put $P 0644 system/usr/share/skillfish/tuner-presets.json usr/share/skillfish/tuner-presets.json
put $P 0644 system/usr/share/applications/os.skillfish.Tuner.desktop usr/share/applications/os.skillfish.Tuner.desktop
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfish-tuner.png usr/share/icons/hicolor/256x256/apps/skillfish-tuner.png
put $P 0644 system/etc/systemd/system/skillfish-cu.service etc/systemd/system/skillfish-cu.service
opt $P 0644 system/usr/share/polkit-1/actions/os.skillfish.tuner.policy usr/share/polkit-1/actions/os.skillfish.tuner.policy
shot $P apps/tuner/os.skillfish.Tuner.metainfo.xml
ctrl $P "python3, python3-pyqt6, polkitd | policykit-1" "SkillFishOS Tuner - BC-250 hardware control GUI"

P=skillfish-hub
put $P 0755 apps/hub/skillfish-hub        usr/local/bin/skillfish-hub
put $P 0755 apps/hub/skillfish-hub-helper usr/local/bin/skillfish-hub-helper
put $P 0644 system/usr/share/applications/os.skillfish.hub.desktop usr/share/applications/os.skillfish.hub.desktop
# L'icona e' la borsa steampunk del NOSTRO tema — quella che SkillFishSteampunk
# usa per Discover, di cui l'Hub prende il posto nella barra — copiata come
# skillfish-hub invece di puntare al nome "plasmadiscover", che appartiene a
# plasma-discover-common: se togliessimo Discover dalla ISO l'Hub resterebbe con
# un quadrato vuoto.
# Qui vanno solo le copie in HICOLOR, che sono l'icona propria dell'Hub e
# funzionano con qualunque tema. La variante steampunk la spedisce
# skillfish-theme insieme al resto del tema: due pacchetti che scrivono nella
# stessa cartella del tema sarebbero un guaio inutile.
# I PNG servono perche' nel codice l'icona della finestra e' un PERCORSO passato
# a QPixmap, non un nome di tema.
put $P 0644 system/usr/share/icons/hicolor/scalable/apps/skillfish-hub.svg usr/share/icons/hicolor/scalable/apps/skillfish-hub.svg
put $P 0644 system/usr/share/icons/hicolor/48x48/apps/skillfish-hub.png   usr/share/icons/hicolor/48x48/apps/skillfish-hub.png
put $P 0644 system/usr/share/icons/hicolor/128x128/apps/skillfish-hub.png usr/share/icons/hicolor/128x128/apps/skillfish-hub.png
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfish-hub.png usr/share/icons/hicolor/256x256/apps/skillfish-hub.png
shot $P apps/hub/os.skillfish.hub.metainfo.xml
ctrl $P "python3, python3-pyqt6, python3-apt, gir1.2-appstream-1.0, appstream, curl, polkitd | policykit-1" "SkillFishOS Hub - Discover-style software centre"

P=skillfish-monitor
put $P 0755 apps/monitor/skillfish-monitor usr/local/bin/skillfish-monitor
put $P 0644 system/usr/share/applications/os.skillfish.monitor.desktop usr/share/applications/os.skillfish.monitor.desktop
put $P 0644 system/usr/share/mime/packages/os.skillfish.monitor.xml usr/share/mime/packages/os.skillfish.monitor.xml
shot $P apps/monitor/os.skillfish.monitor.metainfo.xml
ctrl $P "python3, python3-pyqt6" "SkillFishOS Monitor - live sensor charts + .sfmon benchmark analyzer"
# monitor ships a MIME type (.sfmon recordings) → also refresh the shared-mime db
printf '#!/bin/sh\nset -e\nupdate-mime-database /usr/share/mime >/dev/null 2>&1 || true\nupdate-desktop-database -q 2>/dev/null || true\nappstreamcli refresh-cache --force >/dev/null 2>&1 || true\nexit 0\n' > "$OUT/$P/DEBIAN/postinst"
chmod 0755 "$OUT/$P/DEBIAN/postinst"

P=skillfish-kernel-manager
put $P 0755 apps/kernel-manager/skillfish-kernel-manager usr/local/bin/skillfish-kernel-manager
put $P 0755 apps/kernel-manager/skillfish-kernel-helper  usr/local/bin/skillfish-kernel-helper
put $P 0644 system/usr/share/applications/os.skillfish.kernel.desktop usr/share/applications/os.skillfish.kernel.desktop
shot $P apps/kernel-manager/os.skillfish.kernel.metainfo.xml
ctrl $P "python3, python3-pyqt6, polkitd | policykit-1" "SkillFishOS Kernel Manager"

P=skillfish-ai-panel
put $P 0755 apps/ai-panel/skillfish-ai-panel usr/local/bin/skillfish-ai-panel
put $P 0755 apps/ai-panel/skillfish-gtt      usr/local/bin/skillfish-gtt
# the setup wizard shells out to this to install the Unsloth engine
put $P 0755 scripts/install-unsloth.sh       usr/local/share/skillfish/install-unsloth.sh
put $P 0644 system/usr/share/applications/os.skillfish.ai.desktop usr/share/applications/os.skillfish.ai.desktop
shot $P apps/ai-panel/os.skillfish.ai.metainfo.xml
ctrl $P "python3, python3-pyqt6, polkitd | policykit-1" "SkillFish AI - on-device LLM control panel"

P=skillfish-base
put $P 0755 system/usr/local/bin/skillfish-freeze-check.sh  usr/local/bin/skillfish-freeze-check.sh
put $P 0755 system/usr/local/bin/skillfish-freeze-notify.sh usr/local/bin/skillfish-freeze-notify.sh
put $P 0644 system/etc/systemd/system/skillfish-freeze-check.service etc/systemd/system/skillfish-freeze-check.service
put $P 0644 system/etc/xdg/autostart/skillfish-freeze-notify.desktop  etc/xdg/autostart/skillfish-freeze-notify.desktop
put $P 0644 system/etc/modules-load.d/skillfish-watchdog.conf         etc/modules-load.d/skillfish-watchdog.conf
put $P 0644 system/etc/systemd/system.conf.d/10-skillfish-watchdog.conf etc/systemd/system.conf.d/10-skillfish-watchdog.conf
put $P 0644 system/etc/modules-load.d/skillfish-nct6686.conf          etc/modules-load.d/skillfish-nct6686.conf
put $P 0644 system/etc/systemd/system/skillfish-wol.service          etc/systemd/system/skillfish-wol.service
put $P 0644 system/etc/modprobe.d/skillfish-nct6686.conf              etc/modprobe.d/skillfish-nct6686.conf
put $P 0644 system/etc/modules-load.d/skillfish-ntsync.conf           etc/modules-load.d/skillfish-ntsync.conf
put $P 0755 system/usr/local/bin/skillfish-core-unlock                usr/local/bin/skillfish-core-unlock
put $P 0755 system/usr/local/bin/skillfish-fix-boot-extents         usr/local/bin/skillfish-fix-boot-extents
put $P 0755 system/usr/local/bin/skillfish-is-bc250                usr/local/bin/skillfish-is-bc250
put $P 0644 system/etc/systemd/system/skillfish-sshd-keygen.service etc/systemd/system/skillfish-sshd-keygen.service
put $P 0644 system/etc/ssh/sshd_config.d/10-skillfish.conf        etc/ssh/sshd_config.d/10-skillfish.conf
put $P 0644 system/etc/systemd/coredump.conf.d/10-skillfish.conf  etc/systemd/coredump.conf.d/10-skillfish.conf
put $P 0644 system/etc/systemd/system/skillfish-core-unlock.service   etc/systemd/system/skillfish-core-unlock.service
put $P 0755 system/usr/local/bin/skillfish-gpu-freq-sampler           usr/local/bin/skillfish-gpu-freq-sampler
put $P 0644 system/etc/systemd/system/skillfish-gpu-freq.service      etc/systemd/system/skillfish-gpu-freq.service
put $P 0644 system/etc/skel/.config/conky/skillfish.conf              etc/skel/.config/conky/skillfish.conf
# L'autostart del HUD viaggia insieme alla configurazione conky qui sopra:
# spedire l'una senza l'altro lascia il HUD che non parte, oppure un autostart
# che punta a un file che non c'e'. Prima non apparteneva a NESSUN pacchetto,
# quindi arrivava solo a chi installava dalla ISO.
put $P 0644 system/etc/skel/.config/autostart/skillfish-conky.desktop etc/skel/.config/autostart/skillfish-conky.desktop
# skillfish-info: fastfetch in un terminale che resta aperto. Anche questi due
# non appartenevano a nessun pacchetto. Il comando sta in uno script perche' nel
# campo Exec di un .desktop "%s" e' un codice di sostituzione riservato e il "$"
# va raddoppiato: desktop-file-validate rifiutava la vecchia riga.
put $P 0755 system/usr/local/bin/skillfish-info                       usr/local/bin/skillfish-info
put $P 0644 system/usr/share/applications/skillfish-info.desktop      usr/share/applications/skillfish-info.desktop
put $P 0755 system/usr/local/bin/skillfish-acpi-pstates               usr/local/bin/skillfish-acpi-pstates
put $P 0644 system/usr/share/skillfish/acpi/SSDT-PST.aml              usr/share/skillfish/acpi/SSDT-PST.aml
put $P 0644 system/usr/share/skillfish/acpi/SSDT-PST.dsl              usr/share/skillfish/acpi/SSDT-PST.dsl
put $P 0644 system/usr/share/skillfish/acpi/SSDT-CST.aml              usr/share/skillfish/acpi/SSDT-CST.aml
put $P 0644 system/usr/share/skillfish/acpi/SSDT-CST.dsl              usr/share/skillfish/acpi/SSDT-CST.dsl
ctrl $P "systemd, libnotify-bin, python3, cpio, locales" "SkillFishOS base - hardware watchdog + freeze detector + 8-core unlock"
# base needs its own postinst: enable the watchdog and the freeze check.
# NOTE: core-unlock is only *enabled* (never --now): it warm-reboots the machine when
# it flips the mask, which must not happen during apt. It fires on the next boot.
cat > "$OUT/$P/DEBIAN/postinst" <<'POSTINST'
#!/bin/sh
set -e
if [ -d /run/systemd/system ]; then
  systemctl daemon-reload || true
  # senza chiavi host ssh.service fallisce all'infinito su installazione fresca
  systemctl enable skillfish-sshd-keygen.service || true
  [ -f /etc/ssh/ssh_host_ed25519_key ] || ssh-keygen -A || true
  systemctl enable --now skillfish-freeze-check.service || true
  systemctl enable skillfish-core-unlock.service || true
  # ntsync serve a Proton: caricalo subito, non al prossimo riavvio
  modprobe ntsync 2>/dev/null || true
  # guardia hardware sui servizi specifici della BC-250: senza, su un PC
  # normale ripartono ogni 5 secondi all'infinito
  for u in cyan-skillfish-governor skillfish-core-unlock skillfish-cu            skillfish-gpu-freq skillfish-gpu-util skillfish-thermal-guard            skillfish-dp-hotswap; do
    f=""
    for d in /etc/systemd/system /usr/lib/systemd/system; do
      [ -f "$d/$u.service" ] && { f="$d/$u.service"; break; }
    done
    [ -n "$f" ] || continue
    grep -q 'ExecCondition=/usr/local/bin/skillfish-is-bc250' "$f" && continue
    grep -q '^ExecStart=' "$f" || continue
    # Il ritorno a capo va scritto come \n nella sostituzione. Prima c'era un
    # a capo VERO dentro le virgolette singole, e sed rispondeva
    #   sed: -e expression #1, char 65: unterminated `s' command
    # cioe' non inseriva NIENTE: la guardia hardware non e' mai stata aggiunta a
    # questi servizi, che e' proprio il guasto che doveva evitare.
    sed -i '0,/^ExecStart=/s|^ExecStart=|ExecCondition=/usr/local/bin/skillfish-is-bc250\nExecStart=|' "$f" || true
  done
  systemctl daemon-reload || true
  systemctl enable --now skillfish-gpu-freq.service || true
  systemctl enable --now skillfish-wol.service || true
  modprobe sp5100_tco 2>/dev/null || true
  modprobe nct6687 force=1 2>/dev/null || true
  systemctl daemon-reexec || true
fi

# ACPI P-states: the BC-250 firmware exposes no _PSS, so Linux has no cpufreq at all.
# The helper injects an SSDT via GRUB's early initrd and no-ops on anything that is
# not a BC-250. It only rewrites the GRUB config — the change lands on next boot.
/usr/local/bin/skillfish-acpi-pstates enable || true

# HUD migration: the desktop widget was wired for 6c/12t. Now that the 8 cores are
# unlocked it needs 16 bars. Only the two cpubar rows are rewritten, and only when
# they still match what we originally shipped — any other customisation is kept,
# and a hand-edited HUD is left alone.
OLD_A='${voffset 3}${color D8A849}${cpubar cpu1 6,16} ${cpubar cpu2 6,16} ${cpubar cpu3 6,16} ${cpubar cpu4 6,16} ${cpubar cpu5 6,16} ${cpubar cpu6 6,16}'
OLD_B='${voffset 2}${color D8A849}${cpubar cpu7 6,16} ${cpubar cpu8 6,16} ${cpubar cpu9 6,16} ${cpubar cpu10 6,16} ${cpubar cpu11 6,16} ${cpubar cpu12 6,16}'
NEW_A='${voffset 3}${color D8A849}${cpubar cpu1 6,16} ${cpubar cpu2 6,16} ${cpubar cpu3 6,16} ${cpubar cpu4 6,16} ${cpubar cpu5 6,16} ${cpubar cpu6 6,16} ${cpubar cpu7 6,16} ${cpubar cpu8 6,16}'
NEW_B='${voffset 2}${color D8A849}${cpubar cpu9 6,16} ${cpubar cpu10 6,16} ${cpubar cpu11 6,16} ${cpubar cpu12 6,16} ${cpubar cpu13 6,16} ${cpubar cpu14 6,16} ${cpubar cpu15 6,16} ${cpubar cpu16 6,16}'
for cfg in /home/*/.config/conky/skillfish.conf /root/.config/conky/skillfish.conf; do
  [ -f "$cfg" ] || continue
  grep -qF "$OLD_B" "$cfg" || continue
  python3 - "$cfg" "$OLD_A" "$OLD_B" "$NEW_A" "$NEW_B" <<'PY' || true
import sys
p, oa, ob, na, nb = sys.argv[1:6]
t = open(p, encoding='utf-8').read()
open(p, 'w', encoding='utf-8').write(t.replace(oa, na).replace(ob, nb))
PY
  echo "skillfish-base: HUD aggiornato a 16 thread in $cfg"
done

# Le quattro lingue di SkillFishOS.
#
# Le traduzioni polacche (di cyryllo) sono nelle app da mesi, ma sull'immagine
# risultavano generati solo en_US e it_IT: senza il locale generato, KDE non
# mostra la lingua nel menu delle impostazioni e SDDM non la offre. Il polacco
# era quindi presente nel codice e irraggiungibile per l'utente. Verificato
# sulla scheda con `locale -a`: due voci in tutto.
#
# Qui li abilitiamo tutti e quattro in locale.gen e rigeneriamo, ma solo se
# qualcosa e' davvero cambiato: locale-gen ci mette parecchio e non ha senso
# rifarlo a ogni aggiornamento del pacchetto.
if [ -f /etc/locale.gen ]; then
  need=0
  for l in en_US.UTF-8 it_IT.UTF-8 pl_PL.UTF-8 uk_UA.UTF-8; do
    if grep -qE "^${l} UTF-8" /etc/locale.gen; then
      continue
    elif grep -qE "^[#[:space:]]*${l} UTF-8" /etc/locale.gen; then
      sed -i "s|^[#[:space:]]*\(${l} UTF-8\)|\1|" /etc/locale.gen
      need=1
    else
      echo "${l} UTF-8" >> /etc/locale.gen
      need=1
    fi
  done
  if [ "$need" = 1 ]; then
    echo "skillfish-base: genero i locale it/en/pl/uk (ci vuole qualche secondo)"
    locale-gen >/dev/null 2>&1 || true
  fi
fi

exit 0
POSTINST
# On removal the SSDT would vanish while GRUB still referenced it, so undo the
# bootloader change before the files go away.
cat > "$OUT/$P/DEBIAN/prerm" <<'PRERM'
#!/bin/sh
set -e
if [ "$1" = remove ] || [ "$1" = purge ]; then
  [ -x /usr/local/bin/skillfish-acpi-pstates ] && /usr/local/bin/skillfish-acpi-pstates disable || true
fi
exit 0
PRERM
chmod 0755 "$OUT/$P/DEBIAN/postinst" "$OUT/$P/DEBIAN/prerm"

P=skillfish-console
put $P 0755 system/usr/local/bin/skillfish-gaming-mode usr/local/bin/skillfish-gaming-mode
put $P 0644 system/usr/share/wayland-sessions/skillfish-gaming.desktop usr/share/wayland-sessions/skillfish-gaming.desktop
# Il comando che permette di USCIRE dalla console. Con -steamos3 Steam crede di
# essere su SteamOS e per tornare al desktop esegue `steamos-session-select
# desktop`: da noi non esisteva, quindi restava per sempre su "passaggio al
# desktop in corso".
#
# Due copie: una sull'host, una in /opt perche' Steam e' un flatpak e lo esegue
# DENTRO il sandbox. Non puo' stare sotto /usr — li' il sandbox ha gia' il
# proprio runtime e flatpak si rifiuta di montarci sopra il percorso dell'host.
put $P 0755 system/usr/local/bin/steamos-session-select usr/local/bin/steamos-session-select
put $P 0755 system/usr/local/bin/steamos-session-select opt/skillfish/steam-bin/steamos-session-select
ctrl $P "gamescope, flatpak" "SkillFishOS Console - SteamOS-style Big Picture session"
# Steam deve poter trovare ed eseguire quel comando: la cartella, il PATH del
# sandbox e il permesso di parlare col servizio Flatpak, che serve a
# flatpak-spawn per agire sull'host.
cat > "$OUT/$P/DEBIAN/postinst" <<'POSTCONS'
#!/bin/sh
set -e
if command -v flatpak >/dev/null 2>&1; then
  flatpak override --system com.valvesoftware.Steam       --filesystem=/opt/skillfish/steam-bin:ro       --talk-name=org.freedesktop.Flatpak       --env=PATH=/opt/skillfish/steam-bin:/app/bin:/app/utils/bin:/usr/bin 2>/dev/null || true
fi
exit 0
POSTCONS
chmod 0755 "$OUT/$P/DEBIAN/postinst"

P=skillfish-dashboard
put $P 0755 apps/dashboard/skillfish-dashboardd      usr/local/bin/skillfish-dashboardd
put $P 0755 apps/dashboard/skillfish-remote-manager  usr/local/bin/skillfish-remote-manager
put $P 0755 apps/dashboard/skillfish-remote-ctl      usr/local/bin/skillfish-remote-ctl
put $P 0755 apps/dashboard/skillfish-hub-catalog     usr/local/bin/skillfish-hub-catalog
put $P 0644 apps/dashboard/web/index.html  usr/share/skillfish/dashboard/index.html
put $P 0644 apps/dashboard/web/app.js      usr/share/skillfish/dashboard/app.js
put $P 0644 apps/dashboard/web/aichat.html usr/share/skillfish/dashboard/aichat.html
put $P 0644 apps/dashboard/web/tuner.html  usr/share/skillfish/dashboard/tuner.html
put $P 0644 apps/dashboard/web/hub.html    usr/share/skillfish/dashboard/hub.html
put $P 0644 system/etc/skillfish/dashboard.json usr/share/skillfish/dashboard-default.json
put $P 0644 system/etc/systemd/system/skillfish-dashboard.service etc/systemd/system/skillfish-dashboard.service
put $P 0644 system/usr/share/applications/os.skillfish.remote-manager.desktop usr/share/applications/os.skillfish.remote-manager.desktop
opt $P 0644 system/usr/share/polkit-1/actions/os.skillfish.remote-manager.policy usr/share/polkit-1/actions/os.skillfish.remote-manager.policy
mkdir -p "$OUT/$P/DEBIAN"
cat > "$OUT/$P/DEBIAN/control" <<EOF
Package: skillfish-dashboard
Version: $VER
Architecture: all
Maintainer: SkillFishOS <info@skillfishos.com>
Depends: python3, python3-pyqt6, python3-apt, gir1.2-appstream-1.0, appstream, curl, openssl, polkitd | policykit-1
Recommends: ttyd, novnc, websockify, x11vnc, ethtool, wakeonlan, flatpak, snapd
Suggests: zerotier-one, docker.io
Section: utils
Priority: optional
Homepage: https://skillfishos.com
Description: SkillFishOS Remote Manager - web control dashboard for the BC-250
 A modular, self-hosted web dashboard (PAM login over HTTPS) to control the
 board remotely: live telemetry, software KVM (noVNC), web terminal (ttyd),
 the Tuner (CPU/GPU/compute-unit control), a full Hub app store, AI/OpenWebUI,
 logs, Wake-on-LAN and ZeroTier. Ships the always-available daemon plus the
 native Remote Manager toggle app. Built from git by CI.
EOF
printf '#!/bin/sh\nset -e\nmkdir -p /etc/skillfish\n[ -f /etc/skillfish/dashboard.json ] || cp /usr/share/skillfish/dashboard-default.json /etc/skillfish/dashboard.json\nif [ -d /run/systemd/system ]; then systemctl daemon-reload || true; fi\nupdate-desktop-database -q 2>/dev/null || true\nexit 0\n' > "$OUT/$P/DEBIAN/postinst"
printf '#!/bin/sh\nset -e\nif [ "$1" = remove ] || [ "$1" = purge ]; then systemctl disable --now skillfish-dashboard.service 2>/dev/null || true; fi\nexit 0\n' > "$OUT/$P/DEBIAN/prerm"
chmod 0755 "$OUT/$P/DEBIAN/postinst" "$OUT/$P/DEBIAN/prerm"

P=skillfish-theme
# The steampunk look used to be baked into the ISO filesystem only (no package
# owned it), so a fix could not reach installed systems through apt. It ships
# as a package now — same paths, so it simply takes ownership of the files.
putdir $P theme/icons/SkillFishSteampunk              usr/share/icons/SkillFishSteampunk
putdir $P theme/cursors/SkillFish-Steampunk-Cursors   usr/share/icons/SkillFish-Steampunk-Cursors
putdir $P theme/plasma-theme/SkillFishSteampunk       usr/share/plasma/desktoptheme/SkillFishSteampunk
putdir $P theme/look-and-feel/org.skillfish.steampunk usr/share/plasma/look-and-feel/org.skillfish.steampunk
putdir $P theme/Kvantum/SkillFishSteampunk            usr/share/Kvantum/SkillFishSteampunk
put $P 0644 theme/color-scheme/SkillFishSteampunk.colors usr/share/color-schemes/SkillFishSteampunk.colors
# Lo sfondo come vero PACCHETTO wallpaper, non come PNG sciolto.
# Plasma, nella chiave Image= del look-and-feel, si aspetta una cartella con
# metadata.json e contents/images/: davanti a un file singolo non lo risolve e
# ricade sullo sfondo predefinito. Ecco perche' nessuno vedeva il nostro sfondo
# ne' nella live ne' dopo l'installazione. Il percorso e' dichiarato in
# theme/look-and-feel/org.skillfish.steampunk/contents/defaults.
#
# Queste righe stavano piu' in basso, in mezzo ai controlli: giravano dopo
# dpkg-deb e i file non entravano mai nel pacchetto.
put $P 0644 system/usr/share/wallpapers/SkillFishOS/metadata.json \
    usr/share/wallpapers/SkillFishOS/metadata.json
put $P 0644 system/usr/share/wallpapers/SkillFishOS/contents/images/3840x2160.png \
    usr/share/wallpapers/SkillFishOS/contents/images/3840x2160.png
# Il desktop preconfigurato che ogni nuovo utente eredita. Era un file orfano
# sul disco della scheda, come lo sfondo: nessun pacchetto lo possedeva, quindi
# una correzione non poteva raggiungere chi aveva gia' installato.
#
# La sua chiave Image= vince su quella del look-and-feel, ed e' il motivo per
# cui il pacchetto wallpaper da solo non bastava: puntava ancora al PNG grezzo
# e Plasma, davanti a un file singolo, ricade sul proprio sfondo predefinito.
put $P 0644 system/etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc     etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc
# Lo sfondo va IMPOSTATO, non solo dichiarato: Plasma riscrive appletsrc al
# primo accesso e butta via la nostra riga. Questo lo applica dopo.
put $P 0755 system/usr/local/bin/skillfish-first-login-wallpaper usr/local/bin/skillfish-first-login-wallpaper
# Il tema della schermata di accesso non apparteneva a NESSUN pacchetto: viveva
# solo nel filesystem della ISO, quindi una correzione non poteva raggiungere
# via apt chi aveva gia' installato. E ce n'era una da fare: le scritte erano
# cablate in italiano ("Accedi") anche in polacco e ucraino — la primissima cosa
# che si vede del sistema, nella lingua sbagliata.
putdir $P system/usr/share/sddm/themes/skillfish-brass usr/share/sddm/themes/skillfish-brass
put $P 0644 system/etc/skel/.config/autostart/skillfish-wallpaper.desktop etc/skel/.config/autostart/skillfish-wallpaper.desktop
for a in theme/avatars/steampunk-*.png; do
  put $P 0644 "$a" "usr/share/plasma/avatars/$(basename "$a")"
done
ctrl $P "hicolor-icon-theme" "SkillFishOS Steampunk theme - icons, cursors, Plasma theme and colours"
# NON generare una icon-theme.cache per i nostri temi: TOGLIERLA.
#
# Qui c'era `gtk-update-icon-cache -f` sul tema, con `|| rm -f` come ripiego.
# L'intenzione era "costruisci la cache, e se non ci riesci togli quella
# vecchia". Ma il comando RIESCE, e la cache che produce Qt non la sa usare:
# risultato, tutti i lanciatori della barra diventano fogli bianchi. Successo
# davvero l'11/08/2026 sulla scheda, e sarebbe ricapitato su OGNI macchina a
# ogni aggiornamento del pacchetto.
#
# Senza cache Qt legge direttamente le cartelle del tema, che funziona sempre.
# La cache di hicolor invece va aggiornata, e la fa gia' ctrl().
printf '#!/bin/sh\nset -e\nfor t in SkillFishSteampunk SkillFish-Steampunk-Cursors; do\n  rm -f "/usr/share/icons/$t/icon-theme.cache" 2>/dev/null || true\ndone\nexit 0\n' > "$OUT/$P/DEBIAN/postinst"
chmod 0755 "$OUT/$P/DEBIAN/postinst"

echo "== building =="
P=skillfish-iso-mount
# Era rimasto nel vecchio apps/build-debs.sh, che prende i file dal disco della
# scheda: fuori dalla catena automatica, quindi fermo a 26.06 mentre tutto il
# resto avanzava, e una correzione qui non sarebbe mai arrivata a nessuno.
put $P 0755 system/usr/local/bin/skillfish-iso-mount usr/local/bin/skillfish-iso-mount
put $P 0644 system/usr/share/kio/servicemenus/skillfish-iso.desktop usr/share/kio/servicemenus/skillfish-iso.desktop
put $P 0644 system/etc/polkit-1/rules.d/49-skillfish-udisks.rules etc/polkit-1/rules.d/49-skillfish-udisks.rules
ctrl $P "udisks2, polkitd | policykit-1" "SkillFishOS native ISO mounting for KDE"

P=skillfish-menu
# Questo non stava in NESSUNO script: esisteva solo come .deb costruito a mano
# chissa' quando. Definisce la categoria "SkillFishOS" nel menu delle
# applicazioni — i due .menu (uno per il menu XDG, uno per quello di Plasma) e
# la voce di categoria con nome e descrizione.
put $P 0644 system/etc/xdg/menus/applications-merged/skillfishos.menu etc/xdg/menus/applications-merged/skillfishos.menu
put $P 0644 system/etc/xdg/menus/plasma-applications-merged/skillfishos.menu etc/xdg/menus/plasma-applications-merged/skillfishos.menu
put $P 0644 system/usr/share/desktop-directories/skillfishos.directory usr/share/desktop-directories/skillfishos.directory
ctrl $P "" "SkillFishOS application menu group"

P=skillfish-emulators
# Gli emulatori NON possono viaggiare nella ISO: EmuDeck installa tutto nella
# home dell'utente (flatpak --user e AppImage in ~/Applications), e la ISO
# replica /etc/skel, non la home di chi ha costruito il sistema. Vanno quindi
# reinstallati su ogni macchina, e servono due voci nel menu GIOCHI — che e'
# esattamente dove si va a cercarli e non si trovava niente.
# Due voci e non una perche' fanno cose diverse: EmuDeck configura anche
# cartelle ROM, BIOS e controlli ma nasce per Steam Deck; l'altro prende singoli
# emulatori da Flathub e basta.
put $P 0755 scripts/install-emudeck.sh    usr/local/share/skillfish/install-emudeck.sh
put $P 0755 scripts/install-emulators.sh  usr/local/share/skillfish/install-emulators.sh
put $P 0644 system/usr/share/applications/os.skillfish.emudeck.desktop   usr/share/applications/os.skillfish.emudeck.desktop
put $P 0644 system/usr/share/applications/os.skillfish.emulators.desktop usr/share/applications/os.skillfish.emulators.desktop
ctrl $P "flatpak, curl" "SkillFishOS Emulators - install emulators after the installation"

for P in skillfish-tuner skillfish-hub skillfish-monitor skillfish-kernel-manager skillfish-ai-panel skillfish-base skillfish-console skillfish-dashboard skillfish-theme skillfish-emulators skillfish-iso-mount skillfish-menu; do
  find "$OUT/$P" -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
  dpkg-deb --root-owner-group --build "$OUT/$P" "$OUT/out/${P}_${VER}_all.deb" >/dev/null
done
ls -l "$OUT/out"

echo "== content verification (the bogus-deb guard) =="
check() { dpkg-deb --fsys-tarfile "$OUT/out/$1" | tar -xO "$2" | grep "$3" >/dev/null \
  && echo "OK  $1: $2 contains '$3'" || { echo "FAIL $1: $2 missing '$3'" >&2; exit 1; }; }
check skillfish-tuner_${VER}_all.deb         ./usr/local/bin/skillfish-tuner-helper  gov-mode
check skillfish-tuner_${VER}_all.deb         ./usr/local/bin/skillfish-tuner         gov_perf
check skillfish-hub_${VER}_all.deb           ./usr/local/bin/skillfish-hub           "return None"
check skillfish-kernel-manager_${VER}_all.deb ./usr/local/bin/skillfish-kernel-manager skillfish
check skillfish-ai-panel_${VER}_all.deb      ./usr/local/bin/skillfish-ai-panel       skillfish
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-freeze-check.sh unclean-shutdown
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-core-unlock     0x5A870
check skillfish-base_${VER}_all.deb          ./etc/modules-load.d/skillfish-ntsync.conf ntsync
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-fix-boot-extents reflink=never
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-is-bc250        0x13fe
check skillfish-base_${VER}_all.deb          ./etc/systemd/system/skillfish-sshd-keygen.service ssh-keygen
check skillfish-base_${VER}_all.deb          ./etc/ssh/sshd_config.d/10-skillfish.conf PasswordAuthentication
check skillfish-base_${VER}_all.deb          ./etc/systemd/coredump.conf.d/10-skillfish.conf ExternalSizeMax
check skillfish-tuner_${VER}_all.deb         ./usr/local/bin/skillfish-tuner          _silicon
check skillfish-console_${VER}_all.deb       ./opt/skillfish/steam-bin/steamos-session-select flatpak-spawn
check skillfish-console_${VER}_all.deb       ./usr/local/bin/skillfish-gaming-mode    /usr/games
check skillfish-monitor_${VER}_all.deb       ./usr/local/bin/skillfish-monitor        SFMON_EXT
check skillfish-dashboard_${VER}_all.deb     ./usr/local/bin/skillfish-dashboardd     "SkillFish Remote"
check skillfish-dashboard_${VER}_all.deb     ./usr/local/bin/skillfish-hub-catalog    AppStream
check skillfish-dashboard_${VER}_all.deb     ./usr/share/skillfish/dashboard/hub.html "SkillFishOS Hub"
# Il HUD: il lanciatore deve esserci E deve contenere il controllo
# sull'hardware, altrimenti partirebbe su PC dove la finestra collassa a 15x15.
check skillfish-tuner_${VER}_all.deb         ./usr/local/bin/skillfish-hud            skillfish-is-bc250
# L'autostart deve chiamare il percorso assoluto: con "sh -c" e le virgolette,
# KDE lo converte in servizio systemd e $HOME resta letterale.
check skillfish-base_${VER}_all.deb          ./etc/skel/.config/autostart/skillfish-conky.desktop "Exec=/usr/local/bin/skillfish-hud"
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-info           fastfetch
# L'icona dell'Hub: che sia davvero un'immagine e non un file vuoto.
check skillfish-hub_${VER}_all.deb           ./usr/share/icons/hicolor/scalable/apps/skillfish-hub.svg "svg"
# Gli emulatori: il repository giusto e' emudeck-electron, non dragoonDorise —
# quest'ultimo non ha allegati nelle release e lo scaricamento fallirebbe.
check skillfish-emulators_${VER}_all.deb     ./usr/local/share/skillfish/install-emudeck.sh   emudeck-electron
check skillfish-emulators_${VER}_all.deb     ./usr/local/share/skillfish/install-emulators.sh flathub
# I due pacchetti rientrati oggi nella catena automatica: erano fermi a 26.06
# perche' uno stava nel vecchio script e l'altro in nessuno.
check skillfish-iso-mount_${VER}_all.deb    ./usr/local/bin/skillfish-iso-mount              udisks
# Si cerca il TESTO polacco, non la chiave "Comment[pl]": quella passa a grep
# come espressione regolare, dove [pl] vale "un carattere fra p e l" e non
# combacia mai. Cercare la traduzione vera verifica anche di piu'.
check skillfish-menu_${VER}_all.deb         ./usr/share/desktop-directories/skillfishos.directory "Narzędzia SkillFishOS"
# Nella barra deve esserci il NOSTRO Hub. Il collegamento a Discover era rimasto
# solo nello skel, quindi non si vedeva sulla board — dove il pannello era gia'
# stato sistemato a mano — ma lo ereditava chiunque installasse da ISO.
check skillfish-theme_${VER}_all.deb         ./etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc os.skillfish.hub.desktop
# La schermata di accesso non deve piu' dire "Accedi" a un polacco: si controlla
# che il testo passi dalla funzione di traduzione e non sia piu' una costante.
check skillfish-theme_${VER}_all.deb         ./usr/share/sddm/themes/skillfish-brass/Main.qml "root.tr(root.txtLogin)"
# I diacritici polacchi nei preset: "Wydajnosc" non esiste, si scrive
# "Wydajnosc" con la n accentata. Senza questo controllo tornerebbero a perdersi.
check skillfish-tuner_${VER}_all.deb         ./usr/share/skillfish/tuner-presets.json "Wydajność"
check skillfish-theme_${VER}_all.deb         ./usr/share/icons/SkillFishSteampunk/index.theme        SkillFish
# guard: the icon must paint with its OWN gradient — a dangling cross-icon ref
# renders as an empty frame on qt6-svg >= 6.10.2-9 (see fix-icon-gradient-refs.py)
check skillfish-theme_${VER}_all.deb ./usr/share/icons/SkillFishSteampunk/scalable/actions/document-open.svg document_open_copper
check skillfish-theme_${VER}_all.deb ./usr/share/wallpapers/SkillFishOS/metadata.json SkillFishOS
check skillfish-theme_${VER}_all.deb ./etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc usr/share/wallpapers/SkillFishOS
check skillfish-theme_${VER}_all.deb ./usr/local/bin/skillfish-first-login-wallpaper plasma-apply-wallpaperimage
check skillfish-theme_${VER}_all.deb ./usr/share/plasma/look-and-feel/org.skillfish.steampunk/contents/defaults usr/share/wallpapers/SkillFishOS
echo "ALL DEBS VERIFIED"

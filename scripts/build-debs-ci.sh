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
put $P 0644 system/etc/systemd/system/skillfish-core-unlock.service   etc/systemd/system/skillfish-core-unlock.service
put $P 0755 system/usr/local/bin/skillfish-gpu-freq-sampler           usr/local/bin/skillfish-gpu-freq-sampler
put $P 0644 system/etc/systemd/system/skillfish-gpu-freq.service      etc/systemd/system/skillfish-gpu-freq.service
put $P 0644 system/etc/skel/.config/conky/skillfish.conf              etc/skel/.config/conky/skillfish.conf
put $P 0755 system/usr/local/bin/skillfish-acpi-pstates               usr/local/bin/skillfish-acpi-pstates
put $P 0644 system/usr/share/skillfish/acpi/SSDT-PST.aml              usr/share/skillfish/acpi/SSDT-PST.aml
put $P 0644 system/usr/share/skillfish/acpi/SSDT-PST.dsl              usr/share/skillfish/acpi/SSDT-PST.dsl
put $P 0644 system/usr/share/skillfish/acpi/SSDT-CST.aml              usr/share/skillfish/acpi/SSDT-CST.aml
put $P 0644 system/usr/share/skillfish/acpi/SSDT-CST.dsl              usr/share/skillfish/acpi/SSDT-CST.dsl
ctrl $P "systemd, libnotify-bin, python3, cpio" "SkillFishOS base - hardware watchdog + freeze detector + 8-core unlock"
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
    sed -i '0,/^ExecStart=/s##ExecCondition=/usr/local/bin/skillfish-is-bc250
ExecStart=#' "$f" || true
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
ctrl $P "gamescope, flatpak" "SkillFishOS Console - SteamOS-style Big Picture session"

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
for a in theme/avatars/steampunk-*.png; do
  put $P 0644 "$a" "usr/share/plasma/avatars/$(basename "$a")"
done
ctrl $P "hicolor-icon-theme" "SkillFishOS Steampunk theme - icons, cursors, Plasma theme and colours"
# refresh the icon cache of our own themes (and drop any stale one we replaced)
printf '#!/bin/sh\nset -e\nfor t in SkillFishSteampunk SkillFish-Steampunk-Cursors; do\n  [ -d "/usr/share/icons/$t" ] || continue\n  gtk-update-icon-cache -q -f "/usr/share/icons/$t" 2>/dev/null || rm -f "/usr/share/icons/$t/icon-theme.cache" 2>/dev/null || true\ndone\nexit 0\n' > "$OUT/$P/DEBIAN/postinst"
chmod 0755 "$OUT/$P/DEBIAN/postinst"

echo "== building =="
for P in skillfish-tuner skillfish-hub skillfish-monitor skillfish-kernel-manager skillfish-ai-panel skillfish-base skillfish-console skillfish-dashboard skillfish-theme; do
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
check skillfish-tuner_${VER}_all.deb         ./usr/local/bin/skillfish-tuner          _silicon
check skillfish-monitor_${VER}_all.deb       ./usr/local/bin/skillfish-monitor        SFMON_EXT
check skillfish-dashboard_${VER}_all.deb     ./usr/local/bin/skillfish-dashboardd     "SkillFish Remote"
check skillfish-dashboard_${VER}_all.deb     ./usr/local/bin/skillfish-hub-catalog    AppStream
check skillfish-dashboard_${VER}_all.deb     ./usr/share/skillfish/dashboard/hub.html "SkillFishOS Hub"
check skillfish-theme_${VER}_all.deb         ./usr/share/icons/SkillFishSteampunk/index.theme        SkillFish
# guard: the icon must paint with its OWN gradient — a dangling cross-icon ref
# renders as an empty frame on qt6-svg >= 6.10.2-9 (see fix-icon-gradient-refs.py)
check skillfish-theme_${VER}_all.deb ./usr/share/icons/SkillFishSteampunk/scalable/actions/document-open.svg document_open_copper
echo "ALL DEBS VERIFIED"

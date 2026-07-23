#!/bin/bash
# Build SkillFishOS app .debs from the installed (working) files on the box.
set -euo pipefail
VER="26.06"
OUT=/tmp/debs
rm -rf "$OUT"; mkdir -p "$OUT/out"

stage() { # stage <pkgdir> ; creates DEBIAN dir
  mkdir -p "$OUT/$1/DEBIAN"
}
cp_into() { # cp_into <pkgdir> <src> <dest-rel>  (dest-rel under pkg root, no leading /)
  local d="$OUT/$1/$3"
  install -D -m "${4:-0644}" "$2" "$d"
}

############ skillfish-tuner ############
P=skillfish-tuner; stage $P
cp_into $P /usr/local/bin/skillfish-tuner         usr/local/bin/skillfish-tuner        0755
cp_into $P /usr/local/bin/skillfish-tuner-helper  usr/local/bin/skillfish-tuner-helper 0755
cp_into $P /usr/local/bin/skillfish-cu            usr/local/bin/skillfish-cu           0755
cp_into $P /usr/local/bin/skillfish-hud-val       usr/local/bin/skillfish-hud-val      0755
cp_into $P /usr/local/bin/skillfish-hud-bt        usr/local/bin/skillfish-hud-bt       0755
cp_into $P /usr/share/skillfish/tuner-presets.json usr/share/skillfish/tuner-presets.json
cp_into $P /usr/share/applications/os.skillfish.Tuner.desktop usr/share/applications/os.skillfish.Tuner.desktop
cp_into $P /usr/share/icons/hicolor/256x256/apps/skillfish-tuner.png usr/share/icons/hicolor/256x256/apps/skillfish-tuner.png
[ -f /usr/share/icons/hicolor/128x128/apps/skillfish-tuner.png ] && cp_into $P /usr/share/icons/hicolor/128x128/apps/skillfish-tuner.png usr/share/icons/hicolor/128x128/apps/skillfish-tuner.png || true
cp_into $P /etc/systemd/system/skillfish-cu.service etc/systemd/system/skillfish-cu.service
cat > "$OUT/$P/DEBIAN/control" <<EOF
Package: skillfish-tuner
Version: $VER
Architecture: all
Maintainer: SkillFishOS <info@skillfishos.com>
Depends: python3, python3-pyqt6, polkitd | policykit-1
Recommends: umr
Section: utils
Priority: optional
Homepage: https://skillfishos.com
Description: SkillFishOS Tuner - BC-250 hardware control GUI
 PyQt6 desktop app to control the AMD BC-250 with no terminal: CPU
 overclock/undervolt, GPU governor safe-point, fan curve, UMA VRAM split and
 live 40 Compute Unit control with per-WGP health tests and a live monitor
 (temperature, frequency, voltage, fan). Talks to a privileged JSON helper via
 a single polkit authentication.
EOF
cat > "$OUT/$P/DEBIAN/postinst" <<'EOF'
#!/bin/sh
set -e
if [ -d /run/systemd/system ]; then
  systemctl daemon-reload || true
  systemctl enable skillfish-cu.service || true
fi
gtk-update-icon-cache -q -f /usr/share/icons/hicolor 2>/dev/null || true
update-desktop-database -q 2>/dev/null || true
exit 0
EOF
chmod 0755 "$OUT/$P/DEBIAN/postinst"

############ skillfish-ai-panel ############
P=skillfish-ai-panel; stage $P
cp_into $P /usr/local/bin/skillfish-ai-panel usr/local/bin/skillfish-ai-panel 0755
cp_into $P /usr/local/bin/skillfish-gtt usr/local/bin/skillfish-gtt 0755
cp_into $P /usr/share/applications/os.skillfish.ai.desktop usr/share/applications/os.skillfish.ai.desktop
[ -f /usr/share/icons/hicolor/256x256/apps/skillfish-ai.png ] && cp_into $P /usr/share/icons/hicolor/256x256/apps/skillfish-ai.png usr/share/icons/hicolor/256x256/apps/skillfish-ai.png || true
cat > "$OUT/$P/DEBIAN/control" <<EOF
Package: skillfish-ai-panel
Version: $VER
Architecture: all
Maintainer: SkillFishOS <info@skillfishos.com>
Depends: python3, python3-pyqt6, polkitd | policykit-1
Recommends: docker.io | docker-ce, ollama
Section: utils
Priority: optional
Homepage: https://skillfishos.com
Description: SkillFish AI - on-device LLM control panel
 PyQt6 panel to start/stop the local LLM stack (Ollama + Vulkan) on the AMD
 BC-250 integrated GPU with one click, freeing GPU memory and RAM for gaming
 when the assistant is not in use.
EOF
cat > "$OUT/$P/DEBIAN/postinst" <<'EOF'
#!/bin/sh
set -e
gtk-update-icon-cache -q -f /usr/share/icons/hicolor 2>/dev/null || true
update-desktop-database -q 2>/dev/null || true
exit 0
EOF
chmod 0755 "$OUT/$P/DEBIAN/postinst"

############ skillfish-iso-mount ############
P=skillfish-iso-mount; stage $P
cp_into $P /usr/local/bin/skillfish-iso-mount usr/local/bin/skillfish-iso-mount 0755
cp_into $P /usr/share/kio/servicemenus/skillfish-iso.desktop usr/share/kio/servicemenus/skillfish-iso.desktop
install -D -m 0644 /tmp/49-skillfish-udisks.rules "$OUT/$P/etc/polkit-1/rules.d/49-skillfish-udisks.rules"
cat > "$OUT/$P/DEBIAN/control" <<EOF
Package: skillfish-iso-mount
Version: $VER
Architecture: all
Maintainer: SkillFishOS <info@skillfishos.com>
Depends: udisks2, polkitd | policykit-1
Section: utils
Priority: optional
Homepage: https://skillfishos.com
Description: SkillFishOS native ISO mounting for KDE
 Mount and unmount disk images from the KDE/Dolphin context menu through
 udisks2 (loop devices), with a polkit rule that lets administrators mount
 without a password prompt. No GNOME dependencies.
EOF
cat > "$OUT/$P/DEBIAN/postinst" <<'EOF'
#!/bin/sh
set -e
update-desktop-database -q 2>/dev/null || true
exit 0
EOF
chmod 0755 "$OUT/$P/DEBIAN/postinst"

############ build all ############
for P in skillfish-tuner skillfish-ai-panel skillfish-iso-mount; do
  chmod -R u+rwX,go+rX "$OUT/$P"
  dpkg-deb --root-owner-group --build "$OUT/$P" "$OUT/out/${P}_${VER}_all.deb"
done
echo "=== built ==="
ls -l "$OUT/out"
echo "=== lintian-ish check ==="
for f in "$OUT"/out/*.deb; do echo "## $f"; dpkg-deb -I "$f" | sed -n '1,20p'; echo; done
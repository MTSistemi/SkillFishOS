#!/bin/bash
# Development install of the Control Center tree on a board (not the package):
#     installa-locale.sh [--lancia]
# Copies everything into place, compiles, and optionally relaunches the window
# in the desktop session of the logged-in user, capturing a screenshot after.
set -e
cd "$(dirname "$0")"
sed -i 's/\r$//' skillfish-control-center skillfish-cc-helper installa-locale.sh $(find sfcc -name "*.py")
python3 -m py_compile skillfish-control-center skillfish-cc-helper $(find sfcc -name "*.py")
mkdir -p /usr/share/skillfish/control-center
rm -rf /usr/share/skillfish/control-center/sfcc
cp -r sfcc /usr/share/skillfish/control-center/
find /usr/share/skillfish/control-center -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
install -m 0755 skillfish-control-center /usr/local/bin/skillfish-control-center
install -m 0755 skillfish-cc-helper /usr/local/bin/skillfish-cc-helper
install -m 0644 os.skillfish.control-center.policy /usr/share/polkit-1/actions/
install -m 0644 os.skillfish.control-center.desktop /usr/share/applications/
install -m 0644 profili.json /usr/share/skillfish/profili.json
install -m 0644 vf-curva-predefinita.json /usr/share/skillfish/vf-curva-predefinita.json
for n in skillfish-control-center skillfish-giochi skillfish-profili; do
  install -m 0644 icone/$n.svg /usr/share/icons/hicolor/scalable/apps/$n.svg
  for s in 48 128 256; do rsvg-convert -w $s -h $s icone/$n.svg -o /usr/share/icons/hicolor/${s}x${s}/apps/$n.png; done
done
gtk-update-icon-cache -q -f /usr/share/icons/hicolor 2>/dev/null || true
update-desktop-database -q 2>/dev/null || true
echo "installato"
if [ "${1:-}" = "--lancia" ]; then
  UTENTE=$(who | awk '/:0/{print $1; exit}'); UTENTE=${UTENTE:-skillfishdev}
  pkill -f "skillfish-control-cente[r]" 2>/dev/null || true
  sleep 1
  rm -f /tmp/cc.log
  python3 /opt/attrezzi-banco/launch-with-session-env.py "$UTENTE" /tmp/cc.log \
      /usr/local/bin/skillfish-control-center ${2:+--pagina "$2"} | tail -1
  sleep "${3:-9}"
  rm -f /tmp/shot.log /tmp/cc1.png
  python3 /opt/attrezzi-banco/launch-with-session-env.py "$UTENTE" /tmp/shot.log import -window root /tmp/cc1.png >/dev/null
  sleep 3
  echo "=== log"; tail -25 /tmp/cc.log
  echo "=== vivo?"; pgrep -fa "control-cente[r]" | grep -v pgrep | head -2
  ls -la /tmp/cc1.png 2>/dev/null
fi

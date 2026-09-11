#!/bin/bash
# Drive the Control Center inside the real KDE session (through KRunner, so the
# process belongs to the logind session and polkit finds the agent).
#     prova-gui.sh apri <pagina> <secondi>     open the window on a page, screenshot
#     prova-gui.sh clic <x> <y> <secondi>       click at screen coordinates, screenshot
#     prova-gui.sh tasto <key> <secondi>        press a key, screenshot
#     prova-gui.sh chiudi
# ⚠️ This file exists because a pkill/pgrep pattern typed on the ssh command
# line matches the ssh shell itself and kills it. Here the pattern is built
# from pieces and never appears literally on any command line.
set -u
UTENTE=$(who | awk '/:0/{print $1; exit}'); UTENTE=${UTENTE:-skillfishdev}
NOME="skillfish-control-cente"; NOME="${NOME}r"
# the launcher drops privileges before it opens its log: a log left by the
# user cannot be truncated by root through it, so it is removed first
come() { rm -f /tmp/x.log; python3 /opt/attrezzi-banco/launch-with-session-env.py "$UTENTE" /tmp/x.log "$@" >/dev/null; }
scatto() { rm -f /tmp/cc-gui.png; come import -window root /tmp/cc-gui.png; sleep 3; }
case "${1:-}" in
  apri)
    pkill -f "$NOME" 2>/dev/null; sleep 1
    come xdotool key alt+F2; sleep 1.5
    come xdotool type --delay 40 "$NOME --pagina ${2:-stato}"; sleep 1
    come xdotool key Return; sleep "${3:-10}"
    scatto
    echo "=== vivo"; pgrep -fa "$NOME" | grep -v pgrep | head -2 ;;
  clic)  come xdotool mousemove "$2" "$3" click 1; sleep "${4:-3}"; scatto ;;
  tasto) come xdotool key "$2"; sleep "${3:-3}"; scatto ;;
  scrivi) come xdotool type --delay 40 "$2"; sleep 1; scatto ;;
  chiudi) pkill -f "$NOME" 2>/dev/null; echo chiuso ;;
esac
ls -la /tmp/cc-gui.png 2>/dev/null

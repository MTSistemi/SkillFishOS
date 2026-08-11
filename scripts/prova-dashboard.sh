#!/bin/bash
# Carica DAVVERO le pagine della dashboard in un browser e cattura gli errori
# della console.
#
# `node --check` verifica solo la sintassi: una chiamata a una funzione che non
# esiste e' sintatticamente perfetta ed esplode solo a runtime. E' cosi' che ho
# scritto S("chiave") 52 volte al posto di T() e ho lasciato la dashboard con la
# pagina vuota, dicendo pure "JavaScript valido".
set -u
W=/usr/share/skillfish/dashboard
OUT=/tmp/prova-pagina
mkdir -p "$OUT"; rm -f "$OUT"/*

pkill -f "http.server 8901" 2>/dev/null
cd "$W" && (python3 -m http.server 8901 --bind 127.0.0.1 >/dev/null 2>&1 &)
sleep 2
echo "  server: HTTP $(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8901/index.html)"

for p in index.html tuner.html hub.html aichat.html; do
  log="$OUT/$p.log"
  google-chrome --headless --disable-gpu --no-sandbox \
    --enable-logging=stderr --v=0 --virtual-time-budget=6000 \
    --dump-dom "http://127.0.0.1:8901/$p" > "$OUT/$p.dom" 2> "$log"

  err=$(grep -icE "Uncaught|is not defined|is not a function|SyntaxError|TypeError" "$log" 2>/dev/null || echo 0)
  dom=$(wc -c < "$OUT/$p.dom")
  printf '  %-13s DOM %6s byte   errori JS: %s\n' "$p" "$dom" "$err"
  if [ "$err" != "0" ]; then
    grep -iE "Uncaught|is not defined|is not a function|SyntaxError|TypeError" "$log" \
      | sed 's/^.*CONSOLE/CONSOLE/' | head -4 | sed 's/^/      /'
  fi
done

echo
echo "=== il corpo della pagina viene popolato? ==="
# se app.js muore, #app o simili restano vuoti
grep -o 'id="app"[^>]*>' "$OUT/index.html.dom" 2>/dev/null | head -1 | sed 's/^/  /'
printf '  parole nel corpo di index: %s\n' "$(sed 's/<[^>]*>/ /g' "$OUT/index.html.dom" 2>/dev/null | wc -w)"

pkill -f "http.server 8901" 2>/dev/null
exit 0

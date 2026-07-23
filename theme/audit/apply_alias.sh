#!/bin/sh
# Crea alias di icone copiando un SVG ottone esistente sul nome mancante.
# Uso: apply_alias.sh <theme_root> < alias_map.txt
export LANG=C
TH="$1"
ok=0; skip=0
while read -r target source; do
  [ -z "$target" ] && continue
  src=$(find "$TH" -name "$source.svg" 2>/dev/null | head -1)
  if [ -z "$src" ]; then echo "  SKIP $target  (source $source.svg non trovato)"; skip=$((skip+1)); continue; fi
  dst="$(dirname "$src")/$target.svg"
  if [ -e "$dst" ]; then echo "  esiste gia $target"; continue; fi
  cp "$src" "$dst" && { echo "  + $target  <-  $source"; ok=$((ok+1)); }
done
echo "applicati=$ok  saltati=$skip"

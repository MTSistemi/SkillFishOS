#!/bin/sh
# Per ogni icona candidata stampa da quale tema viene risolta (ordine di inheritance reale).
export LANG=C
THEMES="SkillFishSteampunk breeze-dark breeze Adwaita hicolor"
while IFS= read -r n; do
  [ -z "$n" ] && continue
  found="NONE"
  for t in $THEMES; do
    if find "/usr/share/icons/$t" \( -name "$n.svg" -o -name "$n.png" \) 2>/dev/null | grep -q .; then
      found="$t"; break
    fi
  done
  printf '%-42s %s\n' "$n" "$found"
done < /tmp/cand.txt

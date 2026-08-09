#!/bin/bash
# install-minecraft-mods.sh — Fabric + performance mods for Minecraft: Java Edition
# on the BC-250. Installs the Fabric loader for the target Minecraft version, then the
# FPS/perf mod pack into ~/.minecraft/mods:
#   - Sodium      (GPU renderer — the big FPS win on gfx1013)
#   - Lithium     (game-logic / tick optimiser — extra useful with the 8-core unlock)
#   - FerriteCore (lower RAM use)
#   - Fabric API  (common dependency)
#
# Mods are fetched from Modrinth: the newest build compatible with the target MC
# version, preferring release > beta > alpha. On a brand-new MC release Sodium is
# typically only available as an alpha — that's expected and is what everyone runs
# on that version; it is not a stability concern in practice.
#
# Run as root ON THE BOX, with the Minecraft launcher CLOSED:
#   sudo bash install-minecraft-mods.sh [MCVERSION]
# MCVERSION defaults to the current Mojang release.
set -euo pipefail
USER_NAME="${SKILLFISH_USER:-skillfish}"
HOME_DIR="$(getent passwd "$USER_NAME" | cut -d: -f6)"
MC="$HOME_DIR/.minecraft"
MODS="$MC/mods"
asuser() { su "$USER_NAME" -c "$1"; }

# --- target MC version: 1st arg, else latest release from the Mojang manifest ---
MCVER="${1:-}"
if [ -z "$MCVER" ]; then
  MCVER=$(curl -fsSL https://launchermeta.mojang.com/mc/game/version_manifest_v2.json \
    | python3 -c "import sys,json;print(json.load(sys.stdin)['latest']['release'])")
fi
echo ">>> [1/3] target Minecraft: $MCVER"

# --- Fabric loader (stable) via the official installer ---
FIN_URL=$(curl -fsSL https://meta.fabricmc.net/v2/versions/installer \
  | python3 -c "import sys,json;print([x['url'] for x in json.load(sys.stdin) if x['stable']][0])")
LOADER=$(curl -fsSL https://meta.fabricmc.net/v2/versions/loader \
  | python3 -c "import sys,json;print([x['version'] for x in json.load(sys.stdin) if x['stable']][0])")
TMP=$(mktemp -d); curl -fsSL -o "$TMP/fabric-installer.jar" "$FIN_URL"
echo ">>> [2/3] Fabric loader $LOADER for $MCVER"
asuser "java -jar '$TMP/fabric-installer.jar' client -mcversion '$MCVER' -loader '$LOADER' -dir '$MC'"

# --- performance mods from Modrinth ---
echo ">>> [3/3] performance mods"
asuser "mkdir -p '$MODS'"
get_mod() {  # prints "<filename>\t<url>\t<type>" for the best build for $MCVER
  curl -fsSL "https://api.modrinth.com/v2/project/$1/version?loaders=%5B%22fabric%22%5D&game_versions=%5B%22$MCVER%22%5D" \
    | python3 -c "
import sys,json
d=json.load(sys.stdin)
if not d: sys.exit(1)
order={'release':0,'beta':1,'alpha':2}
d.sort(key=lambda v: order.get(v['version_type'],3))
f=d[0]['files'][0]
print(f['filename']+'\t'+f['url']+'\t'+d[0]['version_type'])
"
}
for slug in sodium lithium ferrite-core fabric-api; do
  if ! line=$(get_mod "$slug"); then echo "  ! $slug: no build for $MCVER, skipped"; continue; fi
  fn=$(echo "$line" | cut -f1); url=$(echo "$line" | cut -f2); typ=$(echo "$line" | cut -f3)
  asuser "curl -fsSL -o '$MODS/$fn' '$url'"
  echo "  + $slug: $fn [$typ]"
done

cat <<EOF

=========================================================================
 Fabric + Sodium/Lithium/FerriteCore installed for Minecraft $MCVER.

 In the launcher pick the profile "fabric-loader-$MCVER" and play.
 Press F3 in game to see the FPS — Sodium typically doubles them on the BC-250.
=========================================================================
EOF

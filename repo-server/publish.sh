#!/bin/bash
# Pubblica uno o piu' .deb nel repo SkillFishOS (codename: skillfishos).
# Installato sul host repo come /opt/skillfishos-repo/publish.sh
set -e
BASE=/srv/skillfishos-repo
CODENAME=skillfishos
if [ $# -eq 0 ]; then echo "uso: $0 file1.deb [file2.deb ...]"; exit 1; fi
for f in "$@"; do
  echo ">> includedeb $f"
  reprepro -b "$BASE" includedeb "$CODENAME" "$f"
done
echo ">> contenuto repo:"
reprepro -b "$BASE" list "$CODENAME"

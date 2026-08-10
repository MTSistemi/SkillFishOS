#!/bin/bash
# Rende lo sfondo SkillFishOS quello predefinito, davvero.
#
# IL PROBLEMA
# Il look-and-feel org.skillfish.steampunk dichiarava:
#     [Wallpaper]
#     Image=/usr/share/skillfish/skillfish-wallpaper.png
# cioe' un PNG grezzo. Plasma in quella chiave si aspetta un **pacchetto**
# wallpaper (una cartella con metadata.json e contents/images/), non un file:
# non riuscendo a risolverlo ricade sullo sfondo predefinito di Plasma.
#
# Risultato: chi installa non vede lo sfondo di SkillFishOS ne' nella live ne'
# nel sistema installato. Sulla macchina di sviluppo sembrava funzionare solo
# perche' era stato impostato a mano.
#
# In piu' l'immagine non apparteneva a NESSUN pacchetto: stava sul disco della
# scheda e finiva nella ISO solo perche' l'immagine si costruisce dal sistema
# vivo. Chi installava skillfish-theme da apt su un'altra macchina non se la
# portava dietro.
#
# LA CORREZIONE
# Creare un vero pacchetto wallpaper in /usr/share/wallpapers/SkillFishOS e
# puntarci il look-and-feel. Cosi' lo sfondo compare anche nel selettore di
# Plasma, che prima non lo mostrava.
set -u

SRC=/usr/share/skillfish/skillfish-wallpaper.png
PKG=/usr/share/wallpapers/SkillFishOS
LNF=/usr/share/plasma/look-and-feel/org.skillfish.steampunk/contents/defaults

[ -f "$SRC" ] || { echo "FATAL: manca $SRC" >&2; exit 1; }

echo "=== creo il pacchetto wallpaper ==="
mkdir -p "$PKG/contents/images" "$PKG/contents/screenshots"

# Plasma sceglie l'immagine dal nome <larghezza>x<altezza>.png
read -r W H <<EOF
$(python3 - "$SRC" <<'PY' 2>/dev/null || echo "3840 2160"
import struct, sys
d = open(sys.argv[1], 'rb').read(33)
print(struct.unpack('>II', d[16:24])[0], struct.unpack('>II', d[16:24])[1])
PY
)
EOF
echo "  risoluzione rilevata: ${W}x${H}"

cp -f "$SRC" "$PKG/contents/images/${W}x${H}.png"
cp -f "$SRC" "$PKG/contents/screenshots/${W}x${H}.png"

cat > "$PKG/metadata.json" <<'JSON'
{
    "KPlugin": {
        "Authors": [
            {
                "Name": "SkillFishOS"
            }
        ],
        "Id": "SkillFishOS",
        "License": "CC-BY-SA-4.0",
        "Name": "SkillFishOS",
        "Name[it]": "SkillFishOS",
        "Website": "https://skillfishos.com"
    },
    "X-KDE-PluginInfo-Category": "Wallpaper"
}
JSON

echo "  creato $PKG"
find "$PKG" -type f -printf '     %p (%s byte)\n'

echo
echo "=== punto il look-and-feel al pacchetto invece che al file ==="
if [ -f "$LNF" ]; then
    [ -f "$LNF.skfbak" ] || cp "$LNF" "$LNF.skfbak"
    if grep -q '^Image=' "$LNF"; then
        sed -i "s|^Image=.*|Image=$PKG|" "$LNF"
    else
        printf '\n[Wallpaper]\nImage=%s\n' "$PKG" >> "$LNF"
    fi
    echo "  ora dichiara:"
    grep -A 1 '\[Wallpaper\]' "$LNF" | sed 's/^/     /'
else
    echo "  ATTENZIONE: manca $LNF"
fi

echo
echo "=== allineo anche la configurazione di skel ==="
for f in /etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc \
         /home/*/.config/plasma-org.kde.plasma.desktop-appletsrc; do
    [ -f "$f" ] || continue
    grep -q 'skillfish-wallpaper.png' "$f" || continue
    echo "     $f (lasciato com'e': il percorso diretto funziona per chi ce l'ha gia')"
done
echo
echo "fatto. Il pacchetto va spedito da skillfish-theme, vedi build-debs-ci.sh"

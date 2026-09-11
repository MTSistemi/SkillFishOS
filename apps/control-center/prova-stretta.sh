#!/bin/bash
# Lab: install the responsive changes and photograph the window at 1000x640.
set -u
R=/root/sfx-src
CC=/usr/share/skillfish/control-center
S=/tmp/cc5
find $S -type f | xargs sed -i 's/\r$//'
for f in sfcc/stile.py sfcc/finestra.py sfcc/pagine/monitor.py sfcc/pagine/tuner.py; do
    install -m 0644 $S/$f $R/apps/control-center/$f
    install -m 0644 $S/$f $CC/$f
done
python3 -m py_compile $CC/sfcc/stile.py $CC/sfcc/finestra.py $CC/sfcc/pagine/monitor.py $CC/sfcc/pagine/tuner.py && echo "compila: ok"
cd $R/apps/control-center
U=skillfishdev
X="runuser -u $U -- env DISPLAY=:0"
for pagina in tuner monitor stato giochi; do
    bash prova-gui.sh apri $pagina 6 >/dev/null 2>&1
    W=$($X xdotool search --name "SkillFishOS Control Center" 2>/dev/null | tail -1)
    $X xdotool windowsize $W 1000 640 2>/dev/null
    sleep 2
    $X import -window root /tmp/cc-stretto-$pagina.png
    bash prova-gui.sh chiudi 1 >/dev/null 2>&1
done
ls -la /tmp/cc-stretto-*.png | awk '{print $5, $9}'
grep -i "traceback\|error" /tmp/x.log | head -3

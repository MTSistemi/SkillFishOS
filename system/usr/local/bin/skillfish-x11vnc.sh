#!/bin/bash
export DISPLAY=:0
xset s off 2>/dev/null; xset s noblank 2>/dev/null; xset -dpms 2>/dev/null
exec x11vnc -display "$DISPLAY" -nopw -forever -shared -noxdamage -repeat -bg -o /tmp/x11vnc.log

#!/bin/sh
# Continuously sample GPU utilization (radeontop GRBM, since gpu_busy_percent is
# non-functional on gfx1013) into a cache file the HUD/conky reads instantly.
# radeontop -l 1 itself takes ~1s, so the loop paces itself at ~1 Hz.
while true; do
  v=$(radeontop -d - -l 1 2>/dev/null | grep -oE 'gpu [0-9]+' | head -1 | grep -oE '[0-9]+')
  printf '%s\n' "${v:-0}" > /run/skillfish-gpu-util.tmp 2>/dev/null \
    && mv -f /run/skillfish-gpu-util.tmp /run/skillfish-gpu-util 2>/dev/null
  sleep 1
done

#!/bin/bash
# SkillFishOS freeze detector (system side, runs once at boot as root).
# If the PREVIOUS boot did not shut down cleanly (hard hang -> watchdog reset,
# or power loss), log it and leave a flag for the desktop notifier.
LOG=/var/log/skillfish-freeze.log
FLAG=/run/skillfish-freeze-detected
# a clean shutdown always logs the journald stop message as one of its last lines
if journalctl -b -1 --no-pager -n 60 -q 2>/dev/null | grep -qE "Journal stopped|Reached target.*(Power-Off|Reboot)|systemd-shutdown"; then
    exit 0  # previous boot ended cleanly
fi
# no previous boot at all (first boot ever / cleared journal): nothing to report
journalctl --list-boots 2>/dev/null | grep -q '^ *-1 ' || exit 0
ts=$(date -Is)
cpu=$(grep -m1 '^frequency' /etc/bc250-smu-oc.conf 2>/dev/null | tr -d ' ')
gpu=$(grep -A1 '\[\[safe-points\]\]' /etc/cyan-skillfish-governor/config.toml 2>/dev/null | grep -oE '[0-9]+' | sort -n | tail -1)
echo "$ts unclean-shutdown cpu=${cpu:-?} gpu_max=${gpu:-?}MHz" >> "$LOG"
count=$(wc -l < "$LOG")
printf '%s\n' "$count" > "$FLAG"
chmod 0644 "$FLAG" "$LOG"
exit 0

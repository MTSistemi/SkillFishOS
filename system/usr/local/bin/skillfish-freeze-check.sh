#!/bin/bash
# SkillFishOS unclean-shutdown detector (system side, runs as root).
#
#   skillfish-freeze-check.sh boot      once at startup   (ExecStart)
#   skillfish-freeze-check.sh shutdown  once at halt      (ExecStop)
#
# WHY THIS NO LONGER READS THE JOURNAL
# The first version decided by grepping the last 60 lines of the previous boot
# for "Journal stopped" / "Reached target ... Reboot" / "systemd-shutdown". It
# reported two perfectly clean reboots of the development machine as freezes,
# and it could not have done anything else:
#
#   1. journald is stopped BEFORE the machine actually goes down, so the very
#      messages that would prove an orderly shutdown are the ones that never
#      reach the disk. What survives as the last lines is ordinary "Stopped
#      <unit>" chatter. A bigger window does not help: the evidence is absent,
#      not further back.
#   2. those strings are English, while systemd translates its messages and our
#      installs are frequently not in English. On an Italian desktop the grep
#      can only fail - and failing means "freeze", the wrong way round.
#
# So we stop reading tea leaves and leave a mark of our own. The unit that runs
# this at boot also runs it at shutdown; the shutdown run writes a marker file.
# A boot that finds the marker knows the previous shutdown was orderly, removes
# it and says nothing. A boot that does not find it knows the machine went down
# without being asked: hard hang plus watchdog reset, power loss, or the reset
# button. No text to match, no language to get right, no journal to consult.
#
# This is also what the documentation has always described ("no clean-shutdown
# marker"); the code simply never did it.
set -u

STATO=/var/lib/skillfish
PULITO=$STATO/clean-shutdown          # written at halt, removed at boot
ARMATO=$STATO/detector-armed          # "the marker mechanism was active last boot"
LOG=/var/log/skillfish-freeze.log
FLAG=/run/skillfish-freeze-detected

# The board-specific advice lives here; on anything else it must not be shown.
E_BC250=/usr/local/bin/skillfish-is-bc250

arma() { mkdir -p "$STATO"; : > "$ARMATO"; }

# every "frequency = N" of a config file, one per line, key stripped
mhz() {
    sed -n 's/^[[:space:]]*frequency[[:space:]]*=[[:space:]]*\([0-9]\{1,\}\).*/\1/p' \
        "$1" 2>/dev/null
}

registra() {
    ts=$(date -Is)
    # The overclock profile is meaningful only on the board. skillfish-base
    # installs /etc/bc250-smu-oc.conf everywhere, so reading it unconditionally
    # printed a BC-250 overclock next to a freeze on a Xeon workstation.
    if [ -x "$E_BC250" ] && "$E_BC250" 2>/dev/null; then
        profilo=bc250
        # the old parser kept the key as well and logged "cpu=frequency=3500"
        cpu=$(mhz /etc/bc250-smu-oc.conf | head -1)
        # Every safe-point of the governor curve is a "frequency = N"; the top of
        # the curve is the highest of them. The old code took the line after each
        # [[safe-points]] header and grepped any number out of it, which only
        # works as long as frequency stays the first key of the block.
        gpu=$(mhz /etc/cyan-skillfish-governor/config.toml | sort -n | tail -1)
        dettagli=" cpu=${cpu:-?}MHz gpu_max=${gpu:-?}MHz"
    else
        profilo=generic
        dettagli=""
    fi
    printf '%s unclean-shutdown profile=%s%s\n' "$ts" "$profilo" "$dettagli" >> "$LOG"
    # First line stays the count: the Tuner, the dashboard and an older notifier
    # all read it that way. The second line is new and optional.
    printf '%s\n%s\n' "$(wc -l < "$LOG" | tr -d ' ')" "$profilo" > "$FLAG"
    chmod 0644 "$FLAG" "$LOG" 2>/dev/null || true
}

case "${1:-boot}" in                  # no argument = boot, so an old unit file
                                      # left behind by an upgrade still works
    shutdown)
        mkdir -p "$STATO"
        date -Is > "$PULITO" 2>/dev/null || : > "$PULITO"
        # The next thing to touch this disk may be a power cut: get it down now.
        sync -f "$PULITO" 2>/dev/null || sync
        ;;
    boot)
        mkdir -p "$STATO"
        if [ -e "$PULITO" ]; then
            rm -f "$PULITO"
            arma
            exit 0                    # previous shutdown was orderly
        fi
        # No marker. That only accuses somebody if the mechanism was armed: on
        # the first boot of a fresh install, or on the first boot after the
        # upgrade that introduced this, nobody could have written a marker and
        # reporting a freeze would repeat the original false positive.
        if [ ! -e "$ARMATO" ]; then
            arma
            exit 0
        fi
        registra
        arma
        ;;
    *)
        echo "uso: ${0##*/} [boot|shutdown]" >&2
        exit 2
        ;;
esac
exit 0

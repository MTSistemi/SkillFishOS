#!/bin/bash
# SkillFishOS freeze notifier (user side, runs once at KDE login).
# If the boot-time check flagged an unclean previous shutdown, tell the user
# and point them at the Tuner (their OC/UV profile may be unstable).
FLAG=/run/skillfish-freeze-detected
[ -f "$FLAG" ] || exit 0
count=$(cat "$FLAG" 2>/dev/null)
case "${LANG:-en}" in
  it*) title="SkillFishOS — ripreso da un blocco"
       body="Il sistema non si era spento correttamente (blocco n°${count:-?}).\nSe succede di nuovo, apri il Tuner e scendi di uno scalino con CPU/GPU (🎰 Trova il massimo)." ;;
  *)   title="SkillFishOS — recovered from a freeze"
       body="The system did not shut down cleanly (freeze #${count:-?}).\nIf it happens again, open the Tuner and step your CPU/GPU down one notch (🎰 Find my max)." ;;
esac
notify-send -a SkillFishOS -i skillfishos -u critical "$title" "$body" 2>/dev/null || true
exit 0

#!/bin/bash
# SkillFishOS unclean-shutdown notifier (user side, runs once at KDE login).
#
# The boot-time check leaves /run/skillfish-freeze-detected with two lines:
#   1) how many episodes are in the log   (first line: read by older builds too)
#   2) which profile the machine has      ("bc250" or "generic")
#
# WHY THE PROFILE MATTERS
# The old text always said "open the Tuner and step your CPU/GPU down one
# notch". That is the right advice on an overclocked BC-250 and nonsense
# everywhere else: on a Generic install there is no Tuner profile to lower, and
# an unclean shutdown is far more likely to be a power cut or a forced reset.
# Telling a user to undo an overclock they never applied wastes their time and
# makes the system look like it does not know its own hardware.
FLAG=/run/skillfish-freeze-detected
[ -f "$FLAG" ] || exit 0

count=$(sed -n 1p "$FLAG" 2>/dev/null)
profilo=$(sed -n 2p "$FLAG" 2>/dev/null)
# Flag written by an older skillfish-base: work the profile out ourselves.
if [ -z "$profilo" ]; then
    if /usr/local/bin/skillfish-is-bc250 2>/dev/null; then profilo=bc250; else profilo=generic; fi
fi

case "${LANG:-en}" in it*) L=it ;; pl*) L=pl ;; uk*) L=uk ;; *) L=en ;; esac

if [ "$profilo" = bc250 ]; then
    # An unstable overclock is worth interrupting for.
    urgenza=critical
    case "$L" in
      it) titolo="SkillFishOS — ripreso da un blocco"
          testo="Il sistema non si era spento correttamente (blocco n°${count:-?}).\nSe succede di nuovo, apri il Tuner e scendi di uno scalino con CPU/GPU (Trova il massimo)." ;;
      pl) titolo="SkillFishOS — po zawieszeniu"
          testo="System nie został wyłączony poprawnie (zawieszenie nr ${count:-?}).\nJeśli powtórzy się to ponownie, otwórz Tuner i obniż CPU/GPU o jeden stopień (Znajdź moje maksimum)." ;;
      uk) titolo="SkillFishOS — відновлено після зависання"
          testo="Систему не було вимкнено належним чином (зависання №${count:-?}).\nЯкщо це повториться, відкрийте Tuner і знизьте CPU/GPU на один щабель (Знайти мій максимум)." ;;
      *)  titolo="SkillFishOS — recovered from a freeze"
          testo="The system did not shut down cleanly (freeze #${count:-?}).\nIf it happens again, open the Tuner and step your CPU/GPU down one notch (Find my max)." ;;
    esac
else
    # On ordinary hardware this is information, not an alarm.
    urgenza=normal
    case "$L" in
      it) titolo="SkillFishOS — spegnimento anomalo"
          testo="La sessione precedente non si è chiusa correttamente (episodio n°${count:-?}).\nPuò essere mancata la corrente, un riavvio forzato o un blocco: se si ripete, guarda /var/log/skillfish-freeze.log." ;;
      pl) titolo="SkillFishOS — nieprawidłowe wyłączenie"
          testo="Poprzednia sesja nie zakończyła się poprawnie (zdarzenie nr ${count:-?}).\nMogła to być utrata zasilania, wymuszony restart lub zawieszenie: jeśli się powtórzy, sprawdź /var/log/skillfish-freeze.log." ;;
      uk) titolo="SkillFishOS — некоректне вимкнення"
          testo="Попередній сеанс завершився неналежним чином (подія №${count:-?}).\nЦе могло бути зникнення живлення, примусове перезавантаження або зависання: якщо повториться, перегляньте /var/log/skillfish-freeze.log." ;;
      *)  titolo="SkillFishOS — unclean shutdown"
          testo="The previous session did not end cleanly (event #${count:-?}).\nIt may have been a power cut, a forced reset or a hang: if it repeats, check /var/log/skillfish-freeze.log." ;;
    esac
fi

notify-send -a SkillFishOS -i skillfishos -u "$urgenza" "$titolo" "$testo" 2>/dev/null || true
exit 0

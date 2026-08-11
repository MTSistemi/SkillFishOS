#!/bin/bash
# Apre la ISO e controlla che le correzioni di oggi siano DENTRO l'immagine.
# Il build script verifica dimensione, kernel e assenza di file di /root; questo
# guarda il contenuto vero del filesystem che l'utente si ritrova installato.
set -u
ISO=${1:?serve il percorso della ISO}
M=/mnt/ispez-iso
S=/mnt/ispez-squash
PASS=0; FAIL=0
ok() { printf '  \033[32mOK\033[0m   %s\n' "$1"; PASS=$((PASS+1)); }
ko() { printf '  \033[31mNO\033[0m   %s\n' "$1"; FAIL=$((FAIL+1)); }

umount "$S" 2>/dev/null; umount "$M" 2>/dev/null
mkdir -p "$M" "$S"
mount -o loop,ro "$ISO" "$M" || exit 1
mount -o loop,ro "$M/live/filesystem.squashfs" "$S" || { umount "$M"; exit 1; }

echo "=== identita' ==="
grep -m1 PRETTY_NAME "$S/etc/os-release" | sed 's/^/  /'

echo
echo "=== le correzioni di oggi ==="
q=$S/usr/share/sddm/themes/skillfish-brass/Main.qml
grep -q 'root.tr(root.txtLogin)' "$q" 2>/dev/null \
  && ok "SDDM: il testo di accesso passa dalla traduzione" || ko "SDDM: ancora cablato"
for l in it pl uk; do
  grep -q "\"$l\":" "$q" 2>/dev/null && ok "SDDM: lingua $l" || ko "SDDM: manca $l"
done

grep -q 'os.skillfish.hub.desktop' "$S/etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc" 2>/dev/null \
  && ok "barra: c'e' il nostro Hub" || ko "barra: manca l'Hub"
grep -q 'discover' "$S/etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc" 2>/dev/null \
  && ko "barra: c'e' ANCORA Discover" || ok "barra: nessun Discover"

[ -x "$S/usr/local/bin/skillfish-hud" ] && ok "HUD: lanciatore presente" || ko "HUD: lanciatore assente"
grep -q 'skillfish-is-bc250' "$S/usr/local/bin/skillfish-hud" 2>/dev/null \
  && ok "HUD: protetto fuori dalla BC-250" || ko "HUD: senza guardia hardware"
grep -q '^Exec=/usr/local/bin/skillfish-hud' "$S/etc/skel/.config/autostart/skillfish-conky.desktop" 2>/dev/null \
  && ok "HUD: autostart con percorso assoluto" || ko "HUD: autostart sbagliato"

[ -e "$S/usr/share/icons/SkillFishSteampunk/icon-theme.cache" ] \
  && ko "tema: c'e' la icon-theme.cache (icone della barra vuote!)" \
  || ok "tema: nessuna icon-theme.cache"
[ -f "$S/usr/share/icons/SkillFishSteampunk/scalable/apps/skillfish-hub.svg" ] \
  && ok "icona Hub steampunk presente" || ko "icona Hub steampunk assente"

for f in install-emudeck.sh install-emulators.sh; do
  [ -x "$S/usr/local/share/skillfish/$f" ] && ok "emulatori: $f" || ko "emulatori: manca $f"
done
grep -q 'emudeck-electron' "$S/usr/local/share/skillfish/install-emudeck.sh" 2>/dev/null \
  && ok "emulatori: repository corretto" || ko "emulatori: repository sbagliato"

# LA DASHBOARD WEB DENTRO L'IMMAGINE.
# Due ISO l'hanno contenuta ROTTA: gli script di traduzione avevano scritto
# S("chiave") dove la funzione si chiama T(), quindi ReferenceError alla prima
# scheda e pagina vuota. E' sintatticamente valido, percio' node --check non lo
# vedeva e io avevo scritto "JavaScript valido".
D="$S/usr/share/skillfish/dashboard"
if [ -f "$D/app.js" ]; then
    n=$(grep -cF 'S("' "$D/app.js" 2>/dev/null || true)
    [ "${n:-0}" = "0" ] && ok "dashboard: nessuna chiamata a S() (si chiama T)" \
                        || ko "dashboard: $n chiamate a S() — la pagina restera' VUOTA"
    grep -qF 'pl:' "$D/app.js" && ok "dashboard: app.js tradotto" \
                               || ko "dashboard: app.js senza polacco"
    [ -f "$D/i18n.js" ] && ok "dashboard: i18n.js presente" \
                        || ko "dashboard: i18n.js ASSENTE (404 sulle tre pagine)"
    grep -qF 'data-i18n' "$D/tuner.html" 2>/dev/null \
        && ok "dashboard: tuner.html agganciato al dizionario" \
        || ko "dashboard: tuner.html non tradotto"
else
    ko "dashboard: app.js non trovato nell'immagine"
fi

grep -q 'Wydajność' "$S/usr/share/skillfish/tuner-presets.json" 2>/dev/null \
  && ok "preset: diacritici polacchi" || ko "preset: diacritici persi"

grep -q 'fastfetch' "$S/usr/local/bin/skillfish-info" 2>/dev/null \
  && ok "skillfish-info presente" || ko "skillfish-info assente"

# LA PRESENTAZIONE DI CALAMARES, DENTRO L'IMMAGINE.
# Mancava proprio questo controllo, ed e' costato due ISO. Verificavo la
# show.qml sulla board, ma eggs RIGENERA il branding a ogni produce prendendola
# dai propri addon: nell'immagine finiva la sua versione italiana, e
# l'installazione in polacco mostrava l'interfaccia in polacco e le diapositive
# in italiano.
BR=$(grep -m1 '^branding:' "$S/etc/calamares/settings.conf" | cut -d: -f2 | tr -d ' ')
Q="$S/etc/calamares/branding/$BR/show.qml"
if [ -f "$Q" ] && grep -q 'Qt.locale()' "$Q"; then
  ok "presentazione Calamares multilingua (branding $BR)"
  for l in it pl uk en; do
    grep -q "\"$l\":" "$Q" && ok "  presentazione: $l" || ko "  presentazione: manca $l"
  done
else
  ko "presentazione Calamares A LINGUA FISSA: eggs l'ha rigenerata dai suoi addon"
fi

echo
echo "=== servizi della BC-250: guardia hardware ==="
n=0; g=0
for f in "$S"/etc/systemd/system/skillfish-*.service "$S"/etc/systemd/system/cyan-*.service; do
  [ -f "$f" ] || continue
  grep -q '^ExecStart=' "$f" || continue
  case "$(basename "$f")" in
    skillfish-core-unlock.service|skillfish-cu.service|skillfish-gpu-freq.service|\
    skillfish-gpu-util.service|skillfish-thermal-guard.service|skillfish-dp-hotswap.service|\
    cyan-skillfish-governor.service)
      n=$((n+1))
      grep -q 'ExecCondition=/usr/local/bin/skillfish-is-bc250' "$f" && g=$((g+1)) ;;
  esac
done
[ "$n" -gt 0 ] && { [ "$g" = "$n" ] && ok "tutti i $n servizi protetti" || ko "solo $g su $n protetti"; }

echo
echo "=== versioni dei nostri pacchetti nell'immagine ==="
chroot "$S" dpkg -l 'skillfish-*' 2>/dev/null | awk '/^ii/{printf "  %-26s %s\n", $2, $3}'

# Nessun pacchetto deve restare indietro. skillfish-iso-mount e skillfish-menu
# erano fermi a 26.06 mentre tutti gli altri erano a 26.08.13: uno stava solo nel
# vecchio script di build, l'altro in nessuno. Me ne sono accorto guardando
# l'elenco a occhio, che non e' un modo di lavorare — qui la differenza la trova
# lo script, confrontando ogni versione con quella piu' diffusa.
COMUNE=$(chroot "$S" dpkg -l 'skillfish-*' 2>/dev/null | awk '/^ii/{print $3}' \
         | sort | uniq -c | sort -rn | head -1 | awk '{print $2}')
INDIETRO=$(chroot "$S" dpkg -l 'skillfish-*' 2>/dev/null \
           | awk -v v="$COMUNE" '/^ii/ && $3 != v {printf "%s(%s) ", $2, $3}')
if [ -n "$INDIETRO" ]; then
  ko "versioni disallineate rispetto a $COMUNE: $INDIETRO"
else
  ok "tutti i pacchetti allineati a $COMUNE"
fi

echo
printf '  superati %d, falliti %d\n' "$PASS" "$FAIL"
umount "$S"; umount "$M"
exit $([ "$FAIL" -eq 0 ] && echo 0 || echo 1)

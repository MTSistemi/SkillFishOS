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
# L'elenco e' esplicito e nominato uno per uno. Prima il ciclo pescava con
# skillfish-*.service e cyan-*.service, cosi' bc250-smu-oc.service non veniva
# nemmeno guardato: il controllo diceva "tutti i 7 servizi protetti" mentre
# l'ottavo partiva su ogni PC non BC-250 e moriva con un traceback python.
# Un controllo che non sa cosa gli manca non e' un controllo.
BC250_UNITS="cyan-skillfish-governor.service skillfish-core-unlock.service
skillfish-cu.service skillfish-gpu-freq.service skillfish-gpu-util.service
skillfish-thermal-guard.service skillfish-dp-hotswap.service bc250-smu-oc.service"
n=0; g=0
for u in $BC250_UNITS; do
  f="$S/etc/systemd/system/$u"
  [ -f "$f" ] || { ko "servizio $u assente dall'immagine"; continue; }
  grep -q '^ExecStart=' "$f" || continue
  n=$((n+1))
  if grep -q 'ExecCondition=/usr/local/bin/skillfish-is-bc250' "$f"; then
    g=$((g+1))
  else
    ko "  $u SENZA guardia hardware"
  fi
done
[ "$n" -gt 0 ] && { [ "$g" = "$n" ] && ok "tutti i $n servizi protetti" || ko "solo $g su $n protetti"; }

echo
echo "=== presentazione Calamares: rilegge la lingua al momento giusto? ==="
# La causa vera per cui usciva sempre in inglese: `property string lang:
# Qt.locale()...` e' un binding calcolato una volta sola, alla creazione del
# componente, cioe' prima che l'utente scelga la lingua. Le traduzioni c'erano,
# non le leggeva nessuno. Ora la lingua si rilegge dentro onActivate().
for q in "$S"/etc/calamares/branding/*/show.qml; do
  [ -f "$q" ] || continue
  b=$(basename "$(dirname "$q")")
  grep -q 'presentation.lang = ' "$q" \
    && ok "  $b: rilegge la lingua in onActivate()" \
    || ko "  $b: lingua letta una volta sola, restera' in inglese"
  grep -q 'Qt.uiLanguage' "$q" \
    && ok "  $b: usa Qt.uiLanguage (reattiva)" \
    || ko "  $b: non usa Qt.uiLanguage"
done

echo
echo "=== snapshot Btrfs sul sistema installato ==="
F="$S/usr/local/bin/skillfish-firstboot-snapshots.sh"
U="$S/etc/systemd/system/skillfish-firstboot-snapshots.service"
[ -f "$F" ] && ok "script del primo avvio presente" || ko "script del primo avvio ASSENTE"
grep -q 'btrfs subvolume show /.snapshots' "$F" 2>/dev/null \
  && ok "decide guardando il filesystem, non il marcatore" \
  || ko "si fida ancora del solo marcatore: gli snapshot non partiranno"
grep -q 'ConditionPathExists=!/var/lib/skillfish/.snapshots-setup-done' "$U" 2>/dev/null \
  && ko "la unit ha ancora la condizione sul marcatore: il servizio verra' SALTATO" \
  || ok "unit senza condizione sul marcatore"

echo
echo "=== tabella ACPI della BC-250: solo nell'edizione giusta ==="
# Nell'immagine Generic non deve esserci ne' il cpio ne' la riga in
# /etc/default/grub: la tabella si aggancia a \_PR.P000..P00F, che su un PC
# qualsiasi non esistono, e regala 32 errori ACPI a ogni avvio.
# L'edizione si riconosce dal kernel che AVVIA l'immagine, in live/ — NON da
# /boot dentro il squashfs: li' ci sono tutti e due i kernel, perche' sulla
# scheda di sviluppo sono installati entrambi. Guardando /boot il controllo
# diceva "Generic" anche sull'immagine BC-250 e la bocciava per una tabella ACPI
# che li' ci va eccome.
gen=0
ls "$M"/live/vmlinuz-*generic* >/dev/null 2>&1 && gen=1
[ "$gen" = 1 ] && echo "  (edizione riconosciuta: Generic)" || echo "  (edizione riconosciuta: BC-250)"
if [ "$gen" = 1 ]; then
  [ -e "$S/boot/SkillFishOS-acpi.cpio" ] \
    && ko "Generic: c'e' la tabella ACPI della BC-250 dentro l'immagine" \
    || ok "Generic: nessuna tabella ACPI della BC-250"
  grep -q '^GRUB_EARLY_INITRD_LINUX_CUSTOM=' "$S/etc/default/grub" 2>/dev/null \
    && ko "Generic: /etc/default/grub inietta ancora la tabella" \
    || ok "Generic: grub non inietta nulla"
else
  [ -e "$S/boot/SkillFishOS-acpi.cpio" ] \
    && ok "BC-250: tabella ACPI presente (giusto)" \
    || ko "BC-250: manca la tabella ACPI"
fi
grep -q '^  auto)' "$S/usr/local/bin/skillfish-acpi-pstates" 2>/dev/null \
  && ok "skillfish-acpi-pstates ha la modalita' auto" \
  || ko "skillfish-acpi-pstates senza modalita' auto"

echo
echo "=== file di scarto che non devono viaggiare ==="
n=$(find "$S/usr/local/bin" "$S/usr/share/skillfish" "$S/etc/calamares" "$S/etc/skillfish" \
     \( -name '*.bak' -o -name '*.bak.*' -o -name '*.bak-*' -o -name '*.skfbak' -o -name '*~' \) \
     2>/dev/null | wc -l)
if [ "$n" = 0 ]; then
  ok "nessun file di scarto nell'immagine"
else
  ko "$n file di scarto dentro l'immagine:"
  find "$S/usr/local/bin" "$S/usr/share/skillfish" "$S/etc/calamares" "$S/etc/skillfish" \
     \( -name '*.bak' -o -name '*.bak.*' -o -name '*.bak-*' -o -name '*.skfbak' -o -name '*~' \) \
     2>/dev/null | sed "s|$S||" | head -12 | sed 's/^/       /'
fi

echo
echo "=== voci di menu: una sola categoria principale ==="
for d in "$S"/usr/share/applications/os.skillfish.*.desktop; do
  [ -f "$d" ] || continue
  # il "Categories=" va tolto, altrimenti la PRIMA categoria non viene mai
  # contata: diceva 0 su tutti, compresi quelli con tre categorie principali
  cat=$(grep '^Categories=' "$d" | head -1 | sed 's/^Categories=//')
  n=$(echo "$cat" | tr ';' '\n' | grep -cE '^(AudioVideo|Audio|Video|Development|Education|Game|Graphics|Network|Office|Science|Settings|System|Utility)$')
  [ "${n:-0}" -le 1 ] && ok "  $(basename "$d"): $n categoria principale" \
                      || ko "  $(basename "$d"): $n categorie principali, comparira' piu' volte nel menu"
done

echo
echo "=== spegnimento della dashboard ==="
grep -q 'ExecStopPost=/usr/local/bin/skillfish-dashboard-stop' "$S/etc/systemd/system/skillfish-dashboard.service" 2>/dev/null \
  && ok "spegnimento in uno script (niente pkill che si suicida)" \
  || ko "ExecStopPost ancora dentro la unit: il servizio restera' in failed"

echo
echo "=== Wake-on-LAN ==="
[ -x "$S/usr/local/bin/skillfish-wol-arm" ] && ok "script wol-arm presente" || ko "script wol-arm assente"
grep -q 'grep -oP' "$S/etc/systemd/system/skillfish-wol.service" 2>/dev/null \
  && ko "la regex e' ancora dentro la unit: systemd si mangia \\K e \\S" \
  || ok "niente regex dentro la unit"

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

#!/bin/bash
# Allinea la versione di SkillFishOS in TUTTI i posti dove compare.
#
# PERCHE' ESISTE
# La versione era scritta a mano in sette file diversi e nessuno era d'accordo
# con gli altri. Sulla scheda, prima di questo script:
#
#   /etc/os-release                              26.06.2
#   /usr/lib/os-release                          26.06
#   /etc/lsb-release                             26.06
#   /etc/issue, /etc/issue.net                   26.06
#   eggs branding.js                             26.06
#   calamares/branding/eggs/branding.desc        26.06     <- QUESTO si vede
#   calamares/branding/skillfish/branding.desc   26.06.2   <- e questo no
#
# Il dettaglio che conta: /etc/calamares/settings.conf dice `branding: eggs`,
# quindi l'installer mostrava 26.06 mentre il sistema installato si dichiarava
# 26.06.2. La cartella "skillfish", curata a mano, non la guardava nessuno.
#
# Il branding di Calamares lo GENERA eggs da branding.js al momento del
# produce, quindi la patch autorevole e' quella: le branding.desc gia' presenti
# le allineiamo comunque, cosi' il sistema vivo e la ISO raccontano lo stesso.
#
# NOTA su branding.js: appartiene al pacchetto penguins-eggs. Un aggiornamento
# di eggs lo sovrascrive e riporta la data di build al posto del nome della
# release. Dopo ogni `apt upgrade` che tocchi eggs, rilanciare questo script.
#
# Uso:  sudo bash set-release-branding.sh 26.06.3
#       sudo bash set-release-branding.sh 26.06.3 --dry
set -u

VER="${1:-}"
DRY=0
[ "${2:-}" = "--dry" ] && DRY=1
if [ -z "$VER" ]; then
    echo "uso: $0 <versione> [--dry]   esempio: $0 26.06.3" >&2
    exit 2
fi
CODENAME="Aetherium"
FULL="SkillFishOS $VER $CODENAME"

echo "=== porto tutto a: $FULL ==="
echo

ed() {  # ed <file> <sed-expr...>
    local f="$1"; shift
    [ -f "$f" ] || { printf "   MANCA  %s\n" "$f"; return; }
    if [ "$DRY" = 1 ]; then
        printf "   [dry]  %s\n" "$f"
        return
    fi
    [ -f "$f.pre-$VER" ] || cp "$f" "$f.pre-$VER"
    sed -i "$@" "$f"
    printf "   scritto %s\n" "$f"
}

echo "--- 1. identita' del sistema ---"
for f in /etc/os-release /usr/lib/os-release; do
    ed "$f" \
        -e "s|^PRETTY_NAME=.*|PRETTY_NAME=\"SkillFishOS $VER ($CODENAME)\"|" \
        -e "s|^VERSION=.*|VERSION=\"$VER ($CODENAME)\"|" \
        -e "s|^VERSION_ID=.*|VERSION_ID=\"$VER\"|"
done
ed /etc/lsb-release \
    -e "s|^DISTRIB_RELEASE=.*|DISTRIB_RELEASE=$VER|" \
    -e "s|^DISTRIB_DESCRIPTION=.*|DISTRIB_DESCRIPTION=\"SkillFishOS $VER ($CODENAME)\"|"
ed /etc/issue     -e "s|^SkillFishOS .*|SkillFishOS $VER \"$CODENAME\" \\\\n \\\\l|"
ed /etc/issue.net -e "s|^SkillFishOS .*|SkillFishOS $VER \"$CODENAME\"|"

echo
echo "--- 2. eggs: e' lui che genera il branding di Calamares nella ISO ---"
B=/usr/lib/penguins-eggs/dist/classes/incubation/branding.js
if [ -f "$B" ]; then
    if ! grep -q "const version = " "$B"; then
        echo "   ATTENZIONE: branding.js non ha la forma attesa."
        echo "   Probabilmente eggs e' stato aggiornato e ha rimesso la data di"
        echo "   build al posto del nome della release: va ripatchato a mano."
    else
        # Le sostituzioni arrivano a fine riga (`.*`) apposta: senza, rilanciando
        # lo script il commento in coda si duplicava a ogni giro.
        #
        # knownIssuesUrl qui e' cablato al tracker di penguins-eggs. E' questo
        # il punto che conta: eggs RIGENERA branding.desc a ogni produce, quindi
        # correggere solo il .desc non serve a niente, torna com'era.
        ed "$B" \
            -e "s|const version = '[^']*';.*|const version = '$VER'; // SkillFishOS release (era la data di build)|" \
            -e "s|const shortVersion = '[^']*';.*|const shortVersion = '$VER';|" \
            -e "s|const versionedName = remix.fullname + '[^']*';.*|const versionedName = remix.fullname + ' $VER $CODENAME';|" \
            -e "s|const shortVersionedName = remix.fullname + '[^']*';.*|const shortVersionedName = remix.fullname + ' $VER $CODENAME';|" \
            -e "s|const knownIssuesUrl = '[^']*';.*|const knownIssuesUrl = 'https://github.com/MTSistemi/SkillFishOS/issues';|" \
            -e "s|const releaseNotesUrl = bugReportUrl;.*|const releaseNotesUrl = 'https://github.com/MTSistemi/SkillFishOS/releases';|"
    fi
else
    echo "   MANCA $B"
fi

echo
echo "--- 3. i branding di Calamares gia' generati ---"
for d in /etc/calamares/branding/*/branding.desc \
         /etc/penguins-eggs.d/distros/*/calamares/branding/*/branding.desc; do
    [ -f "$d" ] || continue
    # shortVersion e' una chiave a parte e se la si dimentica resta indietro:
    # e' successo, l'installer mostrava 26.06.3 nel titolo e 26.06 nel piede.
    #
    # knownIssuesUrl arriva dal branding di eggs e punta al tracker di
    # penguins-eggs: chi installa SkillFishOS e clicca "problemi noti" finiva
    # sulle issue di un altro progetto.
    ed "$d" \
        -e "s|^\(\s*version:\).*|\1 '$VER'|" \
        -e "s|^\(\s*shortVersion:\).*|\1 '$VER'|" \
        -e "s|^\(\s*versionedName:\).*|\1 $FULL|" \
        -e "s|^\(\s*shortVersionedName:\).*|\1 $FULL|" \
        -e "s|^\(\s*knownIssuesUrl:\).*|\1 https://github.com/MTSistemi/SkillFishOS/issues|" \
        -e "s|^\(\s*releaseNotesUrl:\).*|\1 https://github.com/MTSistemi/SkillFishOS/releases|"
done

echo
echo "=== verifica: cosa dicono adesso ==="
grep -h "^PRETTY_NAME" /etc/os-release /usr/lib/os-release 2>/dev/null | sed 's/^/   /'
grep -h "^DISTRIB_DESCRIPTION" /etc/lsb-release 2>/dev/null | sed 's/^/   /'
head -1 /etc/issue 2>/dev/null | sed 's/^/   issue: /'
grep -h "const versionedName" "$B" 2>/dev/null | sed 's/^/   eggs: /'
echo "   branding usato da Calamares: $(grep -E '^\s*branding:' /etc/calamares/settings.conf 2>/dev/null | awk '{print $2}')"
for d in /etc/calamares/branding/*/branding.desc; do
    printf "      %-46s %s\n" "$d" "$(grep -E '^\s*versionedName:' "$d" | sed 's/.*versionedName:\s*//')"
done

echo
n=$(grep -rhoE "26\.06(\.[0-9]+)?" /etc/os-release /usr/lib/os-release /etc/lsb-release \
        /etc/issue /etc/issue.net "$B" /etc/calamares/branding/*/branding.desc 2>/dev/null \
    | sort -u | grep -v "^$VER$" | tr '\n' ' ')
if [ -n "$n" ]; then
    echo "   ATTENZIONE: restano in giro altre versioni: $n"
else
    echo "   tutti i punti dicono $VER"
fi

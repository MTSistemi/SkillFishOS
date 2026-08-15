#!/bin/bash
# Collauda skillfish-prepara-live in un finto sistema, senza toccare niente.
#
# PERCHE' ESISTE
# skillfish-prepara-live gira a ogni avvio della live e decide tre cose che si
# vedono subito: chi entra e con quale sessione grafica, se il salvaschermo
# blocca lo schermo, e se sulla scrivania c'e' l'icona per installare. Un suo
# difetto non si scopre leggendo il codice: si scopre dopo tre ore di
# costruzione della ISO e una prova in macchina virtuale. Questo lo prova in
# un minuto, sulla macchina di sviluppo, senza avviare niente.
#
# Le tre situazioni che contano:
#   1. live con l'utente "user"    - il predefinito di live-build
#   2. live con l'utente "live"    - quello che usa eggs
#   3. sistema installato          - qui NON deve fare assolutamente niente
#
# ⚠️ TRAPPOLA DEL BANCO DI PROVA, non dello script
# La casa dell'utente dichiarata nel finto /etc/passwd deve essere quella VERA
# dentro il banco di prova. Alla prima stesura ci avevo scritto /home/user, che
# sulla macchina di sviluppo non esiste: lo script usciva subito su
# `[ -d "$CASA" ] || exit 0`, il collaudo diceva "non fa niente" e sembrava un
# guasto grave. Non lo era. Vale sempre la pena controllare il collaudo prima
# di credere a quello che dice.
set -u
export LC_ALL=C

QUI="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOK="$QUI/iso/config/hooks/normal/0112-live-session-setup.hook.chroot"
BANCO=/tmp/banco-prepara-live
GUASTI=0

[ -f "$HOOK" ] || { echo "non trovo $HOOK"; exit 1; }

# L'hook e' un generatore: il codice vero sta dentro un heredoc, e sh -n
# sull'involucro non lo guarda nemmeno.
rm -rf "$BANCO"; mkdir -p "$BANCO"
sed -n '/^cat > \/usr\/local\/bin\/skillfish-prepara-live/,/^SCR$/p' "$HOOK" \
    | sed '1d;$d' > "$BANCO/originale.sh"

echo "=== script generato: $(wc -l < "$BANCO/originale.sh") righe ==="
sh -n "$BANCO/originale.sh" || { echo "   SINTASSI NON VALIDA"; exit 1; }
echo "   sintassi valida"

prova() {   # $1 = nome, $2 = riga di avvio finta, $3 = utente (vuoto = nessuno)
    local nome="$1" cmdline="$2" utente="$3"
    local B="$BANCO/$nome"
    rm -rf "$B"
    mkdir -p "$B/proc" "$B/etc/sddm.conf.d" "$B/usr/share/applications" "$B/usr/share/xsessions"
    echo "$cmdline" > "$B/proc/cmdline"

    printf 'root:x:0:0:root:/root:/bin/bash\n' > "$B/etc/passwd"
    if [ -n "$utente" ]; then
        mkdir -p "$B/home/$utente"
        printf '%s:x:1000:1000:Live:%s:/bin/bash\n' "$utente" "$B/home/$utente" >> "$B/etc/passwd"
    fi

    # com'e' messo il sistema prima: live-config ha gia' scritto il suo
    # accesso automatico, con la sessione Wayland
    printf '[Autologin]\nUser=%s\nSession=plasma.desktop\n' "${utente:-nessuno}" > "$B/etc/sddm.conf"
    touch "$B/usr/share/xsessions/plasmax11.desktop"
    printf '[Desktop Entry]\nName=Install SkillFishOS\nExec=pkexec calamares\n' \
        > "$B/usr/share/applications/calamares.desktop"

    sed -e "s|/proc/cmdline|$B/proc/cmdline|g" \
        -e "s|/etc/passwd|$B/etc/passwd|g" \
        -e "s|/etc/sddm.conf|$B/etc/sddm.conf|g" \
        -e "s|/usr/share/xsessions|$B/usr/share/xsessions|g" \
        -e "s|/usr/share/applications|$B/usr/share/applications|g" \
        "$BANCO/originale.sh" > "$B/prova.sh"
    # gli utenti finti non esistono davvero: chown fallirebbe e basta
    sed -i 's|^chown |chown 2>/dev/null |' "$B/prova.sh"

    echo
    echo "--- $nome ---"
    sh "$B/prova.sh"
}

verifica() {   # $1 = descrizione, $2 = "si" se ci si aspetta la cosa, $3 = file
    local desc="$1" atteso="$2" file="$3"
    if [ -e "$file" ]; then
        if [ "$atteso" = "si" ]; then echo "   OK    $desc"
        else echo "   GUASTO: $desc non doveva succedere"; GUASTI=$((GUASTI + 1)); fi
    else
        if [ "$atteso" = "no" ]; then echo "   OK    $desc (giustamente assente)"
        else echo "   GUASTO: $desc manca"; GUASTI=$((GUASTI + 1)); fi
    fi
}

contiene() {   # $1 = descrizione, $2 = file, $3 = testo atteso
    if grep -q -- "$3" "$2" 2>/dev/null; then
        echo "   OK    $1"
    else
        echo "   GUASTO: $1 (in $2 non c'e' \"$3\")"; GUASTI=$((GUASTI + 1))
    fi
}

# --- 1. live con l'utente di live-build --------------------------------------
prova "1-live-user" "BOOT_IMAGE=/live/vmlinuz boot=live components" "user"
B="$BANCO/1-live-user"
verifica "accesso automatico scritto"  si "$B/etc/sddm.conf.d/01-live-autologin.conf"
contiene "nomina l'utente vero"           "$B/etc/sddm.conf.d/01-live-autologin.conf" "User=user"
contiene "sessione X11, non Wayland"      "$B/etc/sddm.conf.d/01-live-autologin.conf" "Session=plasmax11"
contiene "corregge anche /etc/sddm.conf"  "$B/etc/sddm.conf" "Session=plasmax11"
contiene "blocco schermo spento"          "$B/home/user/.config/kscreenlockerrc" "Autolock=false"
verifica "icona sulla scrivania"       si "$B/home/user/Desktop/calamares.desktop"
[ -x "$B/home/user/Desktop/calamares.desktop" ] \
    && echo "   OK    l'icona e' eseguibile (KDE altrimenti chiede conferma)" \
    || { echo "   GUASTO: icona non eseguibile"; GUASTI=$((GUASTI + 1)); }

# --- 2. live con l'utente di eggs --------------------------------------------
prova "2-live-live" "BOOT_IMAGE=/live/vmlinuz boot=live components" "live"
B="$BANCO/2-live-live"
contiene "si adatta al nome diverso" "$B/etc/sddm.conf.d/01-live-autologin.conf" "User=live"
verifica "icona anche qui"        si "$B/home/live/Desktop/calamares.desktop"

# --- 3. sistema installato: non deve toccare NIENTE --------------------------
prova "3-installato" "BOOT_IMAGE=/vmlinuz root=UUID=abc ro quiet" "mattia"
B="$BANCO/3-installato"
verifica "nessun accesso automatico" no "$B/etc/sddm.conf.d/01-live-autologin.conf"
verifica "blocco schermo non toccato" no "$B/home/mattia/.config/kscreenlockerrc"
verifica "nessuna icona aggiunta"    no "$B/home/mattia/Desktop/calamares.desktop"
contiene "sessione lasciata com'era"    "$B/etc/sddm.conf" "Session=plasma.desktop"

rm -rf "$BANCO"
echo
if [ "$GUASTI" -eq 0 ]; then
    echo "=== tutto a posto ==="
    exit 0
fi
echo "=== $GUASTI controlli falliti ==="
exit 1

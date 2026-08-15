#!/bin/bash
# Costruisce l'immagine live-build con KDE. Da lanciare sulla BC-250.
#
#   scripts/costruisci-iso.sh              costruzione da capo
#   scripts/costruisci-iso.sh riprendi     riprende dopo un'interruzione
#
# La scheda e' anche la console di casa: si costruisce con priorita' bassa su
# CPU e disco, cosi' se qualcuno si mette a giocare non se ne accorge. Ci mette
# di piu', ma nessuno ha fretta.
#
# Non si chiama "lb build" diretto: build.sh applica prima una toppa a
# live-build (che con --linux-packages none non copierebbe mai il kernel
# nell'immagine) e poi chiama lb. Saltarlo produrrebbe una ISO senza kernel.
#
# ⚠️ COSA E' SUCCESSO IL 15/08/2026, ED E' IL MOTIVO DELLA MODALITA' "riprendi"
# La costruzione e' morta a fine fase chroot con
#     umount: .../chroot/proc: target is busy
# senza che un solo processo stesse usando quel punto di mount (verificato con
# fuser e leggendo /proc/*/root): e' un montaggio propagato a un altro spazio
# dei nomi, e si stacca solo con `umount -l`. Ripartire da zero avrebbe voluto
# dire rifare ore di chroot per un difetto di dieci secondi.
#
# E c'era un secondo colpo dietro: la coda di `lb chroot` scrive `chroot.files`
# (chroot:64, `Chroot chroot "ls -lR" > chroot.files`). Morendo prima, non lo
# aveva scritto, e la fase finale si fermava subito dopo con
#     cp: cannot stat 'chroot.files': No such file or directory
# Un errore che non nomina la causa vera ed e' facile scambiare per altro.
set -u
export LC_ALL=C

MODO="${1:-daccapo}"
QUI="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ALBERO="$QUI/iso"
LOG=/root/build-live-kde.log

cd "$ALBERO" || { echo "ALBERO ASSENTE: $ALBERO"; exit 1; }

# --- residui di una costruzione interrotta ----------------------------------
# Vanno tolti sempre, anche prima di una costruzione da capo: `rm -rf chroot`
# su una cartella con dentro un mount fallisce a meta' e lascia un albero
# monco, che poi da' errori incomprensibili tre fasi piu' avanti.
pulisci_montaggi() {
    local trovati=0
    while read -r M; do
        [ -n "$M" ] || continue
        umount -l "$M" 2>/dev/null && echo "   staccato $M"
        trovati=$((trovati + 1))
    done < <(awk -v p="$ALBERO/chroot" '$5 ~ "^" p {print $5}' /proc/self/mountinfo | tac)
    [ "$trovati" -eq 0 ] && echo "   nessun montaggio residuo"
    return 0
}

echo "=== montaggi rimasti da prima ==="
pulisci_montaggi

if [ "$MODO" = "riprendi" ]; then
    echo
    echo "=== ripresa: si rifa' solo quello che manca ==="
    # chroot.files: se il chroot e' completo ma il file non c'e', lo si
    # rigenera con lo stesso comando di live-build invece di rifare tutto.
    if [ -d chroot/usr ] && [ ! -f chroot.files ]; then
        echo "   chroot.files mancante, lo rigenero (come fa lb chroot)"
        chroot chroot ls -lR > chroot.files 2>/dev/null
        echo "   $(wc -l < chroot.files) righe"
    fi
    echo "   fasi gia' concluse: $(ls .build 2>/dev/null | wc -l)"
    date '+   inizio: %H:%M:%S'
    nice -n 19 ionice -c3 lb binary noauto > /root/build-binary.log 2>&1
    ESITO=$?
    date '+   fine:   %H:%M:%S'
    echo "   codice di uscita: $ESITO"
    ls -lh "$ALBERO"/*.iso 2>/dev/null | sed 's/^/   /' || echo "   nessuna ISO"
    exit $ESITO
fi

echo
echo "=== stato di partenza ==="
echo "   live-build: $(dpkg-query -W -f='${Version}' live-build 2>/dev/null)"
echo "   spazio: $(df -h --output=avail / | tail -1 | tr -d ' ')"
echo "   carico: $(uptime | sed 's/.*load average: //')"

echo
echo "=== l'albero e' quello giusto? ==="
if [ -f config/package-lists/10-desktop-kde.list.chroot ]; then
    echo "   lista KDE presente ($(grep -vc '^#\|^$' config/package-lists/10-desktop-kde.list.chroot) pacchetti)"
else
    echo "   ERRORE: manca la lista KDE, l'albero e' ancora quello vecchio"; exit 1
fi
[ -f config/package-lists/10-desktop-hyprland.list.chroot ] && { echo "   ERRORE: c'e' ancora la lista Hyprland"; exit 1; }
grep -q 'kernel-7.1.7' config/hooks/normal/0005-install-tkg-kernel.hook.chroot \
    && echo "   kernel: 7.1.7" || { echo "   ERRORE: tag del kernel non aggiornato"; exit 1; }
[ -x config/includes.chroot/usr/local/bin/skillfish-fix-boot-extents ] \
    && echo "   script di correzione: eseguibili" \
    || { echo "   ERRORE: skillfish-fix-boot-extents non e' eseguibile"; exit 1; }

echo
echo "=== le correzioni ci sono tutte? ==="
# Ognuna e' costata una prova di installazione per essere trovata. Costruire
# un'immagine che ne sia priva vorrebbe dire rifare tutto: meglio fermarsi
# adesso che accorgersene fra tre ore.
controlla() {   # $1 = descrizione, $2 = file, $3 = testo che deve esserci
    if grep -q -- "$3" "$2" 2>/dev/null; then
        echo "   $1"
    else
        echo "   ERRORE: manca $1"
        echo "          atteso \"$3\" dentro $2"
        exit 1
    fi
}
controlla "Flatpak non si scarica dentro la RAM della live" \
    config/hooks/normal/0070-flatpak-setup.hook.chroot 'ConditionKernelCommandLine=!boot=live'
controlla "vmlinuz riscritto senza buchi (issue #12)" \
    config/includes.chroot/usr/local/bin/skillfish-fix-boot-extents 'sparse=never'
controlla "Kbuild per il modulo nct6687 (issue #30)" \
    config/hooks/normal/0050-nct6687.hook.chroot 'Kbuild'
controlla "un modulo rotto non ferma l'installazione" \
    'config/includes.chroot/etc/calamares/modules/shellprocess@boot_reconfigure.conf' 'update-initramfs'
controlla "sessione live: accesso, blocco schermo, icona" \
    config/hooks/normal/0112-live-session-setup.hook.chroot 'skillfish-prepara-live'
controlla "servizio snapshot abilitato" \
    config/hooks/normal/0090-snapper-grub-btrfs.hook.chroot 'systemctl enable skillfish-firstboot-snapshots'
controlla "zstd, o l'initrd esce compresso con gzip" \
    config/package-lists/00-base.list.chroot 'zstd'
[ -f config/bootloaders/splash.svg ] \
    && echo "   menu di avvio col nostro marchio" \
    || { echo "   ERRORE: manca config/bootloaders/splash.svg"; exit 1; }
[ -f config/hooks/normal/0112-live-autologin-session.hook.chroot ] \
    && { echo "   ERRORE: c'e' ancora il vecchio hook 0112-live-autologin-session"; exit 1; }

echo
echo "=== la ISO precedente si mette da parte, non si butta ==="
# E' l'unica immagine di cui sappiamo che si installa e si avvia: finche' la
# nuova non e' provata, quella vecchia resta la rete di sicurezza.
for I in "$ALBERO"/*.iso; do
    [ -e "$I" ] || continue
    mv -f "$I" "$I.precedente"
    echo "   messa da parte: $(basename "$I").precedente"
done

echo
echo "=== pulizia ==="
lb clean --purge >/dev/null 2>&1 || true
pulisci_montaggi
rm -rf .build cache/stages chroot binary 2>/dev/null || true
echo "   fatto"

echo
echo "=== avvio (priorita' bassa, registro in $LOG) ==="
date '+   inizio: %H:%M:%S'
nice -n 19 ionice -c3 ./build.sh > "$LOG" 2>&1
ESITO=$?
date '+   fine:   %H:%M:%S'
echo "   codice di uscita: $ESITO"

if [ $ESITO -ne 0 ]; then
    echo
    echo "   La costruzione si e' interrotta. Se il chroot e' completo"
    echo "   (iso/chroot/usr esiste), quasi sempre basta:"
    echo "       scripts/costruisci-iso.sh riprendi"
    echo "   invece di rifare tutto da capo."
fi

echo
echo "=== cosa e' uscito ==="
ls -lh "$ALBERO"/*.iso 2>/dev/null | sed 's/^/   /' || echo "   nessuna ISO prodotta"
echo
echo "=== ultime righe del registro ==="
tail -25 "$LOG" | sed 's/^/   /'
exit $ESITO

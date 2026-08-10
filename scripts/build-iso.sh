#!/bin/bash
# Costruisce una ISO di SkillFishOS e la verifica.
#
# Stava solo su /root della scheda di sviluppo, quindi non era ripetibile da
# nessun altro e non aveva storia. Ora sta nel repo.
#
# LA COMPRESSIONE LA DECIDE IL FLAG, NON eggs.yaml
# Questo e' il dettaglio che costa un'ora di build se lo si sbaglia. Avevo
# impostato `compression: xz -Xbcj x86 -b 1M` in /etc/penguins-eggs.d/eggs.yaml
# e il comando realmente eseguito era `-comp zstd -b 1M -Xcompression-level 3`.
# eggs sceglie in base a un flag di `produce`:
#
#   (nessuno)       zstd -Xcompression-level 3      veloce, immagine grossa
#   -S --standard   xz -b 1M
#   -p --pendrive   zstd -b 1M -Xcompression-level 15
#   -m --max        xz -Xbcj x86 -b 1M
#
# Misurato su 641 MB di binari, -m vale il 13% in meno di -comp xz liscio: il
# filtro BCJ x86 riscrive gli indirizzi dei salti prima di comprimere e il
# blocco da 1 MB allarga la finestra di ricerca delle ripetizioni. Si paga in
# tempo di costruzione, il che per una ISO che si scarica migliaia di volte e'
# un ottimo cambio.
#
# Gli altri flag: -n nessuna interazione, -N nessuna icona di eggs sul desktop,
# -K il kernel da mettere nell'immagine. NON usare -i: includerebbe /root, cioe'
# il nostro banco di lavoro, dentro l'immagine pubblica.
#
# Uso:  sudo bash build-iso.sh 7.1.7-skillfishos-generic SkillFishOS-26.06.3-Aetherium-Generic-amd64.iso
set -u

KVER="${1:-}"
FINAL="${2:-}"
if [ -z "$KVER" ] || [ -z "$FINAL" ]; then
    echo "uso: $0 <versione-kernel> <nome-finale.iso>" >&2
    exit 2
fi

BASE="${FINAL%-amd64.iso}"
OUT=/home/iso-out
LOG="$OUT/build-$BASE.log"
ST="$OUT/$BASE.status"
mkdir -p "$OUT"

{
echo "==== BUILD $BASE (kernel $KVER) inizio: $(date) ===="
echo "RUNNING" > "$ST"

if [ ! -f "/boot/vmlinuz-$KVER" ]; then
    echo "FATAL: /boot/vmlinuz-$KVER non esiste"
    echo "FAIL-NOKERNEL" > "$ST"; exit 1
fi

# --- profilo di overclock di sicurezza, per la durata della build ----------
# L'immagine si costruisce dal sistema vivo, quindi /etc/bc250-smu-oc.conf ci
# finisce COM'E'. Sulla scheda di sviluppo c'e' il profilo di Mattia, che e'
# tarato su QUESTO esemplare: spedirlo vorrebbe dire applicare il suo overclock
# alla scheda di chiunque installi, e la lotteria del silicio non la si vince
# per procura. La ISO 26.06.3 costruita senza questo accorgimento imbarcava
# frequency = 3600.
#
# Il trap fa il ripristino anche se la build fallisce a meta' o viene
# interrotta: senza, la scheda resterebbe a 3500 e ce ne accorgeremmo tardi.
OCF=/etc/bc250-smu-oc.conf
OCBAK=/root/oc.conf.user
restore_oc() {
    if [ -f "$OCBAK" ]; then
        mv -f "$OCBAK" "$OCF"
        echo "profilo overclock dell'utente ripristinato: $(grep -h frequency "$OCF" 2>/dev/null | tr -d ' ')"
    fi
}
if [ -f "$OCF" ]; then
    cp -f "$OCF" "$OCBAK"
    trap restore_oc EXIT INT TERM
    printf '[overclock]\nfrequency = 3500\nscale = 0\nmax_temperature = 85\n' > "$OCF"
    echo "profilo overclock: messo quello di sicurezza (3500) per la durata della build"
fi

rm -f /home/eggs/mnt/*.iso 2>/dev/null
eggs produce -n -N -m -K "$KVER" --basename="$BASE"
RC=$?
echo "produce rc=$RC"
[ $RC -ne 0 ] && { echo "FAIL rc=$RC" > "$ST"; echo "==== FALLITA ===="; exit 1; }

ISO=$(ls -t /home/eggs/mnt/*.iso 2>/dev/null | head -1)
[ -f "$ISO" ] || { echo "FAIL-NOISO" > "$ST"; exit 1; }
mv -f "$ISO" "$OUT/$FINAL"
( cd "$OUT" && sha256sum "$FINAL" > "$FINAL.sha256" )
SZ=$(du -h "$OUT/$FINAL" | cut -f1)

# --- verifica di quello che e' finito dentro -------------------------------
# Non fidarsi: la ISO si costruisce dal sistema vivo e basta una esclusione
# scritta male per perdere pezzi. Qui controlliamo le cose che sono gia'
# andate storte almeno una volta.
M=/mnt/verif-$BASE; mkdir -p "$M"; mount -o loop,ro "$OUT/$FINAL" "$M" 2>/dev/null
VK=$(ls "$M"/live/vmlinuz* 2>/dev/null; ls "$M"/boot/vmlinuz* 2>/dev/null)
SQ=$(find "$M" -name '*.squashfs' | head -1)
L=$(unsquashfs -l "$SQ" 2>/dev/null)
APPS=$(echo "$L" | grep -cE 'usr/local/bin/skillfish-(tuner|hub|monitor)$')
MENU=$(echo "$L" | grep -cE 'desktop-directories/skillfishos.directory|applications-merged/skillfishos.menu')
WALL=$(echo "$L" | grep -c 'usr/share/wallpapers/SkillFishOS/metadata.json')
ROOTH=$(echo "$L" | grep -cE '^squashfs-root/root/.')
DUMPS=$(echo "$L" | grep -c 'var/lib/systemd/coredump/core')
COMP=$(unsquashfs -s "$SQ" 2>/dev/null | grep -i '^Compression' | awk '{print $2}')
unsquashfs -n -d /tmp/ocheck-$$ -f "$SQ" etc/bc250-smu-oc.conf >/dev/null 2>&1
OCFREQ=$(grep -h 'frequency' /tmp/ocheck-$$/etc/bc250-smu-oc.conf 2>/dev/null | tr -d ' ')
rm -rf /tmp/ocheck-$$
umount "$M" 2>/dev/null; rmdir "$M" 2>/dev/null

echo "size=$SZ  compressione=$COMP  kernel=[$VK]"
echo "app=$APPS  menu=$MENU  wallpaper=$WALL  file-in-root=$ROOTH  coredump=$DUMPS"
echo "overclock spedito: $OCFREQ"
case "$OCFREQ" in
    *3500*) ;;
    *) echo "ATTENZIONE: l'immagine NON ha il profilo di sicurezza 3500 ma [$OCFREQ]" ;;
esac
[ "$WALL" -lt 1 ]  && echo "ATTENZIONE: manca il pacchetto wallpaper"
[ "$ROOTH" -gt 0 ] && echo "ATTENZIONE: dentro /root ci sono $ROOTH file, non dovrebbe essercene nessuno"
[ "$DUMPS" -gt 0 ] && echo "ATTENZIONE: ci sono $DUMPS core dump nell'immagine"

echo "DONE size=$SZ comp=$COMP apps=$APPS menu=$MENU wall=$WALL" > "$ST"
echo "==== BUILD $BASE finita: $(date) ===="
} >> "$LOG" 2>&1

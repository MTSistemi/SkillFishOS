#!/bin/bash
# SkillFishOS first-boot: set up snapper + grub-btrfs on the INSTALLED system.
#
# Calamares installs the root as the btrfs subvolume /@ (+ /@home /@cache /@log)
# but does NOT create a .snapshots subvolume, so snapper has nowhere to store
# snapshots and grub-btrfs lists nothing -> after `apt upgrade` there are no
# restore points in GRUB. This service fixes that once, on the first boot of a
# real install (it is a no-op on the live ISO, whose root is an overlay).
set -uo pipefail
MARK=/var/lib/skillfish/.snapshots-setup-done
mkdir -p /var/lib/skillfish

log(){ echo "[skillfish-firstboot-snapshots] $*"; }

ROOTFS=$(findmnt -no FSTYPE / 2>/dev/null || echo none)
if [ "$ROOTFS" != "btrfs" ]; then
  # live overlay or non-btrfs install: nothing to do
  touch "$MARK"; exit 0
fi

# Il marcatore da solo NON basta come prova che il lavoro sia stato fatto.
# La ISO e' un'istantanea della macchina di build, dove gli snapshot erano gia'
# configurati: il marcatore finiva dentro il squashfs (trovato con data
# 7 giugno su un'installazione dell'11 agosto) e questo servizio veniva saltato
# su OGNI macchina installata. Risultato: /.snapshots restava una cartella
# normale, snapper-boot moriva con ".snapshots is not a btrfs subvolume" e non
# esisteva un solo punto di ripristino - cioe' proprio la rete di sicurezza che
# promettiamo a chi sta su sid.
# Da qui in avanti la verita' e' il filesystem, non il marcatore.
# Quanti snapshot tenere. Cinque in tutto, e non per avarizia: su sid gli
# aggiornamenti sono grossi e frequenti, e ogni snapshot trattiene i blocchi
# vecchi. Con i valori di prima (10 numerati + 6 importanti + 5 orari + 7
# giornalieri) il disco si riempiva in fretta, e oltre cinque punti di ritorno
# non serve a niente: se un guasto non lo scopri entro cinque aggiornamenti, il
# problema non e' l'aggiornamento.
#   3 ordinari       le coppie pre/post di apt
#   2 importanti     quelle che toccano kernel o systemd, le piu' preziose
#   + il punto zero  "SkillFishOS - clean install", che non scade mai
# La linea temporale e' spenta: su una console di casa fare uno snapshot ogni
# ora significa solo consumare disco senza che nessuno li guardi mai.
LIMITI="TIMELINE_CREATE=no TIMELINE_CLEANUP=yes NUMBER_CLEANUP=yes
        NUMBER_LIMIT=3 NUMBER_LIMIT_IMPORTANT=2
        EMPTY_PRE_POST_CLEANUP=yes
        TIMELINE_LIMIT_HOURLY=0 TIMELINE_LIMIT_DAILY=0 TIMELINE_LIMIT_WEEKLY=0
        TIMELINE_LIMIT_MONTHLY=0 TIMELINE_LIMIT_YEARLY=0"

# I limiti si riapplicano SEMPRE, anche quando il resto e' gia' a posto: se li
# scrivessimo solo alla prima configurazione, cambiarli in un aggiornamento non
# avrebbe effetto su chi ha gia' installato.
# Si passa dal demone quando c'e', e solo in mancanza si scrive il file a mano.
# Con --no-dbus il file viene scritto bene, ma snapperd, se sta girando, continua
# a usare i valori che ha in memoria: `get-config` racconta i vecchi limiti e
# soprattutto la pulizia automatica continua a lavorare con quelli fino al
# riavvio. Misurato: file NUMBER_LIMIT="3", demone convinto che fosse 10.
applica_limiti() {
  # shellcheck disable=SC2086
  snapper -c root set-config $LIMITI >/dev/null 2>&1 && return 0
  # shellcheck disable=SC2086
  snapper --no-dbus -c root set-config $LIMITI >/dev/null 2>&1 || return 1
  # scritto senza demone: se sta girando, va rimesso in pari
  systemctl try-restart snapperd.service >/dev/null 2>&1 || true
}

if snapper --no-dbus -c root get-config >/dev/null 2>&1; then
  applica_limiti || true
  snapper -c root cleanup number   >/dev/null 2>&1 || true
  snapper -c root cleanup timeline >/dev/null 2>&1 || true
fi

if [ -e "$MARK" ] && btrfs subvolume show /.snapshots >/dev/null 2>&1; then
  exit 0
fi
rm -f "$MARK"

# 1. ensure /.snapshots is a real btrfs subvolume with a valid snapper config
if ! btrfs subvolume show /.snapshots >/dev/null 2>&1; then
  log "creating snapper 'root' config + .snapshots subvolume"
  [ -d /.snapshots ] && rmdir /.snapshots 2>/dev/null || true
  snapper --no-dbus -c root delete-config >/dev/null 2>&1 || true
  if ! snapper --no-dbus -c root create-config / >/dev/null 2>&1; then
    log "create-config failed, creating subvolume manually"
    btrfs subvolume create /.snapshots >/dev/null 2>&1 || true
    chmod 750 /.snapshots 2>/dev/null || true
  fi
fi

# 2. i limiti, sulla configurazione appena creata
# shellcheck disable=SC2086
snapper --no-dbus -c root set-config $LIMITI >/dev/null 2>&1 || true

# 3. enable the snapshot services on the installed system
# Niente snapper-timeline.timer: la linea temporale e' spenta apposta.
systemctl enable --now snapperd.service snapper-cleanup.timer \
  grub-btrfsd.service >/dev/null 2>&1 || true
systemctl disable --now snapper-timeline.timer >/dev/null 2>&1 || true

# 4. first restore point + regenerate GRUB so grub-btrfs shows it
snapper --no-dbus -c root create -d "SkillFishOS - clean install" >/dev/null 2>&1 || true
if command -v update-grub >/dev/null 2>&1; then
  update-grub >/dev/null 2>&1 || true
else
  grub-mkconfig -o /boot/grub/grub.cfg >/dev/null 2>&1 || true
fi

# Il marcatore si scrive solo se il lavoro e' RIUSCITO davvero: se lo scrivessimo
# comunque, un errore qui si trasformerebbe in "gia' fatto" per sempre.
if btrfs subvolume show /.snapshots >/dev/null 2>&1; then
  log "done"
  touch "$MARK"
else
  log "ATTENZIONE: /.snapshots non e' un sottovolume btrfs, riprovo al prossimo avvio"
fi

# Niente `systemctl disable`: il servizio si disabilitava da solo dopo la prima
# riuscita, quindi nell'immagine finiva gia' disabilitato. Adesso resta attivo e
# alla partenza costa una `findmnt` piu' una `btrfs subvolume show`.
exit 0

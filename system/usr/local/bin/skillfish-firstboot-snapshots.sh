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
[ -e "$MARK" ] && exit 0

log(){ echo "[skillfish-firstboot-snapshots] $*"; }

ROOTFS=$(findmnt -no FSTYPE / 2>/dev/null || echo none)
if [ "$ROOTFS" != "btrfs" ]; then
  # live overlay or non-btrfs install: nothing to do
  touch "$MARK"; exit 0
fi

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

# 2. retention tuning (timeline + number cleanup)
snapper --no-dbus -c root set-config \
  TIMELINE_CREATE=yes TIMELINE_CLEANUP=yes NUMBER_CLEANUP=yes \
  NUMBER_LIMIT=10 NUMBER_LIMIT_IMPORTANT=6 \
  TIMELINE_LIMIT_HOURLY=5 TIMELINE_LIMIT_DAILY=7 TIMELINE_LIMIT_WEEKLY=0 \
  TIMELINE_LIMIT_MONTHLY=0 TIMELINE_LIMIT_YEARLY=0 >/dev/null 2>&1 || true

# 3. enable the snapshot services on the installed system
systemctl enable --now snapperd.service snapper-timeline.timer \
  snapper-cleanup.timer grub-btrfsd.service >/dev/null 2>&1 || true

# 4. first restore point + regenerate GRUB so grub-btrfs shows it
snapper --no-dbus -c root create -d "SkillFishOS - clean install" >/dev/null 2>&1 || true
if command -v update-grub >/dev/null 2>&1; then
  update-grub >/dev/null 2>&1 || true
else
  grub-mkconfig -o /boot/grub/grub.cfg >/dev/null 2>&1 || true
fi

log "done"
touch "$MARK"
systemctl disable skillfish-firstboot-snapshots.service >/dev/null 2>&1 || true
exit 0

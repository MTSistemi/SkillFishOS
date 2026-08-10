#!/usr/bin/env python3
# Rende affidabile l'avvio dopo l'installazione da Calamares.
#
# IL PROBLEMA (issue #12 btrfs e #20 ext4, stessa causa)
# ------------------------------------------------------
# Il firmware della BC-250 avvia molto spesso dal percorso EFI *removibile*
# \EFI\BOOT\BOOTX64.EFI invece che dalla voce NVRAM della distribuzione.
# Con `installEFIFallback: true` Calamares ci copia shim + grubx64, ma NON
# lo stub `grub.cfg` che sta accanto al binario nella directory della
# distribuzione. Il GRUB avviato da li' ha quindi un prefix che non risolve
# nessuna configurazione e cade in `grub rescue>`.
#
# Digitando `exit` il controllo torna al firmware, che prova la voce
# successiva (quella buona) e il sistema parte: e' esattamente il sintomo
# descritto nella #20. La causa non c'entra col filesystem, ed e' il motivo
# per cui colpisce sia btrfs sia ext4.
#
# LA CORREZIONE
# -------------
# Dopo il modulo `bootloader`, nel chroot del sistema appena installato,
# rieseguiamo grub-install due volte: una per la voce NVRAM normale e una
# con `--removable`, che scrive un BOOTX64.EFI **autonomo** (prefix corretto
# e stub di configurazione al posto giusto). Poi un update-grub finale.
#
# Su btrfs grub-install viene eseguito con il layout di mount reale, quindi
# grub-probe calcola da solo il prefix comprensivo di sottovolume (/@/boot/grub).
#
# Nota su Secure Boot: `--removable` scrive grub direttamente, non shim. Sulla
# BC-250 il Secure Boot non e' attivo. Se un giorno lo fosse, la voce NVRAM
# firmata resta comunque installata dal primo grub-install: il fallback non
# sostituisce nulla, si aggiunge.
#
# Da eseguire DOPO che eggs ha generato /etc/calamares e PRIMA di produrre la ISO.
import os
import shutil

MODDIR = "/etc/calamares/modules"

# --- 1. il passo post-bootloader ------------------------------------------
RECONF = os.path.join(MODDIR, "shellprocess@boot_reconfigure.conf")
RECONF_BODY = """---
message: Final reconfiguration of the kernel and bootloader...
dontChroot: false
timeout: 600
script:
    - chmod 644 /boot/vmlinuz-`uname -r`
    - chown 0:0 /boot/vmlinuz-`uname -r`
    - INITRD=No dpkg-reconfigure -fnoninteractive linux-image-`uname -r`
    - >-
      grub-install --target=x86_64-efi --efi-directory=/boot/efi
      --bootloader-id=skillfishos --recheck || true
    - >-
      grub-install --target=x86_64-efi --efi-directory=/boot/efi
      --removable --recheck || true
    - update-grub || true
"""

# --- 2. layout dei sottovolumi sicuro per GRUB ----------------------------
# Nessun @boot: /boot resta dentro @, cosi' GRUB non deve attraversare un
# secondo sottovolume per trovare la propria configurazione (era l'errore
# "@boot subvolume not found" della #12).
WANT_SUBVOLS = """btrfsSubvolumes:
    - mountPoint: /
      subvolume: /@
    - mountPoint: /home
      subvolume: /@home
    - mountPoint: /var/cache
      subvolume: /@cache
    - mountPoint: /var/log
      subvolume: /@log
"""


def backup(path):
    if os.path.exists(path) and not os.path.exists(path + ".skfbak"):
        shutil.copy(path, path + ".skfbak")


def main():
    if not os.path.isdir(MODDIR):
        raise SystemExit("FATAL: %s non esiste — eggs ha gia' generato la config?" % MODDIR)

    backup(RECONF)
    with open(RECONF, "w", encoding="utf-8") as f:
        f.write(RECONF_BODY)
    print("OK  : scritto", RECONF)

    mount = os.path.join(MODDIR, "mount.conf")
    if os.path.exists(mount):
        with open(mount, encoding="utf-8") as f:
            s = f.read()
        if "/@boot" in s:
            print("ATTENZIONE: mount.conf contiene un sottovolume @boot — GRUB non lo trovera'")
        if "subvolume: /@\n" in s or "subvolume: /@ " in s:
            print("OK  : mount.conf ha gia' il layout con /@")
        else:
            print("ATTENZIONE: mount.conf non ha il layout atteso, controllalo a mano:")
            print(WANT_SUBVOLS)
    else:
        print("ATTENZIONE: manca", mount)

    boot = os.path.join(MODDIR, "bootloader.conf")
    if os.path.exists(boot):
        with open(boot, encoding="utf-8") as f:
            s = f.read()
        print("info: installEFIFallback =",
              "true" if "installEFIFallback: true" in s else "NON impostato a true")

    seq = "/etc/calamares/settings.conf"
    if os.path.exists(seq):
        with open(seq, encoding="utf-8") as f:
            s = f.read()
        i_boot = s.find("- bootloader\n")
        i_reco = s.find("- shellprocess@boot_reconfigure")
        if i_boot == -1 or i_reco == -1:
            print("ATTENZIONE: non trovo i due moduli nella sequenza di settings.conf")
        elif i_reco < i_boot:
            print("ATTENZIONE: boot_reconfigure viene PRIMA di bootloader: il fix non avrebbe effetto")
        else:
            print("OK  : boot_reconfigure viene dopo bootloader nella sequenza")


if __name__ == "__main__":
    main()

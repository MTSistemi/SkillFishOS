#!/bin/bash
set -e
cd "$(dirname "$0")"

# ⚠️ QUALE EDIZIONE. Ne pubblichiamo due e finora questo file ne costruiva una
# sola, con dentro anche i pacchetti dell'altra. L'edizione decide tre cose
# INSIEME, e sbagliarne una sola da' un'immagine che sembra giusta e non parte:
#
#   EDIZIONE=generic  kernel 7.2.5-skillfishos-x64  lista BC-250 esclusa
#   EDIZIONE=bc250    kernel 7.2.5-skillfishos      lista BC-250 inclusa
#
EDIZIONE="${EDIZIONE:-generic}"
case "$EDIZIONE" in
    bc250)   SAPORE="7.2.5-skillfishos";     VARIANTE="bc250"; DESCR="BC-250 (znver2)" ;;
    generic) SAPORE="7.2.5-skillfishos-x64"; VARIANTE="x64";   DESCR="generic x86-64" ;;
    *) echo "EDIZIONE sconosciuta: $EDIZIONE (bc250 o generic)" >&2; exit 2 ;;
esac
export SKILLFISH_LINUX_FLAVOUR="$SAPORE"
# ⚠️ L'ambiente NON attraversa il chroot: live-build esegue gli hook dentro, e
# li' SKILLFISH_KERNEL_VARIANT non arriva. La prima immagine "BC-250" e' uscita
# col kernel x64 proprio cosi'. L'edizione si scrive in un file che entra
# nell'immagine, e l'hook 0005 legge quello.
install -d config/includes.chroot/etc
printf '%s\n' "$VARIANTE" > config/includes.chroot/etc/skillfish-kernel-variant
echo "    variante del kernel per gli hook: $VARIANTE"

# ⚠️ IL NUMERO DI VERSIONE STA IN iso/VERSIONE, E VALE LA REGOLA DEL +1
# SULL'ULTIMA PUBBLICATA SU SOURCEFORGE. Non sull'ultima costruita: due
# immagini diverse con lo stesso numero sono il modo piu' veloce per non capire
# piu' quale sta girando su una macchina.
VERSIONE=$(tr -d ' \n' < VERSIONE 2>/dev/null)
[ -n "$VERSIONE" ] || { echo "manca iso/VERSIONE" >&2; exit 2; }
NOME_EDIZIONE=$([ "${EDIZIONE:-generic}" = bc250 ] && echo BC250 || echo Generic)
ISO_FINALE="SkillFishOS-${VERSIONE}-Aetherium-${NOME_EDIZIONE}-amd64.iso"

echo "=== SkillFish OS Build ==="
echo "Edizione: $EDIZIONE | Kernel: linux-tkg $SAPORE ($DESCR)"
echo "Distribution: Debian sid | Desktop: KDE Plasma 6"
echo ""

# La lista dell'hardware BC-250 entra solo nell'edizione della scheda: la
# nostra Mesa e' il driver della gfx1013, su un PC normale non ha senso.
LISTA_BC=config/package-lists/30-hardware-bc250.list.chroot
if [ "$EDIZIONE" = "bc250" ]; then
    [ -f "$LISTA_BC.esclusa" ] && mv "$LISTA_BC.esclusa" "$LISTA_BC"
else
    [ -f "$LISTA_BC" ] && mv "$LISTA_BC" "$LISTA_BC.esclusa"
fi


# Il numero di versione dentro l'immagine: la schermata di Calamares e
# /etc/os-release, cosi' il sistema installato sa dire cos'e'.
BRAND=config/includes.chroot/etc/calamares/branding/skillfish/branding.desc
if [ -f "$BRAND" ]; then
    sed -i -E "s/^( *shortVersionedName:).*/\\1 SkillFishOS ${VERSIONE} Aetherium/;
               s/^( *versionedName:).*/\\1 SkillFishOS ${VERSIONE} Aetherium/;
               s/^( *version:).*/\\1 '${VERSIONE}'/" "$BRAND"
fi
OSREL=config/includes.chroot/etc/os-release
if [ -f "$OSREL" ]; then
    sed -i "/^VERSION/d; /^PRETTY_NAME/d" "$OSREL"
    {
        echo "VERSION=\"${VERSIONE} (Aetherium)\""
        echo "VERSION_ID=\"${VERSIONE}\""
        echo "VERSION_CODENAME=aetherium"
        echo "PRETTY_NAME=\"SkillFishOS ${VERSIONE} Aetherium\""
    } >> "$OSREL"
fi
echo "    versione dentro l'immagine: $VERSIONE"

# Prerequisites check
for cmd in lb debootstrap git curl gpg; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "ERROR: '$cmd' is required. Run: apt-get install live-build debootstrap git curl gnupg"
        exit 1
    fi
done

# Run lb config (fetches keys, configures live-build)
echo ">>> Running auto/config ..."
bash auto/config

# Build
# --- WORKAROUND (custom kernel) -------------------------------------------
# With --linux-packages none (kernel installed via hook 0005, not apt),
# live-build's binary_linux-image early-exits and never copies the kernel
# into binary/live, breaking syslinux/grub. Neutralize that gate so it still
# globs chroot/boot/vmlinuz-* into the image.
BLI=/usr/lib/live/build/binary_linux-image
if [ -f "$BLI" ] && ! grep -q 'SKF-patched' "$BLI"; then
    sed -i 's|if \[ "${LB_LINUX_PACKAGES}" = "none" \]|if false  # SKF-patched: kernel from hook 0005|' "$BLI"
    echo "Patched $BLI for custom-kernel binary copy."
fi
# --------------------------------------------------------------------------

echo ">>> Running lb build ..."
lb build noauto 2>&1 | tee build.log
echo ""
echo "=== Build complete ==="
USCITA=$(ls -1 *.hybrid.iso SkillFishOS*.iso 2>/dev/null | head -1)
if [ -n "$USCITA" ] && [ "$USCITA" != "$ISO_FINALE" ]; then
    mv "$USCITA" "$ISO_FINALE"
fi
if [ -f "$ISO_FINALE" ]; then
    sha256sum "$ISO_FINALE" | tee "$ISO_FINALE.sha256"
    ls -lh "$ISO_FINALE"
else
    echo "Nessuna ISO: guarda build.log"
fi

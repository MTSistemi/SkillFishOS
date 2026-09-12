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
export SKILLFISH_KERNEL_VARIANT="$VARIANTE"
export SKILLFISH_LINUX_FLAVOUR="$SAPORE"

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
ls -lh skillfish-os*.iso 2>/dev/null || echo "Check build.log for errors."

#!/bin/bash
set -e
cd "$(dirname "$0")"

echo "=== SkillFish OS Build ==="
echo "Distribution: Debian forky | Desktop: Hyprland+DMS | Kernel: linux-tkg 7.0.10 (BORE/znver2/BC-250)"
echo ""

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

# Copy governor binaries into includes.chroot if they exist on the build host
GOV_SRC="/usr/local/bin/cyan-skillfish-governor-smu"
GOV_DEST="config/includes.chroot/usr/local/bin/cyan-skillfish-governor-smu"
if [ -x "$GOV_SRC" ] && [ ! -f "$GOV_DEST" ]; then
    mkdir -p "$(dirname "$GOV_DEST")"
    cp "$GOV_SRC" "$GOV_DEST"
    cp "/usr/local/bin/cyan-skillfish-performance-mode"        "config/includes.chroot/usr/local/bin/cyan-skillfish-performance-mode" 2>/dev/null || true
    echo "Governor binaries copied from build host."
fi

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

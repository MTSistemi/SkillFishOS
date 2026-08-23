#!/bin/bash
# Build the skillfishos-kernel wrapper for a given kernel version.
# Usage: build_wrapper.sh <kver> <debver> <reltag> [wrapver]
#   e.g. build_wrapper.sh 7.2.0-skillfishos 7.2.0-1 kernel-7.2.0-skillfishos
#        build_wrapper.sh 7.2.0-skillfishos 7.2.0-1 kernel-7.2.0-skillfishos 7.2.0-2
#
# ⚠️ DEBVER e WRAPVER sono due cose diverse, e prima erano la stessa.
# DEBVER e' la versione dei .deb del KERNEL, e finisce dentro i nomi dei file
# del rilascio GitHub. WRAPVER e' la versione di QUESTO pacchetto. Tenendole
# unite, per pubblicare un wrapper corretto bisognava ricostruire e
# ripubblicare anche 155 MB di kernel, o il download sarebbe andato a cercare
# un file che non esiste. Senza il quarto argomento, WRAPVER vale DEBVER e
# tutto si comporta come prima.
set -euo pipefail
KVER="$1"; DEBVER="$2"; RELTAG="$3"; WRAPVER="${4:-$2}"
OUT=/root/wrap; rm -rf "$OUT"; mkdir -p "$OUT/DEBIAN"
cat > "$OUT/DEBIAN/control" <<EOF
Package: skillfishos-kernel
Version: ${WRAPVER}
Architecture: amd64
Maintainer: SkillFishOS <apt@skillfishos.com>
Depends: curl | wget, initramfs-tools, skillfish-base (>= 26.08.27)
Section: kernel
Priority: optional
Description: SkillFishOS BC-250 kernel (linux-tkg ${KVER})
 Meta-package that downloads and installs the prebuilt linux-tkg ${KVER} kernel
 (image + headers) for the AMD BC-250 from the SkillFishOS GitHub release. The
 ~150 MB kernel image is hosted as a release asset because GitHub's 100 MB/file
 limit prevents shipping it in the APT pool.
EOF
cat > "$OUT/DEBIAN/postinst" <<EOF
#!/bin/sh
set -e
BASE="https://github.com/MTSistemi/SkillFishOS/releases/download/${RELTAG}"
IMG="linux-image-${KVER}_${DEBVER}_amd64.deb"
HDR="linux-headers-${KVER}_${DEBVER}_amd64.deb"
# La cache non e' temporanea apposta: i due .deb devono sopravvivere alla fine
# del postinst, perche' a installarli sara' un lavoro che parte dopo.
CACHE=/var/cache/skillfishos-kernel
dl(){ if command -v curl >/dev/null 2>&1; then curl -fSL "\$1" -o "\$2"; else wget -O "\$2" "\$1"; fi; }
if dpkg-query -W -f='\${Status}' linux-image-${KVER} 2>/dev/null | grep -q "install ok installed"; then
  echo "skillfishos-kernel: ${KVER} already installed, skipping download."
else
  echo "skillfishos-kernel: fetching ${KVER} image + headers from GitHub release..."
  mkdir -p "\$CACHE"
  if ! dl "\$BASE/\$IMG" "\$CACHE/\$IMG" || ! dl "\$BASE/\$HDR" "\$CACHE/\$HDR"; then
    # Rete assente o rilascio irraggiungibile: non e' un motivo per rompere apt.
    echo "skillfishos-kernel: download failed, the kernel was NOT installed."
    echo "  retry later with:  sudo dpkg-reconfigure skillfishos-kernel"
    rm -f "\$CACHE/\$IMG" "\$CACHE/\$HDR"
    exit 0
  fi
  # ⚠️ QUI NON SI INSTALLA. Un dpkg -i dentro un postinst non puo' prendere il
  # lock del database, perche' ce l'ha dpkg che sta eseguendo questo script.
  # Prima ci provava lo stesso: usciva 100, il pacchetto restava in iF e da quel
  # momento ogni comando apt della macchina falliva, «apt -f install» compreso.
  # Riprodotto in un container pulito il 23/08/2026.
  if command -v systemd-run >/dev/null 2>&1; then
    systemd-run --quiet --on-active=20 --unit=skillfishos-kernel-install \\
      /bin/sh -c "dpkg -i '\$CACHE/\$IMG' '\$CACHE/\$HDR' && apt-mark hold linux-image-${KVER} linux-headers-${KVER} >/dev/null 2>&1; command -v update-grub >/dev/null 2>&1 && update-grub; rm -f '\$CACHE/\$IMG' '\$CACHE/\$HDR'" >/dev/null 2>&1 || true
    echo "skillfishos-kernel: ${KVER} will be installed in the background in a few seconds."
    echo "  follow it with:  systemctl status skillfishos-kernel-install"
  else
    # Niente systemd: si dice all'utente la riga esatta invece di lasciarlo
    # con due file scaricati e nessuna spiegazione.
    echo "skillfishos-kernel: no systemd here, finish by hand with:"
    echo "  sudo dpkg -i \$CACHE/\$IMG \$CACHE/\$HDR"
  fi
fi
# ⚠️ IL BLOCCO, e perche' prima non c'era mai.
# Sta fuori dal ramo perche' non dipende dall'aver scaricato: se il kernel era
# gia' li' — messo a mano dal rilascio GitHub, o perche' e' la macchina su cui
# l'abbiamo costruito — restava senza.
# E soprattutto: `apt-mark hold` scrive le selezioni di dpkg e vuole il lock del
# frontend, che dentro un postinst ce l'ha dpkg stesso. Esce 100 e non fa
# niente. Con `2>/dev/null || true` davanti non se ne accorgeva nessuno, e la
# riga «il kernel e' trattenuto» nella documentazione era falsa da mesi.
# Si prova subito (fuori da una transazione funziona), e se non passa si
# riprova quando dpkg ha mollato il lock.
if ! apt-mark hold linux-image-${KVER} linux-headers-${KVER} >/dev/null 2>&1; then
  if command -v systemd-run >/dev/null 2>&1; then
    systemd-run --quiet --on-active=15 --unit=skillfishos-kernel-hold \
      /usr/bin/apt-mark hold linux-image-${KVER} linux-headers-${KVER} >/dev/null 2>&1 || true
  fi
fi
# update-grub lo fa il lavoro programmato, dopo aver messo il kernel: farlo qui
# rigenererebbe il menu prima che il kernel esista.
exit 0
EOF
chmod 0755 "$OUT/DEBIAN/postinst"
# ⚠️ LA SCHEDA E L'ICONA VANNO QUI, non in scripts/build-debs-ci.sh.
# Questo .deb lo scrive questo file, e per questo era l'unico nostro pacchetto
# che nell'Hub restava senza descrizione tradotta, senza icona e senza note.
SRC=/root/sfx-src
install -Dm644 "$SRC/kernel-build/os.skillfish.kernel-image.metainfo.xml" "$OUT/usr/share/metainfo/os.skillfish.kernel-image.metainfo.xml"
install -Dm644 "$SRC/system/usr/share/icons/hicolor/scalable/apps/skillfishos-kernel.svg" "$OUT/usr/share/icons/hicolor/scalable/apps/skillfishos-kernel.svg"
for M in 48 128 256; do
  install -Dm644 "$SRC/system/usr/share/icons/hicolor/${M}x${M}/apps/skillfishos-kernel.png" "$OUT/usr/share/icons/hicolor/${M}x${M}/apps/skillfishos-kernel.png"
done
dpkg-deb --root-owner-group --build "$OUT" "/root/skillfishos-kernel_${WRAPVER}_amd64.deb"
echo "=== built ==="; dpkg-deb -I "/root/skillfishos-kernel_${WRAPVER}_amd64.deb" | grep -E 'Package|Version|Description' | head -3
echo "--- postinst preview ---"; sed -n '1,8p' "$OUT/DEBIAN/postinst"

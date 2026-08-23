#!/bin/bash
# Build the skillfishos-kernel wrapper for a given kernel version.
# Usage: build_wrapper.sh <kver> <debver> <reltag> [wrapver] [kver_x64]
#   e.g. build_wrapper.sh 7.2.0-skillfishos 7.2.0-1 kernel-7.2.0-skillfishos
#        build_wrapper.sh 7.2.0-skillfishos 7.2.0-1 kernel-7.2.0-skillfishos 7.2.0-3 7.2.0-skillfishos-x64
#
# ⚠️ DEBVER e WRAPVER sono due cose diverse, e prima erano la stessa.
# DEBVER e' la versione dei .deb del KERNEL, e finisce dentro i nomi dei file
# del rilascio GitHub. WRAPVER e' la versione di QUESTO pacchetto. Tenendole
# unite, per pubblicare un wrapper corretto bisognava ricostruire e
# ripubblicare anche 155 MB di kernel, o il download sarebbe andato a cercare
# un file che non esiste. Senza il quarto argomento, WRAPVER vale DEBVER e
# tutto si comporta come prima.
#
# ⚠️ IL QUINTO ARGOMENTO, e perche' esiste (23/08/2026).
# Questo pacchetto si chiama skillfishos-kernel su OGNI macchina, ma fino a oggi
# scaricava sempre e solo il kernel della BC-250. Su un PC normale quel kernel
# e' tarato znver2 e non parte: l'utente vede GRUB caricare e poi niente. E'
# successo davvero, ed e' la issue #53. Adesso il postinst guarda l'hardware con
# /usr/local/bin/skillfish-is-bc250 — lo stesso controllo che gia' fa da guardia
# ai servizi della scheda — e scarica il flavour giusto. Senza quinto argomento
# non c'e' nessuna alternativa x64 e si comporta come prima.
#
# ⚠️ IL POSTINST SI SCRIVE CON I SEGNAPOSTO, non con un heredoc che espande.
# Prima era un <<EOF non quotato, quindi ogni variabile di ESECUZIONE andava
# scritta \$COSI. Con due flavour e una scelta a tempo di installazione le
# variabili di esecuzione diventano tante, e una barra dimenticata non da'
# errore: da' un postinst che fa la cosa sbagliata in silenzio. Qui l'heredoc e'
# quotato — dentro non si espande NIENTE — e i tre valori noti a tempo di
# costruzione entrano dopo, con una sed su segnaposto @COSI@.
set -euo pipefail
KVER="$1"; DEBVER="$2"; RELTAG="$3"; WRAPVER="${4:-$2}"; KVER_X64="${5:-}"
OUT=/root/wrap; rm -rf "$OUT"; mkdir -p "$OUT/DEBIAN"

if [ -n "$KVER_X64" ]; then
  DESCR="SkillFishOS kernel (linux-tkg ${KVER} / ${KVER_X64})"
  DESCR2=" Meta-package that downloads and installs the prebuilt linux-tkg kernel (image
 + headers) from the SkillFishOS GitHub release. It picks the right build for the
 machine it is installed on: ${KVER} on an AMD BC-250, ${KVER_X64} on
 any other x86-64 PC. The ~150 MB kernel image is hosted as a release asset
 because GitHub's 100 MB/file limit prevents shipping it in the APT pool."
else
  DESCR="SkillFishOS BC-250 kernel (linux-tkg ${KVER})"
  DESCR2=" Meta-package that downloads and installs the prebuilt linux-tkg ${KVER} kernel
 (image + headers) for the AMD BC-250 from the SkillFishOS GitHub release. The
 ~150 MB kernel image is hosted as a release asset because GitHub's 100 MB/file
 limit prevents shipping it in the APT pool."
fi

cat > "$OUT/DEBIAN/control" <<EOF
Package: skillfishos-kernel
Version: ${WRAPVER}
Architecture: amd64
Maintainer: SkillFishOS <apt@skillfishos.com>
Depends: curl | wget, initramfs-tools, skillfish-base (>= 26.08.27)
Section: kernel
Priority: optional
Description: ${DESCR}
${DESCR2}
EOF

# Heredoc QUOTATO: qui dentro non si espande niente, ne' a tempo di costruzione
# ne' per sbaglio. I valori entrano subito sotto con una sed sui segnaposto.
cat > "$OUT/DEBIAN/postinst" <<'POSTINST'
#!/bin/sh
set -e
BASE="https://github.com/MTSistemi/SkillFishOS/releases/download/@RELTAG@"
DEBVER="@DEBVER@"

# ⚠️ QUALE KERNEL. Il pacchetto e' uno solo ma i kernel sono due, e prendere
# quello sbagliato vuol dire una macchina che non riparte (issue #53). Il
# controllo e' lo stesso che fa da ExecCondition ai servizi della scheda:
# /usr/local/bin/skillfish-is-bc250, spedito da skillfish-base, esce 0 solo su
# una BC-250 vera (CPU e device PCI 0x13fe).
# Se il controllo non c'e' — installazione vecchia, o skillfish-base non ancora
# aggiornato — si ricade sul kernel della BC-250, che e' il comportamento di
# prima: non peggioriamo la situazione di nessuno.
KVER="@KVER@"
if [ -n "@KVER_X64@" ]; then
  if [ -x /usr/local/bin/skillfish-is-bc250 ]; then
    if /usr/local/bin/skillfish-is-bc250 >/dev/null 2>&1; then
      KVER="@KVER@"
      echo "skillfishos-kernel: this is a BC-250, using $KVER"
    else
      KVER="@KVER_X64@"
      echo "skillfishos-kernel: not a BC-250, using $KVER"
    fi
  else
    echo "skillfishos-kernel: no hardware check available, falling back to $KVER"
  fi
fi

IMG="linux-image-${KVER}_${DEBVER}_amd64.deb"
HDR="linux-headers-${KVER}_${DEBVER}_amd64.deb"
# La cache non e' temporanea apposta: i due .deb devono sopravvivere alla fine
# del postinst, perche' a installarli sara' un lavoro che parte dopo.
CACHE=/var/cache/skillfishos-kernel
dl(){ if command -v curl >/dev/null 2>&1; then curl -fSL "$1" -o "$2"; else wget -O "$2" "$1"; fi; }
if dpkg-query -W -f='${Status}' "linux-image-${KVER}" 2>/dev/null | grep -q "install ok installed"; then
  echo "skillfishos-kernel: ${KVER} already installed, skipping download."
else
  echo "skillfishos-kernel: fetching ${KVER} image + headers from GitHub release..."
  mkdir -p "$CACHE"
  if ! dl "$BASE/$IMG" "$CACHE/$IMG" || ! dl "$BASE/$HDR" "$CACHE/$HDR"; then
    # Rete assente o rilascio irraggiungibile: non e' un motivo per rompere apt.
    echo "skillfishos-kernel: download failed, the kernel was NOT installed."
    echo "  retry later with:  sudo dpkg-reconfigure skillfishos-kernel"
    rm -f "$CACHE/$IMG" "$CACHE/$HDR"
    exit 0
  fi
  # ⚠️ QUI NON SI INSTALLA. Un dpkg -i dentro un postinst non puo' prendere il
  # lock del database, perche' ce l'ha dpkg che sta eseguendo questo script.
  # Prima ci provava lo stesso: usciva 100, il pacchetto restava in iF e da quel
  # momento ogni comando apt della macchina falliva, «apt -f install» compreso.
  # Riprodotto in un container pulito il 23/08/2026.
  if command -v systemd-run >/dev/null 2>&1; then
    systemd-run --quiet --on-active=20 --unit=skillfishos-kernel-install \
      /bin/sh -c "dpkg -i '$CACHE/$IMG' '$CACHE/$HDR' && apt-mark hold linux-image-${KVER} linux-headers-${KVER} >/dev/null 2>&1; command -v update-grub >/dev/null 2>&1 && update-grub; rm -f '$CACHE/$IMG' '$CACHE/$HDR'" >/dev/null 2>&1 || true
    echo "skillfishos-kernel: ${KVER} will be installed in the background in a few seconds."
    echo "  follow it with:  systemctl status skillfishos-kernel-install"
  else
    # Niente systemd: si dice all'utente la riga esatta invece di lasciarlo
    # con due file scaricati e nessuna spiegazione.
    echo "skillfishos-kernel: no systemd here, finish by hand with:"
    echo "  sudo dpkg -i $CACHE/$IMG $CACHE/$HDR"
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
if ! apt-mark hold "linux-image-${KVER}" "linux-headers-${KVER}" >/dev/null 2>&1; then
  if command -v systemd-run >/dev/null 2>&1; then
    systemd-run --quiet --on-active=15 --unit=skillfishos-kernel-hold \
      /usr/bin/apt-mark hold "linux-image-${KVER}" "linux-headers-${KVER}" >/dev/null 2>&1 || true
  fi
fi
# update-grub lo fa il lavoro programmato, dopo aver messo il kernel: farlo qui
# rigenererebbe il menu prima che il kernel esista.
exit 0
POSTINST

# I valori noti a tempo di costruzione entrano adesso. Il separatore e' | perche'
# tag e versioni contengono trattini e punti, mai una barra verticale.
sed -i \
  -e "s|@RELTAG@|${RELTAG}|g" \
  -e "s|@DEBVER@|${DEBVER}|g" \
  -e "s|@KVER_X64@|${KVER_X64}|g" \
  -e "s|@KVER@|${KVER}|g" \
  "$OUT/DEBIAN/postinst"
# I due segnaposto non si pestano i piedi: la chiusura e' una @ su entrambi, e
# «@KVER_X64@» non contiene «@KVER@». Il controllo qui sotto e' la rete: se un
# giorno se ne aggiunge uno che collide, il pacchetto non si costruisce invece
# di uscire con una riga sbagliata dentro.
if grep -q '@[A-Z_]*@' "$OUT/DEBIAN/postinst"; then
  echo "ERRORE: segnaposto non sostituiti nel postinst:" >&2
  grep -o '@[A-Z_]*@' "$OUT/DEBIAN/postinst" | sort -u >&2
  exit 1
fi
chmod 0755 "$OUT/DEBIAN/postinst"
# Un postinst che non e' sh valido rompe l'installazione a casa dell'utente, non
# qui: si controlla adesso.
sh -n "$OUT/DEBIAN/postinst" || { echo "ERRORE: il postinst non e' sh valido" >&2; exit 1; }

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
echo "--- quale kernel sceglie il postinst ---"; grep -nE 'KVER="|skillfish-is-bc250' "$OUT/DEBIAN/postinst" | head -8

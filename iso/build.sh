#!/bin/bash
set -e
cd "$(dirname "$0")"

# ⚠️ QUALE EDIZIONE. Ne pubblichiamo due e finora questo file ne costruiva una
# sola, con dentro anche i pacchetti dell'altra. L'edizione decide tre cose
# INSIEME, e sbagliarne una sola da' un'immagine che sembra giusta e non parte:
#
#   EDIZIONE=generic  kernel 7.2.6-skillfishos-x64  lista BC-250 esclusa
#   EDIZIONE=bc250    kernel 7.2.6-skillfishos      lista BC-250 inclusa
#
# ⚠️ live-build vive in /usr/sbin (debootstrap, mksquashfs, xorriso). Una shell
# non interattiva, per esempio quella di una connessione ssh con un comando
# solo, quel percorso non ce l'ha: la costruzione si fermava dicendo che manca
# debootstrap, che invece e' installato da sempre.
case ":$PATH:" in *:/usr/sbin:*) ;; *) PATH="$PATH:/usr/sbin:/sbin" ;; esac
export PATH

EDIZIONE="${EDIZIONE:-generic}"
case "$EDIZIONE" in
    bc250)   SAPORE="7.2.6-skillfishos";     VARIANTE="bc250"; DESCR="BC-250 (znver2)" ;;
    generic) SAPORE="7.2.6-skillfishos-x64"; VARIANTE="x64";   DESCR="generic x86-64" ;;
    *) echo "EDIZIONE sconosciuta: $EDIZIONE (bc250 o generic)" >&2; exit 2 ;;
esac
export SKILLFISH_LINUX_FLAVOUR="$SAPORE"
# ⚠️ L'ambiente NON attraversa il chroot: live-build esegue gli hook dentro, e
# li' SKILLFISH_KERNEL_VARIANT non arriva. La prima immagine "BC-250" e' uscita
# col kernel x64 proprio cosi'. L'edizione si scrive in un file che entra
# nell'immagine, e l'hook 0005 legge quello.
install -d config/includes.chroot/etc
# ⚠️ live-build gira da root e lascia i suoi file dentro includes.chroot con
# quel proprietario: alla seconda costruzione questo file non e' piu' nostro e
# il `>` si ferma con "Permesso negato". Si toglie prima di riscriverlo.
VAR_FILE=config/includes.chroot/etc/skillfish-kernel-variant
[ -e "$VAR_FILE" ] && [ ! -w "$VAR_FILE" ] && sudo rm -f "$VAR_FILE"
printf '%s\n' "$VARIANTE" > "$VAR_FILE"
echo "    variante del kernel per gli hook: $VARIANTE"

# ⚠️ IL NUMERO DI VERSIONE STA IN iso/VERSIONE, E VALE LA REGOLA DEL +1
# SULL'ULTIMA PUBBLICATA SU SOURCEFORGE. Non sull'ultima costruita: due
# immagini diverse con lo stesso numero sono il modo piu' veloce per non capire
# piu' quale sta girando su una macchina.
VERSIONE=$(tr -d ' \n' < VERSIONE 2>/dev/null)
[ -n "$VERSIONE" ] || { echo "manca iso/VERSIONE" >&2; exit 2; }

# ⚠️ E QUI SI CONTROLLA DAVVERO. Il commento qui sopra c'e' dal primo giorno e
# non ha impedito due immagini 26.06.6 mentre su SourceForge c'era la 26.06.4.
ATTESA=$(bash "$(dirname "$0")/../scripts/versione-iso-attesa.sh" 2>/dev/null)
if [ -z "$ATTESA" ]; then
    echo "FERMO: non riesco a chiedere a SourceForge qual e' l'ultima" >&2
    echo "       immagine pubblicata, quindi non so se $VERSIONE e' giusta." >&2
    echo "       Guarda https://sourceforge.net/projects/skillfishos/files/ e," >&2
    echo "       se il numero e' quello, rilancia con SALTA_CONTROLLO_VERSIONE=1" >&2
    [ "${SALTA_CONTROLLO_VERSIONE:-0}" = 1 ] || exit 2
elif [ "$VERSIONE" != "$ATTESA" ]; then
    echo "FERMO: iso/VERSIONE dice $VERSIONE, ma l'ultima pubblicata su" >&2
    echo "       SourceForge chiede la $ATTESA." >&2
    echo "       Il numero e' +1 sull'ULTIMA PUBBLICATA, non sull'ultima" >&2
    echo "       costruita: i file di prova sul disco non contano. Se il nome" >&2
    echo "       e' gia' occupato si sposta il vecchio." >&2
    exit 2
fi
echo "    versione: $VERSIONE (ultima pubblicata + 1)"
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
    # ⚠️ shortVersion c'e' perche' mancava: era rimasta a 26.06.3 dentro
    # un'immagine 26.06.5, e si vede nel titolo della finestra.
    sed -i -E "s/^( *shortVersion:).*/\\1 '${VERSIONE}'/;
               s/^( *shortVersionedName:).*/\\1 SkillFishOS ${VERSIONE} Aetherium/;
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
# ⚠️ I CINQUE FILE CHE lb config RIGENERA RESTANO DI ROOT.
# live-build gira i suoi passi da root e questi cinque (bootstrap, binary,
# chroot, common, source) rimangono con quel proprietario: alla costruzione
# dopo `lb config` non riesce piu' a riscriverli e si ferma con "Permission
# denied". Sono generati da lb config a ogni giro e stanno nel .gitignore:
# toglierli non perde niente. ⚠️ Solo questi cinque nomi, mai config/ intero:
# li' dentro ci sono le nostre liste, gli hook e includes.chroot.
for f in bootstrap binary chroot common source; do
    if [ -e "config/$f" ] && [ ! -w "config/$f" ]; then sudo rm -f "config/$f"; fi
done
# Stessa storia per .build, il quaderno dove live-build segna i passi gia'
# fatti: lo scrive da root e `lb clean` non lo tocca.
if [ -d .build ] && [ ! -w .build ]; then sudo rm -rf .build; fi

# ⚠️ IL CONTROLLO DELL'ARCHIVIO VA FATTO ADESSO, NON DOPO.
# I nostri pacchetti si scaricano da GitHub Pages, che dopo un push ci mette
# qualche minuto a mostrare i file nuovi. Se non ci sono, live-build se ne
# accorge DOPO il bootstrap, con "Unable to locate package", e a quel punto il
# chroot e' gia' da rifare da capo. Un HEAD adesso costa un secondo.
ARCHIVIO=https://mtsistemi.github.io/SkillFishOS
INDICE="$ARCHIVIO/dists/aetherium/main/binary-amd64/Packages"
if command -v curl >/dev/null 2>&1; then
    echo ">>> controllo dell'archivio ..."
    PKGS=$(curl -fsS --max-time 30 "$INDICE" 2>/dev/null) || {
        echo "L'archivio non risponde: $INDICE" >&2
        echo "Senza quello esce un Debian sid con KDE, non SkillFishOS." >&2
        exit 3
    }
    # L'ultimo pacchetto della lista e' quello che si e' pubblicato per ultimo:
    # se c'e' quello, ci sono anche gli altri.
    for ATTESO in skillfish-boot skillfish-theme skillfish-base skillfishos-kernel; do
        FILE=$(printf '%s' "$PKGS" | awk -v p="Package: $ATTESO" \
               '$0 == p { f = 1 } f && /^Filename:/ { print $2; exit }')
        if [ -z "$FILE" ]; then
            echo "L'indice dell'archivio non elenca $ATTESO." >&2
            echo "Hai pubblicato? scripts/pubblica-apt.sh e poi sincronizza-ghpages.py" >&2
            exit 3
        fi
        if ! curl -fsI --max-time 30 "$ARCHIVIO/$FILE" >/dev/null 2>&1; then
            echo "$ATTESO e' nell'indice ma il file non si scarica ancora:" >&2
            echo "   $ARCHIVIO/$FILE" >&2
            echo "GitHub Pages sta ancora pubblicando: aspetta un paio di minuti." >&2
            exit 3
        fi
    done
    echo "    archivio a posto"
    # Issue #103: hook 0005 installs the kernel skillfishos-kernel names, while
    # live-build boots $SAPORE. If the two differ the image has no bootable
    # kernel, so they are compared here, before hours of chroot.
    KPKG=$(printf '%s' "$PKGS" | awk '$0 == "Package: skillfishos-kernel" { f = 1 }
                                      f && /^Version:/ { print $2; exit }')
    if [ "${KPKG%%-*}" != "${SAPORE%%-*}" ]; then
        echo "FERMO: skillfishos-kernel $KPKG brings kernel ${KPKG%%-*}, but this" >&2
        echo "       build boots $SAPORE. Align SAPORE above with the published kernel." >&2
        exit 3
    fi
    echo "    kernel: $SAPORE, the one skillfishos-kernel $KPKG brings"
fi

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

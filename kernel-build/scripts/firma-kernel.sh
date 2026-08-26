#!/bin/bash
# Firma il vmlinuz dentro i pacchetti del kernel con la chiave Secure Boot di
# SkillFishOS, e li richiude.
#
#   firma-kernel.sh <linux-image-*.deb> [altri.deb ...]
#   firma-kernel.sh /root/linux-tkg/DEBS/linux-image-*.deb
#
# PERCHE'. Con Secure Boot acceso — cioe' come esce di fabbrica quasi ogni PC —
# un kernel che nessuno ha firmato viene rifiutato dallo shim e la macchina non
# parte: «Verification failed: Security Policy Violation». E' la segnalazione
# #53. Firmato con la NOSTRA chiave, dopo che l'utente l'ha registrata una volta
# sola, lo stesso kernel parte. Provato il 26/08/2026 sulla VM 953 del Proxmox
# 192.168.5.102: stesso prompt di GRUB, il kernel non firmato respinto e quello
# firmato caricato senza un errore.
#
# ⚠️ FIRMARE NON FA MALE A NESSUNO. Con Secure Boot spento la firma viene
# ignorata e il kernel parte come sempre. Quindi si firma SEMPRE, tutte le
# edizioni, senza casi particolari da ricordarsi.
#
# ⚠️ LA CHIAVE PRIVATA NON STA NEL REPOSITORY e non ci deve finire. Sta in
# /root/.skillfishos-secureboot sulla macchina che firma, con i permessi 600, ed
# e' da custodire come quella dell'archivio apt: se si perde, chi ha registrato
# la nostra chiave non riceve piu' kernel che il suo firmware accetti.
set -euo pipefail
export LC_ALL=C

DIR="${SKF_SB_DIR:-/root/.skillfishos-secureboot}"
KEY="$DIR/SkillFishOS-SB.key"
CRT="$DIR/SkillFishOS-SB.crt"

if [ $# -eq 0 ]; then
    echo "uso: $0 <linux-image-*.deb> [altri.deb ...]" >&2
    exit 2
fi
for c in sbsign sbverify sbattach dpkg-deb; do
    command -v "$c" >/dev/null 2>&1 || { echo "manca $c (apt install sbsigntool)" >&2; exit 1; }
done
if [ ! -f "$KEY" ] || [ ! -f "$CRT" ]; then
    echo "la chiave Secure Boot non e' su questa macchina: $DIR" >&2
    echo "sta dove si firma, fuori dal repository. Portala qui, oppure firma da li'." >&2
    exit 1
fi

# ⚠️ `sbverify --list` ESCE 0 ANCHE SENZA FIRMA: stampa «No signature table
# present» e non se ne lamenta. Un controllo basato sul codice di uscita dice
# «firmato» per qualunque file. Si guarda il testo.
firmato_da_noi() {
    sbverify --cert "$CRT" "$1" 2>&1 | grep -q 'Signature verification OK'
}

fatti=0; gia=0; saltati=0
for deb in "$@"; do
    nome=$(basename "$deb")
    case "$nome" in
        linux-image-*) ;;
        *) printf '   %-56s non e un pacchetto immagine, lo salto\n' "$nome"; saltati=$((saltati+1)); continue ;;
    esac
    case "$nome" in
        *-dbg_*) printf '   %-56s pacchetto di debug, lo salto\n' "$nome"; saltati=$((saltati+1)); continue ;;
    esac
    [ -f "$deb" ] || { echo "   $nome: non esiste" >&2; exit 1; }

    tmp=$(mktemp -d)
    # shellcheck disable=SC2064
    trap "rm -rf '$tmp'" EXIT
    dpkg-deb -R "$deb" "$tmp/x"

    k=$(find "$tmp/x/boot" -maxdepth 1 -name 'vmlinuz-*' 2>/dev/null | head -1)
    if [ -z "$k" ]; then
        printf '   %-56s dentro non c e un vmlinuz\n' "$nome"
        rm -rf "$tmp"; trap - EXIT; saltati=$((saltati+1)); continue
    fi

    if firmato_da_noi "$k"; then
        printf '   %-56s gia firmato da noi\n' "$nome"
        rm -rf "$tmp"; trap - EXIT; gia=$((gia+1)); continue
    fi

    # Una firma altrui (o mezza) va tolta prima, o sbsign ne accoda una seconda
    # e certi firmware guardano solo la prima.
    sbattach --remove "$k" >/dev/null 2>&1 || true
    sbsign --key "$KEY" --cert "$CRT" --output "$k.firmato" "$k" >/dev/null
    mv -f "$k.firmato" "$k"
    chmod 0644 "$k"

    firmato_da_noi "$k" || { echo "   $nome: la firma non torna, non lo richiudo" >&2; exit 1; }

    # ⚠️ md5sums va rifatto: il vmlinuz e' cambiato, e senza questo `dpkg -V`
    # segnala il pacchetto come manomesso a ogni controllo.
    if [ -f "$tmp/x/DEBIAN/md5sums" ]; then
        ( cd "$tmp/x" && find . -path ./DEBIAN -prune -o -type f -print0 \
            | xargs -0 md5sum 2>/dev/null | sed 's| \./| |' > DEBIAN/md5sums.nuovo \
            && mv -f DEBIAN/md5sums.nuovo DEBIAN/md5sums )
    fi

    dpkg-deb --root-owner-group --build "$tmp/x" "$deb" >/dev/null
    printf '   %-56s firmato\n' "$nome"
    fatti=$((fatti+1))
    rm -rf "$tmp"; trap - EXIT
done

echo
echo "   firmati adesso: $fatti   gia a posto: $gia   saltati: $saltati"

# --- controprova, aprendo i pacchetti veri ----------------------------------
echo
echo "   controprova (riaperti dal disco):"
for deb in "$@"; do
    nome=$(basename "$deb")
    case "$nome" in linux-image-*) ;; *) continue ;; esac
    case "$nome" in *-dbg_*) continue ;; esac
    tmp=$(mktemp -d)
    dpkg-deb -x "$deb" "$tmp" 2>/dev/null || { rm -rf "$tmp"; continue; }
    k=$(find "$tmp/boot" -maxdepth 1 -name 'vmlinuz-*' 2>/dev/null | head -1)
    if [ -n "$k" ] && firmato_da_noi "$k"; then
        printf '      %-53s firma valida\n' "$nome"
    else
        printf '      %-53s ⚠️ SENZA FIRMA\n' "$nome"
        rm -rf "$tmp"; exit 1
    fi
    rm -rf "$tmp"
done

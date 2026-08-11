#!/bin/bash
# SkillFishOS - installazione degli emulatori.
#
# PERCHE' NON SONO GIA' NELLA ISO
# Non sono stati tolti: non ci sono mai stati. Nella ISO restano solo Steam,
# Heroic, Ryujinx, ProtonUp-Qt e Minecraft. Gli emulatori pesano diversi GB in
# totale e non servono a tutti, mentre la ISO deve stare in una misura
# ragionevole (siamo passati da 10,19 GB a 4,58 GB proprio togliendo il
# superfluo). Chi li vuole se li prende con questo script.
#
# PERCHE' FLATPAK E NON APT
# La BC-250 e' una gfx1013 e va di Vulkan. Gli emulatori nei pacchetti Debian
# sono spesso vecchi di anni e su questa GPU o non partono o rendono male. I
# Flatpak sono aggiornati e portano dietro il loro runtime, che e' esattamente
# quello che serve qui.
#
# USO
#   install-emulators.sh              elenco e scelta interattiva
#   install-emulators.sh --consigliati  solo quelli che girano bene sulla BC-250
#   install-emulators.sh --tutti        tutti quelli in elenco
#   install-emulators.sh retroarch dolphin ...   solo quelli nominati
set -uo pipefail

# chiave|id flatpak|nome|descrizione|consigliato-su-bc250
EMU="
retroarch|org.libretro.RetroArch|RetroArch|Frontend multi-core: NES, SNES, Mega Drive, PS1, GBA e decine di altri|si
dolphin|org.DolphinEmu.dolphin-emu|Dolphin|GameCube e Wii|si
pcsx2|net.pcsx2.PCSX2|PCSX2|PlayStation 2|si
duckstation|org.duckstation.DuckStation|DuckStation|PlayStation 1, molto accurato|si
ppsspp|org.ppsspp.PPSSPP|PPSSPP|PlayStation Portable|si
melonds|net.kuribo64.melonDS|melonDS|Nintendo DS|si
mgba|io.mgba.mGBA|mGBA|Game Boy, Game Boy Color e Advance|si
flycast|org.flycast.Flycast|Flycast|Dreamcast e Naomi|si
lime3ds|io.github.lime3ds.Lime3DS|Lime3DS|Nintendo 3DS|si
xemu|app.xemu.xemu|xemu|Xbox originale|no
rpcs3|net.rpcs3.RPCS3|RPCS3|PlayStation 3 - pesante, su questo hardware aspettati poco|no
vita3k|org.vita3k.Vita3K|Vita3K|PlayStation Vita - ancora sperimentale|no
"

ok()   { printf '  \033[32m%s\033[0m %s\n' "OK" "$1"; }
ko()   { printf '  \033[31m%s\033[0m %s\n' "!!" "$1"; }
info() { printf '%s\n' "$1"; }

need_flatpak() {
    if ! command -v flatpak >/dev/null; then
        ko "flatpak non e' installato."
        info "  Installalo con:  sudo apt install flatpak"
        exit 1
    fi
    # Senza il remote flathub non c'e' niente da scaricare. Lo aggiungo per
    # l'utente (--user), non a sistema: cosi' non serve essere root e resta
    # coerente con il modo in cui sono installati Steam e Heroic.
    if ! flatpak remotes --user 2>/dev/null | grep -q flathub; then
        info "Aggiungo il repository Flathub per l'utente..."
        flatpak remote-add --user --if-not-exists flathub \
            https://dl.flathub.org/repo/flathub.flatpakrepo || exit 1
    fi
}

riga_di() { echo "$EMU" | awk -F'|' -v k="$1" '$1==k {print; exit}'; }

elenco() {
    printf '\n%-13s %-12s %s\n' "CHIAVE" "CONSIGLIATO" "EMULATORE"
    printf '%s\n' "-------------------------------------------------------------------"
    echo "$EMU" | while IFS='|' read -r k id nome desc cons; do
        [ -z "$k" ] && continue
        stato="no"
        flatpak info "$id" >/dev/null 2>&1 && stato="GIA' INSTALLATO"
        printf '%-13s %-12s %s\n' "$k" "$cons" "$nome"
        printf '%-13s %-12s   %s\n' "" "" "$desc"
        [ "$stato" = "GIA' INSTALLATO" ] && printf '%-13s %-12s   -> %s\n' "" "" "$stato"
    done
    echo
}

installa() {
    local k="$1" riga id nome
    riga=$(riga_di "$k")
    if [ -z "$riga" ]; then ko "chiave sconosciuta: $k"; return 1; fi
    id=$(echo "$riga" | cut -d'|' -f2); nome=$(echo "$riga" | cut -d'|' -f3)
    if flatpak info "$id" >/dev/null 2>&1; then ok "$nome era gia' installato"; return 0; fi
    info "Installo $nome ($id)..."
    if flatpak install --user -y flathub "$id"; then ok "$nome installato"; else ko "$nome NON installato"; return 1; fi
}

case "${1:-}" in
    --tutti)       need_flatpak; SEL=$(echo "$EMU" | awk -F'|' 'NF>1 {print $1}') ;;
    --consigliati) need_flatpak; SEL=$(echo "$EMU" | awk -F'|' '$5=="si" {print $1}') ;;
    "")
        elenco
        info "Scrivi le chiavi separate da spazio, oppure 'consigliati' o 'tutti'."
        read -r -p "> " risposta
        case "$risposta" in
            tutti)       SEL=$(echo "$EMU" | awk -F'|' 'NF>1 {print $1}') ;;
            consigliati) SEL=$(echo "$EMU" | awk -F'|' '$5=="si" {print $1}') ;;
            "")          info "Niente da fare."; exit 0 ;;
            *)           SEL="$risposta" ;;
        esac
        need_flatpak
        ;;
    -h|--help) sed -n '1,30p' "$0"; exit 0 ;;
    *)         need_flatpak; SEL="$*" ;;
esac

FALLITI=0
for k in $SEL; do installa "$k" || FALLITI=$((FALLITI + 1)); done

echo
if [ "$FALLITI" -gt 0 ]; then
    ko "$FALLITI non installati: rileggi i messaggi qui sopra."
else
    ok "fatto."
fi

# Il menu di KDE tiene una cache dei .desktop: senza questo le voci nuove
# possono non comparire finche' non si riavvia la sessione.
command -v kbuildsycoca6 >/dev/null && kbuildsycoca6 --noincremental >/dev/null 2>&1
info "Le voci compaiono nel menu sotto Giochi."

exit $([ "$FALLITI" -gt 0 ] && echo 1 || echo 0)

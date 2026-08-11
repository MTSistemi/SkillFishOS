#!/bin/bash
# STATO: NON FUNZIONANTE. Lo scaricamento fallisce, vedi il commento su URL
# piu sotto. Non pubblicare finche non e risolto.
# SkillFishOS - installazione di EmuDeck.
#
# COS'E' E PERCHE' CONVIENE
# EmuDeck installa e configura da solo quasi tutti gli emulatori, le cartelle
# delle ROM, i BIOS e i controlli. E' la stessa strada usata sulla board, dove
# ha portato RetroArch, Dolphin, melonDS, PPSSPP, MAME, ScummVM, xemu,
# Supermodel, Primehack piu' gli AppImage di Cemu, DuckStation e azahar.
#
# PERCHE' NON E' GIA' NELLA ISO
# EmuDeck installa TUTTO nella home dell'utente: i flatpak con --user (cioe' in
# ~/.local/share/flatpak) e gli AppImage in ~/Applications. La ISO replica
# /etc/skel, non la home di chi ha costruito il sistema, quindi quelle
# installazioni non arrivano a nessun altro. Non e' un difetto della ISO: e'
# come funziona EmuDeck, e va rifatto su ogni macchina. Da qui questo script.
#
# COSA FA
# Scarica l'AppImage ufficiale dal repository di EmuDeck su GitHub, lo mette in
# ~/Applications, gli crea una voce di menu e lo avvia. Da li' in poi comanda
# EmuDeck: sceglie tu quali emulatori installare e dove tenere le ROM.
#
# NOTA ONESTA
# EmuDeck nasce per Steam Deck. Su Linux normale funziona, ma alcune cose sono
# pensate per SteamOS: l'integrazione con la modalita' gaming di Steam e i temi
# di Steam Rom Manager possono comportarsi in modo diverso. Gli emulatori e le
# cartelle, che sono il grosso, funzionano.
set -uo pipefail

APPDIR="$HOME/Applications"
APPIMG="$APPDIR/EmuDeck.AppImage"
DESKTOP="$HOME/.local/share/applications/emudeck.desktop"
# ATTENZIONE: questo indirizzo NON funziona. La release 2.3.8 di EmuDeck non ha
# allegati su GitHub, quindi l AppImage non si distribuisce dalle release. La
# fonte vera si ricava dalla copia gia presente sulla board in
# /home/skillfish/Applications/EmuDeck.AppImage. Da sistemare prima di usarlo.
API="https://api.github.com/repos/dragoonDorise/EmuDeck/releases/latest"

ok()   { printf '  \033[32mOK\033[0m %s\n' "$1"; }
ko()   { printf '  \033[31m!!\033[0m %s\n' "$1"; }
info() { printf '%s\n' "$1"; }

# --- requisiti -------------------------------------------------------------
for c in curl flatpak; do
    command -v "$c" >/dev/null || { ko "manca $c. Installalo con: sudo apt install $c"; exit 1; }
done

# EmuDeck installa i suoi emulatori da Flathub, con --user. Senza il remote non
# potrebbe scaricare niente, e fallirebbe a meta' lavoro invece che subito.
if ! flatpak remotes --user 2>/dev/null | grep -q flathub; then
    info "Aggiungo il repository Flathub per l'utente..."
    flatpak remote-add --user --if-not-exists flathub \
        https://dl.flathub.org/repo/flathub.flatpakrepo || exit 1
fi

# --- spazio ----------------------------------------------------------------
# Un set completo di emulatori con i loro runtime supera facilmente i 10 GB, e
# EmuDeck non avvisa: si ferma a meta' con un errore poco chiaro.
LIBERI=$(df -BG --output=avail "$HOME" | tail -1 | tr -dc '0-9')
if [ "${LIBERI:-0}" -lt 15 ]; then
    ko "solo ${LIBERI} GB liberi in $HOME."
    info "  Un set completo di emulatori ne vuole almeno 15. Libera spazio o"
    info "  scegli meno emulatori dentro EmuDeck."
    read -r -p "  Continuo lo stesso? [s/N] " r
    case "$r" in s|S|y|Y) ;; *) exit 1 ;; esac
fi

# --- scarico ---------------------------------------------------------------
mkdir -p "$APPDIR" "$(dirname "$DESKTOP")"

if [ -f "$APPIMG" ]; then
    ok "EmuDeck.AppImage e' gia' in $APPDIR"
    info "  Lo sovrascrivo con l'ultima versione."
fi

info "Cerco l'ultima versione su GitHub..."
URL=$(curl -fsSL "$API" | grep -o 'https://[^"]*EmuDeck\.AppImage' | head -1)
if [ -z "$URL" ]; then
    ko "non riesco a trovare l'AppImage nelle release."
    info "  Puo' essere GitHub che limita le richieste, o un cambio di nome del file."
    info "  Scaricalo a mano da: https://github.com/dragoonDorise/EmuDeck/releases"
    exit 1
fi
info "  $URL"

# scarico su un file temporaneo e sposto solo a scaricamento riuscito, cosi' un
# download interrotto non lascia al suo posto un AppImage monco che poi non parte
TMP=$(mktemp "$APPDIR/.emudeck.XXXXXX") || exit 1
trap 'rm -f "$TMP"' EXIT
if ! curl -fL --progress-bar -o "$TMP" "$URL"; then
    ko "scaricamento fallito."; exit 1
fi
# un AppImage valido comincia con l'intestazione ELF: se GitHub ha risposto con
# una pagina di errore HTML, questo se ne accorge subito
if ! head -c 4 "$TMP" | grep -q ELF; then
    ko "il file scaricato non e' un eseguibile (probabilmente una pagina di errore)."
    exit 1
fi
mv "$TMP" "$APPIMG"; trap - EXIT
chmod +x "$APPIMG"
ok "scaricato in $APPIMG ($(du -h "$APPIMG" | cut -f1))"

# --- voce di menu ----------------------------------------------------------
cat > "$DESKTOP" <<EOF
[Desktop Entry]
Type=Application
Name=EmuDeck
GenericName=Emulator installer
GenericName[it]=Installazione emulatori
GenericName[pl]=Instalator emulatorow
GenericName[uk]=Встановлення емуляторів
Comment=Install and configure emulators, ROM folders and controls
Comment[it]=Installa e configura emulatori, cartelle ROM e controlli
Comment[pl]=Instaluje i konfiguruje emulatory, foldery ROM i sterowanie
Comment[uk]=Встановлює та налаштовує емулятори, теки ROM і керування
Exec=$APPIMG
Icon=applications-games
Terminal=false
Categories=Game;Emulator;
Keywords=emulator;emudeck;retro;roms;
EOF
ok "voce di menu creata (Giochi > EmuDeck)"

# Il menu di KDE tiene una cache dei .desktop: senza questo la voce puo' non
# comparire finche' non si riavvia la sessione.
command -v kbuildsycoca6 >/dev/null && kbuildsycoca6 --noincremental >/dev/null 2>&1

# --- avvio -----------------------------------------------------------------
echo
info "Da qui in avanti comanda EmuDeck: ti chiedera' dove tenere le ROM"
info "(consigliato un disco con spazio, non la partizione di sistema) e quali"
info "emulatori installare."
info ""
info "Sulla BC-250 vanno bene RetroArch, Dolphin, PCSX2, DuckStation, PPSSPP,"
info "melonDS e Flycast. RPCS3 e Vita3K girano male su questo hardware."
echo
read -r -p "Avvio EmuDeck adesso? [S/n] " r
case "$r" in
    n|N) info "Lo trovi nel menu sotto Giochi, o esegui: $APPIMG" ;;
    *)   exec "$APPIMG" ;;
esac

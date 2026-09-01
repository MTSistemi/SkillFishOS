#!/bin/bash
# Costruisce una ISO di SkillFishOS e la verifica.
#
# Stava solo su /root della scheda di sviluppo, quindi non era ripetibile da
# nessun altro e non aveva storia. Ora sta nel repo.
#
# LA COMPRESSIONE LA DECIDE IL FLAG, NON eggs.yaml
# Questo e' il dettaglio che costa un'ora di build se lo si sbaglia. Avevo
# impostato `compression: xz -Xbcj x86 -b 1M` in /etc/penguins-eggs.d/eggs.yaml
# e il comando realmente eseguito era `-comp zstd -b 1M -Xcompression-level 3`.
# eggs sceglie in base a un flag di `produce`:
#
#   (nessuno)       zstd -Xcompression-level 3      veloce, immagine grossa
#   -S --standard   xz -b 1M
#   -p --pendrive   zstd -b 1M -Xcompression-level 15
#   -m --max        xz -Xbcj x86 -b 1M
#
# Misurato su 641 MB di binari, -m vale il 13% in meno di -comp xz liscio: il
# filtro BCJ x86 riscrive gli indirizzi dei salti prima di comprimere e il
# blocco da 1 MB allarga la finestra di ricerca delle ripetizioni. Si paga in
# tempo di costruzione, il che per una ISO che si scarica migliaia di volte e'
# un ottimo cambio.
#
# Gli altri flag: -n nessuna interazione, -N nessuna icona di eggs sul desktop,
# -K il kernel da mettere nell'immagine. NON usare -i: includerebbe /root, cioe'
# il nostro banco di lavoro, dentro l'immagine pubblica.
#
# Uso:  sudo bash build-iso.sh 7.1.7-skillfishos-generic SkillFishOS-26.06.3-Aetherium-Generic-amd64.iso
set -u

KVER="${1:-}"
FINAL="${2:-}"
if [ -z "$KVER" ] || [ -z "$FINAL" ]; then
    echo "uso: $0 <versione-kernel> <nome-finale.iso>" >&2
    exit 2
fi

BASE="${FINAL%-amd64.iso}"
OUT=/home/iso-out
LOG="$OUT/build-$BASE.log"
ST="$OUT/$BASE.status"
mkdir -p "$OUT"

{
echo "==== BUILD $BASE (kernel $KVER) inizio: $(date) ===="
echo "RUNNING" > "$ST"

if [ ! -f "/boot/vmlinuz-$KVER" ]; then
    echo "FATAL: /boot/vmlinuz-$KVER non esiste"
    echo "FAIL-NOKERNEL" > "$ST"; exit 1
fi

# --- profilo di overclock di sicurezza, per la durata della build ----------
# L'immagine si costruisce dal sistema vivo, quindi /etc/bc250-smu-oc.conf ci
# finisce COM'E'. Sulla scheda di sviluppo c'e' il profilo di Mattia, che e'
# tarato su QUESTO esemplare: spedirlo vorrebbe dire applicare il suo overclock
# alla scheda di chiunque installi, e la lotteria del silicio non la si vince
# per procura. La ISO 26.06.3 costruita senza questo accorgimento imbarcava
# frequency = 3600.
#
# Il trap fa il ripristino anche se la build fallisce a meta' o viene
# interrotta: senza, la scheda resterebbe a 3500 e ce ne accorgeremmo tardi.
OCF=/etc/bc250-smu-oc.conf
OCBAK=/root/oc.conf.user
GOVF=/etc/cyan-skillfish-governor/config.toml
GOVBAK=/root/governor.conf.user

# --- e la lingua di partenza dell'immagine --------------------------------
# Stessa storia: /etc/default/locale finisce nell'immagine com'e', e sulla
# scheda di sviluppo dice it_IT. Ecco perche' la live partiva in italiano anche
# per chi in Italia non ci vive. La ISO deve partire in INGLESE e lasciare
# scegliere la lingua all'installazione: e' quello che ci siamo detti dopo la
# recensione, ed e' anche la scelta sensata per una distro che si scarica da
# mezzo mondo.
LOCF=/etc/default/locale
LOCBAK=/root/locale.user

# --- e la tabella ACPI della BC-250 ---------------------------------------
# Stessa storia ancora una volta, e questa faceva danno vero. La scheda ha la
# SSDT con i P-state iniettata via GRUB (GRUB_EARLY_INITRD_LINUX_CUSTOM +
# /boot/SkillFishOS-acpi.cpio). Tutti e due finiscono nell'immagine, quindi
# l'edizione GENERIC arrivava sul PC di chiunque con la tabella della BC-250 gia'
# attiva. La tabella si aggancia a \_PR.P000..P00F, che su un'altra macchina non
# esistono: misurate 32 righe di "ACPI BIOS Error (bug): Could not resolve
# symbol" a ogni avvio, installando la Generic in macchina virtuale.
# La guardia dentro skillfish-acpi-pstates non serviva a niente qui: impedisce di
# ATTIVARE la tabella, ma l'immagine se la portava dietro gia' attivata.
ACPIMARK=/root/acpi-da-riattivare

# --- e la tastiera, che nell'immagine finisce com'e' sulla scheda ------------
# ⚠️ TROVATO PROVANDO LA LIVE il 26/08/2026: scrivendo nel terminale i due punti
# uscivano «ç» e la barra verticale «§». La scheda di sviluppo ha la tastiera
# italiana, e /etc/default/keyboard finisce nell'immagine tale e quale — quindi
# un polacco o un brasiliano si ritrovano una tastiera italiana. E' la stessa
# storia della lingua, e si sistema allo stesso modo: nell'immagine si spedisce
# «us», poi l'installatore chiede all'utente quale vuole.
KBDF=/etc/default/keyboard
KBDBAK=/root/keyboard.user

# --- il nome della macchina -------------------------------------------------
# L'immagine Generic si chiamava «BC-250» anche su un PC normale, perche' eggs
# clona questa scheda. Si vede nel prompt del terminale e in rete.
HOSTF=/etc/hostname
HOSTBAK=/root/hostname.user

# --- e la riga di comando del kernel ----------------------------------------
# ⚠️ TROVATO IL 01/09/2026. /etc/default/grub finisce nell'immagine com'e', e
# Calamares ci genera sopra il grub.cfg del sistema installato: qualunque
# parametro che teniamo sulla scheda per prova arriverebbe sul PC di chiunque.
# Il caso concreto e' amdgpu.gpu_recovery=0, che stiamo provando qui perche' su
# questo hardware un reset della GPU si porta via la macchina - ma il kernel si
# marchia da solo («Setting dangerous option») e la prova non e' finita.
#
# Si toglie SOLO quello che sta in questa lista. tsc=directsync resta: e' una
# scelta fatta, non un esperimento. E i parametri bc250_* servono all'edizione
# BC-250.
GRUBF=/etc/default/grub
GRUBBAK=/root/grub.default.user
# Questi non escono MAI dalla scheda.
PARAMETRI_FUORI_DALLA_ISO="amdgpu.gpu_recovery="

# ⚠️ E QUESTI ESCONO SOLO NELL'EDIZIONE BC-250. Trovato il 01/09/2026
# guardando la riga di comando di una Generic INSTALLATA in macchina
# virtuale: si portava dietro i parametri della scheda.
# amdgpu.bc250_cc_write_mode su un PC normale viene ignorato, ma
# ttm.pages_limit FISSA il limite a 6 GB qualunque sia la RAM della
# macchina: su un PC da 4 GB e' troppo, su uno da 64 e' troppo poco.
# E' la stessa famiglia della tabella ACPI della BC-250 che per mesi
# abbiamo spedito a tutti.
PARAMETRI_SOLO_BC250="amdgpu.bc250_cc_write_mode= ttm.pages_limit= ttm.page_pool_size="
case "$FINAL" in
    *BC250*) ;;
    *) PARAMETRI_FUORI_DALLA_ISO="$PARAMETRI_FUORI_DALLA_ISO $PARAMETRI_SOLO_BC250" ;;
esac

# ⚠️ UN BACKUP RIMASTO DA UNA BUILD INTERROTTA RIMETTE VALORI VECCHI SOPRA A
# QUELLI VIVI. Le righe `[ -f "$X" ] || cp ...` piu' sotto salvano solo se il
# file non c'e' gia': serve a non sovrascrivere il backup buono se la stessa
# build ripassa di li'. Ma se una build PRECEDENTE e' morta prima del
# ripristino, quel file resta - e alla fine di QUESTA build viene rimesso al
# posto della configurazione attuale.
# Il 31/08/2026 e' successo davvero: finita la ISO, la scheda si e' ritrovata
# l'overclock a 3900, valore di una sessione vecchia, al posto dei 3700
# dell'utente. E la build aveva scritto «profilo overclock dell'utente
# ripristinato», quindi sembrava tutto a posto.
# Qui i residui si mettono da parte con la data: la configurazione VIVA e'
# l'unica verita', e quella si salva adesso.
for _vecchio in "$OCBAK" "$GOVBAK" "$LOCBAK" "$KBDBAK" "$HOSTBAK" "$GRUBBAK"; do
    if [ -f "$_vecchio" ]; then
        mv -f "$_vecchio" "$_vecchio.interrotta-$(date +%Y%m%d-%H%M%S)"
        echo "ATTENZIONE: backup di una build interrotta messo da parte: $_vecchio"
    fi
done

# --- sudo nella live --------------------------------------------------------
# ⚠️ NELLA LIVE NON SI DIVENTAVA ROOT. L'utente `live` sta nel gruppo sudo, ma la
# sua password e' VUOTA e sudo le password vuote non le accetta: usciva
# «sudo: 3 incorrect password attempts». L'unica regola senza password era per
# /usr/bin/calamares, quindi l'installatore partiva e nient'altro.
#
# ⚠️ E NON SI RIMEDIA DANDOGLI UNA PASSWORD. Con una password nota (eggs dice
# «live/evolution») sshd la accetterebbe e chiunque sulla stessa rete entrerebbe
# in una sessione live altrui. Con la password vuota sshd rifiuta, e va bene
# cosi': si lascia vuota e si da' il permesso via sudoers, come fa Debian Live.
SUDOF=/etc/sudoers.d/99-skillfish-live
SUDOMARK=/root/sudoers-live-da-togliere

restore_build_env() {
    if [ -f "$KBDBAK" ]; then
        mv -f "$KBDBAK" "$KBDF"
        echo "tastiera della scheda ripristinata: $(grep -h '^XKBLAYOUT' "$KBDF" 2>/dev/null | tr -d ' ')"
    fi
    if [ -f "$HOSTBAK.hosts" ]; then
        mv -f "$HOSTBAK.hosts" /etc/hosts
    fi
    if [ -f "$HOSTBAK" ]; then
        mv -f "$HOSTBAK" "$HOSTF"
        echo "nome della scheda ripristinato: $(cat "$HOSTF" 2>/dev/null)"
    fi
    if [ -f "$SUDOMARK" ]; then
        rm -f "$SUDOF" "$SUDOMARK"
        echo "regola sudo della live tolta dalla scheda"
    fi
    if [ -f "$GOVBAK" ]; then
        mv -f "$GOVBAK" "$GOVF"
        echo "curva GPU della scheda ripristinata: punta $(grep -h voltage "$GOVF" 2>/dev/null | tail -1 | tr -dc 0-9) mV"
    fi
    if [ -f "$OCBAK" ]; then
        mv -f "$OCBAK" "$OCF"
        echo "profilo overclock dell'utente ripristinato: $(grep -h frequency "$OCF" 2>/dev/null | tr -d ' ')"
    fi
    if [ -f "$LOCBAK" ]; then
        mv -f "$LOCBAK" "$LOCF"
        echo "lingua della scheda ripristinata: $(grep -h '^LANG=' "$LOCF" 2>/dev/null)"
    fi
    if [ -f "$GRUBBAK" ]; then
        mv -f "$GRUBBAK" "$GRUBF"
        echo "riga di comando del kernel ripristinata sulla scheda"
    fi
    if [ -f "$ACPIMARK" ]; then
        rm -f "$ACPIMARK"
        /usr/local/bin/skillfish-acpi-pstates enable >/dev/null 2>&1 \
            && echo "tabella ACPI rimessa sulla scheda" \
            || echo "ATTENZIONE: non sono riuscito a rimettere la tabella ACPI sulla scheda"
    fi
}
trap restore_build_env EXIT INT TERM

# ⚠️ NON si sovrascrive un backup che c'e' gia'. Il 19/08/2026 due build
# di fila hanno perso il profilo di Mattia: la prima non l'aveva ripristinato,
# la seconda ha salvato come "profilo dell'utente" il 3500 di sicurezza che
# aveva trovato, e il 3700/-16 e' rimasto solo dentro gli snapshot btrfs.
if [ -f "$OCF" ]; then
    [ -f "$OCBAK" ] || cp -f "$OCF" "$OCBAK"
    printf '[overclock]\nfrequency = 3500\nscale = 0\nmax_temperature = 85\n' > "$OCF"
    echo "profilo overclock: messo quello di sicurezza (3500) per la durata della build"
fi

# La riga di comando del kernel. Si salva com'e' e si tolgono i parametri che
# non devono uscire dalla scheda. Il trap la rimette anche se la build muore.
if [ -f "$GRUBF" ]; then
    [ -f "$GRUBBAK" ] || cp -f "$GRUBF" "$GRUBBAK"
    for _p in $PARAMETRI_FUORI_DALLA_ISO; do
        grep -q -- "$_p" "$GRUBF" || continue
        # ⚠️ NIENTE ESCAPE COSTRUITO CON sed. Provato il 01/09/2026: passando
        # dalla shell il backslash si perdeva, la sostituzione non toglieva
        # niente, e il parametro restava nell'immagine SENZA UN ERRORE. I
        # parametri qui sono parole semplici (lettere, cifre, punto,
        # underscore, uguale) e si tolgono cosi' come sono.
        # Le voci finiscono con «=» e si tolgono CON IL VALORE: cosi' la
        # pulizia regge anche se un domani quel valore cambia.
        sed -i "s| *$_p[^ \"]*||g" "$GRUBF"
        # ⚠️ E SI CONTROLLA. Una pulizia che fallisce in silenzio spedisce a
        # tutti quello che volevamo tenerci: meglio fermare la build.
        if grep -q -- "$_p" "$GRUBF"; then
            echo "FAIL: «$_p» è ancora nella riga di comando del kernel"
            exit 1
        fi
        echo "riga di comando: tolto «$_p», non esce dalla scheda"
    done
fi

# La curva tensione/frequenza della GPU. Stessa storia dell'overclock: l'immagine
# clona la scheda, quindi senza questo passaggio spediremmo a tutti la curva
# PERSONALE di questa scheda invece di quella di serie.
# ⚠️ E la curva di serie ora e' quella a 1080 mV di punta: quella a 1000 fa
# calcolare SBAGLIATO le schede meno tolleranti, in silenzio (issue GPU 29/08).
if [ -f "$GOVF" ]; then
    [ -f "$GOVBAK" ] || cp -f "$GOVF" "$GOVBAK"
    python3 - "$GOVF" <<'FINEGOV'
import io, re, sys
p = sys.argv[1]
t = io.open(p, encoding="utf-8").read()
t = re.sub(r'(\[\[safe-points\]\]\s*\nfrequency[^\n]*\nvoltage[^\n]*\n?)+', '', t).rstrip() + "\n"
for f, v in ((350,700),(600,872),(800,898),(1000,924),(1200,950),
             (1400,976),(1600,1002),(1800,1028),(2000,1054),(2200,1080)):
    t += "[[safe-points]]\nfrequency = %d\nvoltage = %d\n" % (f, v)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
FINEGOV
    echo "curva GPU: messa quella di serie (punta 1080 mV) per la durata della build"
fi
if [ -f "$LOCF" ]; then
    cp -f "$LOCF" "$LOCBAK"
    printf '#  File generated by update-locale\nLANG=en_US.UTF-8\n' > "$LOCF"
    echo "lingua: l'immagine partira' in inglese"
fi
if [ -f "$KBDF" ]; then
    cp -f "$KBDF" "$KBDBAK"
    printf '%s\n' \
        '# Tastiera dell immagine SkillFishOS: si parte da "us" e la sceglie' \
        '# l utente durante l installazione. La scheda che costruisce le' \
        '# immagini ha la tastiera italiana, e senza questo finiva addosso a' \
        '# chiunque scaricasse la ISO.' \
        'XKBMODEL="pc105"' \
        'XKBLAYOUT="us"' \
        'XKBVARIANT=""' \
        'XKBOPTIONS=""' \
        'BACKSPACE="guess"' > "$KBDF"
    echo "tastiera: l'immagine partira' con la disposizione us"
fi
if [ ! -f "$SUDOF" ]; then
    # ⚠️ Il file si crea QUI, non si spedisce in un pacchetto: vale solo per la
    # sessione live. skillfish-base lo toglie dai sistemi installati, dove
    # l'utente `live` non esiste.
    printf '%s\n' \
        '# Solo per la sessione live di SkillFishOS.' \
        '# L utente live ha la password vuota (cosi sshd rifiuta gli accessi da' \
        '# rete) e senza questa riga non potrebbe fare NIENTE da amministratore:' \
        '# nemmeno registrare la chiave Secure Boot. E quello che fa Debian Live.' \
        'live ALL=(ALL:ALL) NOPASSWD: ALL' > "$SUDOF"
    chmod 0440 "$SUDOF"
    touch "$SUDOMARK"
    echo "sudo: nella live l'utente potra' fare l'amministratore"
fi

# Per quale macchina e' questa immagine. Lo dice il nome della ISO, che e'
# l'unico posto dove l'edizione e' stata davvero decisa da qualcuno.
#
# ⚠️ QUESTO BLOCCO STAVA PIU' IN BASSO, e l'ha spostato qui il fatto che la
# decisione sulla tabella ACPI, qui sotto, ne ha bisogno.
case "$FINAL" in
  *Generic*|*generic*) EDIZIONE=generic ;;
  *BC250*|*bc250*)     EDIZIONE=bc250 ;;
  *)
    echo "FAIL-EDIZIONE" > "$ST"
    echo "==== FALLITA: dal nome $FINAL non capisco l'edizione ===="
    echo "     il nome deve contenere BC250 oppure Generic"
    exit 1
    ;;
esac

# Il nome della macchina nella live. Sull'edizione Generic diceva «BC-250» anche
# su un PC normale, perche' eggs clona questa scheda: si vedeva nel prompt del
# terminale e in rete. Sull'edizione BC-250 invece e' giusto e resta.
# Il nome definitivo lo chiede comunque l'installatore.
if [ "$EDIZIONE" = generic ] && [ -f "$HOSTF" ]; then
    cp -f "$HOSTF" "$HOSTBAK"
    VECCHIO_HOST=$(cat "$HOSTF")
    printf 'skillfishos\n' > "$HOSTF"
    # /etc/hosts nomina la macchina: se resta il vecchio nome, ogni comando che
    # risolve l'hostname aspetta il timeout del DNS prima di arrendersi.
    if [ -n "$VECCHIO_HOST" ] && grep -q "$VECCHIO_HOST" /etc/hosts 2>/dev/null; then
        cp -f /etc/hosts "$HOSTBAK.hosts"
        sed -i "s/\b$VECCHIO_HOST\b/skillfishos/g" /etc/hosts
    fi
    echo "nome: nell'immagine la macchina si chiamera' skillfishos (era $VECCHIO_HOST)"
fi

# L'edizione Generic non deve imbarcare la tabella ACPI della BC-250. Quella per
# la BC-250 invece se la tiene: li' e' proprio il motivo per cui esiste.
#
# ⚠️ SI GUARDA L'EDIZIONE, NON IL NOME DEL KERNEL. Prima c'era
#     case "$KVER" in *generic*)
# e ha smesso di funzionare il giorno in cui il kernel per i PC normali si e'
# chiamato -x64 invece di -generic: quella riga cadeva nel ramo «BC-250» e la
# tabella ACPI della scheda sarebbe finita dentro un'immagine per PC normali,
# senza un errore e senza un avviso. Dedurre l'edizione da come si chiama il
# kernel era comodo finche' i due nomi combaciavano.
if [ "$EDIZIONE" = generic ]; then
    if [ -f /boot/SkillFishOS-acpi.cpio ] || grep -q '^GRUB_EARLY_INITRD_LINUX_CUSTOM=' /etc/default/grub 2>/dev/null; then
        touch "$ACPIMARK"
        /usr/local/bin/skillfish-acpi-pstates disable >/dev/null 2>&1
        echo "ACPI: tabella della BC-250 tolta per la durata della build Generic"
    fi
else
    echo "ACPI: edizione BC-250, la tabella resta"
fi

# --- correzione di GRUB prima di ogni produce (issue #12 e #20) --------------
# eggs rigenera /etc/calamares dai propri modelli a OGNI produce, quindi la
# correzione (secondo grub-install piu' update-grub dopo il modulo bootloader,
# e riparazione degli extent del kernel scritto da unpackfs) va riapplicata
# ogni volta, non solo la prima. Un aggiornamento del pacchetto penguins-eggs
# puo' perfino sovrascrivere i modelli stessi: e' gia' successo a show.qml e a
# customize-partitions.js.
#
# Prima questo passaggio andava ricordato a mano. Se qualcuno se lo dimentica,
# la ISO esce con GRUB rotto e nessuno se ne accorge finche' non prova a
# installarla: meglio fermare la build. Segnalato da Cyryl Sochacki (cyryllo)
# nella PR #26.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# La versione mostrata dall'installatore. Lo script esisteva da mesi ma NON
# LO CHIAMAVA NESSUNO: era stato lanciato a mano una volta e poi dimenticato,
# cosi' il numero e' rimasto fermo al rilascio di allora. La 26.06.5 del
# 19/08/2026 presentava l'installatore come "SkillFishOS 26.06.4 Aetherium".
# Il numero si ricava dal nome del file .iso, che e' l'unico posto dove lo
# scriviamo gia'.
# ⚠️ Niente sed qui: la riga di prima era
#      sed -n "s/^SkillFishOS-\([0-9.]*\)-.*//p"
#    cioe' con la sostituzione VUOTA, perche' il \1 se l'erano mangiato le
#    virgolette doppie quando e' stata scritta. Restituiva sempre stringa
#    vuota, scattava il ripiego, e ogni ISO ha continuato a presentare
#    l'installatore come "26.06": la correzione non ha mai corretto niente.
#    Due tagli di shell fanno lo stesso lavoro e non hanno niente da
#    proteggere: via il prefisso, poi via tutto dal primo trattino.
VERSIONE_ISO="${FINAL#SkillFishOS-}"
VERSIONE_ISO="${VERSIONE_ISO%%-*}"
python3 "$SCRIPT_DIR/fix-eggs-calamares-version.py" "${VERSIONE_ISO:-26.06}"

# La versione dichiarata dal sistema, che finisce in neofetch, nell'HUD e in
# ogni segnalazione di errore.
# ⚠️ Prima nessuno la toccava: veniva clonata dalla scheda, quindi la ISO
# diceva il numero dell'ULTIMA immagine costruita, non il proprio. La 26.06.5
# di stanotte si presentava come 26.06.6. Ora la decide il nome del file, come
# per l'installatore, e i due numeri non possono piu' divergere.
# ⚠️ I file sono DUE per via del dpkg-divert su /usr/lib/os-release: scriverne
# uno solo lascia due risposte diverse alla stessa domanda.
for OSREL in /usr/lib/os-release /etc/os-release; do
    [ -f "$OSREL" ] || continue
    sed -i \
        -e "s|^PRETTY_NAME=.*|PRETTY_NAME=\"SkillFishOS ${VERSIONE_ISO} (Aetherium)\"|" \
        -e "s|^VERSION=.*|VERSION=\"${VERSIONE_ISO} (Aetherium)\"|" \
        -e "s|^VERSION_ID=.*|VERSION_ID=\"${VERSIONE_ISO}\"|" \
        "$OSREL"
done
LETTO=$(sed -n 's/^VERSION_ID="\(.*\)"/\1/p' /etc/os-release | head -1)
if [ "$LETTO" = "$VERSIONE_ISO" ]; then
    echo "OK  : os-release dichiara $LETTO"
else
    echo "FAIL: os-release dice «$LETTO» invece di «$VERSIONE_ISO»"
    echo "FAIL-OSRELEASE" > "$ST"
    exit 1
fi

python3 "$SCRIPT_DIR/fix-eggs-calamares-boot.py"
# Il menu di avvio: titolo in inglese, e Safe/Text Mode che fanno davvero
# qualcosa invece di essere copie della voce normale. Sta qui perche' i file
# appartengono al pacchetto penguins-eggs e un suo aggiornamento li riscrive.
# Per quale macchina e' questa immagine. Le due edizioni si chiamavano tutte
# e due "SkillFishOS Live/Installation": chi scaricava la BC-250 e la metteva
# in un PC normale vedeva il menu e poi lo schermo nero, senza mai leggere da
# nessuna parte che quel kernel e' fatto per quella scheda e non parte
# altrove (issue #53). Il menu e' l'ultimo posto in cui glielo si puo' dire.
python3 "$SCRIPT_DIR/fix-eggs-menu-avvio.py" "$EDIZIONE"
RC=$?
echo "fix GRUB rc=$RC"
if [ $RC -ne 0 ]; then
    echo "FAIL-BOOTFIX rc=$RC" > "$ST"
    echo "==== FALLITA (la correzione di GRUB non regge) ===="
    exit 1
fi

# --- firmware: la Generic va sui portatili, e li' serve ----------------------
# ⚠️ TROVATO IL 23/08/2026 APRENDO L'IMMAGINE PUBBLICATA, non leggendo una
# lista. Nella 26.06.5 Generic i pacchetti di firmware erano DUE:
# firmware-amd-graphics e firmware-realtek. Niente iwlwifi, niente atheros,
# niente brcm80211, niente mediatek. Su un portatile recente il Wi-Fi e' quasi
# sempre Intel: senza firmware-iwlwifi la scheda non compare proprio, e a
# schermo non c'e' niente che dica che manca un file. Sembra la rete rotta
# invece che assente. Jim l'aveva segnalato il 25/06/2026 e gli avevamo
# risposto "e' uscita una versione nuova".
#
# ⚠️ NON CERCARE LA RISPOSTA IN iso/config/package-lists: quello e' l'albero di
# live-build, che con --firmware-chroot true si tira dentro 34 pacchetti di
# firmware. Le immagini pubblicate pero' le fa eggs CLONANDO QUESTA SCHEDA,
# quindi conta solo cosa e' installato qui. I due alberi raccontano cose
# diverse, e la prima volta ho creduto all'albero sbagliato.
#
# Le due edizioni escono dallo stesso clone, quindi la differenza si fa qui:
# per la Generic si installano, per la BC-250 si tolgono. Idempotente nei due
# versi, cosi' non conta in che ordine si costruiscono le due immagini.
#
# ⚠️ firmware-realtek e firmware-amd-graphics NON si toccano: il primo serve
# alla rete cablata di questa scheda, il secondo alla sua GPU.
#
# Quanto pesano, misurati il 23/08/2026 con la stessa compressione che usa
# eggs (xz, filtro BCJ x86, blocchi da 1 MB): 679 MB sul disco, 293 MB dentro
# la ISO. Il grosso e' nvidia-graphics (102 MB), iwlwifi (63), atheros (42) e
# mediatek (35). Comprimendoli tutti insieme si guadagna mezzo MB rispetto alla
# somma dei singoli: non c'e' nessuno sconto nascosto da sperare.
#
# firmware-nvidia-graphics da solo vale un terzo del totale, ed era rimasto
# fuori per quello. Ci entra perche' i portatili a grafica ibrida sono
# esattamente il caso da cui e' partita questa correzione, e su una NVIDIA
# recente senza quel firmware nouveau non accende lo schermo.
#
# ⚠️ Se un giorno la ISO diventa troppo grossa, questo e' il primo posto dove
# guardare, ma si tolga sapendo cosa si perde, non a caso.
FW_PORTATILI="firmware-iwlwifi firmware-atheros firmware-brcm80211 firmware-mediatek firmware-ti-connectivity firmware-libertas firmware-misc-nonfree firmware-intel-misc firmware-intel-sound firmware-sof-signed firmware-intel-graphics firmware-nvidia-graphics"
if [ "$EDIZIONE" = "generic" ]; then
    echo "firmware: installo quelli dei portatili (Wi-Fi, Bluetooth, audio, grafica Intel)"
    if ! DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends $FW_PORTATILI; then
        # Non si va avanti: un'immagine Generic senza firmware Wi-Fi e'
        # esattamente il difetto che stiamo chiudendo, e chi la scarica non
        # ha modo di capire perche' la rete non c'e'.
        echo "FAIL-FIRMWARE" > "$ST"
        echo "==== FALLITA: i firmware non si sono installati ===="
        echo "     serve rete su questa scheda al momento della build"
        exit 1
    fi
else
    echo "firmware: edizione BC-250, tolgo quelli dei portatili se ci sono"
    DA_TOGLIERE=""
    for f in $FW_PORTATILI; do
        if dpkg-query -W -f='${Status}' "$f" 2>/dev/null | grep -q "^install ok installed$"; then
            DA_TOGLIERE="$DA_TOGLIERE $f"
        fi
    done
    if [ -n "$DA_TOGLIERE" ]; then
        # Se non se ne vanno non e' un disastro: l'immagine BC-250 esce piu'
        # grossa di 191 MB, non rotta. Quindi si avvisa e si prosegue.
        DEBIAN_FRONTEND=noninteractive apt-get purge -y $DA_TOGLIERE \
            || echo "ATTENZIONE: non tolti, l'immagine BC-250 sara' piu' pesante"
    else
        echo "   non ce n'erano"
    fi
fi

rm -f /home/eggs/mnt/*.iso 2>/dev/null

# --- l'identita' della macchina di build resta fuori dall'immagine -----------
# eggs clona questa scheda, e con lei si porterebbe dietro la chiave privata
# della dashboard, il suo certificato e il segreto delle sessioni: ogni
# installazione fatta da quella ISO avrebbe gli STESSI. E' lo stesso problema
# delle chiavi host di ssh, che escludiamo da sempre; a questi non ci aveva
# pensato nessuno, e sono dentro anche alle ISO 26.06.x gia' pubblicate.
#
# Piu' i due segnaposto, che sono bugie: dicono a ogni macchina che installa
# l'immagine che un lavoro e' gia' stato fatto quando non e' vero.
# core-unlock.abilitato in particolare ACCENDE lo sblocco degli 8 core, cioe'
# la issue #31 ripresa dalla parte opposta.
#
# ⚠️ Non si usa una regola di exclude.list perche' su un FILE singolo non
# morde: le regole di eggs funzionano solo se finiscono con /*. La prova e'
# che .snapshots-setup-done era escluso da mesi ed era comunque nell'immagine.
# Qui si sposta e si rimette: deterministico, e il trap lo garantisce anche se
# la costruzione fallisce a meta'.
DAPARTE=/root/.identita-macchina

# Cartelle che non devono uscire di casa, per due motivi diversi.
#
# Licenza: bc250-cu-ref deriva da un progetto senza licenza e qui non si perde
# niente a toglierlo, perche' skillfish-cu e' nostro e lavora con umr.
#
# ⚠️ bc250_memcfg NON e' in questa lista, ed e' una scelta consapevole. Non ha
# licenza - gliela abbiamo chiesta e aspettiamo risposta - ma e' l'unico modo
# che c'e' oggi per cambiare lo split della RAM, cioe' per dare memoria all'AI.
# skillfish-memcfg, che avevamo scritto per sostituirlo, SCRIVE il blocco CMOS
# correttamente ma il firmware lo rimette identico al riavvio (misurato il
# 15/08): quel blocco e' dove il firmware SCRIVE, non da dove legge. Togliere
# una funzione che funziona per rimpiazzarla con una che non funziona sarebbe
# una regressione con una buona motivazione. La via d'uscita e' scrivere
# qualcosa di nostro che funzioni davvero, non togliere e basta.
#
# Ambiente di sviluppo: aider-venv, dockge, realesrgan sono roba della scheda,
# non prodotto.
#
# ⚠️ Perche' non bastano le regole di esclusione: mksquashfs riceve un solo
# file (-ef /etc/penguins-eggs.d/exclude.list) e eggs quel file lo rigenera dal
# proprio modello a ogni produce; exclude.list.d/ non viene concatenata, e'
# solo la cartella da cui eggs copia i modelli all'installazione. Provato: con
# le regole scritte in entrambi i posti, nella ISO /opt/bc250_memcfg aveva
# ancora 48 file dentro.
FUORI_IMMAGINE="
/opt/bc250-cu-ref
/opt/aider-venv
/opt/dockge
/opt/realesrgan
"

IDENTITA="
/etc/skillfish/core-unlock.abilitato
/etc/skillfish/dashboard-key.pem
/etc/skillfish/dashboard-cert.pem
/etc/skillfish/dashboard.secret
/etc/skillfish/dashboard.json.pre-key
/var/lib/skillfish/.snapshots-setup-done
"


# --- i kernel che non appartengono a QUESTA edizione ------------------------
# ⚠️ VERIFICATO APRENDO LE ISO: l'edizione Generic si e' sempre portata dentro
# anche il kernel della BC-250, 26.06.4 pubblicata compresa. La live avvia
# quello giusto, ma il sistema INSTALLATO se li ritrova tutti e due in /boot e
# GRUB li elenca entrambi. Il kernel della scheda e' compilato -march=znver2:
# su un Intel quella voce di menu puo' non partire affatto. Un kernel che a
# volte si avvia e' peggio di uno che non c'e'.
#
# ⚠️ SI SPOSTA SOLO /boot, NON /lib/modules. I moduli del kernel IN ESECUZIONE
# servono mentre la build gira: portarli via vorrebbe dire rompere la macchina a
# meta' produzione. Senza vmlinuz e initrd in /boot, pero', GRUB del sistema
# installato non ha nulla da elencare, che e' la parte pericolosa. I moduli
# rimasti sono spazio sprecato, non un rischio, e si vedono nel controllo finale.
ALTRI_KERNEL=/root/.kernel-da-parte

# --- l'officina non si spedisce ---------------------------------------------
# ⚠️ TROVATO IL 01/09/2026 CONFRONTANDO DUE IMMAGINI. La 26.06.4 pesava 4,8 GB e
# la 26.06.5 ne pesava 6,0. Aperte tutte e due e confrontate file per file, i
# 7,65 GB di differenza da scompattati non erano funzionalita' nuove: era la
# NOSTRA officina, clonata dentro l'immagine pubblica.
#
#   mingw-w64 e libwine     dall'esperimento FSR4, chiuso il 22/08      1,3 GB
#   llvm/clang di sviluppo  dalla Mesa nostra, che avevamo scartato     0,7 GB
#   rustc, cargo, rustlib   da quando abbiamo compilato scx_lavd        0,2 GB
#   valgrind, intestazioni di quattro kernel, /opt/bc250-fsr4           0,4 GB
#   qBittorrent             21 MB di app che si tirava dietro 1,06 GB
#                           di runtime KDE, usato solo da lei
#
# Ce ne siamo accorti DOPO, a immagine fatta, e non era la prima volta. Adesso
# la build si ferma PRIMA di produrre e dice cosa c'e' di troppo: la pulizia e'
# una decisione da prendere qui, non un giro di rifiniture dopo.
#
# ⚠️ Gli elenchi si allungano, non si aggirano. Se una cosa va spedita davvero,
# la si mette in FLATPAK_SPEDITI; se serve solo a noi, si toglie dalla scheda.
# Il compilatore di sistema NON e' in questa lista: da quando il kernel della
# BC-250 si compila sulla scheda, gcc-16 e le intestazioni del kernel in corso
# devono restare.
PACCHETTI_VIETATI="mingw-w64 mingw-w64-common mingw-w64-tools gcc-mingw-w64-base binutils-mingw-w64-x86-64 binutils-mingw-w64-i686 libwine wine wine64 wine64-tools libwine-dev llvm-21-dev libclang-21-dev libclang-dev clang clang-21 rustc cargo libstd-rust-dev valgrind bindgen"
FLATPAK_SPEDITI="com.valvesoftware.Steam com.heroicgameslauncher.hgl io.github.ryubing.Ryujinx net.davidotek.pupgui2 org.onlyoffice.desktopeditors org.vinegarhq.Sober"

officina_pulita() {
    _guai=0
    for _p in $PACCHETTI_VIETATI; do
        if dpkg -l "$_p" 2>/dev/null | grep -q "^ii  $_p "; then
            _kb=$(dpkg-query -Wf '${Installed-Size}' "$_p" 2>/dev/null)
            echo "OFFICINA: «$_p» e' installato e finirebbe nell'immagine (${_kb:-?} KB)"
            _guai=1
        fi
    done
    for _a in $(flatpak list --app --columns=application 2>/dev/null); do
        case " $FLATPAK_SPEDITI " in
            *" $_a "*) ;;
            *) echo "OFFICINA: il flatpak «$_a» non e' fra quelli che spediamo"; _guai=1 ;;
        esac
    done
    if [ "$_guai" = 1 ]; then
        echo "FAIL-OFFICINA" > "$ST"
        echo "==== FALLITA: c'e' roba nostra che finirebbe nell'immagine ===="
        echo "     Toglila dalla scheda, oppure aggiungila all'elenco se va spedita."
        exit 1
    fi
    echo "officina: niente di nostro finirebbe nell'immagine"
}


kernel_estranei() {
    mkdir -p "$ALTRI_KERNEL/boot" "$ALTRI_KERNEL/modules" "$ALTRI_KERNEL/src"
    local f base
    for f in /boot/vmlinuz-* /boot/initrd.img-* /boot/System.map-* /boot/config-*; do
        [ -e "$f" ] || continue
        case "$f" in *"$KVER") continue ;; esac
        base=$(basename "$f")
        mv -f "$f" "$ALTRI_KERNEL/boot/$base" && echo "   messo da parte $base (non e' di questa edizione)"
    done
    # ⚠️ E I MODULI, che fino al 01/09/2026 restavano. In /boot il kernel era
    # uno solo e i controlli passavano, ma usr/lib/modules li conteneva tutti:
    # ogni immagine si portava dietro 194 MB di moduli dell'altra edizione.
    for f in /usr/lib/modules/*; do
        [ -d "$f" ] || continue
        base=$(basename "$f")
        [ "$base" = "$KVER" ] && continue
        mv -f "$f" "$ALTRI_KERNEL/modules/$base" && echo "   messi da parte i moduli di $base"
    done
    for f in /usr/src/linux-headers-*; do
        [ -e "$f" ] || continue
        base=$(basename "$f")
        case "$base" in *"$KVER") continue ;; esac
        mv -f "$f" "$ALTRI_KERNEL/src/$base" && echo "   messe da parte le intestazioni di $base"
    done
}

# --- il compilatore non si spedisce -----------------------------------------
# Serve alla scheda per compilare i kernel della BC-250, e a nessun altro:
# dentro all'immagine sono 800 MB che non apre nessuno. Si sposta per la durata
# del produce. Niente di quello che gira nel frattempo compila.
OFFICINA_DAPARTE=/root/.officina-da-parte
OFFICINA_CARTELLE="/usr/libexec/gcc /usr/lib/gcc"

officina_fuori() {
    mkdir -p "$OFFICINA_DAPARTE"
    local d base
    for d in $OFFICINA_CARTELLE; do
        [ -d "$d" ] || continue
        base=$(printf '%s' "$d" | tr / _)
        mv -f "$d" "$OFFICINA_DAPARTE/$base" \
            && echo "   messo da parte $d ($(du -sh "$OFFICINA_DAPARTE/$base" 2>/dev/null | cut -f1))"
    done
    apt-get clean >/dev/null 2>&1 && echo "   svuotata la cache dei pacchetti"
}

rimetti_officina() {
    [ -d "$OFFICINA_DAPARTE" ] || return 0
    local f d
    for f in "$OFFICINA_DAPARTE"/*; do
        [ -e "$f" ] || continue
        d=$(basename "$f" | tr _ /)
        mkdir -p "$(dirname "$d")"
        mv -f "$f" "$d" && echo "   rimesso $d"
    done
    rmdir "$OFFICINA_DAPARTE" 2>/dev/null
}
rimetti_kernel_estranei() {
    [ -d "$ALTRI_KERNEL" ] || return 0
    local f
    for f in "$ALTRI_KERNEL"/boot/*; do
        [ -e "$f" ] || continue
        mv -f "$f" /boot/ && echo "   rimesso $(basename "$f")"
    done
    for f in "$ALTRI_KERNEL"/modules/*; do
        [ -e "$f" ] || continue
        mv -f "$f" /usr/lib/modules/ && echo "   rimessi i moduli di $(basename "$f")"
    done
    for f in "$ALTRI_KERNEL"/src/*; do
        [ -e "$f" ] || continue
        mv -f "$f" /usr/src/ && echo "   rimesse le intestazioni $(basename "$f")"
    done
    rmdir "$ALTRI_KERNEL"/boot "$ALTRI_KERNEL"/modules "$ALTRI_KERNEL"/src "$ALTRI_KERNEL" 2>/dev/null
}

rimetti_identita() {
    # ⚠️ PRIMA l'igiene: e' quella che tiene da parte l'identita' ZeroTier, le
    # chiavi Bluetooth, la chiave di firma DKMS e l'hash di root di Mattia. Se
    # il produce muore a meta' e questa non gira, la scheda resta monca.
    # ⚠️ Si prende lo script DA DOVE C'E'. /root/sfx-src e' nella lista di cio'
    # che l'igiene mette da parte, quindi applicandola lo script sposta via la
    # cartella che contiene lo script stesso: chiamarlo dal percorso di prima
    # dava "No such file or directory" e il ripristino non partiva. Il 19/08/2026
    # la scheda e' rimasta senza identita' ZeroTier, con root bloccato, col
    # profilo di overclock di sicurezza al posto di quello di Mattia e senza le
    # cartelle condivise dei flatpak. Ora l'igiene si deposita una copia di se'
    # stessa, e qui si usa quella se l'originale non c'e' piu'.
    IGIENE="$SCRIPT_DIR/igienizza-immagine.sh"
    [ -x "$IGIENE" ] || IGIENE=/root/.igiene-immagine/igienizza-immagine.sh
    if [ -x "$IGIENE" ]; then
        bash "$IGIENE" ripristina 2>&1 | sed 's/^/   /'
    else
        echo "   ATTENZIONE: non trovo l'igienizzatore, la scheda resta IGIENIZZATA"
    fi
    # ⚠️ Queste righe stavano DENTRO il ramo else, cioe' correvano solo
    # quando l'igienizzatore non si trovava: sul percorso normale non sono
    # mai state eseguite, e la scheda e' rimasta due volte col profilo di
    # sicurezza. Vanno fuori dall'if, sempre.
    # ⚠️ DOPO l'igiene, non prima. L'igiene rimette /etc/bc250-smu-oc.conf
    # com'era quando ha applicato, cioe' col profilo di SICUREZZA che questo
    # script aveva appena scritto. Affidarsi alla sola trap EXIT non basta:
    # il 19/08/2026 la scheda e' rimasta a 3500/0 invece di 3700/-16 e me ne
    # sono accorto solo controllando a mano.
    rimetti_kernel_estranei
    rimetti_officina
    restore_build_env  # esplicito, dopo l'igiene
    # Il rilevatore di snapshot era stato sospeso PRIMA di produrre, perche'
    # l'immagine lo eredita spento. Sulla scheda va riacceso, se no il menu
    # degli snapshot sparisce a chi ci lavora tutti i giorni.
    [ -x /usr/local/bin/skillfish-grub-btrfs ] && \
        /usr/local/bin/skillfish-grub-btrfs riaccendi >/dev/null 2>&1 || true
    for f in $IDENTITA $FUORI_IMMAGINE; do
        [ -e "$DAPARTE/$(basename "$f")" ] || continue
        mkdir -p "$(dirname "$f")"
        mv -f "$DAPARTE/$(basename "$f")" "$f"
    done
    rmdir "$DAPARTE" 2>/dev/null || true
}
trap rimetti_identita EXIT INT TERM

mkdir -p "$DAPARTE"
tolti=0
for f in $IDENTITA $FUORI_IMMAGINE; do
    [ -e "$f" ] || continue
    mv -f "$f" "$DAPARTE/$(basename "$f")"
    tolti=$((tolti + 1))
done
echo "messi da parte prima del produce: $tolti fra file e cartelle"
echo "   (identita' della macchina, codice di terzi senza licenza, ambiente di sviluppo)"

# --- i nostri backup non viaggiano ------------------------------------------
# I nostri script salvano una copia prima di riscrivere un file di sistema
# (.skfbak). Sulla scheda di sviluppo servono; dentro l'immagine no. E uno di
# loro e' peggio che inutile: skillfish-core-unlock.service.skfbak conserva la
# unit PRIMA delle guardie, cioe' quella che riavviava la scheda durante
# l'installazione. Il vecchio file difettoso accanto a quello corretto e' il
# modo migliore per far perdere mezza giornata a chi ci mettera' le mani.
# Sono tutte copie di file che stanno in git: cancellarle non perde niente.
# --- igiene: fuori tutto quello che appartiene a QUESTA macchina ------------
# I .skfbak li gestisce ora igienizza-immagine.sh insieme a tutto il resto, e li
# SPOSTA invece di cancellarli: non si perde niente e la scheda torna com'era.
#
# Cosa copre, e perche' e' nata (16/08/2026, aprendo le immagini gia' fatte):
#   identita' privata ZeroTier   chi installava diventava un nodo della rete
#                                privata di Mattia, con la sua chiave
#   chiave API Unsloth           dentro dashboard.json, vera, pubblicata
#   chiave di firma DKMS         uguale per tutti: firma moduli che il Secure
#                                Boot di chiunque accetta
#   chiavi Bluetooth             accoppiamenti e MAC dei suoi dispositivi
#   hash password di root        della scheda di sviluppo
#   800 MB di journal            i registri della sua macchina
# Gli stessi file sono anche nella 26.06.3 pubblicata: non e' una regressione,
# e' che non aveva mai guardato nessuno.
bash "$SCRIPT_DIR/igienizza-immagine.sh" applica 2>&1 | sed 's/^/   /'

# controprova prima di comprimere: se un segreto e' ancora li', non si produce
resti=0
for s in /var/lib/zerotier-one/identity.secret /var/lib/dkms/mok.key \
         /var/lib/bluetooth /var/log/journal; do
    [ -e "$s" ] && { echo "IGIENE FALLITA: $s e' ancora al suo posto"; resti=1; }
done
grep -q '^root:[^!*]' /etc/shadow && { echo "IGIENE FALLITA: root ha ancora una password"; resti=1; }
grep -q 'unsloth_api_key": ""' /etc/skillfish/dashboard.json 2>/dev/null || {
    echo "IGIENE FALLITA: dashboard.json ha ancora una chiave API"; resti=1; }
if [ "$resti" = 1 ]; then
    echo "FAIL-IGIENE" > "$ST"
    echo "==== FALLITA: non produco un'immagine con dentro roba della scheda ===="
    exit 1
fi
echo "igiene: controprova superata, nessun segreto della scheda nell'immagine"

officina_pulita
kernel_estranei
officina_fuori
eggs produce -n -N -m -K "$KVER" --basename="$BASE"
RC=$?
echo "produce rc=$RC"
[ $RC -ne 0 ] && { echo "FAIL rc=$RC" > "$ST"; echo "==== FALLITA ===="; exit 1; }

ISO=$(ls -t /home/eggs/mnt/*.iso 2>/dev/null | head -1)
[ -f "$ISO" ] || { echo "FAIL-NOISO" > "$ST"; exit 1; }
mv -f "$ISO" "$OUT/$FINAL"
( cd "$OUT" && sha256sum "$FINAL" > "$FINAL.sha256" )
SZ=$(du -h "$OUT/$FINAL" | cut -f1)

# --- verifica di quello che e' finito dentro -------------------------------
# Non fidarsi: la ISO si costruisce dal sistema vivo e basta una esclusione
# scritta male per perdere pezzi. Qui controlliamo le cose che sono gia'
# andate storte almeno una volta.
M=/mnt/verif-$BASE; mkdir -p "$M"; mount -o loop,ro "$OUT/$FINAL" "$M" 2>/dev/null
VK=$(ls "$M"/live/vmlinuz* 2>/dev/null; ls "$M"/boot/vmlinuz* 2>/dev/null)
SQ=$(find "$M" -name '*.squashfs' | head -1)
L=$(unsquashfs -l "$SQ" 2>/dev/null)
APPS=$(echo "$L" | grep -cE 'usr/local/bin/skillfish-(tuner|hub|monitor)$')
MENU=$(echo "$L" | grep -cE 'desktop-directories/skillfishos.directory|applications-merged/skillfishos.menu')
WALL=$(echo "$L" | grep -c 'usr/share/wallpapers/SkillFishOS/metadata.json')
ROOTH=$(echo "$L" | grep -cE '^squashfs-root/root/.')
DUMPS=$(echo "$L" | grep -c 'var/lib/systemd/coredump/core')
COMP=$(unsquashfs -s "$SQ" 2>/dev/null | grep -i '^Compression' | awk '{print $2}')
unsquashfs -n -d /tmp/ocheck-$$ -f "$SQ" etc/bc250-smu-oc.conf >/dev/null 2>&1
OCFREQ=$(grep -h 'frequency' /tmp/ocheck-$$/etc/bc250-smu-oc.conf 2>/dev/null | tr -d ' ')
rm -rf /tmp/ocheck-$$
umount "$M" 2>/dev/null; rmdir "$M" 2>/dev/null

echo "size=$SZ  compressione=$COMP  kernel=[$VK]"
echo "app=$APPS  menu=$MENU  wallpaper=$WALL  file-in-root=$ROOTH  coredump=$DUMPS"
echo "overclock spedito: $OCFREQ"
case "$OCFREQ" in
    *3500*) ;;
    *) echo "ATTENZIONE: l'immagine NON ha il profilo di sicurezza 3500 ma [$OCFREQ]" ;;
esac
[ "$WALL" -lt 1 ]  && echo "ATTENZIONE: manca il pacchetto wallpaper"
[ "$ROOTH" -gt 0 ] && echo "ATTENZIONE: dentro /root ci sono $ROOTH file, non dovrebbe essercene nessuno"
[ "$DUMPS" -gt 0 ] && echo "ATTENZIONE: ci sono $DUMPS core dump nell'immagine"

echo "DONE size=$SZ comp=$COMP apps=$APPS menu=$MENU wall=$WALL" > "$ST"
echo "==== BUILD $BASE finita: $(date) ===="
} >> "$LOG" 2>&1

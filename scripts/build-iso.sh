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

restore_build_env() {
    if [ -f "$OCBAK" ]; then
        mv -f "$OCBAK" "$OCF"
        echo "profilo overclock dell'utente ripristinato: $(grep -h frequency "$OCF" 2>/dev/null | tr -d ' ')"
    fi
    if [ -f "$LOCBAK" ]; then
        mv -f "$LOCBAK" "$LOCF"
        echo "lingua della scheda ripristinata: $(grep -h '^LANG=' "$LOCF" 2>/dev/null)"
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
if [ -f "$LOCF" ]; then
    cp -f "$LOCF" "$LOCBAK"
    printf '#  File generated by update-locale\nLANG=en_US.UTF-8\n' > "$LOCF"
    echo "lingua: l'immagine partira' in inglese"
fi

# L'edizione Generic non deve imbarcare la tabella ACPI della BC-250. Quella per
# la BC-250 invece se la tiene: li' e' proprio il motivo per cui esiste.
case "$KVER" in
  *generic*)
    if [ -f /boot/SkillFishOS-acpi.cpio ] || grep -q '^GRUB_EARLY_INITRD_LINUX_CUSTOM=' /etc/default/grub 2>/dev/null; then
        touch "$ACPIMARK"
        /usr/local/bin/skillfish-acpi-pstates disable >/dev/null 2>&1
        echo "ACPI: tabella della BC-250 tolta per la durata della build Generic"
    fi
    ;;
  *)
    echo "ACPI: edizione BC-250, la tabella resta"
    ;;
esac

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

python3 "$SCRIPT_DIR/fix-eggs-calamares-boot.py"
# Il menu di avvio: titolo in inglese, e Safe/Text Mode che fanno davvero
# qualcosa invece di essere copie della voce normale. Sta qui perche' i file
# appartengono al pacchetto penguins-eggs e un suo aggiornamento li riscrive.
# Per quale macchina e' questa immagine. Le due edizioni si chiamavano tutte
# e due "SkillFishOS Live/Installation": chi scaricava la BC-250 e la metteva
# in un PC normale vedeva il menu e poi lo schermo nero, senza mai leggere da
# nessuna parte che quel kernel e' fatto per quella scheda e non parte
# altrove (issue #53). Il menu e' l'ultimo posto in cui glielo si puo' dire.
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
python3 "$SCRIPT_DIR/fix-eggs-menu-avvio.py" "$EDIZIONE"
RC=$?
echo "fix GRUB rc=$RC"
if [ $RC -ne 0 ]; then
    echo "FAIL-BOOTFIX rc=$RC" > "$ST"
    echo "==== FALLITA (la correzione di GRUB non regge) ===="
    exit 1
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
kernel_estranei() {
    mkdir -p "$ALTRI_KERNEL"
    local f base
    for f in /boot/vmlinuz-* /boot/initrd.img-*; do
        [ -e "$f" ] || continue
        case "$f" in *"$KVER") continue ;; esac
        base=$(basename "$f")
        mv -f "$f" "$ALTRI_KERNEL/$base" && echo "   messo da parte $base (non e' di questa edizione)"
    done
}
rimetti_kernel_estranei() {
    [ -d "$ALTRI_KERNEL" ] || return 0
    local f
    for f in "$ALTRI_KERNEL"/*; do
        [ -e "$f" ] || continue
        mv -f "$f" /boot/ && echo "   rimesso $(basename "$f")"
    done
    rmdir "$ALTRI_KERNEL" 2>/dev/null
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

kernel_estranei
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

#!/bin/bash
# Toglie dalla ISO quello che non c'entra niente con SkillFishOS.
#
# PERCHE'
# La 26.06.3-rc2 pesa 10,19 GB contro i 6,66 GB della 26.06. Ho dato la colpa
# prima ai flatpak e poi a /root: sbagliato tutte e due le volte. La risposta e'
# arrivata solo montando le due immagini e confrontandone il contenuto:
#
#   +3,10 GB  /var/lib/systemd     <- la causa
#   +0,68 GB  /usr/libexec/gcc
#   +0,19 GB  /usr/lib/jvm
#   +0,15 GB  /var/lib/flatpak     <- non erano loro
#
# In /var/lib/systemd/coredump c'erano cinque core dump lasciati dai nostri test
# degli emulatori: 1,6 GB di Ryujinx, 826 e 767 MB di eden, piu' python3 e
# plasmashell. La configurazione predefinita di systemd li tiene fino al 10% del
# disco senza limite per singolo file, e siccome l'immagine si costruisce dal
# sistema vivo, quei gigabyte finiscono nella ISO di tutti.
#
# La cura vera e' il tetto in system/etc/systemd/coredump.conf.d/10-skillfish.conf,
# spedito da skillfish-base, che impedisce che si riaccumulino. Qui li togliamo
# dall'immagine e basta.
#
# LA CACHE DI APT, CHE EGGS CREDE DI ESCLUDERE E NON ESCLUDE
# Nella exclude.list predefinita di eggs c'e' questa riga:
#
#     var/cache/* var/lib/aide/*
#
# due pattern sulla stessa riga. mksquashfs legge il file una riga per pattern,
# quindi cerca un percorso che si chiama letteralmente "var/cache/* var/lib/aide/*"
# e non lo trova mai: /var/cache finisce intero nell'immagine, 601 MB di cui 509
# di cache di apt. Qui riscriviamo le voci che contano una per riga.
#
# Non escludiamo tutto /var/cache: swcatalog (47 MB) e' il catalogo di AppStream
# che riempie il negozio software. Toglierlo farebbe aprire un negozio vuoto a
# chi avvia la live senza rete, che e' un peggioramento visibile per risparmiare
# 47 MB.
#
# LE REGOLE SU /root SONO RIDONDANTI, E RESTANO APPOSTA
# eggs esclude gia' root/* e root/.* da solo, a meno che non gli si passi
# --includeRootHome, e noi lanciamo `eggs produce -n -N -K ... --basename=...`
# senza quel flag: verificato montando la ISO, dentro /root e' vuota. Le regole
# qui sotto non recuperano quindi nemmeno un byte. Le lascio come rete: se un
# giorno qualcuno aggiunge -i alla riga di comando per qualsiasi motivo, senza
# queste regole si ritroverebbe nell'immagine pubblica 5 GB di ambiente Unsloth,
# i pesi degli LLM, /root/.ssh, la cronologia della shell e una ventina di
# script di prova con dentro in chiaro le password della scheda, di SourceForge
# e di OVH. Costano niente e coprono un errore che sarebbe grave.
#
# COSA **NON** SI TOCCA
# /root/bc250_smu_oc, /root/bc250_memcfg e /root/bench NON vanno esclusi:
# skillfish-tuner-helper e skillfish-thermal-guard li cercano li' con il
# percorso scritto dentro. Oggi il Tuner funziona sui sistemi installati solo
# perche' /root finisce nella ISO - una dipendenza fragile che andra' sistemata
# spostando quei programmi in /opt e mettendoli in un pacchetto, ma e' un lavoro
# a parte: farlo qui significherebbe rischiare di rompere l'overclock per
# guadagnare 6 MB.
#
# Uso:  sudo bash slim-iso.sh          mostra e applica
#       sudo bash slim-iso.sh --dry    mostra soltanto
set -u

EXCL=/etc/penguins-eggs.d/exclude.list
DRY=0
[ "${1:-}" = "--dry" ] && DRY=1

MARK_A="# --- SkillFishOS: fuori dall'immagine (slim-iso.sh) ---"
MARK_B="# --- fine SkillFishOS ---"

# I percorsi sono relativi alla radice, come tutti gli altri in exclude.list.
read -r -d '' RULES <<'EOF'
var/lib/systemd/coredump/*
var/cache/apt/archives/*
var/cache/apt/apt-file/*
var/cache/apt/pkgcache.bin
var/cache/apt/srcpkgcache.bin
var/cache/cups/*
var/cache/man/*
var/cache/snapd/*
root/.unsloth/*
root/.unsloth
root/models/*
root/models
root/.npm/*
root/.bun/*
root/.local/share/uv/*
root/sfx-src/*
root/waydroid_script/*
root/skillfish-apt/*
root/cyan-skillfish-governor/*
root/*.sh
root/*.py
root/*.log
root/*.json
root/.attic/*
root/.ssh/*
root/.gnupg/*
root/.bash_history
root/.python_history
root/.wget-hsts
root/.lesshst
root/.viminfo
home/*/.ssh/*
home/*/.bash_history
home/*/.python_history
# --- Codice di terzi senza licenza: non puo' stare in un'immagine che
# --- distribuiamo. Al posto di bc250_memcfg c'e' skillfish-memcfg, nostro e
# --- GPL-3.0, dentro skillfish-base.
opt/bc250_memcfg/*
opt/bc250_memcfg
opt/bc250-cu-ref/*
opt/bc250-cu-ref
root/bc250_memcfg/*
root/bc250_memcfg
# --- Il mio ambiente di sviluppo sulla scheda: non e' prodotto.
opt/aider-venv/*
opt/aider-venv
opt/dockge/*
opt/dockge
opt/realesrgan/*
opt/realesrgan
EOF

echo "=== quello che togliamo DAVVERO dall'immagine ==="
tot=0
for p in /var/lib/systemd/coredump; do
    [ -e "$p" ] || continue
    kb=$(du -sx -k "$p" 2>/dev/null | cut -f1)
    tot=$((tot + kb))
    printf "   %-38s %8s\n" "$p" "$(du -sxh "$p" 2>/dev/null | cut -f1)"
done
printf "   recuperato:                            %s\n" \
    "$(awk -v k=$tot 'BEGIN{printf "%.2f GB", k/1048576}')"

echo
echo "=== e quello che eggs escludeva gia' da solo (regole di scorta) ==="
red=0
for p in /root/.unsloth /root/models /root/.npm /root/.bun \
         /root/sfx-src /root/waydroid_script /root/skillfish-apt /root/cyan-skillfish-governor; do
    [ -e "$p" ] || continue
    red=$((red + $(du -sx -k "$p" 2>/dev/null | cut -f1)))
    printf "   %-38s %8s\n" "$p" "$(du -sxh "$p" 2>/dev/null | cut -f1)"
done
n=$(ls -1 /root/*.sh 2>/dev/null | wc -l)
echo "   script di prova sotto /root:            $n file"
printf "   gia' fuori dall'immagine:              %s (nessun guadagno, e' una rete)\n" \
    "$(awk -v k=$red 'BEGIN{printf "%.1f GB", k/1048576}')"

echo
echo "=== metto al riparo gli script che contengono credenziali ==="
# Spostati, non cancellati: sono cose che potrebbero servire ancora, e .attic
# e' comunque escluso dall'immagine. Cancellare e' irreversibile, spostare no.
mkdir -p /root/.attic
moved=0
for f in /root/*.sh; do
    [ -f "$f" ] || continue
    if grep -qIE 'DioBestia|47yk2d8r6c|sshpass|github_pat_|ghp_[A-Za-z0-9]{20}' "$f" 2>/dev/null; then
        if [ "$DRY" = 1 ]; then
            echo "   [dry] $(basename "$f") -> /root/.attic/"
        else
            mv -f "$f" /root/.attic/ && echo "   $(basename "$f") -> /root/.attic/"
        fi
        moved=$((moved + 1))
    fi
done
[ "$moved" = 0 ] && echo "   nessuno (gia' fatto)"

echo
echo "=== aggiorno $EXCL ==="
if [ ! -f "$EXCL" ]; then
    echo "FATAL: manca $EXCL - eggs non e' installato?" >&2
    exit 1
fi
if [ "$DRY" = 1 ]; then
    echo "$RULES" | sed 's/^/   [dry] /'
else
    [ -f "$EXCL.pre-slim" ] || cp "$EXCL" "$EXCL.pre-slim"
    # blocco delimitato: rieseguire lo script non duplica le righe
    if grep -qF "$MARK_A" "$EXCL"; then
        sed -i "/$(printf '%s' "$MARK_A" | sed 's/[][\.*^$/]/\\&/g')/,/$(printf '%s' "$MARK_B" | sed 's/[][\.*^$/]/\\&/g')/d" "$EXCL"
    fi
    { echo "$MARK_A"; echo "$RULES"; echo "$MARK_B"; } >> "$EXCL"
    echo "   scritte $(echo "$RULES" | wc -l) regole (backup in $EXCL.pre-slim)"
fi

echo
echo "=== compressione dell'immagine ==="
# ATTENZIONE: la chiave `compression:` di eggs.yaml NON conta.
#
# Ci sono cascato: l'avevo impostata a "xz -Xbcj x86 -b 1M" e il comando che
# eggs ha davvero eseguito era `-comp zstd -b 1M -Xcompression-level 3`. La
# compressione la decide un FLAG di `eggs produce`, non il file di configurazione:
#
#   (nessun flag)   zstd -Xcompression-level 3      veloce e grosso
#   -S --standard   xz -b 1M
#   -p --pendrive   zstd -b 1M -Xcompression-level 15
#   -m --max        xz -Xbcj x86 -b 1M              <- quello che vogliamo
#
# Quindi la riga che conta e' in scripts/build-iso.sh: `eggs produce -n -N -m`.
# Il valore in eggs.yaml lo scriviamo lo stesso, per coerenza e per il caso in
# cui qualcuno lanci eggs a mano senza flag, ma non e' lui a decidere.
#
# La misura che ha portato a scegliere -m, fatta sulla scheda su un campione di
# 641 MB di binari (/usr/bin):
#
#   -comp xz                       190,0 MB   14 s   <- quello che facciamo ora
#   -comp xz -Xbcj x86             180,0 MB   28 s   -5,5%
#   -comp xz -Xbcj x86 -b 1M       166,0 MB   36 s   -13,0%
#   -comp zstd -Xcompression-level 19 -b 1M  190,0 MB  21 s   -0,2%
#
# Il filtro BCJ x86 riscrive gli indirizzi relativi delle istruzioni di salto
# in forma assoluta prima di comprimere: sul codice macchina i pattern
# diventano molto piu' ripetitivi. Il blocco da 1 MB da' a xz una finestra piu'
# grande su cui trovare ripetizioni. Insieme valgono il 13% sui binari, meno
# sul resto, ma sono gratis: il prezzo e' solo tempo di costruzione.
#
# zstd al massimo livello non serve: comprime come xz predefinito ma non come
# xz regolato. Va bene per chi vuole un boot piu' rapido, non per la dimensione.
Y=/etc/penguins-eggs.d/eggs.yaml
WANT='compression: xz -Xbcj x86 -b 1M'
if [ -f "$Y" ]; then
    if grep -qF "$WANT" "$Y"; then
        echo "   gia' impostata: $(grep '^compression:' "$Y")"
    elif [ "$DRY" = 1 ]; then
        echo "   [dry] $(grep '^compression:' "$Y")  ->  $WANT"
    else
        [ -f "$Y.pre-comp" ] || cp "$Y" "$Y.pre-comp"
        sed -i "s|^compression:.*|$WANT|" "$Y"
        echo "   impostata: $(grep '^compression:' "$Y")"
    fi
else
    echo "   ATTENZIONE: manca $Y"
fi

echo
echo "=== controllo che le cose che servono NON siano state escluse ==="
for keep in /root/bc250_smu_oc /root/bc250_memcfg /root/bench; do
    if [ -e "$keep" ]; then
        echo "   $keep resta nell'immagine (serve al Tuner)"
    else
        echo "   ATTENZIONE: $keep non esiste - il Tuner non troverebbe i suoi strumenti"
    fi
done

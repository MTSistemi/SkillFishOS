#!/bin/bash
# Toglie dalla ISO quello che non c'entra niente con SkillFishOS.
#
# PERCHE'
# La 26.06.3 pesa 9,5 GB contro i 6,3 GB della precedente. Cercando il motivo
# avevo dato la colpa ai flatpak: sbagliato. La causa vera e' che eggs copia
# nell'immagine anche **/root**, e nella /root della scheda di sviluppo ci sono
# 5,0 GB di /root/.unsloth (l'ambiente Python di Unsloth Studio) e 1,1 GB di
# /root/models (i pesi degli LLM con cui abbiamo fatto le prove). Roba nostra da
# banco di lavoro, spedita a tutti quelli che scaricano la ISO.
#
# E C'E' DI PEGGIO
# Sotto /root ci sono 146 script di prova, 18 dei quali contengono la password
# della scheda e quelle di SourceForge/OVH in chiaro. La ISO e' pubblica: quelle
# credenziali sarebbero finite su SourceForge dentro l'immagine. Insieme a
# /root/.ssh e a /root/.bash_history.
#
# Unsloth non serve nell'immagine: si installa a richiesta con
# scripts/install-unsloth.sh, che se lo scarica da unsloth.ai. I modelli li
# sceglie l'utente. Quindi qui non si perde nessuna funzione, si smette solo di
# spedire il nostro disco fisso.
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
EOF

echo "=== quanto pesa oggi quello che stiamo per escludere ==="
tot=0
for p in /root/.unsloth /root/models /root/.npm /root/.bun /root/sfx-src \
         /root/waydroid_script /root/skillfish-apt /root/cyan-skillfish-governor; do
    [ -e "$p" ] || continue
    kb=$(du -sx -k "$p" 2>/dev/null | cut -f1)
    tot=$((tot + kb))
    printf "   %-38s %8s\n" "$p" "$(du -sxh "$p" 2>/dev/null | cut -f1)"
done
n=$(ls -1 /root/*.sh 2>/dev/null | wc -l)
echo "   script di prova sotto /root:            $n file"
printf "   TOTALE recuperato dal sorgente:        %s\n" \
    "$(awk -v k=$tot 'BEGIN{printf "%.1f GB", k/1048576}')"

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
echo "=== controllo che le cose che servono NON siano state escluse ==="
for keep in /root/bc250_smu_oc /root/bc250_memcfg /root/bench; do
    if [ -e "$keep" ]; then
        echo "   $keep resta nell'immagine (serve al Tuner)"
    else
        echo "   ATTENZIONE: $keep non esiste - il Tuner non troverebbe i suoi strumenti"
    fi
done

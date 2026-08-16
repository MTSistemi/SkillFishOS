#!/bin/bash
# Toglie dalla scheda, per la sola durata della produzione dell'immagine, tutto
# cio' che appartiene a QUESTA macchina e non al prodotto. Poi lo rimette.
#
#   igienizza-immagine.sh applica      prima di `eggs produce`
#   igienizza-immagine.sh ripristina   dopo, sempre, anche se il produce fallisce
#   igienizza-immagine.sh controlla    dice cosa troverebbe, senza toccare niente
#
# PERCHE' ESISTE, e non e' un dettaglio di pulizia.
# Il 16/08/2026, aprendo le immagini gia' costruite, abbiamo trovato dentro:
#
#   /var/lib/zerotier-one/identity.secret   la chiave privata della rete
#                                           privata di Mattia, con il servizio
#                                           abilitato: chi installava diventava
#                                           un SUO nodo
#   /etc/skillfish/dashboard.json           la sua chiave API Unsloth vera, e il
#                                           pannello in ascolto su 0.0.0.0 come root
#   /var/lib/dkms/mok.key                   la chiave privata con cui si firmano
#                                           i moduli per Secure Boot, uguale per tutti
#   /var/lib/bluetooth/                     le chiavi di accoppiamento e i MAC dei
#                                           suoi dispositivi personali
#   /etc/shadow                             l'hash della password di root della
#                                           scheda di sviluppo
#
# Gli stessi file sono anche nella 26.06.3 gia' pubblicata. Non e' una svista
# recente: e' che nessuno aveva mai guardato. Il meccanismo che gia' proteggeva
# la chiave TLS della dashboard era giusto, era solo troppo corto.
#
# ⚠️ SI SPOSTA, NON SI CANCELLA. Questa e' la macchina di lavoro di Mattia:
# la sua identita' ZeroTier, i suoi accoppiamenti Bluetooth e la sua password
# devono tornare al loro posto appena finito. Il deposito e' fuori dall'immagine
# (/root e' escluso dallo squashfs) e il ripristino sta in una trap.
set -u
export LC_ALL=C

AZIONE="${1:-controlla}"
DEP=/root/.igiene-immagine
REG="$DEP/registro.txt"

# --- 1. roba che identifica QUESTA macchina --------------------------------
# Tutto qui dentro si rigenera da solo sulla macchina dell'utente al primo
# avvio: ZeroTier rifa' l'identita', dkms rifa' la coppia di firma, systemd
# rifa' il seed, NetworkManager rifa' la sua chiave.
IDENTITA_MACCHINA="
/var/lib/zerotier-one/identity.secret
/var/lib/zerotier-one/identity.public
/var/lib/zerotier-one/authtoken.secret
/var/lib/zerotier-one/metricstoken.secret
/var/lib/zerotier-one/peers.d
/var/lib/zerotier-one/controller.d
/var/lib/zerotier-one/networks.d
/var/lib/bluetooth
/var/lib/dkms/mok.key
/var/lib/dkms/mok.pub
/etc/ssl/private/ssl-cert-snakeoil.key
/etc/ssl/certs/ssl-cert-snakeoil.pem
/var/lib/systemd/random-seed
/var/lib/systemd/timers
/var/lib/systemd/credential.secret
/etc/NetworkManager/system-connections
/var/lib/NetworkManager
/etc/dhcpcd.duid
/etc/dhcpcd.secret
/var/lib/dhcpcd
/var/lib/fwupd
/var/lib/transmission-daemon
/var/lib/AccountsService/users
"

# --- 2. stato della scheda che nell'immagine e' sbagliato o morto -----------
# grub-btrfs.cfg elenca gli snapshot di QUESTA scheda, con il suo UUID: sul
# disco dell'utente sono undici voci di menu che non portano da nessuna parte.
STATO_SCHEDA="
/boot/grub/grub-btrfs.cfg
/boot/grub/grubenv
/var/lib/btrfs
/var/log/journal
/var/crash
"

# --- 3. banco di lavoro, non prodotto ---------------------------------------
# umr da solo pesa 215 MB e ha dentro il suo albero git.
BANCO_DI_LAVORO="
/opt/umr
/opt/bench
/opt/bc250-cu-ref
/opt/aider-venv
/opt/dockge
/opt/realesrgan
/usr/local/bin/opencode
"

# --- 3bis. servizi che sulla scheda hanno senso e nell'immagine no ---------
# Si spostano i COLLEGAMENTI di abilitazione, non le unit: sulla macchina di
# Mattia i servizi restano come li aveva, nell'immagine partono spenti.
#   waydroid-container   e' abilitato ma Waydroid non e' inizializzato: al primo
#                        avvio dell'utente finisce dritto in failed
#   snapper-timeline     il progetto dice a voce alta che la linea temporale e'
#                        spenta apposta, e poi la spediva accesa
#   lxc / lxcfs          infrastruttura di sviluppo: sta sul container .103,
#                        non ha niente da fare sulla macchina di chi installa
#   kscreenlockerrc      in /etc/skel toglie il blocco schermo a OGNI nuovo
#                        utente del sistema installato, non solo alla live
SERVIZI_DA_NON_SPEDIRE="
/etc/systemd/system/multi-user.target.wants/waydroid-container.service
/etc/systemd/system/timers.target.wants/snapper-timeline.timer
/etc/systemd/system/multi-user.target.wants/lxc.service
/etc/systemd/system/multi-user.target.wants/lxc-net.service
/etc/systemd/system/multi-user.target.wants/lxcfs.service
/etc/skel/.config/kscreenlockerrc
"

# --- 4. file che nell'immagine vanno SOSTITUITI, non tolti ------------------
# (l'originale torna al suo posto col ripristino)

deposita() { # <percorso assoluto>
    [ -e "$1" ] || [ -L "$1" ] || return 0
    local dest="$DEP/albero$1"
    mkdir -p "$(dirname "$dest")"
    mv -f "$1" "$dest" || return 1
    echo "$1" >> "$REG"
    return 0
}

rimetti_tutto() {
    [ -f "$REG" ] || { echo "   niente da rimettere"; return 0; }
    local n=0
    while IFS= read -r p; do
        [ -n "$p" ] || continue
        local src="$DEP/albero$p"
        if [ -e "$src" ] || [ -L "$src" ]; then
            mkdir -p "$(dirname "$p")"
            mv -f "$src" "$p" && n=$((n + 1))
        fi
    done < "$REG"
    rm -f "$REG"
    echo "   rimessi al loro posto: $n"
}

case "$AZIONE" in

applica)
    rm -rf "$DEP"; mkdir -p "$DEP"; : > "$REG"
    tolti=0; peso=0
    for f in $IDENTITA_MACCHINA $STATO_SCHEDA $BANCO_DI_LAVORO $SERVIZI_DA_NON_SPEDIRE; do
        if [ -e "$f" ] || [ -L "$f" ]; then
            k=$(du -s --apparent-size "$f" 2>/dev/null | cut -f1); k=${k:-0}
            deposita "$f" && { tolti=$((tolti + 1)); peso=$((peso + k)); }
        fi
    done
    echo "igiene: messi da parte $tolti fra file e cartelle ($((peso / 1024)) MB)"

    # --- i file di scarto: spostati anche loro, cosi' non si perde niente ---
    scarti=0
    while IFS= read -r f; do
        [ -n "$f" ] || continue
        deposita "$f" && scarti=$((scarti + 1))
    done < <(find /etc /usr/local /boot -xdev \
                  \( -name '*.bak' -o -name '*.skfbak' -o -name '*.orig' \
                     -o -name '*.dpkg-new' -o -name '*.dpkg-old' -o -name '*.dpkg-dist' \
                     -o -name '*.ucf-dist' -o -name '*.ucf-old' -o -name '*.pre-*' \
                     -o -name '*~' \) 2>/dev/null)
    echo "igiene: messi da parte $scarti file di scarto"

    # --- __pycache__ sotto /usr/local: si rigenera, si cancella e basta -----
    py=$(find /usr/local -type d -name '__pycache__' 2>/dev/null | wc -l)
    find /usr/local -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null
    echo "igiene: cancellate $py cartelle __pycache__ (si rigenerano)"

    # --- root: nell'immagine la password non deve esserci -------------------
    # Sulla scheda l'hash resta (viene rimesso dal ripristino). Nell'immagine
    # root risulta bloccato, come in ogni live Debian: si usa sudo, e chi
    # installa la password la sceglie in Calamares.
    if grep -q '^root:[^!*]' /etc/shadow; then
        cp -a /etc/shadow "$DEP/shadow.originale"
        sed -i 's|^root:[^:]*:|root:!:|' /etc/shadow
        echo "igiene: root bloccato nell'immagine (l'hash della scheda e' al sicuro nel deposito)"
    fi

    # --- la voce di avvio predefinita non puo' contenere l'UUID di questo disco
    # Con l'id assoluto della scheda, sul disco dell'utente GRUB non trova la
    # voce e ripiega sulla numero 0 - che per l'ordinamento di 10_linux e' il
    # kernel -generic anche nell'edizione BC250.
    if grep -q '^GRUB_DEFAULT="gnulinux' /etc/default/grub; then
        cp -a /etc/default/grub "$DEP/grub.originale"
        sed -i 's|^GRUB_DEFAULT=.*|GRUB_DEFAULT=0|' /etc/default/grub
        echo "igiene: GRUB_DEFAULT=0 (l'id con l'UUID della scheda e' nel deposito)"
    fi

    # --- deb-src: indici dei sorgenti di sid che nessun utente usa ----------
    if grep -q '^Types: deb deb-src' /etc/apt/sources.list.d/debian.sources 2>/dev/null; then
        cp -a /etc/apt/sources.list.d/debian.sources "$DEP/debian.sources.originale"
        sed -i 's/^Types: deb deb-src/Types: deb/' /etc/apt/sources.list.d/debian.sources
        echo "igiene: deb-src spento nell'immagine"
    fi

    # --- la configurazione della dashboard va spedita neutra ----------------
    if [ -f /etc/skillfish/dashboard.json ]; then
        cp -a /etc/skillfish/dashboard.json "$DEP/dashboard.json.originale"
        python3 - <<'PY'
import json
p = "/etc/skillfish/dashboard.json"
d = json.load(open(p))
# la chiave API e' di Mattia, l'ascolto su 0.0.0.0 come root non e' un
# predefinito difendibile, e l'utente e' quello della scheda di sviluppo.
d["unsloth_api_key"] = ""
d["bind"] = "127.0.0.1"
d.pop("user", None)
json.dump(d, open(p, "w"), indent=2)
PY
        echo "igiene: dashboard.json spedito senza chiave API e in ascolto su 127.0.0.1"
    fi
    ;;

ripristina)
    rimetti_tutto
    for coppia in "shadow.originale:/etc/shadow" \
                  "debian.sources.originale:/etc/apt/sources.list.d/debian.sources" \
                  "grub.originale:/etc/default/grub" \
                  "dashboard.json.originale:/etc/skillfish/dashboard.json"; do
        src="$DEP/${coppia%%:*}"; dst="${coppia##*:}"
        [ -f "$src" ] && { cp -a "$src" "$dst" && rm -f "$src" && echo "   rimesso $dst"; }
    done
    rmdir "$DEP/albero" 2>/dev/null
    ;;

controlla)
    echo "cosa verrebbe messo da parte (niente viene toccato):"
    for f in $IDENTITA_MACCHINA $STATO_SCHEDA $BANCO_DI_LAVORO $SERVIZI_DA_NON_SPEDIRE; do
        [ -e "$f" ] || [ -L "$f" ] && printf '   %-52s %s\n' "$f" \
            "$(du -sh --apparent-size "$f" 2>/dev/null | cut -f1)"
    done
    echo "   file di scarto: $(find /etc /usr/local /boot -xdev \( -name '*.bak' -o -name '*.skfbak' -o -name '*.orig' -o -name '*.dpkg-*' -o -name '*.ucf-*' -o -name '*.pre-*' -o -name '*~' \) 2>/dev/null | wc -l)"
    echo "   root ha una password: $(grep -q '^root:[^!*]' /etc/shadow && echo si || echo no)"
    echo "   GRUB_DEFAULT: $(grep '^GRUB_DEFAULT' /etc/default/grub)"
    ;;

*)
    echo "uso: $0 applica|ripristina|controlla" >&2
    exit 2
    ;;
esac

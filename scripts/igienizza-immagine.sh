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
#   ~/.config/autostart/x11vnc.desktop      avvia x11vnc SENZA PASSWORD su tutte
#                                           le interfacce al login. Sulla scheda
#                                           di sviluppo serve e resta; dentro
#                                           l'immagine sarebbe il desktop di
#                                           chiunque installi, aperto a chiunque
#                                           passi. Il VNC che l'utente deve avere
#                                           e' quello del Remote Manager: 5901,
#                                           solo localhost, con password.
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
/home/skillfish/.config/autostart/x11vnc.desktop
"

# --- 1bis. come si entra in QUESTA macchina --------------------------------
# ⚠️ Serve da quando la Generic si produce dalla macchina di sviluppo e non piu'
# clonando la BC-250. Quella macchina ha un utente con la password, l'accesso
# automatico e le chiavi con cui ci entriamo da remoto: se finiscono
# nell'immagine, ogni installazione nasce con la stessa porta aperta. E' lo
# stesso errore della 26.06.3, su file diversi.
#
# Le chiavi di HOST le toglie gia' eggs quando produce, e skillfish-sshd-keygen
# le rigenera al primo avvio: qui si aggiungono lo stesso, perche' un
# comportamento che dipende da un'altra squadra non e' una garanzia.
ACCESSO_DI_SVILUPPO="
/etc/ssh/ssh_host_rsa_key
/etc/ssh/ssh_host_rsa_key.pub
/etc/ssh/ssh_host_ecdsa_key
/etc/ssh/ssh_host_ecdsa_key.pub
/etc/ssh/ssh_host_ed25519_key
/etc/ssh/ssh_host_ed25519_key.pub
/etc/ssh/ssh_host_mldsa44_ed25519_key
/etc/ssh/ssh_host_mldsa44_ed25519_key.pub
/root/.ssh
/root/.bash_history
/root/.python_history
/root/.lesshst
# I core dump sono IMMAGINI DI MEMORIA dei processi caduti: dentro ci puo'
# essere qualunque cosa avessero in RAM, password digitate comprese. Sulla
# scheda erano 62 MB accumulati fra prove e sviluppo, e nessuno li toglieva.
/etc/sddm.conf.d/90-autologin-dev.conf
/var/lib/systemd/coredump
/etc/ssh/sshd_config.d/90-skillfish-dev-root.conf
"

# Le stesse cose dentro le cartelle personali, qualunque sia il nome dell'utente:
# sulla BC-250 era "skillfish", sulla macchina di sviluppo e' "skillfishdev", e
# domani potrebbe essere un altro. Si scoprono a runtime invece di elencarle.
# --- le cartelle personali dentro le impostazioni flatpak -------------------
# ⚠️ NON si sposta il file intero. In /var/lib/flatpak/overrides/ ci finiscono
# due cose diverse: le cartelle che Mattia ha condiviso con un'applicazione
# (/mnt/nas: roba sua, non va distribuita) e i rimedi che ci mettiamo NOI
# perche' certi flatpak partano - per esempio QT_XCB_GL_INTEGRATION=none, senza
# il quale ProtonUp-Qt aborta all'avvio sulla BC-250. Portando via il file si
# porterebbe via anche la correzione, e l'utente si ritroverebbe l'applicazione
# che non parte.
#
# Si toglie quindi SOLO la riga filesystems=, lasciando intatto [Environment].
igiene_flatpak() {
    local f
    for f in /var/lib/flatpak/overrides/* /home/*/.local/share/flatpak/overrides/*; do
        [ -f "$f" ] || continue
        grep -q '^filesystems=' "$f" 2>/dev/null || continue
        cp -a "$f" "$DEP/$(echo "$f" | tr / _)" 2>/dev/null
        sed -i '/^filesystems=/d' "$f"
        echo "   tolte le cartelle condivise da $(basename "$f")"
    done
}

casa_da_ripulire() {
    local u
    for u in /home/*; do
        [ -d "$u" ] || continue
        printf '%s\n' "$u/.ssh" "$u/.bash_history" "$u/.python_history" \
                       "$u/.lesshst" "$u/.local/share/krunnerstaterc"
    done
}

# --- 1ter. il banco di lavoro della macchina di sviluppo -------------------
# Il clone del repository con dentro l'albero di compilazione: centinaia di MB
# che all'utente non servono, e con dentro i nostri file di lavoro.
BANCO_DI_SVILUPPO="
/root/sfx-src
/root/k72
/root/debs-2608-26
/root/dist-debs
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
    # ⚠️ PRIMA DI TUTTO: una copia di QUESTO script nel deposito.
    #
    # COSA E' SUCCESSO IL 19/08/2026. /root/sfx-src e' in BANCO_DI_SVILUPPO,
    # quindi applicando l'igiene lo script sposta via la cartella che contiene
    # lo script stesso. build-iso.sh poi chiama `igienizza-immagine.sh ripristina`
    # dal percorso di prima e trova:
    #     bash: /root/sfx-src/scripts/igienizza-immagine.sh: No such file
    # Il ripristino non parte, e la scheda resta igienizzata: senza identita'
    # ZeroTier, con root bloccato, col profilo di overclock di sicurezza al posto
    # di quello dell'utente e senza le cartelle condivise dei flatpak.
    # Il deposito NON viene spostato da nessuno, quindi la copia li' dentro
    # sopravvive sempre a se' stessa.
    rm -rf "$DEP"; mkdir -p "$DEP"; : > "$REG"
    cp -f "$0" "$DEP/igienizza-immagine.sh" 2>/dev/null && chmod +x "$DEP/igienizza-immagine.sh"
    tolti=0; peso=0
    for f in $IDENTITA_MACCHINA $STATO_SCHEDA $BANCO_DI_LAVORO $ACCESSO_DI_SVILUPPO $BANCO_DI_SVILUPPO $(casa_da_ripulire) $SERVIZI_DA_NON_SPEDIRE; do
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

    # --- flatpak: via le cartelle personali, restano i nostri rimedi -------
    igiene_flatpak

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
# ⚠️ si SVUOTA, non si toglie: build-iso.sh controlla che il campo ci sia
# e sia vuoto. Con il pop il campo spariva, il controllo non lo trovava e
# la build falliva sempre dicendo che la chiave c'era ancora.
d["unsloth_api_key"] = ""
# ⚠️ NIENTE bind=127.0.0.1. Chiudeva il Remote Manager a chiunque, compreso chi
# aveva appena installato, e non c'era modo di riaprirlo se non modificando
# questo file via SSH. Adesso il servizio ascolta ovunque ma ACCETTA solo dalle
# reti a cui la macchina e' attaccata (la LAN, e la ZeroTier se configurata),
# quindi non si espone al mondo e l'utente lo raggiunge da casa.
d.pop("user", None)
json.dump(d, open(p, "w"), indent=2)
PY
        echo "igiene: dashboard.json spedito senza chiave API; ascolta su tutte le
              interfacce ma accetta solo dalle reti locali"
        # ⚠️ si SPOSTA, non si cancella: e' la chiave vera di questa scheda.
        # `deposita` la mette nel deposito e la registra, e `ripristina` la
        # rimette a fine build. Prima qui c'era un `rm` con "$RAD", una
        # variabile che in questo script non esiste: con set -u l'igiene
        # usciva a meta' e la build falliva sempre.
        deposita /etc/skillfish/unsloth.key
    fi
    ;;

ripristina)
    rimetti_tutto
    # Le impostazioni flatpak non si spostano (dentro ci sono anche i NOSTRI
    # rimedi, che devono restare): si toglie solo la riga delle cartelle
    # condivise e se ne tiene una copia. Quella copia va rimessa, altrimenti
    # Steam resta senza la cartella dei giochi e senza il NAS - successo il
    # 19/08/2026, e nessuno se ne accorge finche' non prova ad avviare un gioco.
    rifl=0
    for b in "$DEP"/_*flatpak_overrides_*; do
        [ -f "$b" ] || continue
        dst="/$(basename "$b" | sed 's/^_//' | tr '_' '/')"
        if [ -f "$dst" ]; then cp -f "$b" "$dst" && rm -f "$b" && rifl=$((rifl + 1)); fi
    done
    [ "$rifl" -gt 0 ] && echo "   rimesse le cartelle condivise di $rifl flatpak"
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
    for f in $IDENTITA_MACCHINA $STATO_SCHEDA $BANCO_DI_LAVORO $ACCESSO_DI_SVILUPPO $BANCO_DI_SVILUPPO $(casa_da_ripulire) $SERVIZI_DA_NON_SPEDIRE; do
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

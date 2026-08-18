#!/bin/bash
# Build the SkillFishOS app .debs from the repo sources (CI / clean machine).
# Unlike the on-box builders, every input comes from git — this catches the
# "stale binary packaged into a new version" failure mode before publishing.
set -euo pipefail
cd "$(dirname "$0")/.."
VER="${1:-0.0~ci$(date +%Y%m%d)}"
OUT="${OUT:-/tmp/sfx-debs}"
rm -rf "$OUT"; mkdir -p "$OUT/out"

# Ogni put/opt/putdir annota la SORGENTE in .sources. Serve a generare il
# changelog del pacchetto dai commit che toccano davvero i SUOI file, invece di
# un testo generico uguale per tutti.
note_src() { mkdir -p "$OUT/$1"; echo "$2" >> "$OUT/$1/.sources"; }

put() { # put <pkg> <mode> <src> <dest-rel>
  [ -f "$3" ] || { echo "FATAL: missing source file $3" >&2; exit 1; }
  install -D -m "$2" "$3" "$OUT/$1/$4"
  note_src "$1" "$3"
}
opt() { # like put, but optional
  [ -f "$3" ] && { install -D -m "$2" "$3" "$OUT/$1/$4"; note_src "$1" "$3"; } \
               || echo "  (optional, skipped: $3)"
}
putdir() { # putdir <pkg> <src-dir> <dest-rel-dir>: install a whole tree (0644)
  [ -d "$2" ] || { echo "FATAL: missing source dir $2" >&2; exit 1; }
  local f
  while IFS= read -r f; do
    install -D -m 0644 "$2/$f" "$OUT/$1/$3/$f"
  done < <(cd "$2" && find . -type f ! -name 'icon-theme.cache' -printf '%P\n')
  note_src "$1" "$2"
}
# CHANGELOG E COPYRIGHT, che prima non c'erano affatto.
#
# I nostri .deb non avevano nemmeno la cartella /usr/share/doc/<pkg>/. Per la
# Debian Policy changelog.Debian.gz e copyright sono OBBLIGATORI, non un
# optional: senza, chi installa non ha modo di sapere cosa e' cambiato ne' con
# quale licenza sta usando il software. Su un sistema che si scarica da mezzo
# mondo e' una mancanza seria.
#
# Il changelog NON e' un testo di comodo: si genera dai commit git che toccano
# i file di QUEL pacchetto (l'elenco lo ha accumulato note_src). Se un pacchetto
# non e' cambiato, la sua voce lo dice invece di inventare una riga.
docs() { # docs <pkg>
  local p="$1" d="$OUT/$1/usr/share/doc/$1"
  mkdir -p "$d"

  # --- changelog dai commit veri ---
  local righe=""
  if [ -f "$OUT/$p/.sources" ] && git -C . rev-parse >/dev/null 2>&1; then
    # shellcheck disable=SC2046
    righe=$(git log -n 12 --no-merges --pretty=format:'%s' -- \
              $(sort -u "$OUT/$p/.sources" | tr '\n' ' ') 2>/dev/null \
            | sed 's/[[:space:]]*$//' | awk 'NF' | head -8)
  fi
  [ -n "$righe" ] || righe="Nessuna modifica ai file di questo pacchetto in questa versione."

  {
    printf '%s (%s) unstable; urgency=medium\n\n' "$p" "$VER"
    printf '%s\n' "$righe" | sed 's/^/  * /'
    printf '\n -- SkillFishOS <info@skillfishos.com>  %s\n' "$(date -R)"
  } > "$d/changelog.Debian"
  gzip -9n -f "$d/changelog.Debian"

  # --- copyright ---
  cat > "$d/copyright" <<COPY
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: SkillFishOS
Source: https://github.com/skillfishos/SkillFishOS

Files: *
Copyright: 2026 Mattia Tadini e collaboratori SkillFishOS
License: GPL-3+
 Questo programma e' software libero: puoi ridistribuirlo e/o modificarlo nei
 termini della GNU General Public License come pubblicata dalla Free Software
 Foundation, versione 3 o (a tua scelta) una successiva.
 .
 E' distribuito nella speranza che sia utile, ma SENZA ALCUNA GARANZIA, senza
 nemmeno la garanzia implicita di COMMERCIABILITA' o IDONEITA' PER UNO SCOPO
 PARTICOLARE. Vedi la GNU General Public License per i dettagli.
 .
 Su un sistema Debian il testo completo della GPL versione 3 si trova in
 /usr/share/common-licenses/GPL-3.
COPY
}

ctrl() { # ctrl <pkg> <depends> <desc-first-line>
  mkdir -p "$OUT/$1/DEBIAN"
  docs "$1"
  printf 'Package: %s\nVersion: %s\nArchitecture: all\nMaintainer: SkillFishOS <info@skillfishos.com>\nDepends: %s\nSection: utils\nPriority: optional\nHomepage: https://skillfishos.com\nDescription: %s\n built from git by CI.\n' \
    "$1" "$VER" "$2" "$3" > "$OUT/$1/DEBIAN/control"
  printf '#!/bin/sh\nset -e\nupdate-desktop-database -q 2>/dev/null || true\ngtk-update-icon-cache -q -f /usr/share/icons/hicolor 2>/dev/null || true\nappstreamcli refresh-cache --force >/dev/null 2>&1 || true\nexit 0\n' > "$OUT/$1/DEBIAN/postinst"
  chmod 0755 "$OUT/$1/DEBIAN/postinst"
}
shot() { # shot <pkg> <metainfo-path>: install metainfo + its referenced screenshots
  put "$1" 0644 "$2" "usr/share/metainfo/$(basename "$2")"
  for s in $(grep -oE 'screenshots/[A-Za-z0-9._-]+' "$2" | sed 's#screenshots/##' | sort -u); do
    opt "$1" 0644 "screenshots/$s" "usr/share/skillfish/screenshots/$s"
  done
}

P=skillfish-tuner
put $P 0755 apps/tuner/skillfish-tuner            usr/local/bin/skillfish-tuner
put $P 0755 apps/tuner/skillfish-tuner-helper     usr/local/bin/skillfish-tuner-helper
put $P 0755 system/usr/local/bin/skillfish-cu     usr/local/bin/skillfish-cu
# Configurazione della memoria: nostra, GPL-3.0. Prima il Tuner cercava uno
# strumento di terzi in /opt che non e' ridistribuibile e che su una macchina
# installata da apt non esisteva: la voce della VRAM era li' e non funzionava.
put $P 0755 system/usr/local/bin/skillfish-memcfg usr/local/bin/skillfish-memcfg
put $P 0755 system/usr/local/bin/skillfish-hud-val usr/local/bin/skillfish-hud-val
put $P 0755 system/usr/local/bin/skillfish-hud-config usr/local/bin/skillfish-hud-config
put $P 0755 system/usr/local/bin/skillfish-hud-bt usr/local/bin/skillfish-hud-bt
# Il lanciatore del HUD sta qui e non in un pacchetto suo perche' legge i due
# helper qui sopra: separarli permetterebbe di installarlo senza i sensori che
# gli servono. Deve essere un file eseguibile e non un comando dentro il
# .desktop: KDE converte l'autostart in un servizio systemd e in quel passaggio
# $HOME resta letterale, quindi conky non trovava la configurazione.
put $P 0755 system/usr/local/bin/skillfish-hud     usr/local/bin/skillfish-hud
put $P 0644 system/usr/share/skillfish/tuner-presets.json usr/share/skillfish/tuner-presets.json
put $P 0644 system/usr/share/applications/os.skillfish.Tuner.desktop usr/share/applications/os.skillfish.Tuner.desktop
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfish-tuner.png usr/share/icons/hicolor/256x256/apps/skillfish-tuner.png
put $P 0644 system/etc/systemd/system/skillfish-cu.service etc/systemd/system/skillfish-cu.service
opt $P 0644 system/usr/share/polkit-1/actions/os.skillfish.tuner.policy usr/share/polkit-1/actions/os.skillfish.tuner.policy
shot $P apps/tuner/os.skillfish.Tuner.metainfo.xml
ctrl $P "python3, python3-pyqt6, polkitd | policykit-1" "SkillFishOS Tuner - BC-250 hardware control GUI"

P=skillfish-hub
put $P 0755 apps/hub/skillfish-hub        usr/local/bin/skillfish-hub
put $P 0755 apps/hub/skillfish-hub-helper usr/local/bin/skillfish-hub-helper
put $P 0644 system/usr/share/applications/os.skillfish.hub.desktop usr/share/applications/os.skillfish.hub.desktop
# L'icona e' la borsa steampunk del NOSTRO tema — quella che SkillFishSteampunk
# usa per Discover, di cui l'Hub prende il posto nella barra — copiata come
# skillfish-hub invece di puntare al nome "plasmadiscover", che appartiene a
# plasma-discover-common: se togliessimo Discover dalla ISO l'Hub resterebbe con
# un quadrato vuoto.
# Qui vanno solo le copie in HICOLOR, che sono l'icona propria dell'Hub e
# funzionano con qualunque tema. La variante steampunk la spedisce
# skillfish-theme insieme al resto del tema: due pacchetti che scrivono nella
# stessa cartella del tema sarebbero un guaio inutile.
# I PNG servono perche' nel codice l'icona della finestra e' un PERCORSO passato
# a QPixmap, non un nome di tema.
put $P 0644 system/usr/share/icons/hicolor/scalable/apps/skillfish-hub.svg usr/share/icons/hicolor/scalable/apps/skillfish-hub.svg
put $P 0644 system/usr/share/icons/hicolor/48x48/apps/skillfish-hub.png   usr/share/icons/hicolor/48x48/apps/skillfish-hub.png
put $P 0644 system/usr/share/icons/hicolor/128x128/apps/skillfish-hub.png usr/share/icons/hicolor/128x128/apps/skillfish-hub.png
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfish-hub.png usr/share/icons/hicolor/256x256/apps/skillfish-hub.png
shot $P apps/hub/os.skillfish.hub.metainfo.xml
ctrl $P "python3, python3-pyqt6, python3-apt, gir1.2-appstream-1.0, appstream, curl, polkitd | policykit-1" "SkillFishOS Hub - Discover-style software centre"

P=skillfish-monitor
put $P 0755 apps/monitor/skillfish-monitor usr/local/bin/skillfish-monitor
put $P 0644 system/usr/share/applications/os.skillfish.monitor.desktop usr/share/applications/os.skillfish.monitor.desktop
put $P 0644 system/usr/share/mime/packages/os.skillfish.monitor.xml usr/share/mime/packages/os.skillfish.monitor.xml
shot $P apps/monitor/os.skillfish.monitor.metainfo.xml
ctrl $P "python3, python3-pyqt6" "SkillFishOS Monitor - live sensor charts + .sfmon benchmark analyzer"
# monitor ships a MIME type (.sfmon recordings) → also refresh the shared-mime db
printf '#!/bin/sh\nset -e\nupdate-mime-database /usr/share/mime >/dev/null 2>&1 || true\nupdate-desktop-database -q 2>/dev/null || true\nappstreamcli refresh-cache --force >/dev/null 2>&1 || true\nexit 0\n' > "$OUT/$P/DEBIAN/postinst"
chmod 0755 "$OUT/$P/DEBIAN/postinst"

P=skillfish-kernel-manager
put $P 0755 apps/kernel-manager/skillfish-kernel-manager usr/local/bin/skillfish-kernel-manager
put $P 0755 apps/kernel-manager/skillfish-kernel-helper  usr/local/bin/skillfish-kernel-helper
put $P 0644 system/usr/share/applications/os.skillfish.kernel.desktop usr/share/applications/os.skillfish.kernel.desktop
shot $P apps/kernel-manager/os.skillfish.kernel.metainfo.xml
ctrl $P "python3, python3-pyqt6, polkitd | policykit-1" "SkillFishOS Kernel Manager"

P=skillfish-ai-panel
put $P 0755 apps/ai-panel/skillfish-ai-panel usr/local/bin/skillfish-ai-panel
put $P 0755 apps/ai-panel/skillfish-gtt      usr/local/bin/skillfish-gtt
# the setup wizard shells out to this to install the Unsloth engine
put $P 0755 scripts/install-unsloth.sh       usr/local/share/skillfish/install-unsloth.sh
# ⚠️ Il lanciatore del motore AI e la sua unit NON erano in nessun pacchetto:
#    stavano solo sul disco della scheda. Come per lo sfondo, una correzione non
#    poteva arrivare a chi aveva gia' installato. E il lanciatore aveva dentro
#    /root, che nell'immagine non c'e': il motore non partiva per nessuno.
put $P 0755 system/usr/local/bin/skillfish-unsloth        usr/local/bin/skillfish-unsloth
put $P 0755 system/usr/local/bin/skillfish-unsloth-update usr/local/bin/skillfish-unsloth-update
put $P 0644 system/etc/systemd/system/skillfish-unsloth.service etc/systemd/system/skillfish-unsloth.service
put $P 0644 system/usr/share/applications/os.skillfish.ai.desktop usr/share/applications/os.skillfish.ai.desktop
shot $P apps/ai-panel/os.skillfish.ai.metainfo.xml
ctrl $P "python3, python3-pyqt6, polkitd | policykit-1" "SkillFish AI - on-device LLM control panel"
# ⚠️ L'unita' del motore AI veniva spedita e non la accendeva nessuno: sulla
# scheda risultava attiva solo perche' l'avevo abilitata a mano, e nella ISO ci
# finiva per clonazione. Chi installa da apt si ritrovava il file dell'unita' e
# nessun servizio. "--now" e' sicuro: skillfish-unsloth esce con 0, non con 1,
# quando Unsloth non e' installato, quindi niente ciclo di riavvii.
printf '#!/bin/sh\nset -e\nupdate-desktop-database -q 2>/dev/null || true\ngtk-update-icon-cache -q -f /usr/share/icons/hicolor 2>/dev/null || true\nappstreamcli refresh-cache --force >/dev/null 2>&1 || true\nif [ -d /run/systemd/system ]; then\n  systemctl daemon-reload || true\n  systemctl enable --now skillfish-unsloth.service 2>/dev/null || true\nfi\nexit 0\n' > "$OUT/$P/DEBIAN/postinst"
chmod 0755 "$OUT/$P/DEBIAN/postinst"

P=skillfishos-archive-keyring
# La sorgente apt e la chiave di firma erano gli ultimi due file di sistema che
# non appartenevano a nessun pacchetto: scritti a mano sulla scheda, copiati
# nella ISO, e da li' in poi immutabili. Se un giorno la chiave scade o cambia
# indirizzo il repository, oggi non avremmo nessun modo di aggiornarli sulle
# macchine gia' installate — proprio lo strumento che serve per rimediare
# passerebbe da un repository che non si riesce piu' a verificare.
#
# Come per debian-archive-keyring: il pacchetto porta chiave e sorgente, e da
# quel momento si aggiornano da soli con un apt upgrade.
put $P 0644 system/usr/share/keyrings/skillfishos-archive-keyring.gpg usr/share/keyrings/skillfishos-archive-keyring.gpg
put $P 0644 system/etc/apt/sources.list.d/skillfishos.sources          etc/apt/sources.list.d/skillfishos.sources
ctrl $P "gnupg | gpgv" "SkillFishOS archive keyring and APT source"

P=skillfish-base
# Script nostri che stavano solo dentro l'immagine e non in un pacchetto: una
# correzione a uno di questi non poteva raggiungere chi ha gia' installato.
put $P 0755 system/usr/local/bin/skillfish-dp-hotswap.sh    usr/local/bin/skillfish-dp-hotswap.sh
put $P 0755 system/usr/local/bin/skillfish-thermal-guard.sh usr/local/bin/skillfish-thermal-guard.sh
put $P 0755 system/usr/local/bin/skillfish-gpu-util.sh      usr/local/bin/skillfish-gpu-util.sh
put $P 0755 system/usr/local/bin/skillfish-kde-firstrun.sh  usr/local/bin/skillfish-kde-firstrun.sh
put $P 0755 system/usr/local/bin/skillfish-x11vnc.sh        usr/local/bin/skillfish-x11vnc.sh
put $P 0755 system/usr/local/bin/skillfish-freeze-check.sh  usr/local/bin/skillfish-freeze-check.sh
put $P 0755 system/usr/local/bin/skillfish-freeze-notify.sh usr/local/bin/skillfish-freeze-notify.sh
put $P 0644 system/etc/systemd/system/skillfish-freeze-check.service etc/systemd/system/skillfish-freeze-check.service
put $P 0644 system/etc/xdg/autostart/skillfish-freeze-notify.desktop  etc/xdg/autostart/skillfish-freeze-notify.desktop
put $P 0644 system/etc/modules-load.d/skillfish-watchdog.conf         etc/modules-load.d/skillfish-watchdog.conf
put $P 0644 system/etc/systemd/system.conf.d/10-skillfish-watchdog.conf etc/systemd/system.conf.d/10-skillfish-watchdog.conf
put $P 0644 system/etc/modules-load.d/skillfish-nct6686.conf          etc/modules-load.d/skillfish-nct6686.conf
put $P 0644 system/etc/systemd/system/skillfish-wol.service          etc/systemd/system/skillfish-wol.service
put $P 0755 system/usr/local/bin/skillfish-wol-arm                    usr/local/bin/skillfish-wol-arm
# Snapshot Btrfs del primo avvio. Questi due file non appartenevano a NESSUN
# pacchetto: arrivavano solo dentro la ISO, quindi non potevamo correggerli con
# un aggiornamento. E c'era da correggere: il marcatore
# /var/lib/skillfish/.snapshots-setup-done finiva nel squashfs preso dalla
# macchina di build, la condizione della unit lo trovava e il servizio veniva
# saltato su OGNI installazione. Nessun sottovolume /.snapshots, nessun punto di
# ripristino, snapper-boot in failed.
put $P 0755 system/usr/local/bin/skillfish-firstboot-snapshots.sh     usr/local/bin/skillfish-firstboot-snapshots.sh
put $P 0644 system/etc/systemd/system/skillfish-firstboot-snapshots.service etc/systemd/system/skillfish-firstboot-snapshots.service
# Il menu di ripristino: grub-btrfsd non lo aggiorna (durante apt fallisce, a
# riposo non reagisce), quindi lo rigeneriamo noi a fine transazione apt.
put $P 0755 system/usr/local/bin/skillfish-snapshot-menu               usr/local/bin/skillfish-snapshot-menu
put $P 0644 system/etc/apt/apt.conf.d/99-skillfish-snapshots           etc/apt/apt.conf.d/99-skillfish-snapshots
# Tornare a uno snapshot per davvero: dal menu di avvio ci si entra in sola
# lettura, e `snapper rollback` non funziona perche' grub.cfg fissa subvol=@.
put $P 0755 system/usr/local/bin/skillfish-rollback                    usr/local/bin/skillfish-rollback
put $P 0644 system/etc/modprobe.d/skillfish-nct6686.conf              etc/modprobe.d/skillfish-nct6686.conf
put $P 0644 system/etc/modules-load.d/skillfish-ntsync.conf           etc/modules-load.d/skillfish-ntsync.conf
put $P 0755 system/usr/local/bin/skillfish-core-unlock                usr/local/bin/skillfish-core-unlock
put $P 0755 system/usr/local/bin/skillfish-fix-boot-extents         usr/local/bin/skillfish-fix-boot-extents
put $P 0755 system/usr/local/bin/skillfish-clean-live-autologin   usr/local/bin/skillfish-clean-live-autologin
put $P 0755 system/usr/local/bin/skillfish-fix-nct6687              usr/local/bin/skillfish-fix-nct6687
put $P 0755 system/usr/local/bin/skillfish-grub-btrfs               usr/local/bin/skillfish-grub-btrfs
# Gancio del kernel: gira PRIMA di dkms (run-parts va in ordine alfabetico e
# il gancio di DKMS si chiama "dkms"), cosi' il sorgente e' gia' a posto
# quando DKMS prova a costruirlo. Con un nome tipo zz- avremmo corretto il
# sorgente subito dopo il fallimento, cioe' mai in tempo.
put $P 0755 system/etc/kernel/postinst.d/00-skillfish-nct6687       etc/kernel/postinst.d/00-skillfish-nct6687
put $P 0755 system/usr/local/bin/skillfish-is-bc250                usr/local/bin/skillfish-is-bc250
put $P 0644 system/etc/systemd/system/skillfish-sshd-keygen.service etc/systemd/system/skillfish-sshd-keygen.service
put $P 0644 system/etc/ssh/sshd_config.d/10-skillfish.conf        etc/ssh/sshd_config.d/10-skillfish.conf
put $P 0644 system/etc/systemd/coredump.conf.d/10-skillfish.conf  etc/systemd/coredump.conf.d/10-skillfish.conf
put $P 0644 system/etc/systemd/system/skillfish-core-unlock.service   etc/systemd/system/skillfish-core-unlock.service
put $P 0755 system/usr/local/bin/skillfish-gpu-freq-sampler           usr/local/bin/skillfish-gpu-freq-sampler
put $P 0644 system/etc/systemd/system/skillfish-gpu-freq.service      etc/systemd/system/skillfish-gpu-freq.service
put $P 0644 system/etc/skel/.config/conky/skillfish.conf              etc/skel/.config/conky/skillfish.conf
# L'autostart del HUD viaggia insieme alla configurazione conky qui sopra:
# spedire l'una senza l'altro lascia il HUD che non parte, oppure un autostart
# che punta a un file che non c'e'. Prima non apparteneva a NESSUN pacchetto,
# quindi arrivava solo a chi installava dalla ISO.
put $P 0644 system/etc/skel/.config/autostart/skillfish-conky.desktop etc/skel/.config/autostart/skillfish-conky.desktop
# skillfish-info: fastfetch in un terminale che resta aperto. Anche questi due
# non appartenevano a nessun pacchetto. Il comando sta in uno script perche' nel
# campo Exec di un .desktop "%s" e' un codice di sostituzione riservato e il "$"
# va raddoppiato: desktop-file-validate rifiutava la vecchia riga.
put $P 0755 system/usr/local/bin/skillfish-info                       usr/local/bin/skillfish-info
put $P 0644 system/usr/share/applications/skillfish-info.desktop      usr/share/applications/skillfish-info.desktop
put $P 0755 system/usr/local/bin/skillfish-acpi-pstates               usr/local/bin/skillfish-acpi-pstates
put $P 0644 system/usr/share/skillfish/acpi/SSDT-PST.aml              usr/share/skillfish/acpi/SSDT-PST.aml
put $P 0644 system/usr/share/skillfish/acpi/SSDT-PST.dsl              usr/share/skillfish/acpi/SSDT-PST.dsl
put $P 0644 system/usr/share/skillfish/acpi/SSDT-CST.aml              usr/share/skillfish/acpi/SSDT-CST.aml
put $P 0644 system/usr/share/skillfish/acpi/SSDT-CST.dsl              usr/share/skillfish/acpi/SSDT-CST.dsl
ctrl $P "systemd, libnotify-bin, python3, cpio, locales" "SkillFishOS base - hardware watchdog + freeze detector + 8-core unlock"
# base needs its own postinst: enable the watchdog and the freeze check.
# NOTE: core-unlock is only *enabled* (never --now): it warm-reboots the machine when
# it flips the mask, which must not happen during apt. It fires on the next boot.
cat > "$OUT/$P/DEBIAN/postinst" <<'POSTINST'
#!/bin/sh
set -e
if [ -d /run/systemd/system ]; then
  systemctl daemon-reload || true
  # senza chiavi host ssh.service fallisce all'infinito su installazione fresca
  systemctl enable skillfish-sshd-keygen.service || true
  [ -f /etc/ssh/ssh_host_ed25519_key ] || ssh-keygen -A || true
  systemctl enable --now skillfish-freeze-check.service || true
  # enable --now avvia solo se e' ferma: se era gia' attiva con la vecchia
  # definizione, la nuova (RemainAfterExit + ExecStop) non entrerebbe in vigore
  # fino al riavvio. Il try-restart e' innocuo: scrive il marcatore e lo
  # riconsuma subito.
  systemctl try-restart skillfish-freeze-check.service || true
  # Ripulisce cio' che la live si lascia dietro su un sistema installato:
  # l'accesso automatico dell'utente 'live' e il generatore di getty orfano.
  # Non fa niente se non c'e' niente da fare, ed e' l'unico modo di arrivare
  # a chi ha installato prima che la correzione esistesse.
  /usr/local/bin/skillfish-clean-live-autologin >/dev/null 2>&1 || true
  # Il gancio del kernel serve ai kernel FUTURI; chi ha gia' installato il
  # 7.2 a mano, o lo installera' nella stessa transazione di questo
  # pacchetto, ha bisogno che il sorgente sia corretto adesso.
  /usr/local/bin/skillfish-fix-nct6687 >/dev/null 2>&1 || true
  # Lo sblocco degli 8 core dal 16/08/2026 e' A RICHIESTA: il servizio resta
  # abilitato ma non parte senza il segnaposto. Chi aveva gia' gli 8 core li ha
  # perche' il vecchio servizio glieli sbloccava da solo: se al momento
  # dell'aggiornamento la maschera e' gia' 0xFF vuol dire che li stava usando, e
  # non glieli spegniamo sotto il naso. Chi non li aveva resta com'era.
  if [ ! -e /etc/skillfish/core-unlock.abilitato ] \
     && [ "$(/usr/local/bin/skillfish-core-unlock --maschera 2>/dev/null)" = "0xff" ]; then
    mkdir -p /etc/skillfish
    printf '%s\n' \
      "# Creato aggiornando da una versione in cui lo sblocco era automatico:" \
      "# questa macchina aveva gia' gli 8 core attivi, quindi li tiene." \
      "# Si spegne dall'interruttore 8 core in SkillFishOS Tuner." \
      > /etc/skillfish/core-unlock.abilitato
  fi
  systemctl enable skillfish-core-unlock.service || true
  # ntsync serve a Proton: caricalo subito, non al prossimo riavvio
  modprobe ntsync 2>/dev/null || true
  # guardia hardware sui servizi specifici della BC-250: senza, su un PC
  # normale ripartono ogni 5 secondi all'infinito
  for u in cyan-skillfish-governor skillfish-core-unlock skillfish-cu            skillfish-gpu-freq skillfish-gpu-util skillfish-thermal-guard            skillfish-dp-hotswap bc250-smu-oc; do
    f=""
    for d in /etc/systemd/system /usr/lib/systemd/system; do
      [ -f "$d/$u.service" ] && { f="$d/$u.service"; break; }
    done
    [ -n "$f" ] || continue
    grep -q 'ExecCondition=/usr/local/bin/skillfish-is-bc250' "$f" && continue
    grep -q '^ExecStart=' "$f" || continue
    # Il ritorno a capo va scritto come \n nella sostituzione. Prima c'era un
    # a capo VERO dentro le virgolette singole, e sed rispondeva
    #   sed: -e expression #1, char 65: unterminated `s' command
    # cioe' non inseriva NIENTE: la guardia hardware non e' mai stata aggiunta a
    # questi servizi, che e' proprio il guasto che doveva evitare.
    sed -i '0,/^ExecStart=/s|^ExecStart=|ExecCondition=/usr/local/bin/skillfish-is-bc250\nExecStart=|' "$f" || true
  done
  systemctl daemon-reload || true
  systemctl enable --now skillfish-gpu-freq.service || true
  # lo stato failed di prima resta appiccicato anche dopo la correzione
  systemctl reset-failed skillfish-wol.service bc250-smu-oc.service 2>/dev/null || true
  systemctl enable --now skillfish-wol.service || true
  # Snapshot Btrfs: abilita il servizio e falli adesso, non al prossimo riavvio.
  # Chi ha installato da una ISO precedente non ha /.snapshots come sottovolume e
  # quindi non ha nemmeno un punto di ripristino: con questo aggiornamento lo
  # ottiene subito. Sulla macchina di build lo script vede che c'e' gia' tutto ed
  # esce in un istante.
  systemctl enable skillfish-firstboot-snapshots.service || true
  if [ -x /usr/local/bin/skillfish-firstboot-snapshots.sh ]; then
    /usr/local/bin/skillfish-firstboot-snapshots.sh || true
  fi
  # Accesso automatico rimasto dalla sessione live. Sul sistema installato punta
  # a un utente che li' non esiste: SDDM ci prova a ogni avvio, fallisce con
  # "could not identify user" e ripiega sulla schermata di accesso. Nessun danno,
  # ma una riga rossa nel journal a ogni avvio.
  # La condizione e' precisa: si tocca il file SOLO se l'utente indicato non
  # esiste. Sulla sessione live l'utente c'e' e il file resta dov'e', che e'
  # esattamente quello che serve perche' la live parta senza chiedere nulla.
  AL=/etc/sddm.conf.d/autologin.conf
  if [ -f "$AL" ]; then
    u=$(sed -n 's/^ *User *= *//p' "$AL" | head -1)
    if [ -n "$u" ] && ! id "$u" >/dev/null 2>&1; then
      rm -f "$AL"
      echo "SkillFishOS: tolto l'accesso automatico dell'utente «$u», che su questo sistema non esiste"
    fi
  fi
  # e le voci di ripristino nel menu, subito
  [ -x /usr/local/bin/skillfish-snapshot-menu ] && /usr/local/bin/skillfish-snapshot-menu || true
  modprobe sp5100_tco 2>/dev/null || true
  modprobe nct6687 force=1 2>/dev/null || true
  systemctl daemon-reexec || true
fi

# ACPI P-states: the BC-250 firmware exposes no _PSS, so Linux has no cpufreq at all.
# The helper injects an SSDT via GRUB's early initrd and no-ops on anything that is
# not a BC-250. It only rewrites the GRUB config — the change lands on next boot.
# "auto", non "enable": su una macchina che non e' una BC-250 la tabella non va
# solo "non attivata", va TOLTA, perche' l'immagine se la porta dietro dalla
# scheda di sviluppo dove era attiva. Con "enable" lo script si limitava a dire
# "non e' una BC-250" e se ne andava, lasciando l'iniezione al suo posto e 32
# errori ACPI a ogni avvio.
/usr/local/bin/skillfish-acpi-pstates auto || true

# HUD migration: the desktop widget was wired for 6c/12t. Now that the 8 cores are
# unlocked it needs 16 bars. Only the two cpubar rows are rewritten, and only when
# they still match what we originally shipped — any other customisation is kept,
# and a hand-edited HUD is left alone.
OLD_A='${voffset 3}${color D8A849}${cpubar cpu1 6,16} ${cpubar cpu2 6,16} ${cpubar cpu3 6,16} ${cpubar cpu4 6,16} ${cpubar cpu5 6,16} ${cpubar cpu6 6,16}'
OLD_B='${voffset 2}${color D8A849}${cpubar cpu7 6,16} ${cpubar cpu8 6,16} ${cpubar cpu9 6,16} ${cpubar cpu10 6,16} ${cpubar cpu11 6,16} ${cpubar cpu12 6,16}'
NEW_A='${voffset 3}${color D8A849}${cpubar cpu1 6,16} ${cpubar cpu2 6,16} ${cpubar cpu3 6,16} ${cpubar cpu4 6,16} ${cpubar cpu5 6,16} ${cpubar cpu6 6,16} ${cpubar cpu7 6,16} ${cpubar cpu8 6,16}'
NEW_B='${voffset 2}${color D8A849}${cpubar cpu9 6,16} ${cpubar cpu10 6,16} ${cpubar cpu11 6,16} ${cpubar cpu12 6,16} ${cpubar cpu13 6,16} ${cpubar cpu14 6,16} ${cpubar cpu15 6,16} ${cpubar cpu16 6,16}'
for cfg in /home/*/.config/conky/skillfish.conf /root/.config/conky/skillfish.conf; do
  [ -f "$cfg" ] || continue
  grep -qF "$OLD_B" "$cfg" || continue
  python3 - "$cfg" "$OLD_A" "$OLD_B" "$NEW_A" "$NEW_B" <<'PY' || true
import sys
p, oa, ob, na, nb = sys.argv[1:6]
t = open(p, encoding='utf-8').read()
open(p, 'w', encoding='utf-8').write(t.replace(oa, na).replace(ob, nb))
PY
  echo "skillfish-base: HUD aggiornato a 16 thread in $cfg"
done

# Le quattro lingue di SkillFishOS.
#
# Le traduzioni polacche (di cyryllo) sono nelle app da mesi, ma sull'immagine
# risultavano generati solo en_US e it_IT: senza il locale generato, KDE non
# mostra la lingua nel menu delle impostazioni e SDDM non la offre. Il polacco
# era quindi presente nel codice e irraggiungibile per l'utente. Verificato
# sulla scheda con `locale -a`: due voci in tutto.
#
# Qui li abilitiamo tutti e quattro in locale.gen e rigeneriamo, ma solo se
# qualcosa e' davvero cambiato: locale-gen ci mette parecchio e non ha senso
# rifarlo a ogni aggiornamento del pacchetto.
if [ -f /etc/locale.gen ]; then
  need=0
  for l in en_US.UTF-8 it_IT.UTF-8 pl_PL.UTF-8 uk_UA.UTF-8; do
    if grep -qE "^${l} UTF-8" /etc/locale.gen; then
      continue
    elif grep -qE "^[#[:space:]]*${l} UTF-8" /etc/locale.gen; then
      sed -i "s|^[#[:space:]]*\(${l} UTF-8\)|\1|" /etc/locale.gen
      need=1
    else
      echo "${l} UTF-8" >> /etc/locale.gen
      need=1
    fi
  done
  if [ "$need" = 1 ]; then
    echo "skillfish-base: genero i locale it/en/pl/uk (ci vuole qualche secondo)"
    locale-gen >/dev/null 2>&1 || true
  fi
fi

exit 0
POSTINST
# On removal the SSDT would vanish while GRUB still referenced it, so undo the
# bootloader change before the files go away.
cat > "$OUT/$P/DEBIAN/prerm" <<'PRERM'
#!/bin/sh
set -e
if [ "$1" = remove ] || [ "$1" = purge ]; then
  [ -x /usr/local/bin/skillfish-acpi-pstates ] && /usr/local/bin/skillfish-acpi-pstates disable || true
fi
exit 0
PRERM
chmod 0755 "$OUT/$P/DEBIAN/postinst" "$OUT/$P/DEBIAN/prerm"

P=skillfish-console
put $P 0755 system/usr/local/bin/skillfish-gaming-mode usr/local/bin/skillfish-gaming-mode
put $P 0644 system/usr/share/wayland-sessions/skillfish-gaming.desktop usr/share/wayland-sessions/skillfish-gaming.desktop
# Il comando che permette di USCIRE dalla console. Con -steamos3 Steam crede di
# essere su SteamOS e per tornare al desktop esegue `steamos-session-select
# desktop`: da noi non esisteva, quindi restava per sempre su "passaggio al
# desktop in corso".
#
# Due copie: una sull'host, una in /opt perche' Steam e' un flatpak e lo esegue
# DENTRO il sandbox. Non puo' stare sotto /usr — li' il sandbox ha gia' il
# proprio runtime e flatpak si rifiuta di montarci sopra il percorso dell'host.
put $P 0755 system/usr/local/bin/steamos-session-select usr/local/bin/steamos-session-select
put $P 0755 system/usr/local/bin/steamos-session-select opt/skillfish/steam-bin/steamos-session-select
ctrl $P "gamescope, flatpak" "SkillFishOS Console - SteamOS-style Big Picture session"
# Steam deve poter trovare ed eseguire quel comando: la cartella, il PATH del
# sandbox e il permesso di parlare col servizio Flatpak, che serve a
# flatpak-spawn per agire sull'host.
cat > "$OUT/$P/DEBIAN/postinst" <<'POSTCONS'
#!/bin/sh
set -e
if command -v flatpak >/dev/null 2>&1; then
  flatpak override --system com.valvesoftware.Steam       --filesystem=/opt/skillfish/steam-bin:ro       --talk-name=org.freedesktop.Flatpak       --env=PATH=/opt/skillfish/steam-bin:/app/bin:/app/utils/bin:/usr/bin 2>/dev/null || true
fi
exit 0
POSTCONS
chmod 0755 "$OUT/$P/DEBIAN/postinst"

P=skillfish-dashboard
put $P 0755 apps/dashboard/skillfish-dashboardd      usr/local/bin/skillfish-dashboardd
put $P 0755 apps/dashboard/skillfish-remote-manager  usr/local/bin/skillfish-remote-manager
put $P 0755 apps/dashboard/skillfish-remote-ctl      usr/local/bin/skillfish-remote-ctl
put $P 0755 system/usr/local/bin/skillfish-dashboard-stop usr/local/bin/skillfish-dashboard-stop
put $P 0755 apps/dashboard/skillfish-hub-catalog     usr/local/bin/skillfish-hub-catalog
put $P 0644 apps/dashboard/web/index.html  usr/share/skillfish/dashboard/index.html
put $P 0644 apps/dashboard/web/app.js      usr/share/skillfish/dashboard/app.js
# i18n.js e' il dizionario condiviso delle pagine che NON caricano app.js
# (tuner, hub, aichat). Se non viaggia nel pacchetto quelle tre pagine lo
# chiedono, ricevono un 404 e restano senza traduzioni: il difetto sarebbe
# passato inosservato perche' il testo statico resta comunque leggibile.
put $P 0644 apps/dashboard/web/i18n.js     usr/share/skillfish/dashboard/i18n.js
put $P 0644 apps/dashboard/web/aichat.html usr/share/skillfish/dashboard/aichat.html
put $P 0644 apps/dashboard/web/tuner.html  usr/share/skillfish/dashboard/tuner.html
put $P 0644 apps/dashboard/web/hub.html    usr/share/skillfish/dashboard/hub.html
put $P 0644 system/etc/skillfish/dashboard.json usr/share/skillfish/dashboard-default.json
put $P 0644 system/etc/systemd/system/skillfish-dashboard.service etc/systemd/system/skillfish-dashboard.service
put $P 0644 system/usr/share/applications/os.skillfish.remote-manager.desktop usr/share/applications/os.skillfish.remote-manager.desktop
opt $P 0644 system/usr/share/polkit-1/actions/os.skillfish.remote-manager.policy usr/share/polkit-1/actions/os.skillfish.remote-manager.policy
mkdir -p "$OUT/$P/DEBIAN"
# Questo pacchetto scrive il proprio control a mano invece di usare ctrl(),
# quindi va chiamata docs() esplicitamente: senza, era l'unico a restare senza
# changelog e copyright.
docs $P
cat > "$OUT/$P/DEBIAN/control" <<EOF
Package: skillfish-dashboard
Version: $VER
Architecture: all
Maintainer: SkillFishOS <info@skillfishos.com>
Depends: python3, python3-pyqt6, python3-apt, gir1.2-appstream-1.0, appstream, curl, openssl, polkitd | policykit-1
Recommends: ttyd, novnc, websockify, x11vnc, ethtool, wakeonlan, flatpak, snapd
Suggests: zerotier-one, docker.io
Section: utils
Priority: optional
Homepage: https://skillfishos.com
Description: SkillFishOS Remote Manager - web control dashboard for the BC-250
 A modular, self-hosted web dashboard (PAM login over HTTPS) to control the
 board remotely: live telemetry, software KVM (noVNC), web terminal (ttyd),
 the Tuner (CPU/GPU/compute-unit control), a full Hub app store, AI/OpenWebUI,
 logs, Wake-on-LAN and ZeroTier. Ships the always-available daemon plus the
 native Remote Manager toggle app. Built from git by CI.
EOF
# ⚠️ Si MASCHERA ttyd.service, non lo si disabilita soltanto.
# Il pacchetto Debian ttyd porta una sua unita' abilitata, che parte con le
# opzioni di /etc/default/ttyd (-W -i lo -p 7681 -O login) e occupa la porta
# 7681 SENZA il percorso base /terminal. La dashboard inoltra /terminal/...
# senza togliere il prefisso, perche' si aspetta il ttyd che avvia lei con
# -b /terminal: con quello di systemd in mezzo, il terminale rispondeva 404.
# Disabilitarla non basta: ha Restart=, e un aggiornamento di ttyd la
# rimetterebbe in piedi. Con `-O login` per giunta il terminale richiedeva di
# nuovo utente e password, buttando via il single sign-on della dashboard.
printf '#!/bin/sh\nset -e\nmkdir -p /etc/skillfish\n[ -f /etc/skillfish/dashboard.json ] || cp /usr/share/skillfish/dashboard-default.json /etc/skillfish/dashboard.json\nif [ -d /run/systemd/system ]; then\n  systemctl daemon-reload || true\n  systemctl disable --now ttyd.service 2>/dev/null || true\n  systemctl mask ttyd.service 2>/dev/null || true\nfi\nupdate-desktop-database -q 2>/dev/null || true\nexit 0\n' > "$OUT/$P/DEBIAN/postinst"
printf '#!/bin/sh\nset -e\nif [ "$1" = remove ] || [ "$1" = purge ]; then systemctl disable --now skillfish-dashboard.service 2>/dev/null || true; fi\nexit 0\n' > "$OUT/$P/DEBIAN/prerm"
chmod 0755 "$OUT/$P/DEBIAN/postinst" "$OUT/$P/DEBIAN/prerm"

P=skillfish-theme
# The steampunk look used to be baked into the ISO filesystem only (no package
# owned it), so a fix could not reach installed systems through apt. It ships
# as a package now — same paths, so it simply takes ownership of the files.
putdir $P theme/icons/SkillFishSteampunk              usr/share/icons/SkillFishSteampunk
putdir $P theme/cursors/SkillFish-Steampunk-Cursors   usr/share/icons/SkillFish-Steampunk-Cursors
putdir $P theme/plasma-theme/SkillFishSteampunk       usr/share/plasma/desktoptheme/SkillFishSteampunk
putdir $P theme/look-and-feel/org.skillfish.steampunk usr/share/plasma/look-and-feel/org.skillfish.steampunk
putdir $P theme/Kvantum/SkillFishSteampunk            usr/share/Kvantum/SkillFishSteampunk
put $P 0644 theme/color-scheme/SkillFishSteampunk.colors usr/share/color-schemes/SkillFishSteampunk.colors
# Lo sfondo come vero PACCHETTO wallpaper, non come PNG sciolto.
# Plasma, nella chiave Image= del look-and-feel, si aspetta una cartella con
# metadata.json e contents/images/: davanti a un file singolo non lo risolve e
# ricade sullo sfondo predefinito. Ecco perche' nessuno vedeva il nostro sfondo
# ne' nella live ne' dopo l'installazione. Il percorso e' dichiarato in
# theme/look-and-feel/org.skillfish.steampunk/contents/defaults.
#
# Queste righe stavano piu' in basso, in mezzo ai controlli: giravano dopo
# dpkg-deb e i file non entravano mai nel pacchetto.
put $P 0644 system/usr/share/wallpapers/SkillFishOS/metadata.json \
    usr/share/wallpapers/SkillFishOS/metadata.json
put $P 0644 system/usr/share/wallpapers/SkillFishOS/contents/images/3840x2160.png \
    usr/share/wallpapers/SkillFishOS/contents/images/3840x2160.png
# Il desktop preconfigurato che ogni nuovo utente eredita. Era un file orfano
# sul disco della scheda, come lo sfondo: nessun pacchetto lo possedeva, quindi
# una correzione non poteva raggiungere chi aveva gia' installato.
#
# La sua chiave Image= vince su quella del look-and-feel, ed e' il motivo per
# cui il pacchetto wallpaper da solo non bastava: puntava ancora al PNG grezzo
# e Plasma, davanti a un file singolo, ricade sul proprio sfondo predefinito.
put $P 0644 system/etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc     etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc
# Lo sfondo va IMPOSTATO, non solo dichiarato: Plasma riscrive appletsrc al
# primo accesso e butta via la nostra riga. Questo lo applica dopo.
put $P 0755 system/usr/local/bin/skillfish-first-login-wallpaper usr/local/bin/skillfish-first-login-wallpaper
# Il tema della schermata di accesso non apparteneva a NESSUN pacchetto: viveva
# solo nel filesystem della ISO, quindi una correzione non poteva raggiungere
# via apt chi aveva gia' installato. E ce n'era una da fare: le scritte erano
# cablate in italiano ("Accedi") anche in polacco e ucraino — la primissima cosa
# che si vede del sistema, nella lingua sbagliata.
putdir $P system/usr/share/sddm/themes/skillfish-brass usr/share/sddm/themes/skillfish-brass
put $P 0644 system/etc/skel/.config/autostart/skillfish-wallpaper.desktop etc/skel/.config/autostart/skillfish-wallpaper.desktop
for a in theme/avatars/steampunk-*.png; do
  put $P 0644 "$a" "usr/share/plasma/avatars/$(basename "$a")"
done
ctrl $P "hicolor-icon-theme" "SkillFishOS Steampunk theme - icons, cursors, Plasma theme and colours"
# NON generare una icon-theme.cache per i nostri temi: TOGLIERLA.
#
# Qui c'era `gtk-update-icon-cache -f` sul tema, con `|| rm -f` come ripiego.
# L'intenzione era "costruisci la cache, e se non ci riesci togli quella
# vecchia". Ma il comando RIESCE, e la cache che produce Qt non la sa usare:
# risultato, tutti i lanciatori della barra diventano fogli bianchi. Successo
# davvero l'11/08/2026 sulla scheda, e sarebbe ricapitato su OGNI macchina a
# ogni aggiornamento del pacchetto.
#
# Senza cache Qt legge direttamente le cartelle del tema, che funziona sempre.
# La cache di hicolor invece va aggiornata, e la fa gia' ctrl().
printf '#!/bin/sh\nset -e\nfor t in SkillFishSteampunk SkillFish-Steampunk-Cursors; do\n  rm -f "/usr/share/icons/$t/icon-theme.cache" 2>/dev/null || true\ndone\nexit 0\n' > "$OUT/$P/DEBIAN/postinst"
chmod 0755 "$OUT/$P/DEBIAN/postinst"

echo "== building =="
P=skillfish-iso-mount
# Era rimasto nel vecchio apps/build-debs.sh, che prende i file dal disco della
# scheda: fuori dalla catena automatica, quindi fermo a 26.06 mentre tutto il
# resto avanzava, e una correzione qui non sarebbe mai arrivata a nessuno.
put $P 0755 system/usr/local/bin/skillfish-iso-mount usr/local/bin/skillfish-iso-mount
put $P 0644 system/usr/share/kio/servicemenus/skillfish-iso.desktop usr/share/kio/servicemenus/skillfish-iso.desktop
put $P 0644 system/etc/polkit-1/rules.d/49-skillfish-udisks.rules etc/polkit-1/rules.d/49-skillfish-udisks.rules
ctrl $P "udisks2, polkitd | policykit-1" "SkillFishOS native ISO mounting for KDE"

P=skillfish-menu
# Questo non stava in NESSUNO script: esisteva solo come .deb costruito a mano
# chissa' quando. Definisce la categoria "SkillFishOS" nel menu delle
# applicazioni — i due .menu (uno per il menu XDG, uno per quello di Plasma) e
# la voce di categoria con nome e descrizione.
put $P 0644 system/etc/xdg/menus/applications-merged/skillfishos.menu etc/xdg/menus/applications-merged/skillfishos.menu
put $P 0644 system/etc/xdg/menus/plasma-applications-merged/skillfishos.menu etc/xdg/menus/plasma-applications-merged/skillfishos.menu
put $P 0644 system/usr/share/desktop-directories/skillfishos.directory usr/share/desktop-directories/skillfishos.directory
ctrl $P "" "SkillFishOS application menu group"

P=skillfish-emulators
# Gli emulatori NON possono viaggiare nella ISO: EmuDeck installa tutto nella
# home dell'utente (flatpak --user e AppImage in ~/Applications), e la ISO
# replica /etc/skel, non la home di chi ha costruito il sistema. Vanno quindi
# reinstallati su ogni macchina, e servono due voci nel menu GIOCHI — che e'
# esattamente dove si va a cercarli e non si trovava niente.
# Due voci e non una perche' fanno cose diverse: EmuDeck configura anche
# cartelle ROM, BIOS e controlli ma nasce per Steam Deck; l'altro prende singoli
# emulatori da Flathub e basta.
put $P 0755 scripts/install-emudeck.sh    usr/local/share/skillfish/install-emudeck.sh
put $P 0755 scripts/install-emulators.sh  usr/local/share/skillfish/install-emulators.sh
put $P 0644 system/usr/share/applications/os.skillfish.emudeck.desktop   usr/share/applications/os.skillfish.emudeck.desktop
put $P 0644 system/usr/share/applications/os.skillfish.emulators.desktop usr/share/applications/os.skillfish.emulators.desktop
ctrl $P "flatpak, curl" "SkillFishOS Emulators - install emulators after the installation"

for P in skillfish-tuner skillfish-hub skillfish-monitor skillfish-kernel-manager skillfish-ai-panel skillfish-base skillfish-console skillfish-dashboard skillfish-theme skillfish-emulators skillfish-iso-mount skillfish-menu skillfishos-archive-keyring; do
  find "$OUT/$P" -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
  # .sources e' l'elenco di lavoro usato per generare il changelog: sta nella
  # radice del pacchetto, quindi finirebbe dentro il .deb come file spurio.
  rm -f "$OUT/$P/.sources"
  dpkg-deb --root-owner-group --build "$OUT/$P" "$OUT/out/${P}_${VER}_all.deb" >/dev/null
done
ls -l "$OUT/out"

echo "== ogni pacchetto ha changelog e copyright? =="
# Debian Policy li rende obbligatori, e fino a oggi NON c'erano: i nostri .deb
# non avevano nemmeno /usr/share/doc/<pkg>/. Qui si verifica che ci siano tutti,
# perche' e' il tipo di cosa che si dimentica al primo pacchetto nuovo.
manca=0
for d in "$OUT"/out/*.deb; do
  p=$(dpkg-deb -f "$d" Package)
  # l'elenco si scrive su file: con `dpkg-deb -c | grep -q` grep esce al primo
  # riscontro, chiude la pipe e dpkg-deb muore di SIGPIPE — con pipefail attivo
  # il risultato e' un falso negativo su un pacchetto perfettamente a posto
  # (successo davvero con skillfish-theme, 839 file).
  dpkg-deb -c "$d" > /tmp/elenco.$$ 2>/dev/null || true
  for f in "usr/share/doc/$p/changelog.Debian.gz" "usr/share/doc/$p/copyright"; do
    grep -qF "$f" /tmp/elenco.$$ || { echo "FAIL $p: manca $f" >&2; manca=1; }
  done
  grep -qF '/.sources' /tmp/elenco.$$ && { echo "FAIL $p: .sources finito dentro il pacchetto" >&2; manca=1; }
  rm -f /tmp/elenco.$$
done
[ "$manca" = 0 ] && echo "OK  tutti i pacchetti hanno changelog e copyright" || exit 1

echo "== content verification (the bogus-deb guard) =="
notcheck() { # come check, ma FALLISCE se il testo e' presente
  dpkg-deb --fsys-tarfile "$OUT/out/$1" | tar -xO "$2" | grep -F "$3" >/dev/null   && { echo "FAIL $1: $2 contiene '$3' e non dovrebbe" >&2; exit 1; }   || echo "OK  $1: $2 non contiene '$3'"; }
# Come check(), ma per un file che deve ESISTERE nella cartella di preparazione
# invece che per una stringa dentro a un file.
deve_esserci() { [ -s "$1" ] && echo "OK  $2" || { echo "FAIL manca: $2 ($1)" >&2; exit 1; }; }
check() { dpkg-deb --fsys-tarfile "$OUT/out/$1" | tar -xO "$2" | grep "$3" >/dev/null \
  && echo "OK  $1: $2 contains '$3'" || { echo "FAIL $1: $2 missing '$3'" >&2; exit 1; }; }
check skillfish-tuner_${VER}_all.deb         ./usr/local/bin/skillfish-tuner-helper  gov-mode
check skillfish-tuner_${VER}_all.deb         ./usr/local/bin/skillfish-tuner         gov_perf
check skillfish-hub_${VER}_all.deb           ./usr/local/bin/skillfish-hub           "return None"
# L'ambito dei flatpak va detto sempre: senza --system, con flathub configurato
# sia a sistema sia per utente, ogni installazione dall'Hub falliva con
# "Remote flathub found in multiple installations".
check skillfish-hub_${VER}_all.deb           ./usr/local/bin/skillfish-hub           '"--system", "flathub"' 
check skillfish-kernel-manager_${VER}_all.deb ./usr/local/bin/skillfish-kernel-manager skillfish
check skillfish-ai-panel_${VER}_all.deb      ./usr/local/bin/skillfish-ai-panel       skillfish
# Il portachiavi deve contenere la chiave GIUSTA: nel repository ne girava una
# RSA che NON firma l'archivio, e chi l'avesse usata si sarebbe trovato apt che
# rifiuta il repository senza capire perche'. L'impronta e' quella della ed25519
# con cui reprepro firma davvero.
# Il portachiavi deve contenere la chiave GIUSTA: nel repository ne girava una
# RSA che NON firma l'archivio, e chi l'avesse usata si sarebbe trovato apt che
# rifiuta il repository senza capire perche'.
#
# Due trappole, in cui sono cascato scrivendo questo controllo:
#  - con pipefail, `... | grep -q` esce al primo riscontro e fa morire dpkg-deb
#    di SIGPIPE: falso negativo su un pacchetto perfetto (la stessa cosa gia'
#    documentata piu' sopra per `dpkg-deb -c`). Si passa da un file temporaneo.
#  - gpg, in forma leggibile a occhio, stampa l'impronta a gruppi di quattro:
#    il confronto non tornerebbe mai. Serve --with-colons.
dpkg-deb --fsys-tarfile "$OUT/out/skillfishos-archive-keyring_${VER}_all.deb" > /tmp/kr.$$ 2>/dev/null || true
tar -xOf /tmp/kr.$$ ./usr/share/keyrings/skillfishos-archive-keyring.gpg > /tmp/krg.$$ 2>/dev/null || true
gpg --show-keys --with-colons /tmp/krg.$$ 2>/dev/null | grep "^fpr" > /tmp/krf.$$ || true
if grep -q "AD1BF591E4DF48164D93BF8A567685099ACF0C94" /tmp/krf.$$; then
  echo "OK  keyring: contiene la chiave che firma davvero l archivio"
else
  echo "FAIL keyring: la chiave non e quella che firma l archivio" >&2
  cat /tmp/krf.$$ >&2 || true
  rm -f /tmp/kr.$$ /tmp/krg.$$ /tmp/krf.$$; exit 1
fi
rm -f /tmp/kr.$$ /tmp/krg.$$ /tmp/krf.$$
check skillfishos-archive-keyring_${VER}_all.deb ./etc/apt/sources.list.d/skillfishos.sources 'Signed-By: /usr/share/keyrings/skillfishos-archive-keyring.gpg'
check skillfishos-archive-keyring_${VER}_all.deb ./etc/apt/sources.list.d/skillfishos.sources 'Suites: aetherium'
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-dp-hotswap.sh compositore
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-freeze-check.sh unclean-shutdown
# Il rilevatore di blocchi decide guardando un marcatore che scrive LUI stesso
# allo spegnimento. Le due righe qui sotto sono quelle che lo rendono possibile:
# senza RemainAfterExit systemd non esegue mai ExecStop, il marcatore non viene
# scritto e ogni avvio denuncia un blocco che non c'e' stato.
check skillfish-base_${VER}_all.deb          ./etc/systemd/system/skillfish-freeze-check.service RemainAfterExit=yes
check skillfish-base_${VER}_all.deb          ./etc/systemd/system/skillfish-freeze-check.service 'ExecStop=/usr/local/bin/skillfish-freeze-check.sh shutdown'
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-core-unlock     0x5A870
check skillfish-base_${VER}_all.deb          ./etc/modules-load.d/skillfish-ntsync.conf ntsync
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-fix-boot-extents sparse=never
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-clean-live-autologin '\[Autologin\]'
# Lo stesso script maschera anche il generatore di getty che live-config-systemd
# si lascia dietro: senza, l'errore compariva 32 volte per avvio su una BC-250
# installata. Il controllo serve perche' e' una riga sola, facile da perdere.
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-clean-live-autologin live-config-getty-generator
# Il gancio DEVE chiamarsi 00-: e' l'unica cosa che lo fa girare prima di dkms.
check skillfish-base_${VER}_all.deb          ./etc/kernel/postinst.d/00-skillfish-nct6687 skillfish-fix-nct6687
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-fix-nct6687 'strscpy(valcp, val, sizeof(valcp))'
# Il rilevatore di snapshot va sospeso durante l'installazione: con snapshot
# gia' presenti sul bersaglio, grub-mkconfig muore con uscita 32 dentro il
# chroot, dove /dev/disk/by-uuid non c'e'. Segnalato da Cyryl Sochacki.
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-grub-btrfs GRUB_BTRFS_DISABLE
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-is-bc250        0x13fe
check skillfish-base_${VER}_all.deb          ./etc/systemd/system/skillfish-sshd-keygen.service ssh-keygen
check skillfish-base_${VER}_all.deb          ./etc/ssh/sshd_config.d/10-skillfish.conf PasswordAuthentication
check skillfish-base_${VER}_all.deb          ./etc/systemd/coredump.conf.d/10-skillfish.conf ExternalSizeMax
# I tre guasti trovati installando la 26.06.4 in macchina virtuale.
# 1. Il servizio degli snapshot deve decidere guardando il filesystem: se torna a
#    fidarsi del solo marcatore, la ISO se lo porta dietro dalla macchina di
#    build e nessuno ha piu' i punti di ripristino.
check    skillfish-base_${VER}_all.deb ./usr/local/bin/skillfish-firstboot-snapshots.sh 'btrfs subvolume show /.snapshots'
notcheck skillfish-base_${VER}_all.deb ./etc/systemd/system/skillfish-firstboot-snapshots.service 'ConditionPathExists=!/var/lib/skillfish/.snapshots-setup-done'
# 2. Il Wake-on-LAN non deve stare dentro la unit: systemd si mangia \K e \S.
check    skillfish-base_${VER}_all.deb ./usr/local/bin/skillfish-wol-arm 'Supports Wake-on'
check    skillfish-base_${VER}_all.deb ./etc/systemd/system/skillfish-wol.service '/usr/local/bin/skillfish-wol-arm'
notcheck skillfish-base_${VER}_all.deb ./etc/systemd/system/skillfish-wol.service 'grep -oP'
# 9. Lo sblocco degli otto core deve chiedere il riavvio SENZA restare in attesa:
#    con `systemctl reboot` e basta, il servizio aspetta systemd e systemd aspetta
#    il servizio — 90 secondi di stallo per avvio, misurati, e un riavvio sporco
#    che non conservava la maschera (quindi due giri invece di uno).
check    skillfish-base_${VER}_all.deb ./usr/local/bin/skillfish-core-unlock 'systemctl --no-block reboot'
# Le guardie che impediscono alla scheda di riavviarsi durante l'installazione
# (issue #31). Senza queste tre righe basta una modifica distratta per
# rimettere in circolo il difetto piu' grave che abbiamo avuto: una ISO che non
# si riesce a installare su hardware vero.
check    skillfish-base_${VER}_all.deb ./etc/systemd/system/skillfish-core-unlock.service 'ConditionKernelCommandLine=!boot=live'
check    skillfish-base_${VER}_all.deb ./etc/systemd/system/skillfish-core-unlock.service 'ConditionPathExists=/etc/skillfish/core-unlock.abilitato'
check    skillfish-base_${VER}_all.deb ./usr/local/bin/skillfish-core-unlock 'core-unlock.abilitato'
# E l'interruttore nel Tuner, che e' l'unico modo che ha l'utente di accenderlo.
check    skillfish-tuner_${VER}_all.deb ./usr/local/bin/skillfish-tuner 'core8_cb'
notcheck skillfish-base_${VER}_all.deb ./usr/local/bin/skillfish-core-unlock 'os.system("systemctl reboot")'
# 7. Il menu di ripristino non deve dipendere da grub-btrfsd, che non lo aggiorna.
check    skillfish-base_${VER}_all.deb ./usr/local/bin/skillfish-snapshot-menu 'grub-mkconfig'
check    skillfish-base_${VER}_all.deb ./etc/apt/apt.conf.d/99-skillfish-snapshots 'DPkg::Post-Invoke'
# 8. Il ripristino permanente: deve spostare anche il sottovolume .snapshots,
#    altrimenti si torna indietro buttando via tutta la cronologia.
check    skillfish-base_${VER}_all.deb ./usr/local/bin/skillfish-rollback 'btrfs subvolume snapshot'
check    skillfish-base_${VER}_all.deb ./usr/local/bin/skillfish-rollback 'mv "$DAPARTE/.snapshots"'
check    skillfish-base_${VER}_all.deb ./usr/local/bin/skillfish-rollback 'annulla|--undo)'
# 4. Lo spegnimento della dashboard non deve stare dentro la unit: il pkill
#    trovava la propria shell e si ammazzava, lasciando il servizio in failed.
check    skillfish-dashboard_${VER}_all.deb ./usr/local/bin/skillfish-dashboard-stop 'ttyd -i lo'
# Il terminale rispondeva 404 perche' il ttyd del pacchetto Debian teneva la
# porta senza -b /terminal. Il postinst lo deve mascherare: se questa riga
# sparisce, il guasto torna e nessuno lo collega alla causa.
grep -q 'mask ttyd.service' "$OUT/skillfish-dashboard/DEBIAN/postinst" \
  && echo "OK  postinst della dashboard: ttyd.service mascherato" \
  || { echo "FATAL: il postinst non maschera ttyd.service" >&2; exit 1; }
check    skillfish-dashboard_${VER}_all.deb ./etc/systemd/system/skillfish-dashboard.service 'ExecStopPost=/usr/local/bin/skillfish-dashboard-stop'
notcheck skillfish-dashboard_${VER}_all.deb ./etc/systemd/system/skillfish-dashboard.service 'ExecStopPost=/bin/sh'
# 5. La tabella ACPI della BC-250 va TOLTA sulle macchine che non lo sono, non
#    solo "non attivata": l'immagine se la porta dietro gia' attiva.
check    skillfish-base_${VER}_all.deb ./usr/local/bin/skillfish-acpi-pstates '  auto)'
# 6. Categorie dei menu: una sola categoria principale, o la voce compare piu' volte.
notcheck skillfish-dashboard_${VER}_all.deb ./usr/share/applications/os.skillfish.remote-manager.desktop 'Categories=System;Settings;Network'
# 3. La guardia hardware deve coprire anche bc250-smu-oc, l'ottavo servizio.
#    Sta nel postinst, che vive nell'archivio di controllo e non in quello dei
#    dati: --fsys-tarfile non lo vedrebbe, serve `dpkg-deb -I`.
if dpkg-deb -I "$OUT/out/skillfish-base_${VER}_all.deb" postinst 2>/dev/null | grep -q 'bc250-smu-oc'; then
  echo "OK  skillfish-base: la guardia hardware copre anche bc250-smu-oc"
else
  echo "FAIL skillfish-base: bc250-smu-oc non e' nell'elenco della guardia hardware" >&2; exit 1
fi
check skillfish-tuner_${VER}_all.deb         ./usr/local/bin/skillfish-tuner          _silicon
check skillfish-console_${VER}_all.deb       ./opt/skillfish/steam-bin/steamos-session-select flatpak-spawn
check skillfish-console_${VER}_all.deb       ./usr/local/bin/skillfish-gaming-mode    /usr/games
check skillfish-monitor_${VER}_all.deb       ./usr/local/bin/skillfish-monitor        SFMON_EXT
check skillfish-dashboard_${VER}_all.deb     ./usr/local/bin/skillfish-dashboardd     "SkillFish Remote"
# Il motore AI non deve piu' puntare a /root: nell'immagine non esiste, e il
# risultato era che su un'installazione fresca non partiva per nessuno.
# ⚠️ Si guarda il CODICE, non i commenti: lo script SPIEGA il vecchio difetto e
#    quindi la stringa /root compare, giustamente, in un commento.
dpkg-deb --fsys-tarfile "$OUT/out/skillfish-ai-panel_${VER}_all.deb"   | tar -xO ./usr/local/bin/skillfish-unsloth 2>/dev/null   | grep -vE '^[[:space:]]*#' | grep -qE '/root/\.unsloth|HOME=/root'   && { echo "FATAL: skillfish-unsloth punta ancora a /root nel codice" >&2; exit 1; }   || echo "OK  skillfish-unsloth: il codice non punta piu' a /root"
check    skillfish-ai-panel_${VER}_all.deb ./usr/local/bin/skillfish-unsloth '127.0.0.1'
dpkg-deb --control "$OUT/out/skillfish-ai-panel_${VER}_all.deb" "$OUT/.ctrl-ai" >/dev/null 2>&1
grep -q 'enable --now skillfish-unsloth' "$OUT/.ctrl-ai/postinst" \
  && echo "OK  skillfish-ai-panel: il postinst abilita skillfish-unsloth.service" \
  || { echo "FATAL: il postinst non abilita skillfish-unsloth.service" >&2; exit 1; }
grep -q 'exit 0' "$OUT/../sfx-src/system/usr/local/bin/skillfish-unsloth" 2>/dev/null || true
rm -rf "$OUT/.ctrl-ai"
check    skillfish-ai-panel_${VER}_all.deb ./usr/local/bin/skillfish-unsloth-update 'install.unsloth.ai'
check    skillfish-ai-panel_${VER}_all.deb ./usr/local/bin/skillfish-unsloth-update 'Desktop/unsloth-studio.desktop'
check skillfish-dashboard_${VER}_all.deb     ./usr/local/bin/skillfish-hub-catalog    AppStream
check skillfish-dashboard_${VER}_all.deb     ./usr/share/skillfish/dashboard/hub.html "SkillFishOS Hub"
# La dashboard web dev'essere in quattro lingue: il dizionario condiviso c'e', e
# le pagine lo agganciano. Senza i18n.js le tre pagine che non caricano app.js
# resterebbero in inglese fisso.
check skillfish-dashboard_${VER}_all.deb     ./usr/share/skillfish/dashboard/i18n.js  'uk:'
check skillfish-dashboard_${VER}_all.deb     ./usr/share/skillfish/dashboard/tuner.html data-i18n
check skillfish-dashboard_${VER}_all.deb     ./usr/share/skillfish/dashboard/app.js   'pl:'
# app.js NON deve contenere S("...": la funzione di traduzione si chiama T().
# I miei script ne avevano scritte 52, ReferenceError alla prima scheda e
# dashboard con la pagina vuota. `node --check` non lo vede: e' sintassi valida.
notcheck skillfish-dashboard_${VER}_all.deb  ./usr/share/skillfish/dashboard/app.js   'S("'
# Il HUD: il lanciatore deve esserci E deve contenere il controllo
# sull'hardware, altrimenti partirebbe su PC dove la finestra collassa a 15x15.
# Il HUD non si tira piu' indietro fuori dalla BC-250: genera la configurazione
# dai sensori che la macchina espone. Qui si controlla che i due pezzi di quel
# meccanismo ci siano davvero nel pacchetto - senza il generatore, skillfish-hud
# ripiegherebbe sulla configurazione di /etc/skel, cablata sulla scheda, e su un
# PC qualunque conky tornerebbe a rimpicciolirsi fino a sparire.
check skillfish-tuner_${VER}_all.deb         ./usr/local/bin/skillfish-hud            skillfish-hud-config
check skillfish-tuner_${VER}_all.deb         ./usr/local/bin/skillfish-hud-config     'cpubar cpu'
# e che i ripieghi generici dei sensori non vengano persi in una riscrittura
check skillfish-tuner_${VER}_all.deb         ./usr/local/bin/skillfish-hud-val        cpu_temp_generico
# L'autostart deve chiamare il percorso assoluto: con "sh -c" e le virgolette,
# KDE lo converte in servizio systemd e $HOME resta letterale.
check skillfish-base_${VER}_all.deb          ./etc/skel/.config/autostart/skillfish-conky.desktop "Exec=/usr/local/bin/skillfish-hud"
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-info           fastfetch
# L'icona dell'Hub: che sia davvero un'immagine e non un file vuoto.
check skillfish-hub_${VER}_all.deb           ./usr/share/icons/hicolor/scalable/apps/skillfish-hub.svg "svg"
# Gli emulatori: il repository giusto e' emudeck-electron, non dragoonDorise —
# quest'ultimo non ha allegati nelle release e lo scaricamento fallirebbe.
check skillfish-emulators_${VER}_all.deb     ./usr/local/share/skillfish/install-emudeck.sh   emudeck-electron
check skillfish-emulators_${VER}_all.deb     ./usr/local/share/skillfish/install-emulators.sh flathub
# I due pacchetti rientrati oggi nella catena automatica: erano fermi a 26.06
# perche' uno stava nel vecchio script e l'altro in nessuno.
check skillfish-iso-mount_${VER}_all.deb    ./usr/local/bin/skillfish-iso-mount              udisks
# Si cerca il TESTO polacco, non la chiave "Comment[pl]": quella passa a grep
# come espressione regolare, dove [pl] vale "un carattere fra p e l" e non
# combacia mai. Cercare la traduzione vera verifica anche di piu'.
check skillfish-menu_${VER}_all.deb         ./usr/share/desktop-directories/skillfishos.directory "Narzędzia SkillFishOS"
# Nella barra deve esserci il NOSTRO Hub. Il collegamento a Discover era rimasto
# solo nello skel, quindi non si vedeva sulla board — dove il pannello era gia'
# stato sistemato a mano — ma lo ereditava chiunque installasse da ISO.
check skillfish-theme_${VER}_all.deb         ./etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc os.skillfish.hub.desktop
# L'icona del menu va per NOME: da Plasma 6.7.4 un percorso assoluto lascia il
# pulsante vuoto, senza dire niente nel giornale. Facile da riscrivere per
# sbaglio salvando il pannello dall'interfaccia, quindi lo si controlla qui.
check skillfish-theme_${VER}_all.deb         ./etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc '^icon=skillfish-tuner'
# ...e l'icona con quel nome deve stare DENTRO al nostro tema. Se manca, KDE
# taglia dopo il trattino, trova "skillfish" nel tema e disegna il pesce
# stilizzato al posto di quello di ottone, senza dire niente a nessuno.
deve_esserci "$OUT/skillfish-theme/usr/share/icons/SkillFishSteampunk/256x256/apps/skillfish-tuner.png" "skillfish-theme: il pesce del menu e' dentro al tema"
# La schermata di accesso non deve piu' dire "Accedi" a un polacco: si controlla
# che il testo passi dalla funzione di traduzione e non sia piu' una costante.
check skillfish-theme_${VER}_all.deb         ./usr/share/sddm/themes/skillfish-brass/Main.qml "root.tr(root.txtLogin)"
# I diacritici polacchi nei preset: "Wydajnosc" non esiste, si scrive
# "Wydajnosc" con la n accentata. Senza questo controllo tornerebbero a perdersi.
check skillfish-tuner_${VER}_all.deb         ./usr/share/skillfish/tuner-presets.json "Wydajność"
check skillfish-theme_${VER}_all.deb         ./usr/share/icons/SkillFishSteampunk/index.theme        SkillFish
# guard: the icon must paint with its OWN gradient — a dangling cross-icon ref
# renders as an empty frame on qt6-svg >= 6.10.2-9 (see fix-icon-gradient-refs.py)
check skillfish-theme_${VER}_all.deb ./usr/share/icons/SkillFishSteampunk/scalable/actions/document-open.svg document_open_copper
check skillfish-theme_${VER}_all.deb ./usr/share/wallpapers/SkillFishOS/metadata.json SkillFishOS
check skillfish-theme_${VER}_all.deb ./etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc usr/share/wallpapers/SkillFishOS
check skillfish-theme_${VER}_all.deb ./usr/local/bin/skillfish-first-login-wallpaper plasma-apply-wallpaperimage
check skillfish-theme_${VER}_all.deb ./usr/share/plasma/look-and-feel/org.skillfish.steampunk/contents/defaults usr/share/wallpapers/SkillFishOS
echo "ALL DEBS VERIFIED"

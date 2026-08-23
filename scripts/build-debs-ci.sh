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

ctrl() { # ctrl <pkg> <depends> <desc-first-line> [<corpo>]
  mkdir -p "$OUT/$1/DEBIAN"
  docs "$1"
  # ⚠️ IL CORPO DELLA DESCRIZIONE LO LEGGONO L'HUB E `apt show`.
  # Fino al 22/08 qui c'era una riga sola, «built from git by CI»: chi apriva
  # la scheda di un nostro pacchetto leggeva soltanto che era stato compilato.
  # Nel control ogni riga del corpo va rientrata di uno spazio e le righe
  # vuote diventano un punto: sed fa esattamente quello.
  { printf 'Package: %s\nVersion: %s\nArchitecture: all\nMaintainer: SkillFishOS <info@skillfishos.com>\nDepends: %s\nSection: utils\nPriority: optional\nHomepage: https://skillfishos.com\nDescription: %s\n' \
      "$1" "$VER" "$2" "$3"
    if [ -n "${4:-}" ]; then
      printf '%s\n' "$4" | sed 's/^[[:space:]]*$/./; s/^/ /'
      printf ' .\n Part of SkillFishOS.\n'
    else
      printf ' Part of SkillFishOS.\n'
    fi
  } > "$OUT/$1/DEBIAN/control"
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
# I sensori della scheda madre. Sta nel pacchetto del HUD per lo stesso
# motivo degli helper qui sotto: e' cio' che rende visibili le ventole su un
# PC qualunque, dove i chip Super-I/O sono su bus ISA e nessun driver si
# carica da solo. Prima non era in NESSUN pacchetto - stava solo nel git e
# sulla scheda, copiato a mano - quindi su una macchina installata non
# esisteva, e con lui sparivano contagiri, tensioni e i ripieghi del HUD.
put $P 0755 system/usr/local/bin/skillfish-sensori usr/local/bin/skillfish-sensori
put $P 0644 system/etc/systemd/system/skillfish-sensori.service etc/systemd/system/skillfish-sensori.service
put $P 0755 system/usr/local/bin/skillfish-hud-val usr/local/bin/skillfish-hud-val
put $P 0755 system/usr/local/bin/skillfish-hud-config usr/local/bin/skillfish-hud-config
put $P 0755 system/usr/local/bin/skillfish-hud-bt usr/local/bin/skillfish-hud-bt
# ⚠️ Le barre dei thread NON stanno piu' nella configurazione di conky: le
# stampa questo, a ogni giro, cosi' seguono i core che si accendono e si
# spengono. Se manca dal pacchetto, la configurazione chiama un comando che
# non c'e' e al posto delle barre resta una riga vuota.
put $P 0755 system/usr/local/bin/skillfish-hud-cpubars usr/local/bin/skillfish-hud-cpubars
# Il lanciatore del HUD sta qui e non in un pacchetto suo perche' legge i due
# helper qui sopra: separarli permetterebbe di installarlo senza i sensori che
# gli servono. Deve essere un file eseguibile e non un comando dentro il
# .desktop: KDE converte l'autostart in un servizio systemd e in quel passaggio
# $HOME resta letterale, quindi conky non trovava la configurazione.
put $P 0755 system/usr/local/bin/skillfish-hud     usr/local/bin/skillfish-hud
# Il configuratore del HUD. Sta qui e non in un pacchetto suo perche' senza
# skillfish-hud-config e skillfish-hud-val non avrebbe niente da configurare
# ne' da mostrare in anteprima.
put $P 0755 apps/hud/skillfish-hud-editor usr/local/bin/skillfish-hud-editor
put $P 0644 system/usr/share/applications/os.skillfish.hud.desktop usr/share/applications/os.skillfish.hud.desktop
put $P 0644 system/usr/share/icons/hicolor/48x48/apps/skillfish-hud.png usr/share/icons/hicolor/48x48/apps/skillfish-hud.png
put $P 0644 system/usr/share/icons/hicolor/128x128/apps/skillfish-hud.png usr/share/icons/hicolor/128x128/apps/skillfish-hud.png
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfish-hud.png usr/share/icons/hicolor/256x256/apps/skillfish-hud.png
put $P 0644 system/usr/share/icons/hicolor/scalable/apps/skillfish-hud.svg usr/share/icons/hicolor/scalable/apps/skillfish-hud.svg
put $P 0644 system/usr/share/skillfish/tuner-presets.json usr/share/skillfish/tuner-presets.json
put $P 0644 system/usr/share/applications/os.skillfish.Tuner.desktop usr/share/applications/os.skillfish.Tuner.desktop
put $P 0644 system/usr/share/icons/hicolor/scalable/apps/skillfish-tuner.svg usr/share/icons/hicolor/scalable/apps/skillfish-tuner.svg
put $P 0644 system/usr/share/icons/hicolor/48x48/apps/skillfish-tuner.png usr/share/icons/hicolor/48x48/apps/skillfish-tuner.png
put $P 0644 system/usr/share/icons/hicolor/128x128/apps/skillfish-tuner.png usr/share/icons/hicolor/128x128/apps/skillfish-tuner.png
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfish-tuner.png usr/share/icons/hicolor/256x256/apps/skillfish-tuner.png
put $P 0644 system/etc/systemd/system/skillfish-cu.service etc/systemd/system/skillfish-cu.service
# umr NON e' nostro: e' di AMD, licenza MIT, e senza di lui skillfish-cu non
# instrada niente. Prima non lo spediva nessun pacchetto e stava nelle immagini
# solo perche' la ISO clona la scheda di sviluppo: chi installava i .deb altrove,
# o costruiva la ISO con live-build, si ritrovava il pannello delle CU che
# falliva senza spiegazione. Ricostruito senza LLVM e senza GUI per non
# dipendere da un soname che in sid cambia ogni pochi mesi.
put $P 0755 vendor/umr/umr     usr/local/bin/umr
put $P 0644 vendor/umr/LICENSE usr/share/doc/skillfish-tuner/umr-LICENSE
opt $P 0644 system/usr/share/polkit-1/actions/os.skillfish.tuner.policy usr/share/polkit-1/actions/os.skillfish.tuner.policy
shot $P apps/tuner/os.skillfish.Tuner.metainfo.xml
# Il HUD viaggia dentro a skillfish-tuner, e la sua scheda pure.
shot $P apps/hud/os.skillfish.hud.metainfo.xml
ctrl $P "python3, python3-pyqt6, polkitd | policykit-1, skillfish-base, libncurses6, libtinfo6, libpciaccess0, zlib1g" "SkillFishOS Tuner - BC-250 hardware control GUI" \
  "Sets the CPU and GPU clocks, the voltage offset, how many compute units are
in use and how much memory the graphics take. Presets from quiet to full, and
a wizard that finds what this chip holds. Also brings the HUD configurator."
# ⚠️ Dopo ctrl, non prima: ctrl() scrive un postinst predefinito e lo
# sovrascriverebbe. Qui si aggiunge l'accensione del servizio dei sensori,
# come si fa gia' per skillfish-unsloth.
printf '#!/bin/sh\nset -e\nupdate-desktop-database -q 2>/dev/null || true\ngtk-update-icon-cache -q -f /usr/share/icons/hicolor 2>/dev/null || true\nappstreamcli refresh-cache --force >/dev/null 2>&1 || true\nif [ -d /run/systemd/system ]; then\n  systemctl daemon-reload || true\n  systemctl enable --now skillfish-sensori.service 2>/dev/null || true\nfi\nexit 0\n' > "$OUT/$P/DEBIAN/postinst"
chmod 0755 "$OUT/$P/DEBIAN/postinst"

P=skillfish-hub
put $P 0755 apps/hub/skillfish-hub        usr/local/bin/skillfish-hub
put $P 0755 apps/hub/skillfish-hub-helper usr/local/bin/skillfish-hub-helper
# La seconda porta e il motore che condividono. ⚠️ Sono programmi separati
# perche' polkit lega l'autorizzazione al percorso: una regola per quello che
# arriva dai nostri repository, una piu' severa per i file presi da fuori.
put $P 0755 apps/hub/skillfish-hub-local usr/local/bin/skillfish-hub-local
put $P 0644 system/usr/local/lib/skillfish/hub-comune.sh usr/local/lib/skillfish/hub-comune.sh
put $P 0755 system/usr/local/lib/skillfish/hub-run usr/local/lib/skillfish/hub-run
put $P 0644 system/usr/share/polkit-1/actions/os.skillfish.hub.policy usr/share/polkit-1/actions/os.skillfish.hub.policy
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
# L'AVVISATORE E I DUE TIMER.
# ⚠️ Sono la meta' che mancava per fare a meno di Discover. L'Hub gli
# aggiornamenti li vede benissimo — ma solo quando lo apri, e nessuno apre un
# centro software per sapere se ha qualcosa da fare. Senza l'avviso, togliere
# Discover vorrebbe dire togliere l'unica cosa che avvisa l'utente.
# Sono due timer separati perche' fanno due mestieri diversi: contare vuol dire
# prendere il lock di apt (e si fa da root, una volta al giorno), avvisare vuol
# dire parlare col bus della sessione (e si fa da utente, o la notifica non
# arriva da nessuna parte).
# Il blocco che tiene Discover fuori: sta qui perche' e' l'Hub a prenderne il
# posto, e va tolto insieme all'Hub se un giorno si torna indietro.
put $P 0644 system/etc/apt/preferences.d/skillfish-no-discover.pref etc/apt/preferences.d/skillfish-no-discover.pref
put $P 0755 apps/hub/skillfish-hub-notify usr/local/bin/skillfish-hub-notify
put $P 0644 system/etc/systemd/system/skillfish-hub-refresh.service etc/systemd/system/skillfish-hub-refresh.service
put $P 0644 system/etc/systemd/system/skillfish-hub-refresh.timer   etc/systemd/system/skillfish-hub-refresh.timer
put $P 0644 system/usr/lib/systemd/user/skillfish-hub-notify.service usr/lib/systemd/user/skillfish-hub-notify.service
put $P 0644 system/usr/lib/systemd/user/skillfish-hub-notify.timer   usr/lib/systemd/user/skillfish-hub-notify.timer
shot $P apps/hub/os.skillfish.hub.metainfo.xml
ctrl $P "python3, python3-pyqt6, python3-apt, gir1.2-appstream-1.0, appstream, curl, polkitd | policykit-1, fwupd, libnotify-bin, systemd" "SkillFishOS Hub - software centre for APT, Flatpak, Snap and firmware" \
  "One place for apt, Flatpak, Snap and device firmware: search, categories, app
pages, sources. Updates keep running if the window closes, because the work is
handed to systemd. Opens .deb and .flatpakref files, and tells you when
updates are waiting."
# ⚠️ Dopo ctrl, che scrive un postinst suo e lo sovrascriverebbe.
cat > "$OUT/$P/DEBIAN/postinst" <<'POSTINST'
#!/bin/sh
set -e
update-desktop-database -q 2>/dev/null || true
gtk-update-icon-cache -q -f /usr/share/icons/hicolor 2>/dev/null || true
if [ -d /run/systemd/system ]; then
  systemctl daemon-reload || true
  systemctl enable --now skillfish-hub-refresh.timer 2>/dev/null || true
  # --global: l'avviso vale per TUTTI gli utenti, compresi quelli creati
  # dopo. Abilitarlo per l'utente corrente non servirebbe a niente:
  # durante l'installazione l'utente corrente e' root, che il desktop non
  # ce l'ha.
  systemctl --global enable skillfish-hub-notify.timer 2>/dev/null || true
  # Il primo conteggio subito e in sottofondo, per non far aspettare fino a
  # domani chi ha appena installato.
  systemctl start --no-block skillfish-hub-refresh.service 2>/dev/null || true
fi
exit 0
POSTINST
chmod 0755 "$OUT/$P/DEBIAN/postinst"

P=skillfish-fan
# SkillFishOS Fan Control. Tre programmi, e non e' una complicazione gratuita:
#   skillfish-fand        gira sempre da root e muove la ventola. Il
#                         raffreddamento non puo' dipendere da una finestra
#                         aperta, ed e' anche l'emergenza termica.
#   skillfish-fan         la finestra, che gira da utente e non muove niente.
#   skillfish-fan-helper  l'unico che scrive, e che non si fida di cio' che
#                         gli arriva: rifa' la configurazione campo per campo.
put $P 0755 apps/fan/skillfish-fan               usr/local/bin/skillfish-fan
put $P 0755 apps/fan/skillfish-fand              usr/local/bin/skillfish-fand
put $P 0755 apps/fan/skillfish-fan-helper        usr/local/bin/skillfish-fan-helper
put $P 0644 system/etc/systemd/system/skillfish-fand.service etc/systemd/system/skillfish-fand.service
put $P 0644 system/usr/share/polkit-1/actions/os.skillfish.fan.policy usr/share/polkit-1/actions/os.skillfish.fan.policy
put $P 0644 system/usr/share/applications/os.skillfish.fan.desktop usr/share/applications/os.skillfish.fan.desktop
put $P 0644 system/usr/share/icons/hicolor/48x48/apps/skillfish-fan.png usr/share/icons/hicolor/48x48/apps/skillfish-fan.png
put $P 0644 system/usr/share/icons/hicolor/128x128/apps/skillfish-fan.png usr/share/icons/hicolor/128x128/apps/skillfish-fan.png
put $P 0644 system/usr/share/skillfish/ventola-giochi.json usr/share/skillfish/ventola-giochi.json
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfish-fan.png usr/share/icons/hicolor/256x256/apps/skillfish-fan.png
put $P 0644 system/usr/share/icons/hicolor/scalable/apps/skillfish-fan.svg usr/share/icons/hicolor/scalable/apps/skillfish-fan.svg
# ⚠️ La dipendenza da skillfish-base non e' decorativa: li' dentro c'e' hwmon.py,
# senza il quale il demone esce al primo giro. Meglio che lo sappia apt.
# ⚠️ La scheda AppStream: senza, nell'Hub questa applicazione mostra solo la
# riga del control, nessuno screenshot e nessuna novita'.
shot $P apps/fan/os.skillfish.fan.metainfo.xml
ctrl $P "python3, python3-pyqt6, skillfish-base, polkitd | policykit-1" "SkillFishOS Fan Control - fan curve with anticipation" \
  "The fan curve, applied every second by a controller that runs with or without
the window. It watches how fast the temperature climbs, and the watts on the
BC-250, to start early. The emergency threshold cannot be switched off."
# ⚠️ Dopo ctrl, che scrive un postinst suo e lo sovrascriverebbe.
# Il servizio si accende all'installazione anche se non e' ancora configurato:
# con `attivo` a falso non tocca la ventola, ma pubblica le letture, e senza di
# lui la finestra si aprirebbe vuota con scritto che non gira niente.
printf '#!/bin/sh\nset -e\nupdate-desktop-database -q 2>/dev/null || true\ngtk-update-icon-cache -q -f /usr/share/icons/hicolor 2>/dev/null || true\nappstreamcli refresh-cache --force >/dev/null 2>&1 || true\nif [ -d /run/systemd/system ]; then\n  systemctl daemon-reload || true\n  systemctl enable --now skillfish-fand.service 2>/dev/null || true\nfi\nexit 0\n' > "$OUT/$P/DEBIAN/postinst"
chmod 0755 "$OUT/$P/DEBIAN/postinst"
# ⚠️ prerm: disinstallando, la ventola deve tornare al firmware. Senza questo
# resterebbe inchiodata sull'ultimo valore scritto da noi, su una macchina da
# cui il programma e' appena stato tolto — cioe' senza piu' nessuno che la
# guardi. E' il caso peggiore che ci sia.
printf '#!/bin/sh\nset -e\nif [ -d /run/systemd/system ]; then\n  systemctl disable --now skillfish-fand.service 2>/dev/null || true\nfi\nexit 0\n' > "$OUT/$P/DEBIAN/prerm"
chmod 0755 "$OUT/$P/DEBIAN/prerm"

P=skillfish-monitor
put $P 0755 apps/monitor/skillfish-monitor usr/local/bin/skillfish-monitor
put $P 0644 system/usr/share/applications/os.skillfish.monitor.desktop usr/share/applications/os.skillfish.monitor.desktop
put $P 0644 system/usr/share/icons/hicolor/scalable/apps/skillfish-monitor.svg usr/share/icons/hicolor/scalable/apps/skillfish-monitor.svg
put $P 0644 system/usr/share/icons/hicolor/48x48/apps/skillfish-monitor.png usr/share/icons/hicolor/48x48/apps/skillfish-monitor.png
put $P 0644 system/usr/share/icons/hicolor/128x128/apps/skillfish-monitor.png usr/share/icons/hicolor/128x128/apps/skillfish-monitor.png
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfish-monitor.png usr/share/icons/hicolor/256x256/apps/skillfish-monitor.png
put $P 0644 system/usr/share/mime/packages/os.skillfish.monitor.xml usr/share/mime/packages/os.skillfish.monitor.xml
shot $P apps/monitor/os.skillfish.monitor.metainfo.xml
ctrl $P "python3, python3-pyqt6" "SkillFishOS Monitor - live sensor charts + .sfmon benchmark analyzer" \
  "Live charts of temperatures, clocks, voltage, watts, load and fan speed. Press
record and the session goes to a .sfmon file you can reopen and walk through
second by second."
# monitor ships a MIME type (.sfmon recordings) → also refresh the shared-mime db
printf '#!/bin/sh\nset -e\nupdate-mime-database /usr/share/mime >/dev/null 2>&1 || true\nupdate-desktop-database -q 2>/dev/null || true\nappstreamcli refresh-cache --force >/dev/null 2>&1 || true\nexit 0\n' > "$OUT/$P/DEBIAN/postinst"
chmod 0755 "$OUT/$P/DEBIAN/postinst"

P=skillfish-kernel-manager
put $P 0755 apps/kernel-manager/skillfish-kernel-manager usr/local/bin/skillfish-kernel-manager
put $P 0755 apps/kernel-manager/skillfish-kernel-helper  usr/local/bin/skillfish-kernel-helper
put $P 0644 system/usr/share/applications/os.skillfish.kernel.desktop usr/share/applications/os.skillfish.kernel.desktop
put $P 0644 system/usr/share/icons/hicolor/scalable/apps/skillfish-kernel.svg usr/share/icons/hicolor/scalable/apps/skillfish-kernel.svg
put $P 0644 system/usr/share/icons/hicolor/48x48/apps/skillfish-kernel.png usr/share/icons/hicolor/48x48/apps/skillfish-kernel.png
put $P 0644 system/usr/share/icons/hicolor/128x128/apps/skillfish-kernel.png usr/share/icons/hicolor/128x128/apps/skillfish-kernel.png
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfish-kernel.png usr/share/icons/hicolor/256x256/apps/skillfish-kernel.png
shot $P apps/kernel-manager/os.skillfish.kernel.metainfo.xml
ctrl $P "python3, python3-pyqt6, polkitd | policykit-1" "SkillFishOS Kernel Manager" \
  "Shows the kernels installed, which one is running and which one GRUB will pick
next. Choose the next boot, remove the ones you no longer want."

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
put $P 0644 system/usr/share/icons/hicolor/scalable/apps/skillfish-ai.svg usr/share/icons/hicolor/scalable/apps/skillfish-ai.svg
put $P 0644 system/usr/share/icons/hicolor/48x48/apps/skillfish-ai.png usr/share/icons/hicolor/48x48/apps/skillfish-ai.png
put $P 0644 system/usr/share/icons/hicolor/128x128/apps/skillfish-ai.png usr/share/icons/hicolor/128x128/apps/skillfish-ai.png
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfish-ai.png usr/share/icons/hicolor/256x256/apps/skillfish-ai.png
shot $P apps/ai-panel/os.skillfish.ai.metainfo.xml
ctrl $P "python3, python3-pyqt6, polkitd | policykit-1" "SkillFish AI - on-device LLM control panel" \
  "Downloads a language model and runs it on the integrated GPU, about five times
faster than on the processor. Questions and answers stay on this machine."
# ⚠️ L'unita' del motore AI veniva spedita e non la accendeva nessuno: sulla
# scheda risultava attiva solo perche' l'avevo abilitata a mano, e nella ISO ci
# finiva per clonazione. Chi installa da apt si ritrovava il file dell'unita' e
# nessun servizio. "--now" e' sicuro: skillfish-unsloth esce con 0, non con 1,
# quando Unsloth non e' installato, quindi niente ciclo di riavvii.
printf '#!/bin/sh\nset -e\nupdate-desktop-database -q 2>/dev/null || true\ngtk-update-icon-cache -q -f /usr/share/icons/hicolor 2>/dev/null || true\nappstreamcli refresh-cache --force >/dev/null 2>&1 || true\nif [ -d /run/systemd/system ]; then\n  systemctl daemon-reload || true\n  systemctl enable --now skillfish-unsloth.service 2>/dev/null || true\nfi\nexit 0\n' > "$OUT/$P/DEBIAN/postinst"
chmod 0755 "$OUT/$P/DEBIAN/postinst"

P=skillfishos-archive-keyring
# La scheda AppStream: senza, la descrizione esiste solo in inglese,
# perche' apt la tiene nel control e li' la lingua e' una sola.
shot $P apps/keyring/os.skillfish.archive-keyring.metainfo.xml
put $P 0644 system/usr/share/icons/hicolor/scalable/apps/skillfishos-archive-keyring.svg usr/share/icons/hicolor/scalable/apps/skillfishos-archive-keyring.svg
put $P 0644 system/usr/share/icons/hicolor/48x48/apps/skillfishos-archive-keyring.png usr/share/icons/hicolor/48x48/apps/skillfishos-archive-keyring.png
put $P 0644 system/usr/share/icons/hicolor/128x128/apps/skillfishos-archive-keyring.png usr/share/icons/hicolor/128x128/apps/skillfishos-archive-keyring.png
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfishos-archive-keyring.png usr/share/icons/hicolor/256x256/apps/skillfishos-archive-keyring.png
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
ctrl $P "gnupg | gpgv" "SkillFishOS archive keyring and APT source" \
  "The signing key of our archive and the apt source that uses it. Without it apt
cannot check where a SkillFishOS package came from."

P=skillfish-base
# La scheda AppStream: senza, la descrizione esiste solo in inglese,
# perche' apt la tiene nel control e li' la lingua e' una sola.
shot $P apps/base/os.skillfish.base.metainfo.xml
put $P 0644 system/usr/share/icons/hicolor/scalable/apps/skillfish-base.svg usr/share/icons/hicolor/scalable/apps/skillfish-base.svg
put $P 0644 system/usr/share/icons/hicolor/48x48/apps/skillfish-base.png usr/share/icons/hicolor/48x48/apps/skillfish-base.png
put $P 0644 system/usr/share/icons/hicolor/128x128/apps/skillfish-base.png usr/share/icons/hicolor/128x128/apps/skillfish-base.png
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfish-base.png usr/share/icons/hicolor/256x256/apps/skillfish-base.png
# Script nostri che stavano solo dentro l'immagine e non in un pacchetto: una
# correzione a uno di questi non poteva raggiungere chi ha gia' installato.
put $P 0755 system/usr/local/bin/skillfish-dp-hotswap.sh    usr/local/bin/skillfish-dp-hotswap.sh
put $P 0755 system/usr/local/bin/skillfish-thermal-guard.sh usr/local/bin/skillfish-thermal-guard.sh
put $P 0755 system/usr/local/bin/skillfish-gpu-util.sh      usr/local/bin/skillfish-gpu-util.sh
put $P 0755 system/usr/local/bin/skillfish-kde-firstrun.sh  usr/local/bin/skillfish-kde-firstrun.sh
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
put $P 0755 system/usr/local/bin/skillfish-flatpak-rimedi           usr/local/bin/skillfish-flatpak-rimedi
put $P 0755 system/usr/local/bin/skillfish-games-subvolume         usr/local/bin/skillfish-games-subvolume
put $P 0755 system/usr/local/bin/skillfish-live-no-lock             usr/local/bin/skillfish-live-no-lock
# Dizionario condiviso delle traduzioni: un file per lingua, comune a tutte le
# app. Serve le lingue NUOVE (ru, es, pt...); italiano, polacco e ucraino
# restano dentro le app, dove hanno le sfumature per contesto.
put $P 0644 system/usr/share/skillfish/i18n.py                       usr/share/skillfish/i18n.py
# I dati del HUD, condivisi fra la finestra e il Remote Manager: sta qui per
# lo stesso motivo di i18n.py, ed e' per questo che i due pacchetti che lo
# usano dipendono da skillfish-base.
put $P 0644 system/usr/share/skillfish/hud_dati.py                   usr/share/skillfish/hud_dati.py
# Il pallino «?» condiviso: le spiegazioni stanno dietro, non nella pagina.
# Sta accanto a i18n.py perche' e' la stessa cosa — un modulo che tutte le
# applicazioni importano da /usr/share/skillfish.
put $P 0644 system/usr/share/skillfish/aiuto.py                      usr/share/skillfish/aiuto.py
# Il riconoscimento dei sensori veri, condiviso come i due qui sopra: lo usa
# il controllo ventola e sono gli stessi canali che leggono HUD e Monitor.
put $P 0644 system/usr/share/skillfish/hwmon.py                      usr/share/skillfish/hwmon.py
for _l in system/usr/share/skillfish/i18n/*.json; do
  put $P 0644 "$_l" "usr/share/skillfish/i18n/$(basename "$_l")"
done
put $P 0644 system/etc/systemd/system/skillfish-live-no-lock.service etc/systemd/system/skillfish-live-no-lock.service
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
# Spegne l'avvio automatico di Blueman: e' l'applet Bluetooth di GTK e Plasma ha
# gia' il suo, a tema e nel vassoio. Con tutti e due accesi ne compaiono DUE, e
# quello di Blueman passa da xembedsniproxy — fondo scuro quadrato, icona sua.
# ⚠️ Non si disinstalla niente: si scrive Hidden=true in un file dell'utente, che
# ha la precedenza su /etc/xdg/autostart. Chi vuole Blueman toglie quel file.
put $P 0644 system/etc/skel/.config/autostart/blueman.desktop etc/skel/.config/autostart/blueman.desktop
# skillfish-info: fastfetch in un terminale che resta aperto. Anche questi due
# non appartenevano a nessun pacchetto. Il comando sta in uno script perche' nel
# campo Exec di un .desktop "%s" e' un codice di sostituzione riservato e il "$"
# va raddoppiato: desktop-file-validate rifiutava la vecchia riga.
put $P 0755 system/usr/local/bin/skillfish-info                       usr/local/bin/skillfish-info
put $P 0644 system/usr/share/applications/skillfish-info.desktop      usr/share/applications/skillfish-info.desktop
put $P 0644 system/usr/share/icons/hicolor/scalable/apps/skillfish-info.svg usr/share/icons/hicolor/scalable/apps/skillfish-info.svg
put $P 0644 system/usr/share/icons/hicolor/48x48/apps/skillfish-info.png usr/share/icons/hicolor/48x48/apps/skillfish-info.png
put $P 0644 system/usr/share/icons/hicolor/128x128/apps/skillfish-info.png usr/share/icons/hicolor/128x128/apps/skillfish-info.png
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfish-info.png usr/share/icons/hicolor/256x256/apps/skillfish-info.png
put $P 0755 system/usr/local/bin/skillfish-acpi-pstates               usr/local/bin/skillfish-acpi-pstates
put $P 0644 system/usr/share/skillfish/acpi/SSDT-PST.aml              usr/share/skillfish/acpi/SSDT-PST.aml
put $P 0644 system/usr/share/skillfish/acpi/SSDT-PST.dsl              usr/share/skillfish/acpi/SSDT-PST.dsl
put $P 0644 system/usr/share/skillfish/acpi/SSDT-CST.aml              usr/share/skillfish/acpi/SSDT-CST.aml
put $P 0644 system/usr/share/skillfish/acpi/SSDT-CST.dsl              usr/share/skillfish/acpi/SSDT-CST.dsl
ctrl $P "systemd, libnotify-bin, python3, cpio, locales" "SkillFishOS base - hardware watchdog + freeze detector + 8-core unlock" \
  "The watchdog that reboots the board if it stops answering, the freeze detector,
the 8-core unlock, the shared translation dictionary and the sensor tables the
applications read."
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
  # Nella live il blocco schermo chiude fuori l'utente (password vuota):
  # il servizio si accende sempre e non fa niente sul sistema installato,
  # dove /run/live/medium non esiste.
  systemctl enable skillfish-live-no-lock.service || true
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
  # Rimedi ai flatpak che su questo hardware non partono (per ora ProtonUp-Qt,
  # che aborta all'avvio perche' GLX non ha configurazioni a buffer singolo).
  /usr/local/bin/skillfish-flatpak-rimedi >/dev/null 2>&1 || true
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

# HUD: niente piu' migrazione delle barre a mano.
# Serviva quando le barre stavano scritte nella configurazione: passando da 6
# a 8 core andavano riscritte le due righe. Da skillfish-hud-config v11 le
# barre non stanno piu' li' - le stampa skillfish-hud-cpubars a ogni giro di
# conky - e una configurazione piu' vecchia della v11 viene rigenerata da
# skillfish-hud al primo avvio, grazie alla firma del generatore. Riscrivere
# righe che non esistono piu' non farebbe danno, ma direbbe una bugia a chi
# legge il codice.

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
# La scheda AppStream: senza, la descrizione esiste solo in inglese,
# perche' apt la tiene nel control e li' la lingua e' una sola.
shot $P apps/console/os.skillfish.console.metainfo.xml
put $P 0644 system/usr/share/icons/hicolor/scalable/apps/skillfish-console.svg usr/share/icons/hicolor/scalable/apps/skillfish-console.svg
put $P 0644 system/usr/share/icons/hicolor/48x48/apps/skillfish-console.png usr/share/icons/hicolor/48x48/apps/skillfish-console.png
put $P 0644 system/usr/share/icons/hicolor/128x128/apps/skillfish-console.png usr/share/icons/hicolor/128x128/apps/skillfish-console.png
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfish-console.png usr/share/icons/hicolor/256x256/apps/skillfish-console.png
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
ctrl $P "gamescope, flatpak" "SkillFishOS Console - SteamOS-style Big Picture session" \
  "A session that opens straight into a full-screen interface driven with a
controller. Separate from the desktop session, chosen at login."
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
put $P 0644 apps/dashboard/web/hud.html    usr/share/skillfish/dashboard/hud.html
# Il modulo Ventola del Remote Manager. ⚠️ Non rifa' il controllo: legge
# quello che skillfish-fand pubblica e scrive dal suo helper. Due controllori
# sullo stesso PWM li abbiamo gia' avuti una volta, e si vedeva.
put $P 0644 apps/dashboard/web/ventola.html usr/share/skillfish/dashboard/ventola.html
# La favicon delle pagine della dashboard: la stessa del sito. Senza questa
# riga la pagina la chiede e prende un 404, che nella scheda del browser si
# vede come icona vuota — cioe' come prima.
put $P 0644 apps/dashboard/web/badge.png   usr/share/skillfish/dashboard/badge.png
put $P 0644 system/etc/skillfish/dashboard.json usr/share/skillfish/dashboard-default.json
put $P 0644 system/etc/systemd/system/skillfish-dashboard.service etc/systemd/system/skillfish-dashboard.service
shot $P apps/dashboard/os.skillfish.remote-manager.metainfo.xml
put $P 0644 system/usr/share/applications/os.skillfish.remote-manager.desktop usr/share/applications/os.skillfish.remote-manager.desktop
put $P 0644 system/usr/share/icons/hicolor/scalable/apps/skillfish-remote.svg usr/share/icons/hicolor/scalable/apps/skillfish-remote.svg
put $P 0644 system/usr/share/icons/hicolor/48x48/apps/skillfish-remote.png usr/share/icons/hicolor/48x48/apps/skillfish-remote.png
put $P 0644 system/usr/share/icons/hicolor/128x128/apps/skillfish-remote.png usr/share/icons/hicolor/128x128/apps/skillfish-remote.png
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfish-remote.png usr/share/icons/hicolor/256x256/apps/skillfish-remote.png
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
Depends: python3, python3-pyqt6, python3-apt, gir1.2-appstream-1.0, appstream, curl, openssl, polkitd | policykit-1, skillfish-base
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
 native Remote Manager toggle app.
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
# La scheda AppStream: senza, la descrizione esiste solo in inglese,
# perche' apt la tiene nel control e li' la lingua e' una sola.
shot $P apps/theme/os.skillfish.theme.metainfo.xml
put $P 0644 system/usr/share/icons/hicolor/scalable/apps/skillfish-theme.svg usr/share/icons/hicolor/scalable/apps/skillfish-theme.svg
put $P 0644 system/usr/share/icons/hicolor/48x48/apps/skillfish-theme.png usr/share/icons/hicolor/48x48/apps/skillfish-theme.png
put $P 0644 system/usr/share/icons/hicolor/128x128/apps/skillfish-theme.png usr/share/icons/hicolor/128x128/apps/skillfish-theme.png
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfish-theme.png usr/share/icons/hicolor/256x256/apps/skillfish-theme.png
# The steampunk look used to be baked into the ISO filesystem only (no package
# owned it), so a fix could not reach installed systems through apt. It ships
# as a package now — same paths, so it simply takes ownership of the files.
putdir $P theme/icons/SkillFishSteampunk              usr/share/icons/SkillFishSteampunk
# ⚠️ La riparazione del pulsante del menu, per chi AGGIORNA.
# La configurazione del pannello sta nella home dell'utente e un pacchetto
# non tocca le home: /etc/skel vale solo per chi arriva nuovo. Senza questo,
# aggiornare il tema significa consegnare a tutti un menu con l'icona
# sbagliata — e nessun modo, per loro, di capire perche'.
put $P 0755 system/usr/local/bin/skillfish-menu-icon-fix usr/local/bin/skillfish-menu-icon-fix
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
ctrl $P "hicolor-icon-theme" "SkillFishOS Steampunk theme - icons, cursors, Plasma theme and colours" \
  "Icons, cursors, Plasma theme, colours and panel layout. Also puts the menu
button back if an update changed it."
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
printf '#!/bin/sh\nset -e\nfor t in SkillFishSteampunk SkillFish-Steampunk-Cursors; do\n  rm -f "/usr/share/icons/$t/icon-theme.cache" 2>/dev/null || true\ndone\n[ -x /usr/local/bin/skillfish-menu-icon-fix ] && /usr/local/bin/skillfish-menu-icon-fix || true\nexit 0\n' > "$OUT/$P/DEBIAN/postinst"
chmod 0755 "$OUT/$P/DEBIAN/postinst"


# ⚠️ COMPILARE NON E' AVVIARE. Il pannello AI della 26.08.37 compilava e non si
# apriva: una costante chiamava L() venti righe prima che L() esistesse, cioe'
# un errore di esecuzione che py_compile e i controlli sul testo non vedono.
#
# Qui il corpo del modulo viene ESEGUITO davvero (import, costanti, classi) con
# un nome diverso da __main__, quindi main() non parte: niente finestre, niente
# password, nessun demone. Serve solo a rispondere alla domanda "si apre?".
#
# ⚠️⚠️ E QUESTO NON BASTA. NON CONFONDERE QUESTA PROVA CON UNA PROVA.
# Il 22/08/2026 questo passo era verde mentre l'Hub, gia' nelle mani degli
# utenti, non mostrava NESSUN flatpak installato (mai, su nessuna macchina) e
# moriva di SIGSEGV al primo cambio di filtro. Nessuna delle due cose si vede
# eseguendo il corpo del modulo: vivono dietro un clic.
#
# Prima di pubblicare un'applicazione la si apre sulla BC-250 e si tocca OGNI
# scheda, OGNI filtro, OGNI tendina, OGNI pulsante, guardando il risultato con
# una schermata. Anche il caso vuoto. E si guarda coredumpctl dopo, perche' un
# crash nativo non stampa niente in Python.
avvia() { # avvia <sorgente-python>
  # I moduli condivisi (hud_dati, aiuto, i18n) su una macchina vera stanno in
  # /usr/share/skillfish, messi li' da skillfish-base. Qui quel pacchetto non
  # e' installato: si indica la stessa cartella dentro al sorgente, altrimenti
  # la prova boccia l'app per un file che nella CI non c'e' mai stato.
  if QT_QPA_PLATFORM=offscreen \
     PYTHONPATH="$PWD/system/usr/share/skillfish:${PYTHONPATH:-}" \
     python3 - "$1" <<'PYAVVIO' >/tmp/avvio.$$ 2>&1
import runpy, sys
runpy.run_path(sys.argv[1], run_name="prova_di_avvio")
PYAVVIO
  then
    echo "OK  si avvia: $1"
  else
    echo "FAIL non si avvia: $1"
    sed 's/^/     /' /tmp/avvio.$$ | tail -12
    rm -f /tmp/avvio.$$
    exit 1
  fi
  rm -f /tmp/avvio.$$
}

echo "== building =="
P=skillfish-iso-mount
# La scheda AppStream: senza, la descrizione esiste solo in inglese,
# perche' apt la tiene nel control e li' la lingua e' una sola.
shot $P apps/iso-mount/os.skillfish.iso-mount.metainfo.xml
put $P 0644 system/usr/share/icons/hicolor/scalable/apps/skillfish-iso-mount.svg usr/share/icons/hicolor/scalable/apps/skillfish-iso-mount.svg
put $P 0644 system/usr/share/icons/hicolor/48x48/apps/skillfish-iso-mount.png usr/share/icons/hicolor/48x48/apps/skillfish-iso-mount.png
put $P 0644 system/usr/share/icons/hicolor/128x128/apps/skillfish-iso-mount.png usr/share/icons/hicolor/128x128/apps/skillfish-iso-mount.png
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfish-iso-mount.png usr/share/icons/hicolor/256x256/apps/skillfish-iso-mount.png
# Era rimasto nel vecchio apps/build-debs.sh, che prende i file dal disco della
# scheda: fuori dalla catena automatica, quindi fermo a 26.06 mentre tutto il
# resto avanzava, e una correzione qui non sarebbe mai arrivata a nessuno.
put $P 0755 system/usr/local/bin/skillfish-iso-mount usr/local/bin/skillfish-iso-mount
put $P 0644 system/usr/share/kio/servicemenus/skillfish-iso.desktop usr/share/kio/servicemenus/skillfish-iso.desktop
put $P 0644 system/etc/polkit-1/rules.d/49-skillfish-udisks.rules etc/polkit-1/rules.d/49-skillfish-udisks.rules
ctrl $P "udisks2, polkitd | policykit-1" "SkillFishOS native ISO mounting for KDE" \
  "Mounts an ISO from the file manager and releases it from the same menu,
through udisks. No terminal, no root."
P=skillfish-snapshots
# «SkillFishOS Snapshot»: gli snapshot in una finestra, senza terminale e senza
# il vocabolario del filesystem. Risponde a tre domande e basta: che snapshot
# ho, fammene uno adesso, riportami li'.
# ⚠️ Btrfs Assistant NON e' piu' installato: tolto il 20/08/2026, perche'
# questa applicazione non si appoggia a lui in nessun punto e due porte per la
# stessa cosa sono una scelta in piu' da spiegare all'utente.
#
# Tre file e non uno perche' /.snapshots e' leggibile solo da root: anche solo
# per MOSTRARE l'elenco serve passare da pkexec, e polkit lega l'autorizzazione
# al percorso del programma. Separando la lettura dalla modifica si puo' dare
# l'elenco senza password e chiedere la password per cancellare o ripristinare.
# Se fossero un programma solo, o si chiede la password ogni volta che si apre
# la finestra, o non la si chiede mai, nemmeno per cancellare.
put $P 0755 apps/snapshots/skillfish-snapshots        usr/local/bin/skillfish-snapshots
put $P 0755 apps/snapshots/skillfish-snapshots-read   usr/local/bin/skillfish-snapshots-read
put $P 0755 apps/snapshots/skillfish-snapshots-helper usr/local/bin/skillfish-snapshots-helper
# La manutenzione programmata: la chiamano sia il programma di lettura (per
# lo stato) sia l'aiutante (per impostarla), e cosi' non serve una terza
# autorizzazione polkit.
put $P 0755 apps/snapshots/skillfish-btrfs-manutenzione usr/local/bin/skillfish-btrfs-manutenzione
put $P 0644 system/usr/share/polkit-1/actions/os.skillfish.snapshots.policy usr/share/polkit-1/actions/os.skillfish.snapshots.policy
shot $P apps/snapshots/os.skillfish.snapshots.metainfo.xml
put $P 0644 system/usr/share/applications/os.skillfish.snapshots.desktop usr/share/applications/os.skillfish.snapshots.desktop
put $P 0644 system/usr/share/icons/hicolor/scalable/apps/skillfish-snapshots.svg usr/share/icons/hicolor/scalable/apps/skillfish-snapshots.svg
# L'icona: il tema la porta gia' dentro skillfish-theme (tutto l'albero),
# ma serve anche in hicolor, per chi cambia tema e per la finestra stessa.
put $P 0644 system/usr/share/icons/hicolor/48x48/apps/skillfish-snapshots.png usr/share/icons/hicolor/48x48/apps/skillfish-snapshots.png
put $P 0644 system/usr/share/icons/hicolor/64x64/apps/skillfish-snapshots.png usr/share/icons/hicolor/64x64/apps/skillfish-snapshots.png
put $P 0644 system/usr/share/icons/hicolor/128x128/apps/skillfish-snapshots.png usr/share/icons/hicolor/128x128/apps/skillfish-snapshots.png
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfish-snapshots.png usr/share/icons/hicolor/256x256/apps/skillfish-snapshots.png
put $P 0644 system/usr/share/icons/hicolor/512x512/apps/skillfish-snapshots.png usr/share/icons/hicolor/512x512/apps/skillfish-snapshots.png
ctrl $P "python3-pyqt6, snapper, btrfs-progs, btrfsmaintenance, policykit-1 | polkitd, skillfish-base" "SkillFishOS Snapshots - system snapshots and scheduled btrfs maintenance" \
  "Snapshots before and after every apt operation, restored in seconds because
btrfs swaps the subvolume. The second tab keeps btrfs in shape on a schedule."


P=skillfish-menu
# La scheda AppStream: senza, la descrizione esiste solo in inglese,
# perche' apt la tiene nel control e li' la lingua e' una sola.
shot $P apps/menu/os.skillfish.menu.metainfo.xml
put $P 0644 system/usr/share/icons/hicolor/scalable/apps/skillfish-menu.svg usr/share/icons/hicolor/scalable/apps/skillfish-menu.svg
put $P 0644 system/usr/share/icons/hicolor/48x48/apps/skillfish-menu.png usr/share/icons/hicolor/48x48/apps/skillfish-menu.png
put $P 0644 system/usr/share/icons/hicolor/128x128/apps/skillfish-menu.png usr/share/icons/hicolor/128x128/apps/skillfish-menu.png
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfish-menu.png usr/share/icons/hicolor/256x256/apps/skillfish-menu.png
# Questo non stava in NESSUNO script: esisteva solo come .deb costruito a mano
# chissa' quando. Definisce la categoria "SkillFishOS" nel menu delle
# applicazioni — i due .menu (uno per il menu XDG, uno per quello di Plasma) e
# la voce di categoria con nome e descrizione.
put $P 0644 system/etc/xdg/menus/applications-merged/skillfishos.menu etc/xdg/menus/applications-merged/skillfishos.menu
put $P 0644 system/etc/xdg/menus/plasma-applications-merged/skillfishos.menu etc/xdg/menus/plasma-applications-merged/skillfishos.menu
put $P 0644 system/usr/share/desktop-directories/skillfishos.directory usr/share/desktop-directories/skillfishos.directory

ctrl $P "" "SkillFishOS application menu group" \
  "One group in the application menu holding the SkillFishOS tools, instead of
leaving them among the system entries."

P=skillfish-emulators
# La scheda AppStream: senza, la descrizione esiste solo in inglese,
# perche' apt la tiene nel control e li' la lingua e' una sola.
shot $P apps/emulators/os.skillfish.emulators.metainfo.xml
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
put $P 0644 system/usr/share/icons/hicolor/scalable/apps/skillfish-emudeck.svg usr/share/icons/hicolor/scalable/apps/skillfish-emudeck.svg
put $P 0644 system/usr/share/icons/hicolor/48x48/apps/skillfish-emudeck.png usr/share/icons/hicolor/48x48/apps/skillfish-emudeck.png
put $P 0644 system/usr/share/icons/hicolor/128x128/apps/skillfish-emudeck.png usr/share/icons/hicolor/128x128/apps/skillfish-emudeck.png
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfish-emudeck.png usr/share/icons/hicolor/256x256/apps/skillfish-emudeck.png
put $P 0644 system/usr/share/applications/os.skillfish.emulators.desktop usr/share/applications/os.skillfish.emulators.desktop
put $P 0644 system/usr/share/icons/hicolor/scalable/apps/skillfish-emulators.svg usr/share/icons/hicolor/scalable/apps/skillfish-emulators.svg
put $P 0644 system/usr/share/icons/hicolor/48x48/apps/skillfish-emulators.png usr/share/icons/hicolor/48x48/apps/skillfish-emulators.png
put $P 0644 system/usr/share/icons/hicolor/128x128/apps/skillfish-emulators.png usr/share/icons/hicolor/128x128/apps/skillfish-emulators.png
put $P 0644 system/usr/share/icons/hicolor/256x256/apps/skillfish-emulators.png usr/share/icons/hicolor/256x256/apps/skillfish-emulators.png
ctrl $P "flatpak, curl" "SkillFishOS Emulators - install emulators after the installation" \
  "Installs console emulators after the system is in place: the whole EmuDeck set
or one at a time. Upstream installers, nothing repackaged."

for P in skillfish-tuner skillfish-fan skillfish-hub skillfish-monitor skillfish-kernel-manager skillfish-ai-panel skillfish-base skillfish-console skillfish-dashboard skillfish-theme skillfish-emulators skillfish-iso-mount skillfish-snapshots skillfish-menu skillfishos-archive-keyring; do
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
# Il nome del sottovolume di sistema NON si ricava da findmnt: dopo un
# ripristino quello risponde col nome del sistema messo da parte, e
# --annulla non trova piu' niente da recuperare (visto sulla Generic).
check skillfish-base_${VER}_all.deb ./usr/local/bin/skillfish-rollback 'sottovol_da_fstab'
check skillfish-base_${VER}_all.deb ./usr/local/bin/skillfish-snapshot-menu 'GRUB_BTRFS_DISABLE'
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
# chattr +C su /games vale solo finche' e' vuota: il flag non converte i file
# gia' scritti. Se sparisce quella riga, i giochi finiscono in copy-on-write
# e nessuno se ne accorge, perche' tutto continua a funzionare - piano.
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-games-subvolume 'chattr +C'
# Prendere "il primo uid >= 1000" durante l'installazione significa prendere
# l'utente della live, che poi viene cancellato: /games resta di un uid orfano.
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-games-subvolume 'nessuna password: e. la live'
# La condizione e' quello che tiene la correzione fuori dal sistema installato:
# senza, si consegnerebbe a tutti un sistema senza blocco schermo.
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-live-no-lock 'run/live/medium'
# idleTime=0 per powerdevil vuol dire SUBITO, non mai: con lo zero la live
# spegne lo schermo appena resta ferma. Il controllo pretende il valore lungo.
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-live-no-lock 'idleTime=86400'
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/i18n.py 'def traduttore'
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/aiuto.py 'class Aiuto'
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/hwmon.py 'def scopri'
# La ventola. Il demone deve contenere i suoi freni: l'emergenza che non
# passa dalla curva, e il ripristino chiamato da ExecStopPost. Sono le due
# righe fra cui sta la differenza tra una ventola e una scheda cotta.
check skillfish-fan_${VER}_all.deb           ./usr/local/bin/skillfish-fand 'emergency'
check skillfish-fan_${VER}_all.deb           ./usr/local/bin/skillfish-fand 'ripristina_da_fuori'
check skillfish-fan_${VER}_all.deb           ./etc/systemd/system/skillfish-fand.service 'ExecStopPost'
check skillfish-fan_${VER}_all.deb           ./usr/local/bin/skillfish-fan-helper 'MINIMO_ASSOLUTO'
check skillfish-fan_${VER}_all.deb           ./usr/share/applications/os.skillfish.fan.desktop 'Name\[fr\]=SkillFishOS Ventilateur'
# La soglia decide se la spiegazione esce come bollicina o come riquadro:
# se sparisse, i testi lunghi del Tuner tornerebbero in una bollicina che si
# chiude al primo movimento del mouse.
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/aiuto.py 'SOGLIA'
# ⚠️ Le tre applicazioni devono reggere l'assenza del modulo: base e le app
# sono pacchetti diversi. Senza il try, un aggiornamento a meta' spegnerebbe
# tre finestre invece di togliere tre pallini.
check skillfish-tuner_${VER}_all.deb         ./usr/local/bin/skillfish-tuner 'from aiuto import Aiuto'
check skillfish-ai-panel_${VER}_all.deb      ./usr/local/bin/skillfish-ai-panel 'from aiuto import Aiuto'
check skillfish-snapshots_${VER}_all.deb ./usr/local/bin/skillfish-snapshots 'from aiuto import Aiuto'
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/i18n/ru.json 'Телеметрия'
# ⚠️ it.json NON serve alle app — per loro l'italiano sta nel codice, e i18n.py
# lo esclude apposta. Serve alle PAGINE WEB della dashboard, che leggono un
# dizionario e basta: senza, un utente italiano vedrebbe le categorie dell'Hub
# in inglese. Ed e' generato dai sorgenti, quindi se qualcuno lo cancella non
# se ne accorge nessuno: l'inglese e' anche il ripiego buono.
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/i18n/it.json 'Giochi da tavolo'
# ⚠️ Tutte le lingue, sempre: e' una regola del progetto, e finora stava
# solo nella testa di chi scriveva. Qui la costruzione si ferma se anche
# una sola delle otto non ha le frasi dell'applicazione degli snapshot.
# Una traduzione che manca non da' nessun segno: l'app ripiega
# sull'inglese e sembra tutto a posto.
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/i18n/de.json 'Jetzt einen Schnappschuss machen'
# e le frasi della manutenzione, che sono arrivate dopo
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/i18n/de.json 'Datenprüfung'
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/i18n/fr.json 'Vérification des données'
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/i18n/pl.json 'Sprawdzenie danych'
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/i18n/uk.json 'Перевірка даних'
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/i18n/ru.json 'Проверка данных'
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/i18n/es.json 'Comprobación de los datos'
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/i18n/pt.json 'Verificação dos dados'
# e l'italiano, che ora dice «snapshot» e non piu' «fotografie»
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/i18n/it.json 'Fai uno snapshot adesso'
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/i18n/es.json 'Hacer una instantánea ahora'
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/i18n/fr.json 'Prendre un instantané maintenant'
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/i18n/pl.json 'Zrób migawkę teraz'
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/i18n/pt.json 'Tirar um snapshot agora'
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/i18n/ru.json 'Сделать снимок сейчас'
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/i18n/uk.json 'Зробити знімок зараз'
check skillfish-base_${VER}_all.deb          ./etc/systemd/system/skillfish-live-no-lock.service 'ConditionPathExists=/run/live/medium'
check skillfish-base_${VER}_all.deb          ./etc/systemd/system/skillfish-live-no-lock.service 'Before=sddm.service'
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
# la pagina della ventola, e che parli col demone e non col PWM
check skillfish-dashboard_${VER}_all.deb  ./usr/share/skillfish/dashboard/ventola.html '/api/ventola'
check skillfish-dashboard_${VER}_all.deb  ./usr/local/bin/skillfish-dashboardd 'ventola_demone'
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
# Il dizionario condiviso arriva alle pagine dalla rotta /api/i18n del server, e
# sfC() e' la funzione che lo consulta. Se salta uno dei due, le categorie
# dell'Hub restano in inglese in tutte le lingue — senza errori a video.
check skillfish-dashboard_${VER}_all.deb     ./usr/share/skillfish/dashboard/i18n.js  'function sfC'
check skillfish-dashboard_${VER}_all.deb     ./usr/local/bin/skillfish-dashboardd      '/api/i18n'
# Le tabelle delle categorie devono portare i nomi INGLESI: sono le chiavi del
# dizionario condiviso. Se qualcuno ci rimette l'italiano, la traduzione non
# aggancia piu' niente.
check skillfish-dashboard_${VER}_all.deb     ./usr/share/skillfish/dashboard/hub.html  '"Word processors"'
# La tendina delle lingue e la favicon: se saltano, la pagina funziona lo
# stesso e nessuno se ne accorge — una fila di nove bottoni e un'icona vuota
# non sono un errore, sono solo brutte.
check skillfish-dashboard_${VER}_all.deb     ./usr/share/skillfish/dashboard/index.html '<details class="langmenu"'
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
# e il pezzo che disegna le barre: la configurazione lo chiama per nome, quindi
# deve esserci, ed e' l'unico posto dove il numero di thread viene deciso.
check skillfish-tuner_${VER}_all.deb         ./usr/local/bin/skillfish-hud-cpubars    cpubar
check skillfish-tuner_${VER}_all.deb         ./usr/local/bin/skillfish-hud-config     skillfish-hud-cpubars
# e che i ripieghi generici dei sensori non vengano persi in una riscrittura
check skillfish-tuner_${VER}_all.deb         ./usr/local/bin/skillfish-hud-val        cpu_temp_generico
# I sensori della scheda madre: lo script E l'unita' che lo fa partire.
# Questo file e' rimasto per mesi nel repository senza essere in nessun
# pacchetto e senza che lo lanciasse nessuno, e non se n'e' accorto nessuno
# perche' un file fuori da ogni elenco non manca a nessuno. Ora manca qui.
check skillfish-tuner_${VER}_all.deb         ./usr/local/bin/skillfish-sensori        modprobe
# Il configuratore del HUD e il generatore devono restare d'accordo: le
# chiavi dei blocchi sono le stesse scritte nelle preferenze, e se una delle
# due parti le rinomina l'ordine salvato non viene piu' capito — in silenzio.
check skillfish-tuner_${VER}_all.deb         ./usr/local/bin/skillfish-hud-editor     'ORDINE_PREDEFINITO'
check skillfish-tuner_${VER}_all.deb         ./usr/local/bin/skillfish-hud-config     'ORDINE_PREDEFINITO'
# e che il generatore non esegua una voce inventata nel file delle preferenze
check skillfish-tuner_${VER}_all.deb         ./usr/local/bin/skillfish-hud-config     'type "b_\$voce"'
check skillfish-tuner_${VER}_all.deb         ./etc/systemd/system/skillfish-sensori.service  ExecStart=/usr/local/bin/skillfish-sensori
# L'autostart deve chiamare il percorso assoluto: con "sh -c" e le virgolette,
# KDE lo converte in servizio systemd e $HOME resta letterale.
check skillfish-base_${VER}_all.deb          ./etc/skel/.config/autostart/skillfish-conky.desktop "Exec=/usr/local/bin/skillfish-hud"
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-info           fastfetch
check skillfish-base_${VER}_all.deb          ./etc/skel/.config/autostart/blueman.desktop 'Hidden=true'
check skillfish-base_${VER}_all.deb          ./usr/local/bin/skillfish-kde-firstrun.sh 'blueman'
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
# Le tre cose che, se saltano, non si vedono finche' non serve il ripristino:
# l'applicazione senza la voce di menu, la voce fuori dal nostro gruppo, e
# soprattutto la regola polkit senza la quale l'elenco chiede la password a
# ogni apertura (o peggio, la cancellazione non la chiede piu').
check skillfish-snapshots_${VER}_all.deb ./usr/local/bin/skillfish-snapshots 'skillfish-snapshots-read'
check skillfish-snapshots_${VER}_all.deb ./usr/share/applications/os.skillfish.snapshots.desktop 'X-SkillFishOS'
check skillfish-snapshots_${VER}_all.deb ./usr/share/applications/os.skillfish.snapshots.desktop 'Name\[fr\]=SkillFishOS Instantanés'
check skillfish-snapshots_${VER}_all.deb ./usr/share/polkit-1/actions/os.skillfish.snapshots.policy '<allow_active>yes</allow_active>'
check skillfish-snapshots_${VER}_all.deb ./usr/share/polkit-1/actions/os.skillfish.snapshots.policy 'auth_admin_keep'
# L'aiutante NON deve accettare un numero qualunque: lo snapshot 0 e' il
# sistema in funzione, e cancellarlo non ha senso.
# L'aiutante parla inglese con un'etichetta davanti: e' la finestra a
# tradurre. Si controlla l'ETICHETTA, che e' cio' che l'applicazione
# riconosce; il testo inglese puo' cambiare senza rompere la costruzione.
check skillfish-snapshots_${VER}_all.deb ./usr/local/bin/skillfish-snapshots-helper 'ERR:zero'
check skillfish-snapshots_${VER}_all.deb ./usr/local/bin/skillfish-snapshots 'def spiega'
# E il programma di sola lettura non deve accettare argomenti: e' quello che
# gira senza password.
check skillfish-snapshots_${VER}_all.deb ./usr/local/bin/skillfish-snapshots-read 'ERR:argomenti'
# Il drop-in DEVE chiamarsi zz-...: systemd legge i drop-in in ordine
# alfabetico, e questo deve venire dopo schedule.conf, che btrfsmaintenance
# rigenera con la sola periodicita'. Rinominarlo vorrebbe dire che l'ora
# scelta non ha piu' effetto, e nessuno se ne accorgerebbe.
check skillfish-snapshots_${VER}_all.deb ./usr/local/bin/skillfish-btrfs-manutenzione 'zz-skillfish.conf'
# Il refresh dei timer lo chiamiamo NOI: il .path che dovrebbe farlo e'
# spento, e senza questa riga la configurazione cambierebbe a vuoto.
check skillfish-snapshots_${VER}_all.deb ./usr/local/bin/skillfish-btrfs-manutenzione 'btrfsmaintenance-refresh-cron.sh'
check skillfish-snapshots_${VER}_all.deb ./usr/local/bin/skillfish-snapshots-read 'skillfish-btrfs-manutenzione stato'
check skillfish-snapshots_${VER}_all.deb ./usr/local/bin/skillfish-snapshots 'def pagina_manutenzione'
# Le spiegazioni stanno dietro a un «?», non nella pagina: e' lo standard
# delle applicazioni nuove (come su PrintFlow). Se qualcuno rimettesse i
# paragrafi nella finestra, questo controllo non se ne accorgerebbe, ma
# almeno il pallino deve esserci.
check skillfish-snapshots_${VER}_all.deb ./usr/local/bin/skillfish-snapshots 'class Aiuto'
# Nella barra deve esserci il NOSTRO Hub. Il collegamento a Discover era rimasto
# solo nello skel, quindi non si vedeva sulla board — dove il pannello era gia'
# stato sistemato a mano — ma lo ereditava chiunque installasse da ISO.
check skillfish-theme_${VER}_all.deb         ./etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc os.skillfish.hub.desktop
# L'ICONA DEL MENU VA PER PERCORSO, E IL FILE DEVE ESSERE NEL TEMA.
# Qui c'era scritto il contrario — «va per nome, un percorso assoluto lascia il
# pulsante vuoto» — e il 22/08 la prova sulla scheda ha detto un'altra cosa:
# col NOME il pannello disegna l'icona piu' piccola delle altre e slavata,
# perche' la tratta come icona di tema (margini e ricolorazione); col PERCORSO
# esce identica a com'era. Il pulsante vuoto di allora si spiega col file
# puntato che non era dentro a nessun pacchetto: adesso il percorso punta al
# tema, che quel file lo installa, e la riga sotto lo verifica.
# ⚠️ Non e' piu' «skillfish-tuner»: quello era un nome di applicazione con
# dentro il logo, e il giorno in cui il Tuner ha avuto la sua icona il menu si
# e' ritrovato i cursori.
check skillfish-theme_${VER}_all.deb         ./etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc '^icon=skillfish-menu-button$'
# ...e l'icona con quel nome deve stare DENTRO al nostro tema. Se manca, KDE
# taglia dopo il trattino, trova "skillfish" nel tema e disegna il pesce
# stilizzato al posto di quello di ottone, senza dire niente a nessuno.
deve_esserci "$OUT/skillfish-theme/usr/share/icons/SkillFishSteampunk/256x256/apps/skillfish-tuner.png" "skillfish-theme: l icona del Tuner e dentro al tema"
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

# Le applicazioni con la finestra: si controlla che si APRANO, non solo che
# compilino. E' il controllo che mancava quando il pannello AI e' uscito rotto.
avvia apps/fan/skillfish-fan
avvia apps/hud/skillfish-hud-editor

# ⚠️ Ogni finestra deve dire a KDE qual e' il suo file .desktop, o la barra
# delle applicazioni scrive «python3» e perde anche l'icona. Sette app su otto
# lo facevano gia': la ottava se n'e' accorta solo passandoci sopra col mouse.
for _app in apps/fan/skillfish-fan apps/hud/skillfish-hud-editor \
            apps/tuner/skillfish-tuner \
            apps/monitor/skillfish-monitor apps/hub/skillfish-hub \
            apps/snapshots/skillfish-snapshots apps/ai-panel/skillfish-ai-panel \
            apps/kernel-manager/skillfish-kernel-manager \
            apps/dashboard/skillfish-remote-manager; do
  if grep -q 'setDesktopFileName' "$_app"; then
    echo "OK  dice il suo .desktop: $_app"
  else
    echo "FAIL $_app non chiama setDesktopFileName: nella barra si chiamera' python3" >&2
    exit 1
  fi
done

avvia apps/fan/skillfish-fand
avvia apps/fan/skillfish-fan-helper
avvia apps/ai-panel/skillfish-ai-panel
avvia apps/snapshots/skillfish-snapshots
avvia apps/kernel-manager/skillfish-kernel-manager


# LE ICONE DELLE APPLICAZIONI.
# Ogni applicazione ha la sua: fino al 21/08 AI, Tuner e Info mostravano lo
# stesso identico file e nel menu non si distinguevano. Qui si verifica sia
# che il disegno viaggi dentro al pacchetto, sia che il .desktop lo chiami
# PER NOME — col percorso di un PNG il tema non puo' sostituirlo e KDE non
# puo' scegliere la misura.
check skillfish-monitor_${VER}_all.deb ./usr/share/icons/hicolor/scalable/apps/skillfish-monitor.svg "<svg"
check skillfish-monitor_${VER}_all.deb ./usr/share/applications/os.skillfish.monitor.desktop "Icon=skillfish-monitor"
check skillfish-tuner_${VER}_all.deb ./usr/share/icons/hicolor/scalable/apps/skillfish-tuner.svg "<svg"
check skillfish-tuner_${VER}_all.deb ./usr/share/applications/os.skillfish.Tuner.desktop "Icon=skillfish-tuner"
check skillfish-fan_${VER}_all.deb ./usr/share/icons/hicolor/scalable/apps/skillfish-fan.svg "<svg"
check skillfish-fan_${VER}_all.deb ./usr/share/applications/os.skillfish.fan.desktop "Icon=skillfish-fan"
check skillfish-tuner_${VER}_all.deb ./usr/share/icons/hicolor/scalable/apps/skillfish-hud.svg "<svg"
check skillfish-tuner_${VER}_all.deb ./usr/share/applications/os.skillfish.hud.desktop "Icon=skillfish-hud"
check skillfish-kernel-manager_${VER}_all.deb ./usr/share/icons/hicolor/scalable/apps/skillfish-kernel.svg "<svg"
check skillfish-kernel-manager_${VER}_all.deb ./usr/share/applications/os.skillfish.kernel.desktop "Icon=skillfish-kernel"
check skillfish-dashboard_${VER}_all.deb ./usr/share/icons/hicolor/scalable/apps/skillfish-remote.svg "<svg"
check skillfish-dashboard_${VER}_all.deb ./usr/share/applications/os.skillfish.remote-manager.desktop "Icon=skillfish-remote"
check skillfish-snapshots_${VER}_all.deb ./usr/share/icons/hicolor/scalable/apps/skillfish-snapshots.svg "<svg"
check skillfish-snapshots_${VER}_all.deb ./usr/share/applications/os.skillfish.snapshots.desktop "Icon=skillfish-snapshots"
check skillfish-ai-panel_${VER}_all.deb ./usr/share/icons/hicolor/scalable/apps/skillfish-ai.svg "<svg"
check skillfish-ai-panel_${VER}_all.deb ./usr/share/applications/os.skillfish.ai.desktop "Icon=skillfish-ai"
check skillfish-base_${VER}_all.deb ./usr/share/icons/hicolor/scalable/apps/skillfish-info.svg "<svg"
check skillfish-base_${VER}_all.deb ./usr/share/applications/skillfish-info.desktop "Icon=skillfish-info"
check skillfish-emulators_${VER}_all.deb ./usr/share/icons/hicolor/scalable/apps/skillfish-emudeck.svg "<svg"
check skillfish-emulators_${VER}_all.deb ./usr/share/applications/os.skillfish.emudeck.desktop "Icon=skillfish-emudeck"
check skillfish-emulators_${VER}_all.deb ./usr/share/icons/hicolor/scalable/apps/skillfish-emulators.svg "<svg"
check skillfish-emulators_${VER}_all.deb ./usr/share/applications/os.skillfish.emulators.desktop "Icon=skillfish-emulators"


# L'HUB SENZA DISCOVER.
# ⚠️ La transazione deve partire STACCATA (systemd-run): se torna a essere un
# processo figlio della finestra, il primo aggiornamento che sostituisce le Qt
# la uccide a meta' e lascia dpkg da riparare a mano.
check skillfish-hub_${VER}_all.deb ./usr/local/lib/skillfish/hub-comune.sh "systemd-run"
check skillfish-hub_${VER}_all.deb ./usr/local/bin/skillfish-hub-helper "tx-start"
# Il firmware c'e', e NON viene portato via da «Aggiorna tutto».
check skillfish-hub_${VER}_all.deb ./usr/local/bin/skillfish-hub-helper "fw-list"
check skillfish-hub_${VER}_all.deb ./usr/local/bin/skillfish-hub "def firmware"
# L'avviso e i suoi due timer.
check skillfish-hub_${VER}_all.deb ./usr/local/bin/skillfish-hub-notify "notify-send"
check skillfish-hub_${VER}_all.deb ./etc/systemd/system/skillfish-hub-refresh.timer "OnCalendar=hourly"
check skillfish-hub_${VER}_all.deb ./usr/lib/systemd/user/skillfish-hub-notify.timer "OnUnitActiveSec"


# IL CONFIGURATORE DEL HUD, ANCHE DAL WEB.
# ⚠️ La finestra e la pagina devono dire la STESSA cosa su quali voci la
# macchina puo' dare: la logica sta in hud_dati.py e le due strade la
# importano. Se qualcuno ne rimettesse una copia dentro all'applicazione,
# al primo sensore nuovo le due direbbero cose diverse.
check skillfish-base_${VER}_all.deb          ./usr/share/skillfish/hud_dati.py 'def disponibili'
check skillfish-tuner_${VER}_all.deb         ./usr/local/bin/skillfish-hud-editor 'import hud_dati'
check skillfish-dashboard_${VER}_all.deb     ./usr/local/bin/skillfish-dashboardd 'import hud_dati'
check skillfish-dashboard_${VER}_all.deb     ./usr/share/skillfish/dashboard/hud.html 'api/hud/conf'
# ⚠️ Il HUD e' dell'utente del desktop: il demone gira da root e se scrivesse
# nella home di root non cambierebbe niente sullo schermo di nessuno.
check skillfish-dashboard_${VER}_all.deb     ./usr/local/bin/skillfish-dashboardd 'def hud_utente'

# L'HUB APRE I FILE CHE APRIVA DISCOVER.
# .deb, .flatpakref, .flatpakrepo e i link appstream:// e apt://. Senza
# queste tre righe si puo' togliere Discover e scoprire dopo che il doppio
# clic su un pacchetto scaricato non apre piu' niente.
check skillfish-hub_${VER}_all.deb ./usr/local/bin/skillfish-hub "def bersaglio"
check skillfish-hub_${VER}_all.deb ./usr/share/applications/os.skillfish.hub.desktop 'application/vnd.flatpak.ref'
# ⚠️ L'helper gira da root: ogni percorso che arriva da fuori si controlla.
check skillfish-hub_${VER}_all.deb ./usr/local/lib/skillfish/hub-comune.sh 'percorso_sicuro'

# IL PULSANTE DEL MENU.
# ⚠️ Il pesce del pannello sta nel tema col nome del logo, e il pannello lo
# chiede per PERCORSO: col nome Plasma lo ricolora e lo rimpicciolisce.
# Prima stava in un file chiamato «skillfish-tuner» — un nome di
# applicazione con dentro il logo — e il giorno in cui il Tuner ha avuto la
# sua icona il menu si e' ritrovato i cursori.
deve_esserci "$OUT/skillfish-theme/usr/share/icons/SkillFishSteampunk/256x256/apps/skillfish-menu-button.png" "skillfish-theme: il pesce del pannello"
check skillfish-theme_${VER}_all.deb ./etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc 'customButtonImage=skillfish-menu-button$'
check skillfish-theme_${VER}_all.deb ./usr/local/bin/skillfish-menu-icon-fix 'org.kde.plasma.kickoff'


# LE ICONE DEI PACCHETTI DI SERVIZIO.
# ⚠️ Il nome del file DEVE essere il nome del pacchetto: l'Hub cerca
# quello, esatto, e una lettera sbagliata riporta il riquadro grigio
# senza dire niente a nessuno.
check skillfish-base_${VER}_all.deb ./usr/share/icons/hicolor/scalable/apps/skillfish-base.svg '<svg'
check skillfish-console_${VER}_all.deb ./usr/share/icons/hicolor/scalable/apps/skillfish-console.svg '<svg'
check skillfish-iso-mount_${VER}_all.deb ./usr/share/icons/hicolor/scalable/apps/skillfish-iso-mount.svg '<svg'
check skillfish-menu_${VER}_all.deb ./usr/share/icons/hicolor/scalable/apps/skillfish-menu.svg '<svg'
check skillfish-theme_${VER}_all.deb ./usr/share/icons/hicolor/scalable/apps/skillfish-theme.svg '<svg'
check skillfishos-archive-keyring_${VER}_all.deb ./usr/share/icons/hicolor/scalable/apps/skillfishos-archive-keyring.svg '<svg'


# ⚠️ IL TUNER DEVE CHIEDERE LA PASSWORD.
# Fino al 22/08 la sua politica diceva <allow_any>yes</allow_any>: l'helper
# che cambia frequenze e tensioni partiva senza autenticazione, anche da una
# sessione remota. Se qualcuno rimette 'yes', questa riga lo ferma.
check skillfish-tuner_${VER}_all.deb ./usr/share/polkit-1/actions/os.skillfish.tuner.policy '<allow_active>auth_admin_keep</allow_active>'
notcheck skillfish-tuner_${VER}_all.deb ./usr/share/polkit-1/actions/os.skillfish.tuner.policy '<allow_any>yes</allow_any>'


check skillfish-hub_${VER}_all.deb ./etc/apt/preferences.d/skillfish-no-discover.pref 'Pin-Priority: -1'


# LE DUE PORTE DELL'HUB.
# ⚠️ La differenza fra le due regole vive nel fatto che l'helper comodo NON
# sappia fare le azioni dell'altro. Se qualcuno gli aggiunge «deb», la
# password una volta per sessione varrebbe anche per un pacchetto che
# nessuno ha firmato, e la divisione non servirebbe piu' a niente.
check skillfish-hub_${VER}_all.deb ./usr/share/polkit-1/actions/os.skillfish.hub.policy 'os.skillfish.hub.local'
check skillfish-hub_${VER}_all.deb ./usr/local/bin/skillfish-hub-local 'flatpakbundle'
notcheck skillfish-hub_${VER}_all.deb ./usr/local/bin/skillfish-hub-helper 'flatpakbundle'
check skillfish-hub_${VER}_all.deb ./usr/local/lib/skillfish/hub-comune.sh 'systemd-run'

echo "
ALL DEBS VERIFIED"

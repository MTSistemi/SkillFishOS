# -*- mode: sh -*-
# Il motore dell'Hub: quello che fa il lavoro, senza decidere chi può chiederlo.
#
# PERCHÉ ESISTE QUESTO FILE
# Le operazioni privilegiate dell'Hub passano da due programmi diversi, non da
# uno: skillfish-hub-helper per quello che viene dai nostri repository,
# skillfish-hub-local per i file presi da fuori e per l'aggiunta di sorgenti.
# polkit lega l'autorizzazione al PERCORSO del programma, quindi due programmi
# vogliono dire due regole: il primo chiede la password una volta per sessione,
# il secondo la chiede sempre. La differenza è la firma: quello che arriva dai
# nostri repository è firmato dalla nostra chiave, un .deb scaricato non lo è.
#
# ⚠️ Il codice però è uno solo, qui dentro. Se fosse copiato nei due programmi,
# fra sei mesi una correzione finirebbe in uno e non nell'altro.
#
# ⚠️ Nessuno dei due programmi delega all'altro. Se l'helper "comodo" sapesse
# fare anche le azioni dell'altro, basterebbe chiamarlo con l'azione giusta per
# installare un .deb qualsiasi pagando la password una volta sola: cioè il
# contrario di quello che stiamo facendo.
set -uo pipefail
export DEBIAN_FRONTEND=noninteractive

SRCDIR=/etc/apt/sources.list.d
KEYDIR=/usr/share/keyrings
STATO=/var/lib/skillfish/hub
REGISTRO="$STATO/tx.log"
TXJSON="$STATO/tx.json"
CONTEGGIO="$STATO/updates.json"
UNITA=skillfish-hub-tx
ESECUTORE=/usr/local/lib/skillfish/hub-run

mkdir -p "$STATO"; chmod 0755 /var/lib/skillfish "$STATO" 2>/dev/null || true

# ⚠️ Le opzioni di apt qui sotto non sono decorazione:
#   noninteractive + force-conf*  un apt che si ferma a chiedere di un file di
#                                 configurazione, senza nessuno che risponda,
#                                 resta lì per sempre e blocca il lock di dpkg.
#   Dpkg::Use-Pty=0               senza terminale l'uscita esce a blocchi e il
#                                 registro si vede a scatti.
#   DPkg::Lock::Timeout           apt-daily.timer e' acceso di serie in Debian e
#                                 fa il suo apt-get update quando gli pare. Se
#                                 capita mentre il Hub sta lavorando, il lock e'
#                                 suo e la nostra transazione muore con rc 100 e
#                                 un errore che l'utente non puo' capire ne'
#                                 evitare. Visto: 22/08/2026. Con questo apt
#                                 aspetta due minuti che l'altro finisca.
ATTESA=(-o DPkg::Lock::Timeout=120)
APTOPT=(-y -o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confold
        -o Dpkg::Use-Pty=0 "${ATTESA[@]}")

safe_name() { case "$1" in (''|*/*|*..*) echo "nome non valido" >&2; exit 2;; esac; }

# ⚠️ Un percorso che arriva da fuori, e qui siamo root: deve essere assoluto e
# deve essere un FILE. Una cartella, un dispositivo o un percorso che non esiste
# non devono nemmeno arrivare ad apt.
percorso_sicuro() {
  case "$1" in (/*) ;; (*) echo "percorso non assoluto: $1" >&2; return 1;; esac
  [ -f "$1" ] || { echo "non e' un file: $1" >&2; return 1; }
  return 0
}

tx_attiva() { systemctl is-active --quiet "${UNITA}.service"; }

scrivi_stato() {   # scrivi_stato <stato> <rc> <azione...>
  local st="$1" rc="$2"; shift 2
  printf '{"stato":"%s","rc":%s,"azione":"%s","quando":%s}\n' \
         "$st" "$rc" "$*" "$(date +%s)" > "$TXJSON"
  chmod 0644 "$TXJSON"
}

# ⚠️ L'AGGIORNAMENTO NON DEVE MORIRE CON LA FINESTRA.
# Prima l'apt era un processo figlio della finestra, con la sua uscita in una
# pipe: bastava che la finestra morisse — e muore facile, visto che
# l'aggiornamento sostituisce sotto di lei le librerie Qt — perché la pipe si
# chiudesse e l'apt se ne andasse a metà strada, lasciando dpkg in mezzo al
# guado. Qui il lavoro parte in un'unità systemd transitoria, che non è figlia
# di nessuno: la finestra lo GUARDA leggendo il registro.
tx_start() {   # tx_start <azione> [argomenti...]
  [ $# -ge 1 ] || { echo "manca l'azione"; exit 2; }
  if tx_attiva; then echo "una transazione e' gia' in corso"; exit 3; fi
  : > "$REGISTRO"; chmod 0644 "$REGISTRO"
  scrivi_stato in-corso null "$@"
  if command -v systemd-run >/dev/null 2>&1; then
    # --collect: se l'unità di ieri è rimasta lì fallita, systemd la raccoglie
    # invece di rifiutarsi di riusare il nome.
    systemd-run --quiet --collect --unit="$UNITA" --service-type=exec \
      --property=StandardOutput=append:"$REGISTRO" \
      --property=StandardError=append:"$REGISTRO" \
      "$ESECUTORE" "$@" \
      || { scrivi_stato finita 1 "$@"; echo "systemd-run ha rifiutato"; exit 1; }
  else
    # Ripiego per un sistema senza systemd: setsid stacca comunque il processo
    # dalla sessione, che è l'unica cosa che conta qui.
    setsid nohup "$ESECUTORE" "$@" >> "$REGISTRO" 2>&1 < /dev/null &
  fi
  echo "avviata: $*"
}

# Il lavoro vero. Lo chiama systemd (o il ripiego qui sopra), mai l'utente.
esegui_azione() {
  local AZIONE="${1:-}"; shift || true
  local RC=0
  case "$AZIONE" in
    elenchi)
      apt-get "${ATTESA[@]}" update || RC=$?
      command -v flatpak >/dev/null 2>&1 && flatpak update --appstream -y || true
      ;;
    aggiorna)
      apt-get "${ATTESA[@]}" update || RC=$?
      apt-get "${APTOPT[@]}" full-upgrade || RC=$?
      if command -v flatpak >/dev/null 2>&1; then
        flatpak update -y --noninteractive || RC=$?
      fi
      if command -v snap >/dev/null 2>&1; then
        snap refresh || true   # snap dice "no updates" con uscita diversa da 0
      fi
      ;;
    installa)
      [ $# -ge 1 ] || { echo "nessun pacchetto"; exit 2; }
      apt-get "${ATTESA[@]}" update || true
      apt-get "${APTOPT[@]}" install "$@" || RC=$?
      ;;
    rimuovi)
      [ $# -ge 1 ] || { echo "nessun pacchetto"; exit 2; }
      apt-get "${APTOPT[@]}" purge "$@" || RC=$?
      apt-get "${APTOPT[@]}" autoremove || true
      ;;
    firmware)
      # ⚠️ Il firmware si aggiorna UNO alla volta e solo se richiesto per id.
      # Non è un pacchetto: se va storto non si reinstalla, si cambia scheda.
      [ $# -ge 1 ] || { echo "nessun dispositivo"; exit 2; }
      for d in "$@"; do
        fwupdmgr update "$d" -y --no-reboot-check || RC=$?
      done
      ;;
    deb)
      # Un pacchetto scaricato a mano. ⚠️ Non viene dai nostri repository e
      # nessuna delle nostre chiavi lo ha firmato: per questo ci si arriva da
      # skillfish-hub-local, che la password la chiede sempre.
      [ $# -ge 1 ] || { echo "nessun file"; exit 2; }
      percorso_sicuro "$1" || exit 2
      apt-get "${APTOPT[@]}" install "$1" || RC=$?
      ;;
    flatpakref)
      [ $# -ge 1 ] || { echo "nessun file"; exit 2; }
      percorso_sicuro "$1" || exit 2
      flatpak install -y --noninteractive --system --from "$1" || RC=$?
      ;;
    flatpakrepo)
      [ $# -ge 1 ] || { echo "nessun file"; exit 2; }
      percorso_sicuro "$1" || exit 2
      NOME=$(basename "$1"); NOME="${NOME%.flatpakrepo}"
      # ⚠️ Il nome del remote viene dal nome del file: si tiene solo ciò che è
      # innocuo, perché finisce in un percorso sotto /var/lib.
      NOME=$(printf '%s' "$NOME" | tr -cd 'A-Za-z0-9_-')
      [ -n "$NOME" ] || NOME=repo
      flatpak remote-add --if-not-exists --system --from "$NOME" "$1" || RC=$?
      ;;
    flatpakbundle)
      [ $# -ge 1 ] || { echo "nessun file"; exit 2; }
      percorso_sicuro "$1" || exit 2
      flatpak install -y --noninteractive --system --bundle "$1" || RC=$?
      ;;
    *) echo "azione sconosciuta: $AZIONE"; exit 2 ;;
  esac
  # Il conteggio si rifà SEMPRE a fine transazione, così il numero accanto ad
  # «Aggiornamenti» è vero appena finito invece che vecchio di un giorno.
  #
  # ⚠️ Si chiama la funzione, e con «dentro». Prima qui si lanciava
  # skillfish-hub-helper conta, che si tira dietro il controllo «c'è una
  # transazione in corso? allora non conto» — e la transazione in corso è
  # QUESTA. Il conteggio si tirava indietro ogni volta e il numero restava
  # quello del giorno prima, senza che niente segnalasse l'errore.
  conta_aggiornamenti dentro >/dev/null 2>&1 || true
  scrivi_stato finita "$RC" "$AZIONE" "$@"
  exit "$RC"
}

conta_aggiornamenti() {   # conta_aggiornamenti [dentro]
  # ⚠️ Se una transazione sta girando NON si tocca apt: il lock è suo, e
  # aspettarlo qui vorrebbe dire un timer appeso per mezz'ora. L'eccezione è la
  # chiamata che arriva dalla fine della transazione stessa, quando apt ha già
  # finito e il lock è libero: lì il conteggio è proprio quello che serve.
  if [ "${1:-}" != dentro ] && tx_attiva; then
    echo "transazione in corso: non conto"; exit 0
  fi
  apt-get "${ATTESA[@]}" update >/dev/null 2>&1 || true
  APT=$(apt-get -s full-upgrade 2>/dev/null | grep -c '^Inst ')
  FLAT=0; SNAP=0; FW=0
  if command -v flatpak >/dev/null 2>&1; then
    FLAT=$(flatpak remote-ls --updates --columns=application 2>/dev/null | grep -cv '^Application ID$')
  fi
  if command -v snap >/dev/null 2>&1; then
    SNAP=$(snap refresh --list 2>/dev/null | tail -n +2 | grep -c .)
  fi
  if command -v fwupdmgr >/dev/null 2>&1; then
    fwupdmgr refresh --force >/dev/null 2>&1 || true
    FW=$(fwupdmgr get-updates --json 2>/dev/null | grep -c '"DeviceId"')
  fi
  printf '{"quando":%s,"apt":%s,"flatpak":%s,"snap":%s,"firmware":%s}\n' \
         "$(date +%s)" "$APT" "$FLAT" "$SNAP" "$FW" > "$CONTEGGIO"
  chmod 0644 "$CONTEGGIO"
  cat "$CONTEGGIO"
}

repo_aggiungi() {   # repo_aggiungi <nome> <base64 del file .sources>
  local NAME="${1:-}" B64="${2:-}"
  safe_name "$NAME"
  printf '%s' "$B64" | base64 -d > "${SRCDIR}/${NAME}.sources"
  chmod 0644 "${SRCDIR}/${NAME}.sources"
  apt-get "${ATTESA[@]}" update
  echo "OK repo-add ${NAME}"
}

repo_togli() {   # repo_togli <nome>
  local NAME="${1:-}"
  safe_name "$NAME"
  rm -f "${SRCDIR}/${NAME}.sources" "${SRCDIR}/${NAME}.list"
  apt-get "${ATTESA[@]}" update || true
  echo "OK repo-remove ${NAME}"
}

repo_accendi() {   # repo_accendi <nome> <0|1>
  local NAME="${1:-}" EN="${2:-1}" F
  safe_name "$NAME"
  F="${SRCDIR}/${NAME}.sources"
  [ -f "$F" ] || { echo "repository inesistente: ${NAME}"; exit 2; }
  if grep -qi '^Enabled:' "$F"; then
    sed -i "s/^[Ee]nabled:.*/Enabled: $([ "$EN" = 1 ] && echo yes || echo no)/" "$F"
  else
    printf 'Enabled: %s\n' "$([ "$EN" = 1 ] && echo yes || echo no)" >> "$F"
  fi
  apt-get "${ATTESA[@]}" update || true
  echo "OK repo-enable ${NAME}=${EN}"
}

chiave_aggiungi() {   # chiave_aggiungi <nome> <base64 della chiave armored>
  local NAME="${1:-}" B64="${2:-}"
  safe_name "$NAME"
  printf '%s' "$B64" | base64 -d | gpg --dearmor > "${KEYDIR}/${NAME}.gpg"
  chmod 0644 "${KEYDIR}/${NAME}.gpg"
  echo "OK key-add ${NAME}"
}

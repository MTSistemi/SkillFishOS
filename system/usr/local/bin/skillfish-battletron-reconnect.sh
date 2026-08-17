#!/bin/bash
# SkillFishOS - riconnessione automatica del "Battletron Nero" (clone Switch Pro
# Controller, hid_nintendo). Il clone non ripagina l'host da idle e l'init di
# hid_nintendo e' lento/instabile. Strategia PAZIENTE (come la riconnessione
# manuale): UN solo connect per volta, poi attendere che l'init hid si completi
# prima di ritentare -> non si interrompe l'handshake a meta'.
# ⚠️ Il MAC era scritto qui dentro, cioe' lo script serviva a una sola
# scrivania. Adesso si mette in /etc/skillfish/battletron.conf:
#
#     MAC=AA:BB:CC:DD:EE:FF
#
# oppure lo si passa da fuori:  MAC=AA:BB:... skillfish-battletron-reconnect.sh
[ -r /etc/skillfish/battletron.conf ] && . /etc/skillfish/battletron.conf
MAC="${MAC:-}"
if [ -z "$MAC" ]; then
    echo "skillfish-battletron-reconnect: no controller address configured." >&2
    echo "Put  MAC=AA:BB:CC:DD:EE:FF  in /etc/skillfish/battletron.conf" >&2
    echo "(find it with: bluetoothctl devices)" >&2
    exit 0
fi

have_input() {  # joystick "Pro Controller" funzionante presente?
  awk 'BEGIN{RS="";IGNORECASE=1} /Name=.*Pro Controller/ && /Handlers=.*js/ {f=1} END{exit !f}' /proc/bus/input/devices
}
is_connected() {
  bluetoothctl info "$MAC" 2>/dev/null | grep -q 'Connected: yes'
}

while true; do
  if have_input; then
    sleep 6; continue                              # gia' funziona: controllo blando
  fi
  # UN tentativo di connessione e ASPETTA l'esito (bluetoothctl connect blocca)
  timeout 20 bluetoothctl connect "$MAC" >/dev/null 2>&1
  # lascia che hid_nintendo completi l'handshake (clone lento)
  for _ in 1 2 3 4 5 6; do have_input && break; sleep 2; done   # fino a ~12s
  if have_input; then
    continue                                       # riuscito
  fi
  # connesso ma init fallito -> ripulisci per il prossimo giro
  if is_connected; then
    bluetoothctl disconnect "$MAC" >/dev/null 2>&1
    sleep 3
  fi
  sleep 8                                           # pausa gentile prima di ritentare
done

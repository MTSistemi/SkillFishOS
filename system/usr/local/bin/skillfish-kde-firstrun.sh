#!/bin/bash
sleep 5
plasma-apply-wallpaperimage /usr/share/skillfish/wallpaper_brass.png
plasma-apply-cursortheme SkillFish-Steampunk-Cursors 2>/dev/null

# ⚠️ DUE INDICATORI BLUETOOTH NEL VASSOIO.
# Blueman e' l'applet Bluetooth di GTK; Plasma ha gia' il suo, che usa le icone
# del nostro tema. Con tutti e due accesi ne compaiono due, e quello di Blueman
# passa da xembedsniproxy: esce col suo fondo scuro quadrato e la sua icona, che
# accanto alle nostre stona.
# Trovato confrontando le due macchine di sviluppo: le icone bluetooth del tema
# erano identiche byte per byte, eppure i vassoi diversi — la differenza non era
# l'icona, era che su una girava anche Blueman.
#
# /etc/skel copre gli utenti NUOVI; questa riga copre chi il suo profilo ce
# l'ha gia', cioe' chi aggiorna da una ISO in cui Blueman c'era.
# ⚠️ Non si disinstalla niente e non si tocca il file di un altro pacchetto: si
# scrive la disattivazione nella cartella dell'utente, che ha la precedenza. Chi
# vuole Blueman toglie quel file e torna come prima.
if [ -f /etc/xdg/autostart/blueman.desktop ] \
   && [ ! -e "$HOME/.config/autostart/blueman.desktop" ]; then
  mkdir -p "$HOME/.config/autostart"
  if [ -f /etc/skel/.config/autostart/blueman.desktop ]; then
    cp /etc/skel/.config/autostart/blueman.desktop "$HOME/.config/autostart/"
  else
    printf '[Desktop Entry]\nType=Application\nName=Blueman Applet\nHidden=true\n' \
      > "$HOME/.config/autostart/blueman.desktop"
  fi
  pkill -f blueman-applet 2>/dev/null
  pkill -f blueman-tray 2>/dev/null
fi

rm -f "$HOME/.config/autostart/skillfish-kde-firstrun.desktop"

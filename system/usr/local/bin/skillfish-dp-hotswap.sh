#!/bin/bash
# SkillFishOS - hot-swap monitor su BC-250 (HPD hardware rotto).
# Il kernel aggiorna PASSIVAMENTE /sys/.../edid su scollega(->0)/ricollega(->nuovo).
# Il demone legge l'EDID in SILENZIO (nessun blink) e forza il compositore a
# rileggere (trigger_hotplug = disconnect->connect = 1 blink + cambio risoluzione)
# SOLO quando l'EDID cambia verso un monitor presente. Risultato: zero blink a
# riposo, un blink solo durante uno swap reale. Dopo lo swap RIAPRE l'HUD eww
# (la finestra layer-shell viene distrutta quando l'output DRM si ri-crea).
# (Richiede cmdline SENZA force `:e` cosi' il trigger genera una transizione reale.)
edid_size() { wc -c < /sys/class/drm/card0-DP-1/edid 2>/dev/null; }
edid_hash() { md5sum /sys/class/drm/card0-DP-1/edid 2>/dev/null | cut -d' ' -f1; }
TRIG=/sys/kernel/debug/dri/0/DP-1/trigger_hotplug
do_trig() { [ -e "$TRIG" ] && echo 1 > "$TRIG" 2>/dev/null; }

# riapre l'HUD eww nella sessione di skillfish (il demone gira da root)
reopen_hud() {
  # Wayfire: ricrea la finestra layer-shell dell'HUD (close+open forza la ricreazione)
  runuser -u skillfish -- env HOME=/home/skillfish XDG_RUNTIME_DIR=/run/user/1000 WAYLAND_DISPLAY=wayland-1 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus sh -c 'eww daemon >/dev/null 2>&1 & sleep 1; eww close hud >/dev/null 2>&1; eww open hud >/dev/null 2>&1' >/dev/null 2>&1
}

# BOOT: triggera finche' il monitor non e' rilevato (poi basta) -> display pronto rapido
for i in $(seq 1 12); do
  s=$(edid_size); [ "${s:-0}" -gt 0 ] && break
  do_trig; sleep 1
done
# un trigger finale per far agganciare il compositore alla risoluzione corretta al boot
do_trig
sleep 2
last=$(edid_hash)

# RUNTIME: poll SILENZIOSO dell'EDID; trigger + riapri HUD solo al cambio verso un monitor presente
while true; do
  cur=$(edid_hash)
  if [ "$cur" != "$last" ]; then
    if [ "$(edid_size)" -gt 0 ]; then
      do_trig            # monitor presente e diverso -> 1 blink, il compositore cambia risoluzione
      sleep 1; do_trig   # secondo trigger: assicura la rilettura dopo stabilizzazione EDID
      sleep 3            # lascia che Hyprland ri-crei l'output e chiuda l'HUD
      reopen_hud         # poi riapri l'HUD (lo swap ha distrutto la finestra layer-shell)
    fi
    last="$cur"
  fi
  sleep 2
done

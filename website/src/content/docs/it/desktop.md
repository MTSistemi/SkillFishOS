---
title: Desktop, tema e remoto
description: KDE Plasma 6, il tema steampunk, l'HUD di sistema, l'anti-suspend e l'accesso remoto.
group: Sistema
order: 4
---

SkillFishOS usa **[KDE Plasma 6](https://kde.org/plasma-desktop/)** come ambiente desktop, vestito con un tema steampunk coerente e una serie di accorgimenti specifici per la BC-250.

## Sessioni

Al login (gestito da **SDDM**, con autologin dell'utente) sono disponibili più sessioni:

- **KDE Plasma X11** — *predefinita*. La scelta dell'X11 rende banale l'accesso remoto (vedi sotto);
- **KDE Plasma Wayland** — selezionabile;
- **Gaming** — una sessione [gamescope](https://github.com/ValveSoftware/gamescope) in stile Big Picture (vedi [Gaming](/docs/gaming)).

## ⚠️ Anti-suspend (critico)

La BC-250 ha la **sospensione ACPI rotta**: se si sospende, **non si risveglia** e serve un reset (vedi [hardware](/docs/hardware-bc250)). Per questo SkillFishOS **disabilita in modo permanente** tutti gli stati di sospensione:

```bash
systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

A questo si aggiungono una regola di `logind` (`IdleAction=ignore`), il blocco schermo automatico disattivato e la gestione energetica con idle "infinito". È una misura **obbligatoria**: una macchina sospesa è anche irraggiungibile da remoto.

## Tema "SkillFish Steampunk"

Il look è coordinato ottone/rame (accento **`#d8a849`**, superfici scure) e coerente dal **boot al desktop**: tema GRUB, splash Plymouth, greeter SDDM, wallpaper a tema pesce. Il pacchetto del tema comprende:

- **icone** (`SkillFishSteampunk`, con `breeze-dark` come fallback) e **cursori** dedicati;
- stile **Kvantum** per le applicazioni Qt e uno **schema colori** KDE;
- **plasma theme**, tema **Konsole**, pulsanti finestra e un **look-and-feel** globale (`org.skillfish.steampunk`);
- avatar utente a tema e una galleria selezionabile.

> I temi predefiniti **Breeze** restano installati come fallback portante (in particolare forniscono la finestra di logout/spegnimento). Non vanno rimossi.

## HUD di sistema (Conky)

In alto a destra c'è un **HUD** in stile ottone realizzato con **[Conky](https://github.com/brndnmtthws/conky)** che mostra in tempo reale: barre per ogni core CPU con MHz/°C/Watt, frequenza/temperatura/VRAM della GPU, RAM, disco, ventola e i **dispositivi Bluetooth collegati** con la relativa carica (gamepad, audio…). I valori arrivano da helper dedicati che leggono direttamente i sensori hardware.

## Accesso remoto (x11vnc)

Poiché la sessione predefinita è X11, l'accesso remoto è semplice: SkillFishOS avvia **[x11vnc](https://github.com/LibVNC/x11vnc)** sul display in uso, condividendo lo schermo reale. Sulla LAN si raggiunge con un qualsiasi client VNC. Questo permette assistenza e configurazione da un altro PC senza tastiera/mouse fisici sulla scheda.

## Rete, audio e applicazioni

- **Rete**: l'ethernet è gestita da **NetworkManager**, quindi visibile e configurabile dalla GUI di Plasma.
- **Audio**: stack **[PipeWire](https://pipewire.org/)** completo (con supporto Bluetooth). Nota: gli adattatori DP→HDMI *attivi* possono rompere l'audio — vedi [Risoluzione problemi](/docs/risoluzione-problemi).
- **Applicazioni di base**: file manager Dolphin, terminale Konsole, PDF Okular, immagini Gwenview, archivi Ark, screenshot Spectacle, store Discover (con flatpak), browser **Google Chrome**, office **OnlyOffice**.
- **App native SkillFishOS** (raggruppate nel menu **"SkillFishOS"**, ognuna installabile/aggiornabile come `.deb` dal repo firmato): **Tuner** (overclock/undervolt/ventola/CU della BC-250), **AI** (LLM locale on-demand sulla GPU integrata), **Monitor** (grafici live di temperatura/frequenza/tensione/ventola), **Kernel Manager** (scegli il kernel di avvio e disinstalla quelli vecchi), **ISO Mount** e **Hub** — il centro software in stile Discover (APT + Flatpak + Snap) con pagine app, carosello di screenshot e gestione delle sorgenti.
- **Display**: un demone (`skillfish-dp-hotswap`) gestisce il rilevamento del monitor, necessario perché l'HPD del DisplayPort è guasto.

## Fonti

- [KDE Plasma](https://kde.org/plasma-desktop/) · [Kvantum](https://github.com/tsujan/Kvantum)
- [Conky](https://github.com/brndnmtthws/conky) · [x11vnc](https://github.com/LibVNC/x11vnc)
- [PipeWire](https://pipewire.org/) · [SDDM](https://github.com/sddm/sddm)
- [Plymouth](https://www.freedesktop.org/wiki/Software/Plymouth/) · [NetworkManager](https://networkmanager.dev/)

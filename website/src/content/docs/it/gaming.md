---
title: Gaming ed emulazione
description: Steam, gamescope, EmuDeck, ES-DE, Heroic, Android e i controller.
group: Uso
order: 1
---

SkillFishOS nasce per giocare. Tutto lo stack di gaming è preinstallato e configurato; tu aggiungi i **tuoi** giochi e le **tue** ROM.

## Steam e Proton

**Steam** (via [Flatpak](https://flatpak.org/)) è integrato con **[gamescope](https://github.com/ValveSoftware/gamescope)** (il compositore di micro-gestione di Valve), **[gamemode](https://github.com/FeralInteractive/gamemode)** e **[MangoHud](https://github.com/flightlessmango/MangoHud)**. È disponibile una **sessione console** dedicata (gamescope in stile Big Picture) selezionabile dal login. I giochi Windows girano tramite **Proton**.

## Giochi non-Steam: Heroic

**[Heroic Games Launcher](https://heroicgameslauncher.com/)** gestisce i giochi **Epic Games** e **GOG**, e i titoli Windows tramite **GE-Proton**. Con **[ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt)** si installano facilmente le versioni di Proton/Wine. È possibile aggiungere i giochi Heroic a Steam (con le relative copertine).

## Emulazione: EmuDeck + ES-DE

**[EmuDeck](https://www.emudeck.com/)** installa e configura in pochi clic un set completo di emulatori (Flatpak): **RetroArch, Dolphin, PCSX2, PPSSPP, melonDS, PrimeHack, Ryujinx, ScummVM** e altri. Il frontend è **[ES-DE](https://es-de.org/)** (EmulationStation Desktop Edition).

In SkillFishOS la cartella `~/Emulation` può puntare a un **NAS di rete** (BIOS, ROM e salvataggi condivisi tra più macchine).

> ⚠️ ES-DE riscrive il proprio file di impostazioni all'uscita: vanno modificate a programma **chiuso**.
>
> ⚠️ Per **Ryujinx** il firmware e le chiavi vanno importati dall'utente: il firmware richiede ogni NCA come directory. **Giochi, ROM, BIOS e chiavi non sono inclusi** nel sistema — è una scelta legale: SkillFishOS offre gli strumenti, i contenuti li metti tu.

## Android e altro

- **[Waydroid](https://waydro.id/)** per le app/giochi Android (binder nel kernel, supporto iptables e librerie ARM);
- **[Sober](https://sober.vinegarhq.org/)** come player per Roblox.

> Nota: l'AI locale e Android non vanno usati insieme ai giochi pesanti, perché condividono la stessa GPU e la stessa memoria.

## Controller

La configurazione consigliata e testata:

- **2× DualShock 4 in Bluetooth** — con giroscopio (utile per il *motion* di giochi come Mario Kart), collegati all'adattatore Realtek integrato;
- **controller via USB** — un cavo **dati** lo fa riconoscere come Xbox 360 (driver `xpad`, XInput), senza giroscopio.

I driver `xpad`, `hid_playstation` e `hid_nintendo` sono inclusi nel kernel. Per ri-accoppiare un DS4: *Share + PS* fino al lampeggio, poi accoppiamento dalla GUI Bluetooth.

## Upscaling

**FSR 4 non è disponibile** sulla BC-250 (richiede hardware RDNA 4). Le alternative sono l'upscaling di **gamescope** (FSR1/NIS) oppure **[OptiScaler](https://github.com/optiscaler/OptiScaler)** per i singoli giochi. Per i titoli *CPU-bound* (es. *Black Myth: Wukong*) abbassare risoluzione o clock GPU non aiuta — vedi [GPU e overclock](/docs/gpu-overclock).

## Fonti

- [Steam](https://store.steampowered.com/) · [gamescope](https://github.com/ValveSoftware/gamescope) · [gamemode](https://github.com/FeralInteractive/gamemode) · [MangoHud](https://github.com/flightlessmango/MangoHud)
- [Heroic](https://heroicgameslauncher.com/) · [ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt) · [Proton GE](https://github.com/GloriousEggroll/proton-ge-custom)
- [EmuDeck](https://www.emudeck.com/) · [ES-DE](https://es-de.org/) · [RetroArch](https://www.retroarch.com/)
- [Waydroid](https://waydro.id/) · [Sober](https://sober.vinegarhq.org/)

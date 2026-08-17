---
title: Granie i emulacja
description: Steam, gamescope, EmuDeck, ES-DE, Heroic, Android i kontrolery.
group: Używanie
order: 1
---

SkillFishOS powstał do grania. Cały zestaw do gier jest zainstalowany i skonfigurowany z góry; ty dokładasz **swoje** gry i **swoje** ROM-y.

## Steam i Proton

**Steam** (przez [Flatpaka](https://flatpak.org/)) jest zintegrowany z **[gamescope](https://github.com/ValveSoftware/gamescope)** (mikrokompozytorem Valve), **[gamemode](https://github.com/FeralInteractive/gamemode)** i **[MangoHud](https://github.com/flightlessmango/MangoHud)**. Przy logowaniu można wybrać osobną **sesję konsolową** (gamescope, w stylu Big Picture). Gry z Windowsa działają przez **Protona**.

## Gry spoza Steama: Heroic

**[Heroic Games Launcher](https://heroicgameslauncher.com/)** obsługuje tytuły z **Epic Games** i **GOG**, a gry windowsowe przez **GE-Proton**. Przy pomocy **[ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt)** łatwo zainstalujesz wersje Protona i Wine. Gry z Heroica można dodać do Steama (razem z okładkami).

## Emulacja: EmuDeck + ES-DE

**[EmuDeck](https://www.emudeck.com/)** w kilku kliknięciach instaluje i konfiguruje komplet emulatorów (jako Flatpaki): **RetroArch, Dolphin, PCSX2, PPSSPP, melonDS, PrimeHack, Ryujinx, ScummVM** i inne. Nakładką jest **[ES-DE](https://es-de.org/)** (EmulationStation Desktop Edition).

W SkillFishOS katalog `~/Emulation` może wskazywać na sieciowy **NAS** (BIOS-y, ROM-y i zapisy wspólne dla kilku maszyn).

> **Uwaga:** ES-DE nadpisuje swój plik ustawień przy wyjściu: edytuj je, gdy program jest **zamknięty**.
>
> **Uwaga:** W przypadku **Ryujinksa** firmware i klucze musi zaimportować użytkownik: firmware oczekuje każdego NCA jako katalogu. **Gry, ROM-y, BIOS-y i klucze nie są dołączone** do systemu — to świadomy wybór prawny: SkillFishOS daje narzędzia, treść dostarczasz ty.

## Android i reszta

- **[Waydroid](https://waydro.id/)** do aplikacji i gier z Androida (binder w jądrze, obsługa iptables i biblioteki ARM);
- **[Sober](https://sober.vinegarhq.org/)** jako odtwarzacz Robloxa — nie jest preinstalowany, weź go ze sklepu poleceniem `flatpak install flathub org.vinegarhq.Sober`. To aplikacja na 18 MB, która ciągnie za sobą 1,1 GB środowiska GNOME: trzymanie jej poza obrazem to właśnie to, co utrzymuje ISO w rozsądnym rozmiarze.

> Uwaga: lokalnej AI i Androida nie należy używać razem z wymagającymi grami, bo dzielą tę samą grafikę i pamięć.

## Kontrolery

Zalecana i sprawdzona konfiguracja:

- **2× DualShock 4 przez Bluetooth** — z żyroskopem (przydaje się do sterowania *ruchem* w grach pokroju Mario Kart), podłączone do wbudowanego układu Realtek;
- **pad przez USB** — kabel **do danych** sprawia, że widziany jest jako Xbox 360 (sterownik `xpad`, XInput), bez żyroskopu.

Sterowniki `xpad`, `hid_playstation` i `hid_nintendo` są wbudowane w jądro. Żeby sparować DS4 na nowo: przytrzymaj *Share + PS*, aż zacznie migać, potem sparuj z okna Bluetootha.

## Skalowanie obrazu

**FSR 4 nie jest dostępne** na BC-250 (wymaga sprzętu RDNA 4). Zamiennikami są skalowanie w **gamescope** (FSR1/NIS) albo **[OptiScaler](https://github.com/optiscaler/OptiScaler)** dla pojedynczych gier. W tytułach *ograniczonych procesorem* (np. *Black Myth: Wukong*) obniżanie rozdzielczości ani taktowania grafiki nic nie da — zobacz [GPU i podkręcanie](/pl/docs/gpu-overclock).

## Źródła

- [Steam](https://store.steampowered.com/) · [gamescope](https://github.com/ValveSoftware/gamescope) · [gamemode](https://github.com/FeralInteractive/gamemode) · [MangoHud](https://github.com/flightlessmango/MangoHud)
- [Heroic](https://heroicgameslauncher.com/) · [ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt) · [Proton GE](https://github.com/GloriousEggroll/proton-ge-custom)
- [EmuDeck](https://www.emudeck.com/) · [ES-DE](https://es-de.org/) · [RetroArch](https://www.retroarch.com/)
- [Waydroid](https://waydro.id/) · [Sober](https://sober.vinegarhq.org/)

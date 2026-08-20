---
title: Игры и эмуляция
description: Steam, gamescope, EmuDeck, ES-DE, Heroic, Android и геймпады.
group: Использование
order: 1
---

SkillFishOS создан, чтобы играть. Весь игровой набор уже установлен и настроен; вы добавляете **свои** игры и **свои** образы картриджей.

## Steam и Proton

**Steam** (через [Flatpak](https://flatpak.org/)) связан с **[gamescope](https://github.com/ValveSoftware/gamescope)** (микрокомпозитором от Valve), **[gamemode](https://github.com/FeralInteractive/gamemode)** и **[MangoHud](https://github.com/flightlessmango/MangoHud)**. Отдельный **консольный сеанс** (gamescope, в духе Big Picture) выбирается на экране входа. Игры для Windows работают через **Proton**.

## Игры не из Steam: Heroic

**[Heroic Games Launcher](https://heroicgameslauncher.com/)** заведует играми из **Epic Games** и **GOG**, а игры для Windows запускает через **GE-Proton**. С помощью **[ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt)** легко ставить версии Proton и Wine. Игры из Heroic можно добавить в Steam (вместе с обложками).

## Эмуляция: EmuDeck + ES-DE

**[EmuDeck](https://www.emudeck.com/)** в несколько щелчков ставит и настраивает целый набор эмуляторов (Flatpak): **RetroArch, Dolphin, PCSX2, PPSSPP, melonDS, PrimeHack, Ryujinx, ScummVM** и другие. Оболочка — **[ES-DE](https://es-de.org/)** (EmulationStation Desktop Edition).

В SkillFishOS папка `~/Emulation` может указывать на сетевое хранилище **NAS** (BIOS, образы и сохранения общие для нескольких машин).

> **Внимание:** ES-DE переписывает свой файл настроек при выходе: правьте его, пока программа **закрыта**.
>
> **Внимание:** для **Ryujinx** прошивку и ключи пользователь ввозит сам: прошивка ждёт каждый NCA в виде каталога. **Игры, образы, BIOS и ключи в систему не входят** — это осознанный правовой выбор: SkillFishOS даёт инструменты, содержимое приносите вы.

## Android и прочее

- **[Waydroid](https://waydro.id/)** для приложений и игр Android (binder в ядре, поддержка iptables и библиотеки ARM);
- **[Sober](https://sober.vinegarhq.org/)** как проигрыватель Roblox — заранее не установлен, берите из магазина командой `flatpak install flathub org.vinegarhq.Sober`. Это приложение на 18 МБ, которое тянет за собой 1,1 ГБ библиотек GNOME: именно потому, что его нет в образе, образ остаётся небольшим.

> Замечание: локальный ИИ и Android не стоит запускать вместе с тяжёлыми играми, потому что они делят одно видеоядро и одну память.

## Геймпады

Рекомендуемая и проверенная связка:

- **два DualShock 4 по Bluetooth** — с гироскопом (полезен для управления наклоном, например в Mario Kart), подключены к встроенному адаптеру Realtek;
- **геймпад по USB** — с кабелем **для данных** он выглядит как Xbox 360 (драйвер `xpad`, XInput), без гироскопа.

Драйверы `xpad`, `hid_playstation` и `hid_nintendo` входят в ядро. Чтобы связать DS4 заново: держите *Share + PS*, пока не замигает, затем свяжите через окно Bluetooth.

## Масштабирование

**FSR 4 на BC-250 недоступен** (ему нужно железо RDNA 4). На замену — масштабирование в **gamescope** (FSR1/NIS) или **[OptiScaler](https://github.com/optiscaler/OptiScaler)** для отдельных игр. Играм, упирающимся в *процессор* (например, *Black Myth: Wukong*), не поможет ни снижение разрешения, ни снижение частоты видеоядра — см. [GPU и разгон](/ru/docs/gpu-overclock).

## Источники

- [Steam](https://store.steampowered.com/) · [gamescope](https://github.com/ValveSoftware/gamescope) · [gamemode](https://github.com/FeralInteractive/gamemode) · [MangoHud](https://github.com/flightlessmango/MangoHud)
- [Heroic](https://heroicgameslauncher.com/) · [ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt) · [Proton GE](https://github.com/GloriousEggroll/proton-ge-custom)
- [EmuDeck](https://www.emudeck.com/) · [ES-DE](https://es-de.org/) · [RetroArch](https://www.retroarch.com/)
- [Waydroid](https://waydro.id/) · [Sober](https://sober.vinegarhq.org/)

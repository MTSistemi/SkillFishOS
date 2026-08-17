---
title: Ігри та емуляція
description: Steam, gamescope, EmuDeck, ES-DE, Heroic, Android і контролери.
group: Користування
order: 1
---

SkillFishOS народився для ігор. Увесь ігровий набір уже встановлено й налаштовано; ви додаєте **свої** ігри та **свої** ROM-и.

## Steam і Proton

**Steam** (через [Flatpak](https://flatpak.org/)) поєднано з **[gamescope](https://github.com/ValveSoftware/gamescope)** (мікрокомпозитором від Valve), **[gamemode](https://github.com/FeralInteractive/gamemode)** і **[MangoHud](https://github.com/flightlessmango/MangoHud)**. Під час входу можна обрати окремий **консольний сеанс** (gamescope, у стилі Big Picture). Ігри для Windows працюють через **Proton**.

## Ігри поза Steam: Heroic

**[Heroic Games Launcher](https://heroicgameslauncher.com/)** веде тайтли з **Epic Games** і **GOG**, а ігри для Windows — через **GE-Proton**. За допомогою **[ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt)** легко встановити потрібні версії Proton і Wine. Ігри з Heroic можна додати до Steam (разом з обкладинками).

## Емуляція: EmuDeck + ES-DE

**[EmuDeck](https://www.emudeck.com/)** за кілька клацань встановлює й налаштовує повний набір емуляторів (як Flatpak): **RetroArch, Dolphin, PCSX2, PPSSPP, melonDS, PrimeHack, Ryujinx, ScummVM** та інші. Оболонка — **[ES-DE](https://es-de.org/)** (EmulationStation Desktop Edition).

У SkillFishOS тека `~/Emulation` може вказувати на мережевий **NAS** (BIOS, ROM-и та збереження спільні для кількох машин).

> **Увага:** ES-DE перезаписує свій файл налаштувань під час виходу: редагуйте їх, коли програму **закрито**.
>
> **Увага:** Для **Ryujinx** мікропрограму та ключі має імпортувати користувач: мікропрограма очікує кожен NCA як каталог. **Ігри, ROM-и, BIOS і ключі не входять** до системи — це свідомий правовий вибір: SkillFishOS дає інструменти, вміст постачаєте ви.

## Android і решта

- **[Waydroid](https://waydro.id/)** для програм та ігор з Android (binder у ядрі, підтримка iptables і бібліотеки ARM);
- **[Sober](https://sober.vinegarhq.org/)** як програвач Roblox — не встановлений наперед, візьміть його з крамниці командою `flatpak install flathub org.vinegarhq.Sober`. Це програма на 18 МБ, яка тягне за собою 1,1 ГБ середовища GNOME: саме те, що ми тримаємо її поза образом, і не дає ISO розпухнути.

> Зауваження: локальний ШІ й Android не варто використовувати разом із важкими іграми, бо вони ділять ту саму графіку й пам'ять.

## Контролери

Рекомендована й перевірена конфігурація:

- **2× DualShock 4 через Bluetooth** — з гіроскопом (стає в пригоді для керування *рухом* в іграх на кшталт Mario Kart), під'єднані до вбудованого адаптера Realtek;
- **геймпад через USB** — кабель **для даних** робить так, що він бачиться як Xbox 360 (драйвер `xpad`, XInput), без гіроскопа.

Драйвери `xpad`, `hid_playstation` і `hid_nintendo` вбудовано в ядро. Щоб наново спарувати DS4: утримуйте *Share + PS*, доки не почне блимати, потім спаруйте у вікні Bluetooth.

## Масштабування зображення

**FSR 4 недоступний** на BC-250 (він потребує заліза RDNA 4). Заміною є масштабування в **gamescope** (FSR1/NIS) або **[OptiScaler](https://github.com/optiscaler/OptiScaler)** для окремих ігор. У тайтлах, що *впираються в процесор* (наприклад, *Black Myth: Wukong*), зниження роздільності чи частоти графіки не допоможе — див. [GPU і розгін](/uk/docs/gpu-overclock).

## Джерела

- [Steam](https://store.steampowered.com/) · [gamescope](https://github.com/ValveSoftware/gamescope) · [gamemode](https://github.com/FeralInteractive/gamemode) · [MangoHud](https://github.com/flightlessmango/MangoHud)
- [Heroic](https://heroicgameslauncher.com/) · [ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt) · [Proton GE](https://github.com/GloriousEggroll/proton-ge-custom)
- [EmuDeck](https://www.emudeck.com/) · [ES-DE](https://es-de.org/) · [RetroArch](https://www.retroarch.com/)
- [Waydroid](https://waydro.id/) · [Sober](https://sober.vinegarhq.org/)

---
title: Ігри та емуляція
description: Steam, gamescope, EmuDeck, ES-DE, Heroic, Android і контролери.
group: Користування
order: 1
---

SkillFishOS народився для ігор. Увесь ігровий набір уже встановлено й налаштовано; ви додаєте **свої** ігри та **свої** ROM-и.

## Наша Mesa (драйвер Vulkan)

Розділ **Ігри** в [Control Center](/uk/docs/control-center) може ввімкнути нашу збірку **Mesa/RADV**, яка відкриває черги compute, що заводський драйвер тримає закритими на цій графіці: виміряно **+4% у Cyberpunk 2077**, **+12% з увімкненим FSR 4**. Працює для лаунчера (Steam, Heroic) через override flatpak, або для **всієї системи** (разом зі стільницею). Потрібне ядро SkillFishOS: на іншому ядрі ці черги compute вішають графіку, і системний перемикач відмовляється стартувати. Програми 32-біт лишаються на драйвері Debian.

## Steam і Proton

**Steam** (через [Flatpak](https://flatpak.org/)) поєднано з **[gamescope](https://github.com/ValveSoftware/gamescope)** (мікрокомпозитором від Valve), **[gamemode](https://github.com/FeralInteractive/gamemode)** і **[MangoHud](https://github.com/flightlessmango/MangoHud)**. Під час входу можна обрати окремий **консольний сеанс** (gamescope, у стилі Big Picture). Ігри для Windows працюють через **Proton**: розділ Ігри в Control Center встановлює й робить типовими **GE-Proton 11-6** і **GE-Proton 10-34**, спільні для Steam і Heroic.

## Ігри поза Steam: Heroic

**[Heroic Games Launcher](https://heroicgameslauncher.com/)** веде тайтли з **Epic Games** і **GOG**, а ігри для Windows — через **GE-Proton**. За допомогою **[ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt)** вручну встановлюють інші версії Proton і Wine, крім тих, що вже встановлює Control Center. Ігри з Heroic можна додати до Steam (разом з обкладинками).

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

Наша Mesa несе **FSR 4** через **[OptiScaler](https://github.com/optiscaler/OptiScaler)** на шляху DLSS гри: GE-Proton 11 сам завантажує OptiScaler, коли знаходить `PROTON_USE_OPTISCALER=1`, гру треба поставити на DLSS, а бібліотеку FSR 4 від AMD (`amdxcffx64.dll`, узяту з драйвера Windows від AMD) — покласти поряд із грою. Заміною лишаються масштабування в **gamescope** (FSR1/NIS) і XeSS, там, де гра має його вбудованим. У тайтлах, що *впираються в процесор* (наприклад, *Black Myth: Wukong*), зниження роздільності чи частоти графіки не допоможе — див. [GPU і розгін](/uk/docs/gpu-overclock).

## Джерела

- [Steam](https://store.steampowered.com/) · [gamescope](https://github.com/ValveSoftware/gamescope) · [gamemode](https://github.com/FeralInteractive/gamemode) · [MangoHud](https://github.com/flightlessmango/MangoHud)
- [Heroic](https://heroicgameslauncher.com/) · [ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt) · [Proton GE](https://github.com/GloriousEggroll/proton-ge-custom)
- [EmuDeck](https://www.emudeck.com/) · [ES-DE](https://es-de.org/) · [RetroArch](https://www.retroarch.com/)
- [Waydroid](https://waydro.id/) · [Sober](https://sober.vinegarhq.org/)

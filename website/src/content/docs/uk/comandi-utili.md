---
title: Корисні команди
description: Шпаргалка для термінала, щоб діагностувати й налаштовувати SkillFishOS.
group: Довідка
order: 4
---

SkillFishOS задумано так, щоб термінал **не** був потрібен: для звичайного користування вистачає [Tuner](/uk/docs/app-native) і решти графічних програм. Ця сторінка — для тих, хто хоче **покопирсатися** чи щось діагностувати. Команди, що потребують прав, використовують `sudo`.

> Перед ризикованими дослідами згадайте про сітку безпеки: знімки Btrfs і повернення назад із меню GRUB (див. [Диски та знімки](/uk/docs/storage-snapshot)).

## Система і ядро

```bash
uname -r                      # чинне ядро (має закінчуватися на -skillfishos)
cat /proc/cmdline             # активні параметри завантаження
journalctl -b -p err          # помилки з поточного запуску
inxi -Fxxxz                   # повний огляд заліза
```

## Графіка, частоти й температури

```bash
# температура графіки з sysfs amdgpu
cat /sys/class/drm/card*/device/hwmon/hwmon*/temp1_input   # °C ×1000
# стан керівника SMU для графіки
systemctl status cyan-skillfish-governor
cat /etc/cyan-skillfish-governor/config.toml               # безпечні точки частоти й напруги
# спостереження за графікою в реальному часі
nvtop        # або: radeontop
```

> На BC-250 керування частотою йде **не** через звичайний sysfs amdgpu, а через **керівника SMU**. Значення змінюйте через [Tuner](/uk/docs/app-native), а не вручну.

## Процесор — розгін і зниження напруги

```bash
systemctl status bc250-smu-oc.service   # «inactive» після застосування — це нормально (служба одноразова)
cat /etc/bc250-smu-oc.conf              # застосовані частота й напруга
lscpu | grep MHz                        # поточні частоти ядер
sensors                                 # температури й напруги (nct6686, k10temp)
```

## Обчислювальні блоки наживо (skillfish-cu)

```bash
skillfish-cu get          # стан у JSON: активні CU + маска на рядок (SE/SH)
sudo skillfish-cu max     # увімкнути всі блоки (40)
sudo skillfish-cu stock   # назад до 24 (базове значення драйвера)
sudo skillfish-cu set 0x1f   # маска WGP для всіх рядків (0x07=24 .. 0x1f=40)
cat /run/skillfish/cu_active # «40/40» (це читає й HUD)
vulkaninfo | grep -i "deviceName\|driverName"   # графіка, як її бачить Vulkan (RADV)
```

Блоками найзручніше керувати із **сітки** в [Tuner](/uk/docs/app-native) (клацання + набори, з «Перевіркою CU»). Перші 24 закріплені драйвером і ввімкнені завжди.

Швидкі тести (ті самі, що використовує Tuner):

```bash
vkpeak                # пропускна здатність FP32 (GFLOPS)
clpeak                # пропускна здатність пам'яті (ГБ/с)
sysbench cpu run      # навантаження й тест процесора
```

## Спільна пам'ять (VRAM/GTT)

```bash
cat /proc/cmdline | tr ' ' '\n' | grep -E 'ttm\.'   # параметри GTT/TTM
glxinfo | grep -i "memory"                                 # пам'ять, яку бачить драйвер
free -h                                                     # спільна RAM/GDDR6
```

## Ігри

```bash
flatpak list                         # програми Flatpak (Steam, емулятори з EmuDeck…)
flatpak update                        # оновити програми Flatpak
gamescope -- %command%               # (впишіть це в параметри запуску у Steam)
# контролери Bluetooth
bluetoothctl                         # scan on / pair / connect / trust
```

## Локальний ШІ

```bash
# одна нативна служба — без контейнерів: Docker не встановлено
systemctl status skillfish-unsloth   # стан рушія ШІ
sudo systemctl start skillfish-unsloth   # запустити
sudo systemctl stop skillfish-unsloth    # спинити й звільнити графіку та пам'ять
curl -s localhost:8888/              # інтерфейс Unsloth Studio (лише локально)
```

## Знімки й повернення назад (Btrfs)

```bash
sudo snapper list                    # перелік знімків
sudo snapper create -d "перед X"     # знімок вручну
sudo btrfs subvolume list /          # підтоми (@, @home, @log, @cache)

# справді повернутися до знімка (діє від наступного запуску)
sudo skillfish-rollback --list       # які знімки доступні
sudo skillfish-rollback 12           # зробити знімок 12 чинною системою
sudo skillfish-rollback --undo       # передумали: повернути попередню
sudo skillfish-rollback --clean      # прибрати системи, відкладені минулими поверненнями

# з меню GRUB → «SkillFishOS snapshots» ви отримуєте той самий знімок
# ЛИШЕ ДЛЯ ЧИТАННЯ: добре, щоб роздивитися і врятувати файли, а тоді виконати команду вище
```

## Оновлення й репозиторій

```bash
sudo apt update && sudo apt full-upgrade   # оновити систему
apt-mark showhold                          # закріплені пакунки (зокрема ядро)
sudo apt install skillfishos-kernel        # встановити/оновити ядро з репозиторію
apt policy <пакунок>                        # з якого репозиторію і якої версії походить пакунок
```

## Мережа й віддалений доступ

```bash
nmcli device status                  # стан мережевих інтерфейсів
ip a                                 # адреси IP
systemctl status x11vnc              # сервер VNC для віддаленої стільниці
hostname -I                          # адреса IP для клієнта VNC
```

## Зображення (HPD у DisplayPort)

```bash
systemctl status skillfish-dp-hotswap   # служба, що обходить зламане HPD
xrandr                                   # виходи й роздільності (сеанс X11)
```

## Джерела

- [Вікі Btrfs](https://btrfs.readthedocs.io/) · [Snapper](http://snapper.io/)
- [Mesa / RADV](https://docs.mesa3d.org/drivers/radv.html) · [vulkaninfo](https://github.com/KhronosGroup/Vulkan-Tools)
- [Arch Wiki](https://wiki.archlinux.org/) — довідка з багатьох команд Linux

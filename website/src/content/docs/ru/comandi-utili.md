---
title: Полезные команды
description: Шпаргалка по терминалу для диагностики и настройки SkillFishOS.
group: Справочник
order: 4
---

SkillFishOS сделан так, чтобы терминал **не** требовался: для обычной работы хватает [Tuner](/ru/docs/app-native) и графических приложений. Эта страница — для тех, кто хочет **повозиться** или разобраться в неполадке. Привилегированные команды идут через `sudo`.

> Перед рискованными опытами вспомните про страховку: снимки Btrfs и возврат из меню GRUB (см. [Хранилище и снимки](/ru/docs/storage-snapshot)).

## Система и ядро

```bash
uname -r                      # работающее ядро (должно оканчиваться на -skillfishos)
cat /proc/cmdline             # действующие параметры загрузки
journalctl -b -p err          # ошибки текущей загрузки
inxi -Fxxxz                   # полная сводка по железу
```

## Видеоядро, частоты и температуры

```bash
# температура GPU из sysfs драйвера amdgpu
cat /sys/class/drm/card*/device/hwmon/hwmon*/temp1_input   # °C ×1000
# состояние регулятора SMU
systemctl status cyan-skillfish-governor
cat /etc/cyan-skillfish-governor/config.toml               # безопасные точки частота/напряжение
# наблюдение за GPU в реальном времени
nvtop        # или: radeontop
```

> На BC-250 управление частотой идёт **не** через обычный sysfs amdgpu, а через **регулятор SMU**. Меняйте значения из [Tuner](/ru/docs/app-native), а не руками.

## Процессор — разгон и снижение напряжения

```bash
systemctl status bc250-smu-oc.service   # «inactive» после применения — это нормально (одноразовая служба)
cat /etc/bc250-smu-oc.conf              # применённые частота и напряжение
lscpu | grep MHz                        # текущие частоты ядер
sensors                                 # температуры и напряжения (nct6686, k10temp)
```

## Вычислительные блоки на ходу (skillfish-cu)

```bash
skillfish-cu get          # состояние в JSON: активные CU и маска по рядам (SE/SH)
sudo skillfish-cu max     # задействовать все CU (40)
sudo skillfish-cu stock   # вернуться к 24 (минимум драйвера)
sudo skillfish-cu set 0x1f   # маска WGP для всех рядов (0x07=24 … 0x1f=40)
cat /run/skillfish/cu_active # «40/40» (это же читает HUD)
vulkaninfo | grep -i "deviceName\|driverName"   # видеоядро глазами Vulkan (RADV)
```

Управлять CU удобнее из **сетки** в [Tuner](/ru/docs/app-native) (щелчок и наборы, с «Проверкой CU»). Первые 24 закреплены драйвером и включены всегда.

Быстрые тесты (те же, что использует Tuner):

```bash
vkpeak                # производительность FP32 (GFLOPS)
clpeak                # пропускная способность памяти (ГБ/с)
sysbench cpu run      # нагрузка и тест процессора
```

## Единая память (видеопамять и GTT)

```bash
cat /proc/cmdline | tr ' ' '\n' | grep -E 'ttm\.'   # параметры GTT/TTM
glxinfo | grep -i "memory"                                 # память глазами драйвера
free -h                                                     # общая RAM/GDDR6
```

## Игры

```bash
flatpak list                         # приложения Flatpak (Steam, эмуляторы EmuDeck…)
flatpak update                        # обновить приложения Flatpak
gamescope -- %command%               # (вписать в параметры запуска в Steam)
# геймпады по Bluetooth
bluetoothctl                         # scan on / pair / connect / trust
```

## Локальный ИИ

```bash
# одна родная служба, без контейнеров: Docker не установлен
systemctl status skillfish-unsloth   # состояние движка ИИ
sudo systemctl start skillfish-unsloth   # запустить
sudo systemctl stop skillfish-unsloth    # остановить и освободить видеоядро и память
curl -s localhost:8888/              # окно Unsloth Studio (только петлевой интерфейс)
```

## Снимки и возврат (Btrfs)

```bash
sudo snapper list                    # список снимков
sudo snapper create -d "перед X"     # снимок вручную
sudo btrfs subvolume list /          # подтома (@, @home, @log, @cache)

# вернуться к снимку по-настоящему (вступает в силу при следующей загрузке)
sudo skillfish-rollback --list       # какие снимки есть
sudo skillfish-rollback 12           # сделать снимок 12 работающей системой
sudo skillfish-rollback --undo       # передумали: вернуть прежнюю
sudo skillfish-rollback --clean      # убрать системы, отставленные прошлыми возвратами

# из меню GRUB → «SkillFishOS snapshots» вы получаете тот же снимок
# ТОЛЬКО ДЛЯ ЧТЕНИЯ: годится осмотреться и спасти файлы, затем выполните команду выше
```

## Обновления и репозиторий

```bash
sudo apt update && sudo apt full-upgrade   # обновить систему
apt-mark showhold                          # закреплённые пакеты (включая ядро)
sudo apt install skillfishos-kernel        # поставить или обновить ядро из репозитория
apt policy <пакет>                          # из какого репозитория и какая версия
```

## Сеть и доступ издалека

```bash
nmcli device status                  # состояние сетевых устройств
ip a                                 # адреса
systemctl status x11vnc              # сервер VNC для удалённого рабочего стола
hostname -I                          # адрес для клиента VNC
```

## Изображение (HPD у DisplayPort)

```bash
systemctl status skillfish-dp-hotswap   # служба, обходящая сломанный HPD
xrandr                                   # выходы и разрешения (сеанс X11)
```

## Источники

- [Вики Btrfs](https://btrfs.readthedocs.io/) · [Snapper](http://snapper.io/)
- [Mesa / RADV](https://docs.mesa3d.org/drivers/radv.html) · [vulkaninfo](https://github.com/KhronosGroup/Vulkan-Tools)
- [Arch Wiki](https://wiki.archlinux.org/) — справочник по множеству команд Linux

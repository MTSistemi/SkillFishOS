---
title: Przydatne polecenia
description: Ściągawka z terminala do diagnozowania i strojenia SkillFishOS.
group: Materiały
order: 4
---

SkillFishOS jest pomyślany tak, żeby terminal **nie** był potrzebny: do normalnego używania wystarczają [Tuner](/pl/docs/app-native) i pozostałe aplikacje graficzne. Ta strona jest dla tych, którzy chcą **pogrzebać** albo zdiagnozować problem. Polecenia wymagające uprawnień używają `sudo`.

> Przed ryzykownymi eksperymentami pamiętaj o siatce bezpieczeństwa: migawki Btrfs i cofanie zmian z menu GRUB (zobacz [Dyski i migawki](/pl/docs/storage-snapshot)).

## System i jądro

```bash
uname -r                      # działające jądro (powinno kończyć się na -skillfishos)
cat /proc/cmdline             # aktywne parametry startowe
journalctl -b -p err          # błędy z bieżącego uruchomienia
inxi -Fxxxz                   # pełne podsumowanie sprzętu
```

## Grafika, taktowanie i temperatury

```bash
# temperatura grafiki z sysfs amdgpu
cat /sys/class/drm/card*/device/hwmon/hwmon*/temp1_input   # °C ×1000
# stan zarządcy SMU dla grafiki
systemctl status cyan-skillfish-governor
cat /etc/cyan-skillfish-governor/config.toml               # bezpieczne punkty częstotliwości i napięcia
# podgląd grafiki w czasie rzeczywistym
nvtop        # albo: radeontop
```

> Na BC-250 sterowanie częstotliwością **nie** idzie przez standardowe sysfs amdgpu, tylko przez **zarządcę SMU**. Wartości zmieniaj [Tunerem](/pl/docs/app-native), a nie ręcznie.

## Procesor — podkręcanie i obniżanie napięcia

```bash
systemctl status bc250-smu-oc.service   # „inactive” po nałożeniu to normalne (usługa jednorazowa)
cat /etc/bc250-smu-oc.conf              # nałożone taktowanie i napięcie
lscpu | grep MHz                        # bieżące częstotliwości rdzeni
sensors                                 # temperatury i napięcia (nct6686, k10temp)
```

## Jednostki obliczeniowe na żywo (skillfish-cu)

```bash
skillfish-cu get          # stan w JSON: aktywne CU + maska na wiersz (SE/SH)
sudo skillfish-cu max     # włącz wszystkie jednostki (40)
sudo skillfish-cu stock   # z powrotem do 24 (wartość bazowa sterownika)
sudo skillfish-cu set 0x1f   # maska WGP dla wszystkich wierszy (0x07=24 .. 0x1f=40)
cat /run/skillfish/cu_active # „40/40” (odczytuje to również HUD)
vulkaninfo | grep -i "deviceName\|driverName"   # grafika widziana przez Vulkana (RADV)
```

Jednostkami najwygodniej zarządzać z **siatki** w [Tunerze](/pl/docs/app-native) (klikanie + profile, z „Testem CU”). Pierwsze 24 są zablokowane przez sterownik i zawsze włączone.

Szybkie testy (te same, których używa Tuner):

```bash
vkpeak                # przepustowość FP32 (GFLOPS)
clpeak                # przepustowość pamięci (GB/s)
sysbench cpu run      # obciążenie i test procesora
```

## Pamięć wspólna (VRAM/GTT)

```bash
cat /proc/cmdline | tr ' ' '\n' | grep -E 'ttm\.'   # parametry GTT/TTM
glxinfo | grep -i "memory"                                 # pamięć widziana przez sterownik
free -h                                                     # dzielona pamięć RAM/GDDR6
```

## Granie

```bash
flatpak list                         # aplikacje Flatpak (Steam, emulatory z EmuDeck…)
flatpak update                        # zaktualizuj aplikacje Flatpak
gamescope -- %command%               # (wpisz to w opcjach uruchamiania w Steamie)
# kontrolery Bluetooth
bluetoothctl                         # scan on / pair / connect / trust
```

## Lokalna AI

```bash
# jedna natywna usługa — bez kontenerów: Docker nie jest zainstalowany
systemctl status skillfish-unsloth   # stan silnika AI
sudo systemctl start skillfish-unsloth   # uruchom
sudo systemctl stop skillfish-unsloth    # zatrzymaj i zwolnij grafikę oraz pamięć
curl -s localhost:8888/              # interfejs Unsloth Studio (tylko lokalnie)
```

## Migawki i cofanie zmian (Btrfs)

```bash
sudo snapper list                    # wypisz migawki
sudo snapper create -d "przed X"     # migawka ręczna
sudo btrfs subvolume list /          # podwoluminy (@, @home, @log, @cache)

# naprawdę wróć do migawki (obowiązuje od następnego uruchomienia)
sudo skillfish-rollback --list       # które migawki są dostępne
sudo skillfish-rollback 12           # ustaw migawkę 12 jako działający system
sudo skillfish-rollback --undo       # zmiana zdania: przywróć poprzedni
sudo skillfish-rollback --clean      # usuń systemy odłożone przez wcześniejsze cofnięcia

# z menu GRUB → „SkillFishOS snapshots” dostajesz tę samą migawkę
# TYLKO DO ODCZYTU: dobre, żeby się rozejrzeć i uratować pliki, a potem użyć polecenia wyżej
```

## Aktualizacje i repozytorium

```bash
sudo apt update && sudo apt full-upgrade   # zaktualizuj system
apt-mark showhold                          # zablokowane pakiety (w tym jądro)
sudo apt install skillfishos-kernel        # zainstaluj/zaktualizuj jądro z repozytorium
apt policy <pakiet>                         # z jakiego repozytorium i w jakiej wersji pochodzi pakiet
```

## Sieć i dostęp zdalny

```bash
nmcli device status                  # stan interfejsów sieciowych
ip a                                 # adresy IP
systemctl status x11vnc              # serwer VNC do zdalnego pulpitu
hostname -I                          # adres IP do wpisania w kliencie VNC
```

## Obraz (HPD w DisplayPort)

```bash
systemctl status skillfish-dp-hotswap   # demon obchodzący zepsute HPD
xrandr                                   # wyjścia i rozdzielczości (sesja X11)
```

## Źródła

- [Wiki Btrfs](https://btrfs.readthedocs.io/) · [Snapper](http://snapper.io/)
- [Mesa / RADV](https://docs.mesa3d.org/drivers/radv.html) · [vulkaninfo](https://github.com/KhronosGroup/Vulkan-Tools)
- [Arch Wiki](https://wiki.archlinux.org/) — źródło wiedzy o wielu poleceniach Linuksa

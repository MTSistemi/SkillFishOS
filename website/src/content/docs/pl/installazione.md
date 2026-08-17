---
title: Instalacja
description: Jak wypalić obraz ISO, uruchomić instalator i dokończyć konfigurację.
group: Instalacja
order: 1
---

SkillFishOS instaluje się z **obrazu live ISO**, który zawiera graficzny instalator [Calamares](https://calamares.io/). Cały proces przechodzi się myszą, terminal nie jest potrzebny.

> Obraz **26.06.4 «Aetherium»** jest dostępny — pobierz go ze strony [Pobieranie](/pl/download). Startuje po **angielsku**, żeby był uniwersalny, a język i układ klawiatury wybierasz podczas instalacji.

## Czego potrzebujesz

- płyty **AMD BC-250** (zobacz [sprzęt](/pl/docs/hardware-bc250));
- dysku **SSD/NVMe** do instalacji;
- monitora podłączonego przez **DisplayPort** (*pasywna* przejściówka DP→HDMI może działać, ale przeczytaj uwagi o obrazie i dźwięku w [Rozwiązywaniu problemów](/pl/docs/risoluzione-problemi));
- **pendrive'a o pojemności co najmniej 8 GB** na instalator;
- klawiatury i myszy na czas instalacji.

## 1. Wypal obraz na pendrive

Pobierz ISO ze strony [Pobieranie](/pl/download) i wypal je na pendrive jednym z narzędzi:

- **[balenaEtcher](https://etcher.balena.io/)** (Windows/macOS/Linux, graficzny, zalecany);
- **[Ventoy](https://www.ventoy.net/)** (pozwala trzymać kilka obrazów ISO na jednym pendrivie);
- z terminala Linuksa poleceniem `dd`:

```bash
sudo dd if=SkillFishOS_amd64.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

> Zamień `/dev/sdX` na właściwe urządzenie twojego pendrive'a. **Uwaga**: `dd` pisze bez pytania i kasuje wszystko na urządzeniu docelowym.

## 2. Uruchom BC-250 z pendrive'a

Włóż pendrive, włącz płytę i wejdź do menu startowego / UEFI, żeby wybrać USB jako urządzenie startowe. Uruchomi się środowisko **live** SkillFishOS (KDE Plasma): możesz obejrzeć system, zanim go zainstalujesz.

## 3. Zainstaluj przez Calamares

Z pulpitu live uruchom instalator (ikona *Install SkillFishOS*). Calamares prowadzi krok po kroku:

1. **Język i strefa czasowa.**
2. **Klawiatura.**
3. **Podział dysku.** SkillFishOS używa **Btrfs** z osobnymi podwoluminami `@rootfs` (system) i `@home` (dane użytkownika): dzięki temu można *cofnąć* system, nie ruszając swoich plików. Układ dopełniają mała partycja **EFI** i partycja **swap**. Większości osób wystarczy instalacja automatyczna („Wymaż dysk”).
4. **Użytkownik.** Utwórz swoje konto (trafi do właściwych grup: granie, dźwięk, render itd.).
5. **Podsumowanie i instalacja.**

Po zakończeniu instalacji uruchom ponownie i wyjmij pendrive.

## 4. Pierwsze uruchomienie

Przy pierwszym uruchomieniu **wszystko jest już skonfigurowane**: zoptymalizowane jądro, zarządca, podkręcanie, motyw, zestaw do grania i migawki są włączone. Nic nie trzeba stroić ręcznie.

Stąd możesz:

- sparować swoje [kontrolery](/pl/docs/gaming) (DualShock 4 przez Bluetooth albo pada przez USB);
- dodać swoje gry do [Steama/EmuDeck](/pl/docs/gaming);
- włączyć [lokalną AI](/pl/docs/ai-locale), kiedy będzie potrzebna;
- dostroić sprzęt [Tunerem](/pl/docs/app-native), jeśli chcesz.

## Układ dysku

| Partycja | System plików | Zawartość |
|---|---|---|
| `nvme0n1p1` | FAT32 (EFI) | program rozruchowy GRUB |
| `nvme0n1p2` | **Btrfs** | `@rootfs` (system) + `@home` (dane) |
| `nvme0n1p3` | swap | przestrzeń wymiany |

## Źródła

- [Calamares](https://calamares.io/) — uniwersalny instalator
- [balenaEtcher](https://etcher.balena.io/) · [Ventoy](https://www.ventoy.net/)
- [Wiki Btrfs](https://btrfs.readthedocs.io/) — podwoluminy i migawki

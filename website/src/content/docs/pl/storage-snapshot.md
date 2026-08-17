---
title: Dyski i migawki Btrfs
description: "Siatka bezpieczeństwa SkillFishOS: samoczynne migawki i cofanie zmian już przy starcie."
group: System
order: 3
---

Jedną z głównych myśli SkillFishOS jest to, żeby dało się **grzebać bez strachu**. Umożliwia to system plików **[Btrfs](https://btrfs.readthedocs.io/)** z samoczynnymi migawkami: każda ważna zmiana zostaje uchwycona, a gdy coś się popsuje, wracasz jednym kliknięciem.

## Osobne podwoluminy

Dysk używa dwóch odrębnych podwoluminów Btrfs:

- **`@rootfs`** — system operacyjny;
- **`@home`** — dane użytkownika.

Trzymanie ich osobno jest kluczowe: cofnięcie systemu **nie rusza plików osobistych**. Możesz wrócić do systemu „z wczoraj”, zachowując dzisiejsze dokumenty, zapisy gier i ustawienia.

## Samoczynne migawki ze Snapperem

SkillFishOS używa **[Snappera](http://snapper.io/)** z konfiguracją `root` i **zaczepami przed i po APT**: za każdym razem, gdy instalujesz albo aktualizujesz pakiety, migawka powstaje samoczynnie *przed* i *po*. Jeśli więc aktualizacja narobi kłopotów, migawka „sprzed” już czeka.

Najważniejsze z konfiguracji:

- limit liczby przechowywanych migawek, żeby dysk się nie zapełnił;
- migawki trzymane przy ważnych *kamieniach milowych* systemu;
- zarządzanie także przez graficzne narzędzie **Btrfs Assistant**.

## Ile ich zostaje

**Pięć**, domyślnie: trzy zwykłe (para przed i po każdej operacji `apt`) oraz dwie „ważne” — z aktualizacji ruszających jądro albo systemd, czyli tych, do których najczęściej chce się wrócić. Ponad nimi stoi punkt *„SkillFishOS — czysta instalacja”*, który nigdy nie wygasa: droga powrotna do systemu prosto z pudełka.

Godzinowa oś czasu jest **wyłączona**. Na domowej konsoli tylko zjada dysk, a i tak nikt do tych migawek nie zagląda. Migawki tworzone **ręcznie** nie liczą się do tych pięciu i nigdy nie są usuwane samoczynnie: jeśli zrobiłeś ją świadomie, zostaje, dopóki jej nie skasujesz.

## Cofanie zmian z menu startowego

Dzięki **[grub-btrfs](https://github.com/Antynea/grub-btrfs)** migawki pojawiają się wprost w menu **GRUB**, pod pozycją *„SkillFishOS snapshots”*. Uruchom ponownie, wybierz migawkę sprzed kłopotów i już w niej jesteś.

Dwie rzeczy warto wiedzieć, zanim na tym polegniesz:

- **To, co uruchamiasz, jest tylko do odczytu.** To środowisko ratunkowe: rozejrzyj się, sprawdź, czy starszy stan naprawdę był w porządku, skopiuj potrzebne pliki. Kilka usług zgłosi przy starcie błąd — po prostu nie mogą pisać. Tak ma być, to nie usterka.
- **Menu startowe odświeża się po każdej operacji `apt`**, więc migawka zrobiona *przed* aktualizacją jest na liście dokładnie wtedy, gdy jej potrzebujesz.

## Jak uczynić powrót trwałym

Uruchomienie migawki samo w sobie niczego nie zmienia, a `snapper rollback` tu nie pomoże: podmienia domyślny podwolumin, podczas gdy nasz wpis w GRUB-ie przypina `subvol=@` i wygrywa. Robi to polecenie:

```bash
sudo skillfish-rollback --list    # które migawki są dostępne
sudo skillfish-rollback 12        # migawka 12 staje się systemem, od następnego uruchomienia
```

Odsuwa ono bieżący system na bok — nie kasuje go, tylko zmienia w `@-rotto-<data>` — i buduje z wybranej migawki nowy, zapisywalny `@`, przenosząc razem z nim całą historię migawek. Jeśli starszy stan też okaże się nie tym, `sudo skillfish-rollback --undo` przywraca wszystko z powrotem, a `--clean` zwalnia miejsce, gdy już masz pewność.

Działa i z normalnego systemu, i z wnętrza migawki uruchomionej tylko do odczytu — czyli w tym przypadku, który liczy się najbardziej: gdy maszyna już nie startuje.

> **Katalog domowy nie jest nigdy ruszany.** `@home` to osobny podwolumin: system cofa się w czasie, twoje pliki zostają takie, jakie są. Dobrze o tym wiedzieć — i pamiętać, zanim policzysz na cofnięcie, że przywróci skasowany dokument. Nie przywróci.

> To ta siatka bezpieczeństwa, dzięki której nawet najmłodsi mogą badać system bez strachu, że popsują go nieodwracalnie.

## Dlaczego Btrfs, a nie Timeshift

SkillFishOS wybrał **Btrfs + Snapper + grub-btrfs** zamiast rozwiązań w rodzaju Timeshifta, bo:

- integracja z APT jest samoczynna (migawka przy każdej operacji na pakietach);
- migawki są rodzime dla systemu plików (natychmiastowe, *copy-on-write*, tanie);
- cofnięcie jest dostępne **już przy starcie**, nawet jeśli system nie uruchamia się normalnie.

## Źródła

- [dokumentacja Btrfs](https://btrfs.readthedocs.io/)
- [Snapper](http://snapper.io/)
- [grub-btrfs (Antynea)](https://github.com/Antynea/grub-btrfs)
- [Btrfs Assistant](https://gitlab.com/btrfs-assistant/btrfs-assistant)

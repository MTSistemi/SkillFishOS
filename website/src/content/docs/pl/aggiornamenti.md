---
title: Aktualizacje i repozytorium
description: Jak SkillFishOS aktualizuje się bezpiecznie, nie dając się popsuć Debianowi sid.
group: Używanie
order: 4
---

SkillFishOS opiera się na **Debianie sid** (*unstable*), czyli gałęzi rozwojowej Debiana: zawsze świeżej, ale z natury podatnej na sporadyczne regresje. Na „egzotycznym” sprzęcie w rodzaju BC-250 nieudana aktualizacja (Mesy, firmware'u albo jądra) potrafi popsuć system. SkillFishOS radzi sobie z tym na dwa sposoby.

## 1. Nasze własne części, z osobnego repozytorium

Najbardziej krytyczne elementy budujemy i rozprowadzamy **my sami**, z **własnego, podpisanego repozytorium APT**:

- zoptymalizowane **[jądro](/pl/docs/kernel)** (obraz + nagłówki);
- **zarządca SMU** i narzędzia do podkręcania;
- **własne aplikacje** [Tuner i AI](/pl/docs/app-native);
- **motyw steampunk** i **oznaczenia marki**;
- konfiguracja systemu.

Wydawanie części z własnego repozytorium oznacza, że możemy **najpierw sprawdzić ją** na prawdziwym sprzęcie i zaktualizować **tylko wtedy, gdy przynosi korzyść** — a nie za każdym razem, gdy coś zmieni się u źródła.

## 2. „Przypinanie” kruchych pakietów

Dla pakietów, które przychodzą z Debiana, ale na tym sprzęcie są delikatne, SkillFishOS stosuje **przypinanie APT**: trzyma je na **sprawdzonej** wersji, dopóki nie przetestujemy nowszej. Główni kandydaci do przypięcia to:

- **Mesa / sterowniki Vulkana (RADV)** — aktualizacja potrafi cofnąć obsługę `gfx1013`;
- **firmware AMD / `linux-firmware`** — mikrokod grafiki;
- **fabryczne jądro Debiana** — żeby zablokować wersje znane z problemów (zobacz [jądro](/pl/docs/kernel));
- **KDE Plasma** — żeby unikać niestabilnych wydań.

Dzięki temu „zwykłe” aktualizacje (czyli większość systemu) przychodzą normalnie, a garstka pakietów zdolnych popsuć wszystko zostaje zamrożona na wersjach, o których wiemy, że działają.

## Jak aktualizować

Jak w każdym Debianie, z terminala:

```bash
sudo apt update && sudo apt full-upgrade
```

…albo z graficznej aplikacji **Discover**, albo z **SkillFishOS Hub** — naszego centrum oprogramowania w stylu Discovera, które instaluje, usuwa i aktualizuje w jednym miejscu z **APT, Flatpaka i Snapa**, z przeglądaniem po kategoriach, stronami aplikacji z karuzelą zrzutów ekranu i przyciskiem „Zaktualizuj wszystko”. Dzięki zaczepom [Snappera](/pl/docs/storage-snapshot) migawka Btrfs powstaje **przed każdą aktualizacją i po niej**: jeśli coś pójdzie źle, cofnięcie z menu GRUB przywraca poprzedni stan.

> Krótko: **my** dajemy sprawdzone jądro, aplikacje i motywy; **Debian** daje resztę świeżego oprogramowania; **przypinanie** zapobiega niespodziankom; **Btrfs** jest siatką bezpieczeństwa. Trzy warstwy ochrony, żeby aktualizowanie nie budziło strachu.

## Oficjalne repozytorium

Repozytorium APT SkillFishOS **działa**, jest podpisane GPG i stoi na **GitHub Pages** (zestaw `aetherium`):

```bash
# 1. zaimportuj klucz podpisujący
sudo curl -fsSL https://mtsistemi.github.io/SkillFishOS/skillfishos-archive-keyring.gpg \
  -o /usr/share/keyrings/skillfishos-archive-keyring.gpg
# 2. dodaj repozytorium
echo "deb [signed-by=/usr/share/keyrings/skillfishos-archive-keyring.gpg] \
https://mtsistemi.github.io/SkillFishOS aetherium main" \
  | sudo tee /etc/apt/sources.list.d/skillfishos.list
# 3. zainstaluj/zaktualizuj jądro przez apt
sudo apt update && sudo apt install skillfishos-kernel
```

Świeże wydania SkillFishOS mają je **już skonfigurowane**; w innym razie powyższe polecenia je dodadzą. [Jądro](/pl/docs/kernel) (obraz na 152 MB) publikowane jest jako *zasób wydania* na GitHubie: maleńki pakiet `skillfishos-kernel` pobiera je i instaluje samoczynnie, więc aktualizacja i tak idzie przez `apt`. Repozytorium prowadzone jest przez **[reprepro](https://salsa.debian.org/debian/reprepro)**, a klient sprawdza podpis własnym *pękiem kluczy*.

## Źródła

- [Debian unstable (sid)](https://wiki.debian.org/DebianUnstable)
- [Przypinanie APT — podręcznik Debiana](https://wiki.debian.org/AptConfiguration)
- [reprepro](https://salsa.debian.org/debian/reprepro) — zarządzanie repozytorium APT
- [Snapper](http://snapper.io/) — migawki przed i po APT

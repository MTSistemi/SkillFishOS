---
title: Rozwiązywanie problemów
description: Najczęstsze problemy BC-250 i to, jak radzi sobie z nimi SkillFishOS.
group: Materiały
order: 1
---

Wiele „problemów” BC-250 to w rzeczywistości znane wady sprzętu, które SkillFishOS obchodzi automatycznie. Oto te najczęstsze.

## Ekran zostaje czarny / monitor nie jest wykrywany

W DisplayPort **zepsute jest wykrywanie podłączenia (Hot-Plug Detect, HPD)**: płyta nie zauważa, że podłączyłeś monitor. SkillFishOS radzi sobie z tym demonem `skillfish-dp-hotswap` (który wymusza wykrycie przy starcie i przy zmianie monitora) oraz parametrem jądra `video=DP-1:e`.

Co sprawdzić:

- używaj monitora **DisplayPort** albo **pasywnej** przejściówki DP→HDMI;
- unikaj **aktywnych** przejściówek DP→HDMI: poza kłopotami z wykrywaniem **psują dźwięk** (patrz niżej);
- jeśli monitor się zmienił, odczekaj kilka sekund: wykrycie jest automatyczne, ale nie natychmiastowe.

## Płyta nie budzi się ze wstrzymania

Wstrzymywanie jest **zepsute na poziomie sprzętu**. Właśnie dlatego SkillFishOS wyłącza je całkowicie (zobacz [Pulpit](/pl/docs/desktop)). Jeśli po bezczynności płyta wygląda na „martwą”, a zarządzanie energią było zmieniane, jedynym wyjściem jest **fizyczny reset**. Nie włączaj z powrotem stanów uśpienia.

## Brak dźwięku z monitora/telewizora

Dźwięk przez DisplayPort działa, ale:

- **aktywne przejściówki DP→HDMI** psują dźwięk: użyj pasywnych, monitora z natywnym DP, **przetwornika USB** albo dźwięku przez **Bluetooth**;
- stosem dźwiękowym jest **PipeWire**: domyślne wyjście ustawia się w ustawieniach dźwięku KDE.

## Kontrolery nie działają

- Pady **DualShock 4** łączą się przez **Bluetooth** (z żyroskopem). Parowanie: przytrzymaj *Share + PS*, aż zaczną migać, potem sparuj z okna Bluetootha.
- Pad **przez USB** trzeba podłączyć kablem **do danych** (nie tylko do ładowania): jest rozpoznawany jako Xbox 360.
- Klony padów potrafią źle dzielić układ Bluetooth z DS4: wtedy używaj ich **przez USB**.

## Grafika wydaje się wolna / temperatury są wysokie

- Sprawdź w [Tunerze](/pl/docs/control-center), czy **40 jednostek obliczeniowych** i regulator V/F (skillfish-vf-governor) są aktywne.
- Pamiętaj, że chłodzenie jest na granicy: po dłuższym obciążeniu wchodzi **zabezpieczenie termiczne** (85 °C). Żeby testy były miarodajne, pozwól płycie ostygnąć między przebiegami (zobacz [GPU](/pl/docs/gpu-overclock)).
- W grach **ograniczonych procesorem** obniżenie rozdzielczości nie podniesie liczby klatek.

## Płyta się zawiesiła (twarde zawieszenie)

BC-250 potrafi **twardo się zawiesić** (całkowita blokada), często przy **zbyt agresywnym obniżeniu napięcia**: niestabilność ujawnia się głównie przy **małym obciążeniu**, więc zawieszenie może trafić nawet na bezczynności. SkillFishOS bierze to z dwóch stron:

- **Sprzętowy watchdog** — licznik **SP5100 TCO** chipsetu jest włączony (`RuntimeWatchdogSec=2min`): przy całkowitej blokadzie płyta **uruchamia się ponownie sama** w ciągu dwóch minut, bez odcinania zasilania.
- **Wykrywacz zawieszeń** — przy starcie usługa zauważa, czy poprzednie wyłączenie było nieprawidłowe (brak znacznika czystego zamknięcia), i **zapisuje to** do `/var/log/skillfish-freeze.log`, wraz z powiadomieniem na pulpicie. Informacja pojawia się też na stronie **Stan** w [Control Center](/pl/docs/control-center).

Jeśli zawieszenia się powtarzają, **obniż sufit krzywej** (np. z Performance na Balanced albo Cautious) w Tunerze: mniej agresywna wartość prawie zawsze załatwia sprawę. Każda krzywa jest stosowana z **automatycznym testem i cofnięciem** — zawieszenie w trakcie próby nigdy nie zostawia płyty na niestabilnej krzywej po ponownym uruchomieniu. Jeśli zdarzają się nawet przy Cautious, podejrzewaj **zasilacz**.

## Aktualizacja coś zepsuła

Każda operacja na pakietach robi migawkę przed i po. Migawki z menu **GRUB → „SkillFishOS snapshots”** startują **tylko do odczytu**: służą do obejrzenia i skopiowania plików, nie do dalszej pracy. Żeby naprawdę wrócić, w terminalu albo konsoli tekstowej (Ctrl+Alt+F3):

```
sudo skillfish-rollback --elenco
sudo skillfish-rollback <number>
sudo reboot
```

`<number>` to migawka „pre” sprzed złej aktualizacji; `sudo skillfish-rollback --annulla` cofa powrót. Folder domowy nie jest ruszany. Zobacz [Dyski i migawki](/pl/docs/storage-snapshot).

## Aktualizacja usunęła pulpit

We wrześniu 2026 Debian przebudowywał Qt i KDE, a **Discover** zaproponował aktualizację, która usuwała cały pulpit KDE. Od tamtej pory SkillFishOS do tego nie dopuszcza, a Hub zastąpił Discover. Aktualizujcie zawsze przez **SkillFishOS Hub**.

Jeśli wam się to przydarzyło, migawka sprzed tej aktualizacji jest najczystszą drogą (patrz wyżej). **Bez migawek**, w konsoli tekstowej (Ctrl+Alt+F3):

```
curl -fsSLo repair.sh https://skillfishos.com/repair.sh
sudo bash repair.sh
```

Skrypt ustala, co usunęła ta aktualizacja, pokazuje plan i pyta, zanim cokolwiek zmieni. Niczego nie usuwa i nie rusza folderu domowego. Uruchomcie ponownie, gdy napisze *Done*.

## AI nie startuje albo wypisuje dziwne rzeczy

- AI działa na Vulkanie (nie na ROCm) i **nie powinno być używane razem z grami** (ta sama grafika i pamięć).
- Jeśli wyjście jest zepsute, upewnij się, że pamięć podręczna KV jest w **f16** (`q4_0` psuje wynik na RADV). Zobacz [Lokalna AI](/pl/docs/ai-locale).

## Źródła

- [bc250.info](https://bc250.info) · [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- [Arch Wiki — Gamepad](https://wiki.archlinux.org/title/Gamepad)
- [PipeWire — rozwiązywanie problemów](https://docs.pipewire.org/)

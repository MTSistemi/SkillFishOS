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

- Sprawdź w [Tunerze](/pl/docs/app-native), czy **40 jednostek obliczeniowych** i zarządca SMU są aktywne.
- Pamiętaj, że chłodzenie jest na granicy: po dłuższym obciążeniu wchodzi **zabezpieczenie termiczne** (85 °C). Żeby testy były miarodajne, pozwól płycie ostygnąć między przebiegami (zobacz [GPU](/pl/docs/gpu-overclock)).
- W grach **ograniczonych procesorem** obniżenie rozdzielczości nie podniesie liczby klatek.

## Płyta się zawiesiła (twarde zawieszenie)

BC-250 potrafi **twardo się zawiesić** (całkowita blokada), często przy **zbyt agresywnym obniżeniu napięcia**: niestabilność ujawnia się głównie przy **małym obciążeniu**, więc zawieszenie może trafić nawet na bezczynności. SkillFishOS bierze to z dwóch stron:

- **Sprzętowy watchdog** — licznik **SP5100 TCO** chipsetu jest włączony (`RuntimeWatchdogSec=2min`): przy całkowitej blokadzie płyta **uruchamia się ponownie sama** w ciągu dwóch minut, bez odcinania zasilania.
- **Wykrywacz zawieszeń** — przy starcie usługa zauważa, czy poprzednie wyłączenie było nieprawidłowe (brak znacznika czystego zamknięcia), i **zapisuje to** do `/var/log/skillfish-freeze.log`, wraz z powiadomieniem na pulpicie. Licznik pojawia się też w panelu **„Mój krzem”** w Tunerze.

Jeśli zawieszenia się powtarzają, **zejdź o jeden profil** (np. z Crazy/Turbo na Performance) w Tunerze: mniej agresywna wartość prawie zawsze załatwia sprawę. Wszystkie profile są **odporne na awarię** — zawieszenie w trakcie testu nigdy nie zostawia płyty na niestabilnym profilu po ponownym uruchomieniu. Jeśli zdarzają się nawet na Stock, podejrzewaj **zasilacz**.

## Aktualizacja coś zepsuła

Uruchom ponownie i z menu **GRUB → „SkillFishOS snapshots”** wybierz działającą wcześniejszą migawkę. Zobacz [Dyski i migawki](/pl/docs/storage-snapshot). Migawki przed aktualizacją i po niej powstają automatycznie.

## AI nie startuje albo wypisuje dziwne rzeczy

- AI działa na Vulkanie (nie na ROCm) i **nie powinno być używane razem z grami** (ta sama grafika i pamięć).
- Jeśli wyjście jest zepsute, upewnij się, że pamięć podręczna KV jest w **f16** (`q4_0` psuje wynik na RADV). Zobacz [Lokalna AI](/pl/docs/ai-locale).

## Źródła

- [bc250.info](https://bc250.info) · [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- [Arch Wiki — Gamepad](https://wiki.archlinux.org/title/Gamepad)
- [PipeWire — rozwiązywanie problemów](https://docs.pipewire.org/)

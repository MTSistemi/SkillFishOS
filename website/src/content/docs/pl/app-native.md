---
title: Własne aplikacje — Tuner i AI
description: Graficzne narzędzia SkillFishOS do sterowania sprzętem i AI bez terminala.
group: Używanie
order: 3
---

SkillFishOS zawiera dwie własne aplikacje (napisane w **PyQt6**, ubrane w motyw przez Kvantum), które oddają sterowanie sprzętem i stosem AI w ręce użytkownika **bez dotykania terminala**.

## SkillFishOS Tuner

**Tuner** to panel sterowania sprzętem. Pozwala ustawić:

- **podkręcanie i obniżanie napięcia procesora**;
- **punkty pracy grafiki** (przez zarządcę SMU, zobacz [GPU i podkręcanie](/pl/docs/gpu-overclock));
- **wentylator** (sterowanie PWM);
- **pamięć VRAM (UMA)** (wymaga ponownego uruchomienia);
- **jednostki obliczeniowe na żywo** — patrz niżej.

### Jednostki obliczeniowe na żywo (siatka)

Tuner pokazuje jednostki obliczeniowe grafiki jako **siatkę kwadratów** (4 wiersze SE/SH × 5 WGP): **zielony = aktywna, czerwony = wyłączona**. Przełącza się je **na żywo, bez restartu** — klikasz pary (1 WGP = 2 CU) albo używasz **profili 24 / 32 / 40 CU** — a potem *Zastosuj*. Pierwsze 24 jednostki to minimum sterownika i zostają zawsze włączone (zobacz [GPU i podkręcanie](/pl/docs/gpu-overclock)).

![SkillFishOS Tuner — siatka jednostek obliczeniowych na żywo, profile i test CU](/img/tuner.jpg)

### Test CU (loteria krzemowa)

Przycisk **„Test CU”** sprawdza kondycję dodatkowych jednostek: włącza każdą parę osobno, obciąża ją **vkpeakiem** i pilnuje **błędów oraz zawieszeń grafiki**, a na koniec obciąża wszystkie 40 naraz. Służy do wyłapania **uszkodzonych CU** na odzyskanych układach „z odrzutu”, żebyś wiedział, czy twój egzemplarz utrzymuje pełne 40.

![Wynik testu CU — wszystkie pary w porządku, 40 CU stabilnie przy 11380 GFLOPS, bez usterek](/img/cu-test.jpg)

### Przebieg „Test” i podgląd na żywo

Przebieg **„Test”** (procesor, grafika, CU, wentylator): nakłada zmianę → uruchamia test wydajności → **sprawdza** stabilność i, jeśli coś jest nie tak, wykonuje automatyczne **cofnięcie**. Przy starcie każdego testu otwiera się okno **[SkillFishOS Telemetry](#skillfishos-telemetry)** z wykresami **temperatury, częstotliwości, napięcia i wentylatora** na żywo (można je zamknąć w dowolnej chwili).

![SkillFishOS Telemetry podczas testu w Tunerze — wykresy temperatury, częstotliwości, napięcia grafiki i wentylatora na żywo](/img/monitor.jpg)

Budowa: graficzna część działa jako użytkownik, a operacje wymagające uprawnień wykonuje mały **demon roota**. Na komputerze domowym jest ustawiony tak, żeby nie pytał o hasło przy każdej czynności. HUD na pulpicie również pokazuje **aktywne CU** na żywo.

### Tryby zarządcy: Zrównoważony i Wydajność

Grafiką BC-250 steruje **zarządca SMU**, który podnosi i opuszcza taktowanie wraz z obciążeniem. Tuner wystawia dwa tryby przełącznikiem:

- **Zrównoważony** *(domyślny)* — taktowanie spada na bezczynności (aż do 350 MHz) i rośnie pod obciążeniem: mniejszy pobór i niższe temperatury na co dzień.
- **Wydajność** — grafika **trzyma się najwyższego taktowania**, gdy tylko pojawi się obciążenie, przez co znikają mikrowahania częstotliwości. W naszym teście *Black Myth: Wukong* daje to **+11% klatek** (z ok. 100 do ok. 111 średnio) i wyższy wynik **1% low** (92 → 102), przy reszcie bez zmian.

Oba tryby pozostają pod **limitem 85 °C**: tryb Wydajność przyciska mocniej, ale nie wyłącza zabezpieczeń.

### Znajdź mój maksimum (kreatory dla procesora i grafiki)

Każda BC-250 jest inna ([loteria krzemowa](/pl/docs/gpu-overclock)). Tuner zawiera dwa kreatory **„Znajdź mój maksimum”**, które charakteryzują **twoją** płytę:

- **Grafika** — podnosi po szczeblach (2000 → 2200 MHz, co 50 MHz), nakładając i **testując** każdy z nich, i zatrzymuje się na ostatnim stabilnym.
- **Procesor** — przechodzi po szczeblach częstotliwości i obniżenia napięcia (od 3600 MHz do 4000 MHz przy skali −36) tym samym schematem **testuj i cofaj**: jeśli krok się nie utrzyma, wraca do ostatniej dobrej wartości.

Wszystko jest **odporne na awarię**: wartość robocza zapisana na dysku to zawsze ostatnia stabilna, więc zawieszenie w trakcie testu nigdy nie zostawi płyty na niestabilnym profilu przy następnym starcie.

### Mój krzem

Panel **„Mój krzem”** podsumowuje profil twojej płyty — najlepszy znaleziony wynik procesora i grafiki, sprawne CU, licznik wykrytych zawieszeń — i pozwala **udostępnić wynik anonimowo** do bazy loterii krzemowej (otwiera wstępnie wypełnione zgłoszenie na GitHubie). Im więcej danych zbierzemy, tym lepsze będą zalecane profile dla wszystkich.

## SkillFishOS Telemetry

**Telemetry** pokazuje w czasie rzeczywistym temperaturę, częstotliwość, obciążenie procesora i grafiki, napięcia, pobór mocy i wentylator. Otwiera się samoczynnie podczas testów Tunera, ale jest też osobną aplikacją. Przycisk **REC** nagrywa sesję testową do pliku **`.sfmon`** (w `~/SkillFishOS-benchmarks/`): otwórz go ponownie, a Telemetry staje się **analizatorem** z suwakiem czasu, którym prześledzisz przebieg sekunda po sekundzie.

![SkillFishOS Telemetry — wykresy z opisaną osią i panel częstotliwości na rdzeń/wątek](/img/telemetry-percore.jpg)

### Częstotliwość na rdzeń i wątek

Przy [ośmiu odblokowanych rdzeniach](/pl/docs/hardware-bc250) jedna liczba „częstotliwość procesora” mówi bardzo mało: na bezczynności szesnaście wątków potrafi siedzieć **jednocześnie** na 800, 1775 i 3990 MHz, więc odczytana wartość zależy tylko od tego, który rdzeń akurat trafił do pomiaru.

Dolny panel rysuje **jeden słupek na wątek**, w parach według rdzenia fizycznego i z podpisem `rdzeń·wątek`. Kolor przechodzi od mosiądzu do żaru, im wyżej wspina się wątek, na każdym słupku wypisane są megaherce, a nagłówek podsumowuje **minimum, średnią, maksimum i liczbę działających wątków**. Wątki wyłączone z Tunera nie znikają: zostają jako przerywane pole **„off”**, więc rzeczywistą konfigurację widać na pierwszy rzut oka.

### Czytelne osie

Każdy wykres ma teraz **skalę z liniami siatki i wartościami na osi pionowej**, dopasowaną do ludzkich liczb (`0 / 1000 / 2000 / 3000`, a nie `-160 / 1394 / 2948`). Gdy dane leżą blisko zera, zero staje się podłogą, więc wykres megaherców albo obrotów wentylatora nigdy nie pokazuje ujemnej podstawy; a płaska linia nie jest już powiększana tak, że szum wygląda jak góra.

## SkillFishOS AI

**Panel AI** włącza i wyłącza lokalny stos modeli jednym kliknięciem, oddając grafikę i pamięć grom, gdy nie jest potrzebny. To „łatwa” twarz tego, co opisuje strona [Lokalna AI](/pl/docs/ai-locale).

![Panel SkillFishOS AI — lokalny silnik modeli (Qwen3 14B) na grafice przez Vulkan, włącz/wyłącz jednym kliknięciem](/img/ai-panel.jpg)

## Po co one są

Celem SkillFishOS jest, żeby **każdy** — łącznie z najmłodszymi — mógł używać i stroić system bez uczenia się poleceń terminala. Te aplikacje przekładają złożone operacje (zarządca SMU, parametry jądra, migawki i cofanie zmian) na kilka kliknięć, trzymając **zabezpieczenia** (ochrona termiczna, testuj i cofaj) cały czas włączone.

## Źródła

- [PyQt6 / Qt for Python](https://doc.qt.io/qtforpython/) · [Kvantum](https://github.com/tsujan/Kvantum)
- [sysbench](https://github.com/akopytov/sysbench) · [vkpeak](https://github.com/nihui/vkpeak)
- Repozytorium projektu — [github.com/MTSistemi/SkillFishOS](https://github.com/MTSistemi/SkillFishOS) (`apps/tuner`, `apps/ai-panel`)

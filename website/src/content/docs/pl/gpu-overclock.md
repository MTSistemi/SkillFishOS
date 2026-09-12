---
title: GPU, CPU, podkręcanie i obniżanie napięcia
description: Jak SkillFishOS steruje taktowaniem, napięciami i temperaturami BC-250 — z prawdziwymi liczbami zmierzonymi na sprzęcie.
group: System
order: 2
---

Na zwykłym APU taktowanie stroi się przez `amdgpu` w sysfs. Na BC-250 **to nie działa**: sterowanie idzie przez **SMU** (System Management Unit) i wymaga osobnych narzędzi. SkillFishOS ma je wszystkie w komplecie, z gotową bezpieczną krzywą i systemem ochrony termicznej.

> **Uwaga:** **Loteria krzemowa.** Każda liczba na tej stronie jest **zmierzona na naszej BC-250**. Każdy egzemplarz jest inny: jeden przyjmie ostrzejszą krzywą, drugi mniejszą. Dlatego SkillFishOS **startuje z fabryczną krzywą** (profil **Performance**, sufit 2100 MHz) i pozwala ją zmienić z [Tunera](/pl/docs/control-center), który sprawdza każdą krzywą **na twojej płycie** automatycznym testem trwającym 25 sekund i sam się wycofuje, jeśli nie zadziała.

## Krzywa napięcie/częstotliwość i trzy profile

[Tuner](/pl/docs/control-center) steruje grafiką **krzywą napięcie/częstotliwość**: MHz w poziomie, miliwolty w pionie, punkty przeciągane na wykresie albo wpisywane w tabeli obok. Trzy profile przesuwają **sufit** krzywej:

| Profil | Sufit GPU | Uwagi |
|---|---|---|
| **Cautious** | 1850 MHz | Punkt dolny z fabrycznym chłodzeniem: niemal te same klatki, dziesięć stopni mniej |
| **Balanced** | 2000 MHz | Kompromis między taktowaniem a ciepłem |
| **Performance** | 2100 MHz | Krzywa z piętnastu punktów zmierzona na płycie deweloperskiej — ta, którą wysyłamy domyślnie |

**Zastosuj to próba, nie natychmiastowy zapis.** Krzywa, która prosi o zbyt niskie napięcie, wiesza płytę, a na BC-250 zawieszenie da się zdjąć tylko odcinając zasilanie. Dlatego Zastosuj trzyma poprzednią krzywą na dysku, próbuje kandydatkę przez **25 sekund** i czeka na potwierdzenie: naciśnij Zachowaj, żeby zapisać ją na dobre; w innym wypadku — albo jeśli płyta się zawiesi i sama zrestartuje — przy starcie wraca poprzednia krzywa.

## Regulator V/F grafiki

Taktowaniem grafiki zajmuje się **skillfish-vf-governor**, nasza usługa, która odbiera zegar i napięcie fabrycznemu regulatorowi i steruje nimi wprost przez SMU, trzymając **sufit częstotliwości**, który ciepło i pobór mocy mogą obniżyć, a gdy płyta się uspokoi — oddać z powrotem. Osobny proces, **skillfish-vf-watchdog**, przejmuje kontrolę, jeśli regulator padnie z wymuszonym taktowaniem.

Zmierzone na *Black Myth: Wukong*, ta sama sesja, te same 84 °C w obu przebiegach: **+4,5%** na zimnej płycie, **+11%** na rozgrzanej, względem fabrycznego regulatora. Przewaga rośnie z temperaturą, bo fabryczny regulator traci taktowanie w miarę nagrzewania się płyty, a nasz nie.

> Standardowe wpisy amdgpu w sysfs (`power_dpm_force_performance_level`, `pp_dpm_sclk`) **nie** sterują BC-250 — robi to wyłącznie skillfish-vf-governor. Grafika wchodzi na sufit tylko przy prawdziwym **nasyceniu obliczeniami graficznymi**.

## Podkręcanie i obniżanie napięcia procesora

Procesorem (**8 rdzeni / 16 wątków** Zen 2 „Oberon”, dwa z nich odblokowane przez SkillFishOS za pomocą SMU — także przed startem, programem EFI, w jednym restarcie) zajmuje się przy podkręcaniu jednorazowa usługa **`bc250-smu-oc.service`**, która nakłada wartości z `/etc/bc250-smu-oc.conf` przy pomocy projektu [bc250_smu_oc](https://github.com/bc250-collective/bc250_smu_oc). Po nałożeniu pokazuje się jako *inactive* — to normalne (jest jednorazowa).

Co zmierzyliśmy, przyciskając **naszą** płytę:

- **3700 MHz** z napięciem obniżonym do ~**1106 mV** (`scale −16`);
- **3900 MHz** przy ~**1199 mV** (`scale −24`);
- **4,0 GHz** zwalidowane przy ~**1224 mV** (`scale −36`) na 120 s ciągłego obciążenia, ze szczytem **83 °C** — użyteczne maksimum tego egzemplarza;
- **Twardy sufit Vid: 1,325 V** (nigdy nieprzekroczony).

**Obniżanie napięcia** nie polega na „przyciskaniu” — chodzi o wykonanie tej samej pracy przy **mniejszym cieple i mniejszym poborze**: przy danej częstotliwości obniżanie napięcia aż do granicy stabilności zbija temperaturę i zostawia zapas termiczny reszcie APU.

### Sprzężenie termiczne procesora i grafiki

Procesor i grafika dzielą **ten sam krzem** i **ten sam budżet mocy**. Pod obciążeniem **mieszanym** (wymagająca gra: procesor i grafika naraz) APU chroni samo siebie i procesor samoczynnie schodzi do ~**3450 MHz**, żeby zmieścić się w budżecie i pod 85 °C. **To nie jest wada**: układ chroni się, zrzucając najmniej przydatne megaherce. Z tego samego powodu obniżenie napięcia procesora zostawia więcej „miejsca” termicznego dla grafiki i odwrotnie.

## 40 jednostek obliczeniowych — na żywo

BC-250 ma **40 jednostek** (20 par), ale sterownik domyślnie włącza **24**. SkillFishOS podnosi je do 40 **przy starcie, bez dodatkowych kroków**; z [Tunera](/pl/docs/control-center) zmieniasz ich liczbę **na żywo**, wpisując żądaną wartość albo klikając na 20 sparowanych kwadratów. Pierwsze 24 jednostki są zablokowane przez sterownik i zawsze włączone.

Ze wszystkimi 40 jednostkami grafika osiąga **11385 GFLOPS** FP32 (vkpeak) na zimno, wobec ~**6141** przy bazowych 24 CU: **+85%**. Pod ciągłym obciążeniem (na gorąco) ustala się w okolicach **10214 GFLOPS**. Zmierzona przepustowość pamięci (clpeak) to **~350–367 GB/s**.

> **Loteria krzemowa.** Na odzyskanych układach „z odrzutu” część jednostek może być słaba. [Tuner](/pl/docs/control-center) ma **„Test CU”**, który obciąża każdą parę vkpeakiem i zgłasza błędy oraz zawieszenia grafiki, żebyś mógł potwierdzić, że twój układ utrzymuje wszystkie 40. (Mechanizm przez `umr`, zapisujący maski WGP — z podziękowaniem dla [bc250-cu-live-manager](https://github.com/WinnieLV/bc250-cu-live-manager), napisane od nowa.)

## Ochrona termiczna — limit 85 °C

Sufit termiczny to **85 °C**, pilnowany na dwóch poziomach:

1. **po stronie regulatora**: `gradi_max` i `watt_max` w `/etc/skillfish-vf-governor.json` obniżają sufit częstotliwości *zanim* przekroczy 85 °C albo limit mocy (nasz, nie firmware'u), i oddają go, gdy płyta się uspokoi;
2. **po stronie systemu**: **skillfish-vf-watchdog**, osobny proces, który przejmuje kontrolę, jeśli regulator padnie z wymuszonym taktowaniem.

O fabrycznym chłodzeniu warto wiedzieć (zobacz też [Sprzęt BC-250](/pl/docs/hardware-bc250) po **obudowy do druku 3D i zalecane wentylatory**):

- fabryczny radiator jest **na granicy**: porównania testów „jeden po drugim” są zafałszowane przez *heat-soak* — daj płycie ostygnąć kilka minut między przebiegami;
- istnieje tylko czujnik *krawędzi* grafiki; **czujnika temperatury VRAM nie ma**;
- przepustowość pamięci jest w porządku, ale `mclk` **nie** da się zmieniać.

## Prawdziwy przypadek: gry ograniczone procesorem

Niektóre tytuły — jak *Black Myth: Wukong* w **rozgrywce** — są **ograniczone procesorem i liczbą wywołań rysowania**: liczba klatek prawie nie zależy od rozdzielczości ani taktowania grafiki. Tam pomaga za to podkręcenie **procesora** i dobre chłodzenie. Jeśli chodzi o skalowanie obrazu, FSR 4 idzie przez [OptiScaler](https://github.com/optiscaler/OptiScaler) na ścieżce DLSS gry (zobacz [Gaming](/pl/docs/gaming)).

Kiedy obciążenie **jest** ograniczone grafiką (np. *przelot* z testu Wukonga), sufit krzywej ma znaczenie: w [Tunerze](/pl/docs/control-center) podnieś profil z Cautious albo Balanced na **Performance** (2100 MHz), albo wpisz własną krzywą. Zmierzona przewaga na teście Wukonga względem starego fabrycznego regulatora to **+4,5% na zimnej płycie i +11% na rozgrzanej**: regulator V/F nie traci taktowania w miarę nagrzewania, w przeciwieństwie do fabrycznego. Zostaje jednak twardy fizyczny limit: **1129 mV**, sufit napięcia, jaki amdgpu deklaruje dla tej grafiki — żadna krzywa go nie przekroczy.

## I to wszystko bez terminala

Taktowanie, krzywa grafiki, wentylator i jednostki obliczeniowe stroi się z okna **Tunera**, mając trzy gotowe profile grafiki i **automatyczną próbę 25 sekund z powrotem do poprzedniej krzywej**, jeśli twoja płyta jej nie utrzyma — zobacz [Control Center](/pl/docs/control-center). To zalecana droga: zacznij od Cautious, przejdź na Balanced albo Performance, a Tuner sprawdzi wszystko na **twojej** BC-250.

## Źródła

- skillfish-vf-governor — nasz regulator V/F dla grafiki, bezpośrednie sterowanie SMU z regulowanym sufitem
- [bc250_smu_oc (bc250-collective)](https://github.com/bc250-collective/bc250_smu_oc) — podkręcanie i obniżanie napięcia procesora przez SMU
- [bc250.info](https://bc250.info) — bezpieczne punkty i notatki termiczne od społeczności
- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) — testy FP32 i przepustowości pamięci

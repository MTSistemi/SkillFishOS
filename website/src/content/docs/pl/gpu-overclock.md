---
title: GPU, CPU, podkręcanie i obniżanie napięcia
description: Jak SkillFishOS steruje taktowaniem, napięciami i temperaturami BC-250 — z prawdziwymi liczbami zmierzonymi na sprzęcie.
group: System
order: 2
---

Na zwykłym APU taktowanie stroi się przez `amdgpu` w sysfs. Na BC-250 **to nie działa**: sterowanie idzie przez **SMU** (System Management Unit) i wymaga osobnych narzędzi. SkillFishOS ma je wszystkie w komplecie, z gotowymi bezpiecznymi profilami i systemem ochrony termicznej.

> **Uwaga:** **Loteria krzemowa.** Każda liczba na tej stronie jest **zmierzona na naszej BC-250**. Każdy egzemplarz jest inny: jeden przyjmie głębsze obniżenie napięcia, drugi mniejsze. Dlatego SkillFishOS **zawsze startuje w profilu Stock** i pozwala wspinać się wyżej [Tunerem](/pl/docs/app-native), który sprawdza każdy profil **na twojej płycie**, z automatycznym testem i cofnięciem zmian.

## Cztery profile

[Tuner](/pl/docs/app-native) udostępnia **cztery gotowe profile**. Obraz ISO startuje w **Stock**; do pozostałych jest jedno kliknięcie po teście.

| Profil | Procesor | Grafika | Uwagi |
|---|---|---|---|
| **Stock** *(domyślny w ISO)* | 3500 MHz | 1500 MHz | Maksymalna zgodność na dowolnej BC-250 |
| **Performance** | 3700 MHz · ~1106 mV | 2000 MHz | Zrównoważony i z obniżonym napięciem |
| **Turbo** | 3900 MHz · ~1199 mV | 2230 MHz | Mocny boost, zwalidowany pod limitem 85 °C |
| **Crazy** | 4,0 GHz · ~1224 mV | 2230 MHz | Zwalidowane maksimum (~83 °C pod obciążeniem) |

Wszystkie profile respektują ten sam **limit 85 °C** i trzymają **wentylator na auto**.

## Zarządca SMU dla grafiki

Taktowaniem grafiki steruje **[cyan-skillfish-governor](https://github.com/Magnap/cyan-skillfish-governor)** (napisany w Ruście), usługa systemowa konfigurowana w `/etc/cyan-skillfish-governor/config.toml`. Definiuje ona *bezpieczne punkty* częstotliwości i napięcia: **350 MHz / 700 mV** na bezczynności oraz wartość z profilu pod obciążeniem (np. 1500/900 w Stock, 2230/1000 w Turbo).

> Standardowe wpisy amdgpu w sysfs (`power_dpm_force_performance_level`, `pp_dpm_sclk`) **nie** sterują BC-250 — robi to wyłącznie zarządca SMU. Grafika wchodzi na taktowanie boost tylko przy prawdziwym **nasyceniu obliczeniami graficznymi**.

## Podkręcanie i obniżanie napięcia procesora

Procesorem (**8 rdzeni / 16 wątków** Zen 2 „Oberon”, dwa z nich odblokowane przez SkillFishOS za pomocą SMU) zajmuje się jednorazowa usługa **`bc250-smu-oc.service`**, która nakłada wartości z `/etc/bc250-smu-oc.conf` przy pomocy projektu [bc250_smu_oc](https://github.com/bc250-collective/bc250_smu_oc). Po nałożeniu pokazuje się jako *inactive* — to normalne (jest jednorazowa).

Co zmierzyliśmy, przyciskając **naszą** płytę:

- **3700 MHz** (profil *Performance*) z napięciem obniżonym do ~**1106 mV** (`scale −16`);
- **3900 MHz** (profil *Turbo*) przy ~**1199 mV** (`scale −24`);
- **4,0 GHz** (profil *Crazy*) zwalidowane przy ~**1224 mV** (`scale −36`) na 120 s ciągłego obciążenia, ze szczytem **83 °C** — użyteczne maksimum tego egzemplarza;
- **Twardy sufit Vid: 1,325 V** (nigdy nieprzekroczony).

**Obniżanie napięcia** nie polega na „przyciskaniu” — chodzi o wykonanie tej samej pracy przy **mniejszym cieple i mniejszym poborze**: przy danej częstotliwości obniżanie napięcia aż do granicy stabilności zbija temperaturę i zostawia zapas termiczny reszcie APU.

### Sprzężenie termiczne procesora i grafiki

Procesor i grafika dzielą **ten sam krzem** i **ten sam budżet mocy**. Pod obciążeniem **mieszanym** (wymagająca gra: procesor i grafika naraz) APU chroni samo siebie i procesor samoczynnie schodzi do ~**3450 MHz**, żeby zmieścić się w budżecie i pod 85 °C. **To nie jest wada**: układ chroni się, zrzucając najmniej przydatne megaherce. Z tego samego powodu obniżenie napięcia procesora zostawia więcej „miejsca” termicznego dla grafiki i odwrotnie.

## 40 jednostek obliczeniowych — na żywo

BC-250 ma **40 jednostek** (20 WGP, 1 WGP = 2 CU), ale sterownik domyślnie włącza **24**. SkillFishOS podnosi je do 40 **w czasie pracy, bez restartu**: system startuje na wartości bazowej sterownika (24 CU), a usługa doprowadza go do 40 przy uruchamianiu; z [Tunera](/pl/docs/app-native) zmieniasz ich liczbę **na żywo** siatką kwadratów i profilami 24/32/40. Pierwsze 24 jednostki są zablokowane przez sterownik i zawsze włączone.

Ze wszystkimi 40 jednostkami grafika osiąga **11385 GFLOPS** FP32 (vkpeak) na zimno, wobec ~**6141** przy bazowych 24 CU: **+85%**. Pod ciągłym obciążeniem (na gorąco) ustala się w okolicach **10214 GFLOPS**. Zmierzona przepustowość pamięci (clpeak) to **~350–367 GB/s**.

> **Loteria krzemowa.** Na odzyskanych układach „z odrzutu” część jednostek może być słaba. [Tuner](/pl/docs/app-native) ma **„Test CU”**, który obciąża każdą parę i zgłasza błędy oraz zawieszenia grafiki, żebyś mógł potwierdzić, że twój układ utrzymuje wszystkie 40. (Mechanizm przez `umr`, zapisujący maski WGP — z podziękowaniem dla [bc250-cu-live-manager](https://github.com/WinnieLV/bc250-cu-live-manager), napisane od nowa.)

## Ochrona termiczna — limit 85 °C

Sufit termiczny to **85 °C**, pilnowany na dwóch poziomach:

1. **po stronie SMU**: wartość `max_temperature` w konfiguracji sprawia, że układ obniża taktowanie *zanim* przekroczy 85 °C (co pozwala uniknąć twardego dławienia);
2. **po stronie systemu**: watchdog **thermal-guard**, który przy przekroczeniu limitu schodzi z taktowaniem po 100 MHz, aż wróci w normę.

O fabrycznym chłodzeniu warto wiedzieć (zobacz też [Sprzęt BC-250](/pl/docs/hardware-bc250) po **obudowy do druku 3D i zalecane wentylatory**):

- fabryczny radiator jest **na granicy**: porównania testów „jeden po drugim” są zafałszowane przez *heat-soak* — daj płycie ostygnąć kilka minut między przebiegami;
- istnieje tylko czujnik *krawędzi* grafiki; **czujnika temperatury VRAM nie ma**;
- przepustowość pamięci jest w porządku, ale `mclk` **nie** da się zmieniać.

## Prawdziwy przypadek: gry ograniczone procesorem

Niektóre tytuły — jak *Black Myth: Wukong* w **rozgrywce** — są **ograniczone procesorem i liczbą wywołań rysowania**: liczba klatek prawie nie zależy od rozdzielczości ani taktowania grafiki. Tam pomaga za to podkręcenie **procesora** i dobre chłodzenie. Jeśli chodzi o skalowanie obrazu, FSR 4 jest **niedostępne** (to sprzęt RDNA 4); użyj gamescope (FSR1/NIS) albo [OptiScalera](https://github.com/optiscaler/OptiScaler) dla wybranych gier.

Kiedy obciążenie **jest** ograniczone grafiką (np. *przelot* z testu Wukonga), taktowanie ma znaczenie: w **Tunerze** możesz przełączyć **zarządcę na „Wydajność”**, co trzyma grafikę na najwyższym bezpiecznym punkcie pod obciążeniem (na bezczynności nadal schodzi do 350 MHz). Zmierzone na teście Wukonga: **100 → 111 klatek średnio (+11%)**, 92 → 102 na najwolniejszych klatkach. Dla bezpieczeństwa Tuner ogranicza grafikę do **2200 MHz @ 1000 mV** (stabilne maksimum na fabrycznym chłodzeniu) z wielopunktową krzywą napięcia — 2230 MHz przy 1000 mV to już obniżone napięcie i może twardo zawiesić maszynę.

## I to wszystko bez terminala

Taktowanie, obniżanie napięcia, wentylator i jednostki obliczeniowe stroi się z okna **Tunera**, mając cztery gotowe profile i **automatyczny test z cofnięciem zmian**, jeśli twoja płyta nie utrzyma wartości — zobacz [Własne aplikacje](/pl/docs/app-native). To zalecana droga: zacznij od Stock, przejdź na Performance, spróbuj Turbo albo Crazy, a Tuner sprawdzi wszystko na **twojej** BC-250.

## Źródła

- [cyan-skillfish-governor (Magnap)](https://github.com/Magnap/cyan-skillfish-governor) — zarządca SMU dla grafiki
- [bc250_smu_oc (bc250-collective)](https://github.com/bc250-collective/bc250_smu_oc) — podkręcanie i obniżanie napięcia procesora przez SMU
- [bc250.info](https://bc250.info) — bezpieczne punkty i notatki termiczne od społeczności
- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) — testy FP32 i przepustowości pamięci

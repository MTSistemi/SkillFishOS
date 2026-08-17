---
title: Wydajność i testy
description: Wszystkie prawdziwe testy BC-250 na SkillFishOS — zrzuty ekranu, pełne ustawienia, taktowanie, napięcia, temperatury i pobór mocy.
group: Materiały
order: 3
---

To jest **pełny dział testów**: każdy przebieg wykonano na **naszej własnej BC-250** ze SkillFishOS, z prawdziwymi zrzutami ekranu, **wszystkimi użytymi ustawieniami** i telemetrią **taktowania, napięć, temperatur, poboru mocy i wentylatora** zapisaną w trakcie.

> **Uwaga:** **Loteria krzemowa + chłodzenie.** Te liczby dotyczą *tego* układu przy odpowiednim chłodzeniu. Fabryczne chłodzenie jest na granicy: porównania „jeden po drugim” bez przerw są zafałszowane przez *heat-soak* — daj płycie ostygnąć kilka minut między przebiegami.

## Warunki testów (stanowisko)

Dotyczą **wszystkich** poniższych testów, o ile nie napisano inaczej.

| Element | Wartość |
|---|---|
| Płyta | **AMD BC-250** — APU Zen 2 „Oberon” + RDNA 2 „Cyan Skillfish” (`gfx1013`) |
| Pamięć | **16 GB GDDR6** wspólne (UMA) |
| Jednostki obliczeniowe | **40 / 40 aktywnych** (podniesione na żywo, zobacz [GPU](/pl/docs/gpu-overclock)) |
| Jądro | **7.0.10-skillfishos** (linux-tkg) — wersja, przy której zebrano te liczby; dziś wydajemy **7.1.7**, przemierzone z różnicą poniżej 2% |
| Sterownik | **Mesa 26.0.8** — RADV (Vulkan) / radeonsi (OpenGL), ACO |
| Zarządca grafiki | cyan-skillfish — bezczynność **350 MHz / 700 mV**, obciążenie **2230 MHz / ~1000 mV** |
| Profil OC | **Turbo/Crazy** (limit grafiki 2230 MHz, procesor 3,9–4,0 GHz) |
| Limit termiczny | **85 °C** (SMU + thermal-guard), wentylator na **auto** |
| Rozdzielczość | **1920×1080** |

> Przypomnienie o budowie układu: procesor i grafika dzielą **ten sam krzem** i **ten sam budżet mocy**. Pod obciążeniem mieszanym procesor samoczynnie oddaje taktowanie (≈3,4–3,5 GHz), żeby zmieścić się w budżecie i pod 85 °C — to nie wada, tylko układ chroniący sam siebie.

---

## Black Myth: Wukong — 112 klatek (1080p)

![Black Myth: Wukong — średnio 112 klatek w 1080p na AMD BC-250](/img/benchmarks/wukong-112fps.jpg)

| Ustawienie | Wartość |
|---|---|
| Rozdzielczość | 1920×1080 |
| Limit klatek | brak |
| Rodzaj obciążenia | **ograniczone procesorem i wywołaniami rysowania** |
| Skalowanie obrazu | FSR 4 niedostępne (RDNA 4) → gamescope FSR1/NIS albo OptiScaler |

**Wynik:** średnio **112 klatek** · maks. **128** · min. **92** · 1% low **101**.

**Telemetria w trakcie przebiegu** (~4 min):

| Wskaźnik | Zmierzona wartość |
|---|---|
| Taktowanie grafiki | ~1,4–1,6 GHz (*bez nasycenia*: gra opiera się o procesor) |
| Krawędź grafiki | 83–86 °C |
| Pobór grafiki | ~90–140 W |
| Napięcie grafiki | ~970–987 mV |
| Taktowanie procesora | ~3,5 GHz (spadek z 3,9 przez wspólny budżet) |
| Temperatura procesora | 85 °C (na limicie) |
| VRAM | ~1,9 GB (menu) → ~4,4 GB (w grze) |
| Wentylator | ~2950–3140 obr./min |

> Wniosek: w *rozgrywce* w tytule ograniczonym wywołaniami rysowania, takim jak Wukong, najbardziej liczy się **stabilność procesora** pod obciążeniem i dobre chłodzenie.

### Zarządca: Zrównoważony kontra Wydajność (narzędzie testowe)

*Przelot* z narzędzia testowego jest **ograniczony grafiką**, więc tam taktowanie ma znaczenie. Po przełączeniu zarządcy na **Wydajność** w Tunerze (trzyma grafikę na najwyższym bezpiecznym punkcie pod obciążeniem, na bezczynności schodząc do 350 MHz):

| Tryb zarządcy | Średnia | 5%-low |
|---|---|---|
| **Zrównoważony** (domyślny) | 100 klatek | 92 klatki |
| **Wydajność** | **111 klatek** | **102 klatki** |

**+11%** na średniej i na najwolniejszych klatkach, samo z utrzymania wysokiego taktowania. Dla bezpieczeństwa Tuner ogranicza grafikę do **2200 MHz @ 1000 mV** z wielopunktową krzywą napięcia: 2230 MHz przy 1000 mV to już obniżone napięcie i może twardo zawiesić maszynę.

---

## Unigine Superposition — 1080p HIGH: 12938

![Unigine Superposition 1080p High — wynik 12938 na BC-250](/img/benchmarks/superposition-high.jpg)

| Ustawienie | Wartość |
|---|---|
| Wersja | 1.1 |
| API graficzne | **OpenGL** |
| Rozdzielczość | 1920×1080, pełny ekran |
| Cieniowanie | **High** |
| Tekstury | High |
| DOF | włączone |
| Motion Blur | włączone |

**Wynik:** **12 938** punktów · klatki min. **75,59** · śr. **96,77** · maks. **127,16**.
**Konfiguracja odczytana przez narzędzie:** procesor AMD BC-250 **@ 3894 MHz**, 7 GB pamięci, grafika AMD BC-250 8 GB (Cyan Skillfish), jądro 7.0.10-skillfishos.

---

## Unigine Superposition — 1080p EXTREME: 5513

![Unigine Superposition 1080p Extreme — wynik 5513 na BC-250](/img/benchmarks/superposition-extreme.jpg)

| Ustawienie | Wartość |
|---|---|
| Wersja | 1.1 |
| API graficzne | **OpenGL** |
| Rozdzielczość | 1920×1080, pełny ekran |
| Cieniowanie | **Extreme** |
| Tekstury | High |
| DOF | włączone |
| Motion Blur | włączone |

**Wynik:** **5513** punktów · klatki średnio **41,25** (min. ~32,8 · maks. ~49).

![Unigine Superposition — scena renderowana w czasie rzeczywistym](/img/benchmarks/superposition-scene.jpg)
*Scena z Superposition renderowana w czasie rzeczywistym na BC-250.*

---

## Unigine Heaven 4.0 — 113,7 klatki · wynik 2865

![Unigine Heaven 4.0 — 113,7 klatki, wynik 2865 na BC-250](/img/benchmarks/heaven-113fps.jpg)

| Ustawienie | Wartość |
|---|---|
| API graficzne | **OpenGL** |
| Rozdzielczość | 1920×1080, w oknie |
| Antyaliasing | **8×** |
| Jakość | **Ultra** |
| Teselacja | **Extreme** |

**Wynik:** **113,7 klatki** · wynik **2865** · min. **54,8** · maks. **219,5**.
**Platforma odczytana przez narzędzie:** Linux 7.0.10-skillfishos x86_64 · procesor AMD BC-250 ×12 · grafika gfx1013.

![Unigine Heaven — scena renderowana w czasie rzeczywistym](/img/benchmarks/heaven-scene.jpg)
*Scena z Heaven renderowana w czasie rzeczywistym na BC-250 w trakcie przebiegu.*

---

## Obliczenia na grafice — vkpeak (syntetyczne)

Przepustowość obliczeniowa Vulkana na **tej samej** płycie, przed odblokowaniem 40 jednostek i po nim.

| Wskaźnik | Bazowe 24 CU | SkillFishOS 40 CU |
|---|---|---|
| **FP32** skalarne | 6141 GFLOPS | **11 329** GFLOPS *(11 385 na zimno)* |
| FP16 vec4 | 12 260 | **22 685** |
| int8 dot-product | 24 550 GIOPS | **45 495** GIOPS |
| FP64 skalarne | 385 | ~640 |
| copy d2d (przepustowość wewnętrzna) | — | 191 GBPS |

Z 40 aktywnymi jednostkami: **+85%** w FP32 wobec wartości bazowej (≈**11,3 TFLOPS**). Na gorąco, pod ciągłym obciążeniem, ustala się w okolicach **10 214 GFLOPS**. Na bezczynności zarządca schodzi do 350 MHz, krawędź ~54 °C po obciążeniu.

## Przepustowość pamięci — clpeak

| Wskaźnik | Wartość |
|---|---|
| Zmierzona przepustowość GDDR6 | **~350–367 GB/s** |
| `mclk` do zmiany | **Nie** (stałe taktowanie pamięci) |
| Pamięć widziana przez Vulkana | ~13 GiB (z rozszerzonym GTT) |

---

## Profile Tunera — taktowanie, napięcia, temperatury

| Profil | Procesor | Napięcie procesora | Grafika | Szczyt temperatury |
|---|---|---|---|---|
| **Stock** *(domyślny w ISO)* | 3500 MHz | — | 1500 MHz | najniższy |
| **Performance** | 3700 MHz | ~1106 mV (`scale −16`) | 2000 MHz | zrównoważony |
| **Turbo** | 3900 MHz | ~1199 mV (`scale −24`) | 2230 MHz | < 85 °C (limit) |
| **Crazy** | 4,0 GHz | ~1224 mV (`scale −36`) | 2230 MHz | ~83 °C przy 120 s obciążenia |

- **Twarde maksimum Vid: 1,325 V** (nigdy nieprzekroczone).
- Limit 85 °C we wszystkich profilach; wentylator na auto; na bezczynności grafika siedzi na **350 MHz / 700 mV**.

## Odblokowanie 8 rdzeni — realne +20%

BC-250 przychodzi z **dwoma rdzeniami wyłączonymi programowo**: maska włączonych rdzeni w SMU pokazuje 3 z 4 rdzeni na CCX. SkillFishOS przepisuje ją i doprowadza procesor do **8 rdzeni / 16 wątków**, bez modyfikowanego BIOS-u.

Zmierzone przy tym samym uruchomieniu, przez wyłączanie i włączanie dwóch dodatkowych rdzeni w czasie pracy:

| Obciążenie | 6r/12w | 8r/16w | |
|---|---|---|---|
| kompresja `xz -T` | 6,41 s | **5,11 s** | **+20%** |
| wnioskowanie modelu na procesorze | 34,0 tok/s | **40,8 tok/s** | **+20%** |
| Temperatura | 66 °C | 68 °C | +2 °C |

Jest to +20%, a nie teoretyczne +33%: przepustowość pamięci i narzut wątków zjadają różnicę. To i tak **jedna piąta wydajności za darmo**.

### Podkręcanie przy wszystkich 8 rdzeniach

Zmierzone krok po kroku, każdy szczebel **stabilny, z zerem MCE**:

| Cel | Osiągnięte pod obciążeniem | Wynik | Temperatura | Wentylator |
|---|---|---|---|---|
| 3500 (kontrola) | 3475 | 5118 ev/s | 57 °C | — |
| 3700 | 3673 | 5410 | 62 °C | 50% |
| 3900 | 3872 | 5704 | 71 °C | 68% |
| **4000** | **3971** | **5849** | **81 °C** | **93%** |

**Stabilne maksimum: 4000 MHz**, +14% w wyniku wobec 3500 — osiągalne dopiero po naprawieniu sterowania wentylatorem. **Uwaga:** przy **łączonym obciążeniu procesora i grafiki** taktowanie ustala się na 3375–3492 MHz przy 86 °C: powyżej ~3900 ogranicza radiator, a nie krzem.

---

## Sprawdzenie termiczne (test obciążeniowy)

Dane zapisane podczas samoczynnej walidacji w Tunerze (test i cofnięcie zmian).

| Faza | Taktowanie | Temperatura | Uwagi |
|---|---|---|---|
| Bezczynność | procesor ~2,5 GHz · grafika 350 MHz | k10 46 °C · grafika 45 °C | w spoczynku |
| **Obciążenie procesora** (12 wątków, 120 s) | procesor **3,68–3,69 GHz** | k10 **85 °C** (na limicie) | liczba historyczna, sprzed odblokowania 8 rdzeni |
| **Obciążenie grafiki** (pętla vkpeak, 120 s) | grafika **2000 MHz** | krawędź do **86 °C** | przy 86 °C zarządca schodzi do 1819–1900 MHz (thermal-guard); procesor spada do ~2,2–2,4 GHz przez wspólny budżet |

---

## Porównania

**Ten sam sprzęt, zmieniony tylko system** — Superposition 1080p Extreme na **tej samej** BC-250:

| System | Wynik |
|---|---|
| **SkillFishOS** (grafika 2230 · procesor 3900, 40 CU) | **5513** |
| Inna dystrybucja (Bazzite, fabryczne taktowanie) | 4102 |

→ **+34% realnej wydajności** z dokładnie tego samego układu, dzięki 40 odblokowanym jednostkom, zarządcy dociskającemu 2230 MHz oraz podkręceniu i obniżeniu napięcia procesora.

**Wobec desktopowych Radeonów** (Superposition 1080p High): BC-250 ze SkillFishOS (**12 938**) dorównuje kartom **RX 6600 / 6600 XT** kosztującym 200+ €, mając surową moc obliczeniową **RX 6700** (~11,3 TFLOPS) — na płycie za jakieś 50 €.

---

## Narzędzia i metoda

| Narzędzie | Co mierzy |
|---|---|
| [vkpeak](https://github.com/nihui/vkpeak) | przepustowość FP32/FP16/int8 przez Vulkana |
| [clpeak](https://github.com/krrishnarraj/clpeak) | przepustowość pamięci i wydajność OpenCL |
| [sysbench](https://github.com/akopytov/sysbench) | obciążenie i test procesora (używany też przez Tuner) |
| [Unigine Superposition / Heaven](https://benchmark.unigine.com/) | graficzne testy OpenGL |
| MangoHud w grze | klatki i czasy klatek w prawdziwych grach |
| własna telemetria | taktowanie, temperatura, moc i wentylator przez sysfs `amdgpu`, `k10temp`, `nct6686` |

## Źródła

- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) · [sysbench](https://github.com/akopytov/sysbench) · [Unigine](https://benchmark.unigine.com/)
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock) — odblokowanie CU
- [bc250.info](https://bc250.info) — bezpieczne punkty i notatki termiczne od społeczności
- [OptiScaler](https://github.com/optiscaler/OptiScaler) — skalowanie obrazu dla wybranych gier

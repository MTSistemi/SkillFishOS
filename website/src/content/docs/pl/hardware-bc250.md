---
title: Sprzęt AMD BC-250
description: Płyta, jej APU, dane techniczne i znane wady sprzętowe.
group: Wprowadzenie
order: 2
---

**AMD BC-250** to niewielka płyta oparta na **półniestandardowym APU** o nazwach kodowych *Oberon* dla procesora i *Cyan Skillfish* dla grafiki — z tej samej rodziny krzemu co konsole AMD obecnej generacji. Produkowano ją do systemów kopiących (zwykle po kilka płyt w jednej obudowie), a dziś pojawia się na rynku wtórnym w niskich cenach.

## Najważniejsze dane

| Element | Szczegóły |
|---|---|
| **Procesor** | 8 rdzeni / 16 wątków **Zen 2** (płyta pokazuje 6; SkillFishOS odblokowuje pozostałe dwa przez SMU) („Oberon”), do **3,9 GHz** (Turbo), 4,0 GHz zwalidowane |
| **Grafika** | **RDNA 2** „Cyan Skillfish” (`gfx1013`), do **40 jednostek obliczeniowych** do odblokowania |
| **Pamięć** | **16 GB GDDR6** dzielone (UMA) między procesor i grafikę |
| **Moc obliczeniowa** | ~**11,3 TFLOPS** FP32 przy 40 CU / 2000 MHz (zmierzone vkpeakiem) |
| **Przepustowość pamięci** | ~350–367 GB/s (zmierzone clpeakiem) |
| **Wyjście obrazu** | 1× DisplayPort |

Pamięć jest **wspólna**: GDDR6 dzieli się między system i grafikę. Domyślnie około 8 GB przypisane jest jako VRAM, ale pod Linuksem przestrzeń graficzną można rozszerzyć przez **GTT** (Graphics Translation Table), dzięki czemu Vulkan widzi ~13 GiB pamięci — szczególnie przydatne przy modelach AI.

## Odblokowanie 8 rdzeni procesora

Płyta przedstawia się jako **6 rdzeni / 12 wątków**, ale fizycznych rdzeni jest **osiem**: dwa brakujące nie są uszkodzone, lecz wyłączone konfiguracją produktu. Zdradza to maska obecności rdzeni — na praktycznie każdej płycie odczytuje się z niej `0x77`, wartość **symetryczną**: po cztery rdzenie na kompleks, z czwartym wyłączonym w obu. Prawdziwy odsiew produkcyjny zostawiłby układ niesymetryczny, bo wady nie rozkładają się tak równo.

SkillFishOS przepisuje tę maskę przez **SMU** przy starcie i płyta wraca jako **8 rdzeni / 16 wątków**. Bez modyfikowanego BIOS-u, bez lutowania.

W usługę wbudowane są dwa zabezpieczenia: jeśli maska **nie** wynosi `0x77`, nie rusza niczego, bo inny układ może oznaczać, że rdzenie naprawdę wyłączono fabrycznie; a ciepły restart następuje **dopiero po** odczytaniu zapisu z powrotem i potwierdzeniu go, więc nie może wpaść w pętlę ponownych uruchomień.

> Zmierzone na naszej własnej płycie: **+20%** przy obciążeniach wielowątkowych. Przy słabo zrównoleglonych zadaniach nic to nie zmienia, czego zresztą należy się spodziewać — dwa dodatkowe rdzenie nie przyspieszą pojedynczego wątku.

Za inżynierię wsteczną odpowiada [bc250-core-unlock (rw-r-r-0644)](https://github.com/rw-r-r-0644/bc250-core-unlock): bez tej pracy ta funkcja by nie istniała.

## Odblokowanie 40 jednostek obliczeniowych

Grafika ma 40 jednostek, ale sterownik domyślnie włącza tylko **24**. SkillFishOS **podnosi je do 40 na żywo** (bez restartu): system startuje na wartości bazowej sterownika, a usługa doprowadza go do 40 przy uruchamianiu, z możliwością zmiany w [Tunerze](/pl/docs/app-native). Inżynieria wsteczna odblokowania jest udokumentowana w [bc250-40cu-unlock](https://github.com/duggasco/bc250-40cu-unlock); sterowanie w czasie pracy przez `umr` inspirowane jest projektem [bc250-cu-live-manager](https://github.com/WinnieLV/bc250-cu-live-manager) (napisane od nowa, bez zaglądania w kod).

> Przy 40 aktywnych jednostkach SkillFishOS mierzy **11385 GFLOPS** FP32 (vkpeak) na zimno, wobec ~6141 dla bazowej konfiguracji 24 CU: około **+85%**.

## Wady sprzętowe, o których warto wiedzieć

BC-250 to sprzęt „kopiący” użyty do czegoś innego: ma kilka ograniczeń, które SkillFishOS obchodzi programowo. Ich znajomość tłumaczy wiele decyzji w tym systemie.

### Zepsute wykrywanie podłączenia (HPD) w DisplayPort

Wykrywanie podłączenia monitora do złącza DisplayPort **nie działa**: płyta nie „widzi”, że podłączyłeś ekran. SkillFishOS rozwiązuje to osobnym demonem (`skillfish-dp-hotswap`), który wymusza wykrycie przy starcie i pilnuje zmian monitora w czasie pracy, oraz parametrem jądra `video=DP-1:e` jako zapasowym rozwiązaniem. Zobacz [Pulpit](/pl/docs/desktop) i [Rozwiązywanie problemów](/pl/docs/risoluzione-problemi).

### Zepsute wstrzymywanie ACPI

Wstrzymywanie (**s2idle jest zepsute**): płyta zasypia, ale **się nie budzi** i wymaga resetu. Wstrzymana maszyna jest też nieosiągalna zdalnie. Właśnie dlatego SkillFishOS **trwale wyłącza** wszystkie stany uśpienia (zobacz [Pulpit](/pl/docs/desktop)). To środek obowiązkowy.

### IOMMU nie do użycia

IOMMU na BC-250 jest niestabilne: **nigdy nie wolno go włączać**. System startuje zawsze bez IOMMU.

### Czujniki temperatury

Dostępny jest tylko czujnik temperatury *krawędzi* grafiki; **czujnika temperatury pamięci VRAM nie ma**. Fabryczne chłodzenie jest na granicy, więc porównania testów robione jeden po drugim są niemiarodajne (efekt *heat-soak*): pozwól płycie ostygnąć przez kilka minut między przebiegami.

## Chłodzenie, obudowy do druku 3D i wentylatory

BC-250 przychodzi **goła**, zaprojektowana pod górnicze stelaże z pięcioma 80-milimetrowymi wentylatorami *screamer* zasilanymi ze złącza rozdziału mocy. Użycie na biurku wymaga własnego chłodzenia. **Chłodzić trzeba dwie rzeczy**: radiator APU **oraz** kości **GDDR6**, które bardzo się grzeją i nie mają czujnika temperatury (zobacz [GPU i podkręcanie](/pl/docs/gpu-overclock)).

**Co działa (rady społeczności):**

- **2× wentylatory 120 mm o wysokim ciśnieniu statycznym** skierowane na radiator to najczęstszy układ biurkowy; bez obudowy można je położyć wprost na radiatorze (opaski zaciskowe przez żeberka).
- **Osobny wentylator na VRAM** jest mocno zalecany przy podkręcaniu: kości GDDR6 to najgorętszy punkt.
- Wentylator podłącza się do **4-pinowego złącza PWM** na płycie — SkillFishOS steruje nim przez `nct6686` (czujniki) i trzyma go na **auto**.

**Obudowy i tunele powietrza (darmowe pliki STL do druku 3D):**

| Model | Autor | Uwagi |
|---|---|---|
| [Console Style Case](https://www.thingiverse.com/thing:7172528) | Arthrimus | Obudowa „konsolowa” + komora zasilacza, tunel na **1× 120 mm** |
| [ASRock BC-250 Shell Case](https://www.printables.com/model/1228207-asrock-amd-bc-250-shell-case) | onemorecap | Zatrzaskowa skorupa, szybki montaż jednego wentylatora |
| [Yet Another BC-250 Fan Shroud](https://www.printables.com/model/1339540-yet-another-bc-250-fan-shroud) | ViRazY | Wlot **140 mm** + wylot **120 mm** |
| [Case ATX PSU & Fan Duct](https://www.printables.com/model/1616167-amd-bc-250-case-atx-psu-fan-duct) | ZMASLO | Pod zwykły zasilacz ATX, tunel, który nie uszkodzi chłodzenia |
| [Standard ATX PSU case](https://www.thingiverse.com/thing:7269520) | CatSiewDai | Pełna obudowa pod zasilacze ATX |
| [OC vRAM Fan Kit (remiks)](https://www.thingiverse.com/thing:7271946) | marccyberwiz | Zestaw wentylatora **dedykowany pamięci VRAM** pod podkręcanie |
| [NexGen3D — DIY Steam Machine (Bazzite)](https://www.printables.com/model/1499974-nexgen3d-diy-steam-machine-powered-by-bazzite) | NexGen3D | Pełna obudowa w stylu **Steam Machine** pod BC-250 |
| [NexGen3D — Steam Machine PRO (chłodzenie cieczą)](https://www.printables.com/model/1614131-nexgen3d-diy-steam-machine-pro-liquid-cooled-bc-25/files) | NexGen3D | Wersja **PRO chłodzona cieczą** (AIO) — maksymalne chłodzenie |
| [NexGen3D — AIO mount for BC-250](https://www.printables.com/model/1554003-nexgen3d-aio-mount-for-the-bc-250) | NexGen3D | Uchwyt do zamontowania **AIO** (chłodzenia cieczą) na BC-250 |

> Przewodnik po chłodzeniu: [Cooling Solutions — amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs/hardware/cooling/).

## Źródła

- [bc250.info](https://bc250.info) — wiki społeczności
- [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs) — dokumentacja techniczna (w tym [chłodzenie](https://elektricm.github.io/amd-bc250-docs/hardware/cooling/))
- [mothenjoyer69/bc250-documentation](https://github.com/mothenjoyer69/bc250-documentation) — notatki o sprzęcie i chłodzeniu
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock) — odblokowanie jednostek obliczeniowych
- [bc250_memcfg (fanoush)](https://github.com/fanoush/bc250_memcfg) — konfiguracja pamięci
- Sterownik jądra Linux `amdgpu` — [docs.kernel.org/gpu/amdgpu](https://docs.kernel.org/gpu/amdgpu/)

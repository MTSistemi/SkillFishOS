---
title: Słowniczek
description: Terminy techniczne SkillFishOS i BC-250, wyjaśnione pokrótce.
group: Materiały
order: 5
---

Terminy, które wracają w całej dokumentacji, każdy wyjaśniony w jednym zdaniu. W kolejności alfabetycznej oryginałów.

## Sprzęt i APU

**APU** — *Accelerated Processing Unit*: układ łączący procesor i grafikę na jednym krzemie. BC-250 nosi półniestandardowy układ AMD.

**BC-250** — płyta, na której działa SkillFishOS: APU Zen 2 + RDNA 2, 16 GB GDDR6, pierwotnie zrobiona do kopania kryptowalut.

**Cyan Skillfish** — nazwa kodowa **graficznej** części (GPU) APU w BC-250. Stąd nazwa „SkillFish”.

**Oberon** — nazwa kodowa **procesorowej** części (Zen 2) tego APU.

**Compute Unit (CU)** — bloki obliczeniowe grafiki. BC-250 ma ich 40, ale domyślnie pokazuje mniej: SkillFishOS **odblokowuje wszystkie** (zobacz [jądro](/pl/docs/kernel)).

**gfx1013** — identyfikator architektury grafiki w BC-250 (rodzina RDNA 2). Ma znaczenie, bo **ROCm go nie obsługuje** → używa się zamiast tego Vulkana.

**RDNA 2** — architektura graficzna AMD tej grafiki (ta sama rodzina co obecne konsole).

**Zen 2** — architektura procesorowa AMD w tym APU (**8 rdzeni / 16 wątków**: płyta pokazuje 6, SkillFishOS odblokowuje pozostałe dwa przez SMU).

**GDDR6** — rodzaj pamięci na płycie: szybka, tutaj **dzielona** między procesor i grafikę.

**UMA** — *Unified Memory Architecture*: procesor i grafika korzystają z **tej samej** puli pamięci (~16 GB GDDR6).

**GTT** — *Graphics Translation Table*: mechanizm pozwalający grafice używać pamięci systemowej poza wydzielonym VRAM-em. SkillFishOS go rozszerza, żeby Vulkan widział ~13 GiB (przydatne przy AI).

## Taktowanie, napięcia, temperatury

**SMU** — *System Management Unit*: mikrokontroler wewnątrz APU zarządzający taktowaniem i napięciami. Na BC-250 sterowanie idzie **wyłącznie** przez niego, a nie przez standardowe sysfs amdgpu.

**Zarządca SMU** — usługa (`cyan-skillfish-governor`) ustawiająca *bezpieczne punkty* częstotliwości i napięcia grafiki.

**sclk / mclk** — taktowanie **rdzenia** grafiki (sclk) i **pamięci** (mclk). Na BC-250 mclk **nie** da się zmieniać.

**Undervolt** — obniżenie napięcia przy tej samej częstotliwości: ta sama praca, **mniej ciepła i poboru**. Zobacz [GPU i podkręcanie](/pl/docs/gpu-overclock).

**Overclock (OC)** — podniesienie taktowania powyżej fabrycznego dla większej wydajności.

**Vid** — napięcie, o które układ prosi przy danej częstotliwości. Na BC-250 twardym maksimum jest **1,325 V**.

**Thermal-guard** — systemowy watchdog obniżający taktowanie po przekroczeniu 85 °C.

**Heat-soak** — nagromadzenie ciepła, które fałszuje testy robione „jeden po drugim”: daj płycie ostygnąć między przebiegami.

**Loteria krzemowa** — fakt, że każdy układ znosi inne podkręcenie i obniżenie napięcia: dlatego SkillFishOS sprawdza profile **na twojej** płycie.

## Oprogramowanie systemowe

**Debian sid** — gałąź *unstable* Debiana, zawsze świeża, ale podatna na regresje: podstawa SkillFishOS (zobacz [Aktualizacje](/pl/docs/aggiornamenti)).

**KDE Plasma 6** — używane środowisko pulpitu, ubrane w motyw steampunk.

**linux-tkg** — przepis na budowanie jądra (Frogging-Family), na którym opiera się dostrojone jądro SkillFishOS.

**Mesa / RADV** — otwartoźródłowe sterowniki graficzne; **RADV** to sterownik **Vulkana** używany przez grafikę BC-250.

**ROCm** — „oficjalny” stos obliczeniowy AMD: **nie** obsługuje gfx1013, więc się go nie używa.

**Vulkan** — API graficzne i obliczeniowe używane na BC-250 zarówno do grania, jak i do **AI** (Unsloth Studio).

**Btrfs** — system plików typu copy-on-write z migawkami, który daje „siatkę bezpieczeństwa” (zobacz [Dyski i migawki](/pl/docs/storage-snapshot)).

**Snapper** — narzędzie tworzące samoczynne migawki Btrfs przed aktualizacjami i po nich.

**grub-btrfs** — sprawia, że migawki pojawiają się w menu GRUB, do cofnięcia zmian przy starcie.

**Przypinanie APT** — trzymanie pakietu na sprawdzonej wersji, dla części kruchych na tym sprzęcie.

**reprepro** — narzędzie prowadzące podpisane repozytorium APT SkillFishOS.

**HPD** — *Hot-Plug Detect*: wykrywanie podłączenia monitora. Na BC-250 **zepsute** → demon `skillfish-dp-hotswap`.

**s2idle / suspend** — stany uśpienia ACPI: na BC-250 **zepsute**, dlatego wyłączone.

**IOMMU** — jednostka zarządzania pamięcią do wirtualizacji wejścia/wyjścia: na BC-250 niestabilna, **nigdy** nie włączana.

## Granie i AI

**Proton** — warstwa zgodności od Valve, uruchamiająca gry windowsowe na Linuksie przez Steama.

**gamescope** — mikrokompozytor Valve do grania (sesja „konsolowa”, skalowanie FSR1/NIS).

**EmuDeck / ES-DE** — instalator emulatorów i nakładka do emulacji.

**FSR / OptiScaler** — technologie **skalowania obrazu**. FSR 4 jest niedostępne (wymaga RDNA 4); używa się FSR1/NIS albo OptiScalera.

**Unsloth Studio** — silnik i interfejs lokalnej AI: uruchamia modele GGUF na grafice i wystawia API zgodne z OpenAI.

**qwen3:14b** — wzorcowy model AI, działający w całości na grafice.

**Tuner** — własna aplikacja SkillFishOS do strojenia sprzętu z testem i cofaniem zmian (zobacz [Własne aplikacje](/pl/docs/app-native)).

## Źródła

- [bc250.info](https://bc250.info) · [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- [dokumentacja amdgpu](https://docs.kernel.org/gpu/amdgpu/) · [Mesa / RADV](https://docs.mesa3d.org/drivers/radv.html)

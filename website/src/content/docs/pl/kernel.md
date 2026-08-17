---
title: Dostrojone jądro
description: Jądro linux-tkg z łatkami pod BC-250, parametry startowe i jądra, których lepiej unikać.
group: System
order: 1
---

Sercem optymalizacji SkillFishOS jest **jądro budowane na zamówienie** pod BC-250, oparte na [linux-tkg](https://github.com/Frogging-Family/linux-tkg) — przepisie od *Frogging Family*, który nakłada łatki nastawione na wydajność i granie.

## Wersja i łatki

Jądro SkillFishOS ma wersję **`7.1.7-skillfishos`** (seria 7.0 dobiegła końca). Poza standardowymi łatkami linux-tkg zawiera:

- łatkę **odblokowującą częstotliwości** BC-250 (zakres 350–2230 MHz);
- łatkę **40 CU**, która włącza wszystkie jednostki obliczeniowe grafiki;
- własną łatkę **RDSEED-quiet**, wyciszającą hałaśliwy komunikat jądra na tym sprzęcie.

Pakiet jądra (obraz + nagłówki) publikowany jest jako wydanie i jest **zablokowany** (`apt-mark hold`), żeby aktualizacja Debiana nie podmieniła go na jądro nieodpowiednie. Jest to domyślne jądro w GRUB-ie.

## Parametry startowe (cmdline)

Wiersz poleceń jądra wygląda tak, a każdy parametr ma dokładny powód:

```
mitigations=off
split_lock_detect=off
ttm.pages_limit=1572864
ttm.page_pool_size=1572864
```

| Parametr | Co robi |
|---|---|
| `mitigations=off` | wyłącza zabezpieczenia Spectre/Meltdown dla maksymalnej wydajności (na domowej konsoli to wybór do przyjęcia) |
| `ttm.pages_limit` / `ttm.page_pool_size` | sufit GTT liczony w stronach po 4 KiB: 1572864 = 6 GiB, dzięki czemu Vulkan widzi ~13 GiB między VRAM a GTT (przydatne przy AI). Kiedyś było to `amdgpu.gttsize`, przestarzałe od jądra 7.x: gdy ustawione są oba, sterownik słucha tego pierwszego i mówi o tym przy każdym starcie |
| `split_lock_detect=off` | wyłącza wykrywanie *split lock*, które inaczej dławi procesy wykonujące niewyrównane dostępy atomowe (a robią to gry i emulatory) |

> **A co z DisplayPort?** HPD na BC-250 jest zepsute (zobacz [sprzęt](/pl/docs/hardware-bc250)), ale SkillFishOS **nie** używa parametru `video=DP-1:e`: usługa `skillfish-dp-hotswap` pilnuje EDID i włącza wyjście z powrotem, gdy monitor wraca. To obejmuje również włączenie monitora po płycie, czego sam parametr nie załatwia.

> **Jednostki obliczeniowe na żywo.** SkillFishOS nie używa już parametru `amdgpu.bc250_cc_write_mode=3` (który przypinał 40 CU przy starcie i blokował zmiany w czasie pracy). System startuje teraz na wartości bazowej sterownika (24 CU), a usługa podnosi **40 CU na żywo** przy uruchamianiu; zmienisz je bez restartu z [Tunera](/pl/docs/app-native). Zobacz [GPU i podkręcanie](/pl/docs/gpu-overclock).

## Jądra, których lepiej unikać

Nie wszystkie świeże jądra działają dobrze na tym sprzęcie. W szczególności serie **6.15.0–6.15.6** oraz **6.17.8–6.17.10** znane są z problemów i lepiej ich unikać. SkillFishOS dostarcza własne, sprawdzone jądro właśnie po to, żeby ominąć te regresje — zobacz [Aktualizacje](/pl/docs/aggiornamenti).

## IOMMU

Jak zaznaczono na stronie o [sprzęcie](/pl/docs/hardware-bc250), **IOMMU na BC-250 nigdy nie wolno włączać**: jest niestabilne. Jądro startuje zawsze z wyłączonym IOMMU.

## Dlaczego własne jądro, a nie XanMod albo fabryczne

- **Fabryczne jądro Debiana** nie ma łatek pod BC-250 (odblokowanie częstotliwości, 40 CU) i idzie za wymienionymi wyżej regresjami.
- **linux-tkg** ułatwia nakładanie własnych łatek oraz wybór planistów i opcji nastawionych na granie.
- Budowanie go samodzielnie oznacza, że aktualizujemy jądro **tylko wtedy, gdy nowa wersja przynosi realną korzyść** — i po sprawdzeniu jej na sprzęcie.

## Źródła

- [linux-tkg (Frogging-Family)](https://github.com/Frogging-Family/linux-tkg)
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock)
- [parametry sterownika amdgpu](https://docs.kernel.org/gpu/amdgpu/module-parameters.html)
- [bc250.info](https://bc250.info) — notatki o jądrze i wierszu poleceń

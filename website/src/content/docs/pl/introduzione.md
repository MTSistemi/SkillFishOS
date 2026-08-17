---
title: Wprowadzenie
description: Czym jest SkillFishOS, dlaczego powstał i dla kogo jest przeznaczony.
group: Wprowadzenie
order: 1
---

**SkillFishOS** to dystrybucja Linuksa zaprojektowana i dostrojona pod jedną konkretną, nietypową płytę: **AMD BC-250**. Jest to gotowy do użytku system typu *konsola-pecet* — granie, emulacja, lokalna sztuczna inteligencja i codzienna praca na pulpicie — zbudowany na [Debianie](https://www.debian.org/) i [KDE Plasma 6](https://kde.org/plasma-desktop/), ze spójnym wyglądem w stylu steampunk od uruchomienia aż po pulpit.

## Filozofia

BC-250 powstała jako płyta do kopania kryptowalut i trafiła na rynek wtórny w bardzo niskich cenach. Pod radiatorem siedzi jednak **półniestandardowy APU AMD** z tej samej rodziny krzemu co konsole obecnej generacji: procesor Zen 2, grafika RDNA 2 i 16 GB GDDR6. Z odpowiednim oprogramowaniem staje się zaskakująco zdolną małą konsolą-pecetem.

Problem w tym, że doprowadzenie jej do porządnego działania pod Linuksem wymaga łatek na jądro, dedykowanego zarządcy częstotliwości, podkręcania, profili termicznych i długiej listy obejść sprzętowych. SkillFishOS istnieje po to, żeby **wykonać całą tę pracę raz** i dać system, który *„włącza się i działa najlepiej jak potrafi”*, bez potrzeby dotykania terminala.

> SkillFishOS nie rozprowadza gier ani ROM-ów: dostarcza **narzędzia** (Steam, EmuDeck, emulatory, nakładki). Treść dokładasz sam, legalnie.

## Dla kogo

Projekt narodził się z konkretnej, osobistej potrzeby: żeby **dzieci używały Linuksa i uczyły się go przy graniu**. Granie jest „marchewką”, która je przyciąga, a **automatyczne migawki** Btrfs są siatką bezpieczeństwa, dzięki której mogą grzebać bez strachu, że popsują system — gdy coś pójdzie nie tak, cofasz wszystko jednym kliknięciem z menu startowego.

SkillFishOS dobrze sprawdzi się więc u:

- każdego, kto ma **BC-250** i chce grać, nie zostając ekspertem od jądra Linuksa;
- **rodzin**, które chcą taniej konsoli będącej jednocześnie edukacyjnym pecetem;
- **majsterkowiczów**, którzy wolą zacząć od dostrojonej bazy, niż budować wszystko od zera.

## Co jest w środku, w skrócie

- **Dostrojone jądro** ([linux-tkg](https://github.com/Frogging-Family/linux-tkg)) z łatkami na BC-250: odblokowane 40 jednostek obliczeniowych, odblokowane częstotliwości, dedykowany zarządca SMU.
- **Pulpit KDE Plasma 6** z motywem steampunk (ikony, kursory, tapeta, systemowy HUD).
- **Gotowe do grania**: Steam, [gamescope](https://github.com/ValveSoftware/gamescope), [EmuDeck](https://www.emudeck.com/), [ES-DE](https://es-de.org/), [Heroic](https://heroicgameslauncher.com/), Proton.
- **Lokalna AI**: [Unsloth Studio](https://unsloth.ai/) przyspieszone przez Vulkan na zintegrowanej grafice — **5,1×** szybciej niż na procesorze, zmierzone.
- **Migawki Btrfs** ze [Snapperem](http://snapper.io/) i cofaniem zmian z menu GRUB.
- **Własne aplikacje**: *Tuner* (sterowanie sprzętem bez terminala) i panel *AI*.
- **Dedykowane, sprawdzone aktualizacje** z naszego repozytorium APT, żeby aktualizacje Debiana nie zaskakiwały.

Kolejne strony omawiają każdy z tych elementów szczegółowo.

## Źródła

- Dokumentacja społeczności BC-250 — [bc250.info](https://bc250.info)
- Dokumentacja AMD BC-250 (elektricm) — [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- Debian — [debian.org](https://www.debian.org/)
- KDE Plasma — [kde.org/plasma-desktop](https://kde.org/plasma-desktop/)

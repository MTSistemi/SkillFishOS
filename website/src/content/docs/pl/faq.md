---
title: Najczęściej zadawane pytania (FAQ)
description: Najczęstsze pytania o SkillFishOS i BC-250, z krótkimi odpowiedziami.
group: Materiały
order: 2
---

Szybkie odpowiedzi na najczęstsze pytania. Po szczegóły każda odpowiedź odsyła na właściwą stronę.

## Ogólne

**Czym jest SkillFishOS?**
Dystrybucją Linuksa (Debian + KDE Plasma 6) zaprojektowaną i dostrojoną pod płytę **AMD BC-250**: granie, emulacja, lokalna AI i praca na pulpicie, wszystko skonfigurowane z góry. Zobacz [Wprowadzenie](/pl/docs/introduzione).

**Na jakim sprzęcie działa?**
Płytą, pod którą jest zbudowany, jest **AMD BC-250** (APU Zen 2 + RDNA 2 „gfx1013”, 16 GB GDDR6) — i tam robi wszystko, co potrafi: 40 odblokowanych jednostek obliczeniowych, zarządca SMU, osiem rdzeni. Jest też edycja **Generic x86-64**, która działa na dowolnym pececie i w maszynie wirtualnej — ze zwykłym jądrem, przy czym elementy dotyczące tylko tej płyty same się chowają, zamiast zgłaszać błędy. Zobacz [Sprzęt BC-250](/pl/docs/hardware-bc250).

**Ile kosztuje? Czy jest otwartoźródłowy?**
Jest **darmowy**. Łączy otwarte oprogramowanie z wielu społeczności; kod projektu jest na [GitHubie](https://github.com/MTSistemi/SkillFishOS). Zobacz [Źródła](/pl/docs/fonti).

**Czy zawiera gry, ROM-y albo BIOS-y?**
Nie. SkillFishOS daje **narzędzia** (Steam, EmuDeck, emulatory, nakładki); treść dokładasz sam i legalnie. Zobacz [Granie](/pl/docs/gaming).

## Instalacja

**Jak to zainstalować?**
Wypal obraz ISO na pendrive i uruchom graficzny instalator **Calamares**. Wszystko myszą. Zobacz [Instalacja](/pl/docs/installazione).

**Czy mogę spróbować bez instalowania?**
Tak: obraz ISO jest **live**, możesz obejrzeć pulpit przed instalacją.

**Czy to skasuje mi dysk?**
Instalacja automatyczna („Wymaż dysk”) tak. Żeby zachować istniejące dane, użyj podziału ręcznego. SkillFishOS używa **Btrfs** z osobnymi podwoluminami: `@` na system, `@home` na twoje dane, a do tego `@cache`, `@log` i `@games`.

**Czy potrzebuję internetu?**
Do instalacji nie; przyda się później do Steama, aktualizacji i AI.

## Wydajność i podkręcanie

**Dlaczego startuje „wolno”, w profilu Stock?**
Dla bezpieczeństwa: każda BC-250 jest inna (*loteria krzemowa*). Profile podnosi się z **[Tunera](/pl/docs/app-native)**, który sprawdza wszystko na twojej własnej płycie. Zobacz [GPU i podkręcanie](/pl/docs/gpu-overclock).

**Czy podkręcanie jest niebezpieczne?**
Tuner nakłada profil, **testuje** go i **cofa**, jeśli płyta sobie nie radzi; limit 85 °C i zabezpieczenie termiczne są zawsze włączone. Zaprojektowano to tak, żeby było bezpieczne.

**Ile klatek w grze X?**
To zależy: niektóre gry są **ograniczone procesorem** (np. *Black Myth: Wukong*) i nie skalują się z grafiką. Zobacz [Wydajność i testy](/pl/docs/prestazioni).

**Czy mogę użyć FSR 4?**
Nie, wymaga sprzętu RDNA 4. Skorzystaj z gamescope (FSR1/NIS) albo OptiScalera. Zobacz [Granie](/pl/docs/gaming).

## Codzienne używanie

**Dlaczego ekran bywa czarny?**
Na BC-250 **zepsute jest wykrywanie podłączenia (HPD) w DisplayPort**: SkillFishOS obchodzi to własnym demonem. Używaj monitora DP albo przejściówki **pasywnej**. Zobacz [Rozwiązywanie problemów](/pl/docs/risoluzione-problemi).

**Dlaczego nie ma dźwięku z telewizora?**
Zwykle winna jest **aktywna** przejściówka DP→HDMI: użyj pasywnej, monitora z DP, przetwornika USB albo dźwięku przez Bluetooth.

**Czy mogę uśpić komputer?**
Nie. **Wstrzymywanie jest zepsute** na poziomie sprzętu i płyta się nie obudzi: SkillFishOS wyłącza je celowo. **Nie włączaj go z powrotem.** Zobacz [Pulpit](/pl/docs/desktop).

**Czy mogę korzystać z niego z innego komputera?**
Tak: domyślna sesja to X11 i działa **x11vnc**, więc pulpitem można sterować przez VNC w sieci lokalnej. Zobacz [Pulpit](/pl/docs/desktop).

## Lokalna AI

**Jakiego modelu AI mogę użyć?**
Silnikiem jest **Unsloth Studio** na **Vulkanie** (nie ROCm, nieobsługiwanym na gfx1013), a modele to pliki GGUF pobierane z Hugging Face. Zmierzone na płycie: **210,7 tok/s** przy generowaniu wobec 41,5 na procesorze. Zobacz [Lokalna AI](/pl/docs/ai-locale).

**Czy mogę grać przy włączonej AI?**
Nie: AI i wymagające gry dzielą tę samą grafikę i pamięć. Wyłącz silnik AI, zanim siądziesz do grania.

## Aktualizacje

**Jak zaktualizować system?**
`sudo apt update && sudo apt full-upgrade` albo aplikacją **Discover**. Migawka powstaje samoczynnie przed każdą aktualizacją i po niej. Zobacz [Aktualizacje](/pl/docs/aggiornamenti).

**Aktualizacja coś zepsuła — co teraz?**
Uruchom ponownie i wybierz migawkę z **GRUB → „SkillFishOS snapshots”**. Zobacz [Dyski i migawki](/pl/docs/storage-snapshot).

**Czy Debian aktualizuje jądro?**
Nie: jądro SkillFishOS jest **zablokowane** (`apt-mark hold`) i aktualizowane tylko z naszego sprawdzonego repozytorium. Zobacz [Jądro](/pl/docs/kernel).

## Projekt

**Czy mogę pomóc albo zgłosić błąd?**
Tak, przez **Issues** na [GitHubie](https://github.com/MTSistemi/SkillFishOS/issues).

**Skąd pobrać obraz ISO?**
Ze strony [Pobieranie](/pl/download) (pliki na SourceForge).

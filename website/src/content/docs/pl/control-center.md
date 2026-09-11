---
title: "Control Center"
description: "Wszystkie narzędzia SkillFishOS w jednym oknie: Tuner, Wentylator, Monitor, Gry, Profile, Jądro, Migawki, AI, Emulatory, Konsola, ISO."
group: Używanie
order: 4
---

Wszystkie narzędzia SkillFishOS mieszczą się w jednym oknie. Otwiera się z menu (SkillFishOS → Control Center) albo poleceniem `skillfish-control-center`. Obsłuży je też kontroler: krzyżak lub gałka do poruszania, A potwierdza, B cofa, LB i RB zmieniają sekcję.

## Sekcje

- **Stan**: jedna liczba na kartę: zegar i sufit GPU, CPU, jednostki obliczeniowe, wentylator, jądro, governor, sterownik Vulkan, czy ostatni start nastąpił po czystym zamknięciu. Tu niczego się nie ustawia.
- **Tuner**: krzywa napięcie/częstotliwość governora GPU, CPU, rdzenie, jednostki obliczeniowe, VRAM.
- **Wentylator**: krzywa wentylatora z wyprzedzeniem, czujniki źródłowe, limity bezpieczeństwa, test PWM.
- **Monitor**: wszystkie odczyty, jeden wykres na jednostkę, plus słupki zegara na wątek. REC nagrywa, CSV eksportuje.
- **Gry**: nasza Mesa per launcher albo dla całego systemu, planista scx_bpfland, FSR 4, instalacja i domyślny GE-Proton.
- **Profile**: sufit, CPU, wentylator i planista jednym kliknięciem; zapisz własne.
- **Jądro**: zainstalowane jądra, domyślne, uruchom raz, odinstaluj.
- **Migawki**: migawki systemu i zaplanowana konserwacja btrfs.
- **AI**: Unsloth Studio na Vulkanie: silnik, aktualizacja, modele z Hubu Hugging Face, próbny czat, pamięć i sieć.
- **Emulatory**: EmuDeck albo emulatory pojedynczo z Flathuba.
- **Konsola**: Steam Big Picture w gamescope, teraz albo z ekranu logowania.
- **ISO**: obrazy dysków montowane przez udisks.

## Tuner

Krzywa jest wykresem: MHz w poziomie, miliwolty w pionie. Przeciągnij punkt, dwuklik dodaje punkt, prawy przycisk go usuwa, albo wpisz liczby w tabeli obok wykresu (+ i − dodają i usuwają punkty). Pionowa przerywana linia to sufit, niebieska kropka to GPU w tej chwili. Trzy presety: **Cautious 1850** (optymalny punkt z fabrycznym radiatorem, prawie te same klatki i dziesięć stopni mniej), **Balanced 2000**, **Performance 2100** (krzywa z piętnastu punktów zmierzona na płycie deweloperskiej, ta, którą wysyłamy).

**Zastosuj to próba.** Krzywa, która żąda za mało napięcia, zawiesza płytę, a na BC-250 zawieszenie leczy się wyjęciem wtyczki. Dlatego Zastosuj uruchamia kandydatkę, gdy poprzednia krzywa wciąż jest na dysku, i odlicza 25 sekund: naciśnij Zachowaj, a kandydatka zostanie zapisana na dobre; nic nie rób, albo płyta padnie i wróci, a wystartuje poprzednia krzywa.

Panele otwierają się na żądanie:

- **CPU**: zegar, stopień undervoltu (po 6,25 mV) i limit termiczny, każdy z suwakiem i polem liczbowym o kroku 1. *Zasugeruj UV* schodzi undervoltem po dwa stopnie z dwunastoma sekundami obciążenia na stopień; *Znajdź maksimum* wspina się od 3600 do 4000 MHz; *Test 60 s* obciąża bieżące wartości. Każdy przebieg pokazuje odliczanie i przycisk Stop; testowane wartości nigdy nie trafiają na dysk, więc zawieszenie startuje z poprzednimi. Powyżej 3500 MHz z ośmioma rdzeniami zysku nie ma: rządzi ciepło.
- **Rdzenie**: które rdzenie są włączone, SMT, odblokowanie 8 rdzeni (6c/12t staje się 8c/16t, zmierzone +20 %) oraz *Przed startem (EFI)*: odblokowanie wykonane przed GRUB-em w jednym starcie zamiast dodatkowego restartu usługi w systemie.
- **CU**: 40 jednostek obliczeniowych jako 20 komórek (pary): zielona włączona, czerwona wyłączona, szara trzymana przez sterownik. Wpisz, ile CU chcesz (24 do 40, parami) albo klikaj komórki; *Test CU* włącza dodatkowe pary pojedynczo pod vkpeak i zgłasza błędy, na loterię krzemową.
- **VRAM**: podział UMA w CMOS, stosowany przy następnym starcie. Przy dynamicznych 512 MB niektóre gry wybierają niskie tekstury: jeśli są rozmyte, spróbuj 4 lub 6 GB na stałe. Od 512 MB do 12 GB, z gotowymi wartościami 512 MB, 1, 2, 4, 6 i 8 GB.
- **Zaawansowane**: pokrętła samego governora: margines przy wchodzeniu, stopień, potwierdzenia przy schodzeniu, progi termiczne i mocy, droop.
- **Test**: vkpeak i dziennik pomocnika.

## Monitor

Jeden wykres na wielkość, każdy z własną prawdziwą skalą: temperatury (CPU, GPU, VRM, system, NVMe), zegary (CPU średni, min, max, GPU i jego sufit), obciążenie, moc, napięcia, wentylator i pamięć (RAM, VRAM, GTT), plus jeden słupek na wątek. Kliknij wpis legendy, żeby ukryć linię; najedź myszą, żeby odczytać wszystkie wykresy w tej samej chwili. REC zapisuje plik `.sfmon` (CSV), który Otwórz wczytuje z suwakiem; CSV eksportuje go do arkusza.

## Gry

- **Sterownik Vulkan**: nasza Mesa otwiera kolejki obliczeniowe, które fabryczny sterownik trzyma zamknięte na tym GPU: +4 % w Cyberpunk 2077, +12 % z FSR 4. Per launcher (Steam, Heroic) przez override flatpaka albo dla całego systemu. Wymaga jądra SkillFishOS: na innym jądrze te kolejki zawieszają GPU, a przełącznik systemowy odmawia tam startu. Karta pokazuje działające jądro.
- **Planista**: scx_bpfland, ładowany tylko gdy działa gra (GameMode go podnosi i zdejmuje): +1,5-2 % w Cyberpunk i równiejsze klatki. Jeśli jądro wyrzuci go dwa razy, usługa zatrzymuje się do wyzerowania licznika: to wiersz „Wyrzucony przez jądro”.
- **FSR 4**: przez OptiScaler na ścieżce DLSS gry. GE-Proton 11 sam pobiera OptiScaler, gdy znajdzie `PROTON_USE_OPTISCALER=1`, grę trzeba ustawić na DLSS, a biblioteka FSR 4 AMD (`amdxcffx64.dll`, ze sterownika Windows AMD) idzie obok gry. XeSS, tam gdzie gra ma go wbudowanego, kosztuje tyle co FSR 3 w 1080p.
- **Proton**: wydania GE-Proton 11; Zainstaluj pobiera jedno (około 500 MB) do folderów Steam i Heroic, Domyślny je wybiera. Steam musi być zamknięty, żeby jego domyślny został zapisany.

## AI

Silnikiem jest **Unsloth Studio**: uruchamia modele GGUF przez llama.cpp na backendzie **Vulkan**, który na gfx1013 w BC-250 jest jedyną przyspieszaną drogą, bo ROCm jej nie obsługuje. Zmierzone na płycie z Qwen3-1.7B Q4_K_M: 210 tokenów na sekundę wobec 41 na samym CPU.

- **Silnik**: włączony, wyłączony, przy starcie. Włączony zajmuje pamięć GPU, więc wyłącza się go przed graniem. Obok są wersja, sprawdzanie aktualizacji i *Aktualizuj*, które ponownie uruchamia oficjalny instalator z pakietem Vulkan dla llama.cpp.
- **Dostęp**: Unsloth przy instalacji tworzy losowe hasło i wyłącza się sam po godzinie, jeśli hasło nie zostanie zmienione. Pierwsze logowanie odbywa się tutaj: wybierasz hasło do Studio, a klucz API powstaje razem z nim i trafia też do Remote Managera.
- **Modele**: te na dysku, z kwantyzacją i rozmiarem. Żeby pobrać model, potrzebna jest nazwa repozytorium na Hugging Face (na przykład `unsloth/Qwen3-4B-GGUF`) i wariant wybrany z listy, z rozmiarami.
- **Czat**: szybka próba na API zgodnym z OpenAI (`http://127.0.0.1:8888/v1`), ze zmierzonymi tokenami na sekundę. Pełny czat, z plikami i wyszukiwaniem, jest w Studio.
- **Pamięć**: VRAM, GTT, RAM, swap i budżet modelu. Limit GTT to parametr jądra: działa od następnego startu.
- **Sieć**: otwarty w sieci lokalnej Studio odpowiada też innym urządzeniom w domu, z własnym użytkownikiem i hasłem. Równoległe czaty to sloty llama-server.

## Wentylator, profile i reszta

Strona **Wentylator** rysuje krzywą wewnątrz wykresu czujników: w tej temperaturze wentylator kręci się tak, z wyprzedzeniem, żeby obroty rosły przed temperaturą. **Profile** przesuwają sufit w obrębie istniejącej krzywej i ustawiają razem CPU, preset wentylatora i planistę. **Migawki** to zdjęcia systemu, twoje pliki pozostają nietknięte. **AI** trzyma pamięć GPU, dopóki jest włączone: wyłącz przed graniem. **Konsola** uruchamia Steam Big Picture w gamescope nad pulpitem albo jako sesję z ekranu logowania. **Remote Manager** odwzorowuje strony Tuner, Gry i Profile w przeglądarce.

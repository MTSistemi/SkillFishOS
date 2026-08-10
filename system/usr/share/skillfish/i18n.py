# -*- coding: utf-8 -*-
"""Traduzioni condivise delle app native di SkillFishOS.

Spedito da `skillfish-base` in /usr/share/skillfish/i18n.py.

Perche' un modulo unico: con sei app che duplicavano lo stesso dizionario, alla
seconda lingua erano dodici copie che divergevano. Qui la tabella e' una sola.

Le chiavi sono le stringhe **inglesi** passate a L(it, en): cosi' la firma non
cambia rispetto alle app bilingui e una stringa non ancora tradotta ricade
sull'inglese invece di sparire.

Uso normale:

    import sys
    sys.path.insert(0, "/usr/share/skillfish")
    from i18n import LANG, make_L
    L = make_L()

Se una stringa ha bisogno di una resa diversa in una app (stesso inglese, altro
contesto), si passa un override locale:

    L = make_L({"pl": {"off": "wy\u0142."}})

Le app devono importarlo dentro un try/except: sono pacchetti .deb separati e
possono trovarsi su un sistema dove skillfish-base non e' installato.

Polacco: **Cyryl Sochacki** (github.com/cyryllo).
Ucraino: ancora da scrivere, non abbiamo un madrelingua. Finche' la tabella e'
vuota un utente ucraino vede l'inglese.
"""
import os

SUPPORTED = ("it", "en", "pl", "uk")


def _detect_lang():
    # Ordine standard dei locale: LC_ALL batte LC_MESSAGES batte LANG;
    # LANGUAGE (la lista con i due punti di gettext) e' l'ultimo ripiego.
    val = (os.environ.get("LC_ALL") or os.environ.get("LC_MESSAGES")
           or os.environ.get("LANG") or os.environ.get("LANGUAGE") or "")
    v = val.lower()
    for code in ("it", "pl", "uk"):
        if v.startswith(code):
            return code
    return "en"


LANG = _detect_lang()

PL = {
    "\nThis cannot be undone. Continue?": "\nTej operacji nie można cofnąć. Kontynuować?",
    "\n⚠ It's the default kernel: the default will move to the running one.": "\n⚠ To domyślny kernel: domyślny zostanie ustawiony na uruchomiony.",
    "  (coming)": "  (wkrótce)",
    "  · at boot: ": "  · przy starcie: ",
    "(expected ~11300 at 40 CU)": "(oczekiwane ~11300 przy 40 CU)",
    "(not installed)": "(nie zainstalowano)",
    "+ Add repository": "+ Dodaj repozytorium",
    "40 CU (max)": "40 CU (maks.)",
    "40 CU under load (vkpeak): %s GFLOPS%s": "40 CU pod obciążeniem (vkpeak): %s GFLOPS%s",
    "ACCESS": "DOSTĘP",
    "APT repositories": "Repozytoria APT",
    "Accessibility": "Dostępność",
    "Action": "Akcja",
    "Active CUs: %d / 40": "Aktywne CU: %d / 40",
    "Add": "Dodaj",
    "Add APT repository": "Dodaj repozytorium APT",
    "Adding the repository…": "Dodawanie repozytorium…",
    "Adventure": "Przygodowe",
    "All": "Wszystkie",
    "All sources": "Wszystkie źródła",
    "Amount of system RAM reserved for the GPU (UMA).\n\n⚠ Writes to the BIOS CMOS and requires a REBOOT to apply. Reversible by clearing the CMOS (jumper on the board).\n\nDon't exceed values that leave too little RAM for the system.": "Ilość pamięci RAM systemu zarezerwowanej dla GPU (UMA).\n\n⚠ Zapisuje w CMOS-ie BIOS-u i wymaga PONOWNEGO URUCHOMIENIA, aby zastosować zmiany. Odwracalne przez wyzerowanie CMOS-u (zworka na płycie).\n\nNie przekraczaj wartości, które zostawiają systemowi zbyt mało RAM-u.",
    "Apply": "Zastosuj",
    "Apps & packages": "Aplikacje i pakiety",
    "Arcade": "Zręcznościowe",
    "Archiving": "Archiwizacja",
    "Astronomy": "Astronomia",
    "Authentication cancelled or helper not started.\nRestart the program and authorize the operation.": "Uwierzytelnienie anulowane lub pomocnik nie został uruchomiony.\nUruchom program ponownie i autoryzuj operację.",
    "Auto rules": "Reguły automatyczne",
    "BC-250 · znver2 · optimized": "BC-250 - znver2 - zoptymalizowany",
    "Backend updated. Reloading…": "Backend zaktualizowany. Ponowne wczytywanie…",
    "Backends": "Backendy",
    "Balanced": "Zbalansowany",
    "Baseline 24 CU: %s GFLOPS": "Bazowo 24 CU: %s GFLOPS",
    "Biology": "Biologia",
    "Board": "Planszowe",
    "Boot once": "Uruchom raz",
    "Browsers": "Przeglądarki internetowe",
    "Building": "Budowanie",
    "CATEGORIES": "KATEGORIE",
    "CPU %d MHz @ %d  ·  GPU %d MHz @ %d mV  ·  Active CUs: %d  ·  Detected freezes: %d": "CPU %d MHz @ %d  ·  GPU %d MHz @ %d mV  ·  Aktywne CU: %d  ·  Wykryte zawieszenia: %d",
    "CPU applied": "CPU zastosowane",
    "CPU boost limit in MHz.\n\n• 3500 = safe base\n• 3700 = verified stable on this chip\n• 3800-3900 = beyond limits, possible thermal throttling\n\nVoltage (Vid) always stays below 1.325 V for safety.": "Limit boostu CPU w MHz.\n\n• 3500 = bezpieczna baza\n• 3700 = zweryfikowana stabilność na tym układzie\n• 3800-3900 = poza limitami, możliwy throttling termiczny\n\nNapięcie (Vid) zawsze pozostaje poniżej 1,325 V dla bezpieczeństwa.",
    "CPU saved at boot": "CPU zapisane przy starcie",
    "CPU temperature limit": "Limit temperatury CPU",
    "CPU test: applying and benchmarking 60s (for a realistic temp)…": "Test CPU: stosuję ustawienia i uruchamiam benchmark 60 s (dla realistycznej temperatury)…",
    "CPU wizard result": "Wynik kreatora CPU",
    "CU error: %s": "Błąd CU: %s",
    "CU test": "Test CU",
    "CU test failed: %s": "Test CU nieudany: %s",
    "CU test result": "Wynik testu CU",
    "CU test running (~2-3 min)…": "Test CU w toku (~2-3 min)…",
    "CUs applied: %s/40 (live)": "CU zastosowane: %s/40 (na żywo)",
    "CUs are the GPU's compute cores. Here you enable/disable them LIVE, no reboot.\n\n• Each square = 1 CU: GREEN = active, RED = off.\n• CLICK a pair to toggle it manually (pairs are managed 2 CU at a time = 1 WGP).\n• Or use the PRESETS (24 / 32 / 40 CU).\n• The first 3 pairs per row (24 CU) are the driver minimum and stay always on.\n• Hit «Apply live» to make the choice effective.\n\nMore CU = more graphics power but also more heat and power draw.\n\nUse «Test CU» to verify the active CUs are stable and defect-free (silicon lottery).": "CU to rdzenie obliczeniowe GPU. Tutaj włączasz/wyłączasz je NA ŻYWO, bez restartu.\n\n• Każdy kwadracik = 1 CU: ZIELONY = aktywna, CZERWONY = wyłączona.\n• KLIKNIJ parę, aby przełączyć ją ręcznie (pary zarządzane są po 2 CU naraz = 1 WGP).\n• Albo użyj PRESETÓW (24 / 32 / 40 CU).\n• Pierwsze 3 pary w każdym rzędzie (24 CU) to minimum sterownika i zawsze pozostają aktywne.\n• Naciśnij «Zastosuj na żywo», aby uaktywnić wybór.\n\nWięcej CU = więcej mocy graficznej, ale też więcej ciepła i poboru energii.\n\nUżyj «Test CU», aby sprawdzić, czy aktywne CU są stabilne i wolne od defektów (loteria krzemowa).",
    "Calculators": "Kalkulatory",
    "Calendar": "Kalendarz",
    "Cancel": "Anuluj",
    "Card": "Karciane",
    "Channel:": "Kanał:",
    "Checking for updates…": "Sprawdzanie aktualizacji…",
    "Chemistry": "Chemia",
    "Choose the boot kernel or remove the ones you don't need": "Wybierz kernel startowy lub usuń te, które są niepotrzebne",
    "Clocks": "Zegary",
    "Close": "Zamknij",
    "Components": "Komponenty",
    "Compute Units (CU)": "Jednostki obliczeniowe (CU)",
    "Compute Units (CU) — live": "Jednostki obliczeniowe (CU) — na żywo",
    "Computer science": "Informatyka",
    "Controls": "Sterowanie",
    "Debugger": "Debugowanie",
    "Desktop (KVM)": "Pulpit (KVM)",
    "Development": "Programowanie",
    "Dictionaries": "Słowniki",
    "EXPOSED MODULES": "UDOSTĘPNIONE MODUŁY",
    "Editing": "Edycja",
    "Editor's choice": "Wybór redakcji",
    "Education & science": "Edukacja i nauka",
    "Everything is up to date ✓": "Wszystko aktualne ✓",
    "Explore": "Odkrywaj",
    "Extreme preset": "Ekstremalny preset",
    "Fan": "Wentylator",
    "Fan (RPM)": "Wentylator (RPM)",
    "Fan error": "Błąd wentylatora",
    "Featured · SkillFishOS": "Polecane · SkillFishOS",
    "Fetching ratings (ODRS)…": "Pobieranie ocen (ODRS)…",
    "File managers": "Menedżery plików",
    "File transfer": "Przesyłanie plików",
    "Filesystem": "System plików",
    "Filter:": "Filtr:",
    "Finance": "Finanse",
    "Find my max": "Znajdź maksimum",
    "Find my max (CPU)": "Znajdź maksimum (CPU)",
    "Flatpak remotes": "Zdalne repozytoria Flatpak",
    "Frequency": "Częstotliwość",
    "Frequency (MHz)": "Częstotliwość (MHz)",
    "GPU applied": "GPU zastosowane",
    "GPU governor mode": "Tryb governora GPU",
    "GPU test: applying and running vkpeak…": "Test GPU: stosuję ustawienia i uruchamiam vkpeak…",
    "GPU voltage (mV)": "Napięcie GPU (mV)",
    "Games": "Gry",
    "Generic · x86-64 · PCs & virtual machines": "Generic - x86-64 - PC i maszyny wirtualne",
    "Geography": "Geografia",
    "Governor mode": "Tryb governora",
    "Governor: Balanced": "Governor: Zbalansowany",
    "Governor: Performance — 2230 MHz under load": "Governor: Performance — 2230 MHz pod obciążeniem",
    "Graphics": "Grafika",
    "Help": "Pomoc",
    "Highest stable point: %d MHz @ 1000 mV%s (already applied).": "Najwyższy stabilny punkt: %d MHz @ 1000 mV%s (już zastosowano).",
    "How the governor picks the GPU clock under load:\n\n• Balanced: raises the clock only as much as needed — cooler and quieter (default).\n• Performance: holds the GPU at max clock under any gaming load (best FPS in GPU-bound games, more heat and power). It still returns to 350 MHz at idle.\n\nBoth modes use the governor's safe SMU path.": "Jak governor dobiera zegar GPU pod obciążeniem:\n\n• Zbalansowany: podnosi zegar tylko na tyle, na ile potrzeba — chłodniej i ciszej (domyślnie).\n• Performance: utrzymuje GPU na maksymalnym zegarze pod każdym obciążeniem w grach (najlepsze FPS w grach ograniczanych przez GPU, więcej ciepła i poboru mocy). W spoczynku i tak wraca do 350 MHz.\n\nOba tryby korzystają z bezpiecznej ścieżki SMU governora.",
    "Install": "Zainstaluj",
    "Installed": "Zainstalowane",
    "Installed kernels": "Zainstalowane kernele",
    "Installing": "Instalowanie",
    "Internet": "Internet",
    "It's the only installed kernel: it can't be removed.": "To jedyny zainstalowany kernel: nie można go usunąć.",
    "Kernel Manager": "Menedżer Kerneli",
    "Key": "Klucz",
    "Kids": "Dla dzieci",
    "Languages": "Języki",
    "Launcher": "Uruchamianie aplikacji",
    "License": "Licencja",
    "Load": "Obciążenie",
    "Loading screenshots…": "Wczytywanie zrzutów ekranu…",
    "Loading the catalogue (APT + Flatpak)…": "Wczytywanie katalogu (APT + Flatpak)…",
    "Loading the software catalogue…": "Wczytywanie katalogu oprogramowania…",
    "Log in with user “%s” password.": "Zaloguj się hasłem użytkownika „%s”.",
    "Logic": "Logiczne",
    "Lowers the CPU voltage relative to the factory curve.\n\n• 0 = no undervolt (default)\n• negative values (-1, -2 ...) = less voltage\n\nUndervolting lowers temperatures and power draw, but too much makes the system unstable. Use «Test» to verify.": "Obniża napięcie CPU względem fabrycznej krzywej.\n\n• 0 = brak undervoltu (domyślnie)\n• wartości ujemne (-1, -2 ...) = mniej napięcia\n\nUndervolt obniża temperatury i pobór mocy, ale zbyt duży czyni system niestabilnym. Użyj «Test», aby sprawdzić.",
    "Manual control (off = automatic curve)": "Kontrola ręczna (wyłączone = krzywa automatyczna)",
    "Manual control: you set the speed in %.\nAutomatic: the chip's curve manages the speed based on temperature.\n\nUse «Test» to hear the fan at the chosen speed for a few seconds.": "Kontrola ręczna: sam ustawiasz prędkość w %.\nAutomatyczna: krzywa układu zarządza prędkością na podstawie temperatury.\n\nUżyj «Test», aby usłyszeć wentylator przy wybranej prędkości przez kilka sekund.",
    "Maths": "Matematyka",
    "Max CPU frequency": "Maksymalna częstotliwość CPU",
    "Max GPU frequency": "Maksymalna częstotliwość GPU",
    "Max GPU voltage": "Maksymalne napięcie GPU",
    "Max frequency": "Maksymalna częstotliwość",
    "Max voltage": "Maksymalne napięcie",
    "Maximum GPU clock (SMU governor).\n\n• 1500 = power saving\n• 2000 = balanced (safe on every board)\n• 2200 = max stable at 1000 mV on stock cooling\n\nThe GPU reaches this frequency only under load, then returns to 350 MHz at idle. Above 2200 MHz at 1000 mV the BC-250 can hard-freeze: it needs more voltage and depends on the silicon lottery.": "Maksymalny zegar GPU (governor SMU).\n\n• 1500 = oszczędzanie energii\n• 2000 = zbalansowany (bezpieczny na każdej płycie)\n• 2200 = maksimum stabilne przy 1000 mV na chłodzeniu fabrycznym\n\nGPU osiąga tę częstotliwość tylko pod obciążeniem, a w spoczynku wraca do 350 MHz. Powyżej 2200 MHz przy 1000 mV BC-250 może się całkowicie zawiesić: potrzeba wyższego napięcia, a wynik zależy od loterii krzemowej.",
    "Messaging": "Komunikatory",
    "Monitoring": "Monitorowanie",
    "Most popular": "Najpopularniejsze",
    "Multimedia": "Multimedia",
    "Music": "Muzyka",
    "Name": "Nazwa",
    "New allocation": "Nowy przydział",
    "No results.": "Brak wyników.",
    "Open": "Otwórz",
    "Open a .sfmon recording to analyze": "Otwórz nagranie .sfmon do analizy",
    "Open in browser": "Otwórz w przeglądarce",
    "Open recording": "Otwórz nagranie",
    "Per core/thread frequency (MHz)": "Częstotliwość na rdzeń/wątek (MHz)",
    "Per extra-CU-pair stability:": "Stabilność wg pary dodatkowych CU:",
    "Performance": "Performance",
    "Permissions": "Uprawnienia",
    "Photography": "Fotografia",
    "Physics": "Fizyka",
    "Power": "Moc",
    "Power schedule": "Harmonogram zasilania",
    "Presentations": "Prezentacje",
    "Presets": "Presety",
    "Productivity": "Produktywność",
    "Publishing": "Publikowanie",
    "Rating": "Ocena",
    "Reboot now": "Uruchom ponownie",
    "Reboot now?": "Uruchomić ponownie teraz?",
    "Record telemetry to a .sfmon file (benchmarks/sessions)": "Nagraj telemetrię do pliku .sfmon (benchmarki/sesje)",
    "Recorders": "Nagrywanie",
    "Recording summary": "Podsumowanie nagrania",
    "Refresh lists and check for updates": "Odśwież listy i sprawdź aktualizacje",
    "Refresh:": "Odświeżanie:",
    "Refreshing the package lists…": "Odświeżanie list pakietów…",
    "Reloading…": "Ponowne wczytywanie…",
    "Remote access": "Zdalny dostęp",
    "Remote control panel · SkillFishOS": "Panel zdalnego sterowania · SkillFishOS",
    "Remove": "Usuń",
    "Removing": "Usuwanie",
    "Removing the repository…": "Usuwanie repozytorium…",
    "Repository updated. Reloading…": "Repozytorium zaktualizowane. Ponowne wczytywanie…",
    "Reviews": "Recenzje",
    "Role-playing": "Fabularne",
    "Save at boot": "Zapisz przy starcie",
    "Saved to (open to analyze):": "Zapisano w (otwórz, aby przeanalizować):",
    "Scanning": "Skanowanie",
    "Search": "Szukaj",
    "Search: ": "Szukaj: ",
    "Searching…": "Wyszukiwanie…",
    "Search…": "Szukaj…",
    "Security": "Bezpieczeństwo",
    "Set (reboot)": "Ustaw (restart)",
    "Set as default": "Ustaw jako domyślny",
    "Share the result (anonymous) in the silicon-lottery database on GitHub?": "Udostępnić wynik (anonimowo) w bazie loterii krzemowej na GitHubie?",
    "Share to the silicon DB": "Udostępnij w bazie krzemu",
    "Shooter": "Strzelanki",
    "Simulation": "Symulacje",
    "Size": "Rozmiar",
    "SkillFishOS — Analysis: ": "SkillFishOS — Analiza: ",
    "SkillFishOS — Kernel Manager": "SkillFishOS — Menedżer Kerneli",
    "SkillFishOS — Monitor · %s": "SkillFishOS — Monitor · %s",
    "SkillFishOS — Remote Manager": "SkillFishOS — Remote Manager",
    "SkillFishOS — Telemetry": "SkillFishOS — Telemetria",
    "Slim · BC-250 · ultra-lean kernel": "Slim - BC-250 - kernel minimalny",
    "Software sources": "Źródła oprogramowania",
    "Sort:": "Sortuj:",
    "Source": "Źródło",
    "Sources": "Źródła",
    "Speed": "Prędkość",
    "Sports": "Sportowe",
    "Spreadsheets": "Arkusze kalkulacyjne",
    "Strategy": "Strategiczne",
    "Suggest UV": "Zasugeruj UV",
    "Suite": "Seria",
    "System": "System",
    "System status": "Stan systemu",
    "Telemetry": "Telemetria",
    "Temperature": "Temperatura",
    "Temperature (°C)": "Temperatura (°C)",
    "Temperature limit": "Limit temperatury",
    "Terminal": "Terminal",
    "Test": "Test",
    "Test (benchmark)": "Test (benchmark)",
    "Test CU": "Test CU",
    "Tests the extra CUs (WGP3-4) one by one to catch defects (silicon lottery): enables each pair alone, stresses it with vkpeak and checks for GPU errors/hangs.\n\nTakes ~2-3 minutes and the GPU will be under load. Proceed?": "Testuje dodatkowe CU (WGP3-4) pojedynczo, aby wykryć defekty (loteria krzemowa): włącza każdą parę osobno, obciąża ją vkpeak i sprawdza błędy/zawieszenia GPU.\n\nZajmuje ~2-3 minuty, a GPU będzie pod obciążeniem. Kontynuować?",
    "Text editors": "Edytory tekstu",
    "The wizard steps the CPU up (3600 → 4000 MHz with progressive undervolt), validating each step with a benchmark and stopping at the first unstable one.\n\n⚠ The last step can freeze some boards: the watchdog then reboots automatically and the last stable value is restored at boot.\n\nNote: the test validates UNDER-LOAD stability; idle stability over days is confirmed by regular use.\n\nProceed?": "Kreator zwiększa zegar CPU krok po kroku (3600 → 4000 MHz z progresywnym undervoltem), sprawdzając każdy krok benchmarkiem i zatrzymując się na pierwszym niestabilnym.\n\n⚠ Ostatni krok może zawiesić niektóre płyty: watchdog wtedy automatycznie uruchamia system ponownie, a przy starcie przywracana jest ostatnia stabilna wartość.\n\nUwaga: test sprawdza stabilność POD OBCIĄŻENIEM; stabilność w spoczynku przez kilka dni potwierdza dopiero codzienne użytkowanie.\n\nKontynuować?",
    "The wizard steps the GPU up (2000 → 2200 MHz at 1000 mV), validating each step with a benchmark and rolling back if unstable.\n\n~2 minutes per step under full GPU load: set the fan high first.\nWhen done it applies the highest stable point for YOUR board.\n\nProceed?": "Kreator zwiększa zegar GPU krok po kroku (2000 → 2200 MHz przy 1000 mV), sprawdzając każdy krok benchmarkiem i cofając się w razie niestabilności.\n\n~2 minuty na krok przy pełnym obciążeniu GPU: najpierw ustaw wysokie obroty wentylatora.\nPo zakończeniu zastosuje najwyższy stabilny punkt dla TWOJEJ płyty.\n\nKontynuować?",
    "Thermal threshold above which the SMU throttles frequency.\n\nRecommended 85 °C. Above it, the system automatically lowers the clock to protect the hardware.": "Próg termiczny, powyżej którego SMU ogranicza częstotliwość.\n\nZalecane 85 °C. Powyżej tej wartości system automatycznie obniża zegar, aby chronić sprzęt.",
    "Time:": "Czas:",
    "Tip: run the system for a few days; if a freeze appears, step down one notch.\n\nShare the result (anonymous) in the silicon-lottery database?": "Wskazówka: używaj systemu przez kilka dni; jeśli pojawi się zawieszenie, zejdź o jeden poziom niżej.\n\nUdostępnić wynik (anonimowo) w bazie loterii krzemowej?",
    "Translation": "Tłumaczenie",
    "Turn off": "Wyłącz",
    "Turn on": "Włącz",
    "Undervolt": "Undervolt",
    "Undervolt (scale)": "Undervolt (skala)",
    "Uninstall": "Odinstaluj",
    "Uninstalling…": "Odinstalowywanie…",
    "Unsupported backend: ": "Nieobsługiwany backend: ",
    "Update all": "Aktualizuj wszystko",
    "Updates": "Aktualizacje",
    "Updating the whole system…": "Aktualizowanie całego systemu…",
    "Utilities": "Narzędzia",
    "VRAM (graphics memory)": "VRAM (pamięć graficzna)",
    "Vector": "Wektorowa",
    "Version": "Wersja",
    "Version control": "Kontrola wersji",
    "Viewers": "Przeglądarki",
    "Voltage": "Napięcie",
    "Voltage tied to the max GPU frequency (mV).\n\nHigher = more stable at high frequency but hotter. Range 700-1129 mV.": "Napięcie powiązane z maksymalną częstotliwością GPU (mV).\n\nWyższe = większa stabilność przy wysokiej częstotliwości, ale wyższa temperatura. Zakres 700-1129 mV.",
    "Website": "Strona internetowa",
    "What's new": "Co nowego",
    "Wizard result": "Wynik kreatora",
    "Word processors": "Procesory tekstu",
    "Writes to the BIOS CMOS. A reboot is needed to apply.": "Zapisuje w CMOS-ie BIOS-u. Aby zastosować, wymagany jest restart.",
    "You can't uninstall the running kernel. Boot another kernel and try again.": "Nie można odinstalować uruchomionego kernela. Uruchom inny kernel i spróbuj ponownie.",
    "avg": "śr.",
    "daemon not running": "demon nie działa",
    "default": "domyślny",
    "devices: ": "urządzenia: ",
    "external kernel (non-SkillFishOS)": "kernel zewnętrzny (spoza SkillFishOS)",
    "filesystem: ": "system plików: ",
    "key .asc URL (optional)": "URL klucza .asc (opcjonalnie)",
    "locked (always on)": "zablokowana (zawsze aktywna)",
    "max": "maks.",
    "min": "min",
    "network/ipc: ": "sieć/ipc: ",
    "off": "wyłączona",
    "on": "aktywna",
    "online": "aktywne",
    "operation cancelled": "operacja anulowana",
    "operation failed": "operacja nie powiodła się",
    "running": "uruchomiony",
    "service unavailable": "usługa niedostępna",
    "sockets: ": "gniazda: ",
    "test failed": "test nieudany",
    "vmlinuz, initrd and the modules will be removed (not dpkg-managed).": "Zostaną usunięte vmlinuz, initrd i moduły (niezarządzane przez dpkg).",
    "■ STOP": "■ STOP",
    "◉  LIVE MONITOR": "◉  MONITOR NA ŻYWO",
    "◉  TELEMETRY LIVE": "◉  TELEMETRIA NA ŻYWO",
    "○ Off": "○ Wyłączona",
    "● On": "● Włączona",
    "● REC": "● REC",
    "⚠ GPU problems under load detected: possible defective CU (silicon lottery). Consider keeping fewer CUs.": "⚠ Wykryto problemy GPU pod obciążeniem: możliwa wadliwa CU (loteria krzemowa). Rozważ pozostawienie mniejszej liczby CU.",
    "⚠ Last freeze: %s — if it happens again, step down one notch with the 🎰 wizards.": "⚠ Ostatnie zawieszenie: %s — jeśli powtórzy się, zejdź o jeden poziom niżej za pomocą kreatorów 🎰.",
    "✓ Done.": "✓ Gotowe.",
    "✓ No defects: all CUs sustain the load with no GPU errors.": "✓ Brak defektów: wszystkie CU wytrzymują obciążenie bez błędów GPU.",
    "✓ Update complete.": "✓ Aktualizacja zakończona.",
    "✗ Not even 2000 MHz is stable on this board: keeping the current profile.": "✗ Nawet 2000 MHz nie jest stabilne na tej płycie: zachowuję bieżący profil.",
    "✗ Not even 3600 MHz is stable: keeping the current profile.": "✗ Nawet 3600 MHz nie jest stabilne: zachowuję bieżący profil.",
    "🎰 Find my max": "🎰 Znajdź maksimum",
    "🎰 My silicon": "🎰 Mój krzem",
    "📂 Open": "📂 Otwórz",
    "📊 ANALYSIS  ·  ": "📊 ANALIZA  ·  ",
}


# Ucraino: da riempire. Vedi website/src/i18n.uk.ts per la terminologia gia'
# usata sul sito, cosi' non traduciamo lo stesso termine in due modi diversi.
UK = {}

TABLES = {"pl": PL, "uk": UK}


def make_L(local=None):
    """Costruisce la funzione L(it, en) per una app.

    `local` e' un dizionario opzionale {lingua: {inglese: traduzione}} che ha la
    precedenza sulla tabella condivisa, per i casi in cui la stessa stringa
    inglese va resa diversamente a seconda del contesto."""
    local = local or {}

    def L(it, en):
        if LANG == "it":
            return it
        table = TABLES.get(LANG)
        if table is None:
            return en
        over = local.get(LANG)
        if over and en in over:
            return over[en]
        return table.get(en, en)

    return L


L = make_L()


def coverage():
    """Quante stringhe sono tradotte per lingua. Utile in fase di rilascio."""
    return {lang: len(t) for lang, t in TABLES.items()}

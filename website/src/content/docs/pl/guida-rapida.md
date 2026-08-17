---
title: Szybki start
description: Pierwsze 10 minut ze SkillFishOS — od pierwszego uruchomienia do pierwszej gry.
group: Wprowadzenie
order: 3
---

Zainstalowałeś SkillFishOS (zobacz [Instalacja](/pl/docs/installazione)) i jesteś przy pierwszym uruchomieniu. Ta strona to **krótka lista kontrolna**, żeby ruszyć od razu: cała reszta jest już skonfigurowana i działa.

## W jednym zdaniu

> Włączasz → jesteś już na dostrojonym pulpicie → podłączasz pada → dodajesz swoje gry → grasz. Bez terminala, bez konfiguracji.

## 1. Pierwsze uruchomienie (wszystko gotowe)

Przy pierwszym uruchomieniu dostajesz pulpit **KDE Plasma 6** z motywem steampunk, zoptymalizowane jądro, zarządcę SMU, profil **Stock**, zestaw do grania i migawki **już włączone**. W prawym górnym rogu **HUD** pokazuje na żywo procesor, grafikę, temperatury, pamięć, wentylator i podłączone urządzenia Bluetooth.

Nie musisz instalować sterowników, ustawiać częstotliwości ani niczego włączać: system startuje „na maksymalnej zgodności”.

## 2. Podłącz się do sieci

Ethernetem zarządza NetworkManager i działa od razu. Do Wi-Fi i Bluetootha użyj ikony sieci na panelu. Połączenie jest potrzebne do Steama, aktualizacji i lokalnej AI.

## 3. Podłącz pada

| Kontroler | Jak |
|---|---|
| **DualShock 4** | Bluetooth: przytrzymaj **Share + PS**, aż zacznie migać, potem sparuj z ikony Bluetooth. Ma **żyroskop**. |
| **Zwykły pad** | Przez **USB** kablem **do danych** (nie tylko do ładowania): widziany jako pad Xbox 360. |

Szczegóły i rozwiązywanie problemów → [Granie](/pl/docs/gaming) i [Rozwiązywanie problemów](/pl/docs/risoluzione-problemi).

## 4. Dodaj swoje gry

- **Steam** jest już zainstalowany i zintegrowany z gamescope/MangoHud. Zaloguj się i zainstaluj swoje gry: tytuły z Windowsa działają przez **Protona**.
- **Epic / GOG** → [Heroic](/pl/docs/gaming).
- **Emulacja** → uruchom **EmuDeck**, wybierz emulatory, a potem graj z nakładki **ES-DE**. ROM-y, BIOS-y i klucze dokładasz sam (zobacz uwagę prawną w [Granie](/pl/docs/gaming)).

## 5. (Opcjonalnie) Przyciśnij sprzęt

SkillFishOS startuje w profilu **Stock**, żeby było bezpiecznie na każdej płycie. Gdy zechcesz więcej wydajności, otwórz **[Tuner](/pl/docs/app-native)** i przejdź poziom wyżej:

**Stock → Performance → Turbo → Crazy**

Tuner **sprawdza każdy profil na twojej własnej BC-250** i automatycznie **cofa zmiany**, jeśli płyta sobie nie radzi. To bezpieczny sposób na znalezienie granicy własnego układu (zobacz [GPU i podkręcanie](/pl/docs/gpu-overclock)).

## 6. (Opcjonalnie) Włącz lokalną AI

Gdy potrzebujesz asystenta AI bez internetu, otwórz **panel AI** i uruchom [Unsloth Studio](/pl/docs/ai-locale). Pamiętaj: AI i wymagających gier **nie** używa się jednocześnie (ta sama grafika i ta sama pamięć). Po wyłączeniu silnika grafika wraca w całości do grania.

## Co warto wiedzieć od razu

- **Nie włączaj z powrotem wstrzymywania**: na BC-250 jest zepsute i płyta się nie obudzi (zobacz [Pulpit](/pl/docs/desktop)).
- Używaj monitora **DisplayPort** albo przejściówki **pasywnej**; **aktywne** przejściówki DP→HDMI psują dźwięk.
- Masz **siatkę bezpieczeństwa**: migawka Btrfs powstaje przed każdą aktualizacją i po niej; jeśli coś pójdzie źle, cofasz się z menu GRUB → *SkillFishOS snapshots* (zobacz [Dyski i migawki](/pl/docs/storage-snapshot)).

## Co dalej?

- Chcesz zrozumieć, **czego** właściwie używasz? → [Sprzęt BC-250](/pl/docs/hardware-bc250)
- Chcesz prawdziwe **liczby** wydajności? → [Wydajność i testy](/pl/docs/prestazioni)
- Masz krótkie **pytanie**? → [FAQ](/pl/docs/faq)
- Nie znasz jakiegoś **terminu**? → [Słowniczek](/pl/docs/glossario)

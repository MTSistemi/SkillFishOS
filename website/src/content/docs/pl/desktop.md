---
title: Pulpit, motyw i dostęp zdalny
description: KDE Plasma 6, motyw steampunk, systemowy HUD, blokada wstrzymywania i dostęp zdalny.
group: System
order: 4
---

SkillFishOS używa **[KDE Plasma 6](https://kde.org/plasma-desktop/)** jako środowiska pulpitu, ubranego w spójny motyw steampunk i zestaw poprawek pisanych pod BC-250.

## Sesje

Przy logowaniu (obsługiwanym przez **SDDM**, z automatycznym logowaniem) dostępnych jest kilka sesji:

- **KDE Plasma X11** — *domyślna*. Wybór X11 sprawia, że dostęp zdalny jest banalny (patrz niżej);
- **KDE Plasma Wayland** — do wyboru;
- **Gaming** — sesja [gamescope](https://github.com/ValveSoftware/gamescope) w stylu Big Picture (zobacz [Granie](/pl/docs/gaming)).

## **Uwaga:** blokada wstrzymywania (krytyczna)

BC-250 ma **zepsute wstrzymywanie ACPI**: jeśli zaśnie, **nie obudzi się** i będzie wymagać resetu (zobacz [sprzęt](/pl/docs/hardware-bc250)). Dlatego SkillFishOS **trwale wyłącza** wszystkie stany uśpienia:

```bash
systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

Do tego dokłada regułę `logind` (`IdleAction=ignore`), wyłączone samoczynne blokowanie ekranu i zarządzanie energią z „nieskończonym” czasem bezczynności. To środek **obowiązkowy**: wstrzymana maszyna jest też nieosiągalna zdalnie.

## Motyw „SkillFish Steampunk”

Wygląd to zestrojona paleta mosiądzu i miedzi (kolor wiodący **`#d8a849`**, ciemne powierzchnie), spójna **od uruchomienia po pulpit**: motyw GRUB-a, ekran powitalny Plymouth, ekran logowania SDDM, tapeta z rybim motywem. Pakiet motywu zawiera:

- **ikony** (`SkillFishSteampunk`, z `breeze-dark` jako zapasowym zestawem) i własne **kursory**;
- styl **Kvantum** dla aplikacji Qt oraz **zestaw kolorów** KDE;
- **motyw plazmy**, motyw **Konsole**, przyciski okien i globalny **wygląd** (`org.skillfish.steampunk`);
- awatary użytkownika w tym samym stylu i galerię do wyboru.

> Domyślne motywy **Breeze** zostają zainstalowane jako nośna podstawa (w szczególności dostarczają okno wylogowania i wyłączania). Nie wolno ich usuwać.

## Systemowy HUD (Conky)

W prawym górnym rogu jest **HUD** w mosiężnym stylu, zbudowany na **[Conky](https://github.com/brndnmtthws/conky)**, pokazujący w czasie rzeczywistym: słupki obciążenia rdzeni z MHz/°C/W, MHz, temperaturę i VRAM grafiki, pamięć, dysk, wentylator oraz **podłączone urządzenia Bluetooth** z poziomem baterii (pady, słuchawki…). Wartości pochodzą z osobnych pomocników, które czytają czujniki wprost ze sprzętu.

## Dostęp zdalny (x11vnc)

Ponieważ domyślna sesja to X11, dostęp zdalny jest prosty: SkillFishOS uruchamia **[x11vnc](https://github.com/LibVNC/x11vnc)** na aktywnym ekranie, udostępniając prawdziwy obraz. W sieci lokalnej połączy się dowolny klient VNC. Pozwala to na pomoc i konfigurację z innego peceta, bez klawiatury i myszy przy samej płycie.

## Sieć, dźwięk i aplikacje

- **Sieć**: ethernetem zarządza **NetworkManager**, więc widać go i konfiguruje z okien Plazmy.
- **Dźwięk**: pełny stos **[PipeWire](https://pipewire.org/)** (z obsługą Bluetootha). Uwaga: *aktywne* przejściówki DP→HDMI potrafią popsuć dźwięk — zobacz [Rozwiązywanie problemów](/pl/docs/risoluzione-problemi).
- **Aplikacje podstawowe**: menedżer plików Dolphin, terminal Konsole, czytnik PDF Okular, przeglądarka obrazów Gwenview, archiwizator Ark, zrzuty ekranu Spectacle, sklep Discover (z flatpakiem), przeglądarka **Google Chrome**, **OnlyOffice**.
- **Własne aplikacje SkillFishOS** (zebrane w menu **„SkillFishOS”**, każda instalowana i aktualizowana jako `.deb` z podpisanego repozytorium): **Tuner** (podkręcanie, napięcia, wentylator i CU dla BC-250), **AI** (lokalny model na zintegrowanej grafice, na żądanie), **Monitor** (wykresy temperatury, częstotliwości, napięcia i wentylatora na żywo), **Kernel Manager** (wybór jądra do uruchomienia i usuwanie starych), **ISO Mount**, **Hub** — centrum oprogramowania w stylu Discovera (APT + Flatpak + Snap) ze stronami aplikacji, karuzelą zrzutów ekranu i zarządzaniem źródłami — a także **Base** (sprzętowy watchdog i wykrywacz zawieszeń z powiadomieniem na pulpicie) oraz **Console**, czyli sesja **„SkillFishOS Console (Big Picture)”** w stylu SteamOS, do wybrania z ekranu logowania.
- **Obraz**: demon (`skillfish-dp-hotswap`) zajmuje się wykrywaniem monitora, co jest konieczne, bo HPD w DisplayPort jest zepsute.

## Źródła

- [KDE Plasma](https://kde.org/plasma-desktop/) · [Kvantum](https://github.com/tsujan/Kvantum)
- [Conky](https://github.com/brndnmtthws/conky) · [x11vnc](https://github.com/LibVNC/x11vnc)
- [PipeWire](https://pipewire.org/) · [SDDM](https://github.com/sddm/sddm)
- [Plymouth](https://www.freedesktop.org/wiki/Software/Plymouth/) · [NetworkManager](https://networkmanager.dev/)

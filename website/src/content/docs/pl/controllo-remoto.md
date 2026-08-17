---
title: Sterowanie zdalne — Remote Manager
description: Panel webowy SkillFishOS do sterowania BC-250 z przeglądarki albo telefonu — telemetria, KVM, terminal, Tuner, sklep z aplikacjami i AI.
group: Używanie
order: 4
---

**SkillFishOS Remote Manager** to modułowy panel webowy, który pozwala sterować BC-250 **z innego peceta albo z telefonu**, w tej samej sieci lokalnej lub — przez ZeroTier — z dowolnego miejsca na świecie. Logujesz się danymi swojego konta systemowego, wszystko po HTTPS.

## Instalacja

```bash
sudo apt update
sudo apt install skillfish-dashboard
```

Pakiet instaluje usługę, własną aplikację **Remote Manager** (do włączania i wyłączania panelu oraz wybierania modułów) i wszystkie strony webowe. Zależności opcjonalne (KVM, terminal, Wake-on-LAN) są w *Recommends* i dociągają się same, gdy są dostępne.

## Włączanie

Otwórz **SkillFishOS Remote Manager** z menu aplikacji:

- **Główny przełącznik** — uruchamia usługę (na stałe, przez systemd).
- **Pola wyboru modułów** — wybierz, co udostępnić (telemetria, Tuner, Hub, KVM, terminal, AI…).
- Pokazuje **adres URL, kod QR i dane logowania** do połączenia.

Albo z terminala: `sudo systemctl enable --now skillfish-dashboard`.

> Dla bezpieczeństwa panel **nie uruchamia się sam** po instalacji — włączasz go, kiedy chcesz.

## Dostęp

Otwórz w przeglądarce **`https://<ip-płyty>:8443`** (albo `https://BC-250.local:8443`). Certyfikat jest podpisany samodzielnie, więc przeglądarka za pierwszym razem ostrzeże — tak ma być, przejdź dalej.

Zaloguj się **nazwą użytkownika i hasłem z systemu** (tymi samymi co przy logowaniu do SkillFishOS): uwierzytelnianie idzie przez PAM.

## Moduły

Panel składa się z modułów, które włączysz:

- **Telemetria** — wykresy temperatur, częstotliwości, watów i obciążenia procesora oraz grafiki na żywo, z wartościami na osi pionowej i panelem słupków pokazującym **częstotliwość na rdzeń i wątek** (wszystkie 16 wątków, wyłączone wyraźnie oznaczone).
- **Stan systemu** — host, adres IP, jądro, czas pracy, pamięć, dysk, aktywne CU, wykryte zawieszenia.
- **Sterowanie (Tuner)** — szybkie profile oraz **pełny Tuner** w wersji webowej: procesor (częstotliwość/napięcie/temperatura), grafika (częstotliwość/napięcie/zarządca), **sterowanie jednostkami obliczeniowymi na żywo** (siatka WGP, bez restartu), wentylator, VRAM, *Test* i kreatory **„Znajdź mój maksimum”**.
- **Aplikacje i pakiety (Hub)** — prawdziwy **sklep z aplikacjami** (AppStream + Flatpak + Snap): przeglądanie po kategoriach, szukanie, instalowanie i usuwanie, aktualizacje. **Aplikacje SkillFishOS** są wyróżnione na górze.
- **Pulpit (KVM)** — patrz na prawdziwy pulpit płyty i steruj nim z przeglądarki (noVNC), bez dodatkowego sprzętu.
- **Terminal** — powłoka webowa (ttyd) wewnątrz panelu.
- **Lokalna AI** — stan silnika Unsloth, przyspieszenie Vulkanem i rozmowa z lokalnym modelem działającym na grafice BC-250.
- **AI-Ops** — lokalny model czyta dzienniki i telemetrię i diagnozuje za ciebie problemy.
- **Dzienniki**, **automatyczne reguły** (samoczynne dławienie powyżej progu °C), **Wake-on-LAN** oraz włączanie i wyłączanie według harmonogramu.
- **ZeroTier** — żeby dosięgnąć panelu **z dowolnego miejsca** (patrz niżej).

Przyciski **Uruchom ponownie** i **Wyłącz** są zawsze dostępne na górnym pasku. Kafelki można **zamykać, otwierać z powrotem i przeciągać**, a **układ zapisać**.

## Dostęp zdalny (ZeroTier)

Panel jest pomyślany dla **sieci lokalnej**. Żeby używać go z zewnątrz, włącz moduł **ZeroTier**: dołącz do jednej ze swoich sieci, zatwierdź płytę na [my.zerotier.com](https://my.zerotier.com), a potem wejdź na panel pod adresem ZeroTier płyty — bez otwierania portów na routerze.

## Bezpieczeństwo

- **HTTPS** z certyfikatem podpisanym samodzielnie (TLS 1.2+), tworzonym przy pierwszym uruchomieniu.
- **Logowanie przez PAM** danymi twojego użytkownika, **podpisane sesje** (HMAC) i **ograniczanie liczby prób**.
- Zaprojektowane pod **sieć lokalną**; do dostępu z zewnątrz używaj ZeroTiera, zamiast wystawiać panel wprost do internetu.

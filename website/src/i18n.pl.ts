// Polish UI strings. Any key missing here falls back to English (see t() in i18n.ts),
// so this file can grow without ever leaving a blank on the page.
// Inline HTML and &nbsp; entities are part of the copy — keep them.
export const pl: Record<string, string> = {
  title: "SkillFishOS — Linux do grania na AMD BC-250",
  "meta.desc":
    "SkillFishOS: steampunkowy system operacyjny do grania na płytce AMD BC-250. Gotowy i zoptymalizowany, bez grzebania. Emulacja, Steam, lokalna AI. Oparty na Debianie + KDE Plasma.",

  "nav.feat": "Funkcje",
  "nav.shots": "Zrzuty ekranu",
  "nav.hw": "Sprzęt",
  "nav.download": "Pobierz",
  "nav.docs": "Dokumentacja",
  "nav.gallery": "Galeria",
  "nav.contact": "Kontakt",
  "nav.donate": "Wesprzyj nas",

  "hero.soon": "Wydanie 26.06 „Aetherium”",
  "hero.tag": "System operacyjny do grania stworzony dla <b>AMD BC-250</b>.",
  "hero.sub":
    "Steampunkowy Linux, gotowy do gry od pierwszego uruchomienia. Wszystko wstępnie dostrojone, bez grzebania. Emulacja, Steam i lokalna AI. Oparty na Debianie i KDE&nbsp;Plasma.",
  "hero.btn1": "Zobacz w akcji",
  "hero.btn2": "Co w środku",
  "hero.pill": "APU AMD · Zen&nbsp;2 + RDNA&nbsp;2 · 16&nbsp;GB GDDR6",

  "intro.eye": "Czym jest",
  "intro.h2": "Konsola-PC,<br>gotowa do użycia.",
  "intro.p1":
    "SkillFishOS zamienia płytkę <strong>AMD BC-250</strong> — półniestandardowe APU z rodziny <strong>AMD Zen&nbsp;2 + RDNA&nbsp;2</strong> (procesor „Oberon”, grafika „Cyan&nbsp;Skillfish”, 16&nbsp;GB GDDR6) — w kompletny system do grania i pracy.",
  "intro.p2":
    "Governor, łatki jądra, podkręcanie i profile termiczne są <strong>gotowe i dostrojone</strong>: system działa na maksimum <strong>bez grzebania</strong>. Spójna <strong>steampunkowa</strong> oprawa od startu po pulpit, pomyślana też po to, by <strong>dzieci uczyły się Linuksa</strong> podczas zabawy.",

  "feat.eye": "Funkcje",
  "feat.h2": "Wszystko gotowe, prosto z pudełka.",
  "feat.sub":
    "Nic nie trzeba konfigurować ręcznie: system jest już dostrojony pod BC-250.",
  "f1.t": "Gotowy do grania",
  "f1.d":
    "Steam, EmuDeck, ES-DE, Heroic i Proton gotowe do użycia. EmuDeck instaluje i konfiguruje emulatory w kilku kliknięciach — gry i ROM-y dokładasz sam.",
  "f2.t": "Jądro szyte na miarę",
  "f2.d":
    "Jądro tkg dostrojone pod BC-250: <b>40 jednostek obliczeniowych</b> odblokowanych, podkręcanie CPU/GPU i dedykowany governor SMU, by wycisnąć każdy TFLOP.",
  "f3.t": "Gotowy, bez grzebania",
  "f3.d":
    "Governor, łatki, podkręcanie i zabezpieczenie termiczne <b>już skonfigurowane i przetestowane</b>. Włączasz i działa na pełnych obrotach: bez terminala, bez ręcznego strojenia.",
  "f4.t": "Motyw steampunk",
  "f4.d":
    "Ciemny pulpit KDE&nbsp;Plasma w stylu steampunk: ikony, kursory, tapety i systemowy HUD w mechaniczno-wiktoriańskiej stylistyce.",
  "f5.t": "Migawki Btrfs",
  "f5.d":
    "Eksperymentuj bez obaw: każda zmiana jest chroniona automatycznymi migawkami. Coś się zepsuło? <b>Przywracanie jednym kliknięciem</b> z menu startowego.",
  "f6.t": "AI lokalnie",
  "f6.d":
    "Silnik AI z akceleracją <b>Vulkan</b> na zintegrowanym GPU. Modele do czatu i kodowania działają u ciebie w domu, bez chmury.",
  "f7.t": "Zdalne sterowanie",
  "f7.d":
    "<b>Remote Manager</b>: panel webowy do sterowania płytką z przeglądarki lub telefonu — telemetria, KVM, terminal, Tuner, sklep z aplikacjami i AI. Logowanie systemowe po HTTPS, a z dowolnego miejsca przez ZeroTier.",

  "show.eye": "Zrzuty ekranu",
  "show.h2": "Ładny w odbiorze, wygodny w użyciu.",
  "s1.t": "Steampunkowy pulpit",
  "s1.d":
    "KDE Plasma w stylu steampunk: tematyczna tapeta, złote akcenty i żywy HUD z CPU, GPU, temperaturami, wentylatorem i baterią padów Bluetooth — zawsze na oku.",
  "s2.t": "Łatwa emulacja z EmuDeck",
  "s2.d":
    "EmuDeck instaluje i konfiguruje emulatory (RetroArch, Dolphin, PCSX2, PPSSPP, RPCS3 i inne) oraz frontend ES-DE w kilku kliknięciach. System daje narzędzia: gry i ROM-y dokładasz sam.",
  "s4.t": "AI w domu, jednym kliknięciem",
  "s4.d":
    "Dedykowany panel włącza i wyłącza lokalny silnik AI na GPU (Vulkan). Czat webowy, terminal do kodowania i zarządzanie: sztuczna inteligencja działa u ciebie, a gdy chcesz grać — zwalnia GPU.",
  "s5.t": "Strojenie na kliknięcie",
  "s5.d":
    "Tuner reguluje zegary, undervolt, wentylator i jednostki obliczeniowe za pomocą gotowych ustawień (Stock, Performance, Turbo, Crazy) oraz zabezpieczenia termicznego chroniącego sprzęt. Cała moc, bezpiecznie, bez wiersza poleceń.",

  "hw.eye": "Sprzęt",
  "hw.h2": "Stworzony dla AMD BC-250.",
  "hw.sub": "Cała moc rodziny AMD Zen 2 + RDNA 2, uwolniona na Linuksie.",
  "hw.c1": 'Procesor "Oberon" · do 4,0 GHz',
  "hw.c2": 'GPU "Cyan Skillfish" · 40 CU',
  "hw.c3": "FP32 · akceleracja Vulkan",
  "hw.c4": "współdzielona GDDR6",

  "cta.h2": 'Włącz. <span class="gold-text">Graj.</span> Ucz się.',
  "cta.p":
    "Otwartoźródłowy system operacyjny, który zamienia surową płytkę w prawdziwą konsolę-PC. Dostępny w dwóch edycjach: AMD BC-250 i Generic (dowolny PC/VM x86-64).",
  "cta.btn": "Pobierz SkillFishOS",

  "foot.based":
    "Otwarte źródła · Oparty na Debianie · KDE Plasma · © 2026 SkillFishOS",

  "dl.title": "Pobierz — SkillFishOS",
  "dl.eye": "Pobierz",
  "dl.h2": 'Pobierz SkillFish<span class="gold-text">OS</span>',
  "dl.sub":
    "Instalowalne obrazy ISO, gotowe do użycia — dla AMD BC-250 i dowolnego PC x86-64.",
  "dl.badge": "26.06.3 „Aetherium”",
  "dl.notice":
    "Wydanie <strong>26.06.3 „Aetherium”</strong> systemu SkillFishOS jest dostępne w <strong>dwóch edycjach</strong>: <strong>BC-250</strong> (płytka AMD) i <strong>Generic</strong> (dowolny PC lub VM x86-64). Kompletne i gotowe do użycia. Projekt <strong>open-source</strong>.",
  "dl.btnsoon": "ISO wkrótce",
  "dl.btn": "Pobierz ISO",
  "dl.ed.bc250": "BC-250",
  "dl.ed.generic": "Generic (PC/VM)",
  "dl.ed.slim": "Slim (BC-250)",
  "dl.ed.all": "Wszystkie pliki na SourceForge →",
  "dl.size":
    "amd64 · ~{size} GB · btrfs + KDE Plasma · 2 edycje na SourceForge",
  "dl.ver":
    "Wersja <strong>26.06.3 „Aetherium”</strong> · <strong>2 edycje</strong> (BC-250 · Generic) · startuje po angielsku, język wybierasz przy instalacji",
  "dl.bugs.h": "Napotkałeś problem?",
  "dl.bugs.d":
    "SkillFishOS jest stale ulepszany. Aby zgłosić błąd lub problem, otwórz <em>issue</em> na GitHubie. (Wkrótce dodamy też adres e-mail.)",
  "dl.bugs.btn": "Zgłoś na GitHubie",

  "dl.req.h": "Wymagania",
  "dl.req.d":
    "Płytka <strong>AMD BC-250</strong> (APU Zen&nbsp;2 + RDNA&nbsp;2, 16&nbsp;GB GDDR6), dysk SSD/NVMe, monitor <strong>DisplayPort</strong> i pendrive min. 8&nbsp;GB na instalator.",
  "dl.inc.h": "Co zawiera",
  "dl.inc.d":
    "Zoptymalizowane jądro (40&nbsp;CU, governor, OC), pełny motyw steampunk, Steam + EmuDeck + ES-DE, lokalny stos AI, migawki Btrfs oraz gotowe narzędzia Tuner i AI.",
  "dl.steps.h": "Instalacja",
  "dl.step1": "Zapisz ISO na pendrive (Etcher, Ventoy lub <code>dd</code>).",
  "dl.step2":
    "Uruchom BC-250 z USB i przejdź przez graficzny instalator (Calamares).",
  "dl.step3":
    "Przy pierwszym starcie wszystko jest już skonfigurowane: włączasz i grasz.",

  "dl.repo.h": "Aktualizacje",
  "dl.repo.d":
    "SkillFishOS aktualizuje się z <strong>oficjalnego repozytorium</strong>: jądro, aplikacje i motywy pochodzą od nas i są przetestowane, więc aktualizacje Debiana sid nie zepsują systemu.",

  "gal.title": "Galeria — SkillFishOS",
  "gal.eye": "Galeria",
  "gal.h2": "Ładny w odbiorze, wygodny w użyciu.",
  "gal.sub":
    "Spojrzenie na SkillFishOS w akcji: pulpit, granie, emulacja i narzędzia.",
  "gal.desktop.t": "Steampunkowy pulpit",
  "gal.desktop.d":
    "Otematyzowane KDE Plasma z żywym systemowym HUD-em w prawym górnym rogu.",
  "gal.about.t": "Informacje o systemie",
  "gal.about.d":
    "Pełny branding: nazwa, logo i sprzęt rozpoznawane jako SkillFishOS.",
  "gal.emudeck.t": "EmuDeck",
  "gal.emudeck.d": "Instalacja i konfiguracja emulatorów w kilku kliknięciach.",
  "gal.esde1.t": "ES-DE — frontend",
  "gal.esde1.d":
    "Frontend ES-DE do przeglądania i uruchamiania twoich bibliotek.",
  "gal.ai.t": "Panel AI",
  "gal.ai.d": "Włącz i wyłącz lokalny stos AI (Vulkan) jednym kliknięciem.",
  "gal.tuner.t": "Tuner — jednostki obliczeniowe na żywo",
  "gal.tuner.d":
    "Siatka CU (zielone = aktywne, czerwone = wyłączone), ustawienia 24/32/40 i test, bez restartu.",
  "gal.tunerctl.t": "Tuner — ustawienia, governor i kreatory",
  "gal.tunerctl.d":
    "Ustawienia Stock/Performance/Turbo/Crazy, panel „Mój krzem”, tryb governora Zrównoważony/Wydajność i kreatory „Znajdź maksimum” dla CPU i GPU.",
  "gal.monitor.t": "Telemetria na żywo podczas testów",
  "gal.monitor.d":
    "Wykresy temperatury, częstotliwości, napięcia i wentylatora w czasie rzeczywistym.",
  "gal.cutest.t": "Test CU — loteria krzemowa",
  "gal.cutest.d":
    "Sprawdza, czy wszystkie 40 CU wytrzymują obciążenie bez błędów (przydatne przy układach z odzysku).",
  "gal.wukong.t": "Black Myth: Wukong — 112 FPS",
  "gal.wukong.d": "Średnia w 1080p na BC-250 (maks. 128, 1% low 101).",
  "gal.super.t": "Unigine Superposition — 12 938",
  "gal.super.d":
    "1080p High: wydajność klasy Radeon RX 6600 na płytce za ~50 €.",
  "gal.heaven.t": "Unigine Heaven — 113,7 FPS",
  "gal.heaven.d": "Wynik 2865 w 1080p Ultra, 8× AA, teselacja Extreme.",
  "gal.boot.t": "Steampunkowy start",
  "gal.boot.d": "Spójny mosiężny splash od GRUB-a po pulpit.",
  "gal.b1.t": "Ten sam sprzęt, +34% — vs Bazzite",
  "gal.b1.d":
    "Superposition 1080p Extreme: ta sama BC-250 osiąga 4102 na fabrycznych zegarach w innej dystrybucji; SkillFishOS dochodzi do 5513. Oficjalny ranking Unigine.",
  "gal.b2.t": "Na równi z Radeonem RX 6600",
  "gal.b2.d":
    "Superposition 1080p High: BC-250 ze SkillFishOS (12 938) dorównuje RX 6600/6600 XT (12 454) za 200 €+. Oficjalny ranking Unigine.",

  "hwp.title": "Sprzęt AMD BC-250 — SkillFishOS",
  "hwp.eye": "Sprzęt",
  "hwp.h2": 'Stworzony dla <span class="gold-text">AMD BC-250</span>.',
  "hwp.sub":
    "Półniestandardowe APU AMD Zen 2 + RDNA 2 z 16 GB GDDR6, uwolnione na Linuksie.",
  "hwp.specs.h": "Specyfikacja",
  "hwp.cpu.t": "CPU — 8× Zen 2",
  "hwp.cpu.d":
    '"Oberon", <strong>8 rdzeni / 16 wątków</strong> (płyta udostępnia 6, SkillFishOS odblokowuje pozostałe dwa przez SMU: zmierzone <strong>+20%</strong>), do <strong>4,0 GHz na wszystkich rdzeniach</strong> po podkręceniu.',
  "hwp.gpu.t": "GPU — RDNA 2",
  "hwp.gpu.d":
    '"Cyan Skillfish" (gfx1013), do 40 możliwych do odblokowania jednostek obliczeniowych.',
  "hwp.mem.t": "Pamięć — 16 GB GDDR6",
  "hwp.mem.d":
    "Współdzielona (UMA) między CPU a GPU; na Linuksie GTT rozszerza pamięć wideo.",
  "hwp.perf.t": "Moc — ~11 TFLOPS",
  "hwp.perf.d": "FP32 przy 40 CU / 2000 MHz (vkpeak), z akceleracją Vulkan.",
  "hwp.quirks.h": "Wady sprzętowe (i jak je naprawiamy)",
  "hwp.q1.t": "Zepsute HPD w DisplayPort",
  "hwp.q1.d":
    "Wykrywanie monitora nie działa → dedykowany demon + parametr jądra <code>video=DP-1:e</code>.",
  "hwp.q2.t": "Zepsute usypianie",
  "hwp.q2.d":
    "Płytka się nie wybudza → wszystkie stany uśpienia trwale wyłączone.",
  "hwp.q3.t": "Niestabilne IOMMU",
  "hwp.q3.d": "Nigdy nie włączać → system zawsze startuje bez IOMMU.",
  "hwp.q4.t": "Marginalne chłodzenie",
  "hwp.q4.d":
    "Tylko czujnik edge, brak czujnika VRAM → zabezpieczenie termiczne 85 °C zawsze aktywne.",
  "hwp.cta": "Więcej w dokumentacji →",

  "bm.h": "Zmierzona wydajność",
  "bm.sub":
    "vkpeak FP32-scalar (GFLOPS) na <strong>tej samej</strong> BC-250, przed i po SkillFishOS.",
  "bm.bar1": "Punkt odniesienia — XanMod, 24 CU",
  "bm.bar2": "tkg + governor, 24 CU",
  "bm.bar3": "SkillFishOS — tkg + governor + 40 CU",
  "bm.unit": "GFLOPS",
  "bm.s1.l": "FP32 vs punkt odniesienia",
  "bm.s2.l": "GFLOPS FP32 (≈11,3 TFLOPS)",
  "bm.s3.l": "GFLOPS FP16 (vec4)",
  "bm.s4.l": "GIOPS int8 (iloczyn skalarny)",
  "bm.note":
    "Pomiary <strong>vkpeak</strong> (Vulkan compute) na tej samej płytce, na zimno i w spoczynku. Z aktywnymi 40 CU GPU daje <strong>1,84×</strong> względem systemu wyjściowego. W spoczynku governor schodzi do 350 MHz; edge ~54 °C po obciążeniu obliczeniowym.",
  "bm.src":
    "Źródło: pomiary projektu na prawdziwym sprzęcie (vkpeak). Szczegóły w",
  "bm.gpulink": "GPU, governor i podkręcanie",

  "wk.h": "Pod realnym obciążeniem — Black Myth: Wukong (1080p)",
  "wk.note":
    "Telemetria z ~4 minut gry: <strong>CPU i GPU utrzymują pełne podkręcenie</strong> w granicy 85 °C — governor, OC i zabezpieczenie termiczne radzą sobie z wymagającym tytułem AAA. (Wukong jest ograniczony przez <em>CPU/draw-calls</em>: liczy się tu stabilność pod obciążeniem, nie rozdzielczość.)",
  "wk.l.gpu": "GPU (safe-point)",
  "wk.l.gpuc": "GPU edge (maks. 81)",
  "wk.l.pwr": "Pobór mocy (szczyt 182 W)",
  "wk.l.cpu": "CPU (podkręcony)",
  "wk.l.vram": "Używana VRAM",
  "wk.l.fan": "Wentylator",

  "bs.h": "Prawdziwe zrzuty — zrobione na naszym sprzęcie",
  "bs.sub":
    "Żadnych renderów ani makiet: rzeczywiste zrzuty ekranu z benchmarków, na <strong>naszej własnej</strong> BC-250 ze SkillFishOS. Dotknij obrazu, aby powiększyć.",
  "bs.wk.c":
    "Black Myth: Wukong — średnio <strong>112 FPS</strong> w 1080p (maks. 128, 1% low 101). APU AMD BC-250, GPU RADV gfx1013.",
  "bs.hv.c":
    "Unigine Heaven 4.0 — <strong>113,7 FPS</strong>, wynik <strong>2865</strong> (1080p Ultra, 8× AA, teselacja Extreme). Jądro 7.0.10-skillfishos.",
  "bs.sc.c":
    "Unigine Heaven — scena renderowana w czasie rzeczywistym na BC-250 podczas testu.",

  "gb.h": "Benchmarki gier — prawdziwe wyniki",
  "gb.sub":
    "Zmierzone na BC-250 ze SkillFishOS, w 1080p. Płytka za <strong>~50&nbsp;€</strong>, która gra w klasie <strong>Radeon RX&nbsp;6600</strong>.",
  "gb.wk.v": "112 FPS",
  "gb.wk.l": "Black Myth: Wukong · średnia w 1080p",
  "gb.hv.v": "2865",
  "gb.hv.l": "Unigine Heaven · 1080p Ultra/Extreme · 8× AA · 113 FPS",
  "gb.sp.v": "12 938",
  "gb.sp.l": "Unigine Superposition · 1080p High · (5513 w Extreme)",

  "cmp.os.h": "Ten sam sprzęt, +34% tylko przez zmianę systemu",
  "cmp.os.sub":
    "Superposition 1080p Extreme, na <strong>tej samej BC-250</strong>: SkillFishOS kontra inna dystrybucja na fabrycznych zegarach.",
  "cmp.os.b1": "SkillFishOS — GPU 2230 · CPU 3900",
  "cmp.os.b2": "Inna dystrybucja (Bazzite) — GPU 2100 · CPU 3436",
  "cmp.os.note":
    "Odblokowane 40 CU, governor podnoszący GPU do 2230 MHz oraz podkręcenie i undervolt CPU: <strong>+34% realnej wydajności</strong> z dokładnie tego samego układu. Źródło: oficjalny ranking Unigine.",

  "cmp.gpu.h": "Starcie z Radeonami desktopowymi",
  "cmp.gpu.sub":
    "Superposition 1080p High: BC-250 ze SkillFishOS dorównuje <strong>RX&nbsp;6600/6600&nbsp;XT</strong> za 200&nbsp;€+.",
  "cmp.gpu.b1": "SkillFishOS — BC-250 (~50 €)",
  "cmp.gpu.b2": "Radeon RX 6600 / 6600 XT",
  "cmp.gpu.b3": "Radeon RX 6700 / 6750 XT",
  "cmp.gpu.note":
    "Surowa moc obliczeniowa RX&nbsp;6700 (~11,3 TFLOPS), wydajność w grach RX&nbsp;6600/6600&nbsp;XT — na płytce za ~50&nbsp;€. Półniestandardowy układ <strong>RDNA&nbsp;2 klasy konsolowej</strong> („Oberon”, gfx1013), uwolniony na Linuksie.",
  "cmp.axis": "Wynik Superposition",

  "oc.h": "Podkręcanie i undervolt — dobrane ręcznie",
  "oc.sub":
    "Krzywe V/F zmierzone przez SMU na APU „Oberon”, z realną walidacją termiczną. Wszystko sterowalne z <strong>Tunera</strong> gotowymi ustawieniami.",
  "oc.cpu.v": "4,0 GHz",
  "oc.cpu.l":
    "CPU 8 rdzeni na wszystkich rdzeniach · zmierzone krok po kroku · 0 MCE",
  "oc.uv.v": "−194 mV",
  "oc.uv.l": "Undervolt CPU przy 3,7 GHz (1206→1012 mV) bez strat",
  "oc.gpu.v": "2230 MHz",
  "oc.gpu.l": "GPU · 40 CU · dedykowany governor SMU",
  "oc.cap.v": "85 °C",
  "oc.cap.l": "Limit termiczny CPU+GPU: obniża zegar, nigdy nie uszkadza",
  "oc.note":
    "Dla każdej częstotliwości znaleźliśmy <strong>najniższe stabilne napięcie</strong>, odczytując rzeczywisty VID z SMU i walidując 120-sekundowym stresem. Ustawienia <strong>Stock · Performance · Turbo · Crazy</strong> stosują te profile jednym kliknięciem, a zabezpieczenie termiczne trzyma wszystko w granicy 85 °C. Pełne szczegóły w dokumentacji.",

  "don.title": "Wesprzyj nas — postaw nam kawę",
  "don.eye": "Wesprzyj projekt",
  "don.h2": 'Pomóż wykuć <span class="gold-text">przyszłość</span> SkillFishOS',
  "don.sub":
    "SkillFishOS jest i pozostanie <strong>darmowy i otwartoźródłowy</strong>. Ale stoi za nim <strong>mały zespół</strong> i jedna jedyna płytka: drobny wkład sprawia, że rozwój idzie szybciej i się nie zatrzymuje.",

  "don.why.h": "Mały zespół. Jedna płytka.",
  "don.why.p1":
    "Za SkillFishOS stoi <strong>mały zespół</strong>, który rozwija, testuje i utrzymuje wszystko — jądro, aplikacje, motyw, repozytorium i stronę — po godzinach i <strong>całkowicie z własnej kieszeni</strong>. System jest i pozostanie darmowy oraz otwartoźródłowy: żadnych opłat, żadnych reklam.",
  "don.why.p2":
    "Dziś mamy <strong>tylko jedną BC-250</strong>. Każda łatka do jądra, governora czy podkręcania musi być sprawdzona na jedynej płytce, jaką mamy: jeśli zawiesi się w trakcie testu, rozwój staje. Żadnych testów równoległych, żadnego porównania różnych układów („loteria krzemowa”), zero marginesu na bezpieczne eksperymenty. <strong>Twoja pomoc to zmienia.</strong>",

  "don.use.h": "Na co idą darowizny",
  "don.use.sub":
    "Pełna przejrzystość: każde euro idzie na szybszy i lepszy rozwój.",
  "don.u1.t": "Kolejne płytki BC-250",
  "don.u1.d":
    "Więcej płytek = szybszy i bezpieczniejszy rozwój: testy równoległe, porównanie krzemu i zapas, gdy jedna padnie.",
  "don.u2.t": "Obudowy i radiatory",
  "don.u2.d":
    "Lepsze chłodzenie, by podnieść podkręcanie i stabilność — oraz by sprawdzić rozwiązania termiczne warte polecenia.",
  "don.u3.t": "Infrastruktura",
  "don.u3.d":
    "Domena, hosting, mirrory i CI: koszty utrzymania strony, repozytorium APT i plików do pobrania — dziś w całości na nas.",
  "don.u4.t": "Czas na rozwój",
  "don.u4.d":
    "Każdy wkład pozwala nam poświęcić więcej godzin nowym funkcjom, poprawkom i wsparciu, zamiast czemuś innemu.",

  "don.give.h": "Postaw nam kawę ",
  "don.give.p":
    "Wybierz kwotę: PayPal otworzy się z gotową sumą. Nawet <strong>1, 2 czy 5 €</strong> robi ogromną różnicę.",
  "don.give.custom": "Dowolna kwota",
  "don.give.or": "albo zeskanuj kod QR telefonem",
  "don.give.scan": "Zeskanuj, aby wesprzeć",
  "don.give.note":
    "Jednorazowa darowizna przez <strong>PayPal</strong>: bez zobowiązań, bez subskrypcji. SkillFishOS pozostaje darmowy i otwartoźródłowy na zawsze.",
  "don.thanks":
    "Z całego serca dziękujemy — każdy wkład rozpala kolejny element tej konsoli. ",

  "comm.h": "Nie możesz wesprzeć finansowo? Pomóż inaczej — za darmo",
  "comm.sub":
    "Trzy gesty na minutę, które rozwijają projekt tak samo jak darowizna.",
  "comm.star.t": "Zostaw gwiazdkę na GitHubie",
  "comm.star.d":
    "Więcej gwiazdek = większa widoczność = więcej osób odkrywa SkillFishOS i pomaga. To najszybszy sposób, by nas wesprzeć.",
  "comm.star.btn": "Zostaw gwiazdkę →",
  "comm.review.t": "Napisz recenzję",
  "comm.review.d":
    "Testowałeś SkillFishOS? Opowiedz, jak poszło, na SourceForge: recenzje przekonują nowych do spróbowania i mówią nam, co poprawić.",
  "comm.review.btn": "Zrecenzuj na SourceForge →",
  "comm.idea.t": "Zaproponuj pomysł",
  "comm.idea.d":
    "Która funkcja ułatwiłaby ci życie? Otwórz dyskusję: pomysły użytkowników wyznaczają kolejne wydania SkillFishOS.",
  "comm.idea.btn": "Zaproponuj funkcję →",

  "ct.title": "Kontakt — SkillFishOS",
  "ct.eye": "Kontakt",
  "ct.h2": "Napisz do nas",
  "ct.sub":
    "Wsparcie, informacje lub cokolwiek innego: wypełnij formularz, a odpowiemy e-mailem.",
  "ct.f.name": "Imię",
  "ct.f.email": "Twój e-mail",
  "ct.f.type": "Rodzaj zgłoszenia",
  "ct.f.msg": "Wiadomość",
  "ct.f.captcha": "Ile wynosi",
  "ct.type.support": "Wsparcie",
  "ct.type.info": "Informacje",
  "ct.type.other": "Inne",
  "ct.send": "Wyślij zgłoszenie",
  "ct.privacy":
    "Nie publikujemy naszego adresu e-mail, by ograniczyć spam: formularz przekazuje go bezpiecznie. Podane dane służą wyłącznie do udzielenia odpowiedzi.",
  "ct.ok": "Wiadomość wysłana! Odpowiemy najszybciej, jak to możliwe.",
  "ct.err.captcha": "Błędna weryfikacja antyspamowa. Spróbuj ponownie.",
  "ct.err.fields":
    "Sprawdź pola: imię, poprawny e-mail i wiadomość są wymagane.",
  "ct.err.send":
    "Wysyłka nie powiodła się. Spróbuj później lub napisz do nas na GitHubie.",
  "ct.err.generic": "Wystąpił błąd. Spróbuj ponownie.",
  "news.title": "Nowości i roadmapa",
  "news.eye": "Na bieżąco",
  "news.h1": "Co się zmieniło,<br>i co nadchodzi",
  "news.h.news": "Nowości",
  "news.h.road": "Roadmapa",
  "nav.news": "Nowości",
  "dl.fast.h": "Najszybszy sposób, z Europy",
  "dl.fast.sub":
    "Internet Archive przechowuje nasze obrazy ISO i udostępnia je z własnych serwerów. Zmierzone z łącza we Włoszech: <strong>około 5 MB/s</strong> wobec 0,4 z SourceForge, które wszystko wysyła z San Diego. Ten sam plik, ta sama suma kontrolna.",
  "dl.fast.bc250": "BC-250",
  "dl.fast.generic": "Generic (PC/VM)",
  "dl.sf.h": "Albo z SourceForge",
  "dl.sf.sub":
    "Wieloletni mirror projektu: wolniejszy z Europy, ale to stamtąd liczymy pobrania.",
  "dl.tor.h": "Albo przez torrent",
  "dl.tor.bc250": "⇅ BC-250 · torrent",
  "dl.tor.generic": "⇅ Generic · torrent",
  "dl.tor.magnet": "magnet",
};

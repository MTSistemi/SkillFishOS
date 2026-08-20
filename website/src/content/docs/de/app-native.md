---
title: Eigene Anwendungen — Tuner und AI
description: Die grafischen Werkzeuge von SkillFishOS, um Hardware und KI ohne Terminal zu steuern.
group: Benutzung
order: 3
---

SkillFishOS bringt zwei eigene Anwendungen mit (in **PyQt6** geschrieben, mit Kvantum gestaltet), die die Steuerung von Hardware und KI **ohne Terminal** in die Hand der Benutzer legen.

## SkillFishOS Tuner

Der **Tuner** ist die Schaltzentrale für die Hardware. Damit lassen sich einstellen:

- **Übertaktung und Undervolting der CPU**;
- die **sicheren Punkte der GPU** (über den SMU-Governor, siehe [GPU und Übertaktung](/de/docs/gpu-overclock));
- der **Lüfter** (PWM-Steuerung);
- der **UMA-Grafikspeicher** (erfordert einen Neustart);
- die **Recheneinheiten im laufenden Betrieb** — siehe unten.

### Recheneinheiten im Betrieb (Raster)

Der Tuner zeigt die CU der GPU als **Raster aus Kästchen** (4 Reihen SE/SH × 5 WGP): **grün = aktiv, rot = aus**. Umschalten geht **im Betrieb, ohne Neustart**: klick auf die Paare (1 WGP = 2 CU) oder nimm die **Vorgaben 24 / 32 / 40 CU**, dann *Anwenden*. Die ersten 24 CU sind der Grundwert des Treibers und bleiben immer an (siehe [GPU und Übertaktung](/de/docs/gpu-overclock)).

![SkillFishOS Tuner — das Raster der Recheneinheiten im Betrieb, die Vorgaben und die CU-Prüfung](/img/tuner.jpg)

### CU-Prüfung (Silizium-Lotterie)

Der Knopf **„CU-Prüfung“** prüft den Zustand der zusätzlichen CU: er schaltet jedes Paar einzeln ein, fordert es mit **vkpeak** und achtet auf **Fehler und Hänger der GPU**, am Schluss noch einmal mit allen 40. Er ist dafür da, **defekte CU** auf aussortierten APUs zu finden, damit du weißt, ob dein Chip alle vierzig trägt.

![Ergebnis der CU-Prüfung — alle Paare in Ordnung, 40 CU stabil bei 11380 GFLOPS, keine Defekte](/img/cu-test.jpg)

### Der Ablauf „Prüfen“ und der Monitor in Echtzeit

Der Ablauf hinter dem Knopf **„Prüfen“** (CPU, GPU, CU, Lüfter): Änderung anwenden → Messung fahren → Stabilität **nachweisen** und, wenn etwas nicht stimmt, automatisch **zurücknehmen**. Sobald eine Prüfung startet, öffnet sich das Fenster **[SkillFishOS Telemetry](#skillfishos-telemetry)** mit Kurven in Echtzeit für **Temperatur, Takt, Spannung und Lüfter** (es lässt sich schließen).

![SkillFishOS Telemetry während einer Prüfung im Tuner — Kurven in Echtzeit für Temperatur, Takt, GPU-Spannung und Lüfter](/img/monitor.jpg)

Der Aufbau: eine Oberfläche für den Benutzer und ein kleiner **Dienst mit Root-Rechten**, der die heiklen Eingriffe ausführt. Auf einem persönlichen Rechner ist er so eingerichtet, dass er nicht bei jedem Handgriff nach einem Passwort fragt. Auch das HUD auf dem Schreibtisch zeigt die **aktiven CU** in Echtzeit.

### Governor-Betriebsarten: Balanced und Performance

Die GPU der BC-250 wird von einem **SMU-Governor** geführt, der den Takt mit der Last hebt und senkt. Der Tuner bietet zwei Betriebsarten über einen Schalter:

- **Balanced** *(Vorgabe)* — im Leerlauf fällt der Takt (bis auf 350 MHz) und steigt unter Last: weniger Verbrauch und niedrigere Temperaturen im Alltag.
- **Performance** — die GPU **bleibt bei Last auf ihrem Höchsttakt stehen**, die kleinen Taktschwankungen verschwinden. In unserer Messung von *Black Myth: Wukong* bringt das **+11% Bilder** (von rund 100 auf rund 111 im Mittel) und ein höheres **1% low** (92 → 102), bei sonst gleichen Bedingungen.

Beide bleiben unter der **Temperaturgrenze von 85 °C**: die Betriebsart Performance drückt stärker, sie schaltet die Schutzmechanismen nicht ab.

### „Finde mein Maximum“ (Assistenten für CPU und GPU)

Jede BC-250 ist anders ([Silizium-Lotterie](/de/docs/gpu-overclock)). Der Tuner bringt zwei Assistenten **„Finde mein Maximum“** mit, die **deine** Platine ausmessen:

- **GPU** — geht in Stufen hoch (2000 → 2200 MHz, in Schritten von 50), wendet jede Stufe an, **prüft** sie und bleibt bei der letzten stabilen stehen.
- **CPU** — läuft die Stufen aus Takt und Undervolting ab (von 3600 MHz bis 4000 MHz bei Skala −36), nach demselben Muster aus **Prüfen und Zurücknehmen**: hält eine Stufe nicht, kehrt er zum letzten guten Wert zurück.

Alles ist **absturzsicher**: der auf der Platte hinterlegte Arbeitswert ist immer der letzte stabile, ein Einfrieren mitten in der Prüfung lässt die Platine beim nächsten Start also nie auf einem unruhigen Profil stehen.

### Mein Silizium

Das Fenster **„Mein Silizium“** fasst das Profil deiner Platine zusammen — bester gefundener Wert für CPU und GPU, gesunde CU, Zähler der erkannten Aussetzer — und lässt dich das Ergebnis **anonym teilen**, in der Datenbank zur Silizium-Lotterie (es öffnet ein vorausgefülltes GitHub-Issue). Je mehr Daten zusammenkommen, desto besser werden die empfohlenen Profile für alle.

## SkillFishOS Telemetry

**Telemetry** zeigt in Echtzeit Temperatur, Takt, Auslastung von CPU und GPU, Spannungen, Leistungsaufnahme und Lüfter. Es öffnet sich bei Prüfungen im Tuner von selbst, ist aber auch eine eigenständige Anwendung. Der Knopf **REC** zeichnet eine Messreihe in eine **`.sfmon`**-Datei auf (in `~/SkillFishOS-benchmarks/`): öffnest du sie wieder, wird Telemetry zum **Auswertungswerkzeug** mit einem Zeitregler, um den Durchlauf Sekunde für Sekunde nachzusehen.

![SkillFishOS Telemetry — Kurven mit beschrifteter Achse und das Feld mit dem Takt je Kern und Thread](/img/telemetry-percore.jpg)

### Takt je Kern und Thread

Mit [acht freigeschalteten Kernen](/de/docs/hardware-bc250) sagt eine einzige Zahl „CPU-Takt“ herzlich wenig: im Leerlauf können die sechzehn Threads **gleichzeitig** bei 800, 1775 und 3990 MHz stehen, der abgelesene Wert hängt also nur davon ab, welcher Kern gerade abgefragt wurde.

Das untere Feld zeichnet **einen Balken je Thread**, nach physischem Kern gepaart und mit `Kern·Thread` beschriftet. Die Farbe geht von Messing zu Glut, je höher der Thread steigt, die MHz stehen auf jedem Balken, und die Kopfzeile fasst **Minimum, Mittel, Maximum und die Zahl der laufenden Threads** zusammen. Threads, die du im Tuner abgeschaltet hast, verschwinden nicht: sie bleiben als gestrichelter Platz mit der Aufschrift **„off“** stehen, sodass die tatsächliche Einstellung auf einen Blick sichtbar ist.

### Lesbare Achsen

Jede Kurve hat nun eine **Skala mit Linien und Werten an der senkrechten Achse**, an menschliche Zahlen angelehnt (`0 / 1000 / 2000 / 3000`, nicht `-160 / 1394 / 2948`). Die Null wird zum Boden, wenn die Werte in ihrer Nähe liegen, eine Kurve für MHz oder Lüfterdrehzahl zeigt also nie eine negative Grundlinie; und eine flache Linie wird nicht mehr so weit gedehnt, bis das Rauschen wie ein Gebirge aussieht.

## SkillFishOS AI

Das **KI-Fenster** schaltet die lokale KI mit einem Klick ein und aus und gibt GPU und Speicher für Spiele frei, wenn sie nicht gebraucht wird. Es ist das „einfache“ Gesicht dessen, was unter [KI auf dem Gerät](/de/docs/ai-locale) beschrieben ist.

![SkillFishOS-KI-Fenster — lokaler Motor (Qwen3 14B) auf der GPU über Vulkan, mit einem Klick ein und aus](/img/ai-panel.jpg)

## Warum es sie gibt

Das Ziel von SkillFishOS ist, dass **jede und jeder** — auch die Jüngsten — das System benutzen und einstellen kann, ohne Terminalbefehle lernen zu müssen. Diese Anwendungen übersetzen verwickelte Eingriffe (SMU-Governor, Kernel-Parameter, Schnappschüsse und Rückkehr) in ein paar Klicks und lassen dabei die **Schutzmechanismen** (Temperaturgrenze, Prüfen mit Rücknahme) durchgehend aktiv.

## Quellen

- [PyQt6 / Qt for Python](https://doc.qt.io/qtforpython/) · [Kvantum](https://github.com/tsujan/Kvantum)
- [sysbench](https://github.com/akopytov/sysbench) · [vkpeak](https://github.com/nihui/vkpeak)
- Projekt-Repository — [github.com/MTSistemi/SkillFishOS](https://github.com/MTSistemi/SkillFishOS) (`apps/tuner`, `apps/ai-panel`)

---
title: GPU, CPU, Übertaktung und Undervolting
description: Wie SkillFishOS die Takte, Spannungen und Temperaturen der BC-250 steuert — mit den echten, auf der Hardware gemessenen Zahlen.
group: System
order: 2
---

Auf einer gewöhnlichen APU stellt man die Takte über das sysfs von `amdgpu` ein. Auf der BC-250 **geht das nicht**: die Steuerung läuft über die **SMU** (System Management Unit) und braucht eigene Werkzeuge. SkillFishOS bringt sie alle mit, vorbereitet mit einer sicheren Werkskurve und einem Schutz vor Überhitzung.

> **Achtung:** **Silizium-Lotterie.** Jede Zahl auf dieser Seite ist **auf unserer BC-250 gemessen**. Jede Platine ist anders: die eine verträgt eine steilere Kurve, die andere weniger. Deshalb startet SkillFishOS **mit der Werkskurve** (Vorgabe **Performance**, Deckel bei 2100 MHz) und lässt dich sie über den [Tuner](/de/docs/control-center) ändern, der jede Kurve **auf deiner Platine** mit einer selbsttätigen 25-Sekunden-Prüfung testet und von sich aus zurücknimmt, wenn sie nicht hält.

## Die Spannungs-/Frequenzkurve und die drei Vorgaben

Der [Tuner](/de/docs/control-center) steuert die GPU über eine **Spannungs-/Frequenzkurve**: MHz waagerecht, Millivolt senkrecht, Punkte, die du im Diagramm ziehst oder in die Tabelle daneben einträgst. Drei Vorgaben verschieben den **Deckel** der Kurve:

| Vorgabe | GPU-Deckel | Anmerkungen |
|---|---|---|
| **Cautious** | 1850 MHz | Der Sweet Spot mit der serienmäßigen Kühlung: fast dieselbe Bildrate, zehn Grad kühler |
| **Balanced** | 2000 MHz | Kompromiss zwischen Takt und Wärme |
| **Performance** | 2100 MHz | Die Kurve aus fünfzehn Punkten, gemessen auf der Entwicklungsplatine — die, die wir standardmäßig ausliefern |

**Anwenden ist ein Versuch, kein sofortiges Schreiben.** Eine Kurve, die zu wenig Spannung verlangt, hängt die Platine auf, und auf der BC-250 löst man ein Hängen nur durch Trennen vom Strom. Deshalb behält Anwenden die vorige Kurve auf der Platte, probiert die Kandidatin **25 Sekunden** lang aus und wartet auf Bestätigung: drück Behalten, und sie wird wirklich geschrieben; sonst — oder wenn die Platine hängt und von selbst neu startet — kehrt beim Start die vorige Kurve zurück.

## Der V/F-Governor der GPU

Die Takte der GPU steuert **skillfish-vf-governor**, unser Dienst, der dem Werks-Governor Takt und Spannung abnimmt und sie direkt über die SMU führt, wobei er einen **Frequenzdeckel** hält, den Wärme und Verbrauch senken dürfen und den er, sobald sich die Platine beruhigt hat, wieder zurückgibt. Ein eigener Vorgang, **skillfish-vf-watchdog**, übernimmt, falls der Governor mit erzwungenem Takt abstürzt.

Gemessen an *Black Myth: Wukong*, dieselbe Sitzung, dieselben 84 °C in beiden Durchläufen: **+4,5 %** auf kalter Platine, **+11 %** auf warmer — gegenüber dem Werks-Governor. Der Vorteil wächst mit der Temperatur, weil der Werks-Governor beim Aufwärmen der Platine Takt abgibt und unserer nicht.

> Das übliche sysfs von amdgpu (`power_dpm_force_performance_level`, `pp_dpm_sclk`) steuert die BC-250 **nicht** — das tut allein skillfish-vf-governor. Die GPU geht nur bei echter **grafischer Auslastung** auf den Deckel.

## Übertaktung und Undervolting der CPU

Die CPU (**8 Kerne / 16 Threads** Zen 2 „Oberon“, zwei davon von SkillFishOS über die SMU freigeschaltet — auch schon vor dem Start, mit einem EFI-Programm, in einem einzigen Neustart) betreut für die Übertaktung ein einmalig laufender Dienst, **`bc250-smu-oc.service`**, der die Werte aus `/etc/bc250-smu-oc.conf` mit dem Projekt [bc250_smu_oc](https://github.com/bc250-collective/bc250_smu_oc) anwendet. Danach zeigt er sich als *inactive* — das gehört so (er läuft einmalig).

Was wir gemessen haben, als wir **unsere** Platine ausgereizt haben:

- **3700 MHz** mit Undervolting auf rund **1106 mV** (`scale −16`);
- **3900 MHz** bei rund **1199 mV** (`scale −24`);
- **4,0 GHz** bei rund **1224 mV** (`scale −36`) über 120 s Dauerlast geprüft, mit Spitze bei **83 °C** — das nutzbare Maximum dieses Exemplars;
- **harte Vid-Grenze: 1,325 V** (nie überschritten).

Beim **Undervolting** geht es nicht ums „Draufdrücken“, sondern darum, dieselbe Arbeit mit **weniger Wärme und weniger Verbrauch** zu leisten: bei gegebenem Takt die Spannung senken, bis es gerade noch stabil bleibt — die Temperatur fällt und es bleibt Wärmereserve für den Rest der APU.

### Wärmekopplung CPU↔GPU

CPU und GPU sitzen auf **demselben Plättchen** und teilen sich **dasselbe Leistungsbudget**. Bei **gemischter** Last (ein forderndes Spiel: CPU und GPU zugleich) schützt sich die APU selbst, und die CPU geht von sich aus auf etwa **3450 MHz** zurück, um im Budget und unter 85 °C zu bleiben. **Das ist kein Fehler**: der Chip gibt die am wenigsten nützlichen Megahertz ab. Aus demselben Grund lässt ein Undervolting der CPU der GPU mehr Wärme-„Raum“ und umgekehrt.

## Die 40 Recheneinheiten — im Betrieb

Die BC-250 hat **40 CU** (20 Paare), der Treiber schaltet aber standardmäßig **24** frei. SkillFishOS bringt sie **beim Start, ohne weiteren Schritt** auf 40; im [Tuner](/de/docs/control-center) stellst du die Zahl **live** ein, indem du den gewünschten Wert einträgst oder auf die 20 gepaarten Kästchen klickst. Die ersten 24 CU sind vom Treiber festgelegt und immer an.

Mit allen 40 CU misst die GPU kalt **11385 GFLOPS** FP32 (vkpeak) gegenüber rund **6141** mit den 24 des Grundwerts: **+85 %**. Unter Dauerlast (warm) pendelt sie sich bei etwa **10214 GFLOPS** ein. Die gemessene Speicherbandbreite (clpeak) liegt bei **~350–367 GB/s**.

> **Silizium-Lotterie.** Bei geretteten oder „aussortierten“ Chips können einzelne CU schwach sein. Der [Tuner](/de/docs/control-center) hat eine **„CU-Prüfung“**, die jedes Paar mit vkpeak belastet und Fehler oder Hänger der GPU meldet, damit du dir sicher sein kannst, dass dein Chip alle 40 trägt. (Der Weg führt über `umr` und das Schreiben der WGP-Masken — Dank an [bc250-cu-live-manager](https://github.com/WinnieLV/bc250-cu-live-manager), eigene Neuumsetzung.)

## Temperaturschutz — die Grenze von 85 °C

Die Wärmegrenze liegt bei **85 °C** und wird auf zwei Ebenen durchgesetzt:

1. **vom Governor**: `gradi_max` und `watt_max` in `/etc/skillfish-vf-governor.json` senken den Frequenzdeckel, *bevor* 85 °C oder die Leistungsgrenze (unsere, nicht die der Firmware) überschritten werden, und geben ihn zurück, sobald sich die Platine beruhigt hat;
2. **vom System**: **skillfish-vf-watchdog**, ein eigener Vorgang, der übernimmt, falls der Governor mit erzwungenem Takt abstürzt.

Was man über die serienmäßige Kühlung wissen sollte (siehe auch [BC-250-Hardware](/de/docs/hardware-bc250) für **im 3D-Druck herstellbare Gehäuse und empfohlene Lüfter**):

- der werkseitige Kühlkörper ist **knapp bemessen**: Vergleiche von Messungen „direkt hintereinander“ werden vom *Wärmestau* verfälscht — lass die Platine zwischen den Durchläufen ein paar Minuten abkühlen;
- es gibt nur den *Rand*-Fühler der GPU; einen Temperaturfühler für den **Grafikspeicher gibt es nicht**;
- die Speicherbandbreite ist gut, aber der `mclk` lässt sich **nicht** verstellen.

## Ein Beispiel aus der Praxis: Spiele im CPU-Limit

Manche Titel — etwa *Black Myth: Wukong* im **Spielgeschehen** — hängen an der **CPU und den Zeichenaufrufen**: die Bildrate hängt kaum von der Auflösung oder vom GPU-Takt ab. Dort helfen eine übertaktete **CPU** und gute Kühlung. Zum Hochskalieren läuft FSR 4 über [OptiScaler](https://github.com/optiscaler/OptiScaler) auf dem DLSS-Pfad des Spiels (siehe [Gaming](/de/docs/gaming)).

Wenn die Last **wirklich** an der GPU hängt (etwa der *Kameraflug* im Wukong-Benchmark), zählt der Deckel der Kurve: im [Tuner](/de/docs/control-center) die Vorgabe von Cautious oder Balanced auf **Performance** (2100 MHz) hochstellen, oder eine eigene Kurve eintragen. Der im Wukong-Benchmark gemessene Vorteil gegenüber dem alten Werks-Governor liegt bei **+4,5 % auf kalter, +11 % auf warmer Platine**: der V/F-Governor gibt beim Aufwärmen keinen Takt ab, der Werks-Governor schon. Es bleibt eine harte physische Grenze: **1129 mV**, der Spannungsdeckel, den amdgpu für diese GPU angibt — keine Kurve kann ihn überschreiten.

## Und das alles ohne Terminal

Takte, die GPU-Kurve, Lüfter und Recheneinheiten stellst du im Fenster des **Tuners** ein, mit den drei fertigen Vorgaben der GPU und einer **selbsttätigen 25-Sekunden-Probe, die zur vorigen Kurve zurückkehrt**, falls deine Platine sie nicht hält — siehe [Control Center](/de/docs/control-center). Das ist der empfohlene Weg: fang bei Cautious an, geh auf Balanced oder Performance — der Tuner prüft alles auf **deiner** BC-250.

## Quellen

- skillfish-vf-governor — unser V/F-Governor für die GPU, direkte SMU-Steuerung mit einstellbarem Deckel
- [bc250_smu_oc (bc250-collective)](https://github.com/bc250-collective/bc250_smu_oc) — Übertaktung und Undervolting der CPU über die SMU
- [bc250.info](https://bc250.info) — sichere Punkte und Wärmehinweise der Gemeinschaft
- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) — Messungen zu FP32 und Speicherbandbreite

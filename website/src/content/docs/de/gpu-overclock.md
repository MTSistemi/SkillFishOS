---
title: GPU, CPU, Übertaktung und Undervolting
description: Wie SkillFishOS die Takte, Spannungen und Temperaturen der BC-250 steuert — mit den echten, auf der Hardware gemessenen Zahlen.
group: System
order: 2
---

Auf einer gewöhnlichen APU stellt man die Takte über das sysfs von `amdgpu` ein. Auf der BC-250 **geht das nicht**: die Steuerung läuft über die **SMU** (System Management Unit) und braucht eigene Werkzeuge. SkillFishOS bringt sie alle mit, vorbereitet mit sicheren Profilen und einem Schutz vor Überhitzung.

> **Achtung:** **Silizium-Lotterie.** Jede Zahl auf dieser Seite ist **auf unserer BC-250 gemessen**. Jede Platine ist anders: die eine verträgt ein tieferes Undervolting, die andere weniger. Deshalb startet SkillFishOS **immer im Profil Stock** und lässt dich über den [Tuner](/de/docs/app-native) höher steigen, der jedes Profil **auf deiner Platine** mit einer selbsttätigen Prüfung und Rücknahme absichert.

## Die vier Profile

Der [Tuner](/de/docs/app-native) bietet **vier Vorgaben**. Das Abbild startet in **Stock**; die übrigen sind nach der Prüfung einen Klick entfernt.

| Profil | CPU | GPU | Anmerkungen |
|---|---|---|---|
| **Stock** *(Vorgabe des Abbilds)* | 3500 MHz | 1500 MHz | Größte Verträglichkeit auf jeder BC-250 |
| **Performance** | 3700 MHz · ~1106 mV | 2000 MHz | Ausgewogen und mit Undervolting |
| **Turbo** | 3900 MHz · ~1199 mV | 2230 MHz | Kräftiger Schub, unter der Grenze von 85 °C geprüft |
| **Crazy** | 4,0 GHz · ~1224 mV | 2230 MHz | Geprüftes Maximum (~83 °C unter Last) |

Alle Profile halten dieselbe **Wärmegrenze von 85 °C** ein und lassen den **Lüfter auf automatisch**.

## Der SMU-Governor der GPU

Die Takte der GPU steuert der **[cyan-skillfish-governor](https://github.com/Magnap/cyan-skillfish-governor)** (in Rust geschrieben), ein Systemdienst, der in `/etc/cyan-skillfish-governor/config.toml` eingerichtet wird. Er legt *sichere Punkte* aus Takt und Spannung fest: **350 MHz / 700 mV** im Leerlauf und den Profilwert unter Last (etwa 1500/900 in Stock, 2230/1000 in Turbo).

> Das übliche sysfs von amdgpu (`power_dpm_force_performance_level`, `pp_dpm_sclk`) steuert die BC-250 **nicht** — das tut allein der SMU-Governor. Die GPU geht nur bei echter **grafischer Auslastung** auf ihren Höchsttakt.

## Übertaktung und Undervolting der CPU

Die CPU (**8 Kerne / 16 Threads** Zen 2 „Oberon“, zwei davon von SkillFishOS über die SMU freigeschaltet) betreut ein einmalig laufender Dienst, **`bc250-smu-oc.service`**, der die Werte aus `/etc/bc250-smu-oc.conf` mit dem Projekt [bc250_smu_oc](https://github.com/bc250-collective/bc250_smu_oc) anwendet. Danach zeigt er sich als *inactive* — das gehört so (er läuft einmalig).

Was wir gemessen haben, als wir **unsere** Platine ausgereizt haben:

- **3700 MHz** (Vorgabe *Performance*) mit Undervolting auf rund **1106 mV** (`scale −16`);
- **3900 MHz** (Vorgabe *Turbo*) bei rund **1199 mV** (`scale −24`);
- **4,0 GHz** (Vorgabe *Crazy*) bei rund **1224 mV** (`scale −36`) über 120 s Dauerlast geprüft, mit Spitze bei **83 °C** — das nutzbare Maximum dieses Exemplars;
- **harte Vid-Grenze: 1,325 V** (nie überschritten).

Beim **Undervolting** geht es nicht ums „Draufdrücken“, sondern darum, dieselbe Arbeit mit **weniger Wärme und weniger Verbrauch** zu leisten: bei gegebenem Takt die Spannung senken, bis es gerade noch stabil bleibt — die Temperatur fällt und es bleibt Wärmereserve für den Rest der APU.

### Wärmekopplung CPU↔GPU

CPU und GPU sitzen auf **demselben Plättchen** und teilen sich **dasselbe Leistungsbudget**. Bei **gemischter** Last (ein forderndes Spiel: CPU und GPU zugleich) schützt sich die APU selbst, und die CPU geht von sich aus auf etwa **3450 MHz** zurück, um im Budget und unter 85 °C zu bleiben. **Das ist kein Fehler**: der Chip gibt die am wenigsten nützlichen Megahertz ab. Aus demselben Grund lässt ein Undervolting der CPU der GPU mehr Wärme-„Raum“ und umgekehrt.

## Die 40 Recheneinheiten — im Betrieb

Die BC-250 hat **40 CU** (20 WGP, 1 WGP = 2 CU), der Treiber schaltet aber standardmäßig **24** frei. SkillFishOS führt sie **im Betrieb, ohne Neustart** auf 40: das System startet auf dem Grundwert des Treibers (24 CU), und ein Dienst bringt sie beim Start auf 40; im [Tuner](/de/docs/app-native) stellst du die Zahl **live** ein — mit einem Raster aus Kästchen und den Vorgaben 24/32/40. Die ersten 24 CU sind vom Treiber festgelegt und immer an.

Mit allen 40 CU misst die GPU kalt **11385 GFLOPS** FP32 (vkpeak) gegenüber rund **6141** mit den 24 des Grundwerts: **+85 %**. Unter Dauerlast (warm) pendelt sie sich bei etwa **10214 GFLOPS** ein. Die gemessene Speicherbandbreite (clpeak) liegt bei **~350–367 GB/s**.

> **Silizium-Lotterie.** Bei geretteten oder „aussortierten“ Chips können einzelne CU schwach sein. Der [Tuner](/de/docs/app-native) hat eine **„CU-Prüfung“**, die jedes Paar belastet und Fehler oder Hänger der GPU meldet, damit du dir sicher sein kannst, dass dein Chip alle 40 trägt. (Der Weg führt über `umr` und das Schreiben der WGP-Masken — Dank an [bc250-cu-live-manager](https://github.com/WinnieLV/bc250-cu-live-manager), eigene Neuumsetzung.)

## Temperaturschutz — die Grenze von 85 °C

Die Wärmegrenze liegt bei **85 °C** und wird auf zwei Ebenen durchgesetzt:

1. **von der SMU**: der Wert `max_temperature` in der Einrichtung lässt den Chip die Takte senken, *bevor* 85 °C überschritten werden (kein hartes Drosseln);
2. **vom System**: ein Wächter, der **thermal-guard**, der bei Überschreiten der Grenze die Takte in Schritten von 100 MHz senkt, bis es wieder passt.

Was man über die serienmäßige Kühlung wissen sollte (siehe auch [BC-250-Hardware](/de/docs/hardware-bc250) für **im 3D-Druck herstellbare Gehäuse und empfohlene Lüfter**):

- der werkseitige Kühlkörper ist **knapp bemessen**: Vergleiche von Messungen „direkt hintereinander“ werden vom *Wärmestau* verfälscht — lass die Platine zwischen den Durchläufen ein paar Minuten abkühlen;
- es gibt nur den *Rand*-Fühler der GPU; einen Temperaturfühler für den **Grafikspeicher gibt es nicht**;
- die Speicherbandbreite ist gut, aber der `mclk` lässt sich **nicht** verstellen.

## Ein Beispiel aus der Praxis: Spiele im CPU-Limit

Manche Titel — etwa *Black Myth: Wukong* im **Spielgeschehen** — hängen an der **CPU und den Zeichenaufrufen**: die Bildrate hängt kaum von der Auflösung oder vom GPU-Takt ab. Dort helfen eine übertaktete **CPU** und gute Kühlung. Zum Hochskalieren steht FSR 4 **nicht** zur Verfügung (es verlangt RDNA-4-Hardware); nimm gamescope (FSR1/NIS) oder je Spiel [OptiScaler](https://github.com/optiscaler/OptiScaler).

Wenn die Last **wirklich** an der GPU hängt (etwa der *Kameraflug* im Wukong-Benchmark), zählt der Takt: im **Tuner** kannst du den **Governor auf „Performance“** stellen, der die GPU unter Last auf ihrem obersten sicheren Punkt hält (im Leerlauf geht sie trotzdem auf 350 MHz). Im Wukong-Benchmark gemessen: **100 → 111 Bilder/s im Mittel (+11 %)**, 92 → 102 bei den langsamsten Bildern. Zur Sicherheit begrenzt der Tuner die GPU auf **2200 MHz bei 1000 mV** (das stabile Maximum mit serienmäßiger Kühlung) mit einer Spannungskurve aus mehreren Punkten: 2230 MHz bei 1000 mV liegt unter der nötigen Spannung und kann die Maschine hart einfrieren lassen.

## Und das alles ohne Terminal

Takte, Undervolting, Lüfter und Recheneinheiten stellst du im Fenster des **Tuners** ein, mit den vier fertigen Vorgaben und **selbsttätiger Prüfung samt Rücknahme**, falls deine Platine einen Wert nicht hält — siehe [Eigene Anwendungen](/de/docs/app-native). Das ist der empfohlene Weg: fang bei Stock an, geh auf Performance, probier Turbo oder Crazy — der Tuner prüft alles auf **deiner** BC-250.

## Quellen

- [cyan-skillfish-governor (Magnap)](https://github.com/Magnap/cyan-skillfish-governor) — SMU-Governor der GPU
- [bc250_smu_oc (bc250-collective)](https://github.com/bc250-collective/bc250_smu_oc) — Übertaktung und Undervolting der CPU über die SMU
- [bc250.info](https://bc250.info) — sichere Punkte und Wärmehinweise der Gemeinschaft
- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) — Messungen zu FP32 und Speicherbandbreite

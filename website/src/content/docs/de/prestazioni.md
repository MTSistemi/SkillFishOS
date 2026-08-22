---
title: Leistung und Messungen
description: Alle echten Messungen der BC-250 unter SkillFishOS — Bildschirmfotos, vollständige Einstellungen, Takte, Spannungen, Temperaturen und Verbrauch.
group: Nachschlagen
order: 3
---

Das ist der **vollständige Messteil**: jeder Durchlauf wurde auf **unserer eigenen BC-250** unter SkillFishOS gefahren, mit echten Bildschirmfotos, **allen verwendeten Einstellungen** und der Aufzeichnung von **Takt, Spannung, Temperatur, Verbrauch und Lüfterdrehzahl** während des Durchlaufs.

> **Achtung:** **Silizium-Lotterie und Kühlung.** Die Zahlen gelten für *diesen* Chip bei ausreichender Kühlung. Der werkseitige Kühlkörper ist knapp bemessen: Vergleiche „direkt hintereinander“ ohne Pause werden vom *Wärmestau* verfälscht — lass die Platine zwischen den Durchläufen ein paar Minuten abkühlen.

## Bedingungen der Messung (Prüfstand)

Gelten für **alle** folgenden Messungen, sofern nichts anderes steht.

| Punkt | Wert |
|---|---|
| Platine | **AMD BC-250** — APU Zen 2 „Oberon“ + RDNA 2 „Cyan Skillfish“ (`gfx1013`) |
| Speicher | **16 GB GDDR6**, gemeinsam genutzt (UMA) |
| Recheneinheiten | **40 / 40 aktiv** (im Betrieb umgeschaltet, siehe [GPU](/de/docs/gpu-overclock)) |
| Kernel | **7.0.10-skillfishos** (linux-tkg) — die Fassung, mit der diese Zahlen entstanden; heute liefern wir **7.2.0** aus; 7.1.7 wurde mit weniger als 2 % Abweichung nachgemessen |
| Treiber | **Mesa 26.0.8** — RADV (Vulkan) / radeonsi (OpenGL), ACO; heute liefern wir **26.1.6** aus |
| GPU-Governor | cyan-skillfish — Leerlauf **350 MHz / 700 mV**, Last **2230 MHz / ~1000 mV** |
| Übertaktungsprofil | **Turbo/Crazy** (GPU-Grenze 2230 MHz, CPU 3,9–4,0 GHz) |
| Wärmegrenze | **85 °C** (SMU und thermal-guard), Lüfter auf **automatisch** |
| Auflösung | **1920×1080** |

> Zur Erinnerung an den Aufbau: CPU und GPU sitzen auf **demselben Plättchen** und teilen sich **dasselbe Leistungsbudget**. Bei gemischter Last gibt die CPU von sich aus Takt ab (≈3,4–3,5 GHz), um im Budget und unter 85 °C zu bleiben — kein Fehler, sondern der Selbstschutz des Chips.

---

## Black Myth: Wukong — 112 Bilder/s (1080p)

![Black Myth: Wukong — 112 Bilder/s im Mittel bei 1080p auf der AMD BC-250](/img/benchmarks/wukong-112fps.jpg)

| Einstellung | Wert |
|---|---|
| Auflösung | 1920×1080 |
| Bildratenbegrenzung | keine |
| Art der Last | **an CPU und Zeichenaufrufen hängend** |
| Hochskalieren | FSR 4 nicht verfügbar (RDNA 4) → gamescope FSR1/NIS oder OptiScaler |

**Ergebnis:** im Mittel **112 Bilder/s** · Höchstwert **128** · Tiefstwert **92** · 1 % schlechteste **101**.

**Messwerte während des Durchlaufs** (~4 min):

| Größe | Gemessener Wert |
|---|---|
| GPU-Takt | ~1,4–1,6 GHz (*nicht ausgelastet*: das Spiel hängt an der CPU) |
| GPU-Rand | 83–86 °C |
| GPU-Leistungsaufnahme | ~90–140 W |
| GPU-Spannung | ~970–987 mV |
| CPU-Takt | ~3,5 GHz (von 3,9 gefallen wegen des gemeinsamen Budgets) |
| CPU-Temperatur | 85 °C (an der Grenze) |
| Grafikspeicher | ~1,9 GB (Menü) → ~4,4 GB (im Spiel) |
| Lüfter | ~2950–3140 U/min |

> Lehre: im *Spielgeschehen* eines an Zeichenaufrufen hängenden Titels wie Wukong zählen vor allem die **Stabilität der CPU** unter Last und eine gute Kühlung.

### Governor Balanced gegen Performance (Messprogramm)

Der *Kameraflug* des Messprogramms hängt dagegen **an der GPU**, dort zählt der Takt. Stellt man den Governor im Tuner auf **Performance** (er hält die GPU unter Last auf ihrem obersten sicheren Punkt und geht im Leerlauf auf 350 MHz):

| Betriebsart des Governors | Mittel | 5 % schlechteste |
|---|---|---|
| **Balanced** (Vorgabe) | 100 Bilder/s | 92 Bilder/s |
| **Performance** | **111 Bilder/s** | **102 Bilder/s** |

**+11 %** im Mittel und bei den langsamsten Bildern, allein durchs Halten des Takts. Zur Sicherheit begrenzt der Tuner die GPU auf **2200 MHz bei 1000 mV** mit einer Spannungskurve aus mehreren Punkten: 2230 MHz bei 1000 mV liegt unter der nötigen Spannung und kann die Maschine hart einfrieren lassen.

---

## Unigine Superposition — 1080p HIGH: 12938

![Unigine Superposition 1080p High — 12938 Punkte auf der BC-250](/img/benchmarks/superposition-high.jpg)

| Einstellung | Wert |
|---|---|
| Fassung | 1.1 |
| Grafikschnittstelle | **OpenGL** |
| Auflösung | 1920×1080, Vollbild |
| Schattierer | **High** |
| Texturen | High |
| Tiefenschärfe | an |
| Bewegungsunschärfe | an |

**Ergebnis:** **12 938** Punkte · Bilder/s Tiefstwert **75,59** · Mittel **96,77** · Höchstwert **127,16**.
**Vom Programm ausgelesene Ausstattung:** CPU AMD BC-250 **bei 3894 MHz**, RAM 7 GB, GPU AMD BC-250 8 GB (Cyan Skillfish), Kernel 7.0.10-skillfishos.

---

## Unigine Superposition — 1080p EXTREME: 5513

![Unigine Superposition 1080p Extreme — 5513 Punkte auf der BC-250](/img/benchmarks/superposition-extreme.jpg)

| Einstellung | Wert |
|---|---|
| Fassung | 1.1 |
| Grafikschnittstelle | **OpenGL** |
| Auflösung | 1920×1080, Vollbild |
| Schattierer | **Extreme** |
| Texturen | High |
| Tiefenschärfe | an |
| Bewegungsunschärfe | an |

**Ergebnis:** **5513** Punkte · im Mittel **41,25** Bilder/s (Tiefstwert ~32,8 · Höchstwert ~49).

![Unigine Superposition — in Echtzeit berechnete Szene](/img/benchmarks/superposition-scene.jpg)
*Eine Szene aus Superposition, in Echtzeit auf der BC-250 berechnet.*

---

## Unigine Heaven 4.0 — 113,7 Bilder/s · 2865 Punkte

![Unigine Heaven 4.0 — 113,7 Bilder/s, 2865 Punkte auf der BC-250](/img/benchmarks/heaven-113fps.jpg)

| Einstellung | Wert |
|---|---|
| Grafikschnittstelle | **OpenGL** |
| Auflösung | 1920×1080, im Fenster |
| Kantenglättung | **8×** |
| Güte | **Ultra** |
| Tessellierung | **Extreme** |

**Ergebnis:** **113,7 Bilder/s** · **2865** Punkte · Tiefstwert **54,8** · Höchstwert **219,5**.
**Vom Programm ausgelesene Umgebung:** Linux 7.0.10-skillfishos x86_64 · CPU AMD BC-250 ×12 · GPU gfx1013.

![Unigine Heaven — in Echtzeit berechnete Szene](/img/benchmarks/heaven-scene.jpg)
*Die Heaven-Szene, während des Durchlaufs in Echtzeit auf der BC-250 berechnet.*

---

## Rechenarbeit auf der GPU — vkpeak (synthetisch)

Vulkan-Rechendurchsatz auf **derselben** Platine, vor und nach dem Freischalten der 40 CU.

| Größe | Grundwert 24 CU | SkillFishOS 40 CU |
|---|---|---|
| **FP32** skalar | 6141 GFLOPS | **11 329** GFLOPS *(11 385 kalt)* |
| FP16 vec4 | 12 260 | **22 685** |
| int8-Skalarprodukt | 24 550 GIOPS | **45 495** GIOPS |
| FP64 skalar | 385 | ~640 |
| copy d2d (interne Bandbreite) | — | 191 GBPS |

Mit allen 40 CU: **+85 %** bei FP32 gegenüber dem Grundwert (≈**11,3 TFLOPS**). Warm, unter Dauerlast, pendelt es sich bei etwa **10 214 GFLOPS** ein. Im Leerlauf geht der Governor auf 350 MHz, der Rand liegt nach der Last bei rund 54 °C.

## Speicherbandbreite — clpeak

| Größe | Wert |
|---|---|
| Gemessene GDDR6-Bandbreite | **~350–367 GB/s** |
| `mclk` verstellbar | **Nein** (fester Speichertakt) |
| Von Vulkan gesehener Speicher | ~13 GiB (mit erweitertem GTT) |

---

## Profile des Tuners — Takte, Spannungen, Temperaturen

| Profil | CPU | CPU-Spannung | GPU | Höchsttemperatur |
|---|---|---|---|---|
| **Stock** *(Vorgabe des Abbilds)* | 3500 MHz | — | 1500 MHz | die niedrigste |
| **Performance** | 3700 MHz | ~1106 mV (`scale −16`) | 2000 MHz | ausgewogen |
| **Turbo** | 3900 MHz | ~1199 mV (`scale −24`) | 2230 MHz | < 85 °C (Grenze) |
| **Crazy** | 4,0 GHz | ~1224 mV (`scale −36`) | 2230 MHz | ~83 °C in 120 s Last |

- **Harte Höchstgrenze Vid: 1,325 V** (nie überschritten).
- Wärmegrenze 85 °C in allen Profilen; Lüfter auf automatisch; im Leerlauf liegt die GPU bei **350 MHz / 700 mV**.

## Das Freischalten der 8 Kerne — echte +20 %

Die BC-250 kommt mit **zwei per Software abgeschalteten Kernen**: die Kern-Freigabemaske der SMU zeigt 3 von 4 je CCX. SkillFishOS schreibt sie neu und bringt die CPU auf **8 Kerne / 16 Threads**, ganz ohne verändertes BIOS.

Im selben Startvorgang gemessen, mit Aus- und Einschalten der beiden zusätzlichen Kerne im Betrieb:

| Last | 6K/12T | 8K/16T | |
|---|---|---|---|
| Packen mit `xz -T` | 6,41 s | **5,11 s** | **+20 %** |
| Sprachmodell auf der CPU | 34,0 Zeichen/s | **40,8 Zeichen/s** | **+20 %** |
| Temperatur | 66 °C | 68 °C | +2 °C |

Es sind +20 % statt der theoretischen +33 %: Speicherbandbreite und der Aufwand für die Threads fressen den Rest. Trotzdem **ein Fünftel mehr Leistung geschenkt**.

### Übertaktung mit allen 8 Kernen

Stufe für Stufe nachgemessen, jede Stufe **stabil, 0 Maschinenfehler**:

| Ziel | Unter Last erreicht | Punkte | Temperatur | Lüfter |
|---|---|---|---|---|
| 3500 (Vergleich) | 3475 | 5118 Ereignisse/s | 57 °C | — |
| 3700 | 3673 | 5410 | 62 °C | 50 % |
| 3900 | 3872 | 5704 | 71 °C | 68 % |
| **4000** | **3971** | **5849** | **81 °C** | **93 %** |

**Stabiles Maximum: 4000 MHz**, +14 % bei den Punkten gegenüber 3500 — und erst erreichbar, nachdem die Lüftersteuerung in Ordnung gebracht war. **Achtung:** bei **gemeinsamer Last auf CPU und GPU** pendelt sich der Takt bei 3375–3492 MHz und 86 °C ein: jenseits von etwa 3900 begrenzt der Kühlkörper, nicht das Silizium.

---

## Wärmeprüfung (Belastungstest)

Werte, aufgezeichnet während der selbsttätigen Prüfung des Tuners (Prüfen und Zurücknehmen).

| Abschnitt | Takt | Temperatur | Anmerkungen |
|---|---|---|---|
| Leerlauf | CPU ~2,5 GHz · GPU 350 MHz | k10 46 °C · GPU 45 °C | ohne Last |
| **CPU-Last** (12 Threads, 120 s) | CPU **3,68–3,69 GHz** | k10 **85 °C** (an der Grenze) | historische Zahl, **vor** dem Freischalten der 8 Kerne aufgenommen |
| **GPU-Last** (vkpeak in Schleife, 120 s) | GPU **2000 MHz** | Rand bis **86 °C** | bei 86 °C geht der Governor auf 1819–1900 MHz zurück (thermal-guard); die CPU fällt wegen des gemeinsamen Budgets auf ~2,2–2,4 GHz |

---

## Vergleiche

**Dieselbe Hardware, nur ein anderes System** — Superposition 1080p Extreme auf **derselben** BC-250:

| System | Punkte |
|---|---|
| **SkillFishOS** (GPU 2230 · CPU 3900, 40 CU) | **5513** |
| Andere Distribution (Bazzite, werkseitige Takte) | 4102 |

→ **+34 % echte Leistung** aus genau demselben Chip, dank 40 freigeschalteter CU, einem Governor, der auf 2230 MHz geht, und Übertaktung samt Undervolting der CPU.

**Gegen Radeon-Karten für den Schreibtisch** (Superposition 1080p High): die BC-250 mit SkillFishOS (**12 938**) hält mit einer **RX 6600 / 6600 XT** für über 200 € mit und hat die rohe Rechenleistung einer **RX 6700** (~11,3 TFLOPS) — auf einer Platine für etwa 50 €.

---

## Werkzeuge und Vorgehen

| Werkzeug | Was es misst |
|---|---|
| [vkpeak](https://github.com/nihui/vkpeak) | Durchsatz FP32/FP16/int8 über Vulkan |
| [clpeak](https://github.com/krrishnarraj/clpeak) | Speicherbandbreite und OpenCL-Durchsatz |
| [sysbench](https://github.com/akopytov/sysbench) | Last und Messung der CPU (nutzt auch der Tuner) |
| [Unigine Superposition / Heaven](https://benchmark.unigine.com/) | Grafikmessungen unter OpenGL |
| MangoHud im Spiel | Bildrate und Bildzeiten in echten Spielen |
| eigene Messwerterfassung | Takt, Temperatur, Verbrauch und Lüfter über das sysfs von `amdgpu`, `k10temp`, `nct6686` |

## Quellen

- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) · [sysbench](https://github.com/akopytov/sysbench) · [Unigine](https://benchmark.unigine.com/)
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock) — Freischalten der CU
- [bc250.info](https://bc250.info) — sichere Punkte und Wärmehinweise der Gemeinschaft
- [OptiScaler](https://github.com/optiscaler/OptiScaler) — Hochskalieren je Spiel

---
title: Die Hardware der AMD BC-250
description: Die Platine, ihre APU, die technischen Daten und die bekannten Schwächen.
group: Einführung
order: 2
---

Die **AMD BC-250** ist eine kompakte Platine auf Basis einer **teilweise maßgefertigten APU** mit den Kennnamen *Oberon* für die CPU und *Cyan Skillfish* für die Grafik — dieselbe Siliziumfamilie wie die Konsolen der aktuellen AMD-Generation. Gebaut wurde sie für Mining-Anlagen (meist mehrere Platinen je Gehäuse), heute taucht sie zu niedrigen Preisen auf dem Gebrauchtmarkt auf.

## Wichtigste technische Daten

| Baustein | Einzelheit |
|---|---|
| **CPU** | 8 Kerne / 16 Threads **Zen 2** (die Platine zeigt 6; SkillFishOS schaltet die anderen beiden über die SMU frei) („Oberon“), bis **3,9 GHz** (Turbo), 4,0 GHz bestätigt |
| **GPU** | **RDNA 2** „Cyan Skillfish“ (`gfx1013`), bis zu **40 Recheneinheiten** freischaltbar |
| **Speicher** | **16 GB GDDR6**, gemeinsam genutzt (UMA) von CPU und GPU |
| **Rechenleistung** | ~**11,3 TFLOPS** FP32 bei 40 CU / 2000 MHz (mit vkpeak gemessen) |
| **Speicherbandbreite** | ~350–367 GB/s (mit clpeak gemessen) |
| **Bildausgang** | 1× DisplayPort |

Der Speicher ist **einheitlich**: der GDDR6 wird zwischen System und Grafik geteilt. Voreingestellt sind etwa 8 GB als Grafikspeicher, unter Linux lässt sich der Videobereich aber über die **GTT** (Graphics Translation Table) erweitern, sodass Vulkan rund 13 GiB sieht — besonders nützlich für KI-Modelle.

## Freischalten der 8 CPU-Kerne

Die Platine gibt sich als **6 Kerne / 12 Threads** aus, physisch sind es aber **acht**: die beiden fehlenden sind nicht defekt, sie sind durch die Produktkonfiguration abgeschaltet. Verraten wird das durch die Maske der vorhandenen Kerne — auf praktisch jeder Platine steht dort `0x77`, ein **symmetrischer** Wert: vier Kerne je Komplex, in beiden ist der vierte deaktiviert. Eine echte Aussortierung in der Fertigung hinterließe ein unsymmetrisches Muster, denn Defekte verteilen sich nicht so ordentlich.

SkillFishOS schreibt diese Maske beim Start über die **SMU** neu, und die Platine kommt als **8 Kerne / 16 Threads** zurück. Kein verändertes BIOS, kein Lötkolben.

Zwei Sicherungen stecken im Dienst: ist die Maske **nicht** `0x77`, wird nichts angefasst, denn ein anderes Muster kann bedeuten, dass die Kerne wirklich ab Werk abgeschaltet wurden; und der warme Neustart erfolgt **erst dann**, wenn der Schreibvorgang zurückgelesen und bestätigt wurde — eine Neustartschleife ist damit ausgeschlossen.

> Auf unserer eigenen Platine gemessen: **+20%** bei mehrfädiger Arbeit. Bei Lasten mit wenigen Threads ändert sich nichts, wie zu erwarten war — zwei zusätzliche Kerne lassen einen einzelnen Thread nicht schneller laufen.

Die Rückentwicklung stammt von [bc250-core-unlock (rw-r-r-0644)](https://github.com/rw-r-r-0644/bc250-core-unlock): ohne diese Arbeit gäbe es die Funktion nicht.

## Freischalten der 40 CU

Die GPU hat 40 CU, der Treiber aktiviert aber standardmäßig nur **24**. SkillFishOS **hebt sie im laufenden Betrieb auf 40** (ohne Neustart): der Start erfolgt mit dem Treiber-Grundwert, ein Dienst bringt sie beim Hochfahren auf 40, einstellbar im [Tuner](/de/docs/app-native). Die Rückentwicklung der Freischaltung ist in [bc250-40cu-unlock](https://github.com/duggasco/bc250-40cu-unlock) dokumentiert; die Steuerung im Betrieb über `umr` ist von [bc250-cu-live-manager](https://github.com/WinnieLV/bc250-cu-live-manager) angeregt (von Grund auf neu geschrieben).

> Mit 40 aktiven CU misst SkillFishOS aus dem kalten Zustand **11385 GFLOPS** FP32 (vkpeak) gegenüber rund 6141 bei einer Grundeinstellung mit 24 CU: etwa **+85%**.

## Schwächen der Hardware, die man kennen sollte

Die BC-250 ist wiederverwendete „Mining“-Hardware: sie hat Grenzen, die SkillFishOS mit Software umgeht. Wer sie kennt, versteht viele Entscheidungen des Systems.

### Defekte Hot-Plug-Erkennung (HPD) am DisplayPort

Die Erkennung des angeschlossenen Bildschirms am DisplayPort **funktioniert nicht**: die Platine „sieht“ nicht, dass ein Bildschirm angesteckt wurde. SkillFishOS löst das mit einem eigenen Dienst (`skillfish-dp-hotswap`), der die Erkennung beim Start erzwingt und im Betrieb auf Bildschirmwechsel achtet, dazu der Kernel-Parameter `video=DP-1:e` als Rückfall. Siehe [Schreibtisch](/de/docs/desktop) und [Fehlersuche](/de/docs/risoluzione-problemi).

### Kaputter ACPI-Ruhezustand

Der Ruhezustand (**s2idle ist kaputt**): die Platine schläft ein, **wacht aber nicht auf** und braucht einen harten Neustart. Zudem ist eine schlafende Maschine aus der Ferne nicht erreichbar. Deshalb schaltet SkillFishOS alle Schlafzustände **dauerhaft ab** (siehe [Schreibtisch](/de/docs/desktop)). Das ist eine zwingende Maßnahme.

### IOMMU unbrauchbar

Die IOMMU der BC-250 ist unruhig: sie **darf niemals eingeschaltet werden**. Das System startet immer ohne IOMMU.

### Temperaturfühler

Verfügbar ist nur der Fühler für die *Randtemperatur* der GPU; **einen Fühler für die Temperatur des Grafikspeichers gibt es nicht**. Die mitgelieferte Kühlung ist knapp, deshalb sind unmittelbar hintereinander gefahrene Messungen nicht vergleichbar (Wärmestau): lass die Platine zwischen den Durchläufen ein paar Minuten abkühlen.

## Kühlung, druckbare Gehäuse und Lüfter

Die BC-250 kommt **nackt** an, gedacht für Mining-Regale mit fünf 80-mm-„Schreihälsen“, die vom Verteilerstecker gespeist werden. Für den Schreibtisch braucht es eine eigene Kühlung. Gekühlt werden müssen **zwei Dinge**: der Kühlkörper der APU **und** die **GDDR6**-Bausteine, die sehr heiß werden und keinen Temperaturfühler haben (siehe [GPU und Übertaktung](/de/docs/gpu-overclock)).

**Was funktioniert (Rat aus der Gemeinschaft):**

- **2× 120-mm-Lüfter** mit hohem Staudruck auf den Kühlkörper gerichtet sind der häufigste Aufbau auf dem Schreibtisch; ohne Gehäuse kann man sie direkt oben auflegen (mit Kabelbindern durch die Lamellen).
- Ein **eigener Lüfter für den Grafikspeicher** ist beim Übertakten sehr zu empfehlen: die GDDR6-Bausteine sind die heißeste Stelle.
- Der Lüfter wird an den **4-poligen PWM-Anschluss** der Platine gesteckt — SkillFishOS steuert ihn über `nct6686` (Sensoren) und lässt ihn auf **automatisch**.

**Gehäuse und Luftführungen (kostenlose STL, im 3D-Druck):**

| Modell | Urheber | Anmerkungen |
|---|---|---|
| [Console Style Case](https://www.thingiverse.com/thing:7172528) | Arthrimus | „Konsolen“-Gehäuse mit Platz fürs Netzteil, Führung für **1× 120 mm** |
| [ASRock BC-250 Shell Case](https://www.printables.com/model/1228207-asrock-amd-bc-250-shell-case) | onemorecap | Aufsteckschale, schnelle Halterung für einen Lüfter |
| [Yet Another BC-250 Fan Shroud](https://www.printables.com/model/1339540-yet-another-bc-250-fan-shroud) | ViRazY | **140 mm** Zuluft und **120 mm** Abluft |
| [Case ATX PSU & Fan Duct](https://www.printables.com/model/1616167-amd-bc-250-case-atx-psu-fan-duct) | ZMASLO | Für ein gewöhnliches ATX-Netzteil, Luftführung, die den Kühler nicht beschädigt |
| [Standard ATX PSU case](https://www.thingiverse.com/thing:7269520) | CatSiewDai | Vollständiges Gehäuse für ATX-Netzteile |
| [OC vRAM Fan Kit (remix)](https://www.thingiverse.com/thing:7271946) | marccyberwiz | Lüftersatz **eigens für den Grafikspeicher** beim Übertakten |
| [NexGen3D — DIY Steam Machine (Bazzite)](https://www.printables.com/model/1499974-nexgen3d-diy-steam-machine-powered-by-bazzite) | NexGen3D | Vollständiges Gehäuse im **Steam-Machine**-Stil für die BC-250 |
| [NexGen3D — Steam Machine PRO (wassergekühlt)](https://www.printables.com/model/1614131-nexgen3d-diy-steam-machine-pro-liquid-cooled-bc-25/files) | NexGen3D | **PRO-Fassung mit Wasserkühlung** (AIO) — größtmögliche Kühlung |
| [NexGen3D — AIO-Halterung für die BC-250](https://www.printables.com/model/1554003-nexgen3d-aio-mount-for-the-bc-250) | NexGen3D | Halterung, um eine **AIO** (Wasserkühlung) auf der BC-250 zu befestigen |

> Nachschlagewerk zur Kühlung: [Cooling Solutions — amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs/hardware/cooling/).

## Quellen

- [bc250.info](https://bc250.info) — Wiki der Gemeinschaft
- [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs) — technische Dokumentation (samt [Kühlung](https://elektricm.github.io/amd-bc250-docs/hardware/cooling/))
- [mothenjoyer69/bc250-documentation](https://github.com/mothenjoyer69/bc250-documentation) — Notizen zu Hardware und Kühlung
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock) — Freischaltung der Recheneinheiten
- [bc250_memcfg (fanoush)](https://github.com/fanoush/bc250_memcfg) — Speicherkonfiguration
- Linux-Kerneltreiber `amdgpu` — [docs.kernel.org/gpu/amdgpu](https://docs.kernel.org/gpu/amdgpu/)

---
title: Glossar
description: Die Fachbegriffe rund um SkillFishOS und die BC-250, kurz erklärt.
group: Nachschlagen
order: 5
---

Die Begriffe, die sich durch die ganze Dokumentation ziehen, jeder in einer Zeile erklärt. In alphabetischer Folge.

## Hardware und APU

**APU** — *Accelerated Processing Unit*: ein Chip, der CPU und GPU auf demselben Plättchen vereint. Die BC-250 trägt eine teilweise maßgefertigte von AMD.

**BC-250** — die Platine, auf der SkillFishOS läuft: APU Zen 2 + RDNA 2, 16 GB GDDR6, ursprünglich fürs Mining gebaut.

**Cyan Skillfish** — der Kennname des **Grafikteils** (GPU) der APU der BC-250. Daher der Name „SkillFish“.

**Oberon** — der Kennname des **CPU-Teils** (Zen 2) derselben APU.

**Recheneinheit (CU)** — die Rechenblöcke der GPU. Die BC-250 hat 40, zeigt aber ab Werk weniger: SkillFishOS **schaltet alle frei** (siehe [Kernel](/de/docs/kernel)).

**gfx1013** — die Kennung der Grafikarchitektur der BC-250 (Familie RDNA 2). Sie ist wichtig, weil **ROCm sie nicht unterstützt** → stattdessen kommt Vulkan zum Einsatz.

**RDNA 2** — die Grafikarchitektur von AMD in dieser GPU (dieselbe Familie wie die aktuellen Konsolen).

**Zen 2** — die CPU-Architektur von AMD in dieser APU (**8 Kerne / 16 Threads**: die Platine zeigt 6, SkillFishOS schaltet die anderen beiden über die SMU frei).

**GDDR6** — der Speichertyp der Platine: schnell und hier von CPU und GPU **gemeinsam genutzt**.

**UMA** — *Unified Memory Architecture*: CPU und GPU benutzen **denselben** Speichervorrat (die rund 16 GB GDDR6).

**GTT** — *Graphics Translation Table*: der Mechanismus, mit dem die GPU über den eigenen Grafikspeicher hinaus Systemspeicher nutzen kann. SkillFishOS erweitert ihn, sodass Vulkan rund 13 GiB sieht (nützlich für die KI).

## Takte, Spannungen, Wärme

**SMU** — *System Management Unit*: der Mikrocontroller in der APU, der Takte und Spannungen regelt. Auf der BC-250 läuft die Steuerung **nur** über ihn, nicht über die gewöhnlichen amdgpu-Dateien in sysfs.

**SMU-Governor** — der Dienst (`cyan-skillfish-governor`), der die *sicheren Punkte* aus Takt und Spannung für die GPU festlegt.

**sclk / mclk** — Takt des **Grafikkerns** (sclk) und des **Speichers** (mclk). Auf der BC-250 lässt sich der mclk **nicht** verstellen.

**Undervolting** — die Spannung bei gleichem Takt senken: dieselbe Arbeit, **weniger Wärme und weniger Verbrauch**. Siehe [GPU und Übertaktung](/de/docs/gpu-overclock).

**Übertaktung (OC)** — die Takte über die Werkseinstellung heben, um mehr Leistung zu bekommen.

**Vid** — die Spannung, die der Chip bei einem bestimmten Takt anfordert. Auf der BC-250 liegt die harte Grenze bei **1,325 V**.

**Temperaturschutz** — der Wächter des Systems, der die Takte senkt, sobald 85 °C überschritten werden.

**Wärmestau (heat-soak)** — die angesammelte Wärme, die unmittelbar hintereinander gefahrene Messungen verfälscht: lass die Platine zwischen den Durchläufen abkühlen.

**Silizium-Lotterie** — die Tatsache, dass jeder Chip eine andere Übertaktung und ein anderes Undervolting verträgt; deshalb prüft SkillFishOS die Profile **auf deiner** Platine.

## Systemsoftware

**Debian sid** — der Zweig *unstable* von Debian, immer aktuell, aber anfällig für Rückschritte: die Grundlage von SkillFishOS (siehe [Aktualisierungen](/de/docs/aggiornamenti)).

**KDE Plasma 6** — die verwendete Arbeitsumgebung, in Steampunk-Gestaltung gekleidet.

**linux-tkg** — das Baurezept für den Kernel (Frogging-Family), auf dem der maßgeschneiderte Kernel von SkillFishOS beruht.

**Mesa / RADV** — die quelloffenen Grafiktreiber; **RADV** ist der **Vulkan**-Treiber, den die GPU der BC-250 benutzt.

**ROCm** — der „offizielle“ Rechenunterbau von AMD: er unterstützt gfx1013 **nicht** und wird daher nicht verwendet.

**Vulkan** — die Schnittstelle für Grafik und Rechenarbeit, die auf der BC-250 sowohl zum Spielen als auch für die **KI** (Unsloth Studio) dient.

**Btrfs** — das Copy-on-Write-Dateisystem mit Schnappschüssen, das das „Sicherheitsnetz“ liefert (siehe [Speicher und Schnappschüsse](/de/docs/storage-snapshot)).

**Snapper** — das Werkzeug, das vor und nach Aktualisierungen automatisch Btrfs-Schnappschüsse anlegt.

**grub-btrfs** — lässt die Schnappschüsse im GRUB-Menü erscheinen, um schon beim Start zurückzukehren.

**APT-Pinning** — ein Paket auf einer geprüften Fassung festhalten, für die Bestandteile, die auf dieser Hardware heikel sind.

**reprepro** — das Werkzeug, mit dem die signierte APT-Paketquelle von SkillFishOS verwaltet wird.

**HPD** — *Hot-Plug Detect*: die Erkennung des angeschlossenen Bildschirms. Auf der BC-250 ist sie **defekt** → daher der Dienst `skillfish-dp-hotswap`.

**s2idle / Ruhezustand** — die Schlafzustände von ACPI: auf der BC-250 **kaputt** und deshalb abgeschaltet.

**IOMMU** — die Speicherverwaltungseinheit für die Virtualisierung von Ein- und Ausgabe: auf der BC-250 unruhig, wird **nie** eingeschaltet.

## Spiele und KI

**Proton** — die Kompatibilitätsschicht von Valve, die Windows-Spiele über Steam unter Linux laufen lässt.

**gamescope** — der Mikro-Compositor von Valve fürs Spielen („Konsolen“-Sitzung, Hochskalieren mit FSR1/NIS).

**EmuDeck / ES-DE** — der Einrichter für Emulatoren und die Oberfläche für die Emulation.

**FSR / OptiScaler** — Verfahren zum **Hochskalieren**. FSR 4 gibt es hier nicht (es verlangt RDNA 4); verwendet werden FSR1/NIS oder OptiScaler.

**Unsloth Studio** — Motor und Oberfläche der lokalen KI: führt GGUF-Modelle auf der GPU aus und bietet eine zu OpenAI kompatible Schnittstelle.

**qwen3:14b** — das Referenzmodell der KI, das vollständig auf der GPU läuft.

**Tuner** — die eigene Anwendung von SkillFishOS, um die Hardware mit Prüfen und Zurücknehmen einzustellen (siehe [Eigene Anwendungen](/de/docs/app-native)).

## Quellen

- [bc250.info](https://bc250.info) · [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- [amdgpu-Dokumentation](https://docs.kernel.org/gpu/amdgpu/) · [Mesa / RADV](https://docs.mesa3d.org/drivers/radv.html)

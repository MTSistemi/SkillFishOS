---
title: Einführung
description: Was SkillFishOS ist, warum es existiert und für wen es gedacht ist.
group: Einführung
order: 1
---

**SkillFishOS** ist eine Linux-Distribution, die für eine bestimmte, ungewöhnliche Platine entworfen und abgestimmt wurde: die **AMD BC-250**. Es ist ein sofort nutzbares *Konsolen-PC*-System — Spiele, Emulation, KI auf dem Gerät selbst und ganz normale Schreibtischarbeit —, aufgebaut auf [Debian](https://www.debian.org/) und [KDE Plasma 6](https://kde.org/plasma-desktop/), mit einem durchgehenden Steampunk-Erscheinungsbild vom Start bis zum Schreibtisch.

## Der Gedanke dahinter

Die BC-250 kam als Platine zum Schürfen von Kryptowährungen auf die Welt und landete zu sehr niedrigen Preisen auf dem Gebrauchtmarkt. Unter dem Kühlkörper sitzt allerdings eine **teilweise maßgefertigte AMD-APU** aus derselben Siliziumfamilie wie die Konsolen der aktuellen Generation: eine Zen-2-CPU, RDNA-2-Grafik und 16 GB GDDR6. Mit der richtigen Software wird daraus ein erstaunlich leistungsfähiger kleiner Konsolen-PC.

Das Problem: Sie unter Linux gut zum Laufen zu bringen, verlangt Kernel-Patches, einen eigenen Frequenz-Governor, Übertaktung, Temperaturprofile und eine lange Liste von Umwegen um Hardware-Macken herum. SkillFishOS gibt es, um **diese ganze Arbeit einmal zu erledigen** und ein System auszuliefern, das *„eingeschaltet wird und sein Bestes gibt“*, ohne dass jemand ein Terminal öffnen muss.

> SkillFishOS verteilt keine Spiele und keine ROMs: es liefert die **Werkzeuge** (Steam, EmuDeck, Emulatoren, Oberflächen). Die Inhalte bringst du selbst mit, auf legalem Weg.

## Für wen es gedacht ist

Das Projekt entstand aus einem ganz konkreten, persönlichen Bedürfnis: **Kinder Linux benutzen und lernen zu lassen, während sie spielen**. Die Spiele sind die Karotte, die sie anlockt, und die **automatischen Schnappschüsse** von Btrfs sind das Sicherheitsnetz, das Herumprobieren erlaubt, ohne Angst zu haben, das System zu zerlegen — geht etwas schief, bist du mit einem Klick aus dem Startmenü wieder zurück.

SkillFishOS passt also gut zu:

- allen, die eine **BC-250** besitzen und spielen wollen, ohne Kernel-Fachleute zu werden;
- **Familien**, die eine günstige Konsole suchen, die zugleich ein Lern-PC ist;
- **Bastlern**, die lieber auf einer schon abgestimmten Grundlage aufbauen, statt alles von vorn zu bauen.

## Was drinsteckt, in Kürze

- Ein **maßgeschneiderter Kernel** ([linux-tkg](https://github.com/Frogging-Family/linux-tkg)) mit den BC-250-Patches: 40 freigeschaltete Recheneinheiten, entsperrte Taktraten, ein eigener SMU-Governor.
- Ein **KDE-Plasma-6-Schreibtisch** in Steampunk-Gestaltung (Symbole, Zeiger, Hintergrundbild, System-HUD).
- **Bereit zum Spielen**: Steam, [gamescope](https://github.com/ValveSoftware/gamescope), [EmuDeck](https://www.emudeck.com/), [ES-DE](https://es-de.org/), [Heroic](https://heroicgameslauncher.com/), Proton.
- **KI auf dem Gerät**: [Unsloth Studio](https://unsloth.ai/), mit Vulkan auf der eingebauten GPU beschleunigt — gemessen **5,1×** schneller als auf der CPU.
- **Btrfs-Schnappschüsse** mit [Snapper](http://snapper.io/) und Rückkehr aus dem GRUB-Menü.
- **Eigene Anwendungen**: der *Tuner* (Hardware-Steuerung ohne Terminal) und das *KI*-Fenster.
- **Eigene, geprüfte Aktualisierungen** aus unserer APT-Paketquelle, damit Debian-Aktualisierungen dich nicht überraschen.

Die folgenden Seiten gehen auf jeden Baustein im Einzelnen ein.

## Quellen

- Dokumentation der BC-250-Gemeinschaft — [bc250.info](https://bc250.info)
- AMD-BC-250-Dokumentation (elektricm) — [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- Debian — [debian.org](https://www.debian.org/)
- KDE Plasma — [kde.org/plasma-desktop](https://kde.org/plasma-desktop/)

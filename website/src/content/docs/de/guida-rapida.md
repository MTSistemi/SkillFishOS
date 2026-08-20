---
title: Schnellstart
description: Deine ersten 10 Minuten mit SkillFishOS — vom ersten Start bis zum ersten Spiel.
group: Einführung
order: 3
---

Du hast SkillFishOS installiert (siehe [Installation](/de/docs/installazione)) und stehst vor dem ersten Start. Diese Seite ist eine **kurze Liste**, um sofort loszulegen: alles andere ist schon eingerichtet und läuft.

## In einer Zeile

> Einschalten → du bist schon auf dem abgestimmten Schreibtisch → Controller verbinden → eigene Spiele hinzufügen → spielen. Kein Terminal, keine Einrichtung.

## 1. Erster Start (es ist alles fertig)

Beim ersten Start bekommst du einen **KDE-Plasma-6**-Schreibtisch in Steampunk-Gestaltung, einen optimierten Kernel, den SMU-Governor, das Profil **Stock**, die Spiele-Ausstattung und Schnappschüsse — **alles bereits aktiv**. Oben rechts zeigt das **HUD** in Echtzeit CPU, GPU, Temperaturen, Arbeitsspeicher, Lüfter und verbundene Bluetooth-Geräte.

Du musst keine Treiber installieren, keine Taktraten setzen und nichts einschalten: das System startet „mit größtmöglicher Verträglichkeit“.

## 2. Mit dem Netzwerk verbinden

Das Kabelnetz übernimmt der NetworkManager, und es ist sofort bereit. Für WLAN und Bluetooth nimm das Netzwerksymbol in der Leiste. Eine Verbindung wird für Steam, Aktualisierungen und die lokale KI gebraucht.

## 3. Einen Controller verbinden

| Controller | Wie |
|---|---|
| **DualShock 4** | Über Bluetooth: **Share + PS** gedrückt halten, bis er blinkt, dann über das Bluetooth-Symbol koppeln. Er hat einen **Lagesensor**. |
| **Beliebiger Controller** | Über **USB** mit einem **Datenkabel** (nicht nur zum Laden): wird als Xbox-360-Controller erkannt. |

Einzelheiten und Fehlersuche → [Spiele](/de/docs/gaming) und [Fehlersuche](/de/docs/risoluzione-problemi).

## 4. Eigene Spiele hinzufügen

- **Steam** ist bereits installiert und mit gamescope und MangoHud verbunden. Melde dich an und installiere deine Spiele: Windows-Titel laufen über **Proton**.
- **Epic / GOG** → [Heroic](/de/docs/gaming).
- **Emulation** → starte **EmuDeck**, wähle deine Emulatoren und spiele dann über die Oberfläche **ES-DE**. ROMs, BIOS-Dateien und Schlüssel bringst du selbst mit (siehe den rechtlichen Hinweis unter [Spiele](/de/docs/gaming)).

## 5. (Freiwillig) Die Hardware ausreizen

SkillFishOS startet im Profil **Stock**, um auf jeder Platine sicher zu sein. Wenn du mehr Leistung willst, öffne den **[Tuner](/de/docs/app-native)** und geh ein Profil höher:

**Stock → Performance → Turbo → Crazy**

Der Tuner **prüft jedes Profil auf deiner eigenen BC-250** und **nimmt es von selbst zurück**, wenn die Platine es nicht mitmacht. Das ist der sichere Weg, die Grenze deines Chips zu finden (siehe [GPU und Übertaktung](/de/docs/gpu-overclock)).

## 6. (Freiwillig) Die lokale KI einschalten

Wenn du einen Assistenten brauchst, der ohne Internet läuft, öffne das **KI-Fenster** und starte [Unsloth Studio](/de/docs/ai-locale). Denk daran: KI und anspruchsvolle Spiele vertragen sich **nicht** gleichzeitig (dieselbe GPU, derselbe Speicher). Ist die KI aus, gehört die GPU wieder ganz den Spielen.

## Was du gleich wissen solltest

- **Schalte den Ruhezustand nicht wieder ein**: auf der BC-250 ist er kaputt, und die Platine wacht nicht mehr auf (siehe [Schreibtisch](/de/docs/desktop)).
- Nimm einen Bildschirm mit **DisplayPort** oder einen **passiven** Adapter; **aktive** DP→HDMI-Adapter zerstören den Ton.
- Du hast ein **Sicherheitsnetz**: vor und nach jeder Aktualisierung wird ein Btrfs-Schnappschuss angelegt; geht etwas schief, kehre über das GRUB-Menü zurück → *SkillFishOS snapshots* (siehe [Speicher und Schnappschüsse](/de/docs/storage-snapshot)).

## Wie geht es weiter?

- Du willst verstehen, **was** du da benutzt? → [BC-250-Hardware](/de/docs/hardware-bc250)
- Du willst die echten **Zahlen** zur Leistung? → [Leistung und Messungen](/de/docs/prestazioni)
- Du hast eine kurze **Frage**? → [Häufige Fragen](/de/docs/faq)
- Ein **Begriff**, den du nicht kennst? → [Glossar](/de/docs/glossario)

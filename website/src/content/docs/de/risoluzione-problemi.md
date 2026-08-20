---
title: Fehlersuche
description: Die häufigsten Schwierigkeiten mit der BC-250 und wie SkillFishOS sie umgeht.
group: Nachschlagen
order: 1
---

Viele „Probleme“ der BC-250 sind in Wahrheit bekannte Hardware-Macken, die SkillFishOS von selbst umgeht. Hier die häufigsten.

## Der Bildschirm bleibt schwarz / der Monitor wird nicht erkannt

Beim DisplayPort ist die **Hot-Plug-Erkennung (HPD) defekt**: die Platine merkt nicht, dass ein Bildschirm angeschlossen wurde. SkillFishOS löst das mit dem Dienst `skillfish-dp-hotswap` (er erzwingt die Erkennung beim Start und beim Wechsel des Bildschirms) und mit dem Kernel-Parameter `video=DP-1:e`.

Was zu prüfen ist:

- nimm einen **DisplayPort-Bildschirm** oder einen **passiven** DP→HDMI-Adapter;
- meide **aktive** DP→HDMI-Adapter: neben Erkennungsproblemen **zerstören sie den Ton** (siehe unten);
- wenn der Bildschirm gewechselt wurde, warte ein paar Sekunden: die Erkennung läuft von selbst, aber nicht sofort.

## Die Platine wacht aus dem Ruhezustand nicht auf

Der Ruhezustand ist **auf Hardware-Ebene kaputt**. Genau deshalb schaltet SkillFishOS ihn vollständig ab (siehe [Schreibtisch](/de/docs/desktop)). Wirkt die Platine nach einer Pause „tot“ und wurde an der Energieverwaltung gedreht, hilft nur noch ein **harter Neustart**. Schalte die Schlafzustände nicht wieder ein.

## Kein Ton über Bildschirm oder Fernseher

Ton über DisplayPort funktioniert, aber:

- **aktive DP→HDMI-Adapter** zerstören den Ton: nimm passive Adapter, einen echten DP-Bildschirm, eine **USB-Soundkarte** oder Ton über **Bluetooth**;
- um den Ton kümmert sich **PipeWire**: das Standardausgabegerät wird in den Toneinstellungen von KDE gewählt.

## Die Controller funktionieren nicht

- **DualShock-4**-Controller laufen über **Bluetooth** (mit Lagesensor). Zum Koppeln: *Share + PS* gedrückt halten, bis sie blinken, dann im Bluetooth-Fenster koppeln.
- Ein Controller **über USB** braucht ein **Datenkabel** (nicht nur ein Ladekabel): er wird als Xbox 360 erkannt.
- Nachbau-Controller vertragen sich manchmal schlecht mit den DS4 am selben Bluetooth-Adapter: dann nimm sie **über USB**.

## Die GPU wirkt langsam / die Temperaturen sind hoch

- Prüfe im [Tuner](/de/docs/app-native), ob die **40 CU** und der SMU-Governor aktiv sind.
- Denk daran, dass die Kühlung knapp ist: nach längerer Last greift der **Temperaturschutz** (85 °C). Für aussagekräftige Messungen lass die Platine zwischen den Durchläufen abkühlen (siehe [GPU](/de/docs/gpu-overclock)).
- Bei Spielen, die an der **CPU** hängen, bringt eine niedrigere Auflösung keine zusätzlichen Bilder.

## Die Platine ist komplett eingefroren

Die BC-250 kann **komplett einfrieren**, oft im Zusammenhang mit **zu beherztem Undervolting**: die Unruhe zeigt sich vor allem bei **geringer Last**, ein Einfrieren kann also sogar im Leerlauf zuschlagen. SkillFishOS geht das von zwei Seiten an:

- **Hardware-Wachhund** — der **SP5100-TCO**-Zeitgeber des Chipsatzes ist aktiv (`RuntimeWatchdogSec=2min`): steht das System vollständig, **startet sich die Platine innerhalb von zwei Minuten selbst neu**, ohne den Stecker zu ziehen.
- **Einfrier-Melder** — beim Start merkt ein Dienst, ob das vorherige Herunterfahren unsauber war (die Markierung für sauberes Beenden fehlt), und **schreibt** das nach `/var/log/skillfish-freeze.log`, mit einer Meldung auf dem Schreibtisch. Der Zähler steht auch im Fenster **„Mein Silizium“** des Tuners.

Häufen sich die Aussetzer, geh im Tuner **ein Profil zurück** (etwa von Crazy oder Turbo auf Performance): der weniger beherzte Wert ist fast immer die Lösung. Alle Profile sind **absturzsicher** — ein Einfrieren mitten in einer Prüfung lässt die Platine beim Neustart nie auf einem unruhigen Profil stehen. Bleiben die Aussetzer selbst bei Stock, verdächtige das **Netzteil**.

## Eine Aktualisierung hat etwas kaputt gemacht

Starte neu und wähle im Menü **GRUB → „SkillFishOS snapshots“** einen früheren Schnappschuss, der lief. Siehe [Speicher und Schnappschüsse](/de/docs/storage-snapshot). Die Schnappschüsse vor und nach einer Aktualisierung entstehen von selbst.

## Die KI startet nicht oder liefert Unsinn

- Die KI läuft über Vulkan (nicht ROCm) und **sollte nicht zusammen mit Spielen** benutzt werden (dieselbe GPU, derselbe Speicher).
- Kommt verstümmelter Text heraus, achte darauf, den KV-Zwischenspeicher in **f16** zu benutzen (`q4_0` verstümmelt die Ausgabe auf RADV). Siehe [KI auf dem Gerät](/de/docs/ai-locale).

## Quellen

- [bc250.info](https://bc250.info) · [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- [Arch Wiki — Gamepad](https://wiki.archlinux.org/title/Gamepad)
- [PipeWire — Fehlersuche](https://docs.pipewire.org/)

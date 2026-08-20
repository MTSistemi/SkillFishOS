---
title: Speicher und Btrfs-Schnappschüsse
description: "Das Sicherheitsnetz von SkillFishOS: automatische Schnappschüsse und Rückkehr direkt beim Start."
group: System
order: 3
---

Einer der Grundgedanken von SkillFishOS ist, **ohne Angst herumprobieren** zu können. Möglich macht das das Dateisystem **[Btrfs](https://btrfs.readthedocs.io/)** mit automatischen Schnappschüssen: jede wichtige Änderung wird festgehalten, und geht etwas kaputt, bist du mit einem Klick zurück.

## Getrennte Unterbände

Die Platte hat eine einzige Btrfs-Partition, aufgeteilt in getrennte Unterbände:

- **`@`** — das Betriebssystem;
- **`@home`** — die Daten der Benutzer;
- **`@cache`** und **`@log`** — Zwischenspeicher und Protokolle, aus den Schnappschüssen herausgehalten, damit eine Rückkehr nicht die Protokolle von gestern mitschleppt;
- **`@games`** — die Spielesammlung, die sonst jeden Schnappschuss riesig machen würde;
- **`@swap`** — die Auslagerungsdatei.

Sie getrennt zu halten ist entscheidend: das System zurückzurollen **rührt die persönlichen Dateien nicht an**. Du kannst zu einem System von „gestern“ zurückkehren und die Dokumente, Spielstände und Einstellungen von heute behalten.

## Automatische Schnappschüsse mit Snapper

SkillFishOS benutzt **[Snapper](http://snapper.io/)** mit einer `root`-Konfiguration und **Vorher-/Nachher-Haken an APT**: jedes Mal, wenn du Pakete installierst oder aktualisierst, entsteht von selbst ein Schnappschuss *davor* und *danach*. Macht eine Aktualisierung also Ärger, ist der Schnappschuss von vorher schon da.

Aus der Konfiguration hervorzuheben:

- eine Obergrenze für die Zahl der aufbewahrten Schnappschüsse, damit die Platte nicht volläuft;
- Schnappschüsse an wichtigen *Wegmarken* des Systems;
- Verwaltung auch über das grafische Werkzeug **Btrfs Assistant**.

## Wie viele aufbewahrt werden

**Fünf**, in der Voreinstellung: drei gewöhnliche (das Paar vor und nach jeder `apt`-Aktion) und zwei „wichtige“ — jene Aktualisierungen, die den Kernel oder systemd betreffen, also genau die, die man am ehesten zurückhaben möchte. Darüber steht der Punkt *„SkillFishOS - clean install“*, der nie verfällt: der Weg zurück zum System, wie es aus der Schachtel kam.

Die stündliche Zeitleiste ist **aus**. Auf einer Konsole zu Hause frisst sie nur Platz, ohne dass jemals jemand in diese Schnappschüsse schaut. Von **Hand** angelegte Schnappschüsse zählen nicht zu den fünf und werden nie von selbst gelöscht: hast du einen mit Absicht gemacht, bleibt er, bis du ihn entfernst.

## Rückkehr aus dem Startmenü

Dank **[grub-btrfs](https://github.com/Antynea/grub-btrfs)** erscheinen die Schnappschüsse direkt im **GRUB**-Menü, unter *„SkillFishOS snapshots“*. Neu starten, den Schnappschuss von vor dem Ärger wählen — und du bist darin.

Zwei Dinge, die man wissen sollte, bevor man sich darauf verlässt:

- **Was du startest, ist nur lesbar.** Es ist eine Rettungsumgebung: sich umsehen, prüfen, ob der ältere Stand wirklich in Ordnung war, die gebrauchten Dateien herausholen. Ein paar Dienste melden beim Start einen Fehler — sie können schlicht nicht schreiben. Das gehört so, es ist kein Defekt.
- **Das Startmenü wird nach jeder `apt`-Aktion aufgefrischt**, der Schnappschuss von *vor* einer Aktualisierung steht also genau dann in der Liste, wenn du ihn brauchst.

## Die Rückkehr dauerhaft machen

Einen Schnappschuss zu starten ändert für sich genommen nichts, und `snapper rollback` hilft hier nicht: es tauscht den voreingestellten Unterband aus, während unser GRUB-Eintrag `subvol=@` festnagelt und gewinnt. Der Befehl, der die Arbeit macht, lautet:

```bash
sudo skillfish-rollback --list    # welche Schnappschüsse es gibt
sudo skillfish-rollback 12        # Schnappschuss 12 wird ab dem nächsten Start das System
```

Er stellt das aktuelle System beiseite — es wird nicht gelöscht, sondern zu `@-rotto-<Datum>` — und baut aus dem gewählten Schnappschuss ein neues, beschreibbares `@`, samt der gesamten Schnappschussgeschichte. Stellt sich heraus, dass auch der ältere Stand nicht die Antwort war, holt `sudo skillfish-rollback --undo` alles zurück, und `--clean` gibt den Platz frei, wenn du sicher bist.

Es funktioniert aus dem normalen System heraus und aus einem nur lesbar gestarteten Schnappschuss — und das ist der Fall, auf den es ankommt, wenn die Maschine gar nicht mehr hochkommt.

> **Dein persönlicher Ordner wird nie angerührt.** `@home` ist ein eigener Unterband: das System reist in der Zeit zurück, deine Dateien bleiben, wie sie sind. Gut zu wissen — und daran zu denken, bevor man auf eine Rückkehr setzt, um ein gelöschtes Dokument zurückzuholen: das tut sie nicht.

> Das ist das Sicherheitsnetz, das auch die Jüngsten das System erkunden lässt, ohne Angst, es unwiederbringlich zu zerlegen.

## Warum Btrfs und nicht Timeshift

SkillFishOS hat sich für **Btrfs + Snapper + grub-btrfs** statt für Lösungen wie Timeshift entschieden, weil:

- die Verzahnung mit APT von selbst geschieht (ein Schnappschuss bei jeder Paketaktion);
- die Schnappschüsse dem Dateisystem eigen sind (sofort da, *copy-on-write*, günstig);
- die Rückkehr **schon beim Start** bereitsteht, selbst wenn das System auf gewöhnlichem Weg nicht mehr hochkommt.

## Quellen

- [Btrfs-Dokumentation](https://btrfs.readthedocs.io/)
- [Snapper](http://snapper.io/)
- [grub-btrfs (Antynea)](https://github.com/Antynea/grub-btrfs)
- [Btrfs Assistant](https://gitlab.com/btrfs-assistant/btrfs-assistant)

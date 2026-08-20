---
title: Fernsteuerung — Remote Manager
description: Die Weboberfläche von SkillFishOS, um die BC-250 vom Browser oder Handy aus zu steuern — Telemetrie, KVM, Terminal, Tuner, Anwendungsverwaltung und KI.
group: Benutzung
order: 4
---

Der **SkillFishOS Remote Manager** ist eine modulare Weboberfläche, mit der sich die BC-250 **von einem anderen Rechner oder vom Handy aus** steuern lässt — im selben Netz oder, über ZeroTier, von überall auf der Welt. Angemeldet wird sich mit den Systemzugangsdaten, alles über HTTPS.

## Installation

```bash
sudo apt update
sudo apt install skillfish-dashboard
```

Das Paket installiert den Dienst, die eigene Anwendung **Remote Manager** (um die Oberfläche ein- und auszuschalten und die Bausteine zu wählen) sowie alle Webseiten. Die freiwilligen Abhängigkeiten (KVM, Terminal, Wake-on-LAN) sind *Recommends* und kommen von selbst mit, wenn sie verfügbar sind.

## Einschalten

Öffne **SkillFishOS Remote Manager** aus dem Anwendungsmenü:

- **Hauptschalter** — startet den Dienst (dauerhaft, über systemd).
- **Kästchen der Bausteine** — wähle, was sichtbar sein soll (Telemetrie, Tuner, Hub, KVM, Terminal, KI …).
- Zeigt **Adresse, QR-Code und Zugangsdaten** zum Verbinden.

Oder aus einem Terminal: `sudo systemctl enable --now skillfish-dashboard`.

> Aus Vorsicht startet die Oberfläche nach der Installation **nicht von selbst** — du schaltest sie ein, wenn du möchtest.

## Zugriff

Öffne **`https://<IP-der-Platine>:8443`** im Browser (oder `https://BC-250.local:8443`). Da das Zertifikat selbst ausgestellt ist, warnt der Browser beim ersten Mal — das gehört so, geh weiter.

Melde dich mit **deinem Systembenutzer und -passwort** an (denselben wie bei der Anmeldung an SkillFishOS): die Prüfung läuft über PAM.

## Die Bausteine

Die Oberfläche setzt sich aus den Bausteinen zusammen, die du eingeschaltet hast:

- **Telemetrie** — Kurven in Echtzeit für Temperaturen, Takte, Watt und Auslastung von CPU und GPU, mit Werten an der senkrechten Achse und einem Balkenfeld für den **Takt je Kern und Thread** (alle 16 Threads, abgeschaltete deutlich gekennzeichnet).
- **Systemzustand** — Rechnername, IP, Kernel, Laufzeit, Arbeitsspeicher, Platte, aktive CU, erkannte Aussetzer.
- **Steuerung (Tuner)** — schnelle Profile sowie der **vollständige Tuner** im Web: CPU (Takt, Undervolting, Temperatur), GPU (Takt, Spannung, Governor), **Steuerung der Recheneinheiten im Betrieb** (WGP-Raster, ohne Neustart), Lüfter, Grafikspeicher, *Prüfen* und die Assistenten **„Finde mein Maximum“**.
- **Anwendungen und Pakete (Hub)** — eine richtige **Anwendungsverwaltung** (AppStream + Flatpak + Snap): nach Kategorien blättern, suchen, installieren und entfernen, aktualisieren. Die **SkillFishOS-Anwendungen** stehen hervorgehoben oben.
- **Schreibtisch (KVM)** — den echten Schreibtisch der Platine im Browser sehen und bedienen (noVNC), ohne zusätzliche Hardware.
- **Terminal** — eine Konsole im Web (ttyd) innerhalb der Oberfläche.
- **KI auf dem Gerät** — Zustand des Unsloth-Motors, Vulkan-Beschleunigung und ein Chat mit dem lokalen Modell, das auf der GPU der BC-250 läuft.
- **AI-Ops** — das lokale Modell liest Protokolle und Telemetrie und stellt für dich die Diagnose.
- **Protokolle**, **automatische Regeln** (Takt drosseln oberhalb einer °C-Schwelle), **Wake-on-LAN** und geplantes Ein- und Ausschalten.
- **ZeroTier** — um die Oberfläche **von überall** zu erreichen (siehe unten).

Die Knöpfe **Neu starten** und **Ausschalten** sind immer in der oberen Leiste. Die Karten lassen sich **schließen, wieder öffnen und verschieben**, und die **Anordnung lässt sich sichern**.

## Zugriff aus der Ferne (ZeroTier)

Die Oberfläche ist für das **eigene Netz** gedacht. Um sie von außen zu nutzen, schalte den Baustein **ZeroTier** ein: tritt einem deiner Netze bei, gib die Platine auf [my.zerotier.com](https://my.zerotier.com) frei und rufe die Oberfläche dann unter der ZeroTier-Adresse der Platine auf — ohne im Router einen Port zu öffnen.

## Sicherheit

- **HTTPS** mit selbst ausgestelltem Zertifikat (TLS 1.2 oder neuer), beim ersten Start erzeugt.
- **Anmeldung über PAM** mit deinen Zugangsdaten, **signierte Sitzungen** (HMAC) und eine **Begrenzung der Versuche**.
- Für das **eigene Netz** gedacht; für den Zugriff von außen nimm ZeroTier, statt sie unmittelbar ins Internet zu stellen.

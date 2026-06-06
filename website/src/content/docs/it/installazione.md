---
title: Installazione
description: Come scrivere la ISO, avviare l'installer e completare la configurazione.
group: Installazione
order: 1
---

SkillFishOS si installa da una **ISO live** che contiene l'installer grafico [Calamares](https://calamares.io/). L'intero processo si fa con il mouse, senza terminale.

> ✅ La ISO **26.06 «Aetherium»** è disponibile: scaricala dalla pagina [Download](/download). Si avvia in **inglese** per essere universale e ti fa scegliere lingua e tastiera durante l'installazione.

## Requisiti

- una scheda **AMD BC-250** (vedi [hardware](/docs/hardware-bc250));
- un disco **SSD/NVMe** su cui installare;
- un monitor collegato in **DisplayPort** (un adattatore *passivo* DP→HDMI può funzionare, ma vedi le note su audio e display in [Risoluzione problemi](/docs/risoluzione-problemi));
- una **chiavetta USB da almeno 8 GB** per l'installer;
- tastiera e mouse per la fase di installazione.

## 1. Scrivere la ISO su USB

Scarica la ISO dalla pagina [Download](/download) e scrivila su una chiavetta con uno di questi strumenti:

- **[balenaEtcher](https://etcher.balena.io/)** (Windows/macOS/Linux, grafico, consigliato);
- **[Ventoy](https://www.ventoy.net/)** (permette di tenere più ISO sulla stessa chiavetta);
- da terminale Linux con `dd`:

```bash
sudo dd if=SkillFishOS_amd64.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

> Sostituisci `/dev/sdX` con il device corretto della tua chiavetta. **Attenzione**: `dd` scrive senza chiedere conferma e cancella tutto sul device indicato.

## 2. Avviare la BC-250 da USB

Inserisci la chiavetta, accendi la scheda ed entra nel menu di boot/UEFI per selezionare la USB come dispositivo di avvio. Partirà l'ambiente **live** di SkillFishOS (KDE Plasma): puoi già esplorare il sistema prima di installarlo.

## 3. Installazione con Calamares

Dal desktop live avvia l'installer (icona *Installa SkillFishOS*). Calamares ti guida passo-passo:

1. **Lingua e fuso orario.**
2. **Tastiera.**
3. **Partizionamento.** SkillFishOS usa **Btrfs** con i sottovolumi `@rootfs` (sistema) e `@home` (dati utente) separati: questo permette di fare il *rollback* del sistema senza toccare i tuoi file. Una piccola partizione **EFI** e una di **swap** completano lo schema. Per la maggior parte degli utenti va bene l'opzione di installazione automatica ("Cancella disco").
4. **Utente.** Crea il tuo account (sarà nei gruppi corretti per gaming, audio, render, ecc.).
5. **Riepilogo e installazione.**

A fine installazione, riavvia e rimuovi la chiavetta.

## 4. Primo avvio

Al primo avvio **è già tutto configurato**: kernel ottimizzato, governor, overclock, tema, gaming e snapshot sono attivi. Non serve nessuna messa a punto manuale.

Da qui puoi:

- collegare i [controller](/docs/gaming) (DualShock 4 in Bluetooth o controller via USB);
- aggiungere i tuoi giochi a [Steam/EmuDeck](/docs/gaming);
- attivare lo stack [AI locale](/docs/ai-locale) quando ti serve;
- regolare l'hardware col [Tuner](/docs/app-native) se vuoi.

## Schema del disco

| Partizione | Filesystem | Contenuto |
|---|---|---|
| `nvme0n1p1` | FAT32 (EFI) | bootloader GRUB |
| `nvme0n1p2` | **Btrfs** | `@rootfs` (sistema) + `@home` (dati) |
| `nvme0n1p3` | swap | memoria di scambio |

## Fonti

- [Calamares](https://calamares.io/) — l'installer universale
- [balenaEtcher](https://etcher.balena.io/) · [Ventoy](https://www.ventoy.net/)
- [Wiki Btrfs](https://btrfs.readthedocs.io/) — sottovolumi e snapshot

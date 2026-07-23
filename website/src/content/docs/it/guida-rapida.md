---
title: Guida rapida
description: I primi 10 minuti con SkillFishOS — dal primo avvio al primo gioco.
group: Introduzione
order: 3
---

Hai installato SkillFishOS (vedi [Installazione](/docs/installazione)) e sei al primo avvio. Questa pagina è una **checklist veloce** per partire subito: tutto il resto è già configurato e funzionante.

## In una riga

> Accendi → sei già al desktop ottimizzato → colleghi un controller → aggiungi i tuoi giochi → giochi. Niente terminale, niente messa a punto.

## 1. Primo avvio (è già tutto pronto)

Al primo boot trovi un desktop **KDE Plasma 6** a tema steampunk, con kernel ottimizzato, governor SMU, profilo **Stock**, gaming stack e snapshot **già attivi**. In alto a destra l'**HUD** mostra in tempo reale CPU, GPU, temperature, RAM, ventola e i dispositivi Bluetooth collegati.

Non devi installare driver, regolare frequenze o attivare nulla: il sistema parte "al massimo della compatibilità".

## 2. Connettiti alla rete

L'ethernet è gestita da NetworkManager ed è già pronta. Per il Wi-Fi/Bluetooth usa l'icona di rete nel pannello. La connessione serve per Steam, gli aggiornamenti e l'AI locale.

## 3. Collega un controller

| Controller | Come |
|---|---|
| **DualShock 4** | Bluetooth: tieni premuto **Share + PS** finché lampeggia, poi accoppia dall'icona Bluetooth. Ha il **giroscopio**. |
| **Controller generico** | Via **USB** con un cavo **dati** (non solo di ricarica): viene visto come Xbox 360. |

Dettagli e risoluzione problemi → [Gaming](/docs/gaming) e [Risoluzione problemi](/docs/risoluzione-problemi).

## 4. Aggiungi i tuoi giochi

- **Steam** è già installato e integrato con gamescope/MangoHud. Accedi col tuo account e installa i giochi: i titoli Windows girano con **Proton**.
- **Epic / GOG** → [Heroic](/docs/gaming).
- **Emulazione** → avvia **EmuDeck**, scegli gli emulatori, poi gioca dal frontend **ES-DE**. ROM, BIOS e chiavi li aggiungi tu (vedi la nota legale in [Gaming](/docs/gaming)).

## 5. (Opzionale) Spingi l'hardware

SkillFishOS parte in profilo **Stock** per essere sicuro su qualunque scheda. Quando vuoi più prestazioni apri il **[Tuner](/docs/app-native)** e sali di profilo:

**Stock → Performance → Turbo → Crazy**

Il Tuner **testa ogni profilo sulla tua BC-250** e fa il *rollback* automatico se la scheda non regge. È il modo sicuro per scoprire fin dove arriva il tuo esemplare (vedi [GPU e overclock](/docs/gpu-overclock)).

## 6. (Opzionale) Accendi l'AI locale

Quando ti serve un assistente AI offline, apri il **pannello AI** e accendi lo stack [Ollama + OpenWebUI](/docs/ai-locale). Ricorda: AI e giochi pesanti **non** vanno usati insieme (stessa GPU e memoria). A stack spento la GPU torna tutta al gaming.

## Cose da sapere subito

- **Non riattivare la sospensione**: sulla BC-250 è guasta e la scheda non si risveglia (vedi [Desktop](/docs/desktop)).
- Usa un **monitor DisplayPort** o un adattatore **passivo**; gli adattatori **attivi** DP→HDMI rompono l'audio.
- Hai una **rete di sicurezza**: prima e dopo ogni aggiornamento viene creato uno snapshot Btrfs; in caso di guai torni indietro dal menu GRUB → *SkillFishOS snapshots* (vedi [Storage e snapshot](/docs/storage-snapshot)).

## E adesso?

- Vuoi capire **cosa** stai usando? → [Hardware BC-250](/docs/hardware-bc250)
- Vuoi i **numeri** reali di prestazioni? → [Prestazioni e benchmark](/docs/prestazioni)
- Hai una **domanda** veloce? → [FAQ](/docs/faq)
- Un **termine** non chiaro? → [Glossario](/docs/glossario)

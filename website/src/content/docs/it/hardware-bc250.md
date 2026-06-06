---
title: L'hardware AMD BC-250
description: La scheda, l'APU, le sue caratteristiche e i suoi difetti hardware noti.
group: Introduzione
order: 2
---

La **AMD BC-250** è una scheda compatta basata su un'**APU semi-custom** chiamata in codice *Oberon* per la parte CPU e *Cyan Skillfish* per la parte grafica — la stessa famiglia di silicio delle console AMD di generazione attuale. Fu prodotta per sistemi di mining (tipicamente montata in cestelli da più schede) e oggi si trova sul mercato dell'usato a prezzi contenuti.

## Specifiche principali

| Componente | Dettaglio |
|---|---|
| **CPU** | 6 core / 12 thread **Zen 2** ("Oberon"), fino a **3.9 GHz** (Turbo), 4.0 GHz validati |
| **GPU** | **RDNA 2** "Cyan Skillfish" (`gfx1013`), fino a **40 Compute Unit** sbloccabili |
| **Memoria** | **16 GB GDDR6** condivisa (UMA) tra CPU e GPU |
| **Potenza** | ~**11.3 TFLOPS** FP32 con 40 CU a 2000 MHz (misurato con vkpeak) |
| **Banda memoria** | ~350–367 GB/s (misurata con clpeak) |
| **Uscita video** | 1× DisplayPort |

La memoria è **unificata**: la GDDR6 è condivisa tra sistema e grafica. Di default circa 8 GB sono assegnati come VRAM, ma su Linux si può estendere lo spazio video sfruttando il **GTT** (Graphics Translation Table), arrivando a far vedere a Vulkan ~13 GiB di memoria — utile soprattutto per i modelli AI.

## Lo sblocco delle 40 CU

La GPU ha 40 CU ma il driver ne attiva solo **24** di default. SkillFishOS le **instrada fino a 40 a caldo** (senza riavvio): si parte dalla baseline driver e un servizio porta a 40 all'avvio, regolabili dal [Tuner](/docs/app-native). Il reverse engineering dello sblocco è documentato da [bc250-40cu-unlock](https://github.com/duggasco/bc250-40cu-unlock); il controllo a runtime via `umr` si ispira a [bc250-cu-live-manager](https://github.com/WinnieLV/bc250-cu-live-manager) (reimplementato clean-room).

> Con 40 CU attive SkillFishOS misura **11385 GFLOPS** FP32 (vkpeak) da freddo, contro i ~6141 di una configurazione baseline a 24 CU: un **+85%** circa.

## Difetti hardware da conoscere

La BC-250 è hardware "da mining" riadattato: ha alcuni limiti che SkillFishOS aggira via software. Conoscerli aiuta a capire molte scelte del sistema.

### Hot-Plug Detect (HPD) del DisplayPort rotto

Il rilevamento del collegamento del monitor sul connettore DisplayPort **non funziona**: la scheda non "vede" quando si attacca uno schermo. SkillFishOS risolve con un demone dedicato (`skillfish-dp-hotswap`) che forza il rilevamento all'avvio e monitora i cambi di monitor a runtime, più il parametro kernel `video=DP-1:e` come fallback. Vedi [Desktop](/docs/desktop) e [Risoluzione problemi](/docs/risoluzione-problemi).

### Sospensione (suspend) ACPI rotta

La sospensione **s2idle è guasta**: la scheda va in sospensione ma **non si risveglia** e richiede un reset. Inoltre una macchina sospesa è irraggiungibile da remoto. Per questo SkillFishOS **disabilita in modo permanente** tutti gli stati di sospensione (vedi [Desktop](/docs/desktop)). È una misura obbligatoria.

### IOMMU non utilizzabile

L'IOMMU sulla BC-250 è instabile: **non va mai abilitato**. Il sistema parte sempre senza IOMMU.

### Sensori termici

È disponibile solo il sensore di temperatura *edge* della GPU; **non esiste un sensore per la temperatura della VRAM**. Il raffreddamento di serie è marginale, quindi i confronti di benchmark "back-to-back" non sono validi (effetto *heat-soak*): tra una prova e l'altra conviene lasciare raffreddare la scheda alcuni minuti.

## Raffreddamento, case 3D e ventole

La BC-250 arriva **nuda**, pensata per cestelli da mining con cinque ventole *screamer* da 80 mm pilotate dal connettore della distribuzione di potenza. Per l'uso desktop serve un raffreddamento dedicato. **Due cose vanno raffreddate**: il dissipatore dell'APU **e** i chip **GDDR6**, che scaldano molto e non hanno un sensore di temperatura (vedi [GPU/overclock](/docs/gpu-overclock)).

**Cosa funziona (consigli dalla comunità):**

- **2× ventole da 120 mm a pressione statica** puntate sul dissipatore sono il setup desktop più diffuso; in mancanza di un case si possono appoggiare direttamente sopra il dissipatore (fissaggio con fascette attraverso le alette).
- Una **ventola dedicata sulla VRAM** è caldamente consigliata se overclocchi: i moduli GDDR6 sono il punto più caldo.
- La ventola si collega all'header **PWM a 4 pin** della scheda — SkillFishOS la pilota via `nct6686` (sensori) e la tiene in **automatico**.

**Case e convogliatori (STL gratuiti, stampabili in 3D):**

| Modello | Autore | Note |
|---|---|---|
| [Console Style Case](https://www.thingiverse.com/thing:7172528) | Arthrimus | Case "console" + alloggio PSU, shroud per **1× 120 mm** |
| [ASRock BC-250 Shell Case](https://www.printables.com/model/1228207-asrock-amd-bc-250-shell-case) | onemorecap | Guscio snap-on, montaggio rapido di una ventola |
| [Yet Another BC-250 Fan Shroud](https://www.printables.com/model/1339540-yet-another-bc-250-fan-shroud) | ViRazY | **140 mm** in aspirazione + **120 mm** in espulsione |
| [Case ATX PSU & Fan Duct](https://www.printables.com/model/1616167-amd-bc-250-case-atx-psu-fan-duct) | ZMASLO | Usa una PSU ATX standard, convogliatore che non danneggia il dissipatore |
| [Case per PSU ATX standard](https://www.thingiverse.com/thing:7269520) | CatSiewDai | Case completo per alimentatori ATX |
| [OC vRAM Fan Kit (remix)](https://www.thingiverse.com/thing:7271946) | marccyberwiz | Kit ventola **dedicato alla VRAM** per overclock |
| [NexGen3D — DIY Steam Machine (Bazzite)](https://www.printables.com/model/1499974-nexgen3d-diy-steam-machine-powered-by-bazzite) | NexGen3D | Case completo stile **Steam Machine** per la BC-250 |
| [NexGen3D — Steam Machine PRO (liquid-cooled)](https://www.printables.com/model/1614131-nexgen3d-diy-steam-machine-pro-liquid-cooled-bc-25/files) | NexGen3D | Versione **PRO raffreddata a liquido** (AIO) — massimo raffreddamento |
| [NexGen3D — Supporto AIO per BC-250](https://www.printables.com/model/1554003-nexgen3d-aio-mount-for-the-bc-250) | NexGen3D | Staffa per montare un **AIO** (raffreddamento a liquido) sulla BC-250 |

> Guida di riferimento sul raffreddamento: [Cooling Solutions — amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs/hardware/cooling/).

## Fonti

- [bc250.info](https://bc250.info) — wiki comunitaria
- [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs) — documentazione tecnica (incl. [raffreddamento](https://elektricm.github.io/amd-bc250-docs/hardware/cooling/))
- [mothenjoyer69/bc250-documentation](https://github.com/mothenjoyer69/bc250-documentation) — note hardware e cooling
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock) — sblocco delle Compute Unit
- [bc250_memcfg (fanoush)](https://github.com/fanoush/bc250_memcfg) — configurazione della memoria
- Driver `amdgpu` del kernel Linux — [docs.kernel.org/gpu/amdgpu](https://docs.kernel.org/gpu/amdgpu/)

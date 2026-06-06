---
title: Glossario
description: I termini tecnici di SkillFishOS e della BC-250, spiegati in breve.
group: Riferimenti
order: 5
---

I termini che ricorrono nella documentazione, spiegati in una riga. In ordine alfabetico.

## Hardware e APU

**APU** — *Accelerated Processing Unit*: un chip che integra CPU e GPU sullo stesso die. La BC-250 ne monta una semi-custom AMD.

**BC-250** — la scheda su cui gira SkillFishOS: APU Zen 2 + RDNA 2, 16 GB GDDR6, nata per il mining.

**Cyan Skillfish** — nome in codice della parte **grafica** (GPU) dell'APU della BC-250. Da qui il nome "SkillFish".

**Oberon** — nome in codice della parte **CPU** (Zen 2) dell'APU.

**Compute Unit (CU)** — i blocchi di calcolo della GPU. La BC-250 ne ha 40, ma di default ne espone meno: SkillFishOS le **sblocca tutte** (vedi [kernel](/docs/kernel)).

**gfx1013** — l'identificativo dell'architettura GPU della BC-250 (famiglia RDNA 2). È importante perché **ROCm non lo supporta** → si usa Vulkan.

**RDNA 2** — l'architettura grafica AMD della GPU (stessa famiglia delle console attuali).

**Zen 2** — l'architettura CPU AMD dell'APU (6 core / 12 thread).

**GDDR6** — il tipo di memoria della scheda: veloce, qui **condivisa** tra CPU e GPU.

**UMA** — *Unified Memory Architecture*: CPU e GPU usano lo **stesso** pool di memoria (i ~16 GB di GDDR6).

**GTT** — *Graphics Translation Table*: meccanismo che permette alla GPU di usare memoria di sistema oltre la VRAM dedicata. SkillFishOS lo estende per far vedere a Vulkan ~13 GiB (utile per l'AI).

## Frequenze, tensioni, termica

**SMU** — *System Management Unit*: il micro-controllore interno all'APU che gestisce frequenze e tensioni. Sulla BC-250 il controllo passa **solo** da qui, non dal sysfs amdgpu standard.

**Governor SMU** — il servizio (`cyan-skillfish-governor`) che imposta i *safe-point* di frequenza/tensione della GPU.

**sclk / mclk** — frequenza del **core** GPU (sclk) e della **memoria** (mclk). Sulla BC-250 il mclk **non** è regolabile.

**Undervolt** — abbassare la tensione a parità di frequenza: stesso lavoro, **meno calore e consumo**. Vedi [GPU e overclock](/docs/gpu-overclock).

**Overclock (OC)** — alzare le frequenze oltre il default per più prestazioni.

**Vid** — la tensione richiesta dal chip a una certa frequenza. Sulla BC-250 il massimo invalicabile è **1.325 V**.

**Thermal-guard** — il watchdog di sistema che riduce i clock se si superano gli 85 °C.

**Heat-soak** — l'accumulo di calore che falsa i benchmark "back-to-back": serve far raffreddare la scheda tra le prove.

**Silicon lottery** — il fatto che ogni esemplare di chip regge OC/undervolt diversi: per questo SkillFishOS valida i profili **sulla tua** scheda.

## Software di sistema

**Debian sid** — il ramo *unstable* di Debian, sempre aggiornato ma soggetto a regressioni: la base di SkillFishOS (vedi [Aggiornamenti](/docs/aggiornamenti)).

**KDE Plasma 6** — l'ambiente desktop usato, vestito a tema steampunk.

**linux-tkg** — la ricetta di compilazione del kernel (Frogging-Family) su cui si basa il kernel su misura di SkillFishOS.

**Mesa / RADV** — i driver grafici open source; **RADV** è il driver **Vulkan** usato dalla GPU della BC-250.

**ROCm** — lo stack di calcolo "ufficiale" AMD: **non** supporta gfx1013, quindi non si usa.

**Vulkan** — l'API grafica/di calcolo usata sia per il gaming sia per l'**AI** (Ollama) sulla BC-250.

**Btrfs** — il filesystem con snapshot copy-on-write che dà la "rete di sicurezza" (vedi [Storage e snapshot](/docs/storage-snapshot)).

**Snapper** — lo strumento che crea snapshot Btrfs automatici prima/dopo gli aggiornamenti.

**grub-btrfs** — fa comparire gli snapshot nel menu GRUB per il rollback all'avvio.

**APT pinning** — bloccare un pacchetto a una versione verificata, per i componenti fragili su questo hardware.

**reprepro** — lo strumento che gestisce il repository APT firmato di SkillFishOS.

**HPD** — *Hot-Plug Detect*: il rilevamento del collegamento del monitor. Sulla BC-250 è **guasto** → demone `skillfish-dp-hotswap`.

**s2idle / suspend** — gli stati di sospensione ACPI: **guasti** sulla BC-250, perciò disabilitati.

**IOMMU** — unità di gestione memoria per la virtualizzazione I/O: instabile sulla BC-250, **mai** abilitata.

## Gaming e AI

**Proton** — il livello di compatibilità (Valve) che fa girare i giochi Windows su Linux via Steam.

**gamescope** — il micro-compositore di Valve per il gaming (sessione "console", upscaling FSR1/NIS).

**EmuDeck / ES-DE** — installer di emulatori e frontend per l'emulazione.

**FSR / OptiScaler** — tecnologie di **upscaling**. FSR 4 non è disponibile (richiede RDNA 4); si usano FSR1/NIS o OptiScaler.

**Ollama / OpenWebUI** — backend ed interfaccia dell'AI locale.

**qwen3:14b** — il modello AI di riferimento, che gira interamente su GPU.

**Tuner** — l'app nativa di SkillFishOS per regolare l'hardware con test-and-rollback (vedi [App native](/docs/app-native)).

## Fonti

- [bc250.info](https://bc250.info) · [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- [Documentazione amdgpu](https://docs.kernel.org/gpu/amdgpu/) · [Mesa / RADV](https://docs.mesa3d.org/drivers/radv.html)

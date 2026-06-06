---
title: Prestazioni e benchmark
description: Tutti i numeri reali misurati sulla nostra BC-250 — FP32, banda memoria, FPS in gioco, profili e consumi.
group: Riferimenti
order: 3
---

Questa pagina raccoglie i **dati di prestazioni reali**, tutti **misurati sulla nostra BC-250**. Servono come riferimento, non come promessa: ogni esemplare è diverso (*silicon lottery*) e il raffreddamento incide moltissimo.

> ⚠️ I numeri sono ottenuti con le 40 CU attive e raffreddamento adeguato. La scheda di serie raffredda male: i confronti "back-to-back" senza pause sono falsati dall'*heat-soak* — lascia raffreddare alcuni minuti tra una prova e l'altra.

## Screenshot dal nostro ferro

Catture dello schermo riprese **durante i benchmark**, sulla **nostra** BC-250 con SkillFishOS — niente render né mockup.

![Black Myth: Wukong — 112 FPS di media a 1080p sulla AMD BC-250](/img/benchmarks/wukong-112fps.jpg)
*Black Myth: Wukong — **112 FPS** di media a 1080p (max 128, 1% basso 101). APU AMD BC-250, GPU RADV gfx1013.*

![Unigine Heaven 4.0 — 113.7 FPS, punteggio 2865](/img/benchmarks/heaven-113fps.jpg)
*Unigine Heaven 4.0 — **113.7 FPS**, punteggio **2865** (1080p Ultra, 8× AA, tassellazione Extreme). Kernel 7.0.10-skillfishos.*

![Unigine Heaven — scena renderizzata in tempo reale sulla BC-250](/img/benchmarks/heaven-scene.jpg)
*Unigine Heaven — la scena renderizzata in tempo reale sulla BC-250 durante il test.*

## GPU — calcolo FP32 (vkpeak)

| Configurazione | FP32 | Note |
|---|---|---|
| Baseline **24 CU** | ~6141 GFLOPS | configurazione non sbloccata |
| **40 CU** a freddo | **11385 GFLOPS** | +85% rispetto alla baseline |
| **40 CU** sotto stress (a caldo) | ~10214 GFLOPS | regime stabile prolungato |

Lo sblocco delle 40 Compute Unit (vedi [kernel](/docs/kernel) e [hardware](/docs/hardware-bc250)) è il singolo intervento che incide di più sulle prestazioni di calcolo.

## GPU — banda di memoria (clpeak)

| Metrica | Valore |
|---|---|
| Banda GDDR6 misurata | **~350–367 GB/s** |
| `mclk` regolabile | **No** (la frequenza memoria è fissa) |

La memoria è **unificata (UMA)**: i ~16 GB di GDDR6 sono condivisi tra CPU e GPU. Con il GTT esteso, Vulkan arriva a vedere **~13 GiB** di memoria — utile per i modelli AI (vedi [AI in locale](/docs/ai-locale)).

## Profili del Tuner — frequenze, tensioni, temperature

| Profilo | CPU | Tensione CPU | GPU | Temp. di picco |
|---|---|---|---|---|
| **Stock** *(default ISO)* | 3500 MHz | — | 1500 MHz | la più bassa |
| **Performance** | 3700 MHz | ~1106 mV (`scale −16`) | 2000 MHz | bilanciata |
| **Turbo** | 3900 MHz | ~1199 mV (`scale −24`) | 2230 MHz | < 85 °C (cap) |
| **Crazy** | 4.0 GHz | ~1224 mV (`scale −36`) | 2230 MHz | ~83 °C in stress 120 s |

- **Vid massimo invalicabile: 1.325 V** (mai superato).
- Cap termico **85 °C** su tutti i profili, ventola in automatico.
- A riposo la GPU scende a **350 MHz / 700 mV** (governor SMU).

I profili oltre Stock vanno **validati dal [Tuner](/docs/app-native)** sulla tua scheda, con test automatico e rollback. Dettagli in [GPU, overclock e undervolt](/docs/gpu-overclock).

## FPS in gioco — il caso *Black Myth: Wukong*

*Black Myth: Wukong* è un titolo **CPU/draw-call bound**: gli FPS **non** scalano con la risoluzione né con il clock GPU.

- Alzare la GPU a Turbo **non** aumenta gli FPS: contano l'**overclock CPU** e un buon raffreddamento.
- **FSR 4 non è disponibile** (richiede hardware RDNA 4). Si usano l'upscaling di **gamescope** (FSR1/NIS) o **[OptiScaler](https://github.com/optiscaler/OptiScaler)** per-gioco.

> Lezione generale: prima di "spingere la GPU", capisci se il gioco è GPU-bound o CPU-bound. Su molti titoli leggeri e indie la BC-250 è abbondante; su titoli pesanti e draw-call bound, il collo di bottiglia è la CPU.

## Accoppiamento termico CPU↔GPU

CPU e GPU condividono **lo stesso die** e **lo stesso budget di potenza**. Sotto carico misto (gioco che usa CPU+GPU insieme) l'APU si autoprotegge e la CPU scende spontaneamente a **~3450 MHz** per restare nel budget e sotto gli 85 °C. **Non è un difetto**: è il chip che cede i clock meno utili. Un undervolt su un lato lascia più margine termico all'altro.

## Consumo e termica

| Voce | Valore indicativo |
|---|---|
| Sensore disponibile | solo *edge* GPU (**nessun** sensore VRAM) |
| Cap termico | **85 °C** (SMU + thermal-guard di sistema) |
| Raffreddamento di serie | marginale → consigliati 2× 120 mm + ventola dedicata VRAM |

Per raffreddamento, case 3D stampabili e ventole consigliate vedi [Hardware BC-250](/docs/hardware-bc250).

## Come sono stati misurati

| Strumento | Cosa misura |
|---|---|
| [vkpeak](https://github.com/nihui/vkpeak) | throughput FP32/FP16 via Vulkan |
| [clpeak](https://github.com/krrishnarraj/clpeak) | banda di memoria e throughput OpenCL |
| [sysbench](https://github.com/akopytov/sysbench) | stress/benchmark CPU (usato anche dal Tuner) |
| MangoHud in-game | FPS e frametime nei giochi reali |

## Fonti

- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) · [sysbench](https://github.com/akopytov/sysbench)
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock) — sblocco CU
- [bc250.info](https://bc250.info) — safe-point e note termiche della comunità
- [OptiScaler](https://github.com/optiscaler/OptiScaler) — upscaling per-gioco

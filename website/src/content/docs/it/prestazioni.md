---
title: Prestazioni e benchmark
description: Tutti i benchmark reali della BC-250 con SkillFishOS — screenshot, settaggi completi, frequenze, tensioni, temperature e consumi.
group: Riferimenti
order: 3
---

Questa è la sezione **completa dei benchmark**: ogni prova è stata eseguita sulla **nostra BC-250** con SkillFishOS, con screenshot reali, **tutti i settaggi usati**, e la telemetria di **frequenze, tensioni, temperature, consumi e ventola** registrata durante il run.

> ⚠️ **Silicon lottery + raffreddamento.** I numeri valgono per *questo* esemplare con un raffreddamento adeguato. La scheda di serie raffredda male: i confronti "back-to-back" senza pause sono falsati dall'*heat-soak* — lascia raffreddare alcuni minuti tra una prova e l'altra.

## Condizioni di test (banco di prova)

Valide per **tutti** i benchmark sotto, salvo dove indicato diversamente.

| Voce | Valore |
|---|---|
| Scheda | **AMD BC-250** — APU Zen 2 "Oberon" + RDNA 2 "Cyan Skillfish" (`gfx1013`) |
| Memoria | **16 GB GDDR6** unificata (UMA) |
| Compute Unit | **40 / 40 attive** (instradate a caldo, vedi [GPU](/docs/gpu-overclock)) |
| Kernel | **7.0.10-skillfishos** (linux-tkg) |
| Driver | **Mesa 26.0.8** — RADV (Vulkan) / radeonsi (OpenGL), ACO |
| Governor GPU | cyan-skillfish — idle **350 MHz / 700 mV**, carico **2230 MHz / ~1000 mV** |
| Profilo OC | **Turbo/Crazy** (GPU cap 2230 MHz, CPU 3.9–4.0 GHz) |
| Cap termico | **85 °C** (SMU + thermal-guard), ventola in **automatico** |
| Risoluzione | **1920×1080** |

> Promemoria architetturale: CPU e GPU condividono **lo stesso die** e **lo stesso budget di potenza**. Sotto carico misto la CPU cede spontaneamente clock (≈3.4–3.5 GHz) per restare nel budget e sotto gli 85 °C — non è un difetto, è il chip che si autoprotegge.

---

## 🎮 Black Myth: Wukong — 112 FPS (1080p)

![Black Myth: Wukong — 112 FPS di media a 1080p sulla AMD BC-250](/img/benchmarks/wukong-112fps.jpg)

| Settaggio | Valore |
|---|---|
| Risoluzione | 1920×1080 |
| Limite FPS | nessuno (illimitato) |
| Tipo carico | **CPU / draw-call bound** |
| Upscaling | FSR 4 non disponibile (RDNA 4) → gamescope FSR1/NIS o OptiScaler |

**Risultato:** media **112 FPS** · massima **128** · minima **92** · 1% basso **101**.

**Telemetria durante il run** (≈4 min):

| Metrica | Valore misurato |
|---|---|
| GPU clock | ~1.4–1.6 GHz (*non satura*: il gioco è CPU-bound) |
| GPU edge | 83–86 °C |
| GPU power | ~90–140 W |
| GPU mV | ~970–987 mV |
| CPU clock | ~3.5 GHz (sceso da 3.9 per il budget condiviso) |
| CPU temp | 85 °C (al cap) |
| VRAM | ~1.9 GB (menu) → ~4.4 GB (in gioco) |
| Ventola | ~2950–3140 RPM |

> Lezione: su un titolo *draw-call bound* come Wukong gli FPS **non** dipendono dalla risoluzione né dal clock GPU. Conta la **stabilità della CPU** sotto carico e un buon raffreddamento.

---

## 🧪 Unigine Superposition — 1080p HIGH: 12938

![Unigine Superposition 1080p High — punteggio 12938 sulla BC-250](/img/benchmarks/superposition-high.jpg)

| Settaggio | Valore |
|---|---|
| Versione | 1.1 |
| API grafica | **OpenGL** |
| Risoluzione | 1920×1080, fullscreen |
| Shaders | **High** |
| Texture | High |
| DOF | abilitato |
| Motion Blur | abilitato |

**Risultato:** punteggio **12 938** · FPS min **75.59** · media **96.77** · max **127.16**.
**Configurazione letta dal tool:** CPU AMD BC-250 **@ 3894 MHz**, RAM 7 GB, GPU AMD BC-250 8 GB (Cyan Skillfish), kernel 7.0.10-skillfishos.

---

## 🧪 Unigine Superposition — 1080p EXTREME: 5513

![Unigine Superposition 1080p Extreme — punteggio 5513 sulla BC-250](/img/benchmarks/superposition-extreme.jpg)

| Settaggio | Valore |
|---|---|
| Versione | 1.1 |
| API grafica | **OpenGL** |
| Risoluzione | 1920×1080, fullscreen |
| Shaders | **Extreme** |
| Texture | High |
| DOF | abilitato |
| Motion Blur | abilitato |

**Risultato:** punteggio **5 513** · FPS media **41.25** (min ~32.8 · max ~49).

![Unigine Superposition — scena renderizzata in tempo reale](/img/benchmarks/superposition-scene.jpg)
*Una scena di Superposition renderizzata in tempo reale sulla BC-250.*

---

## 🏔️ Unigine Heaven 4.0 — 113.7 FPS · score 2865

![Unigine Heaven 4.0 — 113.7 FPS, punteggio 2865 sulla BC-250](/img/benchmarks/heaven-113fps.jpg)

| Settaggio | Valore |
|---|---|
| API grafica | **OpenGL** |
| Risoluzione | 1920×1080, windowed |
| Anti-aliasing | **8×** |
| Qualità | **Ultra** |
| Tassellazione | **Extreme** |

**Risultato:** **113.7 FPS** · punteggio **2865** · min **54.8** · max **219.5**.
**Piattaforma letta dal tool:** Linux 7.0.10-skillfishos x86_64 · CPU AMD BC-250 ×12 · GPU gfx1013.

![Unigine Heaven — scena renderizzata in tempo reale](/img/benchmarks/heaven-scene.jpg)
*La scena di Heaven renderizzata in tempo reale sulla BC-250 durante il test.*

---

## ⚙️ Calcolo GPU — vkpeak (sintetico)

Throughput di calcolo Vulkan sulla **stessa** scheda, prima e dopo lo sblocco delle 40 CU.

| Metrica | Baseline 24 CU | SkillFishOS 40 CU |
|---|---|---|
| **FP32** scalar | 6141 GFLOPS | **11 329** GFLOPS *(11 385 da freddo)* |
| FP16 vec4 | 12 260 | **22 685** |
| int8 dot-product | 24 550 GIOPS | **45 495** GIOPS |
| FP64 scalar | 385 | ~640 |
| copy d2d (banda interna) | — | 191 GBPS |

Con le 40 CU attive: **+85%** in FP32 sulla baseline (≈**11.3 TFLOPS**). A caldo, sotto stress prolungato, si assesta intorno a **10 214 GFLOPS**. A riposo il governor scende a 350 MHz, edge ~54 °C dopo il carico.

## 📦 Banda di memoria — clpeak

| Metrica | Valore |
|---|---|
| Banda GDDR6 misurata | **~350–367 GB/s** |
| `mclk` regolabile | **No** (frequenza memoria fissa) |
| Memoria vista da Vulkan | ~13 GiB (con GTT esteso) |

---

## 🔧 Profili del Tuner — clock, tensioni, temperature

| Profilo | CPU | Tensione CPU | GPU | Temp. di picco |
|---|---|---|---|---|
| **Stock** *(default ISO)* | 3500 MHz | — | 1500 MHz | la più bassa |
| **Performance** | 3700 MHz | ~1106 mV (`scale −16`) | 2000 MHz | bilanciata |
| **Turbo** | 3900 MHz | ~1199 mV (`scale −24`) | 2230 MHz | < 85 °C (cap) |
| **Crazy** | 4.0 GHz | ~1224 mV (`scale −36`) | 2230 MHz | ~83 °C in stress 120 s |

- **Vid massimo invalicabile: 1.325 V** (mai superato).
- Cap termico **85 °C** su tutti i profili; ventola automatica; a riposo GPU **350 MHz / 700 mV**.

## 🌡️ Validazione termica (stress test)

Dati registrati durante la validazione automatica del Tuner (test-and-rollback).

| Fase | Clock | Temperatura | Note |
|---|---|---|---|
| Idle | CPU ~2.5 GHz · GPU 350 MHz | k10 46 °C · GPU 45 °C | a riposo |
| **CPU stress** (12 thread, 120 s) | CPU **3.68–3.69 GHz** | k10 **85 °C** (al cap) | GPU resta a 350 MHz/56 °C |
| **GPU stress** (vkpeak loop, 120 s) | GPU **2000 MHz** | edge fino a **86 °C** | a 86 °C il governor scende a 1819–1900 MHz (thermal-guard); la CPU cala a ~2.2–2.4 GHz per il budget condiviso |

---

## 📊 Confronti

**Stesso hardware, solo cambiando OS** — Superposition 1080p Extreme sulla **stessa** BC-250:

| Sistema | Punteggio |
|---|---|
| **SkillFishOS** (GPU 2230 · CPU 3900, 40 CU) | **5513** |
| Altra distro (Bazzite, clock di fabbrica) | 4102 |

→ **+34% di prestazioni reali** dallo stesso identico chip, grazie a 40 CU sbloccate, governor a 2230 MHz e OC+undervolt CPU.

**Contro le Radeon desktop** (Superposition 1080p High): la BC-250 con SkillFishOS (**12 938**) pareggia una **RX 6600 / 6600 XT** da 200 €+, con compute grezzo da **RX 6700** (~11.3 TFLOPS) — su una scheda da ~50 €.

---

## 🛠️ Strumenti e metodo

| Strumento | Cosa misura |
|---|---|
| [vkpeak](https://github.com/nihui/vkpeak) | throughput FP32/FP16/int8 via Vulkan |
| [clpeak](https://github.com/krrishnarraj/clpeak) | banda di memoria e throughput OpenCL |
| [sysbench](https://github.com/akopytov/sysbench) | stress/benchmark CPU (usato anche dal Tuner) |
| [Unigine Superposition / Heaven](https://benchmark.unigine.com/) | benchmark grafici OpenGL |
| MangoHud in-game | FPS e frametime nei giochi reali |
| telemetria custom | clock/temp/power/ventola via sysfs `amdgpu`, `k10temp`, `nct6686` |

## Fonti

- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) · [sysbench](https://github.com/akopytov/sysbench) · [Unigine](https://benchmark.unigine.com/)
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock) — sblocco CU
- [bc250.info](https://bc250.info) — safe-point e note termiche della comunità
- [OptiScaler](https://github.com/optiscaler/OptiScaler) — upscaling per-gioco

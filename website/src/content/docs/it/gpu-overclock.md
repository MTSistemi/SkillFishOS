---
title: GPU, CPU, overclock e undervolt
description: Come SkillFishOS controlla frequenze, tensioni e temperature della BC-250 — con i dati reali misurati sull'hardware.
group: Sistema
order: 2
---

Su una APU normale le frequenze si regolano via sysfs `amdgpu`. Sulla BC-250 **non funziona così**: il controllo passa per l'**SMU** (System Management Unit) e richiede strumenti dedicati. SkillFishOS li integra tutti, già configurati con profili sicuri e un sistema di protezione termica.

> ⚠️ **Silicon lottery.** Tutti i valori di questa pagina sono **misurati sulla nostra BC-250**. Ogni esemplare è diverso: una scheda può reggere un undervolt più spinto, un'altra meno. Per questo SkillFishOS **parte sempre in profilo Stock** e ti lascia salire con il [Tuner](/docs/app-native), che valida ogni preset **sulla tua scheda** con test automatico e rollback.

## I tre profili

Il [Tuner](/docs/app-native) espone **quattro preset**. La ISO si avvia con **Stock**; gli altri si attivano con un clic dopo il test.

| Profilo | CPU | GPU | Note |
|---|---|---|---|
| **Stock** *(default ISO)* | 3500 MHz | 1500 MHz | Massima compatibilità su qualunque BC-250 |
| **Performance** | 3700 MHz · ~1106 mV | 2000 MHz | Bilanciato e undervoltato |
| **Turbo** | 3900 MHz · ~1199 mV | 2230 MHz | Spinta alta, validato sotto cap 85 °C |
| **Crazy** | 4.0 GHz · ~1224 mV | 2230 MHz | Massimo validato (~83 °C in stress) |

Tutti i profili rispettano lo stesso **cap termico a 85 °C** e tengono la **ventola in automatico**.

## Il governor SMU della GPU

Le frequenze GPU sono gestite dal **[cyan-skillfish-governor](https://github.com/Magnap/cyan-skillfish-governor)** (scritto in Rust), un servizio di sistema con configurazione in `/etc/cyan-skillfish-governor/config.toml`. Definisce dei *safe-point* di frequenza/tensione: a riposo **350 MHz / 700 mV**, sotto carico il valore del profilo (es. 1500/900 in Stock, 2230/1000 in Turbo).

> Il sysfs amdgpu standard (`power_dpm_force_performance_level`, `pp_dpm_sclk`) **non** controlla la BC-250: solo il governor SMU lo fa. La GPU sale alla frequenza di boost solo sotto **saturazione grafica** reale.

## Overclock e undervolt della CPU

La CPU (6 core Zen 2 "Oberon") è gestita da un servizio one-shot **`bc250-smu-oc.service`** che applica i valori da `/etc/bc250-smu-oc.conf` tramite il progetto [bc250_smu_oc](https://github.com/bc250-collective/bc250_smu_oc). Risulta *inactive* dopo l'applicazione: è normale (è "one-shot").

Cosa abbiamo misurato spingendo la **nostra** scheda:

- **3700 MHz** (preset *Performance*) con undervolt a ~**1106 mV** (`scale −16`);
- **3900 MHz** (preset *Turbo*) a ~**1199 mV** (`scale −24`);
- **4.0 GHz** (preset *Crazy*) validati a ~**1224 mV** (`scale −36`) per 120 s di stress continuo, picco **83 °C** — il massimo utile su questo esemplare;
- **Vid massimo invalicabile: 1.325 V** (mai superato).

L'**undervolt** non serve a "spingere" ma a fare lo stesso lavoro con **meno calore e meno consumo**: a parità di frequenza, abbassare la tensione finché resta stabile abbassa la temperatura e lascia margine termico al resto dell'APU.

### Accoppiamento termico CPU↔GPU

CPU e GPU condividono lo **stesso die** e lo **stesso budget di potenza**. Sotto carico **misto** (gioco impegnativo: CPU + GPU insieme) l'APU si autoprotegge e la CPU scende spontaneamente a ~**3450 MHz** per stare nel budget e sotto gli 85 °C. **Non è un difetto**: è il chip che si protegge cedendo i clock meno utili. Per lo stesso motivo un undervolt sulla CPU lascia più "spazio" termico alla GPU, e viceversa.

## Le 40 Compute Unit — a caldo

La BC-250 ha **40 CU** (20 WGP, 1 WGP = 2 CU), ma il driver ne attiva di default **24**. SkillFishOS le instrada fino a 40 **a runtime, senza riavvio**: il sistema parte alla baseline driver (24 CU) e un servizio porta a 40 all'avvio; dal [Tuner](/docs/app-native) regoli la quantità **a caldo** con una griglia di quadratini e i preset 24/32/40. Le prime 24 CU sono bloccate dal driver e restano sempre attive.

Con le 40 CU attive la GPU misura **11385 GFLOPS** FP32 (vkpeak) da freddo, contro i ~**6141** di una baseline a 24 CU: **+85%**. Sotto stress prolungato (a caldo) si assesta intorno a **10214 GFLOPS**. La banda di memoria misurata (clpeak) è **~350–367 GB/s**.

> 🔬 **Lotteria del silicio.** Su esemplari "discarto" qualche CU può essere marginale. Il [Tuner](/docs/app-native) ha un **«Test CU»** che mette sotto sforzo ogni coppia e segnala errori/blocchi GPU, così verifichi che il tuo chip regga le 40 CU. (Meccanismo via `umr`, scrittura delle mask WGP — credito a [bc250-cu-live-manager](https://github.com/WinnieLV/bc250-cu-live-manager), reimplementato clean-room.)

## Protezione termica — il cap a 85 °C

Il tetto termico è **85 °C** ed è applicato su due livelli:

1. **lato SMU**: il valore `max_temperature` nella configurazione fa sì che il chip riduca i clock *prima* di superare gli 85 °C (evitando il throttling brusco);
2. **lato sistema**: un **thermal-guard** (watchdog) che, se la temperatura supera il cap, abbassa di 100 MHz alla volta finché rientra.

Cose da sapere sul raffreddamento di serie (vedi anche [hardware BC-250](/docs/hardware-bc250) per **case 3D e ventole consigliate**):

- il dissipatore di serie è **marginale**: i confronti di benchmark "back-to-back" sono falsati dall'*heat-soak* — lascia raffreddare la scheda alcuni minuti tra una prova e l'altra;
- esiste solo il sensore *edge* della GPU; **nessun sensore per la VRAM**;
- la banda di memoria è sana ma il `mclk` **non** è regolabile.

## Un caso pratico: giochi CPU-bound

Alcuni titoli — come *Black Myth: Wukong* in **gameplay** — sono **CPU/draw-call bound**: gli FPS dipendono poco dalla risoluzione e dal clock della GPU. Lì aiutano l'overclock **CPU** e un buon raffreddamento. Per l'upscaling, FSR 4 **non è disponibile** (è hardware RDNA 4); si usano gamescope (FSR1/NIS) o [OptiScaler](https://github.com/optiscaler/OptiScaler) per-gioco.

Quando invece il carico **è** GPU-bound (es. il *flythrough* del benchmark di Wukong), il clock conta: nel **Tuner** puoi attivare la **modalità governor "Performance"**, che tiene la GPU al suo safe-point massimo sotto carico (a riposo torna comunque a 350 MHz). Misurato nel benchmark di Wukong: **100 → 111 FPS di media (+11%)**, 92 → 102 sui frame più lenti. Per sicurezza il Tuner limita la GPU a **2200 MHz @ 1000 mV** (massimo stabile su raffreddamento stock) con una curva di voltaggio multi-punto — spingere a 2230 MHz a 1000 mV è sotto-voltato e può bloccare la macchina.

## Tutto questo, senza terminale

Frequenze, undervolt, ventola e Compute Unit si regolano dalla GUI **Tuner**, con i quattro preset pronti, **test automatico e rollback** se la tua scheda non regge un valore — vedi [App native](/docs/app-native). È il modo consigliato: parti da Stock, sali a Performance, prova Turbo o Crazy, e il Tuner valida tutto sulla **tua** BC-250.

## Fonti

- [cyan-skillfish-governor (Magnap)](https://github.com/Magnap/cyan-skillfish-governor) — governor SMU GPU
- [bc250_smu_oc (bc250-collective)](https://github.com/bc250-collective/bc250_smu_oc) — overclock/undervolt CPU via SMU
- [bc250.info](https://bc250.info) — safe-point e note termiche della comunità
- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) — benchmark FP32 e banda memoria

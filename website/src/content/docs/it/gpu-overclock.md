---
title: GPU, CPU, overclock e undervolt
description: Come SkillFishOS controlla frequenze, tensioni e temperature della BC-250 — con i dati reali misurati sull'hardware.
group: Sistema
order: 2
---

Su una APU normale le frequenze si regolano via sysfs `amdgpu`. Sulla BC-250 **non funziona così**: il controllo passa per l'**SMU** (System Management Unit) e richiede strumenti dedicati. SkillFishOS li integra tutti, già configurati con una curva sicura e un sistema di protezione termica.

> **Attenzione:** **Silicon lottery.** Tutti i valori di questa pagina sono **misurati sulla nostra BC-250**. Ogni esemplare è diverso: una scheda può reggere una curva più spinta, un'altra meno. Per questo SkillFishOS **parte con la curva di serie** (preset **Performance**, tetto 2100 MHz) e ti lascia cambiarla dal [Tuner](/docs/control-center), che prova ogni curva **sulla tua scheda** con un test automatico di 25 secondi e torna indietro da sola se non regge.

## La curva tensione/frequenza e i tre preset

![la curva tensione/frequenza nel Tuner, con la tabella dei punti e i tre preset](/img/control-center-tuner.png)

Il [Tuner](/docs/control-center) governa la GPU con una **curva tensione/frequenza**: MHz in orizzontale, millivolt in verticale, punti che si trascinano nel grafico o si scrivono a mano nella tabella accanto. Tre preset spostano il **tetto** della curva:

| Preset | Tetto GPU | Note |
|---|---|---|
| **Cautious** | 1850 MHz | Il punto dolce col dissipatore di serie: quasi gli stessi fotogrammi, dieci gradi in meno |
| **Balanced** | 2000 MHz | Compromesso fra clock e calore |
| **Performance** | 2100 MHz | La curva a quindici punti misurata sulla scheda di sviluppo: quella che spediamo di default |

**Applica è una prova, non una scrittura immediata.** Una curva che chiede troppo poca tensione pianta la scheda, e sulla BC-250 un blocco si risolve solo staccando la corrente. Per questo Applica tiene la curva precedente ancora su disco, prova la candidata per **25 secondi** e aspetta conferma: premi Tieni e viene scritta per davvero; altrimenti — o se la scheda si blocca e riparte da sola — all'avvio torna la curva di prima.

## Il governor V/F della GPU

Le frequenze GPU sono gestite da **skillfish-vf-governor**, il nostro servizio che toglie il clock e la tensione al governor di serie e li pilota direttamente via SMU, tenendo un **tetto di frequenza** che calore e potenza possono abbassare e, quando la scheda si è calmata, restituire. Un processo separato, **skillfish-vf-watchdog**, tiene la situazione sotto controllo se il governor si pianta con il clock forzato.

Misurato su *Black Myth: Wukong*, stessa sessione, stessi 84 °C in entrambi i bracci: **+4,5%** a scheda fredda, **+11%** a scheda calda rispetto al governor di serie. Il vantaggio cresce con la temperatura perché il governor di serie cede clock scaldandosi, il nostro no.

> Il sysfs amdgpu standard (`power_dpm_force_performance_level`, `pp_dpm_sclk`) **non** controlla la BC-250: solo skillfish-vf-governor lo fa. La GPU sale al tetto solo sotto **saturazione grafica** reale.

## Overclock e undervolt della CPU

La CPU (**8 core / 16 thread** Zen 2 "Oberon", due sbloccati da SkillFishOS via SMU — anche prima dell'avvio, con un programma EFI, in un solo riavvio) è gestita per l'overclock da un servizio one-shot **`bc250-smu-oc.service`** che applica i valori da `/etc/bc250-smu-oc.conf` tramite il progetto [bc250_smu_oc](https://github.com/bc250-collective/bc250_smu_oc). Risulta *inactive* dopo l'applicazione: è normale (è "one-shot").

Cosa abbiamo misurato spingendo la **nostra** scheda:

- **3700 MHz** con undervolt a ~**1106 mV** (`scale −16`);
- **3900 MHz** a ~**1199 mV** (`scale −24`);
- **4.0 GHz** validati a ~**1224 mV** (`scale −36`) per 120 s di stress continuo, picco **83 °C** — il massimo utile su questo esemplare;
- **Vid massimo invalicabile: 1.325 V** (mai superato).

L'**undervolt** non serve a "spingere" ma a fare lo stesso lavoro con **meno calore e meno consumo**: a parità di frequenza, abbassare la tensione finché resta stabile abbassa la temperatura e lascia margine termico al resto dell'APU.

### Accoppiamento termico CPU↔GPU

CPU e GPU condividono lo **stesso die** e lo **stesso budget di potenza**. Sotto carico **misto** (gioco impegnativo: CPU + GPU insieme) l'APU si autoprotegge e la CPU scende spontaneamente a ~**3450 MHz** per stare nel budget e sotto gli 85 °C. **Non è un difetto**: è il chip che si protegge cedendo i clock meno utili. Per lo stesso motivo un undervolt sulla CPU lascia più "spazio" termico alla GPU, e viceversa.

## Le 40 Compute Unit — a caldo

La BC-250 ha **40 CU** (20 coppie), ma il driver ne attiva di default **24**. SkillFishOS le porta fino a 40 **all'avvio, senza intervento**; dal [Tuner](/docs/control-center) regoli la quantità **a caldo** scrivendo il numero desiderato o cliccando sulle 20 caselle a coppie. Le prime 24 CU sono bloccate dal driver e restano sempre attive.

Con le 40 CU attive la GPU misura **11385 GFLOPS** FP32 (vkpeak) da freddo, contro i ~**6141** di una baseline a 24 CU: **+85%**. Sotto stress prolungato (a caldo) si assesta intorno a **10214 GFLOPS**. La banda di memoria misurata (clpeak) è **~350–367 GB/s**.

> **Lotteria del silicio.** Su esemplari "discarto" qualche CU può essere marginale. Il [Tuner](/docs/control-center) ha un **«Test CU»** che mette sotto sforzo ogni coppia con vkpeak e segnala errori/blocchi GPU, così verifichi che il tuo chip regga le 40 CU. (Meccanismo via `umr`, scrittura delle mask WGP — credito a [bc250-cu-live-manager](https://github.com/WinnieLV/bc250-cu-live-manager), reimplementato clean-room.)

## Protezione termica — il cap a 85 °C

Il tetto termico è **85 °C** ed è applicato su due livelli:

1. **lato governor**: `gradi_max` e `watt_max` in `/etc/skillfish-vf-governor.json` fanno scendere il tetto di frequenza *prima* di superare gli 85 °C o il limite di potenza (il nostro, non quello del firmware), e lo restituiscono quando la scheda si è calmata;
2. **lato sistema**: **skillfish-vf-watchdog**, un processo separato che tiene la situazione sotto controllo se il governor si pianta con il clock forzato.

Cose da sapere sul raffreddamento di serie (vedi anche [hardware BC-250](/docs/hardware-bc250) per **case 3D e ventole consigliate**):

- il dissipatore di serie è **marginale**: i confronti di benchmark "back-to-back" sono falsati dall'*heat-soak* — lascia raffreddare la scheda alcuni minuti tra una prova e l'altra;
- esiste solo il sensore *edge* della GPU; **nessun sensore per la VRAM**;
- la banda di memoria è sana ma il `mclk` **non** è regolabile.

## Un caso pratico: giochi CPU-bound

Alcuni titoli — come *Black Myth: Wukong* in **gameplay** — sono **CPU/draw-call bound**: gli FPS dipendono poco dalla risoluzione e dal clock della GPU. Lì aiutano l'overclock **CPU** e un buon raffreddamento. Per l'upscaling, FSR 4 passa da [OptiScaler](https://github.com/optiscaler/OptiScaler) sul percorso DLSS del gioco (vedi [Gaming](/docs/gaming)).

Quando invece il carico **è** GPU-bound (es. il *flythrough* del benchmark di Wukong), il tetto della curva conta: nel [Tuner](/docs/control-center) alza il preset da Cautious o Balanced a **Performance** (2100 MHz), oppure scrivi una curva tua. Il vantaggio misurato su Wukong contro il vecchio governor di serie è **+4,5% a scheda fredda e +11% a scheda calda**: il governor V/F non cede clock scaldandosi, dove quello di serie lo fa. Resta comunque un limite fisico invalicabile: **1129 mV**, il tetto di tensione che amdgpu dichiara per questa GPU — nessuna curva può superarlo.

## Tutto questo, senza terminale

Frequenze, curva GPU, ventola e Compute Unit si regolano dalla GUI **Tuner**, con i tre preset della GPU pronti, **prova automatica di 25 secondi e ritorno alla curva precedente** se la tua scheda non la regge — vedi [Control Center](/docs/control-center). È il modo consigliato: parti da Cautious, sali a Balanced o Performance, e il Tuner valida tutto sulla **tua** BC-250.

## Fonti

- skillfish-vf-governor — il nostro governor V/F per la GPU, SMU diretto con tetto configurabile
- [bc250_smu_oc (bc250-collective)](https://github.com/bc250-collective/bc250_smu_oc) — overclock/undervolt CPU via SMU
- [bc250.info](https://bc250.info) — safe-point e note termiche della comunità
- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) — benchmark FP32 e banda memoria

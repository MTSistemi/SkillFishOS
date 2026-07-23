---
title: App native — Tuner e AI
description: Gli strumenti grafici di SkillFishOS per controllare l'hardware e l'AI senza terminale.
group: Uso
order: 3
---

SkillFishOS include due applicazioni native (scritte in **PyQt6**, tematizzate con Kvantum) che mettono in mano all'utente il controllo dell'hardware e dello stack AI **senza toccare il terminale**.

## SkillFishOS Tuner

Il **Tuner** è il pannello di controllo dell'hardware. Permette di regolare:

- **overclock e undervolt della CPU**;
- **safe-point della GPU** (tramite il governor SMU, vedi [GPU e overclock](/docs/gpu-overclock));
- la **ventola** (controllo PWM);
- la **VRAM UMA** (richiede riavvio);
- le **Compute Unit a caldo** — vedi sotto.

### Compute Unit a caldo (griglia)

Il Tuner mostra le CU della GPU come una **griglia di quadratini** (4 file SE/SH × 5 WGP): **verde = attiva, rosso = spenta**. Le puoi accendere/spegnere **a caldo, senza riavvio** — con un clic sulle coppie (1 WGP = 2 CU) o con i **preset 24 / 32 / 40 CU** — poi *Applica*. Le prime 24 CU sono il minimo del driver e restano sempre attive (vedi [GPU e overclock](/docs/gpu-overclock)).

![SkillFishOS Tuner — griglia delle Compute Unit a caldo, preset e Test CU](/img/tuner.jpg)

### Test CU (lotteria del silicio)

Il pulsante **«Test CU»** verifica la salute delle CU extra: attiva ogni coppia da sola, la mette sotto sforzo con **vkpeak** e controlla **errori/blocchi della GPU**, più uno stress finale a 40 CU. Serve a scovare **CU difettose** su esemplari "discarto", così sai se la tua APU regge le 40 CU piene.

![Risultato del Test CU — tutte le coppie OK, 40 CU stabili a 11380 GFLOPS, nessun difetto](/img/cu-test.jpg)

### Flusso "Test" e monitor live

Il flusso **"Test"** (CPU, GPU, CU, ventola): applica una modifica → esegue un benchmark → **verifica** la stabilità e, se qualcosa non va, fa il **rollback** automatico. All'avvio di ogni test si apre una **finestra Monitor** con i grafici in tempo reale di **temperatura, frequenza, voltaggio e ventola** (chiudibile a piacere).

![Finestra Monitor del Tuner — grafici live di temperatura, frequenza, voltaggio GPU e ventola durante un test](/img/monitor.jpg)

Architettura: una GUI utente più un piccolo **daemon di root** che esegue le operazioni privilegiate. Su un PC personale è configurato per non richiedere password a ogni operazione. L'HUD del desktop mostra anche le **CU attive** in tempo reale.

### Modalità del governor: Bilanciata e Performance

La GPU della BC-250 è pilotata da un **governor SMU** che alza e abbassa il clock in base al carico. Il Tuner espone due modalità con un interruttore:

- **Bilanciata** *(default)* — il clock scende a riposo (fino a 350 MHz) e sale sotto carico: consumi e temperature più bassi nell'uso normale.
- **Performance** — la GPU **resta agganciata al clock massimo** appena c'è carico, eliminando le micro-oscillazioni di frequenza. Nel nostro benchmark su *Black Myth: Wukong* questo vale **+11% di FPS** (da ~100 a ~111 di media) e un **1% low** più alto (92 → 102), a parità di tutto il resto.

Entrambe restano sotto il **cap termico di 85 °C**: la modalità Performance spinge di più, non disattiva le protezioni.

### Trova il massimo (wizard CPU e GPU)

Ogni BC-250 è diversa ([lotteria del silicio](/docs/gpu-overclock)). Il Tuner include due procedure guidate **«Trova il massimo»** che caratterizzano **la tua** scheda:

- **GPU** — sale a passi (2000 → 2200 MHz, step 50) applicando e **testando** ogni gradino, e si ferma all'ultimo stabile.
- **CPU** — percorre i gradini frequenza/undervolt (da 3600 MHz fino a 4000 MHz @ scale −36) con lo stesso schema **test-and-rollback**: se un passo non regge, torna all'ultimo valore buono.

Tutto è **crash-safe**: il valore di lavoro su disco resta sempre l'ultimo stabile, così un eventuale blocco a metà test non lascia la scheda su un profilo instabile al riavvio.

### Il mio silicio

Il pannello **«Il mio silicio»** riassume il profilo della tua scheda — CPU e GPU massimi trovati, CU sane, contatore dei freeze rilevati — e ti permette di **condividere il risultato in forma anonima** nel database della lotteria del silicio (apre una *issue* GitHub precompilata). Più dati raccogliamo, migliori diventano i profili consigliati per tutti.

## SkillFishOS Telemetry

**Telemetry** mostra in tempo reale temperatura, frequenza, carico CPU/GPU, voltaggi, assorbimento e ventola. Si apre automaticamente durante i test del Tuner, ma è anche un'app a sé. Il pulsante **REC** registra una sessione di benchmark in un file **`.sfmon`** (in `~/SkillFishOS-benchmarks/`): riaprendolo, Telemetry diventa un **analizzatore** con scrubber temporale per rivedere la run secondo per secondo.

![SkillFishOS Telemetry — grafici live di temperatura, frequenza, voltaggio GPU e ventola, con registrazione REC](/img/monitor.jpg)

## SkillFishOS AI

Il **pannello AI** accende e spegne lo stack LLM locale con un clic, liberando GPU e RAM per i giochi quando non serve. È il front-end "facile" dello stack descritto in [AI in locale](/docs/ai-locale).

![Pannello AI di SkillFishOS — motore LLM locale (Qwen3 14B) su GPU Vulkan, acceso/spento con un clic](/img/ai-panel.jpg)

## Perché esistono

L'obiettivo di SkillFishOS è che **chiunque** — compresi i più piccoli — possa usare e regolare il sistema senza dover imparare comandi da terminale. Queste app traducono operazioni complesse (governor SMU, parametri del kernel, container Docker) in pochi clic, mantenendo le **protezioni** (thermal-guard, test-and-rollback) sempre attive.

## Fonti

- [PyQt6 / Qt for Python](https://doc.qt.io/qtforpython/) · [Kvantum](https://github.com/tsujan/Kvantum)
- [sysbench](https://github.com/akopytov/sysbench) · [vkpeak](https://github.com/nihui/vkpeak)
- Repository del progetto — [github.com/MTSistemi/SkillFishOS](https://github.com/MTSistemi/SkillFishOS) (`apps/tuner`, `apps/ai-panel`)

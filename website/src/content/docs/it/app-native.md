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

Il Tuner mostra le CU della GPU come una **griglia di quadratini** (4 file SE/SH × 5 WGP): **verde = attiva, rosso = spenta**. Le puoi accendere/spegnere **a caldo, senza riavvio** — con un clic sulle coppie (1 WGP = 2 CU) o con i **preset 24 / 32 / 40 CU** — poi *Applica a caldo*. Le prime 24 CU sono il minimo del driver e restano sempre attive (vedi [GPU e overclock](/docs/gpu-overclock)).

### Test CU (lotteria del silicio)

Il pulsante **«Test CU»** verifica la salute delle CU extra: attiva ogni coppia da sola, la mette sotto sforzo con **vkpeak** e controlla **errori/blocchi della GPU**, più uno stress finale a 40 CU. Serve a scovare **CU difettose** su esemplari "discarto", così sai se la tua APU regge le 40 CU piene.

### Flusso "Test" e monitor live

Il flusso **"Test"** (CPU, GPU, CU, ventola): applica una modifica → esegue un benchmark → **verifica** la stabilità e, se qualcosa non va, fa il **rollback** automatico. All'avvio di ogni test si apre una **finestra Monitor** con i grafici in tempo reale di **temperatura, frequenza, voltaggio e ventola** (chiudibile a piacere).

Architettura: una GUI utente più un piccolo **daemon di root** che esegue le operazioni privilegiate. Su un PC personale è configurato per non richiedere password a ogni operazione. L'HUD del desktop mostra anche le **CU attive** in tempo reale.

## SkillFishOS AI

Il **pannello AI** accende e spegne lo stack LLM locale con un clic, liberando GPU e RAM per i giochi quando non serve. È il front-end "facile" dello stack descritto in [AI in locale](/docs/ai-locale).

## Perché esistono

L'obiettivo di SkillFishOS è che **chiunque** — compresi i più piccoli — possa usare e regolare il sistema senza dover imparare comandi da terminale. Queste app traducono operazioni complesse (governor SMU, parametri del kernel, container Docker) in pochi clic, mantenendo le **protezioni** (thermal-guard, test-and-rollback) sempre attive.

## Fonti

- [PyQt6 / Qt for Python](https://doc.qt.io/qtforpython/) · [Kvantum](https://github.com/tsujan/Kvantum)
- [sysbench](https://github.com/akopytov/sysbench) · [vkpeak](https://github.com/nihui/vkpeak)
- Repository del progetto — [github.com/MTSistemi/SkillFishOS](https://github.com/MTSistemi/SkillFishOS) (`apps/tuner`, `apps/ai-panel`)

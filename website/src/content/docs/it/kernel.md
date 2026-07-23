---
title: Il kernel su misura
description: Il kernel linux-tkg patchato per la BC-250, i parametri di avvio e i kernel da evitare.
group: Sistema
order: 1
---

Il cuore delle ottimizzazioni di SkillFishOS è un **kernel costruito su misura** per la BC-250, basato su [linux-tkg](https://github.com/Frogging-Family/linux-tkg) — una ricetta di compilazione della *Frogging Family* che applica patch orientate alle prestazioni e al gaming.

## Versione e patch

Il kernel di SkillFishOS è la versione **`7.0.10-skillfishos`**. Oltre alle patch standard di linux-tkg include:

- la **patch di sblocco frequenze** della BC-250 (range 350–2230 MHz);
- la **patch 40-CU** che abilita tutte le Compute Unit della GPU;
- una patch custom **RDSEED-quiet** che silenzia un messaggio rumoroso del kernel su questo hardware.

Il pacchetto del kernel (immagine + headers) viene pubblicato come release ed è **bloccato** (`apt-mark hold`) per evitare che un aggiornamento di Debian lo sostituisca con un kernel non adatto. È il kernel di default in GRUB.

## Parametri di avvio (cmdline)

La riga di comando del kernel è configurata così, e ogni parametro ha un motivo preciso:

```
mitigations=off
amdgpu.gttsize=6144
ttm.pages_limit=4194304
ttm.page_pool_size=4194304
video=DP-1:e
```

| Parametro | Cosa fa |
|---|---|
| `mitigations=off` | disattiva le mitigazioni Spectre/Meltdown per massimizzare le prestazioni (scelta accettabile su una console di casa) |
| `amdgpu.gttsize=6144` | estende il GTT → Vulkan vede ~13 GiB di memoria (utile per l'AI) |
| `ttm.pages_limit` / `ttm.page_pool_size` | alzano i limiti del gestore di memoria TTM coerentemente col GTT ampliato |
| `video=DP-1:e` | **forza l'abilitazione** del connettore DisplayPort (l'HPD è rotto, vedi [hardware](/docs/hardware-bc250)) |

> **Compute Unit a caldo.** SkillFishOS **non** usa più il parametro `amdgpu.bc250_cc_write_mode=3` (che bloccava 40 CU al boot e impediva i cambi a runtime). Ora il sistema parte alla baseline driver (24 CU) e un servizio instrada le **40 CU a caldo** all'avvio; puoi cambiarle senza riavvio dal [Tuner](/docs/app-native). Vedi [GPU e overclock](/docs/gpu-overclock).

## Kernel da evitare

Non tutti i kernel recenti vanno bene su questo hardware. In particolare sono noti problemi con le serie **6.15.0–6.15.6** e **6.17.8–6.17.10**: vanno evitate. SkillFishOS distribuisce il proprio kernel testato proprio per non incappare in queste regressioni — vedi [Aggiornamenti](/docs/aggiornamenti).

## IOMMU

Come ricordato nella pagina [hardware](/docs/hardware-bc250), l'**IOMMU non va mai abilitato** sulla BC-250: è instabile. Il kernel parte sempre con l'IOMMU disattivato.

## Perché un kernel proprio e non XanMod o lo stock

- Il **kernel stock Debian** non contiene le patch BC-250 (sblocco frequenze, 40 CU) e segue le regressioni di cui sopra.
- **linux-tkg** permette di applicare facilmente le patch custom e di scegliere scheduler e opzioni orientate al gaming.
- Compilando noi possiamo aggiornare il kernel **solo quando una nuova versione porta benefici reali** e dopo averla testata sul ferro.

## Fonti

- [linux-tkg (Frogging-Family)](https://github.com/Frogging-Family/linux-tkg)
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock)
- [Parametri del driver amdgpu](https://docs.kernel.org/gpu/amdgpu/module-parameters.html)
- [bc250.info](https://bc250.info) — note su kernel e cmdline

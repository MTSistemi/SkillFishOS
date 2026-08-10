---
title: AI in locale
description: Il motore AI locale accelerato in Vulkan sulla GPU della BC-250 — Unsloth Studio, con i modelli GGUF di Hugging Face.
group: Uso
order: 2
---

SkillFishOS include uno stack di **intelligenza artificiale locale**: modelli di chat e coding che girano interamente sulla GPU della BC-250, **senza cloud** e senza inviare dati all’esterno. Si accende e spegne con un clic, così da liberare GPU e RAM quando vuoi giocare.

![Pannello AI di SkillFishOS — accende e spegne il motore LLM locale accelerato in Vulkan](/img/ai-panel.jpg)

## Perché Vulkan e non ROCm

Lo stack AMD "ufficiale" per il calcolo è **ROCm**, ma **non supporta la `gfx1013`** della BC-250. SkillFishOS usa quindi il backend **Vulkan** con i driver Mesa/RADV: sfrutta la GPU integrata e la memoria condivisa (col GTT esteso, vedi [GPU](/docs/gpu-overclock)).

**Quanto conta.** Misurato sulla scheda con Qwen3-1.7B Q4_K_M:

| | solo CPU | GPU via Vulkan | |
|---|---:|---:|---|
| Generazione | 41,5 tok/s | **210,7 tok/s** | **5,1×** |
| Elaborazione del prompt | 9,2 tok/s | **157,2 tok/s** | **17×** |

## Il motore: Unsloth Studio

Dalla versione 26.08 il motore è **[Unsloth Studio](https://unsloth.ai/)**, che sostituisce il precedente stack Ollama + OpenWebUI in Docker. È un **servizio nativo unico** che offre insieme l’interfaccia di chat e un’**API compatibile OpenAI**, in ascolto su `127.0.0.1:8888`.

Cosa cambia in pratica:

- **Un servizio invece di uno stack Docker.** Prima servivano tre container (Ollama, OpenWebUI, Dockge) e un’immagine custom da ~6,5 GB; ora c’è `skillfish-unsloth.service` e basta.
- **I modelli sono quelli di Hugging Face.** Unsloth scarica direttamente i **GGUF** dal catalogo completo di Hugging Face, invece di un registro curato: la scelta di modelli e di quantizzazioni disponibili è enormemente più ampia, comprese le build che il team Unsloth pubblica per conto proprio.
- **Ascolta solo su localhost.** Da fuori ci si arriva attraverso la dashboard, che autentica via PAM: nessuna porta AI esposta sulla rete.

> Le installazioni più vecchie con Ollama continuano a funzionare: la dashboard riconosce da sola quale motore è presente e adatta i comandi. Il rilevamento non richiede configurazione.

## I modelli

I modelli si scaricano **dentro Unsloth Studio**, dalla sua interfaccia. Regola pratica su questa scheda: i 16 GB di GDDR6 sono condivisi tra sistema e GPU, quindi conviene stare sotto gli ~11 GB di pesi per lasciare respiro al resto.

## Accensione/spegnimento

Un **pannello AI** dedicato (app nativa, vedi [App native](/docs/app-native)) accende e spegne il motore con un clic; lo stesso interruttore c’è nella [dashboard web](/docs/controllo-remoto). Tieni presente che:

- **AI e giochi non vanno usati insieme**: condividono la stessa GPU e la stessa memoria;
- a motore spento, GPU e RAM tornano completamente disponibili per il gaming.

## Fonti

- [Unsloth](https://unsloth.ai/) · [llama.cpp](https://github.com/ggml-org/llama.cpp) · [Hugging Face](https://huggingface.co/)
- [Mesa / RADV (driver Vulkan)](https://docs.mesa3d.org/drivers/radv.html)
- [ROCm — hardware supportato](https://rocm.docs.amd.com/) (la `gfx1013` non è in elenco)

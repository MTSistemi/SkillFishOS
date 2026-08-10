---
title: On-device AI
description: The local AI engine, Vulkan-accelerated on the BC-250 GPU — Unsloth Studio, with GGUF models from Hugging Face.
group: Usage
order: 2
---

SkillFishOS ships a **local AI** stack: chat and coding models running entirely on the BC-250 GPU, **no cloud**, nothing sent outside. One click turns it on and off, so GPU and RAM are free again when you want to play.

![SkillFishOS AI panel — turns the Vulkan-accelerated local LLM engine on and off](/img/ai-panel.jpg)

## Why Vulkan and not ROCm

AMD’s "official" compute stack is **ROCm**, but it **does not support the BC-250’s `gfx1013`**. SkillFishOS therefore uses the **Vulkan** backend with the Mesa/RADV drivers: it makes full use of the integrated GPU and the shared memory (with the extended GTT, see [GPU](/en/docs/gpu-overclock)).

**How much it matters.** Measured on the board with Qwen3-1.7B Q4_K_M:

| | CPU only | GPU over Vulkan | |
|---|---:|---:|---|
| Generation | 41.5 tok/s | **210.7 tok/s** | **5.1×** |
| Prompt processing | 9.2 tok/s | **157.2 tok/s** | **17×** |

## The engine: Unsloth Studio

Since 26.08 the engine is **[Unsloth Studio](https://unsloth.ai/)**, replacing the earlier Ollama + OpenWebUI Docker stack. It is a **single native service** providing both the chat UI and an **OpenAI-compatible API**, listening on `127.0.0.1:8888`.

What changes in practice:

- **One service instead of a Docker stack.** It used to take three containers (Ollama, OpenWebUI, Dockge) plus a ~6.5 GB custom image; now it is just `skillfish-unsloth.service`.
- **Models come from Hugging Face.** Unsloth pulls **GGUF** files straight from the full Hugging Face catalogue rather than a curated registry, so the range of available models and quantisations is vastly wider — including the builds the Unsloth team publishes themselves.
- **It listens on loopback only.** From outside you reach it through the dashboard, which authenticates over PAM: no AI port is exposed to the network.

> From 26.06.3 the dashboard and the AI panel drive **only** Unsloth: the branches that commanded Ollama through Docker are gone, and so is Docker itself, which is no longer installed. Anyone still holding Ollama containers from an earlier install keeps them running as long as they keep Docker, but no longer manages them from here. No configuration needed.

## Models

Models are downloaded **inside Unsloth Studio**, from its own interface. Rule of thumb on this board: the 16 GB of GDDR6 are shared between system and GPU, so staying under ~11 GB of weights leaves room for everything else.

## Turning it on and off

A dedicated **AI panel** (native app, see [Native apps](/en/docs/app-native)) starts and stops the engine with one click; the same switch is in the [web dashboard](/en/docs/controllo-remoto). Bear in mind:

- **AI and games should not run together**: they share the same GPU and the same memory;
- with the engine off, GPU and RAM are fully available for gaming again.

## Sources

- [Unsloth](https://unsloth.ai/) · [llama.cpp](https://github.com/ggml-org/llama.cpp) · [Hugging Face](https://huggingface.co/)
- [Mesa / RADV (Vulkan driver)](https://docs.mesa3d.org/drivers/radv.html)
- [ROCm — supported hardware](https://rocm.docs.amd.com/) (`gfx1013` is not on the list)

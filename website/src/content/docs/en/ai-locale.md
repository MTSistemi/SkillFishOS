---
title: On-device AI
description: The local AI engine, Vulkan-accelerated on the BC-250 GPU — Unsloth Studio, with GGUF models from Hugging Face.
group: Usage
order: 2
---

SkillFishOS ships a **local AI** stack: chat and coding models running entirely on the BC-250 GPU, **no cloud**, nothing sent outside. One click turns it on and off, so GPU and RAM are free again when you want to play.

![The AI section of the Control Center: engine, models, memory and a chat test](/img/control-center-ai.png)

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


## Models

Models are **GGUF** files from the Hugging Face catalogue, and they come from two places: the **AI** section of the [Control Center](/en/docs/control-center), where you type the repository name (for example `unsloth/Qwen3-4B-GGUF`) and pick the variant from the list, sizes included; or the Hub inside Unsloth Studio, which has the search and the full model pages.

Rule of thumb on this board: the 16 GB of GDDR6 are shared between system and GPU, so staying under ~11 GB of weights leaves room for everything else.

## Switch, update and key

The **AI** section of the [Control Center](/en/docs/control-center) starts and stops the engine, enables it at boot and shows the version with a one-click update. The same is in the [Remote Manager](/en/docs/controllo-remoto), from a browser.

Unsloth generates a random password when it installs, and **shuts itself down after an hour** if that password is not changed. The AI section does that step for you: choose the Studio password and the API key is created with it. The key is how the window and the Remote Manager talk to the engine; the models on disk, the memory (VRAM, GTT, RAM, swap) and a chat test with the measured tokens per second sit next to it.

Bear in mind:

- **AI and games should not run together**: they share the same GPU and the same memory;
- with the engine off, GPU and RAM are fully available for gaming again.

## Sources

- [Unsloth](https://unsloth.ai/) · [llama.cpp](https://github.com/ggml-org/llama.cpp) · [Hugging Face](https://huggingface.co/)
- [Mesa / RADV (Vulkan driver)](https://docs.mesa3d.org/drivers/radv.html)
- [ROCm — supported hardware](https://rocm.docs.amd.com/) (`gfx1013` is not on the list)

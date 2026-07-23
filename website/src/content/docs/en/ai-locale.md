---
title: On-device AI
description: The Ollama + OpenWebUI stack accelerated in Vulkan on the BC-250's GPU.
group: Usage
order: 2
---

SkillFishOS includes a **local AI** stack: chat and coding models that run entirely on the BC-250's GPU, **with no cloud** and without sending data anywhere. It turns on and off with one click, so you free up GPU and RAM when you want to play.

![SkillFishOS AI panel — turns the local LLM engine (Qwen3 14B, Vulkan) on/off and opens web chat, Dockge or OpenCode](/img/ai-panel.jpg)

## Why Vulkan and not ROCm

AMD's "official" compute stack is **ROCm**, but it **does not support** the BC-250's `gfx1013`. SkillFishOS therefore uses the **Vulkan** backend of [Ollama](https://ollama.com/), with the Mesa drivers: it works well on the integrated GPU, leveraging the shared memory (and the extended GTT, see [GPU](/en/docs/gpu-overclock)).

## The components

| Component | Role |
|---|---|
| **[Ollama](https://ollama.com/)** (Vulkan backend) | runs the LLM models on the GPU |
| **[OpenWebUI](https://openwebui.com/)** | web chat interface (with web search) |
| **[Dockge](https://github.com/louislam/dockge)** | Docker stack management via web |

The stack runs in **Docker containers** with a custom image (Ollama + Mesa's Vulkan drivers). It is configured **not to start on its own** (`restart: "no"`), so it doesn't steal the GPU from games: you activate it when needed.

## The recommended model

The practical reference model is **`qwen3:14b`**: it runs 100% on the GPU (~10.7 GB) with the KV cache in **f16**.

> ⚠️ On this hardware (RADV driver) the `q4_0` quantization of the KV cache **corrupts the output**: use the **f16** cache.

## Turning it on/off

A dedicated **AI panel** (native app, see [Native apps](/en/docs/app-native)) turns the whole stack on and off with one click. Keep in mind:

- **AI and games/Android should not be used together**: they share the same GPU and memory;
- with the stack off, the GPU and RAM are fully available again for gaming.

## Sources

- [Ollama](https://ollama.com/) · [OpenWebUI](https://openwebui.com/) · [Dockge](https://github.com/louislam/dockge)
- [Mesa / RADV (Vulkan driver)](https://docs.mesa3d.org/drivers/radv.html)
- [ROCm — supported hardware](https://rocm.docs.amd.com/) (`gfx1013` is not listed)

# Local AI on the integrated GPU

The BC‑250's 16 GB of shared GDDR6 makes it a surprisingly capable local‑LLM box. SkillFishOS runs an **Ollama + OpenWebUI** stack accelerated in **Vulkan** on the integrated GPU, with a one‑click brass panel to start/stop it (so it gives the GPU back when you want to game).

## Why Vulkan, not ROCm

ROCm **does not support `GFX1013`** (no rocBLAS/Tensile), and forcing `HSA_OVERRIDE_GFX_VERSION` is unsafe (ISA mismatch → silent errors/crashes). The right path is **llama.cpp / Ollama on the RADV Vulkan backend**. The official Ollama image lacks Mesa Vulkan drivers, so SkillFishOS builds a small custom image adding `mesa-vulkan-drivers libvulkan1 vulkan-tools`.

## Memory tuning (critical)

By default TTM caps GPU‑addressable memory. SkillFishOS raises it on the kernel cmdline:

```
ttm.pages_limit=4194304 ttm.page_pool_size=4194304   # ~16 GB
amdgpu.gttsize=5120                                   # GTT, in MiB
```

With this, Vulkan sees **~13 GiB** (UMA VRAM + GTT) instead of just the VRAM split — enough to fit large models entirely on the GPU. All memory is the same GDDR6, so GTT runs at VRAM speed (no PCIe hop).

## The stack

Managed as a docker‑compose stack (via **Dockge**), `restart: "no"` so it never steals the GPU at boot:

- **Ollama** (Vulkan) on `:11434`, with `OLLAMA_FLASH_ATTENTION=1` and **`OLLAMA_KV_CACHE_TYPE=f16`**.
- **OpenWebUI** (ChatGPT‑style web chat) on `:8080`, optional DuckDuckGo web search.
- **OpenCode** (TUI coding agent) pointed at the local Ollama.

> ⚠️ **Do not use a quantized KV cache (`q4_0`) on RADV** — it corrupts output (gibberish). Use `f16`. The trade‑off is memory: f16 KV is larger, so the practical sweet‑spot models are a **14B** (chat, 100 % GPU) and a **7B coder** (32K context, 100 % GPU). A 30B MoE fits but is slow with a coherent (f16) cache.

## One‑click panel

The **SkillFish AI** panel (brass GTK4) toggles the whole stack: **ON** = `docker compose up -d`, **OFF** = `docker compose stop` (frees GPU + RAM). It shows status, the model in VRAM, and shortcuts to the web chat, Dockge and OpenCode. This is how "AI now, games later" stays a one‑click decision.

See [OPTIMIZATIONS.md §5](OPTIMIZATIONS.md#5-memory-split--vram-uma--gtt) for the memory split details.

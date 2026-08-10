# Local AI on the integrated GPU

The BC‑250's 16 GB of shared GDDR6 makes it a surprisingly capable local‑LLM box. SkillFishOS runs **Unsloth Studio** accelerated in **Vulkan** on the integrated GPU, with a one‑click brass panel to start/stop it (so it gives the GPU back when you want to game).

## Why Vulkan, not ROCm

ROCm **does not support `GFX1013`** (no rocBLAS/Tensile), and forcing `HSA_OVERRIDE_GFX_VERSION` is unsafe (ISA mismatch → silent errors/crashes). The right path is **llama.cpp on the RADV Vulkan backend**, which is exactly what Unsloth Studio ships.

Measured on the board with Qwen3‑1.7B Q4_K_M:

| | CPU only | GPU over Vulkan | |
|---|---:|---:|---|
| Generation | 41.5 tok/s | **210.7 tok/s** | **5.1×** |
| Prompt processing | 9.2 tok/s | **157.2 tok/s** | **17×** |

`UNSLOTH_FORCE_VULKAN=1` has to be set **before the installer runs**: it selects which llama.cpp bundle gets downloaded and cannot be changed at launch time.

## Memory tuning (critical)

By default TTM caps GPU‑addressable memory. SkillFishOS raises it on the kernel cmdline:

```
ttm.pages_limit=4194304 ttm.page_pool_size=4194304   # ~16 GB
amdgpu.gttsize=5120                                   # GTT, in MiB
```

With this, Vulkan sees **~13 GiB** (UMA VRAM + GTT) instead of just the VRAM split — enough to fit large models entirely on the GPU. All memory is the same GDDR6, so GTT runs at VRAM speed (no PCIe hop).

## The engine

`skillfish-unsloth.service` runs Unsloth Studio on `127.0.0.1:8888`. One native service provides **both** the chat UI and an **OpenAI‑compatible API**; it listens on loopback only, and remote access goes through the dashboard's PAM‑authenticated reverse proxy at `/unsloth`.

Models are **GGUF files pulled straight from Hugging Face** through Studio's own interface, rather than from a curated registry — a far wider choice of models and quantisations, including the builds the Unsloth team publishes themselves. On this board, keeping weights under ~11 GB leaves room for everything else.

The venv is built against **uv's bundled Python**, deliberately: an earlier install pointed at the system `python3.13`, and an `apt autoremove` that swept up the now‑orphaned interpreter left the service crash‑looping with `exec: .../bin/unsloth: not found` — the binary was there, the interpreter was not.

### Superseded: the Ollama + OpenWebUI stack

Earlier releases ran Ollama (`:11434`) plus OpenWebUI (`:8080`) as a docker‑compose stack with a custom Vulkan image. It still works and the dashboard **auto‑detects** which engine is present, so existing installs keep running untouched. Two notes if you are still on it: use `OLLAMA_FLASH_ATTENTION=1`, and **never** a quantized KV cache — `q4_0` corrupts output on RADV, use `f16`.

## One‑click panel

The **SkillFish AI** panel toggles the engine, and the same switch exists in the web dashboard's *AI locale* card. It shows engine status, Vulkan acceleration and a shortcut to the chat UI. This is how "AI now, games later" stays a one‑click decision — AI and games should not share the GPU.

See [OPTIMIZATIONS.md §5](OPTIMIZATIONS.md#5-memory-split--vram-uma--gtt) for the memory split details.

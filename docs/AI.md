# Local AI on the integrated GPU

The BC‑250's 16 GB of shared GDDR6 makes it a surprisingly capable local‑LLM box. SkillFishOS runs **Unsloth Studio** accelerated in **Vulkan** on the integrated GPU, controlled from the **AI** section of the Control Center — and mirrored in the Remote Manager — so it gives the GPU back when you want to game.

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
ttm.pages_limit=1572864 ttm.page_pool_size=1572864   # GTT ceiling: 4 KiB pages, so 1572864 = 6 GiB
```

With this, Vulkan sees **~13 GiB** (UMA VRAM + GTT) instead of just the VRAM split — enough to fit large models entirely on the GPU. All memory is the same GDDR6, so GTT runs at VRAM speed (no PCIe hop).

## The engine

`skillfish-unsloth.service` runs Unsloth Studio on `127.0.0.1:8888`. One native service provides **both** the chat UI and an **OpenAI‑compatible API**; it listens on loopback only, and remote access goes through the dashboard's PAM‑authenticated reverse proxy at `/unsloth`.

Models are **GGUF files pulled straight from Hugging Face** through Studio's own interface, rather than from a curated registry — a far wider choice of models and quantisations, including the builds the Unsloth team publishes themselves. On this board, keeping weights under ~11 GB leaves room for everything else.

The venv is built against **uv's bundled Python**, deliberately: an earlier install pointed at the system `python3.13`, and an `apt autoremove` that swept up the now‑orphaned interpreter left the service crash‑looping with `exec: .../bin/unsloth: not found` — the binary was there, the interpreter was not.

### Superseded: the Ollama + OpenWebUI stack

Earlier releases ran Ollama (`:11434`) plus OpenWebUI (`:8080`) as a docker-compose
stack with a custom Vulkan image, managed through Dockge.

As of 26.06.3 none of that is here any more. The Remote Manager and the Control
Center's AI section drive only Unsloth: every `docker compose` and `docker exec ollama` path was removed, and
Docker itself was uninstalled — it was running exactly one container, Dockge, whose
stack directory was empty once the AI moved to a native service. That is a daemon at
every boot, a bridge, iptables rules and a container-management panel listening on
`0.0.0.0:5001`, all for nothing.

An existing installation that still has Docker keeps its Ollama containers running;
they simply are not managed from our tools any more. New installations start with
Unsloth and nothing else.

## The AI section of the Control Center

Since 26.09.3, Unsloth Studio is managed from the **AI** section of the SkillFishOS
Control Center (`skillfish-control-center`, or the old `skillfish-ai-panel`
command, which now just opens this section). The same controls are mirrored in
the Remote Manager's *AI* card. This is how "AI now, games later" stays a
one‑click decision — AI and games should not share the GPU.

- **Engine**: on/off, and "at boot".
- **Version**: the installed Unsloth version, an update check, and a one‑click
  **Update** that reruns the official installer
  (`https://unsloth.ai/install.sh`, with `UNSLOTH_FORCE_VULKAN=1`) through
  `skillfish-unsloth-update`, in the user's home — never `/root`.
- **First sign‑in**: Unsloth generates a random initial password at install
  and shuts itself down after an hour if it isn't changed. The window lets
  the user pick the Studio password and creates the API key in the same
  step.
- **API key**: created from the Studio password, or pasted in. It is shared
  with the Remote Manager at `/etc/skillfish/unsloth.key` (root, mode 0600);
  the window keeps its own copy at `~/.config/skillfish/unsloth.key`.
- **Models**: what's on disk, with quantization and size; download GGUFs
  from the Hugging Face Hub by repository id (e.g. `unsloth/Qwen3-4B-GGUF`),
  with the available variants and their sizes listed.
- **Quick chat**: a small chat over the OpenAI‑compatible API
  (`http://127.0.0.1:8888/v1`) with measured tokens per second — for the
  full chat, Chat with Files (RAG), the Hub page, parallel chats and Deep
  Research, use Studio's own UI at `http://localhost:8888`.
- **Memory**: VRAM, GTT, RAM, swap and the model budget, plus a GTT limit
  slider — the kernel parameter `ttm.pages_limit`, applied after a reboot.
- **Network**: "reachable from the local network" sets `UNSLOTH_BIND=0.0.0.0`
  and `UNSLOTH_PARALLEL=<slots>` in `/etc/default/skillfish-unsloth`, read by
  `skillfish-unsloth.service`. Studio keeps its own login regardless.

See [OPTIMIZATIONS.md §5](OPTIMIZATIONS.md#5-memory-split--vram-uma--gtt) for the memory split details.

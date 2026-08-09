#!/bin/bash
# install-unsloth.sh — Unsloth Studio as the SkillFishOS on-device AI engine.
#
# Unsloth Studio runs GGUF models through llama.cpp with a **Vulkan** backend, which
# is the only GPU-accelerated path on the BC-250 (gfx1013 has no ROCm userspace).
# It replaces the previous Ollama + Open WebUI Docker stack with a single native
# service that provides both the chat UI and an OpenAI-compatible API.
#
# Measured on the board (Qwen3-1.7B Q4_K_M): 210 tok/s generation on Vulkan vs
# 41 tok/s CPU-only — a 5x speedup, and 17x on prompt processing.
#
# UNSLOTH_FORCE_VULKAN=1 must be set BEFORE the installer runs: it selects which
# llama.cpp binary bundle gets downloaded and cannot be changed at launch time.
#
# Run as root ON THE BOX:  sudo bash install-unsloth.sh
set -euo pipefail
PORT="${UNSLOTH_PORT:-8888}"
export HOME=/root
export UNSLOTH_FORCE_VULKAN=1

echo ">>> [1/4] Vulkan disponibile?"
if command -v vulkaninfo >/dev/null 2>&1; then
  vulkaninfo --summary 2>/dev/null | grep -m1 -i 'deviceName' || true
else
  echo "    (vulkaninfo assente — installo mesa-vulkan-drivers/vulkan-tools)"
  apt-get update -qq || true
  DEBIAN_FRONTEND=noninteractive apt-get install -y mesa-vulkan-drivers vulkan-tools || true
fi

echo ">>> [2/4] installo Unsloth Studio (backend Vulkan)"
if [ -x /root/.unsloth/studio/unsloth_studio/bin/unsloth ]; then
  echo "    già installato — aggiorno"
fi
curl -fsSL https://unsloth.ai/install.sh | sh

BIN=/root/.unsloth/studio/unsloth_studio/bin/unsloth
[ -x "$BIN" ] || { echo "FATAL: unsloth non installato" >&2; exit 1; }

echo ">>> [3/4] verifico che la GPU sia vista dal backend"
LLAMA=/root/.unsloth/llama.cpp/build/bin
if [ -x "$LLAMA/llama-server" ]; then
  (cd "$LLAMA" && LD_LIBRARY_PATH=. ./llama-server --list-devices 2>&1 | grep -i vulkan) \
    || echo "    ⚠️ nessun device Vulkan elencato — l'inferenza userà la CPU"
fi

echo ">>> [4/4] servizio systemd"
install -m0755 /dev/stdin /usr/local/bin/skillfish-unsloth <<EOF
#!/bin/sh
# Avvia Unsloth Studio con il backend Vulkan, in ascolto solo su localhost:
# l'accesso dalla LAN passa dalla dashboard (che autentica via PAM).
export HOME=/root
export UNSLOTH_FORCE_VULKAN=1
exec $BIN studio -p ${PORT} -H 127.0.0.1
EOF
cat > /etc/systemd/system/skillfish-unsloth.service <<EOF
[Unit]
Description=SkillFishOS — Unsloth Studio (on-device AI, Vulkan)
Documentation=https://unsloth.ai/docs
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/local/bin/skillfish-unsloth
Restart=on-failure
RestartSec=10
# l'inferenza non deve mai far morire di fame il desktop
Nice=5

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now skillfish-unsloth.service

echo "    attendo l'avvio..."
for i in $(seq 1 30); do
  sleep 2
  curl -fsS -m 2 "http://127.0.0.1:${PORT}/" >/dev/null 2>&1 && break
done
systemctl is-active skillfish-unsloth.service

cat <<EOF

=========================================================================
 Unsloth Studio attivo su http://127.0.0.1:${PORT}
   - UI di chat + API OpenAI-compatibile (/v1/chat/completions)
   - inferenza GGUF accelerata via Vulkan sulla GPU della BC-250
 Dalla LAN si raggiunge dalla dashboard SkillFishOS (login PAM).
 I modelli si scaricano dalla UI (i quant GGUF di unsloth sono consigliati).
=========================================================================
EOF

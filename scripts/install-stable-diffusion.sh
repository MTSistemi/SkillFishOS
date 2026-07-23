#!/bin/bash
# install-stable-diffusion.sh — SkillFishOS image generation on the BC-250 GPU.
#
# The BC-250 GPU (gfx1013 / Cyan Skillfish) has poor ROCm support, so we use
# stable-diffusion.cpp with its **Vulkan** backend (same path the community uses
# for working SD on this board). Produces a CLI `skillfish-sd "prompt" out.png`
# that the dashboard / AI Panel "Images" feature drives.
#
# Run as root ON THE BOX when it is free from gaming (build is CPU/GPU heavy):
#   sudo bash install-stable-diffusion.sh
# Optional: SD_MODEL_URL=... to use a different model (safetensors or GGUF).
set -euo pipefail
PREFIX=/opt/skillfish-sd
MODELS="$PREFIX/models"
JOBS="$(nproc)"
MODEL_URL="${SD_MODEL_URL:-https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors}"
MODEL_FILE="$MODELS/$(basename "${MODEL_URL%%\?*}")"

echo ">>> [0/5] controllo Vulkan sulla GPU"
if command -v vulkaninfo >/dev/null 2>&1; then
  vulkaninfo --summary 2>/dev/null | grep -iE "deviceName|GFX1013|BC-250" | head -2 || true
else
  echo "    (vulkaninfo assente: installo vulkan-tools per la diagnostica)"
fi

echo ">>> [1/5] dipendenze di build"
apt-get update
apt-get install -y --no-install-recommends \
  git cmake build-essential libvulkan-dev vulkan-tools libcurl4-openssl-dev
# glslc (shaderc) è richiesto dal backend Vulkan di ggml; fallback a glslang-tools
apt-get install -y --no-install-recommends glslc 2>/dev/null \
  || apt-get install -y --no-install-recommends glslang-tools

echo ">>> [2/5] sorgenti stable-diffusion.cpp"
mkdir -p "$PREFIX"
if [ -d "$PREFIX/src/.git" ]; then
  git -C "$PREFIX/src" pull --recurse-submodules --ff-only || true
  git -C "$PREFIX/src" submodule update --init --recursive
else
  git clone --recursive https://github.com/leejet/stable-diffusion.cpp "$PREFIX/src"
fi

echo ">>> [3/5] compilazione (Vulkan) — può richiedere alcuni minuti"
cmake -S "$PREFIX/src" -B "$PREFIX/build" -DSD_VULKAN=ON -DCMAKE_BUILD_TYPE=Release
cmake --build "$PREFIX/build" --config Release -j "$JOBS"
BIN="$(find "$PREFIX/build" -maxdepth 3 -name sd -type f -perm -u+x | head -1)"
[ -n "$BIN" ] || { echo "FATAL: binario 'sd' non trovato dopo la build" >&2; exit 1; }
install -m0755 "$BIN" /usr/local/bin/skillfish-sd-bin

echo ">>> [4/5] modello"
mkdir -p "$MODELS"
if [ ! -f "$MODEL_FILE" ]; then
  echo "    scarico $(basename "$MODEL_FILE") (~4 GB)…"
  curl -L --fail --retry 3 -o "$MODEL_FILE.part" "$MODEL_URL"
  mv "$MODEL_FILE.part" "$MODEL_FILE"
else
  echo "    modello già presente: $MODEL_FILE"
fi

echo ">>> [5/5] wrapper skillfish-sd"
cat > /usr/local/bin/skillfish-sd <<EOF
#!/bin/bash
# skillfish-sd "prompt" [output.png] [extra sd args…]
set -e
PROMPT="\${1:?uso: skillfish-sd \\"prompt\\" [out.png]}"
OUT="\${2:-/tmp/skillfish-sd.png}"
MODEL="\${SD_MODEL:-$MODEL_FILE}"
exec /usr/local/bin/skillfish-sd-bin -m "\$MODEL" -p "\$PROMPT" -o "\$OUT" \\
  --steps "\${SD_STEPS:-20}" -W "\${SD_W:-512}" -H "\${SD_H:-512}" --cfg-scale "\${SD_CFG:-7}" "\${@:3}"
EOF
chmod 0755 /usr/local/bin/skillfish-sd

echo
echo ">>> FATTO."
echo "    Prova:  skillfish-sd \"a steampunk brass mechanical fish, cinematic lighting\" /tmp/test.png"
echo "    Modelli in: $MODELS  (SD_MODEL_URL=… per un altro; per velocità su GPU debole usa un modello *turbo*)"
echo "    Poi nella dashboard aggiungeremo il modulo 'Immagini' che chiama skillfish-sd."

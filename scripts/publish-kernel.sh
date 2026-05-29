#!/bin/bash
# Publish the freshly-built linux-tkg BC-250 kernel .deb files as a GitHub Release
# asset on MTSistemi/AMD-BC-250, using the REST API (no gh CLI needed).
#
# Usage:
#   GITHUB_TOKEN=ghp_xxx ./publish-kernel.sh [TAG]
#
# Requires: curl, jq. A token with 'repo' (or 'contents:write') scope.
set -euo pipefail

REPO="MTSistemi/AMD-BC-250"
TAG="${1:-kernel-7.0.10-bc250}"
DEBS_DIR="${DEBS_DIR:-/root/linux-tkg/DEBS}"
API="https://api.github.com"
UPLOADS="https://uploads.github.com"

: "${GITHUB_TOKEN:?Set GITHUB_TOKEN (PAT with repo/contents:write scope)}"

AUTH=(-H "Authorization: Bearer ${GITHUB_TOKEN}" -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28")

echo ">>> Kernel .deb files to publish:"
mapfile -t DEBS < <(find "$DEBS_DIR" -maxdepth 1 -name '*.deb' ! -name '*-dbg_*' ! -name 'linux-libc-dev*' | sort)
if [ ${#DEBS[@]} -eq 0 ]; then
    echo "ERROR: no .deb files in $DEBS_DIR" >&2
    exit 1
fi
printf '  %s\n' "${DEBS[@]}"

# uname -r of the built kernel (from the image package name) for release notes
KVER=$(basename "$(printf '%s\n' "${DEBS[@]}" | grep -m1 linux-image)" | sed -E 's/linux-image-([^_]+)_.*/\1/')

BODY=$(cat <<EOF
## SkillFish OS kernel — linux-tkg ${KVER}

Custom linux-tkg **7.0.10** built for the AMD BC-250 (Cyan Skillfish / gfx1013).

**Optimizations baked in**
- BORE scheduler · 1000 Hz timer · tickless-idle · PREEMPT
- GCC -O3 · \`-march=znver2\` (Zen2 native)
- NTsync + fsync (Proton/Wine)
- Zenify / glitched-base desktop+gaming tweaks

**BC-250 patches**
- GPU SCLK range unlock 350–2230 MHz (\`cyan_skillfish_ppt.c\`)
- 40-CU unlock — **opt-in**, default off. Enable with kernel param \`amdgpu.bc250_cc_write_mode=3\` (thermal-heavy; cap clocks ~1500 MHz/900 mV).

**Notes** — Do NOT enable IOMMU (broken on BC-250). \`uname -r\` = \`${KVER}\`.
EOF
)

echo ">>> Creating/looking up release ${TAG} ..."
REL=$(curl -fsSL "${AUTH[@]}" "${API}/repos/${REPO}/releases/tags/${TAG}" 2>/dev/null || true)
REL_ID=$(printf '%s' "$REL" | jq -r '.id // empty')

if [ -z "$REL_ID" ]; then
    REL=$(curl -fsSL "${AUTH[@]}" -X POST "${API}/repos/${REPO}/releases" \
        -d "$(jq -n --arg t "$TAG" --arg b "$BODY" \
            '{tag_name:$t, name:("Kernel "+$t), body:$b, draft:false, prerelease:false}')")
    REL_ID=$(printf '%s' "$REL" | jq -r '.id')
    echo "Created release id=$REL_ID"
else
    echo "Release already exists id=$REL_ID — will (re)upload assets"
fi

for deb in "${DEBS[@]}"; do
    name=$(basename "$deb")
    # delete existing asset of same name (idempotent re-publish)
    existing=$(curl -fsSL "${AUTH[@]}" "${API}/repos/${REPO}/releases/${REL_ID}/assets" \
        | jq -r --arg n "$name" '.[] | select(.name==$n) | .id')
    if [ -n "$existing" ]; then
        curl -fsSL "${AUTH[@]}" -X DELETE "${API}/repos/${REPO}/releases/assets/${existing}" || true
        echo "  deleted old asset $name"
    fi
    echo "  uploading $name ..."
    curl -fsSL "${AUTH[@]}" -H "Content-Type: application/vnd.debian.binary-package" \
        --data-binary @"$deb" \
        "${UPLOADS}/repos/${REPO}/releases/${REL_ID}/assets?name=${name}" \
        | jq -r '"  -> " + .browser_download_url'
done

echo ">>> Done. Release: https://github.com/${REPO}/releases/tag/${TAG}"

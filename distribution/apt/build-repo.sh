#!/bin/bash
# build-repo.sh — build/refresh the SkillFishOS APT repository with reprepro.
#
# Usage:
#   ./build-repo.sh keygen          # one-time: create the repo signing GPG key
#   ./build-repo.sh add <pkg.deb>   # add a .deb to suite 'aetherium'
#   ./build-repo.sh kernel          # fetch + add the linux-tkg kernel from the GitHub release
#   ./build-repo.sh export          # (re)export the public key to ./skillfishos-archive-keyring.gpg
#
# Output layout (publish the whole ./public/ dir as the repo root):
#   public/dists/aetherium/...      (Release, Packages, signatures)
#   public/pool/main/...            (the .deb files)
#
# Requirements: reprepro, gnupg, curl.  Install: sudo apt install reprepro gnupg curl
set -euo pipefail
cd "$(dirname "$0")"

REPO_DIR="$PWD/public"          # reprepro basedir == published root
KEY_NAME="SkillFishOS Archive Signing Key"
KEY_EMAIL="apt@skillfishos.com"
KERNEL_TAG="kernel-7.0.10-skillfishos"
GH="MTSistemi/SkillFishOS"

mkdir -p "$REPO_DIR/conf"
cp -f conf/distributions "$REPO_DIR/conf/distributions"

case "${1:-}" in
  keygen)
    cat > /tmp/skillfish-gpg.batch <<EOF
%no-protection
Key-Type: eddsa
Key-Curve: ed25519
Subkey-Type: ecdh
Subkey-Curve: cv25519
Name-Real: $KEY_NAME
Name-Email: $KEY_EMAIL
Expire-Date: 0
%commit
EOF
    gpg --batch --gen-key /tmp/skillfish-gpg.batch
    rm -f /tmp/skillfish-gpg.batch
    echo ">> Key created. BACK UP your private key:"
    echo "   gpg --export-secret-keys --armor $KEY_EMAIL > skillfishos-apt-private.asc  (keep OFFLINE, do NOT commit)"
    "$0" export
    ;;
  export)
    # Public key in the binary keyring format used by signed-by=
    gpg --export "$KEY_EMAIL" > skillfishos-archive-keyring.gpg
    gpg --export --armor "$KEY_EMAIL" > skillfishos-archive-keyring.asc
    echo ">> Exported skillfishos-archive-keyring.gpg / .asc"
    ;;
  add)
    [ -f "${2:-}" ] || { echo "usage: $0 add <pkg.deb>"; exit 1; }
    reprepro -b "$REPO_DIR" includedeb aetherium "$2"
    echo ">> Added $2 to aetherium"
    ;;
  kernel)
    tmp="$(mktemp -d)"
    echo ">> Fetching kernel .deb assets from release $KERNEL_TAG ..."
    # Requires gh CLI authenticated, or download manually from the release page.
    gh release download "$KERNEL_TAG" -R "$GH" -p '*.deb' -D "$tmp" || {
      echo "!! gh download failed — download the .deb assets manually from:"
      echo "   https://github.com/$GH/releases/tag/$KERNEL_TAG"
      echo "   then run: $0 add <file.deb>"; exit 1; }
    for d in "$tmp"/*.deb; do reprepro -b "$REPO_DIR" includedeb aetherium "$d"; done
    rm -rf "$tmp"
    echo ">> Kernel added."
    ;;
  *)
    grep -E '^#( |$)' "$0" | sed 's/^# \{0,1\}//'
    ;;
esac

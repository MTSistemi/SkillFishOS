#!/bin/bash
# Build umr (User Mode Register debugger) for the BC-250 — needed for live CU control.
LOG=/tmp/umr_build.log
{
  set -e
  export DEBIAN_FRONTEND=noninteractive
  echo "=== [1/4] apt deps $(date) ==="
  apt-get update -qq
  apt-get install -y -qq cmake libpciaccess-dev libdrm-dev libjson-c-dev \
      bison flex zlib1g-dev libncurses-dev pkg-config build-essential
  echo "=== [2/4] clone umr ==="
  cd /opt && rm -rf umr
  git clone --depth 1 https://gitlab.freedesktop.org/tomstdenis/umr.git
  echo "=== [3/4] cmake ==="
  cd /opt/umr && mkdir -p build && cd build
  cmake -DCMAKE_BUILD_TYPE=Release ..
  echo "=== [4/4] make ==="
  make -j4
  echo "=== INSTALL ==="
  make install || cp -v umr /usr/local/bin/umr 2>/dev/null || true
  command -v umr && umr --version 2>/dev/null | head -1
  echo "=== UMR-BUILD-DONE rc=0 $(date) ==="
} >"$LOG" 2>&1

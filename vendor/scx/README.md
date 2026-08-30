# scx_lavd, built by us

`scx_lavd` is a CPU scheduler written as a BPF program and loaded from user
space through `sched_ext`. Our kernel enables `CONFIG_SCHED_CLASS_EXT`, but the
scheduler itself is a separate program and Debian sid does not carry one -
neither `scx` nor `scx-scheds`, checked again on 30/08/2026. So we build it.

This is the one real kernel-side difference between us and CachyOS. The rest of
their advantage is userspace recompiled for x86-64-v3/v4, which we cannot copy.

## What it buys, measured

Black Myth: Wukong on the BC-250, same conditions on both sides (performance
governor, OC 3500, kernel 7.2.2), the comparison accepted by `skillfish-banco`:

| | without | with scx_lavd | |
|---|---|---|---|
| average | 110.1 fps | 109.9 fps | nothing |
| 1% lows | 60.1 | 72.5 | +20.6% |
| 0.1% lows | 24.1 | 35.9 | +49.0% |

It does not render more frames, it delivers them more evenly. That is what a
scheduler is for, and it is the kind of gain you feel while playing and cannot
see in the average.

⚠️ One run per side. Our measured noise is 12.7% on the 1% lows and 23.4% on
the 0.1% lows, so the numbers are above it - but this is a strong signal, not a
proof. Repeat before quoting it anywhere public.

## How it was built

    apt-get install cargo bpftool libbpf-dev pkg-config
    git clone https://github.com/sched-ext/scx
    cd scx && cargo build --release -p scx_lavd

`rust-toolchain.toml` asks only for `stable`, so Debian's rustc is enough and
rustup is not needed. Built from commit 8bd309a on 30/08/2026, scheduler
version lavd 1.1.3. Licence GPL-2.0, so redistribution is fine.

## The kernel side

`kernel.config` in the scx repository lists what the kernel must have. Ours has
all of it: `SCHED_CLASS_EXT`, `BPF`, `BPF_JIT`, `DEBUG_INFO_BTF`,
`KALLSYMS_ALL`, `FUNCTION_TRACER`, `PREEMPT`. The two it reports missing are
`SCHED_DEBUG`, dropped upstream, and `DEBUG_LOCKDEP`, which is for debugging
the kernel and not for running it.

⚠️ `_ftracedisable` must stay `"false"` in `customization.cfg`: with FTRACE off
LAVD does not work, and customization.cfg says so itself.

# scx_lavd, built by us

`scx_lavd` is a CPU scheduler written as a BPF program and loaded from user
space through `sched_ext`. Our kernel enables `CONFIG_SCHED_CLASS_EXT`, but the
scheduler itself is a separate program and Debian sid does not carry one -
neither `scx` nor `scx-scheds`, checked again on 30/08/2026. So we build it.

This is the one real kernel-side difference between us and CachyOS. The rest of
their advantage is userspace recompiled for x86-64-v3/v4, which we cannot copy.

## It is off by default, and here is why

The first comparison - one run a side - had the 1% lows on Wukong up 20 per
cent and the 0.1% lows up 49. That looked like the classic scheduler win: the
average still, the stutter gone. Then we repeated it, and it fell apart.

**Wukong, three runs a side.** Nothing moves.

| | with lavd | without |
|---|---|---|
| average | 109.9 / 109.8 / 109.0 | 110.1 / 109.9 / 109.4 |
| 1% lows | 72.5 / 74.1 / 42.1 | 60.1 / 70.1 / 39.9 |

The lows swing the same way on both sides. Our measured noise on that figure is
12.7 per cent and these numbers sit inside it.

**Cyberpunk 2077, four runs with and five without,** the last four interleaved
one after the other so that any drift over the session hits both sides equally:

| | with lavd | without |
|---|---|---|
| average | 84.3 / 83.9 / 88.1 / 83.5 | 92.4 / 90.5 / 83.3 / 83.1 / 91.9 |
| 1% lows | 44.4 / 44.3 / 42.4 / 42.7 | 47.7 / 46.4 / 38.0 / 37.3 / 45.6 |

Read it honestly: with lavd the average sits around 85 against 88, so a few per
cent lower, and the 1% lows are the same (43.5 against 43.0). But the runs
without lavd swing from 83 to 92 - a spread that swallows the whole difference.
So there is no evidence of a benefit, some evidence of a small cost, and the
game's own variation is larger than either.

That is why the package ships with the service **not** enabled. The switch is in
the Tuner and in the Remote Manager: anyone whose games disagree turns it on in
one click.

⚠️ The lesson is worth more than the result. One run a side is not a
measurement. The bench had already told us the noise - 0.9 per cent on the
average, 12.7 on the 1% lows, 23.4 on the 0.1% - and a difference inside that
got reported as a win.

## The measuring trap, which cost four discarded runs

Menus and the results screen render at a flat 157 to 175 fps, and MangoHud's
recording window starts at a **fixed** delay after the game launches. Let the
loading take longer than usual and the window lands on a still screen: the
average and the lows shoot up and it looks like a huge improvement. One of those
false numbers was +40 per cent.

The fix is to record a long window and cut afterwards: 5-second blocks, anything
above 150 fps thrown away, the untouched log kept beside it as `.intero.csv`.
Real gameplay oscillates; a still screen does not. Always look at the run
window by window before believing a number.

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

## Two things it does that surprise you

It writes `scx_task_data:83 no task data` about four times a second, out of the
BPF stream rather than Rust's logger, so the log-level option does not touch
it. The service rate-limits the journal instead of silencing stderr, because a
scheduler that fails quietly is worse than a noisy one.

And enabling the unit returns before the scheduler is attached: it needs about
five seconds to load its BPF program. Read the state straight away and you get
"on but not loaded", which looks like a fault and is not one.

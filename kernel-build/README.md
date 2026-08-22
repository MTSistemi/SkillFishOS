# SkillFishOS kernel build recipe (linux-tkg, currently 7.2-skillfishos)

Build host: AMD BC-250 (Debian). Tool: https://github.com/Frogging-Family/linux-tkg

## Steps
1. git clone https://github.com/Frogging-Family/linux-tkg
2. Copy `customization.cfg` over linux-tkg/customization.cfg
3. Patch install.sh line ~176: `_kernel_flavor="tkg-${_kernel_localversion}"` -> `_kernel_flavor="${_kernel_localversion}"` (drops the `tkg-` prefix so uname = 7.0.10-skillfishos)
4. Put userpatches/*.mypatch into linux-tkg/linux70-tkg-userpatches/
   - 0001-bc250-freq-unlock.mypatch  (SCLK 350-2230 MHz)
   - 0002-bc250-40cu-unlock.mypatch  (40 CU, opt-in amdgpu.bc250_cc_write_mode=3) - from duggasco/bc250-40cu-unlock
   - 0003-bc250-rdseed-quiet.mypatch
   - 0004-rtw89-fw-O2.mypatch      (fw.c does not build at -O3)
   - 0005-bc250-vcn.mypatch         (registers VCN 2.0.3 behind amdgpu.bc250_vcn=1;
     off by default, and there is no firmware for it -- see the VCN notes)
   - 0006-bc250-8core-telemetry.mypatch (GPU clock readout with 8 cores unlocked:
     the 8-core SMU metrics layout has no slot for GfxclkFrequency, so the driver
     was reading a residency counter as a clock. Reads it from the firmware
     instead. By higorprado, carried from GabriWar/bc250-core-cu-unlock.
     ⚠️ Once this ships, check whether the Monitor's SMU sampler is still needed:
     it works around this very bug, and two fixes for one bug is one too many.)
 (drops the cosmetic per-CPU `pr_emerg("RDSEED is not reliable...")` boot spam in arch/x86/kernel/cpu/amd.c; RDSEED is still correctly disabled via clear_cpu_cap/msr_clear_bit, just silently)
4b. Copy `config-fragments/*.myfrag` into the linux-tkg root (same folder as
   the PKGBUILD). `customization.cfg` already has `_config_fragments="true"` and
   `_config_fragments_no_confirm="true"`, so they are applied without asking.
   - `skillfish-sched-ext.myfrag` — turns on `CONFIG_SCHED_CLASS_EXT`, the
     extensible scheduler class, plus the BTF it needs.
     Install `dwarves` on the build host first (`pahole`), or the build fails
     late with a missing tool.
5. ./install.sh install  -> .deb in DEBS/  (then publish via scripts/publish-kernel.sh)

Key config: BORE, GCC -O3, -march=znver2, 1000Hz, NTsync+fsync, no LTO,
localversion=skillfishos, and from 7.2.1 onwards `sched_ext` enabled.

### sched_ext: what it does and does not give you

`CONFIG_SCHED_CLASS_EXT` lets the kernel host a scheduler written in BPF and
swap it at runtime. It is the one real kernel-level difference between this
kernel and CachyOS's — measured on 2026-08-23, our config did not have the
symbol at all.

⚠️ On its own it changes nothing for a user. The scheduler itself is a separate
userspace program, and Debian sid ships neither `scx-scheds` nor `scx`. Until we
package them the kernel keeps running BORE, which is the default and is fine.
Enabling it now means the kernel is ready the day those land, instead of asking
people to wait for a rebuild.

⚠️ It is not free. sched_ext needs BTF, BTF needs debug info, and this config
had `CONFIG_DEBUG_INFO_NONE=y` — none at all. Turning it on lengthens the build
and adds a few MB to the image. The build host needs `pahole` from `dwarves`.

⚠️ Leave `_ftracedisable="false"`. With FTRACE off the LAVD scheduler does not
work — customization.cfg says so on the line above the option.

## Two traps that cost a build each

### The config in this repo is not the one that gets used

`install.sh` reads `~/.config/frogminer/linux-tkg.cfg` **if it exists**, and that
file **overrides** `customization.cfg` — the one in this repository. It says so in
one line of output that scrolls past in a second:

    -> External configuration file /root/.config/frogminer/linux-tkg.cfg will be
       used and will override customization.cfg values

On 2026-08-22 that leftover file still said `_version="7.1-latest"`, so a build
started for 7.2 quietly checked out 7.1 instead. Nothing failed; it just built
the wrong kernel.

Before every build, check what will actually be used:

```bash
grep -E '^_(version|kernel_localversion)=' ~/.config/frogminer/linux-tkg.cfg
```

and make it agree with `customization.cfg`, or move it aside.

### `_version` takes `x.y-latest` or an exact tag

`_version="7.2"` is refused — the value has to be either `7.2-latest` (resolves to
the newest 7.2.z) or a tag that exists in the remote, like `v7.2`. Getting this
wrong stops the build at the first step, which at least is honest.

### Userpatches live in a version-specific folder

`linux72-tkg-userpatches` — VERSION and PATCHLEVEL glued together, no dot. Put
them in the wrong folder and **the build succeeds without them**: no core unlock,
no frequency unlock, and nothing says so. Check the log:

```bash
grep 'Applying your own' /root/build-*.log
```

There should be one line per patch.

### A patch with a hunk header that lies

`0004-rtw89-fw-O2.mypatch` claimed three lines of context (`@@ -1,3 +1,6 @@`) and
carried none. `patch(1)` cannot place a hunk it cannot match, and linux-tkg
aborts the whole build on a failed patch. Never hand-write a hunk header:
generate patches with `diff` against the real tree, the way
`0005-bc250-vcn.mypatch` was made.

## Naming: the flavour belongs in the name

The BC-250 kernel is `<version>-skillfishos`. Its `-march=znver2` build will not
boot anywhere else, and the name does not say so — which is fine as long as it
is the only one.

⚠️ The next kernel built for OTHER machines must be named
`<version>-skillfishos-x64` (`LOCALVERSION=-skillfishos-x64`), not
`-skillfishos-generic` and not a bare `-skillfishos`.

The reason is not tidiness: both kernels land in the same `/boot`, the same GRUB
menu and the same APT repository, and a user who ends up with two entries whose
names differ only by version number has no way to tell which one runs on their
hardware. `-x64` says it plainly — this is the one for any 64-bit machine —
while the plain name stays with the board the distribution is built around.

`scripts/iso-prep-kernel.sh` matches `*skillfishos*`, so it keeps working for
both without changes.

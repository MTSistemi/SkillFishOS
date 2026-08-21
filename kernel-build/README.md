# SkillFishOS kernel build recipe (linux-tkg 7.0.10-skillfishos)

Build host: AMD BC-250 (Debian). Tool: https://github.com/Frogging-Family/linux-tkg

## Steps
1. git clone https://github.com/Frogging-Family/linux-tkg
2. Copy `customization.cfg` over linux-tkg/customization.cfg
3. Patch install.sh line ~176: `_kernel_flavor="tkg-${_kernel_localversion}"` -> `_kernel_flavor="${_kernel_localversion}"` (drops the `tkg-` prefix so uname = 7.0.10-skillfishos)
4. Put userpatches/*.mypatch into linux-tkg/linux70-tkg-userpatches/
   - 0001-bc250-freq-unlock.mypatch  (SCLK 350-2230 MHz)
   - 0002-bc250-40cu-unlock.mypatch  (40 CU, opt-in amdgpu.bc250_cc_write_mode=3) - from duggasco/bc250-40cu-unlock
   - 0003-bc250-rdseed-quiet.mypatch (drops the cosmetic per-CPU `pr_emerg("RDSEED is not reliable...")` boot spam in arch/x86/kernel/cpu/amd.c; RDSEED is still correctly disabled via clear_cpu_cap/msr_clear_bit, just silently)
5. ./install.sh install  -> .deb in DEBS/  (then publish via scripts/publish-kernel.sh)

Key config: BORE, GCC -O3, -march=znver2, 1000Hz, NTsync+fsync, no LTO, localversion=skillfishos.

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

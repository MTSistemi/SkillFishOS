---
title: The tailored kernel
description: The linux-tkg kernel patched for the BC-250, the boot parameters and the kernels to avoid.
group: System
order: 1
---

The heart of SkillFishOS's optimizations is a **custom-built kernel** for the BC-250, based on [linux-tkg](https://github.com/Frogging-Family/linux-tkg) — a build recipe from the *Frogging Family* that applies performance- and gaming-oriented patches.

## Version and patches

The SkillFishOS kernel is version **`7.0.10-skillfishos`**. On top of the standard linux-tkg patches it includes:

- the BC-250 **frequency-unlock patch** (range 350–2230 MHz);
- the **40-CU patch** that enables all of the GPU's Compute Units;
- a custom **RDSEED-quiet** patch that silences a noisy kernel message on this hardware.

The kernel package (image + headers) is published as a release and is **held** (`apt-mark hold`) so that a Debian update can't replace it with an unsuitable kernel. It is the default kernel in GRUB.

## Boot parameters (cmdline)

The kernel command line is configured as follows, and every parameter has a precise reason:

```
mitigations=off
amdgpu.gttsize=6144
ttm.pages_limit=4194304
ttm.page_pool_size=4194304
video=DP-1:e
```

| Parameter | What it does |
|---|---|
| `mitigations=off` | disables Spectre/Meltdown mitigations to maximize performance (an acceptable choice on a home console) |
| `amdgpu.gttsize=6144` | extends the GTT → Vulkan sees ~13 GiB of memory (useful for AI) |
| `ttm.pages_limit` / `ttm.page_pool_size` | raise the TTM memory manager limits consistently with the enlarged GTT |
| `video=DP-1:e` | **force-enables** the DisplayPort connector (HPD is broken, see [hardware](/en/docs/hardware-bc250)) |

> **Live Compute Units.** SkillFishOS no longer uses the `amdgpu.bc250_cc_write_mode=3` parameter (which locked 40 CU at boot and blocked runtime changes). The system now boots at the driver baseline (24 CU) and a service routes the **40 CUs live** at startup; you can change them without a reboot from the [Tuner](/en/docs/app-native). See [GPU and overclock](/en/docs/gpu-overclock).

## Kernels to avoid

Not all recent kernels work well on this hardware. In particular the **6.15.0–6.15.6** and **6.17.8–6.17.10** series are known to be problematic and should be avoided. SkillFishOS ships its own tested kernel precisely to avoid these regressions — see [Updates](/en/docs/aggiornamenti).

## IOMMU

As noted on the [hardware](/en/docs/hardware-bc250) page, the **IOMMU must never be enabled** on the BC-250: it is unstable. The kernel always boots with IOMMU disabled.

## Why our own kernel and not XanMod or stock

- The **Debian stock kernel** lacks the BC-250 patches (frequency unlock, 40 CU) and follows the regressions above.
- **linux-tkg** makes it easy to apply the custom patches and to pick gaming-oriented schedulers and options.
- Building it ourselves means we update the kernel **only when a new version brings real benefits** and after testing it on the hardware.

## Sources

- [linux-tkg (Frogging-Family)](https://github.com/Frogging-Family/linux-tkg)
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock)
- [amdgpu driver parameters](https://docs.kernel.org/gpu/amdgpu/module-parameters.html)
- [bc250.info](https://bc250.info) — kernel and cmdline notes

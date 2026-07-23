# Building from source

Two things can be built: the **kernel** and the **ISO**.

---

## Build the kernel

The recipe lives in [`kernel-build/`](../kernel-build/): a `customization.cfg` for [linux‑tkg](https://github.com/Frogging-Family/linux-tkg) plus the BC‑250 userpatches.

### Prerequisites (Debian)

```sh
sudo apt install build-essential bc kmod cpio flex libncurses-dev \
                 libelf-dev libssl-dev bison schedtool ccache git
```

### Steps

```sh
git clone https://github.com/Frogging-Family/linux-tkg
cd linux-tkg

# 1. Use the SkillFishOS customization
cp /path/to/kernel-build/customization.cfg .

# 2. Drop the BC-250 userpatches into the version's userpatches dir
#    (e.g. linux70-tkg-userpatches/ for the 7.0 series):
cp /path/to/kernel-build/userpatches/*.mypatch linux70-tkg-userpatches/

# 3. Build the .deb packages
./install.sh install
```

The three userpatches:

| Patch | Effect |
|---|---|
| GPU frequency unlock | SMU clock range **350–2230 MHz** |
| 40‑CU unlock | enables all 40 compute units (opt‑in) |
| RDSEED‑quiet | removes the cosmetic `RDSEED is not reliable…` boot spam (keeps RDSEED correctly disabled) |

> ⚠️ `.mypatch` files **must stay LF**. A `.gitattributes` (`*.mypatch text eol=lf`) enforces this — CRLF from Windows would break `patch`.

Output `.deb`s land in `DEBS/`. Install:

```sh
sudo dpkg -i linux-image-7.0.10-skillfishos_*.deb linux-headers-7.0.10-skillfishos_*.deb
sudo apt-mark hold linux-image-7.0.10-skillfishos linux-headers-7.0.10-skillfishos
sudo update-grub
```

A prebuilt build is also published under [Releases](../../../releases/tag/kernel-7.0.10-skillfishos).

### Publishing a release

`scripts/publish-kernel.sh` helps attach freshly built `.deb`s as GitHub release assets (the image `.deb` exceeds GitHub's 100 MB in‑repo file limit, so it ships as a release asset, not a committed file).

---

## Build the ISO

The live‑build configuration in [`iso/`](../iso/) reproduces the full system.

### Prerequisites

```sh
sudo apt install live-build
```

### Steps

```sh
cd iso/
sudo bash build.sh      # runs: bash auto/config && lb build
```

This produces a hybrid ISO with the KDE Plasma steampunk desktop, the gamescope console session, Btrfs + Snapper + grub‑btrfs, and a Calamares installer.

> The ISO build hook fetches the tkg kernel from a GitHub Release — make sure it points at the SkillFishOS kernel release.

---

## Notes

- Base distro is Debian **sid**; package availability there is better than testing for the bleeding‑edge bits (Mesa, KDE, Vulkan).
- Never enable IOMMU; avoid kernels 6.15.0–6.15.6 / 6.17.8–6.17.10.
- See [OPTIMIZATIONS.md](OPTIMIZATIONS.md) for the runtime tuning the ISO bakes in.

# The eggs branch of the Calamares configuration

⚠️ **These files are a copy. The live ones live on the build board, not here.**

SkillFishOS has **two** Calamares configurations and they are not the same one:

| branch | where it lives | who uses it |
|---|---|---|
| live-build | `iso/config/includes.chroot/etc/calamares/` | the live-build path |
| **eggs** | **the build board** | **the ISOs we actually publish** |

The ISOs we ship are built with eggs, which clones the board. eggs regenerates
`/etc/calamares/settings.conf` from its own template at
`/etc/penguins-eggs.d/distros/<codename>/calamares/settings.yaml` on every
build — so editing `/etc/calamares/settings.conf` directly is pointless, it is
overwritten. The template is what counts.

⚠️ But the **module** files are the other way round: eggs does *not* copy them
from the template directory. They have to exist in `/etc/calamares/modules/`
on the board, where they survive the regeneration.

That asymmetry cost us a whole ISO build to discover, and the configuration
that decides how every user's disk gets installed was living on one machine
with no copy anywhere. Hence these files.

## What is here

| file | goes to |
|---|---|
| `settings.yaml` | `/etc/penguins-eggs.d/distros/forky/calamares/settings.yaml` |
| `shellprocess@cryptofix.conf` | `/etc/calamares/modules/` |
| `shellprocess@cryptofixpost.conf` | `/etc/calamares/modules/` |

After changing the template, regenerate with:

```sh
eggs calamares --install
```

and check that the sequence really came out as intended:

```sh
grep -nE 'cryptofix|mkinitramfs|grubcfg' /etc/calamares/settings.conf
```

## Why cryptofix runs twice

The encrypted-install fix (issue #61) needs two different moments:

```
initramfscfg
shellprocess@cryptofix       <- pre:  /etc/crypttab, before the boot image is built
shellprocess@mkinitramfs
grubcfg                      <- Calamares REWRITES /etc/default/grub here
bootloader
shellprocess@cryptofixpost   <- post: the splash and the GRUB keymap
shellprocess@boot_reconfigure
```

⚠️ Do everything in the *pre* slot and `grubcfg` overwrites the boot line, so
the splash comes back and hides the passphrase prompt. Do everything in the
*post* slot and the crypttab arrives after the boot image has already been
built — and it cannot be repaired afterwards, because inside the installer
`update-initramfs` refuses to run at all: *"update-initramfs is disabled (live
system is running without media mounted on /run/live/medium)"*. We fell into
both traps, one at a time.

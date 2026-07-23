# Native KDE ISO mounting

A small, dependency‑light way to mount `.iso` disc images on KDE **without GNOME**
(`gnome-disk-image-mounter`). It uses **udisks2** — the same disk daemon KDE/Solid
already talks to — so there is nothing extra to install on a Plasma system.

## What you get

- **Double‑click** an `.iso` in Dolphin → it mounts and opens the contents.
- **Right‑click** an `.iso` → *Mount / Unmount ISO image* (Dolphin service menu).
- Mounts are **read‑only**, **single**, and **idempotent** (re‑opening reuses the
  existing loop device instead of stacking new ones); unmounting frees the loop.

## Files

| File | Install path | Purpose |
|------|--------------|---------|
| `skillfish-iso-mount` | `/usr/local/bin/skillfish-iso-mount` | the wrapper (`udisksctl loop-setup`/mount/unmount) |
| `skillfish-iso.desktop` | `/usr/share/kio/servicemenus/skillfish-iso.desktop` | Dolphin right‑click *Mount / Unmount* |
| `skillfish-iso-mount.desktop` | `/usr/share/applications/skillfish-iso-mount.desktop` | hidden launcher used as the double‑click handler |
| `49-skillfish-udisks.rules` | `/etc/polkit-1/rules.d/49-skillfish-udisks.rules` | let the `sudo` group loop‑setup/mount without a prompt |

Then make `.iso` open with the handler by default:

```sh
xdg-mime default skillfish-iso-mount.desktop application/x-cd-image application/x-iso9660-image
```

(also add it to `/etc/skel/.config/mimeapps.list` so new users get it).

## Gotchas (learned the hard way)

1. **Read‑only.** `udisksctl loop-setup` opens **read‑write** by default → use **`-r`**,
   or you get *Permission denied* on a non‑writable ISO file.
2. **No double‑mount.** udisks auto‑mounts in an active graphical session, *and* the
   wrapper would mount again → two identical mountpoints. The wrapper now **waits for
   the auto‑mount** (polls `findmnt` ~3 s) and only mounts explicitly if it didn't
   happen (non‑active contexts).
3. **Spaces in names.** `findmnt -nro TARGET` prints spaces as `\x20` → de‑escape with
   `sed 's/\\x20/ /g'` before handing the path to Dolphin.
4. **Find the loop with `losetup`, not `lsblk`.** On current util‑linux,
   `lsblk -o NAME,BACK-FILE` reports *unknown column* → the file→loop lookup returned
   empty, so the wrapper never noticed an existing loop and created a new one on every
   double‑click (and unmount found nothing). Use
   `losetup -nO NAME -j "$ISO" | head -1` (works as a normal user, no root).
5. **Dolphin association cache.** A running Dolphin caches MIME defaults in RAM, so
   right after you set the default it may still show *Open With…*; restart Dolphin
   once. Fresh users/installs already have the correct default — nothing to do.

## Hybrid ISOs

For isohybrid images (a partition table instead of a bare filesystem, e.g. the
SkillFishOS installer ISO itself) udisks won't see `loop0` as a filesystem — the
wrapper falls back to `loop0p1`.

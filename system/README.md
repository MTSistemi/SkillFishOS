# system/ — live SkillFishOS system configuration

A snapshot of all the **hand-made config, scripts, units and branding** that make a
plain Debian-sid + KDE box into SkillFishOS on the AMD BC-250. The tree **mirrors the
filesystem root** — each file belongs at its path with the `system/` prefix stripped.

This is the source of truth for reproducing the system / baking the final ISO
(everything here lives on the running BC-250). No secrets are included (no Wi-Fi PSKs,
no VNC password — VNC is `-nopw` LAN-only, autologin has no stored password).

## Layout

| Path | What |
|---|---|
| `usr/local/bin/skillfish-*` | scripts: `x11vnc` (remote), `dp-hotswap` (HPD workaround), `hud-val`/`hud-bt` (Conky HUD sensors), `gaming-mode` (gamescope session), `thermal-guard`, `kde-firstrun`, `iso-mount` |
| `usr/bin/cyan-skillfish-governor` | GPU SMU governor (compiled; src: github.com/Magnap/cyan-skillfish-governor) |
| `opt/bc250_smu_oc/*.py` | CPU OC/UV tool (src: github.com/bc250-collective/bc250_smu_oc) |
| `etc/systemd/system/*` | services: dp-hotswap, bc250-smu-oc (CPU OC), cyan-skillfish-governor (+`after-oc` drop-in), thermal-guard, docker ACL drop-in |
| `etc/systemd/logind.conf.d/` | **anti-suspend** (`IdleAction=ignore`) — pair with `systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target` |
| `etc/cyan-skillfish-governor/config.toml`, `etc/bc250-smu-oc.conf` | GPU safe-points (2000 MHz) + CPU OC (3700 MHz) |
| `etc/default/grub` | kernel cmdline (mitigations=off, 40-CU, gttsize, ttm, video=DP-1:e) |
| `etc/sddm.conf.d/` | autologin skillfish → `plasmax11`, Relogin, brass theme |
| `etc/NetworkManager/NetworkManager.conf` | `[ifupdown] managed=true` (enp4s0 visible in GUI) |
| `etc/xdg/kcm-about-distrorc`, `etc/os-release`, `usr/lib/os-release`, `etc/issue` | branding (SkillFishOS, skillfishos.com) |
| `usr/share/libdrm/amdgpu.ids` | GPU name "AMD Cyan SkillFish (APU)" (device 13FE) |
| `etc/polkit-1/`, `usr/share/polkit-1/actions/` | iso-mount rule + Tuner policy (all-yes, no password on a personal box) |
| `usr/share/{sddm,plymouth}/themes/`, `boot/grub/themes/skillfish/` | brass boot→login branding |
| `usr/share/applications/`, `usr/share/icons/hicolor/.../`, `usr/share/pixmaps/`, `usr/share/skillfish/` | custom launchers (Tuner/AI/Info) + fish logos + avatar + splash |
| `usr/share/kio/servicemenus/` | Dolphin "Mount/Unmount ISO" |
| `etc/skel/.face.icon` | default avatar (fish) for new users |
| `home/skillfish/.config/*` | the **brass KDE defaults** — for new users copy these into `/etc/skel/.config/`: `kdeglobals`/`kcminputrc`/`kscreenlockerrc`/`kwinrc`/`ksmserverrc`, `Kvantum/`, `environment.d/` (QT_STYLE_OVERRIDE, cursor, locale), `autostart/` (conky, x11vnc), `gtk-{3,4}.0/gtk.css`, `conky/skillfish.conf`, `mimeapps.list` |

## Install (rough)

```sh
sudo rsync -a system/usr system/etc system/boot system/opt /
sudo cp -r system/home/skillfish/.config/* /etc/skel/.config/   # for new users
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
sudo systemctl enable --now skillfish-dp-hotswap cyan-skillfish-governor bc250-smu-oc
update-grub && update-initramfs -u
```

> The theme assets proper (icon theme, cursors, Kvantum, color-scheme, plasma-theme,
> look-and-feel, wallpapers, avatars) live in [`../theme/`](../theme/); the GUI apps in
> [`../apps/`](../apps/). This folder is the glue/config around them.

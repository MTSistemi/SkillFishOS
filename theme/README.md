# SkillFish Steampunk theme

The complete brass / steampunk theme used across SkillFishOS — accent `#d8a849` on dark brown, designed to feel coherent from the GRUB menu all the way to the desktop.

## Contents

```
icons/SkillFishSteampunk/   icon theme (incl. symbolic icons that recolor to the scheme)
cursors/                    SkillFish-Steampunk-Cursors (Xcursor theme)
Kvantum/                    Qt widget style (Kvantum)
palettes/                   terminal color palettes (alacritty/foot/kitty)
titlebar/                   window-button artwork
powermenu/                  power-menu icons
wallpapers/                 steampunk wallpapers (resized for the repo)
```

## Install (KDE Plasma)

Copy the system‑wide pieces:

```sh
sudo cp -r icons/SkillFishSteampunk        /usr/share/icons/
sudo cp -r cursors/SkillFish-Steampunk-Cursors /usr/share/icons/
sudo gtk-update-icon-cache -f /usr/share/icons/SkillFishSteampunk

# Kvantum (per-user)
mkdir -p ~/.config/Kvantum
cp -r Kvantum/SkillFishSteampunk ~/.config/Kvantum/
printf '[General]\ntheme=SkillFishSteampunk\n' > ~/.config/Kvantum/kvantum.kvconfig
```

Then apply via the KDE tools (in an active session):

```sh
plasma-apply-icontheme   SkillFishSteampunk      # or kwriteconfig6 kdeglobals [Icons] Theme
plasma-apply-cursortheme SkillFish-Steampunk-Cursors
kwriteconfig6 --file kdeglobals --group KDE     --key widgetStyle  kvantum
kwriteconfig6 --file kdeglobals --group General --key AccentColor  "216,168,73"
```

## Gotchas (learned the hard way)

- **Cursor symlinks get flattened by Windows/Git** (`core.symlinks=false`): the ~80 cursor aliases are symlinks, but on Windows they become text files containing the target name → a broken theme. After extracting, recreate any `cursors/*` file that does **not** start with the `Xcur` magic as a real symlink (`ln -sf <target> <file>`).
- **Generic folders show up blue** unless the icon theme provides `inode-directory` (not just `folder`). KDE asks for `inode-directory` on generic folders. Copy `folder.svg` → `scalable/places/inode-directory.svg` (and `mimetypes/`) and refresh the cache.
- **Symbolic icons** (`*-symbolic.svg`) recolor to the active color scheme — keep them for tray icons (Bluetooth, volume, network) to stay coherent.
- After changing icons, clear `~/.cache/plasma_theme_*.kcache` / `icon-cache.kcache` and restart `plasmashell` (from a real session, not a stripped SSH env, or you lose `XDG_DATA_DIRS`).

## License

Provided for use with SkillFishOS under the project's [GPL‑3.0](../LICENSE).

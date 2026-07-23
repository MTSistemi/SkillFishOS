# Icon audit — SkillFish Steampunk

Data‑driven audit of which icons the **visible** KDE shell actually requests vs.
what the `SkillFishSteampunk` theme provides. Anything the theme doesn't provide
falls through `Inherits=breeze-dark` → the user sees a **blue/grey** icon.

Method: grep the real icon names from the Plasma logout greeter, system‑tray
applets, Kickoff, Dolphin and the KCM `.desktop` files, then resolve each name
against the theme tree (and the inheritance chain) on the live system.

## ✅ Already fixed — 48 brass aliases

These had no dedicated brass SVG but a good equivalent already existed in the
theme, so they're now aliased to it (copied SVG). Highlights:

| Missing name | Aliased to | Where it shows |
|---|---|---|
| `dialog-cancel`, `dialog-close` | `window-close` (brass ✕) | the **Cancel/Annulla** button on the logout screen |
| `system-suspend-hibernate` | `system-hibernate` | logout screen |
| `network-wired-activated` (+ wired states) | `network-workgroup` | **system tray** (this box is on Ethernet) |
| `network-wireless-connected` / signal states | `network-wireless` | system tray (Wi‑Fi) |
| `network-bluetooth-symbolic` (+ BT states) | `bluetooth-symbolic` / `bluetooth` | **system tray Bluetooth** (the known mono‑icon issue) |
| `klipper` | `edit-paste` | clipboard tray icon |
| `arrow-up`, `arrow-down` | `go-up`, `go-down` | system‑tray expander |
| `configure`, `application-menu`, `overflow-menu`, `open-menu-symbolic` | `preferences-system` / `open-menu` | context & hamburger menus |
| `krunner`, `plasma-search` | `system-search` | KRunner |
| `help-about`, `help-contents`, `system-help` | `help-browser` | Help menus |
| `user`, `user-identity` | `skillfish` (fish logo) | logout/Kickoff **avatar** (brand placeholder) |
| `emblem-favorite` | `starred` | favourites |
| `trash-empty`, `edit-clear`, `folder-new`, `system-run` | various | misc actions |

Full map: [`audit/alias_map.txt`](../audit/alias_map.txt) in the work tree.

## ✅ Resolved — art drop 2026‑06‑04

**All groups A–H below were drawn and shipped** in the `SkillFish-Steampunk-KDE`
theme package (icon set grown to ~452 names). After installing, the icon resolver
reports **every** visible‑shell candidate now resolving to `SkillFishSteampunk`
(the only fallback left is `yakuake`, which isn't installed). The KCM/System
Settings set is 46/46. Nothing below falls back to breeze any more.

The list is kept for reference / future contributors. Names are the exact base
names KDE requests (it also picks up `-symbolic` variants automatically).

### A. Logout / shutdown screen (high)
- `dialog-ok`, `dialog-ok-apply` — the confirm checkmark
- `system-reboot-update`, `system-shutdown-update` — reboot/shutdown **with the "updates pending" badge**
- *(a proper brass user avatar to replace the fish placeholder on `user` / `user-identity` — optional)*

### B. System tray (high — always on the panel)
- `notifications`, `notification`, `notification-inactive`, `notifications-disabled`,
  `notification-disabled-symbolic`, `preferences-desktop-notification` — the **notification bell**
- `system-software-update`, `update-none`, `update-low`, `update-medium`, `update-high` — Discover **update notifier**
- `battery`, `battery-full` — battery (KCM/energy; the board has no battery but the panel/KCM still references it)
- `plasmavault` — Plasma Vaults (if used)
- `kdeconnect`, `smartphone` — KDE Connect (if used)
- *(ideal, beyond the aliases: a proper Ethernet/plug icon for `network-wired-*` and a real Wi‑Fi signal‑strength set `network-wireless-signal-{none,weak,ok,good,excellent}`)*

### C. Dialogs & notifications (medium‑high)
- `dialog-information`, `dialog-warning`, `dialog-error`, `dialog-question` — message‑box icons
- `data-warning-symbolic`

### D. Dolphin / file manager (medium)
- `view-list-details`, `view-list-icons`, `view-list-tree` — view‑mode toolbar
- `view-sort`, `view-filter`, `view-group-symbolic`, `view-hidden`
- `edit-rename`, `document-preview`, `archive-extract`

### E. Keyboard / input (medium)
- `input-keyboard`, `preferences-desktop-keyboard`

### F. Window actions (low — KWin draws its own title buttons)
- `window-new`, `window-duplicate`
- `window-close`, `window-minimize`, `window-maximize`, `window-restore` (+ `-symbolic`) —
  present only in `_disabled_window_symbols/` (parked for the GTK‑app fix), so KDE
  menus take them from breeze. Left as‑is on purpose.

### G. System Settings — KCM module icons (low; only seen inside System Settings)
~45 `preferences-*` icons fall back to breeze. Lower priority because they're only
visible while configuring. Names:
`preferences-desktop-accessibility`, `-activities`, `-animations`, `-baloo`,
`-color`, `-cursors`, `-default-applications`, `-display-color`, `-display-randr`,
`-effects`, `-feedback`, `-filetype-association`, `-font`, `-font-installer`,
`-gaming`, `-icons`, `-keyboard-shortcut`, `-locale`, `-mouse`, `-notification-bell`,
`-plasma-theme`, `-sound`, `-tablet`, `-theme-applications`, `-theme-global`,
`-theme-windowdecorations`, `-thunderbolt`, `-touchpad`, `-touchscreen`,
`-user-password`, `-virtual`, `-wallpaper`; `preferences-system-power-management`,
`-users`, `-time`, `-network`, `-network-connection`, `-network-proxy`, `-login`,
`-session-services`, `-splash`, `-tabbox`, `-windows`, `-windows-actions`;
`preferences-security-firewall`, `preferences-smart-status`,
`preferences-web-browser-shortcuts`.

### H. Emblems / overlays (low)
- `emblem-mounted`, `emblem-symbolic-link`, `emblem-shared`, `tag`

---

> The aliases give an immediate brass look on every high‑traffic surface (panel,
> logout, menus). Groups A–C are the ones worth drawing next for a fully on‑brand
> system; D–H are progressively lower‑visibility.

# User avatars

Steampunk/brass user avatars for KDE Plasma, matching the SkillFish theme.
All are 256×256 PNG. KDE shows avatars masked to a **circle**.

- `SkillFish.png` — the default avatar (brass mechanical fish with the Debian swirl).
- `skillfish-portrait-01.png` … `-40.png` — **40 character portraits** in a round
  brass frame (inventors, aviators, aristocrats, masked figures, …).
- `skillfish-emblem-01.png` … `-28.png` — **28 object emblems** (raven, owl,
  butterfly, gears, diving helmet, mechanical hand/arm, airship, locomotive,
  clockwork heart, mask, compass, pocket watch, …).
- `steampunk-01.png` … `steampunk-28.png` — an earlier set of 28 gear‑framed
  characters/objects, circle‑masked (transparent corners).

> De‑dup note: the source pack also shipped `faces-square` (32 portraits) — the
> **same 32 subjects** as `skillfish-portrait-01..32` in a square frame. They are
> intentionally **not included** here (round frames suit KDE's circular display and
> avoid duplicate subjects). The 8 extra round portraits are `-33`…`-40`.

## Install (system‑wide gallery)

Copy them into the KDE avatar gallery so they're selectable in
**System Settings → Users → Choose a picture**:

```sh
cp SkillFish.png steampunk-*.png /usr/share/plasma/avatars/
```

## Set one as a user's avatar

The on‑disk avatar is a **square PNG**. KDE/SDDM read it via AccountsService:

```sh
# clean way (copies + writes the user record):
busctl call org.freedesktop.Accounts /org/freedesktop/Accounts/User1000 \
  org.freedesktop.Accounts.User SetIconFile s /usr/share/plasma/avatars/SkillFish.png
# fallback used by SDDM/login:
cp /usr/share/plasma/avatars/SkillFish.png ~/.face.icon
```

For the installer image, `/etc/skel/.face.icon` makes new users default to the fish.

`_preview.png` is a contact sheet of the set (not an avatar).

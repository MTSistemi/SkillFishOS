# User avatars

Steampunk/brass user avatars for KDE Plasma, matching the SkillFish theme.

- `SkillFish.png` — the default avatar (brass mechanical fish with the Debian swirl).
- `steampunk-01.png` … `steampunk-28.png` — a set of 28 gear‑framed characters
  (inventors, aviators, a raven, cats, an airship, a clockwork heart, …), cropped
  from a single sheet and masked to a clean circle (transparent corners).

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

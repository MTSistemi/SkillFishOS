# Distribution

Everything needed to publish SkillFishOS **26.06 "Aetherium"** (BC-250 release).

| Folder | What | Status |
|---|---|---|
| [`apt/`](apt/) | APT repository (suite `aetherium`, GPG-signed, kernel via wrapper) | ✅ **LIVE** at <https://mtsistemi.github.io/SkillFishOS/> (GitHub Pages, `gh-pages` branch) |
| [`sourceforge/`](sourceforge/) | Project metadata, release notes, ISO upload | ✅ **DONE** — [project](https://sourceforge.net/projects/skillfishos/) populated (description, blog, forum, wiki, GPLv3/Linux, GitHub code import) **and the 6 GB ISO is uploaded & set as the default Linux download** (`…/files/latest/download`) |
| [`distrowatch/`](distrowatch/) | Ready-to-send submission email | ⏳ **send the email** in `distrowatch/submission.md` to distro@distrowatch.com (the SourceForge URL is now rule-compliant) |

## Order of operations

1. ~~**Stand up the APT repo**~~ → **done**, live on GitHub Pages (`apt/README.md`).
2. **Host the ISO** → `sourceforge/UPLOAD.md` (5.6 GB, exceeds GitHub's 2 GB → SourceForge).
3. **Point the site** at the new download URL (`website/src/i18n.ts` → `SITE.isoUrl`, `isoSizeGb`).
4. **Submit to DistroWatch** → `distrowatch/submission.md` (only after step 2 — they need a working download).

## Release facts (single source of truth)

- Version: **26.06**, codename **Aetherium**, suite/codename `aetherium`
- Target: **AMD BC-250** (amd64); generic x86-64 to follow
- ISO: `SkillFishOS-26.06-Aetherium-BC250-amd64.iso` — 5.6 GB
- SHA-256: `8eea73d9dd23a1d8aa8fda3d8cc7639712b6391e2802282518c141145e1fce8c`
- Boots English; language/keyboard chosen at install. Open source.

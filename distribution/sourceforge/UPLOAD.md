# ISO upload checklist (SourceForge Files)

The Aetherium ISO is **5.6 GB** — too large for a GitHub Release asset (2 GB limit),
so the download is hosted on SourceForge (no size limit).

## Artifact (on the build box `192.168.5.40`)

```
/home/eggs/mnt/SkillFishOS-26.06-Aetherium-BC250-amd64.iso        (5.6 GB)
/home/eggs/mnt/SkillFishOS-26.06-Aetherium-BC250-amd64.iso.sha256
```

**SHA-256:**
```
8eea73d9dd23a1d8aa8fda3d8cc7639712b6391e2802282518c141145e1fce8c  SkillFishOS-26.06-Aetherium-BC250-amd64.iso
```

## Steps (turnkey — you only need a SourceForge account)

0. **Create the project** at <https://sourceforge.net/create/> — Unix/URL name **`skillfishos`**.
   Use the metadata in [`PROJECT.md`](PROJECT.md) (name, summary, categories, links, description).
1. Project → **Files** → **Add Folder** → `26.06-Aetherium`.
2. **Upload** the `.iso` and `.iso.sha256` into that folder. Two ways:
   - **Web**: drag the files from your Desktop copy
     (`C:\Users\Mattia\Desktop\SkillFishOS-26.06-Aetherium-BC250-amd64.iso`).
   - **scp (fast, from the build box)** — replace `<SFUSER>` with your SourceForge login:
     ```sh
     scp /home/eggs/mnt/SkillFishOS-26.06-Aetherium-BC250-amd64.iso* \
       <SFUSER>,skillfishos@frs.sourceforge.net:/home/frs/project/skillfishos/26.06-Aetherium/
     ```
3. Click the `.iso` → **⚙ → "Select as default download for: Linux"**.
4. Paste the release notes (`release-notes-26.06.md`) into the folder's README / project News.
5. **This is the URL to give DistroWatch** (transparent, non-cloud → rule-compliant):
   ```
   https://sourceforge.net/projects/skillfishos/files/26.06-Aetherium/SkillFishOS-26.06-Aetherium-BC250-amd64.iso/download
   ```
6. *(optional)* Point the **website** at SourceForge too, for one stable mirror:
   - `website/src/i18n.ts` → `SITE.isoUrl` → the URL above · keep `isoSizeGb: '5.6'`
   - or repoint `public/.htaccess` `/dl/...` 302 → SourceForge instead of Dropbox.
   *(The Dropbox-masked link can stay for the site; SourceForge is what DistroWatch needs.)*

## Verify after download

```sh
sha256sum -c SkillFishOS-26.06-Aetherium-BC250-amd64.iso.sha256
```

Tell me your SourceForge project URL once it's up and I'll fill the DistroWatch submission
(`../distrowatch/submission.md`) — it needs just the 4 fields.

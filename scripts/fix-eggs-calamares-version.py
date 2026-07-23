#!/usr/bin/env python3
# Make eggs' Calamares branding show the RELEASE NAME (26.06 Aetherium)
# instead of the build date, and fix the bootloader entry casing.
import shutil, os
f = "/usr/lib/penguins-eggs/dist/classes/incubation/branding.js"
with open(f, encoding="utf-8") as _f:
    s = _f.read()
if not os.path.exists(f + ".skfbak"):
    shutil.copy(f, f + ".skfbak")
reps = [
 ("const version = today.toISOString().split('T')[0]; // 2021-09-30",
  "const version = '26.06'; // SkillFishOS release (was build date)"),
 ("const shortVersion = version.split('-').join('.'); // 2021.09.30",
  "const shortVersion = '26.06';"),
 ("const versionedName = remix.fullname + ' (' + shortVersion + ')';",
  "const versionedName = remix.fullname + ' 26.06 Aetherium';"),
 ("const shortVersionedName = remix.versionName + ' ' + version;",
  "const shortVersionedName = remix.fullname + ' 26.06 Aetherium';"),
 ("bootloaderEntryName = distro.distroId;",
  "bootloaderEntryName = 'SkillFishOS';"),
]
ok = True
for a, b in reps:
    if a in s:
        s = s.replace(a, b); print("OK  :", a[:55])
    else:
        print("MISS:", a[:55]); ok = False
with open(f, "w", encoding="utf-8") as _f:
    _f.write(s)
print("written:", f, "all-matched=", ok)

#!/usr/bin/env python3
"""Third pass on scripts/build-debs-ci.sh (2026-09-11 evening).

    patch-ci-3.py <repo>

- skillfish-base postinst: install the EFI core-unlock program first in the
  boot order (only on a BC-250, only when the unlock is enabled, only with an
  ESP). Verified with a cold boot: one OS boot instead of two.
- new package skillfish-audio-dolby (MastaG/bc250-dual-audio).
Idempotent.
"""
import os
import sys

p = os.path.join(sys.argv[1], "scripts", "build-debs-ci.sh")
with open(p, encoding="utf-8") as f:
    t = f.read()

# ---- base postinst
if "skillfish-coreunlock-efi installa" not in t:
    i = t.index("\nP=skillfish-base\n")
    j = t.index("\nexit 0\nPOSTINST\n", i)
    blocco = """
# The 8-core unlock done BEFORE the bootloader (Hexxeh's EFI program, MIT):
# only on a BC-250, only where the user opted into the unlock, only with an
# ESP. Verified with a cold boot on the dev board (BIOS P3.00): one OS boot
# instead of two. The in-OS service stays as the fallback and does nothing
# when it finds the mask already at 0xFF.
if [ "$1" = configure ] && [ -x /usr/local/bin/skillfish-is-bc250 ] && /usr/local/bin/skillfish-is-bc250 >/dev/null 2>&1 \\
   && [ -e /etc/skillfish/core-unlock.abilitato ] && [ -d /boot/efi/EFI ]; then
  /usr/local/bin/skillfish-coreunlock-efi installa >/dev/null 2>&1 || true
fi"""
    t = t[:j] + blocco + t[j:]
    print("base postinst: coreunlock")

# ---- the Dolby package
if "P=skillfish-audio-dolby" not in t:
    a = "\nP=skillfish-scx\n"
    i = t.index(a)
    blocco = """
P=skillfish-audio-dolby
# Real-time Dolby Digital 5.1 over HDMI/DisplayPort (MastaG/bc250-dual-audio):
# a second sink that encodes AC-3 live for receivers that only take Dolby.
# The ALSA monitor override is rebased on WirePlumber 0.5.17 EXACTLY, hence
# the pinned dependency. License asked to the author (issue #1, 2026-09-11).
put $P 0644 system/etc/alsa/conf.d/61-bc250-a52.conf                          etc/alsa/conf.d/61-bc250-a52.conf
put $P 0644 system/etc/pipewire/pipewire.conf.d/60-bc250-ac3-output.conf      etc/pipewire/pipewire.conf.d/60-bc250-ac3-output.conf
put $P 0644 system/etc/wireplumber/wireplumber.conf.d/50-bc250-audio.conf     etc/wireplumber/wireplumber.conf.d/50-bc250-audio.conf
put $P 0644 system/usr/local/share/wireplumber/scripts/90-bc250-audio-mode.lua usr/local/share/wireplumber/scripts/90-bc250-audio-mode.lua
put $P 0644 system/usr/local/share/wireplumber/scripts/monitors/alsa.lua      usr/local/share/wireplumber/scripts/monitors/alsa.lua
put $P 0644 system/usr/share/doc/skillfish-audio-dolby/README.upstream.md     usr/share/doc/skillfish-audio-dolby/README.upstream.md
put $P 0644 system/usr/share/doc/skillfish-audio-dolby/UPSTREAM-COMMIT        usr/share/doc/skillfish-audio-dolby/UPSTREAM-COMMIT
ctrl $P "wireplumber (>= 0.5.17), wireplumber (<< 0.5.18), pipewire-audio, libasound2-plugins" "SkillFishOS Dolby Digital 5.1 - live AC-3 encoding over HDMI/DisplayPort" \\
  "Adds a second audio output, Dolby Digital 5.1 (AC3), that encodes the six
channels live at 640 kbps for AV receivers, soundbars and TVs that do not take
multichannel PCM. The normal HDMI/DisplayPort output stays as it is. Pick the
output in the system settings, it applies to every program. Work of MastaG
(bc250-dual-audio), packaged by SkillFishOS. Log out and in once after
installing."
"""
    t = t[:i] + blocco + t[i:]
    # build loop
    a2 = "for P in skillfish-control-center skillfish-tuner"
    assert a2 in t
    t = t.replace(a2, "for P in skillfish-control-center skillfish-audio-dolby skillfish-tuner", 1)
    # the check
    a3 = "check skillfish-control-center_${VER}_all.deb ./usr/share/polkit-1/actions/os.skillfish.control-center.policy '<allow_active>auth_admin_keep</allow_active>'\n"
    assert a3 in t
    t = t.replace(a3, a3 + "check skillfish-audio-dolby_${VER}_all.deb ./usr/local/share/wireplumber/scripts/monitors/alsa.lua 'bc250'\n", 1)
    print("pacchetto skillfish-audio-dolby")

with open(p, "w", encoding="utf-8") as f:
    f.write(t)
print("fatto")

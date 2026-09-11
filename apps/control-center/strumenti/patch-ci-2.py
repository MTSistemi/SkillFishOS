#!/usr/bin/env python3
"""Second pass on scripts/build-debs-ci.sh (2026-09-11): the community items.

    patch-ci-2.py <repo>

- skillfish-base: the STUBS ACPI table (e-tho, MIT), the Mesa driconf
  defaults, the shader-cache environment file, the PipeWire quantum, the EFI
  core-unlock program (Hexxeh, MIT) with its installer script.
- skillfish-control-center: Recommends python3-evdev (gamepad navigation).
Idempotent.
"""
import os
import sys

p = os.path.join(sys.argv[1], "scripts", "build-debs-ci.sh")
t = open(p, encoding="utf-8").read()

# ---- skillfish-base: after the existing ACPI puts
a = "put $P 0644 system/usr/share/skillfish/acpi/SSDT-CST.dsl              usr/share/skillfish/acpi/SSDT-CST.dsl\n"
n = a + """put $P 0644 system/usr/share/skillfish/acpi/SSDT-STUBS.aml            usr/share/skillfish/acpi/SSDT-STUBS.aml
put $P 0644 system/usr/share/skillfish/acpi/SSDT-STUBS.dsl            usr/share/skillfish/acpi/SSDT-STUBS.dsl
put $P 0644 system/usr/share/skillfish/acpi/LICENSE.SSDT-STUBS        usr/share/skillfish/acpi/LICENSE.SSDT-STUBS
# Mesa defaults for the APU (unified heap), the shader cache cap, the PipeWire
# quantum for games: three small files the community converged on (2026-09).
put $P 0644 system/usr/share/drirc.d/50-skillfish.conf                usr/share/drirc.d/50-skillfish.conf
put $P 0644 system/etc/environment.d/50-skillfish-mesa.conf           etc/environment.d/50-skillfish-mesa.conf
put $P 0644 system/etc/pipewire/pipewire.conf.d/50-skillfish-latency.conf etc/pipewire/pipewire.conf.d/50-skillfish-latency.conf
# The 8-core unlock done before GRUB: an EFI program (Hexxeh, MIT) plus the
# script that puts it first in the boot order. Nothing runs at boot unless
# `skillfish-coreunlock-efi installa` was called.
put $P 0644 system/usr/share/skillfish/coreunlock/bc250-unlock.efi    usr/share/skillfish/coreunlock/bc250-unlock.efi
put $P 0644 system/usr/share/skillfish/coreunlock/LICENSE             usr/share/skillfish/coreunlock/LICENSE
put $P 0644 system/usr/share/skillfish/coreunlock/main.c              usr/share/skillfish/coreunlock/main.c
put $P 0644 system/usr/share/skillfish/coreunlock/Makefile            usr/share/skillfish/coreunlock/Makefile
put $P 0755 system/usr/local/bin/skillfish-coreunlock-efi             usr/local/bin/skillfish-coreunlock-efi
"""
if "SSDT-STUBS.aml" not in t:
    assert a in t, "ancora ACPI put"
    t = t.replace(a, n, 1)
    print("skillfish-base: aggiunti")

# ---- control-center: python3-evdev recommended
a2 = "Replaces: skillfish-monitor (<< 26.09)"
if "python3-evdev" not in t:
    i = t.index(a2)
    j = t.index("\n", i) + 1
    t = t[:j] + """# gamepad navigation: optional, the window works without the module
sed -i 's/^Recommends: .*/&, python3-evdev/' "$OUT/$P/DEBIAN/control"
""" + t[j:]
    print("control-center: python3-evdev")

open(p, "w", encoding="utf-8").write(t)
print("fatto")

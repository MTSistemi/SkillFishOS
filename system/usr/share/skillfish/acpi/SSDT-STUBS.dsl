// From e-tho/bc250-acpi-fix (MIT, see LICENSE.SSDT-STUBS). Added to SkillFishOS 2026-09-11.
// Defines control methods the firmware calls but never provides: APTS and
// AWAK for sleep transitions, AFN7 for backlight. Each takes the argument the
// firmware passes and ignores it.
//
// AGESA defines its own sleep methods, but those only call further missing
// methods, so there is nothing to route to.

DefinitionBlock ("", "SSDT", 2, "HACK", "STUBS", 0x00000001)
{
    Method (\APTS, 1, NotSerialized) { }
    Method (\AWAK, 1, NotSerialized) { }
    Method (\AFN7, 1, NotSerialized) { }
}

// SSDT-P-CST-ALIAS-3S.dsl
DefinitionBlock ("", "SSDT", 2, "HACK", "P_CST3", 0x00000001)
{
    // Firmware objects we’re augmenting
    External (\_PR, DeviceObj)
    External (\_PR.P000, ProcessorObj)
    External (\_PR.P001, ProcessorObj)
    External (\_PR.P002, ProcessorObj)
    External (\_PR.P003, ProcessorObj)
    External (\_PR.P004, ProcessorObj)
    External (\_PR.P005, ProcessorObj)
    External (\_PR.P006, ProcessorObj)
    External (\_PR.P007, ProcessorObj)
    External (\_PR.P008, ProcessorObj)
    External (\_PR.P009, ProcessorObj)
    External (\_PR.P00A, ProcessorObj)
    External (\_PR.P00B, ProcessorObj)
    External (\_PR.P00C, ProcessorObj)
    External (\_PR.P00D, ProcessorObj)
    External (\_PR.P00E, ProcessorObj)
    External (\_PR.P00F, ProcessorObj)

    // 3-state C-state package mirroring your Zen2 laptop values
    Method (PCST, 0, NotSerialized)
    {
        Return (Package ()
        {
            0x03,   // number of C-states

            // C1: FFixedHW, BitWidth=0x02, BitOffset=0x02, Lat=0x0001, Power=0
            Package ()
            {
                ResourceTemplate ()
                {
                    Register (FFixedHW,
                        0x02,               // Bit Width
                        0x02,               // Bit Offset
                        0x0000000000000000, // Address
                        /* AccessSize omitted for FFixedHW */
                    )
                },
                0x01,           // C1 type
                0x0001,         // Latency (us)
                0x00000000      // Power (mW)
            },

            // C2: SystemIO @0x414, AccessSize=1, Lat=0x015E, Power=0
            Package ()
            {
                ResourceTemplate ()
                {
                    Register (SystemIO,
                        0x08,                   // Bit Width
                        0x00,                   // Bit Offset
                        0x0000000000000414,     // Address
                        0x01                    // Access Size
                    )
                },
                0x02,           // C2 type
                0x015E,         // Latency (us)
                0x00000000      // Power (mW)
            },

            // C3: SystemIO @0x415, AccessSize=1, Lat=0x0190, Power=0
            Package ()
            {
                ResourceTemplate ()
                {
                    Register (SystemIO,
                        0x08,                   // Bit Width
                        0x00,                   // Bit Offset
                        0x0000000000000415,     // Address
                        0x01                    // Access Size
                    )
                },
                0x03,           // C3 type
                0x0190,         // Latency (us)
                0x00000000      // Power (mW)
            }
        })
    }

    // Add _CST to each vendor processor
    Scope (\_PR.P000) { Method (_CST, 0, NotSerialized) { Return (PCST()) } }
    Scope (\_PR.P001) { Method (_CST, 0, NotSerialized) { Return (PCST()) } }
    Scope (\_PR.P002) { Method (_CST, 0, NotSerialized) { Return (PCST()) } }
    Scope (\_PR.P003) { Method (_CST, 0, NotSerialized) { Return (PCST()) } }
    Scope (\_PR.P004) { Method (_CST, 0, NotSerialized) { Return (PCST()) } }
    Scope (\_PR.P005) { Method (_CST, 0, NotSerialized) { Return (PCST()) } }
    Scope (\_PR.P006) { Method (_CST, 0, NotSerialized) { Return (PCST()) } }
    Scope (\_PR.P007) { Method (_CST, 0, NotSerialized) { Return (PCST()) } }
    Scope (\_PR.P008) { Method (_CST, 0, NotSerialized) { Return (PCST()) } }
    Scope (\_PR.P009) { Method (_CST, 0, NotSerialized) { Return (PCST()) } }
    Scope (\_PR.P00A) { Method (_CST, 0, NotSerialized) { Return (PCST()) } }
    Scope (\_PR.P00B) { Method (_CST, 0, NotSerialized) { Return (PCST()) } }
    Scope (\_PR.P00C) { Method (_CST, 0, NotSerialized) { Return (PCST()) } }
    Scope (\_PR.P00D) { Method (_CST, 0, NotSerialized) { Return (PCST()) } }
    Scope (\_PR.P00E) { Method (_CST, 0, NotSerialized) { Return (PCST()) } }
    Scope (\_PR.P00F) { Method (_CST, 0, NotSerialized) { Return (PCST()) } }

    // Keep the C000..C00F aliases so other AML resolves cleanly
    Scope (\_PR)
    {
        Alias (\_PR.P000, C000)
        Alias (\_PR.P001, C001)
        Alias (\_PR.P002, C002)
        Alias (\_PR.P003, C003)
        Alias (\_PR.P004, C004)
        Alias (\_PR.P005, C005)
        Alias (\_PR.P006, C006)
        Alias (\_PR.P007, C007)
        Alias (\_PR.P008, C008)
        Alias (\_PR.P009, C009)
        Alias (\_PR.P00A, C00A)
        Alias (\_PR.P00B, C00B)
        Alias (\_PR.P00C, C00C)
        Alias (\_PR.P00D, C00D)
        Alias (\_PR.P00E, C00E)
        Alias (\_PR.P00F, C00F)
    }
}


#include <efi.h>

#ifndef NULL
#define NULL ((void *)0)
#endif

#define MASK_REG 0x0115A870
#define MSG_WRITE_FF 0x98
#define Q3_CMD 0x03B10A20
#define Q3_RSP 0x03B10A80
#define Q3_ARG 0x03B10A88

// Set to 1 to halt the system after successful warm reboot validation instead of booting OS
#define TEST_MODE 0

// Freestanding helper routines for compiler intrinsic calls
void *memcpy(void *dest, const void *src, UINTN n) {
    unsigned char *d = (unsigned char *)dest;
    const unsigned char *s = (const unsigned char *)src;
    while (n--) {
        *d++ = *s++;
    }
    return dest;
}

void *memset(void *s, int c, UINTN n) {
    unsigned char *p = (unsigned char *)s;
    while (n--) {
        *p++ = (unsigned char)c;
    }
    return s;
}

// Direct PCI config space access helpers (Bus 0, Device 0, Function 0)
static inline void outpd(unsigned short port, unsigned int val) {
    __asm__ __volatile__("outl %0, %1" : : "a"(val), "Nd"(port));
}

static inline unsigned int inpd(unsigned short port) {
    unsigned int val;
    __asm__ __volatile__("inl %1, %0" : "=a"(val) : "Nd"(port));
    return val;
}

unsigned int smn_rd(unsigned int reg) {
    outpd(0xCF8, 0x80000000 | 0xB8);
    outpd(0xCFC, reg);
    outpd(0xCF8, 0x80000000 | 0xBC);
    return inpd(0xCFC);
}

void smu_wr(unsigned int reg, unsigned int val) {
    outpd(0xCF8, 0x80000000 | 0xB8);
    outpd(0xCFC, reg);
    outpd(0xCF8, 0x80000000 | 0xBC);
    outpd(0xCFC, val);
}

unsigned int smu_rd(unsigned int reg) {
    return smn_rd(reg);
}

int is_done(unsigned int status) {
    return (status == 0x01 || status == 0xFF || status == 0xFE || status == 0xFD || status == 0xFC);
}

int send_msg(EFI_SYSTEM_TABLE *SystemTable, unsigned int msg, unsigned int arg) {
    int timeout = 2500;
    while (!is_done(smu_rd(Q3_RSP)) && timeout > 0) {
        SystemTable->BootServices->Stall(2000);
        timeout--;
    }
    if (timeout <= 0) {
        return -1;
    }
    smu_wr(Q3_RSP, 0);
    smu_wr(Q3_ARG, arg);
    smu_wr(Q3_ARG + 4, 0);
    smu_wr(Q3_CMD, msg);
    
    timeout = 2500;
    while (timeout > 0) {
        unsigned int st = smu_rd(Q3_RSP);
        if (is_done(st)) {
            return (int)st;
        }
        SystemTable->BootServices->Stall(2000);
        timeout--;
    }
    return -2;
}

void print(EFI_SYSTEM_TABLE *SystemTable, UINT16 *str) {
    SystemTable->ConOut->OutputString(SystemTable->ConOut, str);
}

void print_hex(EFI_SYSTEM_TABLE *SystemTable, unsigned int val) {
    UINT16 buf[11];
    buf[0] = '0';
    buf[1] = 'x';
    for (int i = 7; i >= 0; i--) {
        unsigned int digit = (val >> (i * 4)) & 0xF;
        buf[9 - i] = (digit < 10) ? ('0' + digit) : ('A' + (digit - 10));
    }
    buf[10] = '\0';
    print(SystemTable, buf);
}

void print_hex_byte(EFI_SYSTEM_TABLE *SystemTable, unsigned char val) {
    UINT16 buf[5];
    buf[0] = '0';
    buf[1] = 'x';
    for (int i = 1; i >= 0; i--) {
        unsigned char digit = (val >> (i * 4)) & 0xF;
        buf[3 - i] = (digit < 10) ? ('0' + digit) : ('A' + (digit - 10));
    }
    buf[4] = '\0';
    print(SystemTable, buf);
}

EFI_STATUS efi_main(EFI_HANDLE ImageHandle, EFI_SYSTEM_TABLE *SystemTable) {
    // Read mask register
    unsigned int before = smn_rd(MASK_REG);
    unsigned char mask = before & 0xFF;

#if TEST_MODE
    print(SystemTable, L"BC-250 Core Unlocker EFI Utility\r\n");
    print(SystemTable, L"Current Core Mask: ");
    print_hex_byte(SystemTable, mask);
    print(SystemTable, L"\r\n");
#endif

    if (mask == 0xFF) {
#if TEST_MODE
        print(SystemTable, L"Cores already unlocked! (TEST_MODE active). Verification successful! Halting...\r\n");
        while (1) {
            __asm__ __volatile__("hlt");
        }
#endif
        // Cores are unlocked. Return EFI_SUCCESS to allow UEFI Boot Manager to proceed natively to option #2 in BootOrder!
        return EFI_SUCCESS;
    } else {
#if TEST_MODE
        print(SystemTable, L"Sending SMU message to unlock cores...\r\n");
#endif
        int st = send_msg(SystemTable, MSG_WRITE_FF, MASK_REG);
        if (st < 0) {
            print(SystemTable, L"Error: SMU mailbox timeout!\r\n");
            SystemTable->BootServices->Stall(5000000);
            return EFI_LOAD_ERROR;
        }
        if (st != 0x01) {
            print(SystemTable, L"Error: SMU Msg 0x98 returned status: ");
            print_hex(SystemTable, st);
            print(SystemTable, L"\r\n");
            SystemTable->BootServices->Stall(5000000);
            return EFI_LOAD_ERROR;
        }
        
        unsigned int after = smn_rd(MASK_REG);
        if ((after & 0xFF) != 0xFF) {
            print(SystemTable, L"Error: Core mask write failed to take effect!\r\n");
            SystemTable->BootServices->Stall(5000000);
            return EFI_LOAD_ERROR;
        }
        
        // Instant warm reboot
        SystemTable->RuntimeServices->ResetSystem(EfiResetWarm, EFI_SUCCESS, 0, NULL);
        
        while (1) {
            __asm__ __volatile__("hlt");
        }
    }
}

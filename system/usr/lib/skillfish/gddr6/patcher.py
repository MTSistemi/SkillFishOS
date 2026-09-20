"""Install only the pinned P3.0 payload, then verify it before switching Q3/5."""
import hashlib
import logging
from pathlib import Path

from bc250_smu.errors import SmuError
from unlock import unlock

PAYLOAD_START = 0x3AA9C
PAYLOAD_END = 0x3E000
HANDLER_REG = 0x748C
# ⚠️ THE ENTRY POINT IS NOT THE START OF THE PAYLOAD, and it moves every time
# the source does: the compiler puts the literal pool in front of the function,
# and the pool grows with the constants. 0x28 in upstream's build, 0x2C once we
# bounded the waits, 0x30 now that a message can ask for four chips. Get it from
# the ELF - `make handler` in payload/ - and never from memory. Point Q3/5 at
# the wrong address and the SMU jumps into the middle of a constant.
HANDLER = 0x3AACC
PAYLOAD_SHA256 = '58a41751e6958d657e3d05f309486948f495d6b719d53072c2bd8d8928c6b08b'
PAYLOAD_FILE = Path(__file__).resolve().parent / 'payload' / 'SMUPayload.bin'


def load_payload(path=PAYLOAD_FILE):
    data = Path(path).read_bytes()
    if (not data or len(data) % 4 or PAYLOAD_START + len(data) > PAYLOAD_END
            or hashlib.sha256(data).hexdigest() != PAYLOAD_SHA256):
        raise SmuError('payload size/hash does not match the bundled P3.0 build')
    return data


def check_platform(dmi=Path('/sys/class/dmi/id'), pci=Path('/sys/bus/pci/devices')):
    # DMI is a coarse compatibility gate, not a proof of the SMU firmware
    # contents. Custom firmware using the same DMI strings is unsupported.
    board = (dmi / 'board_name').read_text().strip()
    bios = (dmi / 'bios_version').read_text().strip()
    board_id = board.upper().replace('-', '').replace(' ', '')
    if board_id not in ('BC250', 'AMDBC250') or bios.upper() not in ('P3.0', 'P3.00'):
        raise SmuError(f'unsupported board/BIOS: {board!r} / {bios!r}; expected BC-250 P3.0')
    root_vendor = (pci / '0000:00:00.0' / 'vendor').read_text().strip().lower()
    if root_vendor != '0x1022':
        raise SmuError('PCI root is not AMD')
    for device in pci.iterdir():
        if ((device / 'vendor').read_text().strip().lower() == '0x1002'
                and (device / 'device').read_text().strip().lower() == '0x13fe'):
            return
    raise SmuError('BC-250 GPU (1002:13fe) not found')


def read_bytes(smu, start, size):
    return b''.join(smu.smu_read(addr, min(18, (start + size - addr) // 4))
                    for addr in range(start, start + size, 72))


def ensure_patch(smu, payload, allow_install=True):
    if not smu.alive():
        raise SmuError('SMU failed its initial probe')
    current = int.from_bytes(smu.smu_read(HANDLER_REG), 'little')
    installed = read_bytes(smu, PAYLOAD_START, len(payload))
    if current == HANDLER:
        if installed != payload:
            raise SmuError('Q3/5 points at an unexpected payload; reboot before retrying')
        return 'already_patched'
    if not allow_install:
        raise SmuError('SMU patch changed during this boot; reboot before retrying')
    # The slot may be empty before installation (observed on P3.00 with
    # verified SRAM transfers). Installing a new handler does not require an
    # existing handler. Still reject unexpected nonzero pointers.
    if current != 0 and (not 0x800 <= current < 0x40000 or PAYLOAD_START <= current < PAYLOAD_END):
        raise SmuError(f'unexpected original Q3/5 handler: 0x{current:08x}')

    logging.info('Preparing SMU patch; previous Q3/5 handler: 0x%08x', current)
    unlock(smu)
    logging.info('SMU access ready; uploading and verifying payload')
    for offset in range(0, len(payload), 4):
        smu.smu_write32(PAYLOAD_START + offset, int.from_bytes(payload[offset:offset + 4], 'little'))
    if read_bytes(smu, PAYLOAD_START, len(payload)) != payload:
        raise SmuError('payload readback mismatch; handler was not switched')
    smu.smu_write32(HANDLER_REG, HANDLER)
    if int.from_bytes(smu.smu_read(HANDLER_REG), 'little') != HANDLER:
        raise SmuError('handler readback mismatch')
    logging.info('SMU payload and Q3/5 handler verified')
    return 'patched'

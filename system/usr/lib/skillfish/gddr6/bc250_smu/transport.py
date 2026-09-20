import fcntl
import os
import struct


class Bc250PciTransport:
    """PCI config-space SMN window of the root device. Requires root.

    ⚠️ AN SMN ACCESS IS TWO SEPARATE WRITES: the address goes into config 0xB8,
    the value into 0xBC. Anything else driving the same window can land between
    them, and then our address takes somebody else's value - the SMU is handed a
    command nobody sent. On this distribution skillfish-gpu-freq-sampler reads
    the GPU clock through that very window every two seconds, and a malformed
    Q3/5 with a chip index out of range is enough to leave the SMU's handler
    spinning for ever: amdgpu stops getting its metrics table, the GPU sensors
    disappear, and only a reboot brings them back.

    So the pair is taken under flock on the config file itself. The file is the
    lock: every tool that reaches the SMU has it open already, ours and anybody
    else's, so there is no lock path to agree on first.

    bc250_smu_oc upstream added the same flock but takes it around each single
    config access rather than around the pair, which leaves open exactly the gap
    it was meant to close.
    """

    def __init__(self, bdf: str = "0000:00:00.0"):
        self._config_path = f"/sys/bus/pci/devices/{bdf}/config"
        self._fd = None

    def open(self) -> None:
        if self._fd is None:
            if os.geteuid() != 0:
                raise PermissionError("SMN window needs root")
            self._fd = os.open(self._config_path, os.O_RDWR | os.O_CLOEXEC)

    def close(self) -> None:
        if self._fd is not None:
            os.close(self._fd)
            self._fd = None

    def read_smu_reg(self, reg: int) -> int:
        fcntl.flock(self._fd, fcntl.LOCK_EX)
        try:
            self._write_word(reg, 0xB8)
            data = os.pread(self._fd, 4, 0xBC)
        finally:
            fcntl.flock(self._fd, fcntl.LOCK_UN)
        if len(data) != 4:
            raise OSError('short PCI config read')
        return struct.unpack("<I", data)[0]

    def write_smu_reg(self, reg: int, value: int) -> None:
        fcntl.flock(self._fd, fcntl.LOCK_EX)
        try:
            self._write_word(reg, 0xB8)
            self._write_word(value, 0xBC)
        finally:
            fcntl.flock(self._fd, fcntl.LOCK_UN)

    def _write_word(self, value, offset):
        if os.pwrite(self._fd, struct.pack('<I', value), offset) != 4:
            raise OSError('short PCI config write')

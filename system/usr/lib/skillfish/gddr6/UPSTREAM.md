# Upstream source

Source: https://github.com/pan-Rijovich/bc250-memory-temperature

Pinned commit: `b7e6bffcb5d592fc03edde375b7598ddc79aa846`.
The upstream MIT notice is preserved in `LICENSE.upstream`.

`bc250_smu/` and `unlock.py` are adapted from that revision. Only the API
operations needed by this collector are exposed. Changes include strict status
and transfer-length checks, one Q3 argument, shared transaction locking,
validated input ranges, no further commands after transport failure, full
DMA table readback using a cleared buffer, and restoring saved unlock regions
instead of hardcoded contents. No automatic rollback is attempted after a failed
SMU transaction because firmware may still be executing it.

SRAM reads now transfer the staged source twice into differently filled host
buffers and require matching results. This detects missing/partial DMA writes
that would otherwise be mistaken for zero-valued SRAM.

`bc250_smu/transport.py` takes an `flock` on the PCI config file around the
address/value pair. An SMN access is two separate writes - the address into
config `0xB8`, the value into `0xBC` - and anything else driving that window can
land between them, handing the SMU a command nobody sent. On this distribution
`skillfish-gpu-freq-sampler` reads the GPU clock through the same window every
two seconds; it takes the same lock now, and so does `skillfish-core-unlock`.
The config file is the lock, so there is no lock path for other tools to agree
on first. ⚠️ `bc250_smu_oc` upstream has the same `flock` but takes it around
each single config access instead of around the pair, which leaves open exactly
the gap it was meant to close.

## The payload is ours now, and this is why

The upstream handler waits for the memory controller with two loops that cannot
end:

```c
while (5      != umc_read(0, 0x53a20 | (umc_id << 20), 2)) {};
while (0x1234 == umc_read(0, 0x53a2c | (umc_id << 20), 2)) {};
```

One MR3 read that does not complete and the SMU spins inside the message handler
for ever. Measured on a BC-250 on 19 and 20/09/2026: it happened after 31 min,
after 55 min, and once after 5 - the spread of something with a probability per
read rather than a budget that runs out. The host timeout does not cancel
firmware execution, so there is no way back from it.

**And it takes the whole board with it.** With queue 3 stuck, queue 2 times out
too, `amdgpu` stops getting its metrics table (`SMU: No response msg_reg: 3d`),
the GPU temperature, power and busy sensors disappear, and every hwmon read
stalls for seconds inside the driver. `skillfish-fand` then misses its systemd
watchdog, systemd stops feeding the SP5100 hardware watchdog, and the machine
hard-resets about two minutes in. Reproduced twice on the dev board. A GPU reset
does not help: `amdgpu_gpu_recover` never even starts, because it queues behind
the same lock.

So the waits are counted now, and the chip index is checked before it is used to
build an address. A wait that runs out answers `SMU_RETURN_FAILED`; the collector
treats that as one missing reading and carries on, because the exchange
completed and the mailbox is still in step.

| | upstream | ours |
|---|---|---|
| binary | 176 bytes, sha256 `b3190846…` | 212 bytes, sha256 `4ba2528c…` |
| `umc_read_temp_per_chip` | `0x3AAC4` | `0x3AAC8` |
| index out of 0..7 | builds a wild SMN address | answered `0xFF` in 0 ms |
| memory controller does not answer | spins for ever | `0xFF` after `UMC_WAIT_MAX` |

`.text` still starts at `0x3AA9C`. ⚠️ The entry point moved because the literal
pool in front of the function grew by one word: read it from the ELF with
`make handler`, never from memory.

Before changing a line we rebuilt the **unmodified** upstream `main.c` with the
Espressif `xtensa-esp32-elf` gcc 5.2.0 toolchain and got their published binary
back byte for byte. That is what makes the rest of this trustworthy. See
`payload/Makefile` for the toolchain and the check.

Sent upstream: the unbounded loops affect every user of these projects, not just
ours.

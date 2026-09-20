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

## And four chips per message

Reading the eight chips cost eight mailbox round trips, one per chip. Every one
of them is an opportunity to get in the way of everything else that talks to
this SMU - our V/F governor several times a second, the clock sampler, amdgpu
itself - and that traffic is what turns a rare unlucky read into a hang.

A JEDEC temperature code is seven bits, so four of them fit in the single word
the queue gives back. The argument now says what is being asked for:

    0x00 .. 0x07   one chip, the code in the low byte, as upstream
    0x40           chips 0 1 2 3, one byte each, chip 0 in the low byte
    0x41           chips 4 5 6 7
    anything else  SMU_RETURN_FAILED, and nothing is touched

Eight round trips become two. Measured on the dev board: 2.3 ms against 9.0 ms
for the same eight readings, and 40 rounds of both side by side agree to within
0.55 °C on the worst chip, with the per-reading differences centred on zero and
none beyond ±4 - the jitter of a code that moves while you look at it, not an
offset.

⚠️ **An argument of `0x40` sent to the UPSTREAM payload does not fail, it
hangs.** That handler takes whatever number it is given, shifts it into an
address and waits for a memory controller that is not there. The host may only
ask for a group once `ensure_patch` has compared the installed SRAM against our
bundled binary, byte for byte - which is what it does before it returns.

The collector publishes the codes themselves in the snapshot now, rather than
the full 32-bit reads. Every reader masks with `0xFF` - our Monitor, the Control
Center, the dashboard and upstream's own C++ daemon - so nothing downstream can
tell the difference.

| | upstream | ours |
|---|---|---|
| binary | 176 bytes, sha256 `b3190846…` | 400 bytes, sha256 `58a41751…` |
| `umc_read_temp_per_chip` | `0x3AAC4` | `0x3AACC` |
| index out of 0..7 | builds a wild SMN address | answered `0xFF` in 0 ms |
| memory controller does not answer | spins for ever | `0xFF` after `UMC_WAIT_MAX` |
| eight chips | eight messages, 9.0 ms | two messages, 2.3 ms |

`.text` still starts at `0x3AA9C`. ⚠️ The entry point moved because the literal
pool in front of the function grew by one word: read it from the ELF with
`make handler`, never from memory.

Before changing a line we rebuilt the **unmodified** upstream `main.c` with the
Espressif `xtensa-esp32-elf` gcc 5.2.0 toolchain and got their published binary
back byte for byte. That is what makes the rest of this trustworthy. See
`payload/Makefile` for the toolchain and the check.

Sent upstream: the unbounded loops affect every user of these projects, not just
ours.

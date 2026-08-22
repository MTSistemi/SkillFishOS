# Reading what the BC-250 declares about itself

Two readers for the tables the GPU carries. They answer questions that guesswork
and web threads cannot: which hardware blocks this die actually has, and what the
video BIOS claims about them.

Neither reader hardcodes a struct. Both derive field names and offsets from the
kernel's own headers, so when AMD changes a table the reader changes with it
instead of printing wrong numbers with a confident face. Fetch the headers next
to the scripts before running:

```bash
K=https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/gpu/drm/amd
curl -sSLO $K/include/discovery.h -O $K/include/atomfirmware.h \
        -O $K/include/soc15_hw_ip.h -O $K/amdgpu/amdgpu_discovery.c
```

## The IP discovery table — what the silicon says it has

```bash
cat /sys/kernel/debug/dri/0/amdgpu_discovery > discovery.bin   # as root
python3 read-ip-discovery.py discovery.bin
```

Lists every block the die declares, its version, how many instances, and whether
it is harvested (fused off). It also prints the GC table, which is where the
40 CU come from: 2 shader engines x 2 arrays x 5 WGP.

The harvest table is the interesting one. On the BC-250 it is empty — the chip
declares nothing disabled, including the video engine.

## The ATOM tables — what the video BIOS claims

```bash
cat /sys/kernel/debug/dri/0/amdgpu_vbios > vbios.rom           # as root
python3 read-atom-tables.py vbios.rom
```

Prints the ROM header, every data table with its version and size, and decodes
the ones worth reading: firmware info, integrated system info, graphics, SMU,
display.

On the BC-250 this VBIOS identifies itself as "RBN Generic VBIOS" and its
graphics table describes a chip that does not exist — one shader engine, eight
CU per array. It is a placeholder. The driver does not believe it either: it
takes the real layout from the discovery table above. Worth remembering before
anyone builds a theory on a number read out of this ROM.

## Do not redistribute the dumps

The VBIOS image and the firmware blobs are AMD's. Dump them on your own board;
they are not in this repository.

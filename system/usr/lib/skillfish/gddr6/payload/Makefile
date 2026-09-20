# The SMU runs an Xtensa core, so this needs the Espressif toolchain - the same
# gcc 5.2.0 upstream used:
#
#   curl -LO https://dl.espressif.com/dl/xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz
#   tar xzf xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz
#   make CC=$PWD/xtensa-esp32-elf/bin/xtensa-esp32-elf-gcc \
#        OBJCOPY=$PWD/xtensa-esp32-elf/bin/xtensa-esp32-elf-objcopy
#
# Checked on 20/09/2026: building the UNMODIFIED upstream main.c with that
# toolchain reproduces their published binary byte for byte
# (sha256 b31908460e932a615d9eafb6b3112e6448994f9f6fa656d1d80a8616ac1df4df).
# Do that first whenever the toolchain changes - it is the only proof that what
# comes out of here is what we think we built, before writing it into a firmware
# that has no undo.
CC=./xtensa-esp32-elf-gcc-5.2.0/bin/xtensa-esp32-elf-gcc
OBJCOPY=./xtensa-esp32-elf-gcc-5.2.0/bin/xtensa-esp32-elf-objcopy
NM=$(dir $(CC))xtensa-esp32-elf-nm

CFLAGS = -mlongcalls \
           -mtext-section-literals \
          -Wall \
          -nostdlib \
          -Os \

LDFLAGS = -nostdlib \
          -T smu3.ld \
          -lgcc \


DEPS=

OBJS= main.o

NAME=SMUPayload

ELF=$(NAME).elf
BIN=$(NAME).bin

all: $(BIN)


%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

%.o: %.S $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

$(NAME).elf: $(OBJS) smu3.ld
	$(CC) -o $@ $(OBJS) $(LDFLAGS)

%.bin: %.elf
	$(OBJCOPY) -O binary $< $@

# ⚠️ WHERE THE HANDLER STARTS IS NOT WHERE THE PAYLOAD STARTS, and it moves when
# the source does. The compiler puts the literal pool first, so the function sits
# 0x28 into the upstream build and 0x2C into ours. That address goes into
# patcher.py as HANDLER, and it is read from the ELF rather than remembered:
#
#   make handler          ->   HANDLER = 0x0003aac8
#
# Point Q3/5 anywhere else and the SMU jumps into the middle of a constant.
.PHONY: handler
handler: $(ELF)
	@$(NM) $(ELF) | awk '$$3 == "umc_read_temp_per_chip" {print "HANDLER = 0x" $$1}'

.PHONY: clean
clean:
	rm -rf $(ELF) $(BIN) $(OBJS)
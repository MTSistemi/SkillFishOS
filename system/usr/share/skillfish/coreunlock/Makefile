# Target executable name
TARGET = bc250-unlock.efi

# Include directories for yoppeh-efi submodule (MIT Licensed)
INCLUDES = -I yoppeh-efi -DEFI_PLATFORM=1

# Detect OS and locate clang if on macOS
ifeq ($(shell uname), Darwin)
  BREW_LLVM_ARM = /opt/homebrew/opt/llvm/bin/clang
  BREW_LLVM_INTEL = /usr/local/opt/llvm/bin/clang
  ifneq ($(wildcard $(BREW_LLVM_ARM)),)
    CLANG = $(BREW_LLVM_ARM)
  else ifneq ($(wildcard $(BREW_LLVM_INTEL)),)
    CLANG = $(BREW_LLVM_INTEL)
  else
    CLANG = clang
  endif
  MINGW = x86_64-w64-mingw32-gcc
else
  CLANG = clang
  MINGW = x86_64-w64-mingw32-gcc
endif

# Default target
all: mingw

# Build using MinGW-w64 (works on Linux or macOS with 'brew install mingw-w64')
mingw:
	$(MINGW) $(INCLUDES) -nostdlib -mno-red-zone -shared -Wl,--subsystem,10 -e efi_main -o $(TARGET) main.c

# Build using Clang + LLD (works on Linux or macOS with 'brew install llvm')
clang:
	$(CLANG) $(INCLUDES) -target x86_64-unknown-windows -ffreestanding -mno-red-zone -nostdlib -fuse-ld=lld -Wl,-entry:efi_main -Wl,-subsystem:efi_application -o $(TARGET) main.c

clean:
	rm -f $(TARGET)

.PHONY: all mingw clang clean

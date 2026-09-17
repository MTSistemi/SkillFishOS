# The build machine

Everything that produces something we publish is built and signed on one
machine: the build VM, `192.168.5.25`, user `dev`. The two BC-250 boards are
for testing and benchmarking only.

Why it matters: until 12 September 2026 the kernel was built on the VM, the
packages on a board, the signatures on another board and the website on a
laptop. Every step lived in somebody's shell history, and two of them shipped
something different from what the repository said.

## What is on it

| | where |
|---|---|
| repository | `/home/dev/sfx-src` (pushes as Mattia Tadini <info@mtsistemi.it>) |
| kernel tree | `/home/dev/linux-tkg`, with our patches in `linux72-tkg-userpatches/` |
| Secure Boot key | `/root/.skillfishos-secureboot/SkillFishOS-SB.key`, 600 |
| archive and site credentials | `~/.skillfishos/deploy.env`, 600 |
| GitHub token | `~/.skillfishos/github.env`, 600 |
| key for the archive container | `~/.ssh/id_ed25519`, registered on `root@192.168.5.210` |

## Building

**The kernel**, both flavours, from the tree:

    bash ~/costruisci-725.sh          # copy it for the next version

It comes out in `~/DEBS-7.2.6/bc250/` and `~/DEBS-7.2.6/x64/`. The two differ in
`_processor_opt` (znver2 against x86-64) and `_kernel_localversion`: get one
wrong and the package looks right and does not boot on the target machine.

**The packages**:

    cd ~/sfx-src && bash scripts/build-debs-ci.sh 26.09.7

The version is the FIRST ARGUMENT, not an environment variable. Output in
`/tmp/sfx-debs/out/`.

**The website**:

    cd ~/sfx-src && bash scripts/costruisci-sito.sh

It counts what came out and refuses a site with no stylesheet. ⚠️ It puts
`TMPDIR` inside the home on purpose: `astro.config.mjs` writes into
`os.tmpdir()`, `/tmp` here is tmpfs, and Astro's final `rename()` cannot cross
two filesystems.

**The image** needs `live-build` and lives in `iso/`. It is the one step that
does NOT run unattended: an ISO is never built without Mattia saying so.

## Signing

    cd ~/sfx-src && bash kernel-build/scripts/firma-kernel.sh <linux-image-*.deb>

With Secure Boot on, a kernel nobody signed is refused by the shim and the
machine does not boot: that is issue #53. `scripts/publish-kernel.sh` refuses to
publish unsigned kernels, so this is not a reminder, it is a wall.

## Publishing

**apt** (GitHub Pages and the mirror at home):

    bash scripts/pubblica-apt.sh /tmp/sfx-debs/out/skillfish-*_26.09.7_all.deb

**GitHub Pages**, which is where installed systems and the ISOs actually get
their packages, is a separate step and is easy to forget:

    python3 scripts/sincronizza-ghpages.py 26.09.7

**A kernel release** on GitHub, with the .deb files as assets:

    GITHUB_TOKEN=$(sed -n s/^GITHUB_TOKEN=//p ~/.skillfishos/github.env) \
    DEBS_DIR=~/DEBS-7.2.6/bc250 bash scripts/publish-kernel.sh kernel-7.2.6-skillfishos

**The site**:

    bash scripts/pubblica-sito.sh

## Two things to keep in mind

The signing key is on this machine now. Whoever can log in here can sign a
kernel that our users' firmware will accept: the password of `dev` should not
stay what it is today, and the VM should not be reachable from outside the LAN.

And the boards are not build machines any more. If something can only be built
on a BC-250, that is a bug in the recipe, not a reason to go back.

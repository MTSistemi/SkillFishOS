# SkillFishOS 26.06.5 "Aetherium"

A new media release of "Aetherium" for the AMD BC-250. Two editions:
**BC-250** (`7.2.5-skillfishos`, znver2) and **Generic** (`7.2.5-skillfishos-x64`,
any x86-64 PC or VM). Boots in English; the language is chosen at install.

This is the release to use if you are on **26.06.4**. Three of the things fixed
below were found by installing the image and clicking through it, not by reading
a build log, and one of them stopped every application the system had just
installed for you.

## You choose what gets installed

Nothing is preinstalled any more, and that includes the browser. At the first
login a window asks what you want: Steam, Heroic, Lutris, a browser of your
choice (Firefox, Chrome, Chromium, Brave), the emulators, OnlyOffice. Each one
downloads with its own progress bar, and you can shut the machine down halfway
without losing anything: what is missing resumes by itself at the next boot.

Why they are not inside the image: they are about six gigabytes. Older images
carried them because the image was a clone of a working board, which is also
why they weighed 4.7 GB against the 2.9 GB of this one.

The window does not appear while you are trying the system from a USB stick.
There, six gigabytes of applications would land in RAM.

## The applications you install actually start

On a fresh 26.06.4-style install, every flatpak installed at first boot died
immediately:

    error: mkdirat(com.brave.Browser): Permission denied

A folder in your home, `~/.var`, was ending up owned by root, and from there
flatpak could no longer write anything for any application. The script that
prepares the games folder runs as root and created it while writing the Heroic
configuration.

It is fixed, and machines already installed repair themselves at the first
update: the repair runs on every pass, so nobody has to type a `chown`.

## Games have a place, and the pad works inside the flatpaks

`/games` is created and belongs to you, with `SteamLibrary` and `Heroic`
already inside. Steam and Heroic are configured to install there, and their
flatpak permissions include the devices: without that the controller is not
visible inside the sandbox, which on a games console means not playing.

## Encrypted disks: you can see what is being asked, and type it

Two things went wrong with an encrypted install, and both are fixed.

The boot screen asked for the passphrase **without drawing anything**. The
theme only painted the dots, and with zero characters typed there are no dots:
the screen sat on the splash with a still progress bar, and it looked frozen.
Typing the passphrase blind actually worked. Now the prompt from cryptsetup is
shown, with one dot per character.

And the passphrase had to be typed in **qwerty**, whatever your keyboard. The
piece that was missing was a package: `KEYMAP=y` was set and
`cryptsetup-initramfs` was installed, but `console-setup`, which is what
generates the keymap that goes into the initramfs, was not in the image.

## The system version now rises with your updates

Until now the version was written only by the install image. Whoever installed
from 26.06.4 stayed 26.06.4 for ever, however many updates they downloaded, and
the About page showed a number that was no longer true.

`/usr/lib/os-release` now travels inside `skillfish-base`, stamped with the
release number. It is installed through a `dpkg-divert`, so Debian's own file is
kept beside it and a `base-files` upgrade cannot take the branding back.

## AI mode, in three levels

The board can shut its desktop down to free memory for a language model, and now
in three steps chosen from the Control Center or from the Remote Manager: the
desktop alone, the desktop with Unsloth Studio, or `llama-server` by itself on
port 8888 with the same API and the same key. Measured on a board with a model
loaded: 567 MB of system memory becomes 115.

With the desktop down the screen is not black any more. A console shows the
board's name, the addresses it answers on, how much memory the model has, and
the way back.

## Also fixed

- **Icons.** Two sizes the theme shipped but never declared were invisible to
  everything, and one of them is where Heroic exports its only icon. A program
  we have no icon of our own for now shows its own instead of a generic one.
- **The menu notices new applications.** After the first-boot install the KDE
  cache is rebuilt inside your session, so what just arrived appears with its
  own icon instead of waiting for the next login.
- **CoolerControl is no longer in the image.** It was pulled from a third-party
  repository at build time.
- **The installer window** shows the release number in its title again: one of
  the four branding keys had been left three versions behind.

## Known limitations

- The Slim edition is not part of this release, and the slim kernel flavour was
  dropped after `7.2.0`. Only **main** and **x64** ship.
- The video engine of the BC-250 stays off: the silicon declares it, the kernel
  has no firmware for it, and the two donor firmwares we tried hang the board.
- FSR 4 does not run on this GPU.

## Verify your download

    sha256sum -c SkillFishOS-26.06.5-Aetherium-BC250-amd64.iso.sha256

    755f8893c15f0a41173802e849e58c7d8fda7522b0842fa1bc29de170c305e66  SkillFishOS-26.06.5-Aetherium-BC250-amd64.iso
    75038eb57b383cd64662d0571b12149ddb602e945fc85a4a2cfab5321ff0b172  SkillFishOS-26.06.5-Aetherium-Generic-amd64.iso

**Which image is for which machine.** The **BC-250** edition carries a kernel
built for that board's CPU: on an ordinary PC it shows the boot menu and then a
black screen. For any other x86-64 machine, or a virtual one, take **Generic**.

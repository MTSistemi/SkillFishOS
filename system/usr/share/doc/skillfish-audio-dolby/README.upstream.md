# BC-250 Dual Audio

Real-time Dolby Digital output for the AMD BC-250, while leaving the normal
HDMI/DisplayPort output completely untouched.

Tested against **CachyOS / PipeWire 1.6.x / WirePlumber 0.5.17 / AMD BC-250**.

---

## What problem does this solve?

The BC-250 outputs audio over DisplayPort. Plenty of gear on the other end of
that cable — AV receivers, soundbars, older TVs, HDMI audio extractors — cannot
accept multichannel LPCM, but *can* decode Dolby Digital. Without this project
you get stereo. With it you get real 5.1.

The catch is that the board exposes **one** physical audio device. Native PCM
and AC-3 both want to own it, and only one can at a time. Most of the code
here exists to arbitrate that safely: hand the hardware over cleanly on every
switch, and never let two backends collide (which shows up as `EBUSY`, a
disappearing sink, or silence).

## The two outputs

| Output | Shows up as | What it is | Use it when |
|---|---|---|---|
| **Native** | `alsa_output.pci-…hdmi-…` | Stock PipeWire HDMI/DP sink, untouched | Your display/receiver accepts multichannel LPCM. Lossless — always prefer this. |
| **AC-3** | `bc250_ac3` | Dolby Digital 5.1, encoded live (640 kbps default) | The chain can't take multichannel LPCM but decodes Dolby Digital. Widest compatibility. |

Selecting one is just picking the output in Steam, KDE, `pavucontrol` or
`wpctl` — no special tooling. The choice is **global**: every application
follows it. Per-app splits (Firefox on AC-3, Spotify on native) are deliberately
prevented, because they'd mean two owners of one device.

The native sink's channel count is whatever your display reports. This project
never hard-codes it.

## Install

On CachyOS with the [BC-250 repository](https://github.com/MastaG/linux-cachyos-bc250)
configured:

```bash
sudo pacman -Syu bc250-dual-audio
```

Otherwise, from a clone — run as your normal desktop user, **not** with sudo
(the script calls sudo itself):

```bash
./install.sh
```

The installer takes a rollback snapshot, installs the system-wide files and
restarts the audio stack. Reboot once before judging results in Steam Gaming
Mode.

### Requirements

- WirePlumber **0.5.17** — the ALSA monitor override is rebased on this exact
  version and `install.sh` refuses to install onto an unknown base
- `alsa-plugins` (the a52 encoder) and `alsa-utils` (`iecset`, for `check.sh`)

## Check that it works

```bash
/usr/share/bc250-dual-audio/check.sh     # packaged
./check.sh                               # from a clone
```

That prints the sinks, the current mode, what your display advertises, the live
IEC61937 channel status, and any recent errors. On a healthy system the
`recent PipeWire hardware errors` section reads `None.`

Then switch between both outputs a few times and confirm audio follows.

## Common problems

| Symptom | Most likely cause |
|---|---|
| Loud static / screeching | The sink can't decode what you're sending. Expected on a display with no Dolby decoder. |
| Audio stops after switching | Check for `EBUSY` in the PipeWire journal; that's a hardware handover failure. |

There is much more in **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)**.

## Configuration

Defaults are deliberate and most people should not change them. When you do need
to, nothing requires editing code.

**AC-3 bitrate** lives in `/etc/alsa/conf.d/61-bc250-a52.conf` as a plain
`bitrate` value; edit it there and restart WirePlumber. There is deliberately no
environment variable for it: AC-3 is encoded inside ALSA by the PipeWire daemon,
so there is no process of ours to pass one to.

The default is **640**, which is also AC-3's ceiling — the top of the codec's
frame-size table. Lower values are valid (448 was the default before v0.14) but
there is no reason to prefer one here: the encode is software and the link
carries 640 comfortably.

To send without the IEC61937 non-audio bit, point `ac3-alsa-path` at the
fallback PCM in `/etc/wireplumber/wireplumber.conf.d/50-bc250-audio.conf`:

```text
ac3-alsa-path = "plug:bc250_a52_noaes"
```

then restart WirePlumber.

> The sink is named `bc250_ac3`, with no bitrate in the name, because the
> bitrate is configurable and a name like `bc250_ac3_448` stops being true the
> moment you change it. v0.13 renamed it from `bc250_ac3_448`, and v0.14
> removed the E-AC-3 sink entirely; `install.sh` and the package both move a
> saved default across, but if you had pinned an output per application you may
> need to pick it again.

> If you hand-edit any file under `/etc`, note they are in the package's
> `backup=` set: pacman will **preserve your version and write `.pacnew`**
> instead of applying updates. Merge them, or your edits will silently block
> future fixes.

## Latency

AC-3 encodes *inside* PipeWire through the ALSA `a52` plugin, so PipeWire's own
quantum governs it — roughly 20–40 ms plus the 32 ms AC-3 frame, which is the
codec's own frame size and cannot be removed. AC-3 is close to its floor.

This is why v0.14 removed E-AC-3. That path ran through an external FFmpeg
process behind a FIFO, so its latency was the **sum of every buffer in the
chain** — they all filled at startup and nothing drained them again. v0.13 cut
it from roughly 780 ms to a little over 170 ms by sizing each stage explicitly,
but the floor was still an encoder frame, a prebuffer and several pipes, and it
stayed noticeably laggy in use. AC-3 at 640 kbps covers the same hardware
without any of it.

## No capability checks — on purpose

This project does not consult ELD/EDID before pushing a mode to the hardware. It
used to, and that was worse.

ELD is unreliable here: active and passive DP→HDMI adapters synthesise their own,
and it frequently does not describe what is actually downstream. Refusing a mode
because a lying adapter said so is more confusing than letting the sink reject it
audibly. So the selected mode is always attempted.

## Uninstall / rollback

```bash
./rollback.sh                      # restores the pre-install snapshot
sudo pacman -R bc250-dual-audio    # if installed from the repository
```

Package removal never touches the stock WirePlumber ALSA monitor — that file is
left exactly as its own package installed it.

## Documentation

| Document | What's in it |
|---|---|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | How the arbitration works: the mode arbiter, the encoder path, the ownership handshake, why the monitor override lives where it does |
| [docs/AUDIO-BACKGROUND.md](docs/AUDIO-BACKGROUND.md) | The domain knowledge: IEC61937, the non-audio bit, carrier rates, why ELD lies, FFmpeg's encoder limits, bitrate reasoning |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Symptom-driven diagnosis with the commands to run and how to read the output |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

## Files installed

```text
/etc/alsa/conf.d/61-bc250-a52.conf                        AC-3 encoder PCM
/etc/pipewire/pipewire.conf.d/60-bc250-ac3-output.conf    the virtual sink
/etc/wireplumber/wireplumber.conf.d/50-bc250-audio.conf   policy settings
/usr/local/share/wireplumber/scripts/monitors/alsa.lua    patched ALSA monitor
```

The mode arbiter lands in a different place depending on how you installed,
because the package follows distribution convention while `install.sh` is an
unmanaged install:

| File | `install.sh` | pacman package |
|---|---|---|
| mode arbiter | `/usr/local/share/wireplumber/scripts/` | `/usr/share/wireplumber/scripts/` |

If you have used both methods on one machine, check for leftovers from the
other.

The patched `monitors/alsa.lua` is a downstream rebase of the stock WirePlumber
0.5.17 script. It is installed under `/usr/local/share` so it shadows the stock
copy by search-path precedence — the file owned by the `wireplumber` package is
never modified. See [ARCHITECTURE.md](docs/ARCHITECTURE.md#why-usrlocalshare)
for why it can't live anywhere else.

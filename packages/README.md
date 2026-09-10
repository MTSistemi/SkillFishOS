# System packages

The application packages live in `apps/` and are built by `scripts/build-debs-ci.sh`.
The two packages here are different: they are not applications, they carry no
AppStream metadata, and they are built by hand because each one needs something
the CI machine does not have — a board to measure on, or a Mesa checkout.

They were kept outside the repository for months, which meant the only copy of
the governor's source was a directory on one board. That is fixed here.

## `skillfish-vf-governor`

The voltage/frequency governor for the BC-250, plus its watchdog, its trail
reader (`skillfish-vf-traccia`) and `skillfish-vf-rilascia`.

Build:

```
dpkg-deb --root-owner-group --build packages/skillfish-vf-governor \
         skillfish-vf-governor_<version>_all.deb
```

The version lives in `DEBIAN/control`. `etc/skillfish-vf-governor.json` is a
conffile: on upgrade dpkg keeps whatever the user has, so the curve shipped here
only reaches machines installing it for the first time.

**The curve is measured, not calculated.** The one in this tree stops at
2100 MHz / 1050 mV, and that ceiling is the result of a long evening of
benchmarks rather than a guess:

| Ceiling | What happened |
|---|---|
| 2040 / 990 | hangs the board at 40 CU on the first run |
| 2230 / 1129 | passes GravityMark and three Wukong runs, then hangs Cyberpunk in two and a half minutes |
| 2150 / 1080 | passes everything, then hangs the board after a dozen runs — marginal, and worth about 1 per cent |
| **2100 / 1050** | holds |

The lesson is in the table: Cyberpunk is the benchmark that finds these, because
it is the only one loading CPU and GPU hard at the same time, so it is the one
to run **first**. And a curve is not proven by three clean runs — 2150 fooled us
twice, once after nine and once after a dozen.

## `skillfish-mesa-gfx1013`

A RADV build that opens the compute queues on GFX1013. Worth 4.2 per cent on
Cyberpunk 2077 on a BC-250.

```
bash packages/skillfish-mesa-gfx1013/compila-mesa-pubblica.sh   # on a build host
bash packages/skillfish-mesa-gfx1013/pacchetto-mesa.sh
```

It installs under `/opt/skillfish-gfx1013` and never touches the system Mesa;
`skillfish-mesa on` writes the flatpak overrides for Steam and Heroic, `off`
puts them back.

⚠️ **It needs our kernel.** The fix opens queues that the stock driver keeps
closed on purpose, and on a kernel without the compute-queue lifecycle repair
(patches 0130/0131) those queues wedge the GPU.

⚠️ **The FSR 4 work is deliberately not here.** It is measured and it is large —
about 12 per cent in Cyberpunk with FSR 4 running — but the repository it comes
from (`dmorazasanchez/bc250-fsr4`) carries no licence at all, so we have no
permission to redistribute the patch or anything built from it. The compute-queue
fix, which we do ship, is MIT and credited in the package copyright.

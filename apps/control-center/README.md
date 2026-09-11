# SkillFishOS Control Center

One window for every SkillFishOS tool. Twelve sections, one word each:
Status, Tuner, Fan, Monitor, Games, Profiles, Kernel, Snapshots, AI,
Emulators, Console, ISO. The HUD stays a separate program; the Hub (the
software centre) stays separate too, because a shop is not a control.

```
skillfish-control-center [--pagina SECTION] [file.sfmon]
```

The old commands (`skillfish-tuner`, `skillfish-fan`, `skillfish-monitor`,
`skillfish-kernel-manager`, `skillfish-snapshots`, `skillfish-ai-panel`) still
exist: they open the right section. Their packages keep the daemons and
helpers (fan controller, CU router, snapshot helpers, Unsloth launcher) and
depend on this one.

## Layout

```
skillfish-control-center      the launcher (/usr/local/bin)
skillfish-cc-helper           the privileged helper, JSON per line over pkexec
sfcc/                         the program (/usr/share/skillfish/control-center)
  comune.py                   language, the "?" button, small file helpers
  stile.py                    palette, stylesheet, cards, tiles, badges
  grafico.py                  the one chart, and the curve editors inside it
  demone.py                   the helper client, started on the first write
  finestra.py                 sidebar + pages, built on first show
  pagine/*.py                 one module per section
lanciatori/                   the six compatibility launchers
i18n/*.json                   the strings of this window, merged into the
                              shared dictionaries by strumenti/unisci-i18n.py
../dashboard/web/             the same sections for the Remote Manager
                              (tuner.html, giochi.html, profili.html)
strumenti/                    the scripts that patch the CI build and the
                              dashboard, and the i18n tools
```

## The scheme every page follows

Tiles on the left are the legend and the values: click to show or hide a
line. One chart in the middle, scrolling in time. What you edit (a curve) sits
in a movable box inside the chart. Commands at the bottom; everything else
behind buttons that open panels on demand. Explanations live behind the "?"
next to what they explain, never in the page.

## The privileged helper

`skillfish-cc-helper` is a superset of the old `skillfish-tuner-helper`: every
command that one accepted still works, which is how the Remote Manager keeps
working with either. New commands:

| command | what |
|---|---|
| `gov-get` | the governor: curve, ceiling, tunables, service state, heartbeat |
| `gov-set` | validate and write the curve, restart the governor |
| `gov-prova` / `gov-conferma` / `gov-annulla` | the trial (below) |
| `gov-attiva` | switch between our governor and the stock one |
| `scx`, `scx-set`, `scx-azzera` | scx_bpfland armed through GameMode |
| `mesa-sistema`, `mesa-sistema-set` | our Mesa as the system Vulkan driver |
| `kernel`, `snapshot`, `manutenzione`, `ventola`, `servizio`, `gtt` | the other helpers, reached through this one so one password covers the window |

polkit: `auth_admin_keep` on the active session, `auth_admin` elsewhere.

### The trial

A curve that asks too little voltage hangs the board, and on the BC-250 a
hang is fixed by pulling the plug. So Apply never writes the candidate as the
curve that boots:

1. the current (known good) curve is copied aside;
2. the candidate is written and the governor restarted, so it loads it;
3. the known good curve is written back at once;
4. the window counts down 25 seconds; Keep writes the candidate for good,
   anything else (including the board dying) leaves the good curve on disk.

Two things learned the hard way while building this:

- `skillfish-vf-governor.service` allows three starts in five minutes. A trial,
  its confirmation and one more change are three; the fourth was refused and
  the governor stayed down with the board parked at 350 MHz. The helper runs
  `systemctl reset-failed` before every start.
- our Mesa as the system driver is a `dpkg-divert` of the 64-bit
  `libvulkan_radeon.so` (the 32-bit games keep Debian's). The diverted copy
  must NOT stay in `/usr/lib/x86_64-linux-gnu`: `ldconfig` sees a library whose
  SONAME is `libvulkan_radeon.so` and rebuilds the symlink to point at it,
  undoing the switch at the next apt run. It lives in
  `/var/lib/skillfish/mesa-distrib/`.

## Testing on a board

`installa-locale.sh --lancia <page>` installs the tree in place and opens the
window in the desktop session with a screenshot; `prova-gui.sh` drives it
from KRunner (so the process belongs to the logind session and polkit finds
its agent: a window launched from an ssh shell has no agent and every pkexec
fails). Both build the process name from pieces because a `pkill -f` pattern
typed on the ssh command line matches the ssh shell itself.

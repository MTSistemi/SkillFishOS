"""What covers each thing we ship.

EVERY EXECUTABLE in our packages needs an entry here, keyed by its path. A new
program with no entry fails the release check: that is the point. Each one also
gets a static check whatever its entry says (bash -n, a Python compile, or for
a binary: no missing shared library).

Entry kinds:
  ("run", cmd, expect)   run cmd as root; expect = dict with any of
                         rc (list of accepted exit codes, default [0]),
                         out (regex that must match stdout+stderr),
                         kinds (machines it applies to, default both)
  ("unit", name)         a daemon or boot job: covered when that unit is healthy
                         (checks_system) and, here, loaded
  ("gui", module)        a window: started offscreen by checks_gui
  ("helper", name)       exercised command by command by checks_helper
  ("manual", reason)     cannot be exercised automatically; the reason is printed
                         in every report, so it is never silently untested

BC = ("bc250",) marks what only makes sense on the board.
"""
BC = ("bc250",)
ANY = ("bc250", "x64")

EXECUTABLES = {
    # --- skillfish-base -------------------------------------------------------
    "/etc/kernel/postinst.d/00-skillfish-nct6687": ("manual", "kernel postinst hook: runs when a kernel is installed; covered by the kernel release check"),
    # upstream's overclock search stresses every core for minutes: only --help,
    # which still imports the whole bc250_smu module (the package is complete)
    "/opt/bc250_smu_oc/bc250_detect.py": ("run", "python3 /opt/bc250_smu_oc/bc250_detect.py --help",
                                          {"out": r"usage: bc250_detect"}),
    "/usr/local/bin/skillfish-acpi-pstates": ("run", "skillfish-acpi-pstates status", {}),
    "/usr/local/bin/skillfish-ai-console": ("manual", "the tty screen of AI mode; only runs inside AI mode"),
    "/usr/local/bin/skillfish-ai-mode": ("run", "skillfish-ai-mode stato", {"out": r"\{"}),
    "/usr/local/bin/skillfish-clean-live-autologin": ("manual", "live session cleanup; runs once after installation"),
    "/usr/local/bin/skillfish-cluster": ("helper", "cc-helper cluster stato"),
    "/usr/local/bin/skillfish-core-unlock": ("manual", "flips the SMU core mask and warm-reboots the board"),
    "/usr/local/bin/skillfish-coreunlock-efi": ("run", "skillfish-coreunlock-efi stato", {}),
    "/usr/local/bin/skillfish-cpu-governor": ("run", "skillfish-cpu-governor status", {"out": r'"ok": true'}),
    "/usr/local/bin/skillfish-crypto-fix": ("manual", "installer step (Calamares); needs an installation from the ISO"),
    "/usr/local/bin/skillfish-dp-hotswap.sh": ("unit", "skillfish-dp-hotswap.service"),
    "/usr/local/bin/skillfish-firstboot-snapshots.sh": ("manual", "first boot only; its result is checked by skillfish-rollback --elenco"),
    "/usr/local/bin/skillfish-fix-boot-extents": ("manual", "boot repair for issue #12; only acts on a sparse vmlinuz"),
    "/usr/local/bin/skillfish-fix-nct6687": ("manual", "rebuilds the fan module after a kernel change"),
    "/usr/local/bin/skillfish-flatpak-rimedi": ("manual", "repairs broken flatpak homes; acts only when something is broken"),
    "/usr/local/bin/skillfish-freeze-check.sh": ("unit", "skillfish-freeze-check.service"),
    "/usr/local/bin/skillfish-freeze-notify.sh": ("manual", "desktop notification after a freeze; needs a session and a recorded freeze"),
    "/usr/local/bin/skillfish-games-subvolume": ("run", "skillfish-games-subvolume stato", {}),
    "/usr/local/bin/skillfish-gpu-freq-sampler": ("unit", "skillfish-gpu-freq.service"),
    "/usr/local/bin/skillfish-gpu-util.sh": ("manual", "HUD helper; read by conky in a session"),
    "/usr/local/bin/skillfish-grub-btrfs": ("run", "skillfish-grub-btrfs stato", {}),
    "/usr/local/bin/skillfish-hud-gpu": ("manual", "MangoHud helper; runs inside a game"),
    "/usr/local/bin/skillfish-info": ("manual", "interactive: waits for Enter in a terminal"),
    "/usr/local/bin/skillfish-is-bc250": ("run", "skillfish-is-bc250", {"rc_by_kind": {"bc250": [0], "x64": [1]}}),
    "/usr/local/bin/skillfish-kde-firstrun.sh": ("manual", "first login of a user"),
    "/usr/local/bin/skillfish-live-no-lock": ("manual", "live session only"),
    "/usr/local/bin/skillfish-live-polkit": ("manual", "live session only"),
    "/usr/local/bin/skillfish-llama": ("manual", "starts the AI engine with a model; covered by the AI release notes check"),
    "/usr/local/bin/skillfish-repair-desktop": ("run", "skillfish-repair-desktop --dry-run", {"rc": [0, 1], "out": r"Nothing to (do|repair)|Plan"}),
    "/usr/local/bin/skillfish-rollback": ("run", "skillfish-rollback --elenco", {"out": r"\d"}),
    "/usr/local/bin/skillfish-secureboot": ("manual", "enrols keys in the firmware"),
    "/usr/local/bin/skillfish-snapshot-menu": ("manual", "rebuilds the GRUB snapshot menu; runs after every apt transaction"),
    "/usr/local/bin/skillfish-thermal-guard.sh": ("unit", "skillfish-thermal-guard.service"),
    "/usr/local/bin/skillfish-wipe-stale-luks": ("run", "skillfish-wipe-stale-luks --dry-run", {"out": r"nothing to do"}),
    "/usr/local/bin/skillfish-wol-arm": ("unit", "skillfish-wol.service"),
    # --- skillfish-boot -------------------------------------------------------
    "/usr/local/bin/skillfish-clean-cmdline": ("manual", "rewrites /etc/default/grub on non-BC-250 machines; runs from its package"),
    "/usr/local/bin/skillfish-sessione-x11": ("manual", "login session wrapper"),
    # --- skillfish-console ----------------------------------------------------
    "/opt/skillfish/steam-bin/steamos-session-select": ("manual", "switches the login session"),
    "/usr/local/bin/steamos-session-select": ("manual", "switches the login session"),
    "/usr/local/bin/skillfish-gaming-mode": ("manual", "starts the Big Picture session"),
    # --- skillfish-control-center ---------------------------------------------
    "/usr/local/bin/skillfish-cc-helper": ("helper", "cc-helper"),
    "/usr/local/bin/skillfish-control-center": ("gui", "skillfish-control-center"),
    # --- skillfish-dashboard --------------------------------------------------
    "/usr/local/bin/skillfish-dashboardd": ("unit", "skillfish-dashboard.service"),
    "/usr/local/bin/skillfish-dashboard-stop": ("manual", "stops the Remote Manager"),
    "/usr/local/bin/skillfish-hub-catalog": ("manual", "catalogue builder for the Remote Manager's Hub page"),
    "/usr/local/bin/skillfish-remote-ctl": ("manual", "remote control client"),
    "/usr/local/bin/skillfish-remote-manager": ("gui", "skillfish-remote-manager"),
    # --- skillfish-emulators --------------------------------------------------
    "/usr/local/share/skillfish/install-emudeck.sh": ("manual", "downloads and installs EmuDeck"),
    "/usr/local/share/skillfish/install-emulators.sh": ("manual", "downloads and installs emulators"),
    # --- skillfish-fan --------------------------------------------------------
    "/usr/local/bin/skillfish-fan": ("gui", "skillfish-fan"),
    "/usr/local/bin/skillfish-fand": ("unit", "skillfish-fand.service"),
    "/usr/local/bin/skillfish-fan-helper": ("helper", "cc-helper ventola scrivi/etichette"),
    # --- skillfish-gddr6 ------------------------------------------------------
    "/usr/local/bin/skillfish-gddr6-helper": ("helper", "cc-helper gddr6 avvia/ferma"),
    # --- skillfish-hub --------------------------------------------------------
    "/usr/local/bin/skillfish-hub": ("gui", "skillfish-hub"),
    "/usr/local/bin/skillfish-hub-helper": ("run", "skillfish-hub-helper conta", {}),
    "/usr/local/bin/skillfish-hub-local": ("manual", "adds third-party sources and keys"),
    "/usr/local/bin/skillfish-hub-notify": ("manual", "desktop notification; needs a session"),
    "/usr/local/lib/skillfish/hub-run": ("manual", "runs the Hub transaction under systemd"),
    # --- skillfish-iso-mount --------------------------------------------------
    "/usr/local/bin/skillfish-iso-mount": ("manual", "mounts an ISO the user picked in Dolphin"),
    # --- skillfish-kernel-manager ---------------------------------------------
    "/usr/local/bin/skillfish-kernel-helper": ("manual", "changes the default kernel or removes one"),
    "/usr/local/bin/skillfish-kernel-manager": ("gui", "skillfish-kernel-manager"),
    # --- skillfish-monitor ----------------------------------------------------
    "/usr/local/bin/skillfish-monitor": ("gui", "skillfish-monitor"),
    # --- skillfishos-archive-keyring ------------------------------------------
    "/usr/local/bin/skillfish-aggiorna-mirror": ("manual", "rewrites the mirror list from the signed copy; weekly timer"),
    # --- skillfish-primo-avvio ------------------------------------------------
    "/usr/local/bin/skillfish-giochi-cartella": ("manual", "first boot: creates the games folder"),
    "/usr/local/bin/skillfish-install-flatpaks": ("manual", "first boot: downloads the chosen software"),
    "/usr/local/bin/skillfish-primo-avvio": ("gui", "skillfish-primo-avvio"),
    "/usr/local/bin/skillfish-primo-avvio-helper": ("manual", "first boot installer helper"),
    # --- skillfish-scx --------------------------------------------------------
    "/usr/bin/skillfish-gamemode-fine": ("manual", "GameMode end hook; runs when a game quits"),
    "/usr/bin/skillfish-gamemode-inizio": ("manual", "GameMode start hook; runs when a game starts"),
    "/usr/bin/skillfish-scx": ("run", "skillfish-scx stato", {}),
    "/usr/lib/skillfish-scx/scx_bpfland": ("manual", "the scheduler itself; loaded by skillfish-scx while a game runs"),
    # --- skillfish-snapshots --------------------------------------------------
    "/usr/local/bin/skillfish-btrfs-manutenzione": ("manual", "btrfs balance and scrub; long"),
    "/usr/local/bin/skillfish-snapshots": ("gui", "skillfish-snapshots"),
    "/usr/local/bin/skillfish-snapshots-helper": ("helper", "cc-helper snapshot crea/cancella"),
    "/usr/local/bin/skillfish-snapshots-read": ("manual", "reads a snapshot for the GUI"),
    # --- skillfish-theme ------------------------------------------------------
    "/usr/local/bin/skillfish-first-login-wallpaper": ("manual", "first login of a user"),
    "/usr/local/bin/skillfish-menu-icon-fix": ("manual", "rebuilds the KDE menu cache for a user"),
    # --- skillfish-tuner ------------------------------------------------------
    "/usr/local/bin/skillfish-cu": ("run", "skillfish-cu get", {"out": r"active_cu", "kinds": BC}),
    "/usr/local/bin/skillfish-gpu-calibrate": ("manual", "measures the chip for minutes under load"),
    "/usr/local/bin/skillfish-gpu-verify": ("manual", "GPU stress verifier; long"),
    "/usr/local/bin/skillfish-hud": ("manual", "starts conky in a session"),
    "/usr/local/bin/skillfish-hud-bt": ("manual", "HUD helper; read by conky"),
    "/usr/local/bin/skillfish-hud-config": ("manual", "HUD configuration writer; used by the editor"),
    "/usr/local/bin/skillfish-hud-cpubars": ("manual", "HUD helper; read by conky"),
    "/usr/local/bin/skillfish-hud-editor": ("gui", "skillfish-hud-editor"),
    "/usr/local/bin/skillfish-hud-val": ("run", "skillfish-hud-val kernel", {"out": r"\d+\.\d+"}),
    "/usr/local/bin/skillfish-memcfg": ("manual", "writes the memory split to the firmware; never automatically"),
    "/usr/local/bin/skillfish-sensori": ("unit", "skillfish-sensori.service"),
    "/usr/local/bin/skillfish-tuner": ("gui", "skillfish-tuner"),
    "/usr/local/bin/skillfish-tuner-helper": ("manual", "the old Tuner helper; the Remote Manager's calls go through skillfish-cc-helper"),
    "/usr/local/bin/umr": ("run", "umr --help", {"rc": [0, 1], "out": r"(?i)usage|umr", "kinds": BC}),
    # --- skillfish-ai-panel ---------------------------------------------------
    "/usr/local/bin/skillfish-ai-panel": ("gui", "skillfish-ai-panel"),
    "/usr/local/bin/skillfish-gtt": ("manual", "changes the GTT limit on the kernel command line"),
    "/usr/local/bin/skillfish-unsloth": ("unit", "skillfish-unsloth.service"),
    "/usr/local/bin/skillfish-unsloth-update": ("manual", "downloads a new Unsloth"),
    "/usr/local/share/skillfish/install-unsloth.sh": ("manual", "downloads and installs Unsloth"),
    # --- packages built outside the app script --------------------------------
    "/usr/lib/skillfish/vkpeak/vkpeak": ("run", "cd /usr/lib/skillfish/vkpeak && stdbuf -oL -eL timeout 60 ./vkpeak",
                                         {"rc": [0, 124], "out": r"fp32-scalar\s*=\s*[0-9.]+"}),
    "/usr/bin/skillfish-mesa": ("run", "skillfish-mesa json", {"out": r"[{]"}),
    "/usr/lib/systemd/user-environment-generators/60-skillfish-vaapi": (
        "run", "/usr/lib/systemd/user-environment-generators/60-skillfish-vaapi",
        {"out_by_kind": {"bc250": r"LIBVA_DRIVER_NAME=bc250"}, "empty_by_kind": ("x64",)}),
    "/usr/bin/skillfish-vf-governor": ("unit", "skillfish-vf-governor.service"),
    "/usr/bin/skillfish-vf-rilascia": ("manual", "releases the governor's hold; used by its watchdog"),
    "/usr/bin/skillfish-vf-traccia": ("manual", "reads the governor trail; diagnostic"),
    "/usr/bin/skillfish-vf-watchdog": ("unit", "skillfish-vf-watchdog.service"),
    "/usr/lib/skillfish-vf-governor/stock-governor": ("manual", "fallback governor used when ours is off"),
}

# Paths our programs name that are allowed NOT to be installed by a package,
# each with the reason. Everything else they name under /opt, /usr/local/bin
# or /usr/lib/skillfish must exist and belong to a package (checks_exec).
PATHS_NOT_PACKAGED = {
    "/opt/bc250_memcfg/bc250memcfg": "legacy fallback: the Control Center uses the packaged skillfish-memcfg first",
    "/opt/bench/vkpeak": "legacy fallback: skillfish-vkpeak's /usr/lib/skillfish/vkpeak comes first (#91)",
    "/opt/skillfish-rpc": "created by skillfish-cluster on the boards it adds to the AI cluster",
    "/opt/skillfish-rpc/ggml-rpc-server": "created by skillfish-cluster on the boards it adds to the AI cluster",
    "/opt/unsloth/llama.cpp": "one of the places Unsloth may live; Unsloth is installed later by install-unsloth.sh",
    "/usr/local/bin/scx_lavd": "dead code in the old Tuner helper; skillfish-scx replaced it",
}

# Units shipped with an [Install] section that the package deliberately does
# not enable. Anything else must be enabled by its postinst OUTSIDE the
# /run/systemd/system test, or an ISO ships it off (issue #98).
UNITS_ON_DEMAND = {
    "skillfish-dashboard.service": "the Remote Manager: a LAN panel, switched on from the Control Center",
    "skillfish-scx.path": "the gaming scheduler: switched on from the Tuner",
    "skillfish-cluster.service": "AI cluster telemetry: set up by skillfish-cluster on the boards it joins",
    "skillfish-llama.service": "AI mode without Unsloth: chosen on the AI page",
    "skillfish-unsloth.service": "Unsloth Studio: installed later by the user, switched from the AI page",
    "bc250-smu-oc.service": "CPU clock at boot: enabled by Save at boot in the Tuner, after it writes the conf",
    "skillfish-thermal-guard.service": "enabled when the user sets a limit in the Tuner",
    "skillfish-gaming-mode.service": "switched on from the Control Center",
    "skillfish-vf-governor.service": "ships disabled on purpose (see its postinst): chosen in the Tuner",
    "skillfish-vf-watchdog.service": "goes with skillfish-vf-governor, enabled together with it",
}

# Minimum vkpeak fp32 on a BC-250 with the shipped curve. Measured 10144-10165
# on the .32 on 22/09/2026; below 9000 something is wrong with the GPU path.
VKPEAK_MIN_BC250 = 9000.0

# skillfish-cc-helper: every command it accepts. Unknown commands fail the run.
#   "read"     called and must answer ok
#   "write"    exercised by a named test in checks_helper (value put back)
#   "long"     exercised only with --long
#   "manual"   reason printed in the report
CC_COMMANDS = {
    "ping": "read", "get": "read", "gov-get": "read", "gov-mode": "read", "cpu-limits": "read",
    "cpu-cores": "read", "core-unlock": "read", "coreunlock-efi": "read", "thermal-guard-get": "read",
    "cu-get": "read", "cpu-gov": "read", "scx": "read", "mesa-sistema": "read", "unsloth-conf": "read",
    "cluster": "read", "ai-mode": "read",
    "gov-set": "write", "gov-prova": "write", "gov-conferma": "write", "gov-annulla": "write",
    "gov-attiva": "write", "apply-gpu": "write", "apply-cpu": "write", "persist-cpu": "write",
    "cpu-volatile": "write", "cpu-cores-set": "write", "cpu-smt": "write", "thermal-guard": "write",
    "cu-apply": "write", "cu-keep-boot": "write", "scx-set": "write", "scx-azzera": "write",
    "mesa-sistema-set": "write", "unsloth-conf-set": "write", "gddr6": "write", "servizio": "write",
    "bench-gpu": "write", "bench-cpu": "write", "cpu-gov-set": "write",
    "cu-test": "long", "test-gpu": "long", "test-cpu": "long", "suggest-uv": "long",
    "core-unlock-set": ("manual", "flips the SMU core mask and reboots"),
    "cpu-pstates-set": ("manual", "installs the ACPI P-state tables into the boot image; takes effect at the next boot"),
    "coreunlock-efi-set": ("manual", "installs or removes a UEFI boot entry"),
    "set-vram": ("manual", "writes the memory split to CMOS and needs a reboot"),
    "riavvia": ("manual", "reboots the machine"),
    "spegni": ("manual", "powers the machine off"),
    "kernel": ("manual", "changes the default kernel or uninstalls one"),
    "snapshot": "write",
    "manutenzione": ("manual", "btrfs balance and scrub; long"),
    "ventola": "write",
    "gtt": ("manual", "changes the GTT limit on the kernel command line"),
    "ai-livello": ("manual", "downloads a model"),
    "unsloth-password-reset": ("manual", "rotates the Unsloth Studio password"),
    "unsloth-key-set": ("manual", "replaces the Unsloth API key"),
}

# Contributing to SkillFishOS

Thank you for being here. SkillFishOS is a community project and it only grows if people pitch in. **Every kind of contribution counts** — code, packaging, theming, testing on real hardware, documentation, translations, or just a clear bug report.

## Ways to help

- **Test on real BC‑250 hardware.** The board has many revisions and quirks. Tell us what works, what doesn't, and on which BIOS.
- **Improve the kernel patches.** GPU clock range, the 40‑CU unlock, RDSEED, power/thermal behaviour — see [`kernel-build/`](kernel-build/) and [docs/OPTIMIZATIONS.md](docs/OPTIMIZATIONS.md).
- **Polish the desktop & theme.** KDE Plasma config, the SkillFish Steampunk theme ([`theme/`](theme/)), the Tuner, the HUD.
- **Packaging.** Help turn the manually‑tuned system into clean `.deb` packages and a proper APT repository.
- **Documentation & translations.** Make the docs clearer, or translate them (the desktop already ships IT/EN).
- **Triage & reproduce.** Confirm reported bugs, narrow them down, suggest fixes.

## Ground rules

- **English in the repository.** Issues, PRs, commits, code comments and docs are in English so everyone can take part.
- **One topic per PR.** Small, focused changes are reviewed and merged faster.
- **Explain the "why."** The BC‑250 is full of non‑obvious workarounds; a sentence on *why* a change is needed saves everyone time.
- **Test before you push**, and say what you tested it on (hardware revision, BIOS, kernel).
- **Respect the license.** Contributions are accepted under the project's [GPL‑3.0](LICENSE).

## Workflow

1. Fork the repo and create a branch (`fix/display-hpd`, `feat/tuner-fan-curve`, …).
2. Make your change. Keep commits clean; reference issues (`Fixes #12`).
3. Open a Pull Request describing **what** changed and **why**, and **how you tested it**.
4. A maintainer reviews. Iterate if needed. 🎉

## Good first issues

- Verify a documented workaround still applies on the latest sid packages.
- Improve a `docs/` page with details from your own setup.
- Add a missing icon/cursor variant to the theme.
- Report which controllers / monitors / printers work for you.

## Reporting bugs

Open an issue with:

- Hardware (BC‑250 revision, BIOS version) and how it's connected (display, audio, network).
- Kernel (`uname -r`) and whether you're on the prebuilt or self‑built kernel.
- Exact steps to reproduce, what you expected, what happened.
- Relevant logs (`journalctl`, `dmesg`) — trimmed to the relevant part.

## Security & credentials

Never commit passwords, tokens, or private keys. If you find a security issue, please report it privately rather than opening a public issue.

---

Not sure where to start? Open a discussion or a draft PR and ask. We'd rather help you land a contribution than have you give up. **Welcome aboard.** 🐟

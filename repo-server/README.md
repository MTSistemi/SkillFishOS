# APT repository server

The SkillFishOS APT repository is produced with `reprepro` and published to two
public mirrors:

| Mirror | URL | Who uses it |
|---|---|---|
| GitHub Pages | `https://mtsistemi.github.io/SkillFishOS` | **installed systems** — this is the source in `sources.list.d` |
| OVH | `https://skillfishos.com/apt` | manual use, and a fallback |

## Where it runs

Everything runs on a small LXC container on the house Proxmox, not on the
BC-250. The board is also the family console: indexing, signing and uploading
have no business stealing it from whoever is playing.

The container holds:

- `/srv/apt` — the reprepro tree, served over HTTP on the LAN by nginx. Useful
  to try a release before the world sees it.
- the archive signing key (`apt@skillfishos.com`, ed25519), in root's keyring.
- `/root/.skillfishos/deploy.env` — the OVH upload credentials, mode 600.

## Releasing

```sh
skillfish-rilascio pacchetto.deb [...]   # into "aetherium"
skillfish-rilascio --prova pacchetto.deb # into "aetherium-proposed"
skillfish-rilascio --dalla-scheda        # pull the freshly built .deb from the board
skillfish-rilascio --pubblica            # push it out to OVH
```

Without `--pubblica` nothing leaves the house. The upload step also deletes
`.deb` files the remote pool no longer references — without that, the pool grows
at every release and never shrinks. On 12 August 2026 it filled the hosting
quota mid-upload and left the repository incomplete, with `apt` erroring out for
anyone updating at that moment.

## Release checklist

Building the `.deb` is the middle of the job, not the end. The changelog inside
each package is generated from the git commits that touch **that** package's
files, so it takes care of itself. Nothing else does, and the parts that don't
are the parts a user actually reads.

1. Build everything: `OUT=/root/dist-debs bash scripts/build-debs-ci.sh <version>`
2. **If an application changed, open it on the board and use it.** Every tab,
   every filter, every dropdown, every button, at least once, looking at the
   result rather than assuming it. The build's "does it start?" step only
   executes the module body: on 22 August 2026 it was green while the shipped
   Hub showed no installed flatpaks at all and segfaulted on the first filter
   change. Both lived behind a click.
3. **Re-read the `ctrl()` description** of each package that changed. The Hub and
   `apt show` display it — it is the page a user sees before installing. Until
   22 August 2026 it said "built from git by CI" and nothing else, which told
   the reader precisely nothing.
4. **Update the `<release>` block in the app's metainfo.** That is the "What's
   new" shown when the app's page is opened in the Hub. **One entry only, the
   version being released** — old versions stacking up turn the page into a
   changelog nobody asked for, and the real changelog is generated from the
   commits anyway. Nine languages, as everywhere else, and `мВ` rather than `mV`
   in Cyrillic. If the only change is internal, say it is a maintenance release
   instead of inventing a feature.
5. Compare the **contents** against what is already published and ship only what
   changed. In 26.08.43 that was 5 packages out of 15; publishing all fifteen
   makes every user re-download 1.4 MB of identical files.
6. Copy the `.deb` files to the container and compare checksums **before**
   signing.
7. `skillfish-rilascio <files>` — indexes and signs, stays in the house.
8. `skillfish-rilascio --pubblica` — out to OVH.
9. From the PC: `python scripts/sincronizza-ghpages.py <version>` — the mirror
   installed machines actually use.
10. `apt update && apt install` on the board, from the real repository, not by
   hand. Then `appstreamcli refresh-cache --force`, or the Hub keeps reading the
   old catalogue and the new release notes never appear.
11. **The site news is for big things only.** FSR 4 working on the board, a Mesa
   build of our own, a new ISO, a feature that changes how the system is used.
   Not every point release: a note for each small fix drowns the news that
   matter. When you do write one, every language of the site — and then check
   the published site really shows it.

Steps 2, 4 and 11 are the ones that get skipped, and they are the ones the user
actually sees.

## Pulling from the board

`--dalla-scheda` copies the freshly built `.deb` files off the BC-250 over SSH.
Two things have to be set up once, and neither is visible from the code:

**A key for the container.** Without one, `scp` has no way to authenticate and
the pull fails. Generate it on the container and authorise it on the board,
scoped to the job it does:

```sh
# on the container
ssh-keygen -t ed25519 -N "" -C "skillfish-rilascio@container" -f /root/.ssh/id_ed25519

# on the board, in /root/.ssh/authorized_keys
from="192.168.5.103",restrict ssh-ed25519 AAAA... skillfish-rilascio@container
```

`from=` ties the key to the container's address and `restrict` removes the pty,
port forwarding and agent forwarding. It is allowed to copy files, nothing else.

**The board's host key, checked and registered.** The release command uses
`StrictHostKeyChecking=yes` on purpose: the packages that travel over this
connection are the ones we then sign with the archive key, so accepting whatever
answers means signing whatever a stranger hands us, and apt installs it without
a murmur because the signature says it is ours.

Compare the key from more than one machine before trusting it, then register it:

```sh
ssh-keyscan -t ed25519 192.168.5.40 >> /root/.ssh/known_hosts
```

If it is missing, the command stops and says so instead of connecting anyway.

## Distribution layout

Two suites, from `conf/distributions`:

- `aetherium` — the release everyone gets.
- `aetherium-proposed` — staging, for packages that should soak before landing.

The archive keyring is in `keyring/skillfishos-archive-keyring.asc`.

## History

This directory previously described a Docker-based setup (nginx, Portainer,
`docker-compose.yml`, `stack.yml`) from when the repository lived on a different
machine. That is gone — the files were removed rather than left to rot, since a
README describing infrastructure that no longer exists is worse than no README
at all. The old files remain in git history if they are ever needed.

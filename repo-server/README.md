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

# SkillFishOS Update Server

Self-hosted APT repository + container management for distributing SkillFishOS
updates (kernel, native apps, themes, branding) **independently of Debian sid**,
so upstream churn can't silently break the OS.

## Host
- **LXC unprivileged** on Proxmox, Debian 13 (trixie), `192.168.5.22`, hostname `Repository-SkillFishOS`.
- Prereqs for Docker in unprivileged LXC: `nesting=1` + `keyctl=1` (both on). Storage driver: native `overlayfs`.

## Stack
| Component   | Where                                  | Port(s)        | Purpose                                  |
|-------------|----------------------------------------|----------------|------------------------------------------|
| Docker CE   | host                                   | —              | container runtime                        |
| Portainer   | `docker compose` (`/opt/portainer`)    | 8000, **9443** | UI/management (`https://192.168.5.22:9443`) |
| Watchtower  | same compose (`nickfedor/watchtower`)  | —              | daily 04:00 auto-update of containers    |
| nginx repo  | Portainer stack `skillfishos-repo`     | **80**         | serves the APT repo                       |

> Watchtower: the classic `containrrr/watchtower` is unmaintained and breaks on
> Docker 29 (client API 1.25 < min 1.40). We use the maintained fork
> `nickfedor/watchtower`.

## APT repository (reprepro)
- Base: `/srv/skillfishos-repo` (`conf/`, `db/`, `dists/`, `pool/`).
- Codename: **`skillfishos`**, component `main`, arch `amd64` (+ `all`).
- Signed with GPG key `repo@skillfishos.com` (FPR `FD061357FED9E7A5A67A75C4C74AE764562980CF`).
  Private key lives only in the host's `/root/.gnupg` — **never committed**.
- Public keyring: `keyring/skillfishos-archive-keyring.asc` (served at
  `http://192.168.5.22/skillfishos-archive-keyring.asc`).

### Publish a package
```bash
/opt/skillfishos-repo/publish.sh path/to/foo_1.0_amd64.deb
# remove:
reprepro -b /srv/skillfishos-repo remove skillfishos <pkgname>
```
Packages **must** carry `Section:` and `Priority:` fields or reprepro rejects them.

## Client side (SkillFishOS / the ISO)
```bash
# keyring
curl -fsSL http://192.168.5.22/skillfishos-archive-keyring.asc \
  | gpg --dearmor -o /usr/share/keyrings/skillfishos-archive-keyring.gpg
# source (deb822)
cat > /etc/apt/sources.list.d/skillfishos.sources <<EOF
Types: deb
URIs: http://192.168.5.22
Suites: skillfishos
Components: main
Signed-By: /usr/share/keyrings/skillfishos-archive-keyring.gpg
EOF
```
This is intended to ship as the `skillfishos-archive-keyring` + `skillfishos-apt-config` packages.

## Credentials
Portainer admin: `admin` / see deployment notes (not committed).

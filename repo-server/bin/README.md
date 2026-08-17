# Release tooling

These four scripts run on the services container, not on the board and not on
the website host. Together they are the whole path a package takes from a
freshly built `.deb` to something a user's machine can install.

| Script | What it does |
|---|---|
| `skillfish-rilascio` | Puts `.deb` files into the `aetherium` suite with reprepro and regenerates the signed indexes. `--prova` targets `aetherium-proposed` instead, so a release can be rehearsed without the world seeing it. Without `--pubblica` nothing leaves the house. |
| `skillfish-carica-ovh` | Uploads the signed archive to `skillfishos.com/apt` over SFTP. |
| `skillfish-archivia` | Uploads release images to the Internet Archive over its S3 API. |
| `skillfish-stat-sourceforge` | Pulls download counts from the SourceForge API for the statistics page. |

## Credentials

None of these scripts contains a credential. Each reads one file:

    ~/.skillfishos/deploy.env      # OVH host, user, password  (SFTP)
    ~/.skillfishos/archive.env     # Internet Archive S3 access + secret key

Both are mode `600` and are never committed. Copies of the templates are next
to this file as `deploy.env.example` and `archive.env.example`.

The signing key lives only on the container, in a keyring reprepro owns. It has
deliberately **not** been put into a CI secret: see
`.github/workflows/publish-packages.yml`, which builds packages from git and
attaches them to a release but stops short of signing and publishing them.

## Where the board comes in

`skillfish-rilascio --dalla-scheda` fetches the `.deb` files from the build
machine. Its address is not hard-coded:

    SKILLFISH_BOARD=192.168.1.20 skillfish-rilascio --dalla-scheda --pubblica

The default is `skillfish-board.local`.

#!/usr/bin/env python3
"""The scheduler we actually run becomes the one we ship.

    scx-nel-repo.py <repo> <cartella con i file presi dalla scheda>

Fino a oggi il pacchetto skillfish-scx conteneva scx_lavd e un servizio spento,
mentre la scheda di sviluppo girava da settembre con un'altra cosa: scx_bpfland
acceso solo mentre gira un gioco, agganciato a GameMode, con un contatore di
espulsioni che lo ferma dopo due. Quei file non erano mai stati messi nel
repository: il Control Center descriveva quello e l'utente riceveva l'altro.

Questo script mette i file al loro posto e riscrive la sezione del CI.
"""
import os
import shutil
import sys

repo, src = sys.argv[1], sys.argv[2]

COPIE = [
    ("skillfish-scx", "system/usr/bin/skillfish-scx", 0o755),
    ("skillfish-gamemode-inizio", "system/usr/bin/skillfish-gamemode-inizio", 0o755),
    ("skillfish-gamemode-fine", "system/usr/bin/skillfish-gamemode-fine", 0o755),
    ("skillfish-scx.path", "system/lib/systemd/system/skillfish-scx.path", 0o644),
    ("skillfish-scx.service", "system/lib/systemd/system/skillfish-scx.service", 0o644),
    ("scx_bpfland", "vendor/scx/scx_bpfland", 0o755),
]
for nome, dest, modo in COPIE:
    d = os.path.join(repo, dest)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copyfile(os.path.join(src, nome), d)
    os.chmod(d, modo)
    print("messo %s (%d KB)" % (dest, os.path.getsize(d) // 1024))

# ---- the CI section -------------------------------------------------------------
ci = os.path.join(repo, "scripts", "build-debs-ci.sh")
with open(ci, encoding="utf-8") as f:
    s = f.read()

inizio = s.index("P=skillfish-scx\n")
fine = s.index("P=skillfish-base\n", inizio)
NUOVA = '''P=skillfish-scx
put $P 0755 vendor/scx/scx_bpfland                        usr/lib/skillfish-scx/scx_bpfland
put $P 0755 system/usr/bin/skillfish-scx                  usr/bin/skillfish-scx
put $P 0755 system/usr/bin/skillfish-gamemode-inizio      usr/bin/skillfish-gamemode-inizio
put $P 0755 system/usr/bin/skillfish-gamemode-fine        usr/bin/skillfish-gamemode-fine
put $P 0644 system/lib/systemd/system/skillfish-scx.path    lib/systemd/system/skillfish-scx.path
put $P 0644 system/lib/systemd/system/skillfish-scx.service lib/systemd/system/skillfish-scx.service
ctrl $P "systemd, gamemode" "SkillFishOS scheduler - scx_bpfland while a game runs" \\
  "A CPU scheduler loaded into the kernel through sched_ext, the one CachyOS
uses. It runs ONLY while a game runs: GameMode raises a flag when the game
starts, a .path unit starts the scheduler, and the flag going away stops it.
If the kernel ejects it twice the service refuses to start again until the
counter is reset, because a scheduler that keeps being ejected wedges the
desktop every forty seconds. Turn it on from the Control Center or from the
Remote Manager."
# ⚠️ I GANCI DI GAMEMODE STANNO IN /etc/gamemode.ini, che non e' di nessun
# pacchetto: Debian ne spedisce solo l'esempio. Quindi il file lo tocchiamo noi,
# aggiungendo le due righe se non ci sono, e le togliamo quando il pacchetto se
# ne va. Senza quelle due righe il pacchetto e' installato e non si accende mai:
# nessun errore, nessun sintomo, solo niente.
cat > "$OUT/$P/DEBIAN/postinst" <<'POSTSCX'
#!/bin/sh
set -e
if [ "$1" = configure ]; then
    INI=/etc/gamemode.ini
    [ -f "$INI" ] || { [ -f /usr/share/gamemode/gamemode.ini ] && cp /usr/share/gamemode/gamemode.ini "$INI"; }
    [ -f "$INI" ] || printf '[custom]\\n' > "$INI"
    if ! grep -q 'skillfish-gamemode-inizio' "$INI"; then
        if grep -q '^\\[custom\\]' "$INI"; then
            sed -i 's|^\\[custom\\]|[custom]\\nstart=/usr/bin/skillfish-gamemode-inizio\\nend=/usr/bin/skillfish-gamemode-fine|' "$INI"
        else
            printf '\\n[custom]\\nstart=/usr/bin/skillfish-gamemode-inizio\\nend=/usr/bin/skillfish-gamemode-fine\\n' >> "$INI"
        fi
    fi
    mkdir -p /var/lib/skillfish
    [ -f /var/lib/skillfish/scx-espulsioni ] || echo 0 > /var/lib/skillfish/scx-espulsioni
    # ⚠️ NON si accende da solo: il .path si abilita dal Control Center. Il
    # servizio comunque non parte se il kernel non ha sched_ext.
    systemctl daemon-reload 2>/dev/null || true
fi
exit 0
POSTSCX
chmod 0755 "$OUT/$P/DEBIAN/postinst"
cat > "$OUT/$P/DEBIAN/prerm" <<'PRESCX'
#!/bin/sh
set -e
if [ "$1" = remove ]; then
    systemctl disable --now skillfish-scx.path 2>/dev/null || true
    systemctl stop skillfish-scx.service 2>/dev/null || true
    sed -i '\\|^start=/usr/bin/skillfish-gamemode-inizio$|d; \\|^end=/usr/bin/skillfish-gamemode-fine$|d' /etc/gamemode.ini 2>/dev/null || true
fi
exit 0
PRESCX
chmod 0755 "$OUT/$P/DEBIAN/prerm"

'''
s = s[:inizio] + NUOVA + s[fine:]
with open(ci, "w", encoding="utf-8", newline="\n") as f:
    f.write(s)
print("riscritta la sezione skillfish-scx del CI")

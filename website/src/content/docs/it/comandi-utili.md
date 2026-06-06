---
title: Comandi utili
description: Cheat-sheet dei comandi da terminale per diagnosticare e regolare SkillFishOS.
group: Riferimenti
order: 4
---

SkillFishOS è pensato per **non** richiedere il terminale: il [Tuner](/docs/app-native) e le app grafiche bastano per l'uso normale. Questa pagina è per chi vuole **smanettare** o diagnosticare. Comandi privilegiati = con `sudo`.

> 🛟 Prima di esperimenti rischiosi, ricorda la rete di sicurezza: snapshot Btrfs e rollback dal menu GRUB (vedi [Storage e snapshot](/docs/storage-snapshot)).

## Sistema e kernel

```bash
uname -r                      # versione kernel in uso (deve finire con -skillfishos)
cat /proc/cmdline             # parametri di avvio attivi
journalctl -b -p err          # errori dell'avvio corrente
inxi -Fxxxz                   # riepilogo hardware completo
```

## GPU, frequenze e temperature

```bash
# frequenza/temperatura GPU dal sysfs amdgpu
cat /sys/class/drm/card*/device/hwmon/hwmon*/temp1_input   # °C ×1000
# stato del governor SMU della GPU
systemctl status cyan-skillfish-governor
cat /etc/cyan-skillfish-governor/config.toml               # safe-point freq/volt
# monitoraggio GPU in tempo reale
nvtop        # oppure: radeontop
```

> Sulla BC-250 il controllo frequenze **non** passa dal sysfs amdgpu standard ma dal **governor SMU**. Modifica i valori dal [Tuner](/docs/app-native), non a mano.

## CPU — overclock/undervolt

```bash
systemctl status bc250-smu-oc.service   # "inactive" dopo l'applicazione è normale (one-shot)
cat /etc/bc250-smu-oc.conf              # frequenza/tensione applicate
lscpu | grep MHz                        # frequenze correnti dei core
sensors                                 # temperature/tensioni (nct6686, k10temp)
```

## Verifica 40 Compute Unit

```bash
# le 40 CU dipendono dal parametro kernel amdgpu.bc250_cc_write_mode=3
grep bc250_cc_write_mode /proc/cmdline
vulkaninfo | grep -i "deviceName\|driverName"   # GPU vista da Vulkan (RADV)
```

Benchmark rapido (gli stessi usati dal Tuner):

```bash
vkpeak                # throughput FP32 (GFLOPS)
clpeak                # banda memoria (GB/s)
sysbench cpu run      # stress/benchmark CPU
```

## Memoria unificata (VRAM/GTT)

```bash
cat /proc/cmdline | tr ' ' '\n' | grep -E 'gttsize|ttm'   # parametri GTT/TTM
glxinfo | grep -i "memory"                                 # memoria vista dal driver
free -h                                                     # RAM/GDDR6 condivisa
```

## Gaming

```bash
flatpak list                         # app Flatpak (Steam, emulatori EmuDeck…)
flatpak update                        # aggiorna le app Flatpak
gamescope -- %command%               # (da impostare nelle opzioni di avvio di Steam)
# Bluetooth controller
bluetoothctl                         # scan on / pair / connect / trust
```

## AI locale

```bash
# lo stack gira in container Docker (vedi pannello AI)
docker ps                            # container attivi (ollama, openwebui, dockge)
docker compose -f <stack> up -d      # avvia lo stack
docker compose -f <stack> down       # ferma e libera GPU/RAM
ollama list                          # modelli installati (es. qwen3:14b)
```

## Snapshot e rollback (Btrfs)

```bash
sudo snapper list                    # elenco snapshot
sudo snapper create -d "prima di X"  # snapshot manuale
sudo btrfs subvolume list /          # sottovolumi (@rootfs, @home)
# il rollback più semplice è dal menu GRUB → "SkillFishOS snapshots"
```

## Aggiornamenti e repository

```bash
sudo apt update && sudo apt full-upgrade   # aggiorna il sistema
apt-mark showhold                          # pacchetti bloccati (incl. il kernel)
sudo apt install skillfishos-kernel        # installa/aggiorna il kernel dal repo
apt policy <pacchetto>                      # da quale repo/versione viene un pacchetto
```

## Rete e accesso remoto

```bash
nmcli device status                  # stato interfacce di rete
ip a                                 # indirizzi IP
systemctl status x11vnc              # server VNC per il desktop remoto
hostname -I                          # IP da usare col client VNC
```

## Display (HPD DisplayPort)

```bash
systemctl status skillfish-dp-hotswap   # demone che aggira l'HPD rotto
xrandr                                   # uscite e risoluzioni (sessione X11)
```

## Fonti

- [Wiki Btrfs](https://btrfs.readthedocs.io/) · [Snapper](http://snapper.io/)
- [Mesa / RADV](https://docs.mesa3d.org/drivers/radv.html) · [vulkaninfo](https://github.com/KhronosGroup/Vulkan-Tools)
- [Arch Wiki](https://wiki.archlinux.org/) — riferimento per molti comandi Linux

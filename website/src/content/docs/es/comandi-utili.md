---
title: Órdenes útiles
description: Una chuleta de terminal para diagnosticar y ajustar SkillFishOS.
group: Referencia
order: 4
---

SkillFishOS está pensado para **no** necesitar la terminal: para el uso normal bastan el [Tuner](/es/docs/app-native) y las aplicaciones gráficas. Esta página es para quien quiere **trastear** o diagnosticar. Las órdenes con privilegios usan `sudo`.

> Antes de experimentos arriesgados, recuerda la red de seguridad: instantáneas Btrfs y vuelta atrás desde el menú de GRUB (ver [Almacenamiento e instantáneas](/es/docs/storage-snapshot)).

## Sistema y núcleo

```bash
uname -r                      # núcleo en marcha (debe acabar en -skillfishos)
cat /proc/cmdline             # parámetros de arranque activos
journalctl -b -p err          # errores del arranque actual
inxi -Fxxxz                   # resumen completo del hardware
```

## GPU, frecuencias y temperaturas

```bash
# temperatura de la GPU desde el sysfs de amdgpu
cat /sys/class/drm/card*/device/hwmon/hwmon*/temp1_input   # °C ×1000
# estado del gobernador SMU
systemctl status cyan-skillfish-governor
cat /etc/cyan-skillfish-governor/config.toml               # puntos seguros de frecuencia y voltaje
# vigilancia de la GPU en tiempo real
nvtop        # o: radeontop
```

> En la BC-250 el control de la frecuencia **no** pasa por el sysfs estándar de amdgpu, sino por el **gobernador SMU**. Cambia los valores desde el [Tuner](/es/docs/app-native), no a mano.

## CPU — overclock y undervolt

```bash
systemctl status bc250-smu-oc.service   # que quede «inactive» tras aplicar es normal (es de una sola pasada)
cat /etc/bc250-smu-oc.conf              # frecuencia y voltaje aplicados
lscpu | grep MHz                        # frecuencias actuales de los núcleos
sensors                                 # temperaturas y voltajes (nct6686, k10temp)
```

## Unidades de cómputo en caliente (skillfish-cu)

```bash
skillfish-cu get          # estado en JSON: CU activas y máscara por fila (SE/SH)
sudo skillfish-cu max     # poner en marcha todas las CU (40)
sudo skillfish-cu stock   # volver a 24 (mínimo del controlador)
sudo skillfish-cu set 0x1f   # máscara WGP para todas las filas (0x07=24 … 0x1f=40)
cat /run/skillfish/cu_active # «40/40» (también lo lee el HUD)
vulkaninfo | grep -i "deviceName\|driverName"   # la GPU tal como la ve Vulkan (RADV)
```

Las CU se manejan mejor desde la **rejilla** del [Tuner](/es/docs/app-native) (clic y perfiles, con «Prueba de CU»). Las primeras 24 están fijadas por el controlador y siempre encendidas.

Mediciones rápidas (las mismas que usa el Tuner):

```bash
vkpeak                # rendimiento FP32 (GFLOPS)
clpeak                # ancho de banda de memoria (GB/s)
sysbench cpu run      # carga y medición de la CPU
```

## Memoria unificada (VRAM y GTT)

```bash
cat /proc/cmdline | tr ' ' '\n' | grep -E 'ttm\.'   # parámetros de GTT/TTM
glxinfo | grep -i "memory"                                 # memoria vista por el controlador
free -h                                                     # RAM/GDDR6 compartida
```

## Juegos

```bash
flatpak list                         # aplicaciones Flatpak (Steam, emuladores de EmuDeck…)
flatpak update                        # actualizar las aplicaciones Flatpak
gamescope -- %command%               # (ponerlo en las opciones de lanzamiento de Steam)
# mandos por Bluetooth
bluetoothctl                         # scan on / pair / connect / trust
```

## IA local

```bash
# un solo servicio propio, sin contenedores: Docker no está instalado
systemctl status skillfish-unsloth   # estado del motor de IA
sudo systemctl start skillfish-unsloth   # arrancarlo
sudo systemctl stop skillfish-unsloth    # pararlo y liberar GPU y memoria
curl -s localhost:8888/              # la interfaz de Unsloth Studio (solo loopback)
```

## Instantáneas y vuelta atrás (Btrfs)

```bash
sudo snapper list                    # listar instantáneas
sudo snapper create -d "antes de X"  # instantánea a mano
sudo btrfs subvolume list /          # subvolúmenes (@, @home, @log, @cache, @games)

# volver a una instantánea de verdad (surte efecto en el siguiente arranque)
sudo skillfish-rollback --list       # qué instantáneas hay
sudo skillfish-rollback 12           # hacer que la instantánea 12 sea el sistema
sudo skillfish-rollback --undo       # te has arrepentido: devolver el anterior
sudo skillfish-rollback --clean      # quitar los sistemas apartados por vueltas atrás previas

# desde el menú de GRUB → «SkillFishOS snapshots» obtienes la misma instantánea
# EN SOLO LECTURA: sirve para mirar y rescatar archivos; luego ejecuta la orden de arriba
```

## Actualizaciones y repositorio

```bash
sudo apt update && sudo apt full-upgrade   # actualizar el sistema
apt-mark showhold                          # paquetes retenidos (incluido el núcleo)
sudo apt install skillfishos-kernel        # instalar o actualizar el núcleo desde el repositorio
apt policy <paquete>                        # de qué repositorio y versión viene un paquete
```

## Red y acceso remoto

```bash
nmcli device status                  # estado de las interfaces de red
ip a                                 # direcciones IP
systemctl status x11vnc              # servidor VNC para el escritorio remoto
hostname -I                          # IP para usar con el cliente VNC
```

## Pantalla (HPD del DisplayPort)

```bash
systemctl status skillfish-dp-hotswap   # servicio que sortea el HPD averiado
xrandr                                   # salidas y resoluciones (sesión X11)
```

## Fuentes

- [Wiki de Btrfs](https://btrfs.readthedocs.io/) · [Snapper](http://snapper.io/)
- [Mesa / RADV](https://docs.mesa3d.org/drivers/radv.html) · [vulkaninfo](https://github.com/KhronosGroup/Vulkan-Tools)
- [Arch Wiki](https://wiki.archlinux.org/) — referencia de muchas órdenes de Linux

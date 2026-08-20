---
title: Instalación
description: Cómo grabar la ISO, arrancar el instalador y terminar la configuración.
group: Instalación
order: 1
---

SkillFishOS se instala desde una **ISO en vivo** que trae el instalador gráfico [Calamares](https://calamares.io/). Todo el proceso se hace con el ratón, sin terminal.

> La ISO **26.06.4 «Aetherium»** está disponible — descárgala desde la página de [Descarga](/es/download). Arranca en **inglés** para ser universal y te deja elegir idioma y teclado durante la instalación.

## Requisitos

- una placa **AMD BC-250** (ver [hardware](/es/docs/hardware-bc250));
- un **SSD o NVMe** donde instalar;
- un monitor conectado por **DisplayPort** (un adaptador DP→HDMI *pasivo* puede servir, pero mira las notas sobre imagen y audio en [Solución de problemas](/es/docs/risoluzione-problemi));
- una **memoria USB de al menos 8 GB** para el instalador;
- teclado y ratón para la instalación.

## 1. Graba la ISO en el USB

Descarga la ISO desde la página de [Descarga](/es/download) y grábala en una memoria con una de estas herramientas:

- **[balenaEtcher](https://etcher.balena.io/)** (Windows/macOS/Linux, con ventana, recomendado);
- **[Ventoy](https://www.ventoy.net/)** (permite guardar varias ISOs en la misma memoria);
- desde una terminal de Linux con `dd`:

```bash
sudo dd if=SkillFishOS_amd64.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

> Sustituye `/dev/sdX` por el dispositivo correcto de tu memoria. **Cuidado**: `dd` escribe sin preguntar y borra todo lo que haya en el destino.

## 2. Arranca la BC-250 desde el USB

Pon la memoria, enciende la placa y entra en el menú de arranque o en la UEFI para elegir el USB como dispositivo de arranque. Se iniciará el entorno **en vivo** de SkillFishOS (KDE Plasma): puedes recorrer el sistema antes de instalarlo.

## 3. Instala con Calamares

Desde el escritorio en vivo abre el instalador (icono *Install SkillFishOS*). Calamares te lleva paso a paso:

1. **Idioma y zona horaria.**
2. **Teclado.**
3. **Particionado.** SkillFishOS usa **Btrfs** con subvolúmenes separados: `@` (sistema), `@home` (tus datos), `@cache` y `@log` (fuera de las instantáneas), `@games` (la biblioteca de juegos). Así puedes *volver atrás* el sistema sin tocar tus archivos. Una pequeña partición **EFI** completa el reparto, y el intercambio es un **archivo**, no una partición. Para la mayoría, la opción automática («Borrar disco») va bien.
4. **Usuario.** Crea tu cuenta (quedará en los grupos correctos para juegos, audio, render, etc.).
5. **Resumen e instalación.**

Cuando termine, reinicia y saca la memoria.

## 4. Primer arranque

En el primer arranque **está todo configurado**: núcleo optimizado, gobernador, overclock, estética, juegos e instantáneas activos. No hace falta ajustar nada a mano.

Desde aquí puedes:

- emparejar tus [mandos](/es/docs/gaming) (DualShock 4 por Bluetooth o un mando por USB);
- añadir tus juegos a [Steam o EmuDeck](/es/docs/gaming);
- encender la [IA local](/es/docs/ai-locale) cuando la necesites;
- ajustar el hardware con el [Tuner](/es/docs/app-native) si te apetece.

## Reparto del disco

| Partición | Sistema de archivos | Contenido |
|---|---|---|
| `nvme0n1p1` | FAT32 (EFI) | gestor de arranque GRUB |
| `nvme0n1p2` | **Btrfs** | `@` (sistema) · `@home` (datos) · `@cache` · `@log` · `@games` · `@swap` |

No hay partición de intercambio: el intercambio es un **archivo** dentro del subvolumen `@swap`. En Btrfs se cambia de tamaño sin tocar la tabla de particiones, y se queda fuera de las instantáneas.

## Fuentes

- [Calamares](https://calamares.io/) — el instalador universal
- [balenaEtcher](https://etcher.balena.io/) · [Ventoy](https://www.ventoy.net/)
- [Wiki de Btrfs](https://btrfs.readthedocs.io/) — subvolúmenes e instantáneas

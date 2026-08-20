---
title: Introducción
description: Qué es SkillFishOS, por qué existe y para quién está pensado.
group: Introducción
order: 1
---

**SkillFishOS** es una distribución de Linux diseñada y ajustada para una placa concreta y poco común: la **AMD BC-250**. Es un sistema *PC-consola* listo para usar —juegos, emulación, IA en el propio equipo y trabajo diario de escritorio— construido sobre [Debian](https://www.debian.org/) y [KDE Plasma 6](https://kde.org/plasma-desktop/), con una estética steampunk coherente desde el arranque hasta el escritorio.

## La idea

La BC-250 nació como placa para minar criptomonedas y acabó en el mercado de segunda mano a precios muy bajos. Bajo el disipador, sin embargo, hay una **APU semipersonalizada de AMD** de la misma familia de silicio que las consolas de la generación actual: CPU Zen 2, gráficos RDNA 2 y 16 GB de GDDR6. Con el software adecuado se convierte en un PC-consola pequeño y sorprendentemente capaz.

El problema es que hacer que funcione bien en Linux exige parches del núcleo, un gobernador de frecuencia propio, overclock, perfiles térmicos y una larga lista de rodeos para el hardware. SkillFishOS existe para **hacer todo ese trabajo una sola vez** y entregar un sistema que *«se enciende y rinde al máximo»*, sin que haga falta tocar la terminal.

> SkillFishOS no distribuye juegos ni ROMs: pone las **herramientas** (Steam, EmuDeck, emuladores, interfaces). El contenido lo añades tú, legalmente.

## Para quién es

El proyecto nació de una necesidad concreta y personal: **que los niños usen y aprendan Linux mientras juegan**. Los juegos son la zanahoria que los atrae, y las **instantáneas automáticas** de Btrfs son la red de seguridad que permite experimentar sin miedo a romper el sistema: si algo sale mal, vuelves atrás con un clic desde el menú de arranque.

Así que SkillFishOS encaja bien con:

- quien tiene una **BC-250** y quiere jugar sin convertirse en experto del núcleo de Linux;
- **familias** que buscan una consola barata que además sea un PC educativo;
- **quien disfruta trastear** y prefiere partir de una base ya ajustada en vez de rehacerlo todo desde cero.

## Qué lleva dentro, en corto

- Un **núcleo a medida** ([linux-tkg](https://github.com/Frogging-Family/linux-tkg)) con los parches de la BC-250: 40 unidades de cómputo desbloqueadas, frecuencias liberadas, un gobernador SMU propio.
- Un **escritorio KDE Plasma 6** con estética steampunk (iconos, cursores, fondo, HUD del sistema).
- **Listo para jugar**: Steam, [gamescope](https://github.com/ValveSoftware/gamescope), [EmuDeck](https://www.emudeck.com/), [ES-DE](https://es-de.org/), [Heroic](https://heroicgameslauncher.com/), Proton.
- **IA en el propio equipo**: [Unsloth Studio](https://unsloth.ai/) acelerado con Vulkan en la GPU integrada — **5,1×** más rápido que en CPU, medido.
- **Instantáneas Btrfs** con [Snapper](http://snapper.io/) y vuelta atrás desde el menú de GRUB.
- **Aplicaciones propias**: el *Tuner* (control del hardware sin terminal) y el panel de *IA*.
- **Actualizaciones propias y probadas** desde nuestro repositorio APT, para que las de Debian no te den sorpresas.

Las páginas siguientes tratan cada componente en detalle.

## Fuentes

- Documentación de la comunidad BC-250 — [bc250.info](https://bc250.info)
- Documentación de la AMD BC-250 (elektricm) — [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- Debian — [debian.org](https://www.debian.org/)
- KDE Plasma — [kde.org/plasma-desktop](https://kde.org/plasma-desktop/)

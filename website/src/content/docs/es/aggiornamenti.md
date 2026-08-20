---
title: Actualizaciones y repositorio
description: Cómo se actualiza SkillFishOS sin que Debian sid lo rompa.
group: Uso
order: 4
---

SkillFishOS se basa en **Debian sid** (*unstable*), la rama de desarrollo de Debian: siempre al día, pero por naturaleza expuesta a algún retroceso. En hardware «exótico» como la BC-250, una actualización mala (de Mesa, del firmware o del núcleo) puede romper el sistema. SkillFishOS lo aborda con dos herramientas.

## 1. Componentes propios, desde un repositorio dedicado

Las partes más delicadas las compilamos y distribuimos **nosotros**, desde un **repositorio APT propio y firmado**:

- el **[núcleo](/es/docs/kernel)** optimizado (imagen y cabeceras);
- el **gobernador SMU** y las herramientas de overclock;
- las **aplicaciones propias** [Tuner y AI](/es/docs/app-native);
- la **estética steampunk** y la **identidad visual**;
- la configuración del sistema.

Publicar un componente desde nuestro propio repositorio significa que podemos **probarlo antes** en el hardware real y actualizarlo **solo cuando aporta algo**, no cada vez que cambia algo aguas arriba.

## 2. «Fijar» los paquetes frágiles

Para los paquetes que vienen de Debian pero son delicados en este hardware, SkillFishOS usa el **fijado de APT** (*pinning*): los mantiene en una versión **verificada** hasta que probamos una más nueva. Los principales candidatos a fijar son:

- **Mesa y los controladores Vulkan (RADV)** — una actualización puede empeorar `gfx1013`;
- **firmware de AMD / `linux-firmware`** — microcódigo de la GPU;
- **el núcleo estándar de Debian** — para bloquear las versiones problemáticas conocidas (ver [núcleo](/es/docs/kernel));
- **KDE Plasma** — para no toparse con una entrega inestable.

Así, las actualizaciones «normales» (la mayor parte del sistema) siguen llegando con regularidad, mientras el puñado de paquetes capaces de romperlo todo se queda en versiones que sabemos que funcionan.

## Cómo actualizar

Como en cualquier sistema Debian, desde la terminal:

```bash
sudo apt update && sudo apt full-upgrade
```

…o desde la aplicación gráfica **Discover**, o desde el **SkillFishOS Hub** — nuestro centro de software al estilo Discover que instala, quita y actualiza en un solo sitio a través de **APT, Flatpak y Snap**, con navegación por categorías, páginas de aplicación con carrusel de capturas y un «Actualizar todo» de un clic. Gracias a los enganches de [Snapper](/es/docs/storage-snapshot), se crea una instantánea Btrfs **antes y después** de cada actualización: si algo sale mal, la vuelta atrás desde el menú de GRUB restaura el estado anterior.

> En resumen: **nosotros** damos un núcleo, unas aplicaciones y una estética probados; **Debian** da el resto del software actualizado; el **fijado** evita sorpresas; **Btrfs** es la red de seguridad. Tres capas de protección, para que actualizar no dé miedo.

## El repositorio oficial

El repositorio APT de SkillFishOS está **en marcha**, firmado con GPG y alojado en **GitHub Pages** (suite `aetherium`):

```bash
# 1. importar la clave de firma
sudo curl -fsSL https://mtsistemi.github.io/SkillFishOS/skillfishos-archive-keyring.gpg \
  -o /usr/share/keyrings/skillfishos-archive-keyring.gpg
# 2. añadir el repositorio
echo "deb [signed-by=/usr/share/keyrings/skillfishos-archive-keyring.gpg] \
https://mtsistemi.github.io/SkillFishOS aetherium main" \
  | sudo tee /etc/apt/sources.list.d/skillfishos.list
# 3. instalar o actualizar el núcleo con apt
sudo apt update && sudo apt install skillfishos-kernel
```

Las compilaciones recientes de SkillFishOS lo traen **ya configurado**; si no, las órdenes de arriba lo dejan listo. El [núcleo](/es/docs/kernel) (imagen de 152 MB) se publica como *release asset* de GitHub: el diminuto paquete `skillfishos-kernel` lo descarga e instala solo, así que la actualización sigue pasando por `apt`. El repositorio se gestiona con **[reprepro](https://salsa.debian.org/debian/reprepro)** y el cliente comprueba la firma con el *keyring* dedicado.

## Fuentes

- [Debian unstable (sid)](https://wiki.debian.org/DebianUnstable)
- [Fijado de APT — manual de Debian](https://wiki.debian.org/AptConfiguration)
- [reprepro](https://salsa.debian.org/debian/reprepro) — gestión del repositorio APT
- [Snapper](http://snapper.io/) — instantáneas antes y después de APT

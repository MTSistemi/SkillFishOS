---
title: Escritorio, estética y acceso remoto
description: KDE Plasma 6, la estética steampunk, el HUD del sistema, el bloqueo de la suspensión y el acceso a distancia.
group: Sistema
order: 4
---

SkillFishOS usa **[KDE Plasma 6](https://kde.org/plasma-desktop/)** como entorno de escritorio, vestido con una estética steampunk coherente y un conjunto de ajustes propios de la BC-250.

## Sesiones

En la pantalla de acceso (de la que se encarga **SDDM**, con entrada automática) hay varias sesiones disponibles:

- **KDE Plasma X11** — *por defecto*. Elegir X11 hace que el acceso remoto sea trivial (ver más abajo);
- **KDE Plasma Wayland** — se puede elegir;
- **Gaming** — una sesión de [gamescope](https://github.com/ValveSoftware/gamescope) al estilo Big Picture (ver [Juegos](/es/docs/gaming)).

## **Atención:** bloqueo de la suspensión (crítico)

La BC-250 tiene la **suspensión ACPI rota**: si se duerme, **no despierta** y hace falta un reinicio físico (ver [hardware](/es/docs/hardware-bc250)). Por eso SkillFishOS **desactiva de forma permanente** todos los estados de reposo:

```bash
systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

A eso añade una regla de `logind` (`IdleAction=ignore`), el bloqueo automático de pantalla desactivado y una gestión de energía con inactividad «infinita». Es una medida **obligatoria**: una máquina suspendida además queda inalcanzable a distancia.

## Estética «SkillFish Steampunk»

El aspecto es una paleta coordinada de latón y cobre (acento **`#d8a849`**, superficies oscuras) y se mantiene **del arranque al escritorio**: tema de GRUB, pantalla de Plymouth, saludo de SDDM, fondo con el pez. El paquete de estética incluye:

- **iconos** (`SkillFishSteampunk`, con `breeze-dark` como respaldo) y **cursores** propios;
- un estilo **Kvantum** para las aplicaciones Qt y un **esquema de color** de KDE;
- un **tema de Plasma**, un tema de **Konsole**, botones de ventana y un **aspecto y comportamiento** global (`org.skillfish.steampunk`);
- avatares de usuario con la misma estética y una galería para elegir.

> Los temas **Breeze** de serie siguen instalados como respaldo estructural (en particular aportan el diálogo de cierre de sesión y apagado). No se deben quitar.

## HUD del sistema (Conky)

Arriba a la derecha hay un **HUD** de latón hecho con **[Conky](https://github.com/brndnmtthws/conky)** que muestra en tiempo real: barras de CPU por núcleo con MHz, °C y vatios, frecuencia, temperatura y VRAM de la GPU, memoria, disco, ventilador y los **dispositivos Bluetooth conectados** con su nivel de batería (mandos, auriculares…). Los valores vienen de ayudantes propios que leen los sensores del hardware directamente.

## Acceso a distancia (x11vnc)

Como la sesión por defecto es X11, el acceso remoto es sencillo: SkillFishOS arranca **[x11vnc](https://github.com/LibVNC/x11vnc)** en la pantalla activa y comparte la imagen real. En la red local puede conectarse cualquier cliente VNC. Así se puede dar soporte y configurar desde otro PC sin teclado ni ratón conectados a la placa.

## Red, audio y aplicaciones

- **Red**: de la conexión por cable se encarga **NetworkManager**, así que se ve y se configura desde las ventanas de Plasma.
- **Audio**: un conjunto completo de **[PipeWire](https://pipewire.org/)** (con soporte de Bluetooth). Ojo: los adaptadores DP→HDMI *activos* pueden romper el audio — ver [Solución de problemas](/es/docs/risoluzione-problemi).
- **Aplicaciones base**: gestor de archivos Dolphin, terminal Konsole, visor de PDF Okular, visor de imágenes Gwenview, archivador Ark, capturas Spectacle, tienda Discover (con flatpak), navegador **Google Chrome**, **OnlyOffice**.
- **Aplicaciones propias de SkillFishOS** (agrupadas en el menú **«SkillFishOS»**, cada una instalable y actualizable como `.deb` desde el repositorio firmado): **Tuner** (control de overclock, undervolt, ventilador y CU de la BC-250), **AI** (modelo de lenguaje local en la GPU integrada, bajo demanda), **Monitor** (gráficas en vivo de temperatura, frecuencia, voltaje y ventilador), **Kernel Manager** (elegir el núcleo de arranque y desinstalar los viejos), **ISO Mount**, **Hub** — el centro de software al estilo Discover (APT + Flatpak + Snap) con páginas de aplicación, carrusel de capturas y gestión de las fuentes — más **Base** (vigilante por hardware y detector de cuelgues con aviso en el escritorio) y **Console**, una sesión **«SkillFishOS Console (Big Picture)»** al estilo SteamOS que se elige en la pantalla de acceso.
- **Pantalla**: un servicio (`skillfish-dp-hotswap`) se ocupa de detectar el monitor, necesario porque el HPD del DisplayPort está averiado.

## Fuentes

- [KDE Plasma](https://kde.org/plasma-desktop/) · [Kvantum](https://github.com/tsujan/Kvantum)
- [Conky](https://github.com/brndnmtthws/conky) · [x11vnc](https://github.com/LibVNC/x11vnc)
- [PipeWire](https://pipewire.org/) · [SDDM](https://github.com/sddm/sddm)
- [Plymouth](https://www.freedesktop.org/wiki/Software/Plymouth/) · [NetworkManager](https://networkmanager.dev/)

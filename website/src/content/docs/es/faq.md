---
title: Preguntas frecuentes
description: Las dudas más habituales sobre SkillFishOS y la BC-250, con respuestas cortas.
group: Referencia
order: 2
---

Respuestas rápidas a las preguntas más habituales. Para profundizar, cada respuesta enlaza con la página adecuada.

## General

**¿Qué es SkillFishOS?**
Una distribución de Linux (Debian + KDE Plasma 6) diseñada y ajustada para la placa **AMD BC-250**: juegos, emulación, IA local y uso de escritorio, todo preconfigurado. Ver [Introducción](/es/docs/introduzione).

**¿En qué hardware funciona?**
La placa para la que está hecho es la **AMD BC-250** (APU Zen 2 + RDNA 2 «gfx1013», 16 GB GDDR6), y ahí hace todo lo que sabe hacer: 40 unidades de cómputo desbloqueadas, gobernador SMU, ocho núcleos. También hay una edición **Generic x86-64** que funciona en cualquier PC o máquina virtual — un núcleo normal, con las partes propias de la placa escondiéndose en vez de fallar. Ver [Hardware BC-250](/es/docs/hardware-bc250).

**¿Cuánto cuesta? ¿Es de código abierto?**
Es **gratuito**. Integra software libre de muchas comunidades; el código del proyecto está en [GitHub](https://github.com/MTSistemi/SkillFishOS). Ver [Fuentes](/es/docs/fonti).

**¿Incluye juegos, ROMs o BIOS?**
No. SkillFishOS pone las **herramientas** (Steam, EmuDeck, emuladores, interfaces); el contenido lo añades tú, legalmente. Ver [Juegos](/es/docs/gaming).

## Instalación

**¿Cómo se instala?**
Graba la ISO en una memoria USB y arranca el instalador gráfico **Calamares**. Todo con el ratón. Ver [Instalación](/es/docs/installazione).

**¿Puedo probarlo sin instalar?**
Sí: la ISO es **en vivo**, puedes recorrer el escritorio antes de instalar.

**¿Me borra el disco?**
La instalación automática («Borrar disco») sí. Para conservar datos existentes, usa el particionado manual. SkillFishOS usa **Btrfs** con subvolúmenes separados `@rootfs` y `@home`.

**¿Necesito conexión a internet?**
Para instalar no; luego hará falta para Steam, las actualizaciones y la IA.

## Rendimiento y overclock

**¿Por qué arranca «lento», en Stock?**
Por seguridad: cada BC-250 es distinta (*lotería del silicio*). Los perfiles se suben desde el **[Tuner](/es/docs/app-native)**, que lo valida todo en tu propia placa. Ver [GPU y overclock](/es/docs/gpu-overclock).

**¿Es peligroso el overclock?**
El Tuner aplica un perfil, lo **prueba** y **vuelve atrás** si la placa no aguanta; el tope de 85 °C y la protección térmica están siempre activos. Está pensado para ser seguro.

**¿Cuántos FPS en el juego X?**
Depende: algunos juegos dependen de la **CPU** (por ejemplo *Black Myth: Wukong*) y no mejoran con una GPU más rápida. Ver [Rendimiento y pruebas](/es/docs/prestazioni).

**¿Puedo usar FSR 4?**
No, necesita hardware RDNA 4. Usa gamescope (FSR1/NIS) u OptiScaler. Ver [Juegos](/es/docs/gaming).

## Uso diario

**¿Por qué a veces la pantalla se queda en negro?**
El **HPD del DisplayPort está averiado** en la BC-250: SkillFishOS lo sortea con un servicio propio. Usa un monitor DP o un adaptador **pasivo**. Ver [Solución de problemas](/es/docs/risoluzione-problemi).

**¿Por qué no hay audio por el televisor?**
Suele ser un adaptador DP→HDMI **activo**: usa uno pasivo, un monitor DP, una tarjeta de sonido USB o audio por Bluetooth.

**¿Puedo suspender el PC?**
No. **La suspensión está rota** a nivel de hardware y la placa no despierta: SkillFishOS la desactiva a propósito. **No la vuelvas a activar.** Ver [Escritorio](/es/docs/desktop).

**¿Puedo usarlo desde otro ordenador?**
Sí: la sesión por defecto es X11 y **x11vnc** está funcionando, así que puedes manejar el escritorio por VNC en la red local. Ver [Escritorio](/es/docs/desktop).

## IA local

**¿Qué modelo de IA puedo usar?**
El motor es **Unsloth Studio** sobre **Vulkan** (no ROCm, que no está soportado en gfx1013), y los modelos son archivos GGUF descargados de Hugging Face. Medido en la placa: **210,7 tok/s** generando frente a 41,5 en CPU. Ver [IA en el equipo](/es/docs/ai-locale).

**¿Puedo jugar con la IA encendida?**
No: la IA y los juegos pesados comparten GPU y memoria. Apaga la IA antes de jugar.

## Actualizaciones

**¿Cómo actualizo el sistema?**
`sudo apt update && sudo apt full-upgrade` o la aplicación **Discover**. Se toma una instantánea automáticamente antes y después de cada actualización. Ver [Actualizaciones](/es/docs/aggiornamenti).

**Una actualización ha roto algo, ¿y ahora?**
Reinicia y elige una instantánea en **GRUB → «SkillFishOS snapshots»**. Ver [Almacenamiento e instantáneas](/es/docs/storage-snapshot).

**¿Debian actualiza el núcleo?**
No: el núcleo de SkillFishOS está **retenido** (`apt-mark hold`) y solo se actualiza desde nuestro repositorio probado. Ver [Núcleo](/es/docs/kernel).

## Proyecto

**¿Puedo contribuir o informar de un fallo?**
Sí, con las **Issues** en [GitHub](https://github.com/MTSistemi/SkillFishOS/issues).

**¿Dónde descargo la ISO?**
En la página de [Descarga](/es/download) (alojada en SourceForge).

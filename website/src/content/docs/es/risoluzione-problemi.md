---
title: Solución de problemas
description: Los fallos más habituales de la BC-250 y cómo los sortea SkillFishOS.
group: Referencia
order: 1
---

Muchos de los «problemas» de la BC-250 son en realidad defectos conocidos del hardware que SkillFishOS sortea por su cuenta. Estos son los más habituales.

## La pantalla se queda en negro / no detecta el monitor

El **Hot-Plug Detect (HPD) del DisplayPort está averiado**: la placa no se entera de que has conectado un monitor. SkillFishOS lo resuelve con el servicio `skillfish-dp-hotswap` (que fuerza la detección al arrancar y al cambiar de monitor) y con el parámetro del núcleo `video=DP-1:e`.

Qué comprobar:

- usa un **monitor con DisplayPort** o un adaptador DP→HDMI **pasivo**;
- evita los adaptadores DP→HDMI **activos**: además de dar problemas de detección, **rompen el audio** (ver más abajo);
- si has cambiado de monitor, espera unos segundos: la detección es automática pero no instantánea.

## La placa no despierta de la suspensión

La suspensión está **rota a nivel de hardware**. Por eso mismo SkillFishOS la desactiva del todo (ver [Escritorio](/es/docs/desktop)). Si la placa parece «muerta» tras un rato inactiva y se había tocado la gestión de energía, la única salida es un **reinicio físico**. No vuelvas a activar los estados de reposo.

## No hay audio por el monitor o el televisor

El audio por DisplayPort funciona, pero:

- los adaptadores DP→HDMI **activos** rompen el audio: usa adaptadores pasivos, un monitor DP nativo, una **tarjeta de sonido USB** o audio por **Bluetooth**;
- del sonido se encarga **PipeWire**: la salida por defecto se elige en los ajustes de audio de KDE.

## Los mandos no funcionan

- Los mandos **DualShock 4** van por **Bluetooth** (con giroscopio). Para emparejarlos: mantén *Share + PS* hasta que parpadeen y empareja desde la ventana de Bluetooth.
- Un mando **por USB** hay que conectarlo con un cable **de datos** (no solo de carga): se reconoce como un Xbox 360.
- Los mandos clónicos a veces no conviven bien con los DS4 en el mismo adaptador Bluetooth: en ese caso úsalos **por USB**.

## La GPU parece lenta / las temperaturas son altas

- Comprueba en el [Tuner](/es/docs/app-native) que estén activas las **40 CU** y el gobernador SMU.
- Recuerda que la refrigeración va justa: tras una carga larga entra la **protección térmica** (85 °C). Para pruebas válidas, deja enfriar la placa entre pasadas (ver [GPU](/es/docs/gpu-overclock)).
- En juegos que dependen de la **CPU**, bajar la resolución no sube los FPS.

## La placa se ha colgado del todo

La BC-250 puede sufrir un **cuelgue total**, a menudo por un **undervolt demasiado agresivo**: la inestabilidad aparece sobre todo con **poca carga**, así que un cuelgue puede darse incluso en reposo. SkillFishOS lo ataca por dos lados:

- **Vigilante por hardware** — el temporizador **SP5100 TCO** del chipset está activo (`RuntimeWatchdogSec=2min`): si el sistema se bloquea por completo, la placa **se reinicia sola** en menos de dos minutos, sin quitar la corriente.
- **Detector de cuelgues** — al arrancar, un servicio nota si el apagado anterior fue anormal (falta la marca de apagado limpio) y lo **anota** en `/var/log/skillfish-freeze.log`, con un aviso en el escritorio. El contador aparece también en el panel **«Mi silicio»** del Tuner.

Si los cuelgues se repiten, **baja un perfil** (por ejemplo de Crazy o Turbo a Performance) en el Tuner: el valor menos agresivo casi siempre lo arregla. Todos los perfiles son **a prueba de cuelgue**: un bloqueo a mitad de una prueba nunca deja la placa con un perfil inestable al reiniciar. Si persisten incluso en Stock, sospecha de la **fuente de alimentación**.

## Una actualización ha roto algo

Reinicia y en el menú **GRUB → «SkillFishOS snapshots»** elige una instantánea anterior que funcionara. Ver [Almacenamiento e instantáneas](/es/docs/storage-snapshot). Las instantáneas antes y después de actualizar son automáticas.

## La IA no arranca o devuelve cosas raras

- La IA va sobre Vulkan (no ROCm) y **no debe usarse a la vez que los juegos** (comparten GPU y memoria).
- Si la salida sale corrupta, asegúrate de usar la caché KV en **f16** (`q4_0` corrompe la salida en RADV). Ver [IA en el equipo](/es/docs/ai-locale).

## Fuentes

- [bc250.info](https://bc250.info) · [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- [Arch Wiki — Gamepad](https://wiki.archlinux.org/title/Gamepad)
- [PipeWire — solución de problemas](https://docs.pipewire.org/)

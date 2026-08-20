---
title: Inicio rápido
description: Tus primeros 10 minutos con SkillFishOS — del primer arranque al primer juego.
group: Introducción
order: 3
---

Has instalado SkillFishOS (ver [Instalación](/es/docs/installazione)) y estás en el primer arranque. Esta página es una **lista rápida** para empezar enseguida: todo lo demás ya está configurado y funcionando.

## En una línea

> Enciendes → ya estás en el escritorio ajustado → conectas un mando → añades tus juegos → juegas. Sin terminal y sin configuración.

## 1. Primer arranque (está todo listo)

En el primer arranque encuentras un escritorio **KDE Plasma 6** con estética steampunk, un núcleo optimizado, el gobernador SMU, el perfil **Stock**, el conjunto para jugar y las instantáneas **ya activas**. Arriba a la derecha, el **HUD** muestra en tiempo real CPU, GPU, temperaturas, memoria, ventilador y dispositivos Bluetooth conectados.

No hace falta instalar controladores, fijar frecuencias ni activar nada: el sistema arranca «con la máxima compatibilidad».

## 2. Conéctate a la red

La red por cable la gestiona NetworkManager y está lista. Para Wi-Fi y Bluetooth usa el icono de red en el panel. Hace falta conexión para Steam, las actualizaciones y la IA local.

## 3. Conecta un mando

| Mando | Cómo |
|---|---|
| **DualShock 4** | Por Bluetooth: mantén **Share + PS** hasta que parpadee y empareja desde el icono de Bluetooth. Tiene **giroscopio**. |
| **Mando genérico** | Por **USB** con un cable **de datos** (no solo de carga): se ve como un mando de Xbox 360. |

Detalles y solución de problemas → [Juegos](/es/docs/gaming) y [Solución de problemas](/es/docs/risoluzione-problemi).

## 4. Añade tus juegos

- **Steam** ya está instalado e integrado con gamescope y MangoHud. Inicia sesión e instala tus juegos: los títulos de Windows funcionan con **Proton**.
- **Epic / GOG** → [Heroic](/es/docs/gaming).
- **Emulación** → abre **EmuDeck**, elige los emuladores y juega desde la interfaz **ES-DE**. Las ROMs, las BIOS y las claves las pones tú (ver la nota legal en [Juegos](/es/docs/gaming)).

## 5. (Opcional) Exprimir el hardware

SkillFishOS arranca con el perfil **Stock** para ir seguro en cualquier placa. Cuando quieras más rendimiento abre el **[Tuner](/es/docs/app-native)** y sube un perfil:

**Stock → Performance → Turbo → Crazy**

El Tuner **prueba cada perfil en tu propia BC-250** y **vuelve atrás solo** si la placa no aguanta. Es la forma segura de encontrar el límite de tu chip (ver [GPU y overclock](/es/docs/gpu-overclock)).

## 6. (Opcional) Encender la IA local

Cuando necesites un asistente que funcione sin internet, abre el **panel de IA** y arranca [Unsloth Studio](/es/docs/ai-locale). Recuerda: la IA y los juegos pesados **no** conviven (comparten GPU y memoria). Con el motor apagado, la GPU vuelve entera a los juegos.

## Cosas que conviene saber ya

- **No vuelvas a activar la suspensión**: en la BC-250 está rota y la placa no despierta (ver [Escritorio](/es/docs/desktop)).
- Usa un monitor con **DisplayPort** o un adaptador **pasivo**; los adaptadores DP→HDMI **activos** rompen el audio.
- Tienes una **red de seguridad**: se toma una instantánea Btrfs antes y después de cada actualización; si algo sale mal, vuelve atrás desde el menú de GRUB → *SkillFishOS snapshots* (ver [Almacenamiento e instantáneas](/es/docs/storage-snapshot)).

## ¿Y ahora qué?

- ¿Quieres entender **qué** estás usando? → [Hardware BC-250](/es/docs/hardware-bc250)
- ¿Quieres los **números** reales de rendimiento? → [Rendimiento y pruebas](/es/docs/prestazioni)
- ¿Tienes una **duda** rápida? → [Preguntas frecuentes](/es/docs/faq)
- ¿Un **término** que no conoces? → [Glosario](/es/docs/glossario)

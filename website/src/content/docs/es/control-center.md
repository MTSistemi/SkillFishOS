---
title: "Control Center"
description: "Todas las herramientas de SkillFishOS en una ventana: Tuner, Ventilador, Monitor, Juegos, Perfiles, Kernel, Instantáneas, IA, Emuladores, Consola, ISO."
group: Uso
order: 4
---

Todas las herramientas de SkillFishOS están en una ventana. Se abre desde el menú (SkillFishOS → Control Center) o con `skillfish-control-center`. También se maneja con el mando: cruceta o palanca para moverse, A confirma, B vuelve atrás, LB y RB cambian de sección.

## Las secciones

- **Estado**: un número por tarjeta: frecuencia y techo de la GPU, CPU, unidades de cálculo, ventilador, kernel, governor, driver Vulkan, si el último arranque siguió a un apagado limpio. Aquí no se ajusta nada.
- **Tuner**: la curva tensión/frecuencia del governor de la GPU, la CPU, los núcleos, las unidades de cálculo, la VRAM.
- **Ventilador**: la curva del ventilador con su adelanto, los sensores fuente, los límites de seguridad, la prueba PWM.
- **Monitor**: todas las lecturas, un gráfico por unidad, más las barras de frecuencia por hilo. REC graba, CSV exporta.
- **Juegos**: nuestra Mesa por lanzador o para todo el sistema, el planificador scx_bpfland, FSR 4, instalación y predeterminado de GE-Proton.
- **Perfiles**: techo, CPU, ventilador y planificador en un clic; guarda los tuyos.
- **Kernel**: los kernels instalados, el predeterminado, arrancar una vez, desinstalar.
- **Instantáneas**: las instantáneas del sistema y el mantenimiento btrfs programado.
- **IA**: Unsloth Studio sobre Vulkan: encendido/apagado, hardware, el límite GTT.
- **Emuladores**: EmuDeck, o los emuladores uno a uno desde Flathub.
- **Consola**: Steam Big Picture dentro de gamescope, ahora o desde la pantalla de inicio de sesión.
- **ISO**: imágenes de disco montadas a través de udisks.

## Tuner

La curva es el gráfico: MHz en horizontal, milivoltios en vertical. Arrastra un punto, doble clic para añadir uno, clic derecho para quitarlo, o escribe los números en la tabla junto al gráfico (+ y − añaden y quitan puntos). La línea vertical discontinua es el techo, el punto azul es la GPU ahora mismo. Tres presets: **Cautious 1850** (el punto dulce con el disipador de serie, casi los mismos fotogramas y diez grados menos), **Balanced 2000**, **Performance 2100** (la curva de quince puntos medida en la placa de desarrollo, la que enviamos).

**Aplicar es una prueba.** Una curva que pide muy poca tensión cuelga la placa, y en la BC-250 un cuelgue se arregla desenchufando. Por eso Aplicar arranca la candidata con la curva anterior todavía en disco y cuenta 25 segundos: pulsa Mantener y la candidata se escribe de verdad; no hagas nada, o la placa muere y vuelve, y arranca la curva anterior.

Los paneles se abren cuando hacen falta:

- **CPU**: frecuencia, escalón de undervolt (6,25 mV cada uno) y límite térmico, cada uno con un deslizador y una casilla numérica de paso 1. *Sugerir UV* baja el undervolt de dos en dos escalones con doce segundos de carga por escalón; *Buscar mi máximo* sube de 3600 a 4000 MHz; *Test 60 s* carga los valores actuales. Cada prueba muestra una cuenta atrás y un botón Stop; los valores en prueba nunca se escriben en disco, así que un cuelgue arranca con los anteriores. Por encima de 3500 MHz con ocho núcleos la ganancia es nula: manda el calor.
- **Núcleos**: qué núcleos están activos, SMT, el desbloqueo de los 8 núcleos (6c/12t pasa a 8c/16t, +20 % medido) y *Antes del arranque (EFI)*: el desbloqueo hecho antes de GRUB en un solo arranque, en vez del reinicio extra del servicio dentro del sistema.
- **CU**: las 40 unidades de cálculo como 20 celdas (pares): verde encendida, roja apagada, gris mantenida encendida por el driver. Escribe cuántas CU quieres (de 24 a 40, en pares) o pulsa las celdas; *Test CU* enciende los pares extra uno a uno bajo vkpeak e informa de errores, para la lotería del silicio.
- **VRAM**: el reparto UMA en la CMOS, aplicado en el próximo arranque. Con los 512 MB dinámicos algunos juegos eligen texturas bajas: si se ven borrosas, prueba 4 o 6 GB fijos.
- **Avanzado**: los mandos propios del governor: margen en subida, escalón, confirmaciones en bajada, umbrales térmicos y de potencia, droop.
- **Test**: vkpeak y el registro del asistente.

## Monitor

Un gráfico por magnitud, cada uno con su escala real: temperaturas (CPU, GPU, VRM, sistema, NVMe), frecuencias (CPU media, mínima, máxima, GPU y su techo), carga, potencia, tensiones, ventilador y memoria (RAM, VRAM, GTT), más una barra por hilo. Clic en una entrada de la leyenda para ocultar una línea; pasa el ratón para leer todos los gráficos en el mismo instante. REC escribe un archivo `.sfmon` (CSV) que Abrir recarga con un deslizador; CSV lo exporta para una hoja de cálculo.

## Juegos

- **Driver Vulkan**: nuestra Mesa abre las colas de cómputo que el driver de serie mantiene cerradas en esta GPU: +4 % en Cyberpunk 2077, +12 % con FSR 4. Por lanzador (Steam, Heroic) con un override flatpak, o para todo el sistema. Necesita el kernel de SkillFishOS: en otro kernel esas colas cuelgan la GPU, y el interruptor de sistema se niega a arrancar ahí. La tarjeta muestra el kernel en ejecución.
- **Planificador**: scx_bpfland, cargado solo mientras corre un juego (GameMode lo levanta y lo retira): +1,5-2 % en Cyberpunk y fotogramas más regulares. Si el kernel lo expulsa dos veces, el servicio se para hasta que pongas a cero el contador: es la fila «Expulsado por el kernel».
- **FSR 4**: a través de OptiScaler en la ruta DLSS del juego. GE-Proton 11 descarga OptiScaler solo cuando encuentra `PROTON_USE_OPTISCALER=1`, el juego debe ponerse en DLSS, y la biblioteca FSR 4 de AMD (`amdxcffx64.dll`, del driver Windows de AMD) va junto al juego. XeSS, donde un juego lo trae de serie, cuesta lo mismo que FSR 3 a 1080p.
- **Proton**: las versiones GE-Proton 11; Instalar descarga una (unos 500 MB) en las carpetas de Steam y Heroic, Predeterminada la elige. Steam debe estar cerrado para que se escriba su predeterminada.

## Ventilador, perfiles y el resto

La página **Ventilador** dibuja la curva dentro del gráfico de los sensores: a esta temperatura el ventilador gira así, con un adelanto para que la velocidad suba antes que la temperatura. Los **Perfiles** mueven el techo dentro de la curva que ya está y ajustan juntos CPU, preset del ventilador y planificador. Las **Instantáneas** son fotos del sistema, tus archivos no se tocan. **IA** retiene la memoria de la GPU mientras está encendida: apágala antes de jugar. **Consola** arranca Steam Big Picture dentro de gamescope sobre el escritorio, o como sesión desde la pantalla de inicio. El **Remote Manager** replica las páginas Tuner, Juegos y Perfiles en un navegador.

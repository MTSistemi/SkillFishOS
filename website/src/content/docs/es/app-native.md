---
title: Aplicaciones propias — Tuner y AI
description: Las herramientas gráficas de SkillFishOS para manejar el hardware y la IA sin terminal.
group: Uso
order: 3
---

SkillFishOS incluye dos aplicaciones propias (escritas en **PyQt6**, con la estética de Kvantum) que ponen el control del hardware y del conjunto de IA en manos del usuario **sin tocar la terminal**.

## SkillFishOS Tuner

El **Tuner** es el panel de control del hardware. Permite ajustar:

- **overclock y undervolt de la CPU**;
- los **puntos seguros de la GPU** (mediante el gobernador SMU, ver [GPU y overclock](/es/docs/gpu-overclock));
- el **ventilador** (control PWM);
- la **VRAM UMA** (requiere reiniciar);
- las **unidades de cómputo, en caliente** — ver más abajo.

### Unidades de cómputo en caliente (rejilla)

El Tuner muestra las CU de la GPU como una **rejilla de cuadros** (4 filas SE/SH × 5 WGP): **verde = activa, rojo = apagada**. Se cambian **en caliente, sin reiniciar**: haz clic en las parejas (1 WGP = 2 CU) o usa los **perfiles de 24 / 32 / 40 CU**, y luego *Aplicar*. Las primeras 24 CU son el mínimo del controlador y quedan siempre encendidas (ver [GPU y overclock](/es/docs/gpu-overclock)).

![SkillFishOS Tuner — la rejilla de unidades de cómputo en caliente, los perfiles y la prueba de CU](/img/tuner.jpg)

### Prueba de CU (lotería del silicio)

El botón **«Prueba de CU»** comprueba la salud de las CU adicionales: activa cada pareja por separado, la exige con **vkpeak** y vigila los **fallos y cuelgues de la GPU**, con una carga final sobre las 40. Está para detectar **CU defectuosas** en APU de descarte, para que sepas si tu chip aguanta las cuarenta.

![Resultado de la prueba de CU — todas las parejas correctas, 40 CU estables a 11380 GFLOPS, sin defectos](/img/cu-test.jpg)

### El flujo de «Prueba» y el monitor en vivo

El flujo del botón **«Prueba»** (CPU, GPU, CU, ventilador): aplicar un cambio → lanzar una medición → **comprobar** la estabilidad y, si algo falla, hacer un **retroceso** automático. En cuanto empieza una prueba se abre la ventana de **[SkillFishOS Telemetry](#skillfishos-telemetry)** con gráficas en vivo de **temperatura, frecuencia, voltaje y ventilador** (se puede cerrar).

![SkillFishOS Telemetry durante una prueba del Tuner — gráficas en vivo de temperatura, frecuencia, voltaje de la GPU y ventilador](/img/monitor.jpg)

Cómo está hecho: una ventana de usuario más un pequeño **servicio con permisos de root** que ejecuta las operaciones privilegiadas. En un PC personal está configurado para no pedir contraseña en cada operación. El HUD del escritorio también muestra las **CU activas** en vivo.

### Modos del gobernador: Balanced y Performance

La GPU de la BC-250 la maneja un **gobernador SMU** que sube y baja la frecuencia según la carga. El Tuner ofrece dos modos con un interruptor:

- **Balanced** *(por defecto)* — la frecuencia cae en reposo (hasta 350 MHz) y sube con la carga: menos consumo y menos temperatura en el uso diario.
- **Performance** — la GPU **se queda clavada en su frecuencia máxima** en cuanto hay carga, y desaparecen las microoscilaciones. En nuestra medición de *Black Myth: Wukong* eso vale **+11% de FPS** (de unos 100 a unos 111 de media) y un **1% low** más alto (92 → 102), con todo lo demás igual.

Los dos siguen bajo el **tope térmico de 85 °C**: el modo Performance aprieta más, no desactiva las protecciones.

### «Encuentra mi máximo» (asistentes de CPU y GPU)

Cada BC-250 es distinta ([lotería del silicio](/es/docs/gpu-overclock)). El Tuner trae dos asistentes **«Encuentra mi máximo»** que caracterizan **tu** placa:

- **GPU** — sube por escalones (2000 → 2200 MHz, de 50 en 50), aplicando y **probando** cada peldaño, y se detiene en el último estable.
- **CPU** — recorre los peldaños de frecuencia y undervolt (de 3600 MHz hasta 4000 MHz con escala −36) con el mismo esquema de **prueba y retroceso**: si un escalón no aguanta, vuelve al último valor bueno.

Todo es **a prueba de cuelgue**: el valor de trabajo en disco es siempre el último estable, así que un bloqueo a mitad de prueba nunca deja la placa con un perfil inestable en el siguiente arranque.

### Mi silicio

El panel **«Mi silicio»** resume el perfil de tu placa — el mejor valor de CPU y GPU encontrado, las CU sanas, el contador de cuelgues detectados — y permite **compartir el resultado de forma anónima** en la base de datos de la lotería del silicio (abre una issue de GitHub ya rellenada). Cuantos más datos reunamos, mejores serán los perfiles recomendados para todos.

## SkillFishOS Telemetry

**Telemetry** muestra en tiempo real la temperatura, la frecuencia, la carga de CPU y GPU, los voltajes, el consumo y el ventilador. Se abre sola durante las pruebas del Tuner, pero también es una aplicación por su cuenta. El botón **REC** graba una sesión de medición en un archivo **`.sfmon`** (en `~/SkillFishOS-benchmarks/`): al volver a abrirlo, Telemetry se convierte en un **analizador** con una barra de tiempo para repasar la pasada segundo a segundo.

![SkillFishOS Telemetry — gráficas con eje etiquetado y el panel de frecuencia por núcleo e hilo](/img/telemetry-percore.jpg)

### Frecuencia por núcleo e hilo

Con [ocho núcleos desbloqueados](/es/docs/hardware-bc250), un único número de «frecuencia de la CPU» dice bien poco: en reposo los dieciséis hilos pueden estar **a la vez** a 800, 1775 y 3990 MHz, así que el valor que lees depende solo de qué núcleo tocó mirar.

El panel de abajo dibuja **una barra por hilo**, emparejadas por núcleo físico y etiquetadas `núcleo·hilo`. El color va del latón a la brasa según sube el hilo, los MHz están impresos en cada barra y la cabecera resume **mínimo, media, máximo y cuántos hilos están en marcha**. Los hilos que apagaste desde el Tuner no desaparecen: se quedan como un hueco discontinuo marcado **«off»**, así se ve de un vistazo la configuración real.

### Ejes legibles

Cada gráfica tiene ahora una **escala con líneas y valores en el eje vertical**, ajustada a números humanos (`0 / 1000 / 2000 / 3000`, no `-160 / 1394 / 2948`). El cero pasa a ser el suelo cuando los datos están cerca de él, así que una gráfica de MHz o de revoluciones del ventilador nunca muestra una base negativa; y una línea plana ya no se amplía hasta que el ruido parece una montaña.

## SkillFishOS AI

El **panel de IA** enciende y apaga la IA local con un clic, liberando GPU y memoria para los juegos cuando no hace falta. Es la cara «fácil» de lo que se describe en [IA en el equipo](/es/docs/ai-locale).

![Panel SkillFishOS AI — motor local (Qwen3 14B) en la GPU con Vulkan, encendido y apagado con un clic](/img/ai-panel.jpg)

## Por qué existen

El objetivo de SkillFishOS es que **cualquiera** — incluidos los más pequeños — pueda usar y ajustar el sistema sin aprender órdenes de terminal. Estas aplicaciones traducen operaciones complicadas (gobernador SMU, parámetros del núcleo, instantáneas y vuelta atrás) en unos pocos clics, manteniendo siempre activas las **protecciones** (tope térmico, prueba con retroceso).

## Fuentes

- [PyQt6 / Qt for Python](https://doc.qt.io/qtforpython/) · [Kvantum](https://github.com/tsujan/Kvantum)
- [sysbench](https://github.com/akopytov/sysbench) · [vkpeak](https://github.com/nihui/vkpeak)
- Repositorio del proyecto — [github.com/MTSistemi/SkillFishOS](https://github.com/MTSistemi/SkillFishOS) (`apps/tuner`, `apps/ai-panel`)

---
title: Rendimiento y pruebas
description: Todas las pruebas reales de la BC-250 con SkillFishOS — capturas, ajustes completos, frecuencias, voltajes, temperaturas y consumo.
group: Referencia
order: 3
---

Esta es la **sección completa de pruebas**: cada pasada se hizo en **nuestra propia BC-250** con SkillFishOS, con capturas reales, **todos los ajustes usados** y el registro de **frecuencias, voltajes, temperaturas, consumo y ventilador** durante la pasada.

> **Aviso:** **lotería del silicio más refrigeración.** Las cifras valen para *este* chip con refrigeración suficiente. El disipador de serie va justo: comparar pruebas «seguidas» sin pausas falsea los resultados por el *calor acumulado*; deja enfriar la placa unos minutos entre pasadas.

## Condiciones de la prueba (banco)

Valen para **todas** las pruebas de abajo salvo que se diga otra cosa.

| Elemento | Valor |
|---|---|
| Placa | **AMD BC-250** — APU Zen 2 «Oberon» + RDNA 2 «Cyan Skillfish» (`gfx1013`) |
| Memoria | **16 GB GDDR6** unificada (UMA) |
| Unidades de cómputo | **40 / 40 activas** (conmutadas en caliente, ver [GPU](/es/docs/gpu-overclock)) |
| Núcleo | **7.0.10-skillfishos** (linux-tkg) — la versión con la que se tomaron estas cifras; hoy entregamos el **7.1.7**, vuelto a medir con menos de un 2 % de diferencia |
| Controlador | **Mesa 26.0.8** — RADV (Vulkan) / radeonsi (OpenGL), ACO |
| Gobernador de GPU | cyan-skillfish — reposo **350 MHz / 700 mV**, carga **2230 MHz / ~1000 mV** |
| Perfil de OC | **Turbo/Crazy** (tope de GPU 2230 MHz, CPU 3,9–4,0 GHz) |
| Tope térmico | **85 °C** (SMU y thermal-guard), ventilador en **automático** |
| Resolución | **1920×1080** |

> Recordatorio de arquitectura: CPU y GPU comparten **el mismo chip** y **el mismo presupuesto de potencia**. Con carga mixta la CPU cede frecuencia por sí sola (≈3,4–3,5 GHz) para quedarse dentro del presupuesto y por debajo de 85 °C: no es un defecto, es el chip protegiéndose.

---

## Black Myth: Wukong — 112 FPS (1080p)

![Black Myth: Wukong — 112 FPS de media a 1080p en la AMD BC-250](/img/benchmarks/wukong-112fps.jpg)

| Ajuste | Valor |
|---|---|
| Resolución | 1920×1080 |
| Límite de FPS | ninguno |
| Tipo de carga | **limitada por CPU y llamadas de dibujo** |
| Reescalado | FSR 4 no disponible (RDNA 4) → gamescope FSR1/NIS u OptiScaler |

**Resultado:** media de **112 FPS** · máximo **128** · mínimo **92** · 1 % peores **101**.

**Telemetría durante la pasada** (~4 min):

| Medida | Valor medido |
|---|---|
| Frecuencia de GPU | ~1,4–1,6 GHz (*sin saturar*: el juego está limitado por la CPU) |
| Borde de la GPU | 83–86 °C |
| Consumo de la GPU | ~90–140 W |
| Voltaje de la GPU | ~970–987 mV |
| Frecuencia de CPU | ~3,5 GHz (bajada desde 3,9 por el presupuesto compartido) |
| Temperatura de CPU | 85 °C (en el tope) |
| VRAM | ~1,9 GB (menú) → ~4,4 GB (en partida) |
| Ventilador | ~2950–3140 RPM |

> Lección: en *partida*, con un título limitado por llamadas de dibujo como Wukong, lo que más cuenta es la **estabilidad de la CPU** bajo carga y una buena refrigeración.

### Gobernador Balanced frente a Performance (herramienta de prueba)

El *vuelo de cámara* de la herramienta de prueba sí está **limitado por la GPU**, así que ahí la frecuencia cuenta. Al poner el gobernador en **Performance** desde el Tuner (mantiene la GPU en su punto seguro más alto bajo carga y baja a 350 MHz en reposo):

| Modo del gobernador | Media | 5 % peores |
|---|---|---|
| **Balanced** (por defecto) | 100 FPS | 92 FPS |
| **Performance** | **111 FPS** | **102 FPS** |

**+11 %** en la media y en los fotogramas más lentos, solo por sostener la frecuencia. Por seguridad el Tuner limita la GPU a **2200 MHz a 1000 mV** con una curva de voltaje de varios puntos: 2230 MHz a 1000 mV queda por debajo del voltaje necesario y puede colgar la máquina en seco.

---

## Unigine Superposition — 1080p HIGH: 12938

![Unigine Superposition 1080p High — 12938 puntos en la BC-250](/img/benchmarks/superposition-high.jpg)

| Ajuste | Valor |
|---|---|
| Versión | 1.1 |
| Interfaz gráfica | **OpenGL** |
| Resolución | 1920×1080, pantalla completa |
| Sombreadores | **High** |
| Texturas | High |
| Profundidad de campo | activada |
| Desenfoque de movimiento | activado |

**Resultado:** **12 938** puntos · FPS mínimo **75,59** · media **96,77** · máximo **127,16**.
**Configuración leída por la herramienta:** CPU AMD BC-250 **a 3894 MHz**, RAM 7 GB, GPU AMD BC-250 8 GB (Cyan Skillfish), núcleo 7.0.10-skillfishos.

---

## Unigine Superposition — 1080p EXTREME: 5513

![Unigine Superposition 1080p Extreme — 5513 puntos en la BC-250](/img/benchmarks/superposition-extreme.jpg)

| Ajuste | Valor |
|---|---|
| Versión | 1.1 |
| Interfaz gráfica | **OpenGL** |
| Resolución | 1920×1080, pantalla completa |
| Sombreadores | **Extreme** |
| Texturas | High |
| Profundidad de campo | activada |
| Desenfoque de movimiento | activado |

**Resultado:** **5513** puntos · media de **41,25** FPS (mínimo ~32,8 · máximo ~49).

![Unigine Superposition — escena dibujada en tiempo real](/img/benchmarks/superposition-scene.jpg)
*Una escena de Superposition dibujada en tiempo real en la BC-250.*

---

## Unigine Heaven 4.0 — 113,7 FPS · 2865 puntos

![Unigine Heaven 4.0 — 113,7 FPS, 2865 puntos en la BC-250](/img/benchmarks/heaven-113fps.jpg)

| Ajuste | Valor |
|---|---|
| Interfaz gráfica | **OpenGL** |
| Resolución | 1920×1080, en ventana |
| Suavizado de bordes | **8×** |
| Calidad | **Ultra** |
| Teselado | **Extreme** |

**Resultado:** **113,7 FPS** · **2865** puntos · mínimo **54,8** · máximo **219,5**.
**Plataforma leída por la herramienta:** Linux 7.0.10-skillfishos x86_64 · CPU AMD BC-250 ×12 · GPU gfx1013.

![Unigine Heaven — escena dibujada en tiempo real](/img/benchmarks/heaven-scene.jpg)
*La escena de Heaven dibujada en tiempo real en la BC-250 durante la pasada.*

---

## Cómputo en la GPU — vkpeak (sintético)

Rendimiento de cómputo Vulkan en la **misma** placa, antes y después de desbloquear las 40 CU.

| Medida | Base 24 CU | SkillFishOS 40 CU |
|---|---|---|
| **FP32** escalar | 6141 GFLOPS | **11 329** GFLOPS *(11 385 en frío)* |
| FP16 vec4 | 12 260 | **22 685** |
| producto escalar int8 | 24 550 GIOPS | **45 495** GIOPS |
| FP64 escalar | 385 | ~640 |
| copy d2d (ancho de banda interno) | — | 191 GBPS |

Con las 40 CU activas: **+85 %** en FP32 sobre la base (≈**11,3 TFLOPS**). En caliente, bajo esfuerzo sostenido, se asienta en torno a **10 214 GFLOPS**. En reposo el gobernador baja a 350 MHz, con el borde a unos 54 °C tras la carga.

## Ancho de banda de memoria — clpeak

| Medida | Valor |
|---|---|
| Ancho de banda GDDR6 medido | **~350–367 GB/s** |
| `mclk` ajustable | **No** (frecuencia de memoria fija) |
| Memoria vista por Vulkan | ~13 GiB (con el GTT ampliado) |

---

## Perfiles del Tuner — frecuencias, voltajes, temperaturas

| Perfil | CPU | Voltaje de CPU | GPU | Temperatura pico |
|---|---|---|---|---|
| **Stock** *(por defecto en la ISO)* | 3500 MHz | — | 1500 MHz | la más baja |
| **Performance** | 3700 MHz | ~1106 mV (`scale −16`) | 2000 MHz | equilibrada |
| **Turbo** | 3900 MHz | ~1199 mV (`scale −24`) | 2230 MHz | < 85 °C (tope) |
| **Crazy** | 4,0 GHz | ~1224 mV (`scale −36`) | 2230 MHz | ~83 °C en 120 s de esfuerzo |

- **Máximo duro de Vid: 1,325 V** (nunca superado).
- Tope térmico de 85 °C en todos los perfiles; ventilador en automático; en reposo la GPU se queda en **350 MHz / 700 mV**.

## El desbloqueo de los 8 núcleos: un +20 % real

La BC-250 viene con **dos núcleos apagados por software**: la máscara de núcleos habilitados de la SMU muestra 3 de 4 por CCX. SkillFishOS la reescribe y lleva la CPU a **8 núcleos / 16 hilos**, sin BIOS parcheada.

Medido en el mismo arranque, apagando y encendiendo los dos núcleos extra en caliente:

| Carga | 6n/12h | 8n/16h | |
|---|---|---|---|
| Compresión `xz -T` | 6,41 s | **5,11 s** | **+20 %** |
| Inferencia de LLM en CPU | 34,0 tok/s | **40,8 tok/s** | **+20 %** |
| Temperatura | 66 °C | 68 °C | +2 °C |

Es un +20 % y no el +33 % teórico: el ancho de banda de memoria y el coste de los hilos se comen la diferencia. Aun así, **una quinta parte más de rendimiento gratis**.

### Overclock con los 8 núcleos

Vuelto a medir escalón a escalón, cada peldaño **estable y con 0 MCE**:

| Objetivo | Alcanzado bajo carga | Puntuación | Temperatura | Ventilador |
|---|---|---|---|---|
| 3500 (referencia) | 3475 | 5118 ev/s | 57 °C | — |
| 3700 | 3673 | 5410 | 62 °C | 50 % |
| 3900 | 3872 | 5704 | 71 °C | 68 % |
| **4000** | **3971** | **5849** | **81 °C** | **93 %** |

**Máximo estable: 4000 MHz**, un +14 % en la puntuación frente a 3500, y solo alcanzable una vez arreglado el control del ventilador. **Aviso:** con carga **combinada de CPU y GPU** la frecuencia se asienta en 3375–3492 MHz a 86 °C: pasados los ~3900 el límite es el disipador, no el silicio.

---

## Validación térmica (prueba de esfuerzo)

Datos registrados durante la validación automática del Tuner (prueba con vuelta atrás).

| Fase | Frecuencia | Temperatura | Notas |
|---|---|---|---|
| Reposo | CPU ~2,5 GHz · GPU 350 MHz | k10 46 °C · GPU 45 °C | sin carga |
| **Esfuerzo de CPU** (12 hilos, 120 s) | CPU **3,68–3,69 GHz** | k10 **85 °C** (en el tope) | cifra histórica, tomada **antes** del desbloqueo de los 8 núcleos |
| **Esfuerzo de GPU** (bucle de vkpeak, 120 s) | GPU **2000 MHz** | borde hasta **86 °C** | a 86 °C el gobernador baja a 1819–1900 MHz (thermal-guard); la CPU cae a ~2,2–2,4 GHz por el presupuesto compartido |

---

## Comparaciones

**El mismo hardware, cambiando solo el sistema** — Superposition 1080p Extreme en la **misma** BC-250:

| Sistema | Puntuación |
|---|---|
| **SkillFishOS** (GPU 2230 · CPU 3900, 40 CU) | **5513** |
| Otra distribución (Bazzite, frecuencias de serie) | 4102 |

→ **+34 % de rendimiento real** del mismísimo chip, gracias a las 40 CU desbloqueadas, un gobernador que empuja a 2230 MHz y el overclock con undervolt de la CPU.

**Frente a las Radeon de sobremesa** (Superposition 1080p High): la BC-250 con SkillFishOS (**12 938**) se pone a la altura de una **RX 6600 / 6600 XT** de más de 200 €, con el cómputo bruto de una **RX 6700** (~11,3 TFLOPS), en una placa de unos 50 €.

---

## Herramientas y método

| Herramienta | Qué mide |
|---|---|
| [vkpeak](https://github.com/nihui/vkpeak) | rendimiento FP32/FP16/int8 por Vulkan |
| [clpeak](https://github.com/krrishnarraj/clpeak) | ancho de banda de memoria y rendimiento OpenCL |
| [sysbench](https://github.com/akopytov/sysbench) | esfuerzo y medición de la CPU (también lo usa el Tuner) |
| [Unigine Superposition / Heaven](https://benchmark.unigine.com/) | pruebas gráficas OpenGL |
| MangoHud en juego | FPS y tiempo de fotograma en juegos reales |
| telemetría propia | frecuencia, temperatura, consumo y ventilador por el sysfs de `amdgpu`, `k10temp`, `nct6686` |

## Fuentes

- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) · [sysbench](https://github.com/akopytov/sysbench) · [Unigine](https://benchmark.unigine.com/)
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock) — desbloqueo de las CU
- [bc250.info](https://bc250.info) — puntos seguros y notas térmicas de la comunidad
- [OptiScaler](https://github.com/optiscaler/OptiScaler) — reescalado por juego

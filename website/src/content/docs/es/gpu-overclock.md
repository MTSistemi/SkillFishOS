---
title: GPU, CPU, overclock y undervolt
description: Cómo SkillFishOS controla las frecuencias, los voltajes y las temperaturas de la BC-250, con las cifras reales medidas en el hardware.
group: Sistema
order: 2
---

En una APU normal las frecuencias se ajustan por el sysfs de `amdgpu`. En la BC-250 **eso no funciona**: el control pasa por la **SMU** (System Management Unit) y necesita herramientas propias. SkillFishOS las trae todas, preconfiguradas con perfiles seguros y un sistema de protección térmica.

> **Aviso:** **lotería del silicio.** Cada cifra de esta página está **medida en nuestra BC-250**. Cada placa es distinta: una aguanta un undervolt más profundo, otra menos. Por eso SkillFishOS **arranca siempre en el perfil Stock** y te deja subir desde el [Tuner](/es/docs/app-native), que valida cada perfil **en tu placa** con una prueba automática y vuelta atrás.

## Los cuatro perfiles

El [Tuner](/es/docs/app-native) ofrece **cuatro perfiles**. La ISO arranca en **Stock**; los demás están a un clic tras la prueba.

| Perfil | CPU | GPU | Notas |
|---|---|---|---|
| **Stock** *(por defecto en la ISO)* | 3500 MHz | 1500 MHz | Compatibilidad máxima con cualquier BC-250 |
| **Performance** | 3700 MHz · ~1106 mV | 2000 MHz | Equilibrado y con undervolt |
| **Turbo** | 3900 MHz · ~1199 mV | 2230 MHz | Subida fuerte, validada bajo el tope de 85 °C |
| **Crazy** | 4,0 GHz · ~1224 mV | 2230 MHz | Máximo validado (~83 °C bajo esfuerzo) |

Todos los perfiles respetan el mismo **tope térmico de 85 °C** y dejan el **ventilador en automático**.

## El gobernador SMU de la GPU

Las frecuencias de la GPU las lleva el **[cyan-skillfish-governor](https://github.com/Magnap/cyan-skillfish-governor)** (escrito en Rust), un servicio del sistema que se configura en `/etc/cyan-skillfish-governor/config.toml`. Define *puntos seguros* de frecuencia y voltaje: **350 MHz / 700 mV** en reposo y el valor del perfil bajo carga (por ejemplo 1500/900 en Stock, 2230/1000 en Turbo).

> El sysfs estándar de amdgpu (`power_dpm_force_performance_level`, `pp_dpm_sclk`) **no** controla la BC-250: solo lo hace el gobernador SMU. La GPU únicamente sube a su frecuencia máxima con **saturación gráfica** real.

## Overclock y undervolt de la CPU

La CPU (**8 núcleos / 16 hilos** Zen 2 «Oberon», dos de ellos desbloqueados por SkillFishOS desde la SMU) la gestiona un servicio de una sola pasada, **`bc250-smu-oc.service`**, que aplica los valores de `/etc/bc250-smu-oc.conf` mediante el proyecto [bc250_smu_oc](https://github.com/bc250-collective/bc250_smu_oc). Después de aplicarlos aparece como *inactive*: es normal (es de una sola pasada).

Lo que hemos medido apretando **nuestra** placa:

- **3700 MHz** (perfil *Performance*) con undervolt a unos **1106 mV** (`scale −16`);
- **3900 MHz** (perfil *Turbo*) a unos **1199 mV** (`scale −24`);
- **4,0 GHz** (perfil *Crazy*) validados a unos **1224 mV** (`scale −36`) durante 120 s de esfuerzo sostenido, con pico de **83 °C**: el máximo utilizable en este ejemplar;
- **techo duro de Vid: 1,325 V** (nunca superado).

El **undervolt** no va de «apretar», sino de hacer el mismo trabajo con **menos calor y menos consumo**: a una frecuencia dada, bajar el voltaje hasta el límite de estabilidad reduce la temperatura y deja margen térmico para el resto de la APU.

### Acoplamiento térmico CPU↔GPU

CPU y GPU comparten el **mismo chip** y el **mismo presupuesto de potencia**. Con carga **mixta** (un juego exigente: CPU y GPU a la vez) la APU se protege y la CPU baja sola a unos **3450 MHz** para quedarse dentro del presupuesto y por debajo de 85 °C. **No es un defecto**: el chip se protege soltando los megahercios menos útiles. Por lo mismo, un undervolt en la CPU deja más «sitio» térmico a la GPU, y al revés.

## Las 40 unidades de cómputo, en caliente

La BC-250 tiene **40 CU** (20 WGP, 1 WGP = 2 CU), pero el controlador habilita **24** por defecto. SkillFishOS las lleva a 40 **en caliente, sin reiniciar**: el sistema arranca en el mínimo del controlador (24 CU) y un servicio las sube a 40 al inicio; desde el [Tuner](/es/docs/app-native) ajustas el número **en vivo** con una rejilla de casillas y perfiles de 24/32/40. Las primeras 24 están fijadas por el controlador y siempre encendidas.

Con las 40 CU la GPU mide **11385 GFLOPS** FP32 (vkpeak) en frío, frente a unos **6141** con las 24 de partida: **+85 %**. Bajo esfuerzo sostenido (en caliente) se asienta en torno a **10214 GFLOPS**. El ancho de banda de memoria medido (clpeak) es de **~350–367 GB/s**.

> **Lotería del silicio.** En chips recuperados o de «descarte» algunas CU pueden ser flojas. El [Tuner](/es/docs/app-native) trae una **«Prueba de CU»** que esfuerza cada pareja y señala fallos o cuelgues de la GPU, para confirmar que tu chip aguanta las 40. (Mecanismo con `umr`, escribiendo las máscaras WGP; crédito a [bc250-cu-live-manager](https://github.com/WinnieLV/bc250-cu-live-manager), reimplementación propia.)

## Protección térmica: el tope de 85 °C

El techo térmico es de **85 °C** y se respeta en dos niveles:

1. **por la SMU**: el valor `max_temperature` de la configuración hace que el chip baje frecuencias *antes* de cruzar los 85 °C (evitando el estrangulamiento brusco);
2. **por el sistema**: un vigilante **thermal-guard** que, si se supera el tope, baja las frecuencias de 100 en 100 MHz hasta volver al rango.

Cosas que conviene saber sobre la refrigeración de serie (ver también [Hardware BC-250](/es/docs/hardware-bc250) para **cajas imprimibles en 3D y ventiladores recomendados**):

- el disipador de serie va **justo**: comparar pruebas «seguidas» falsea los resultados por el *calor acumulado*; deja enfriar la placa unos minutos entre pasadas;
- solo existe el sensor de *borde* de la GPU; **no hay sensor de temperatura de la VRAM**;
- el ancho de banda de memoria es bueno, pero `mclk` **no** se puede tocar.

## Un caso real: juegos limitados por CPU

Algunos títulos —como *Black Myth: Wukong* en **partida**— están limitados por la **CPU y las llamadas de dibujo**: los FPS apenas dependen de la resolución ni de la frecuencia de la GPU. Ahí ayudan el overclock de **CPU** y una buena refrigeración. Para el reescalado, FSR 4 **no está disponible** (exige hardware RDNA 4); usa gamescope (FSR1/NIS) o [OptiScaler](https://github.com/optiscaler/OptiScaler) por juego.

Cuando la carga **sí** está limitada por la GPU (por ejemplo el *vuelo de cámara* del benchmark de Wukong), la frecuencia cuenta: en el **Tuner** puedes poner el **gobernador en «Performance»**, que mantiene la GPU en su punto seguro más alto bajo carga (en reposo sigue bajando a 350 MHz). Medido en el benchmark de Wukong: **100 → 111 FPS de media (+11 %)**, 92 → 102 en los fotogramas más lentos. Por seguridad el Tuner limita la GPU a **2200 MHz a 1000 mV** (el máximo estable con la refrigeración de serie) con una curva de voltaje de varios puntos: forzar 2230 MHz a 1000 mV queda por debajo del voltaje necesario y puede colgar la máquina en seco.

## Todo esto, sin terminal

Frecuencias, undervolt, ventilador y unidades de cómputo se ajustan desde la interfaz del **Tuner**, con los cuatro perfiles listos y **prueba automática con vuelta atrás** si tu placa no aguanta un valor; ver [Aplicaciones propias](/es/docs/app-native). Es la vía recomendada: empieza en Stock, pasa a Performance, prueba Turbo o Crazy, y el Tuner lo valida todo en **tu** BC-250.

## Fuentes

- [cyan-skillfish-governor (Magnap)](https://github.com/Magnap/cyan-skillfish-governor) — gobernador SMU de la GPU
- [bc250_smu_oc (bc250-collective)](https://github.com/bc250-collective/bc250_smu_oc) — overclock y undervolt de la CPU por la SMU
- [bc250.info](https://bc250.info) — puntos seguros y notas térmicas de la comunidad
- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) — pruebas de FP32 y de ancho de banda de memoria

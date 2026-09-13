---
title: GPU, CPU, overclock y undervolt
description: Cómo SkillFishOS controla las frecuencias, los voltajes y las temperaturas de la BC-250, con las cifras reales medidas en el hardware.
group: Sistema
order: 2
---

En una APU normal las frecuencias se ajustan por el sysfs de `amdgpu`. En la BC-250 **eso no funciona**: el control pasa por la **SMU** (System Management Unit) y necesita herramientas propias. SkillFishOS las trae todas, con una curva segura de fábrica y un sistema de protección térmica.

> **Aviso:** **lotería del silicio.** Cada cifra de esta página está **medida en nuestra BC-250**. Cada placa es distinta: una aguanta una curva más agresiva, otra menos. Por eso SkillFishOS **arranca con la curva de fábrica** (perfil **Performance**, tope de 2100 MHz) y te deja cambiarla desde el [Tuner](/es/docs/control-center), que prueba cada curva **en tu placa** con un test automático de 25 segundos y vuelve atrás sola si no aguanta.

## La curva voltaje/frecuencia y los tres perfiles

![la curva de tensión y frecuencia en el Tuner, con la tabla de puntos y los tres perfiles](/img/control-center-tuner.png)

El [Tuner](/es/docs/control-center) gobierna la GPU con una **curva voltaje/frecuencia**: MHz en horizontal, milivoltios en vertical, puntos que arrastras en la gráfica o escribes en la tabla de al lado. Tres perfiles mueven el **tope** de la curva:

| Perfil | Tope de GPU | Notas |
|---|---|---|
| **Cautious** | 1850 MHz | El punto dulce con la refrigeración de serie: casi los mismos fotogramas, diez grados menos |
| **Balanced** | 2000 MHz | Equilibrio entre frecuencia y calor |
| **Performance** | 2100 MHz | La curva de quince puntos medida en la placa de desarrollo: la que enviamos por defecto |

**Aplicar es una prueba, no una escritura inmediata.** Una curva que pide muy poco voltaje cuelga la placa, y en la BC-250 un cuelgue solo se resuelve cortando la corriente. Por eso Aplicar deja la curva anterior en el disco, prueba la candidata durante **25 segundos** y espera confirmación: pulsa Mantener y se escribe de verdad; si no —o si la placa se cuelga y arranca sola de nuevo— al iniciar vuelve la curva anterior.

## El gobernador V/F de la GPU

Las frecuencias de la GPU las lleva **skillfish-vf-governor**, nuestro servicio que le quita el reloj y el voltaje al gobernador de fábrica y los maneja directamente por la SMU, manteniendo un **tope de frecuencia** que el calor y el consumo pueden bajar y, cuando la placa se calma, devolver. Un proceso aparte, **skillfish-vf-watchdog**, toma el control si el gobernador se cae con el reloj forzado.

Medido en *Black Myth: Wukong*, misma sesión, mismos 84 °C en ambas pasadas: **+4,5 %** con la placa fría, **+11 %** con la placa caliente, frente al gobernador de fábrica. La ventaja crece con la temperatura porque el gobernador de fábrica pierde reloj al calentarse la placa, y el nuestro no.

> El sysfs estándar de amdgpu (`power_dpm_force_performance_level`, `pp_dpm_sclk`) **no** controla la BC-250: solo lo hace skillfish-vf-governor. La GPU solo sube al tope con **saturación gráfica** real.

## Overclock y undervolt de la CPU

La CPU (**8 núcleos / 16 hilos** Zen 2 «Oberon», dos de ellos desbloqueados por SkillFishOS desde la SMU —también antes de arrancar, con un programa EFI, en un solo reinicio—) la gestiona para el overclock un servicio de una sola pasada, **`bc250-smu-oc.service`**, que aplica los valores de `/etc/bc250-smu-oc.conf` mediante el proyecto [bc250_smu_oc](https://github.com/bc250-collective/bc250_smu_oc). Después de aplicarlos aparece como *inactive*: es normal (es de una sola pasada).

Lo que hemos medido apretando **nuestra** placa:

- **3700 MHz** con undervolt a unos **1106 mV** (`scale −16`);
- **3900 MHz** a unos **1199 mV** (`scale −24`);
- **4,0 GHz** validados a unos **1224 mV** (`scale −36`) durante 120 s de esfuerzo sostenido, con pico de **83 °C**: el máximo utilizable en este ejemplar;
- **techo duro de Vid: 1,325 V** (nunca superado).

El **undervolt** no va de «apretar», sino de hacer el mismo trabajo con **menos calor y menos consumo**: a una frecuencia dada, bajar el voltaje hasta el límite de estabilidad reduce la temperatura y deja margen térmico para el resto de la APU.

### Acoplamiento térmico CPU↔GPU

CPU y GPU comparten el **mismo chip** y el **mismo presupuesto de potencia**. Con carga **mixta** (un juego exigente: CPU y GPU a la vez) la APU se protege y la CPU baja sola a unos **3450 MHz** para quedarse dentro del presupuesto y por debajo de 85 °C. **No es un defecto**: el chip se protege soltando los megahercios menos útiles. Por lo mismo, un undervolt en la CPU deja más «sitio» térmico a la GPU, y al revés.

## Las 40 unidades de cómputo, en caliente

La BC-250 tiene **40 CU** (20 parejas), pero el controlador habilita **24** por defecto. SkillFishOS las lleva a 40 **al arrancar, sin pasos extra**; desde el [Tuner](/es/docs/control-center) ajustas el número **en vivo** escribiendo la cifra que quieras o pulsando las 20 casillas emparejadas. Las primeras 24 están fijadas por el controlador y siempre encendidas.

Con las 40 CU la GPU mide **11385 GFLOPS** FP32 (vkpeak) en frío, frente a unos **6141** con las 24 de partida: **+85 %**. Bajo esfuerzo sostenido (en caliente) se asienta en torno a **10214 GFLOPS**. El ancho de banda de memoria medido (clpeak) es de **~350–367 GB/s**.

> **Lotería del silicio.** En chips recuperados o de «descarte» algunas CU pueden ser flojas. El [Tuner](/es/docs/control-center) trae una **«Prueba de CU»** que esfuerza cada pareja con vkpeak y señala fallos o cuelgues de la GPU, para confirmar que tu chip aguanta las 40. (Mecanismo con `umr`, escribiendo las máscaras WGP; crédito a [bc250-cu-live-manager](https://github.com/WinnieLV/bc250-cu-live-manager), reimplementación propia.)

## Protección térmica: el tope de 85 °C

El techo térmico es de **85 °C** y se respeta en dos niveles:

1. **desde el gobernador**: `gradi_max` y `watt_max` en `/etc/skillfish-vf-governor.json` bajan el tope de frecuencia *antes* de cruzar los 85 °C o el límite de potencia (el nuestro, no el del firmware), y lo devuelven cuando la placa se ha calmado;
2. **desde el sistema**: **skillfish-vf-watchdog**, un proceso aparte que toma el control si el gobernador se cae con el reloj forzado.

Cosas que conviene saber sobre la refrigeración de serie (ver también [Hardware BC-250](/es/docs/hardware-bc250) para **cajas imprimibles en 3D y ventiladores recomendados**):

- el disipador de serie va **justo**: comparar pruebas «seguidas» falsea los resultados por el *calor acumulado*; deja enfriar la placa unos minutos entre pasadas;
- solo existe el sensor de *borde* de la GPU; **no hay sensor de temperatura de la VRAM**;
- el ancho de banda de memoria es bueno, pero `mclk` **no** se puede tocar.

## Un caso real: juegos limitados por CPU

Algunos títulos —como *Black Myth: Wukong* en **partida**— están limitados por la **CPU y las llamadas de dibujo**: los FPS apenas dependen de la resolución ni de la frecuencia de la GPU. Ahí ayudan el overclock de **CPU** y una buena refrigeración. Para el reescalado, FSR 4 pasa por [OptiScaler](https://github.com/optiscaler/OptiScaler) en la ruta DLSS del juego (ver [Juegos](/es/docs/gaming)).

Cuando la carga **sí** está limitada por la GPU (por ejemplo el *vuelo de cámara* del benchmark de Wukong), el tope de la curva cuenta: en el [Tuner](/es/docs/control-center) sube el perfil de Cautious o Balanced a **Performance** (2100 MHz), o escribe tu propia curva. La ventaja medida en Wukong frente al viejo gobernador de fábrica es de **+4,5 % con la placa fría y +11 % con la placa caliente**: el gobernador V/F no pierde reloj al calentarse, cosa que sí hace el de fábrica. Sigue habiendo un límite físico infranqueable: **1129 mV**, el tope de voltaje que amdgpu declara para esta GPU; ninguna curva puede superarlo.

## Todo esto, sin terminal

Frecuencias, la curva de la GPU, ventilador y unidades de cómputo se ajustan desde la interfaz del **Tuner**, con los tres perfiles de la GPU listos y una **prueba automática de 25 segundos que vuelve a la curva anterior** si tu placa no la aguanta; ver [Control Center](/es/docs/control-center). Es la vía recomendada: empieza en Cautious, sube a Balanced o Performance, y el Tuner lo valida todo en **tu** BC-250.

## Fuentes

- skillfish-vf-governor — nuestro gobernador V/F de la GPU, control directo por SMU con tope configurable
- [bc250_smu_oc (bc250-collective)](https://github.com/bc250-collective/bc250_smu_oc) — overclock y undervolt de la CPU por la SMU
- [bc250.info](https://bc250.info) — puntos seguros y notas térmicas de la comunidad
- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) — pruebas de FP32 y de ancho de banda de memoria

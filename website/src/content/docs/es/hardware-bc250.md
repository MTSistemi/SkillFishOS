---
title: El hardware AMD BC-250
description: La placa, su APU, las especificaciones y sus defectos conocidos.
group: Introducción
order: 2
---

La **AMD BC-250** es una placa compacta basada en una **APU semipersonalizada** con nombre en clave *Oberon* para la CPU y *Cyan Skillfish* para los gráficos: la misma familia de silicio que las consolas de la generación actual de AMD. Se fabricó para sistemas de minería (normalmente con varias placas por chasis) y hoy aparece en el mercado de segunda mano a precios bajos.

## Especificaciones principales

| Componente | Detalle |
|---|---|
| **CPU** | 8 núcleos / 16 hilos **Zen 2** (la placa muestra 6; SkillFishOS desbloquea los otros dos por el SMU) («Oberon»), hasta **3,9 GHz** (turbo), 4,0 GHz validados |
| **GPU** | **RDNA 2** «Cyan Skillfish» (`gfx1013`), hasta **40 unidades de cómputo** desbloqueables |
| **Memoria** | **16 GB GDDR6** compartida (UMA) entre CPU y GPU |
| **Cómputo** | ~**11,3 TFLOPS** FP32 con 40 CU / 2000 MHz (medido con vkpeak) |
| **Ancho de banda de memoria** | ~350–367 GB/s (medido con clpeak) |
| **Salida de vídeo** | 1× DisplayPort |

La memoria es **unificada**: la GDDR6 se reparte entre el sistema y los gráficos. De serie se asignan unos 8 GB como VRAM, pero en Linux el espacio de vídeo se puede ampliar con el **GTT** (Graphics Translation Table), de modo que Vulkan ve unos 13 GiB — especialmente útil para los modelos de IA.

## Desbloqueo de los 8 núcleos de la CPU

La placa se presenta como **6 núcleos / 12 hilos**, pero los núcleos físicos son **ocho**: los dos que faltan no están defectuosos, están apagados por configuración del producto. Lo delata la máscara de presencia de núcleos — en prácticamente todas las placas vale `0x77`, un valor **simétrico**: cuatro núcleos por complejo, con el cuarto desactivado en ambos. Un descarte real de fabricación dejaría un patrón asimétrico, porque los defectos no se reparten con tanta pulcritud.

SkillFishOS reescribe esa máscara a través del **SMU** en el arranque y la placa vuelve como **8 núcleos / 16 hilos**. Sin BIOS modificada y sin soldador.

En el servicio hay dos salvaguardas: si la máscara **no** es `0x77` no toca nada, porque un patrón distinto puede significar que los núcleos sí se desactivaron en fábrica; y el reinicio en caliente ocurre **solo después** de releer y confirmar la escritura, así que no puede entrar en un bucle de reinicios.

> Medido en nuestra propia placa: **+20%** en trabajo multihilo. En cargas de pocos hilos no cambia nada, como era de esperar: dos núcleos de más no hacen que un hilo corra más rápido.

La ingeniería inversa es [bc250-core-unlock (rw-r-r-0644)](https://github.com/rw-r-r-0644/bc250-core-unlock): sin ese trabajo esta función no existiría.

## Desbloqueo de las 40 CU

La GPU tiene 40 CU, pero el controlador activa solo **24** de serie. SkillFishOS **las lleva a 40 en caliente** (sin reiniciar): arranca con el mínimo del controlador y un servicio sube a 40 al inicio, ajustable desde el [Tuner](/es/docs/app-native). La ingeniería inversa del desbloqueo está documentada en [bc250-40cu-unlock](https://github.com/duggasco/bc250-40cu-unlock); el control en caliente con `umr` se inspira en [bc250-cu-live-manager](https://github.com/WinnieLV/bc250-cu-live-manager) (reescrito desde cero).

> Con las 40 CU activas, SkillFishOS mide **11385 GFLOPS** FP32 (vkpeak) en frío, frente a unos 6141 de una configuración base de 24 CU: alrededor de **+85%**.

## Defectos del hardware que conviene conocer

La BC-250 es hardware de «minería» reaprovechado: tiene limitaciones que SkillFishOS sortea por software. Conocerlas explica muchas decisiones del sistema.

### Hot-Plug Detect (HPD) del DisplayPort averiado

La detección del monitor en el conector DisplayPort **no funciona**: la placa no «ve» que has enchufado una pantalla. SkillFishOS lo resuelve con un servicio propio (`skillfish-dp-hotswap`) que fuerza la detección al arrancar y vigila los cambios de monitor durante el uso, más el parámetro del núcleo `video=DP-1:e` como respaldo. Ver [Escritorio](/es/docs/desktop) y [Solución de problemas](/es/docs/risoluzione-problemi).

### Suspensión ACPI rota

La suspensión (**s2idle está rota**): la placa se duerme pero **no despierta** y hace falta un reinicio. Además, una máquina suspendida queda inalcanzable a distancia. Por eso SkillFishOS **desactiva de forma permanente** todos los estados de reposo (ver [Escritorio](/es/docs/desktop)). Es una medida obligatoria.

### IOMMU inservible

La IOMMU de la BC-250 es inestable: **no debe activarse nunca**. El sistema arranca siempre sin IOMMU.

### Sensores térmicos

Solo está disponible el sensor de temperatura del *borde* de la GPU; **no hay sensor de temperatura de la VRAM**. La refrigeración de serie va justa, así que comparar pruebas lanzadas una detrás de otra no vale (efecto de calentamiento acumulado): deja enfriar la placa unos minutos entre pasadas.

## Refrigeración, cajas imprimibles y ventiladores

La BC-250 llega **desnuda**, pensada para estanterías de minería con cinco ventiladores «chillones» de 80 mm alimentados por el conector de distribución. Para uso de escritorio hace falta refrigeración propia. Hay que enfriar **dos cosas**: el disipador de la APU **y** los chips de **GDDR6**, que se calientan mucho y no tienen sensor de temperatura (ver [GPU y overclock](/es/docs/gpu-overclock)).

**Lo que funciona (consejos de la comunidad):**

- **2 ventiladores de 120 mm** de presión estática apuntando al disipador es el montaje de escritorio más habitual; sin caja se pueden apoyar directamente sobre el disipador (con bridas por las aletas).
- Un **ventilador dedicado a la VRAM** es muy recomendable si haces overclock: los módulos GDDR6 son el punto más caliente.
- El ventilador se conecta al conector **PWM de 4 pines** de la placa — SkillFishOS lo maneja con `nct6686` (sensores) y lo deja en **automático**.

**Cajas y conductos (STL gratuitos, imprimibles en 3D):**

| Modelo | Autor | Notas |
|---|---|---|
| [Console Style Case](https://www.thingiverse.com/thing:7172528) | Arthrimus | Caja «consola» con hueco para la fuente, conducto para **1× 120 mm** |
| [ASRock BC-250 Shell Case](https://www.printables.com/model/1228207-asrock-amd-bc-250-shell-case) | onemorecap | Carcasa a presión, montaje rápido de un ventilador |
| [Yet Another BC-250 Fan Shroud](https://www.printables.com/model/1339540-yet-another-bc-250-fan-shroud) | ViRazY | Entrada de **140 mm** y salida de **120 mm** |
| [Case ATX PSU & Fan Duct](https://www.printables.com/model/1616167-amd-bc-250-case-atx-psu-fan-duct) | ZMASLO | Usa una fuente ATX estándar, conducto que no daña el disipador |
| [Standard ATX PSU case](https://www.thingiverse.com/thing:7269520) | CatSiewDai | Caja completa para fuentes ATX |
| [OC vRAM Fan Kit (remix)](https://www.thingiverse.com/thing:7271946) | marccyberwiz | Kit de ventilador **dedicado a la VRAM** para overclock |
| [NexGen3D — DIY Steam Machine (Bazzite)](https://www.printables.com/model/1499974-nexgen3d-diy-steam-machine-powered-by-bazzite) | NexGen3D | Caja completa estilo **Steam Machine** para la BC-250 |
| [NexGen3D — Steam Machine PRO (refrigeración líquida)](https://www.printables.com/model/1614131-nexgen3d-diy-steam-machine-pro-liquid-cooled-bc-25/files) | NexGen3D | Versión **PRO con líquida** (AIO) — refrigeración máxima |
| [NexGen3D — soporte AIO para la BC-250](https://www.printables.com/model/1554003-nexgen3d-aio-mount-for-the-bc-250) | NexGen3D | Soporte para montar un **AIO** (refrigeración líquida) en la BC-250 |

> Guía de referencia sobre refrigeración: [Cooling Solutions — amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs/hardware/cooling/).

## Fuentes

- [bc250.info](https://bc250.info) — wiki de la comunidad
- [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs) — documentación técnica (incluida la de [refrigeración](https://elektricm.github.io/amd-bc250-docs/hardware/cooling/))
- [mothenjoyer69/bc250-documentation](https://github.com/mothenjoyer69/bc250-documentation) — notas de hardware y refrigeración
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock) — desbloqueo de las unidades de cómputo
- [bc250_memcfg (fanoush)](https://github.com/fanoush/bc250_memcfg) — configuración de la memoria
- Controlador del núcleo Linux `amdgpu` — [docs.kernel.org/gpu/amdgpu](https://docs.kernel.org/gpu/amdgpu/)

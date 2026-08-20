---
title: Glosario
description: Los términos técnicos de SkillFishOS y de la BC-250, explicados en corto.
group: Referencia
order: 5
---

Los términos que se repiten por toda la documentación, cada uno explicado en una línea. Por orden alfabético.

## Hardware y APU

**APU** — *Accelerated Processing Unit*: un chip que integra CPU y GPU en la misma pastilla. La BC-250 lleva una semipersonalizada de AMD.

**BC-250** — la placa sobre la que corre SkillFishOS: APU Zen 2 + RDNA 2, 16 GB GDDR6, hecha en origen para minar.

**Cyan Skillfish** — el nombre en clave de la parte **gráfica** (GPU) de la APU de la BC-250. De ahí el nombre «SkillFish».

**Oberon** — el nombre en clave de la parte de **CPU** (Zen 2) de esa misma APU.

**Unidad de cómputo (CU)** — los bloques de cálculo de la GPU. La BC-250 tiene 40, pero de serie muestra menos: SkillFishOS **las desbloquea todas** (ver [núcleo](/es/docs/kernel)).

**gfx1013** — el identificador de la arquitectura gráfica de la BC-250 (familia RDNA 2). Importa porque **ROCm no lo soporta** → en su lugar se usa Vulkan.

**RDNA 2** — la arquitectura gráfica de AMD de esta GPU (la misma familia que las consolas actuales).

**Zen 2** — la arquitectura de CPU de AMD de esta APU (**8 núcleos / 16 hilos**: la placa muestra 6, SkillFishOS desbloquea los otros dos por el SMU).

**GDDR6** — el tipo de memoria de la placa: rápida y aquí **compartida** entre CPU y GPU.

**UMA** — *Unified Memory Architecture*: la CPU y la GPU usan **el mismo** conjunto de memoria (los ~16 GB de GDDR6).

**GTT** — *Graphics Translation Table*: el mecanismo que deja a la GPU usar memoria del sistema más allá de la VRAM dedicada. SkillFishOS lo amplía para que Vulkan vea unos 13 GiB (útil para la IA).

## Frecuencias, voltajes, temperatura

**SMU** — *System Management Unit*: el microcontrolador dentro de la APU que gobierna frecuencias y voltajes. En la BC-250 el control pasa **solo** por él, no por los archivos estándar de amdgpu en sysfs.

**Gobernador SMU** — el servicio (`cyan-skillfish-governor`) que fija los *puntos seguros* de frecuencia y voltaje de la GPU.

**sclk / mclk** — frecuencia del **núcleo** gráfico (sclk) y de la **memoria** (mclk). En la BC-250 la mclk **no** se puede ajustar.

**Undervolt** — bajar el voltaje a la misma frecuencia: el mismo trabajo, **menos calor y menos consumo**. Ver [GPU y overclock](/es/docs/gpu-overclock).

**Overclock (OC)** — subir las frecuencias por encima de las de fábrica para ganar rendimiento.

**Vid** — el voltaje que el chip pide a una frecuencia dada. En la BC-250 el máximo absoluto es **1,325 V**.

**Protección térmica** — el vigilante del sistema que baja las frecuencias si se pasan los 85 °C.

**Calentamiento acumulado (heat-soak)** — el calor que se acumula y falsea las pruebas hechas una detrás de otra: deja enfriar la placa entre pasadas.

**Lotería del silicio** — el hecho de que cada chip aguante un overclock y un undervolt distintos; por eso SkillFishOS valida los perfiles **en tu** placa.

## Software del sistema

**Debian sid** — la rama *unstable* de Debian, siempre al día pero propensa a retrocesos: la base de SkillFishOS (ver [Actualizaciones](/es/docs/aggiornamenti)).

**KDE Plasma 6** — el entorno de escritorio que se usa, vestido con la estética steampunk.

**linux-tkg** — la receta de compilación del núcleo (Frogging-Family) en la que se basa el núcleo a medida de SkillFishOS.

**Mesa / RADV** — los controladores gráficos de código abierto; **RADV** es el controlador **Vulkan** que usa la GPU de la BC-250.

**ROCm** — el conjunto de cómputo «oficial» de AMD: **no** soporta gfx1013, así que no se usa.

**Vulkan** — la interfaz de gráficos y cómputo que se usa tanto para jugar como para la **IA** (Unsloth Studio) en la BC-250.

**Btrfs** — el sistema de archivos copy-on-write con instantáneas que aporta la «red de seguridad» (ver [Almacenamiento e instantáneas](/es/docs/storage-snapshot)).

**Snapper** — la herramienta que crea instantáneas Btrfs automáticas antes y después de las actualizaciones.

**grub-btrfs** — hace que las instantáneas aparezcan en el menú de GRUB para volver atrás desde el arranque.

**Fijado de APT (pinning)** — mantener un paquete en una versión verificada, para los componentes frágiles en este hardware.

**reprepro** — la herramienta con la que se gestiona el repositorio APT firmado de SkillFishOS.

**HPD** — *Hot-Plug Detect*: la detección del monitor conectado. En la BC-250 está **averiada** → el servicio `skillfish-dp-hotswap`.

**s2idle / suspensión** — los estados de reposo ACPI: **rotos** en la BC-250 y por eso desactivados.

**IOMMU** — la unidad de gestión de memoria para virtualizar la entrada y salida: inestable en la BC-250, **nunca** se activa.

## Juegos e IA

**Proton** — la capa de compatibilidad de Valve que ejecuta juegos de Windows en Linux a través de Steam.

**gamescope** — el microcompositor de Valve para jugar (sesión «consola», escalado FSR1/NIS).

**EmuDeck / ES-DE** — el instalador de emuladores y la interfaz para la emulación.

**FSR / OptiScaler** — tecnologías de **escalado**. FSR 4 no está disponible (necesita RDNA 4); se usan FSR1/NIS u OptiScaler.

**Unsloth Studio** — motor e interfaz de la IA local: ejecuta modelos GGUF en la GPU y ofrece una API compatible con la de OpenAI.

**qwen3:14b** — el modelo de IA de referencia, funcionando enteramente en la GPU.

**Tuner** — la aplicación propia de SkillFishOS para ajustar el hardware con prueba y retroceso (ver [Aplicaciones propias](/es/docs/app-native)).

## Fuentes

- [bc250.info](https://bc250.info) · [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- [Documentación de amdgpu](https://docs.kernel.org/gpu/amdgpu/) · [Mesa / RADV](https://docs.mesa3d.org/drivers/radv.html)

---
title: El núcleo a medida
description: El núcleo linux-tkg parcheado para la BC-250, los parámetros de arranque y los núcleos a evitar.
group: Sistema
order: 1
---

El corazón de las optimizaciones de SkillFishOS es un **núcleo compilado a medida** para la BC-250, basado en [linux-tkg](https://github.com/Frogging-Family/linux-tkg) — una receta de compilación de la *Frogging Family* que aplica parches orientados al rendimiento y a los juegos.

## Versión y parches

El núcleo de SkillFishOS es la versión **`7.2.0-skillfishos`** (las series 7.0 y 7.1 están fuera de mantenimiento). Sobre los parches estándar de linux-tkg incluye:

- el parche de **desbloqueo de frecuencia** de la BC-250 (rango 350–2230 MHz);
- el parche de **40 CU**, que activa todas las unidades de cómputo de la GPU;
- un parche propio **RDSEED-quiet**, que calla un mensaje ruidoso del núcleo en este hardware.

El paquete del núcleo (imagen y cabeceras) se publica como entrega y está **retenido** (`apt-mark hold`) para que una actualización de Debian no lo sustituya por un núcleo inadecuado. Es el núcleo por defecto en GRUB.

## Parámetros de arranque (cmdline)

La línea de órdenes del núcleo está configurada así, y cada parámetro tiene un motivo preciso:

```
mitigations=off
split_lock_detect=off
ttm.pages_limit=1572864
ttm.page_pool_size=1572864
```

| Parámetro | Qué hace |
|---|---|
| `mitigations=off` | desactiva las protecciones contra Spectre y Meltdown para exprimir el rendimiento (una decisión aceptable en una consola de casa) |
| `ttm.pages_limit` / `ttm.page_pool_size` | el techo del GTT, contado en páginas de 4 KiB: 1572864 = 6 GiB, de modo que Vulkan ve unos 13 GiB entre VRAM y GTT (útil para la IA). Antes era `amdgpu.gttsize`, en desuso desde el núcleo 7.x: con ambos puestos, el controlador obedece a este y lo dice en cada arranque |
| `split_lock_detect=off` | desactiva el detector de *split lock*, que si no ahoga los procesos que hacen accesos atómicos no alineados (los juegos y los emuladores los hacen) |

> **¿Y el DisplayPort?** El HPD de la BC-250 está averiado (ver [hardware](/es/docs/hardware-bc250)), pero SkillFishOS **no** usa el parámetro `video=DP-1:e`: el servicio `skillfish-dp-hotswap` vigila el EDID y vuelve a habilitar la salida cuando el monitor regresa. Eso cubre además el caso de encender el monitor después de la placa, que el parámetro por sí solo no resuelve.

> **Unidades de cómputo en caliente.** SkillFishOS ya no usa el parámetro `amdgpu.bc250_cc_write_mode=3` (que clavaba 40 CU en el arranque y bloqueaba los cambios en caliente). Ahora el sistema arranca con el mínimo del controlador (24 CU) y un servicio **lleva a 40 en caliente** al inicio; puedes cambiarlas sin reiniciar desde el [Tuner](/es/docs/app-native). Ver [GPU y overclock](/es/docs/gpu-overclock).

## Núcleos a evitar

No todos los núcleos recientes se llevan bien con este hardware. En particular, las series **6.15.0–6.15.6** y **6.17.8–6.17.10** son conocidas por dar problemas y conviene esquivarlas. SkillFishOS trae su propio núcleo probado justamente para evitar esos retrocesos — ver [Actualizaciones](/es/docs/aggiornamenti).

## IOMMU

Como se dice en la página de [hardware](/es/docs/hardware-bc250), **la IOMMU no debe activarse nunca** en la BC-250: es inestable. El núcleo arranca siempre con la IOMMU desactivada.

## Por qué un núcleo propio y no XanMod ni el estándar

- Al **núcleo estándar de Debian** le faltan los parches de la BC-250 (desbloqueo de frecuencia, 40 CU) y arrastra los retrocesos mencionados arriba.
- **linux-tkg** facilita aplicar los parches propios y elegir planificadores y opciones pensados para jugar.
- Compilarlo nosotros significa que actualizamos el núcleo **solo cuando una versión nueva aporta algo real** y después de probarla en el hardware.

## Fuentes

- [linux-tkg (Frogging-Family)](https://github.com/Frogging-Family/linux-tkg)
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock)
- [Parámetros del controlador amdgpu](https://docs.kernel.org/gpu/amdgpu/module-parameters.html)
- [bc250.info](https://bc250.info) — notas sobre el núcleo y la línea de órdenes

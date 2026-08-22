---
title: Almacenamiento e instantáneas Btrfs
description: "La red de seguridad de SkillFishOS: instantáneas automáticas y vuelta atrás desde el arranque."
group: Sistema
order: 3
---

Una de las ideas centrales de SkillFishOS es poder **trastear sin miedo**. Lo hace posible el sistema de archivos **[Btrfs](https://btrfs.readthedocs.io/)** con instantáneas automáticas: cada cambio importante queda capturado, y si algo se rompe vuelves atrás con un clic.

## Subvolúmenes separados

El disco tiene una sola partición Btrfs, repartida en subvolúmenes distintos:

- **`@`** — el sistema operativo;
- **`@home`** — los datos del usuario;
- **`@cache`** y **`@log`** — cachés y registros, dejados fuera de las instantáneas para que una vuelta atrás no arrastre consigo los registros de ayer;
- **`@games`** — la biblioteca de juegos, que si no haría enorme cada instantánea;
- **`@swap`** — el archivo de intercambio.

Mantenerlos separados es esencial: volver atrás el sistema **no toca los archivos personales**. Puedes regresar a un sistema de «ayer» conservando los documentos, las partidas guardadas y los ajustes de hoy.

## Instantáneas automáticas con Snapper

SkillFishOS usa **[Snapper](http://snapper.io/)** con una configuración `root` y **enganches antes y después en APT**: cada vez que instalas o actualizas paquetes se crea una instantánea automáticamente *antes* y *después*. Así, si una actualización da problemas, la instantánea de «antes» ya está ahí.

De la configuración conviene destacar:

- un tope de instantáneas conservadas para que el disco no se llene;
- instantáneas guardadas en los *hitos* importantes del sistema;
- gestión desde una ventana con **SkillFishOS Instantáneas**, la aplicación que hemos escrito nosotros.

## Cuántas se guardan

**Cinco**, de serie: tres normales (la pareja antes/después de cada operación de `apt`) y dos «importantes» — las actualizaciones que tocan el núcleo o systemd, que son justo las que más probablemente querrás recuperar. Por encima está el punto *«SkillFishOS - clean install»*, que no caduca nunca: el camino de vuelta al sistema tal como salió de fábrica.

La línea horaria está **desactivada**. En una consola de casa solo se come disco sin que nadie mire nunca esas instantáneas. Las instantáneas que creas **a mano** no cuentan entre las cinco y no se borran solas: si hiciste una a propósito, se queda hasta que la quites.

## Vuelta atrás desde el menú de arranque

Gracias a **[grub-btrfs](https://github.com/Antynea/grub-btrfs)**, las instantáneas aparecen directamente en el menú de **GRUB**, bajo *«SkillFishOS snapshots»*. Reinicia, elige la instantánea de antes del problema y estarás dentro de ella.

Dos cosas que conviene saber antes de confiar en esto:

- **Lo que arrancas es de solo lectura.** Es un entorno de rescate: mira alrededor, comprueba si el estado anterior estaba realmente bien, saca los archivos que necesites. Algunos servicios darán error al arrancar — simplemente no pueden escribir. Es lo esperado, no un fallo.
- **El menú de arranque se refresca tras cada operación de `apt`**, así que la instantánea tomada *antes* de una actualización está en la lista justo cuando la necesitas.

## Cómo hacer permanente la vuelta atrás

Arrancar una instantánea no cambia nada por sí solo, y `snapper rollback` aquí no ayuda: cambia el subvolumen por defecto, mientras que nuestra entrada de GRUB fija `subvol=@` y gana. La orden que hace el trabajo es:

```bash
sudo skillfish-rollback --list    # qué instantáneas hay
sudo skillfish-rollback 12        # la instantánea 12 pasa a ser el sistema desde el próximo arranque
```

Aparta el sistema actual — no lo borra, lo convierte en `@-rotto-<fecha>` — y construye a partir de la instantánea elegida un `@` nuevo y escribible, llevándose consigo todo el historial de instantáneas. Si resulta que el estado anterior tampoco era la solución, `sudo skillfish-rollback --undo` lo devuelve todo, y `--clean` libera el espacio cuando ya estés seguro.

Funciona desde el sistema normal y desde dentro de una instantánea arrancada en solo lectura, que es el caso que importa cuando la máquina ya no arranca.

> **Tu carpeta personal no se toca nunca.** `@home` es un subvolumen aparte: el sistema viaja al pasado, tus archivos se quedan como están. Conviene saberlo, y recordarlo antes de contar con una vuelta atrás para recuperar un documento que borraste — no lo hará.

> Esta es la red de seguridad que permite que hasta los más pequeños exploren el sistema sin miedo a romperlo sin remedio.

## Por qué Btrfs y no Timeshift

SkillFishOS eligió **Btrfs + Snapper + grub-btrfs** frente a soluciones como Timeshift porque:

- la integración con APT es automática (una instantánea en cada operación de paquetes);
- las instantáneas son nativas del sistema de archivos (instantáneas de verdad, *copy-on-write*, baratas);
- la vuelta atrás está disponible **desde el arranque**, aunque el sistema ya no arranque de forma normal.

## Fuentes

- [Documentación de Btrfs](https://btrfs.readthedocs.io/)
- [Snapper](http://snapper.io/)
- [grub-btrfs (Antynea)](https://github.com/Antynea/grub-btrfs)

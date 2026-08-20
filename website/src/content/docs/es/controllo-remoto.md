---
title: Control remoto — Remote Manager
description: El panel web de SkillFishOS para manejar la BC-250 desde el navegador o el móvil — telemetría, KVM, terminal, Tuner, tienda de aplicaciones e IA.
group: Uso
order: 4
---

**SkillFishOS Remote Manager** es un panel web modular que permite manejar la BC-250 **desde otro PC o desde el móvil**, en la misma red local o —a través de ZeroTier— desde cualquier parte del mundo. Entras con tus credenciales del sistema, todo por HTTPS.

## Instalación

```bash
sudo apt update
sudo apt install skillfish-dashboard
```

El paquete instala el servicio, la aplicación propia **Remote Manager** (para encender y apagar el panel y elegir los módulos) y todas las páginas web. Las dependencias opcionales (KVM, terminal, Wake-on-LAN) son *Recommends* y se instalan solas cuando están disponibles.

## Activación

Abre **SkillFishOS Remote Manager** desde el menú de aplicaciones:

- **Interruptor principal** — arranca el servicio (de forma persistente, con systemd).
- **Casillas de los módulos** — elige qué mostrar (telemetría, Tuner, Hub, KVM, terminal, IA…).
- Muestra la **dirección, un código QR y las credenciales** para conectarte.

O desde una terminal: `sudo systemctl enable --now skillfish-dashboard`.

> Por seguridad, el panel **no arranca solo** después de instalarlo: lo activas cuando quieres.

## Acceso

Abre **`https://<ip-de-la-placa>:8443`** en el navegador (o `https://BC-250.local:8443`). Como el certificado es autofirmado, la primera vez el navegador avisará — es lo esperado, continúa.

Entra con **tu usuario y contraseña del sistema** (los mismos del acceso a SkillFishOS): la comprobación se hace con PAM.

## Los módulos

El panel se compone con los módulos que hayas activado:

- **Telemetría** — gráficas en vivo de temperaturas, frecuencias, vatios y carga de CPU y GPU, con los valores en el eje vertical y un panel de barras que muestra la **frecuencia por núcleo e hilo** (los 16 hilos, con los apagados claramente marcados).
- **Estado del sistema** — nombre de la máquina, IP, núcleo, tiempo encendida, memoria, disco, CU activas, cuelgues detectados.
- **Controles (Tuner)** — perfiles rápidos y el **Tuner completo** en la web: CPU (frecuencia, undervolt, temperatura), GPU (frecuencia, voltaje, gobernador), **control de las unidades de cómputo en caliente** (rejilla WGP, sin reiniciar), ventilador, VRAM, *Prueba* y los asistentes **«Encuentra mi máximo»**.
- **Programas y paquetes (Hub)** — una **tienda de aplicaciones** de verdad (AppStream + Flatpak + Snap): navegar por categorías, buscar, instalar y quitar, actualizar. Las **aplicaciones de SkillFishOS** aparecen destacadas arriba.
- **Escritorio (KVM)** — ver y manejar el escritorio real de la placa desde el navegador (noVNC), sin hardware adicional.
- **Terminal** — una consola web (ttyd) dentro del panel.
- **IA en el equipo** — estado del motor Unsloth, aceleración Vulkan y una conversación con el modelo local, funcionando en la GPU de la BC-250.
- **AI-Ops** — el modelo local lee los registros y la telemetría y diagnostica los problemas por ti.
- **Registros**, **reglas automáticas** (bajar la frecuencia por encima de un umbral de °C), **Wake-on-LAN** y encendido y apagado programados.
- **ZeroTier** — para llegar al panel **desde cualquier sitio** (ver más abajo).

Los botones **Reiniciar** y **Apagar** están siempre en la barra superior. Las tarjetas se pueden **cerrar, volver a abrir y arrastrar**, y la **disposición se guarda**.

## Acceso a distancia (ZeroTier)

El panel está pensado para la **red local**. Para usarlo desde fuera, activa el módulo **ZeroTier**: únete a una de tus redes, autoriza la placa en [my.zerotier.com](https://my.zerotier.com) y luego abre el panel en la dirección ZeroTier de la placa — sin abrir ningún puerto del router.

## Seguridad

- **HTTPS** con certificado autofirmado (TLS 1.2 o superior), generado en el primer arranque.
- **Entrada por PAM** con tus credenciales, **sesiones firmadas** (HMAC) y **límite de intentos**.
- Pensado para la **red local**; para el acceso remoto usa ZeroTier en lugar de exponerlo directamente a internet.

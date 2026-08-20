---
title: Der maßgeschneiderte Kernel
description: Der für die BC-250 gepatchte linux-tkg-Kernel, die Startparameter und die Kernel, die man meiden sollte.
group: System
order: 1
---

Das Herz der Optimierungen von SkillFishOS ist ein **eigens gebauter Kernel** für die BC-250, auf Grundlage von [linux-tkg](https://github.com/Frogging-Family/linux-tkg) — einem Baurezept der *Frogging Family*, das auf Leistung und Spiele ausgerichtete Patches einspielt.

## Fassung und Patches

Der Kernel von SkillFishOS trägt die Fassung **`7.1.7-skillfishos`** (die Reihe 7.0 wird nicht mehr gepflegt). Zusätzlich zu den üblichen linux-tkg-Patches enthält er:

- den Patch zum **Entsperren der Taktraten** der BC-250 (Bereich 350–2230 MHz);
- den **40-CU-Patch**, der alle Recheneinheiten der GPU einschaltet;
- einen eigenen **RDSEED-quiet**-Patch, der eine geschwätzige Kernel-Meldung auf dieser Hardware verstummen lässt.

Das Kernel-Paket (Abbild und Header) wird als Auslieferung veröffentlicht und ist **festgehalten** (`apt-mark hold`), damit eine Debian-Aktualisierung es nicht durch einen unpassenden Kernel ersetzt. Es ist der voreingestellte Kernel in GRUB.

## Startparameter (cmdline)

Die Befehlszeile des Kernels ist so eingestellt, und jeder Parameter hat einen genauen Grund:

```
mitigations=off
split_lock_detect=off
ttm.pages_limit=1572864
ttm.page_pool_size=1572864
```

| Parameter | Was er bewirkt |
|---|---|
| `mitigations=off` | schaltet die Gegenmaßnahmen zu Spectre und Meltdown ab, um die Leistung auszureizen (auf einer Konsole zu Hause eine vertretbare Entscheidung) |
| `ttm.pages_limit` / `ttm.page_pool_size` | die Obergrenze der GTT, in Seiten zu 4 KiB gezählt: 1572864 = 6 GiB, sodass Vulkan rund 13 GiB aus Grafikspeicher und GTT sieht (nützlich für die KI). Früher war das `amdgpu.gttsize`, seit Kernel 7.x veraltet: sind beide gesetzt, hält sich der Treiber an diesen und sagt es bei jedem Start |
| `split_lock_detect=off` | schaltet die Erkennung von *split locks* ab, die sonst Prozesse ausbremst, die unausgerichtete atomare Zugriffe machen (Spiele und Emulatoren tun das) |

> **Und der DisplayPort?** Das HPD der BC-250 ist defekt (siehe [Hardware](/de/docs/hardware-bc250)), aber SkillFishOS benutzt den Parameter `video=DP-1:e` **nicht**: der Dienst `skillfish-dp-hotswap` beobachtet die EDID und schaltet den Ausgang wieder ein, sobald der Bildschirm zurück ist. Das deckt auch den Fall ab, dass der Bildschirm nach der Platine eingeschaltet wird — was der Parameter allein nicht schafft.

> **Recheneinheiten im laufenden Betrieb.** SkillFishOS benutzt den Parameter `amdgpu.bc250_cc_write_mode=3` nicht mehr (er nagelte 40 CU beim Start fest und verhinderte Änderungen im Betrieb). Das System startet nun mit dem Grundwert des Treibers (24 CU), und ein Dienst **hebt sie beim Hochfahren im Betrieb auf 40**; ändern lassen sie sich ohne Neustart im [Tuner](/de/docs/app-native). Siehe [GPU und Übertaktung](/de/docs/gpu-overclock).

## Kernel, die man meiden sollte

Nicht jeder neuere Kernel verträgt sich mit dieser Hardware. Vor allem die Reihen **6.15.0–6.15.6** und **6.17.8–6.17.10** sind als heikel bekannt und besser zu umgehen. SkillFishOS bringt seinen eigenen geprüften Kernel gerade deshalb mit, um diesen Rückschritten aus dem Weg zu gehen — siehe [Aktualisierungen](/de/docs/aggiornamenti).

## IOMMU

Wie auf der Seite zur [Hardware](/de/docs/hardware-bc250) steht, **darf die IOMMU auf der BC-250 niemals eingeschaltet werden**: sie ist unruhig. Der Kernel startet immer mit abgeschalteter IOMMU.

## Warum ein eigener Kernel und nicht XanMod oder der Standard

- Dem **Standardkernel von Debian** fehlen die BC-250-Patches (Entsperren der Taktraten, 40 CU), und er folgt den oben genannten Rückschritten.
- **linux-tkg** macht es leicht, die eigenen Patches einzuspielen und auf Spiele ausgerichtete Planer und Einstellungen zu wählen.
- Ihn selbst zu bauen heißt, dass wir den Kernel **nur dann aktualisieren, wenn eine neue Fassung wirklich etwas bringt** — und nachdem wir sie auf der Hardware geprüft haben.

## Quellen

- [linux-tkg (Frogging-Family)](https://github.com/Frogging-Family/linux-tkg)
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock)
- [Parameter des amdgpu-Treibers](https://docs.kernel.org/gpu/amdgpu/module-parameters.html)
- [bc250.info](https://bc250.info) — Notizen zu Kernel und Befehlszeile

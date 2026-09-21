---
title: Solução de problemas
description: As falhas mais comuns da BC-250 e como o SkillFishOS contorna cada uma.
group: Referência
order: 1
---

Muitos dos “problemas” da BC-250 são, na verdade, defeitos conhecidos do hardware que o SkillFishOS contorna sozinho. Estes são os mais comuns.

## A tela fica preta / o monitor não é detectado

O **Hot-Plug Detect (HPD) do DisplayPort é defeituoso**: a placa não percebe quando você liga um monitor. O SkillFishOS resolve isso com o serviço `skillfish-dp-hotswap` (que força a detecção no boot e ao trocar de monitor) e com o parâmetro de kernel `video=DP-1:e`.

O que conferir:

- use um **monitor com DisplayPort** ou um adaptador DP→HDMI **passivo**;
- evite adaptadores DP→HDMI **ativos**: além dos problemas de detecção, eles **quebram o áudio** (veja abaixo);
- se trocou de monitor, espere alguns segundos: a detecção é automática, mas não instantânea.

## A placa não acorda da suspensão

A suspensão está **quebrada no nível do hardware**. É exatamente por isso que o SkillFishOS a desativa por completo (veja [Área de trabalho](/pt/docs/desktop)). Se a placa parecer “morta” depois de um tempo parada e o gerenciamento de energia tiver sido mexido, a única saída é um **reset físico**. Não reative os estados de sono.

## Sem áudio pelo monitor ou pela TV

O áudio pelo DisplayPort funciona, mas:

- adaptadores DP→HDMI **ativos** quebram o áudio: use passivos, um monitor DP nativo, uma **placa de som USB** ou áudio por **Bluetooth**;
- quem cuida do som é o **PipeWire**: a saída padrão se escolhe nas configurações de áudio do KDE.

## Os controles não funcionam

- Os controles **DualShock 4** vão por **Bluetooth** (com giroscópio). Para parear: segure *Share + PS* até piscarem e pareie pela janela do Bluetooth.
- Um controle **por USB** precisa de um cabo **de dados** (não só de carga): ele é reconhecido como um Xbox 360.
- Controles genéricos às vezes não se dão bem com os DS4 no mesmo adaptador Bluetooth: nesse caso use-os **por USB**.

## A GPU parece lenta / as temperaturas estão altas

- Confira no [Tuner](/pt/docs/control-center) se as **40 CU** e o governador V/F (skillfish-vf-governor) estão ativos.
- Lembre que a refrigeração é justa: depois de carga prolongada entra a **proteção térmica** (85 °C). Para testes válidos, deixe a placa esfriar entre as passadas (veja [GPU](/pt/docs/gpu-overclock)).
- Em jogos que dependem da **CPU**, baixar a resolução não aumenta os FPS.

## A placa travou de vez

A BC-250 pode dar um **travamento total**, muitas vezes ligado a um **undervolt agressivo demais**: a instabilidade aparece principalmente com **pouca carga**, então um travamento pode acontecer até em repouso. O SkillFishOS ataca isso por dois lados:

- **Vigia por hardware** — o temporizador **SP5100 TCO** do chipset está ativo (`RuntimeWatchdogSec=2min`): se o sistema travar por completo, a placa **se reinicia sozinha** em menos de dois minutos, sem precisar tirar da tomada.
- **Detector de travamentos** — no boot, um serviço percebe se o desligamento anterior foi anormal (falta a marca de desligamento limpo) e **registra** isso em `/var/log/skillfish-freeze.log`, com um aviso na área de trabalho. A mesma informação aparece na página **Status** do [Control Center](/pt/docs/control-center).

Se os travamentos se repetirem, **abaixe o teto da curva** (por exemplo de Performance para Balanced ou Cautious) no Tuner: o valor menos agressivo quase sempre resolve. Cada curva é aplicada com **teste automático e volta atrás** — um travamento no meio do teste nunca deixa a placa com uma curva instável no próximo boot. Se persistirem até no Cautious, desconfie da **fonte de alimentação**.

## Uma atualização quebrou alguma coisa

Cada operação com pacotes faz um snapshot antes e outro depois. Os do menu **GRUB → “SkillFishOS snapshots”** arrancam **só de leitura**: servem para ver e copiar ficheiros, não para continuar a trabalhar. Para voltar atrás a sério, num terminal ou numa consola de texto (Ctrl+Alt+F3):

```
sudo skillfish-rollback --elenco
sudo skillfish-rollback <number>
sudo reboot
```

`<number>` é o snapshot “pre” mesmo antes da atualização má; `sudo skillfish-rollback --annulla` desfaz a reposição. A pasta pessoal não é tocada. Veja [Armazenamento e snapshots](/pt/docs/storage-snapshot).

## Uma atualização removeu o ambiente de trabalho

Em setembro de 2026 o Debian estava a recompilar o Qt e o KDE, e o **Discover** propôs uma atualização que removia todo o ambiente KDE. Desde então o SkillFishOS impede-o, e o Hub substituiu o Discover. Atualizem sempre pelo **SkillFishOS Hub**.

Se vos aconteceu, o snapshot de antes dessa atualização é o caminho mais limpo (ver acima). **Sem snapshots**, numa consola de texto (Ctrl+Alt+F3):

```
curl -fsSLo repair.sh https://skillfishos.com/repair.sh
sudo bash repair.sh
```

O script descobre o que essa atualização removeu, mostra o plano e pergunta antes de mudar alguma coisa. Não remove nada e não toca na pasta pessoal. Reiniciem quando disser *Done*.

## A IA não inicia ou devolve coisas estranhas

- A IA roda sobre Vulkan (não ROCm) e **não deve ser usada junto com os jogos** (dividem GPU e memória).
- Se a saída sair corrompida, garanta que o cache KV está em **f16** (`q4_0` corrompe a saída no RADV). Veja [IA no aparelho](/pt/docs/ai-locale).

## Fontes

- [bc250.info](https://bc250.info) · [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- [Arch Wiki — Gamepad](https://wiki.archlinux.org/title/Gamepad)
- [PipeWire — solução de problemas](https://docs.pipewire.org/)

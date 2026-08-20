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

- Confira no [Tuner](/pt/docs/app-native) se as **40 CU** e o governador SMU estão ativos.
- Lembre que a refrigeração é justa: depois de carga prolongada entra a **proteção térmica** (85 °C). Para testes válidos, deixe a placa esfriar entre as passadas (veja [GPU](/pt/docs/gpu-overclock)).
- Em jogos que dependem da **CPU**, baixar a resolução não aumenta os FPS.

## A placa travou de vez

A BC-250 pode dar um **travamento total**, muitas vezes ligado a um **undervolt agressivo demais**: a instabilidade aparece principalmente com **pouca carga**, então um travamento pode acontecer até em repouso. O SkillFishOS ataca isso por dois lados:

- **Vigia por hardware** — o temporizador **SP5100 TCO** do chipset está ativo (`RuntimeWatchdogSec=2min`): se o sistema travar por completo, a placa **se reinicia sozinha** em menos de dois minutos, sem precisar tirar da tomada.
- **Detector de travamentos** — no boot, um serviço percebe se o desligamento anterior foi anormal (falta a marca de desligamento limpo) e **registra** isso em `/var/log/skillfish-freeze.log`, com um aviso na área de trabalho. O contador também aparece no painel **“Meu silício”** do Tuner.

Se os travamentos se repetirem, **desça um perfil** (por exemplo de Crazy ou Turbo para Performance) no Tuner: o valor menos agressivo quase sempre resolve. Todos os perfis são **à prova de travamento** — um travamento no meio de um teste nunca deixa a placa com um perfil instável no próximo boot. Se persistirem até no Stock, desconfie da **fonte de alimentação**.

## Uma atualização quebrou alguma coisa

Reinicie e no menu **GRUB → “SkillFishOS snapshots”** escolha um snapshot anterior que funcionava. Veja [Armazenamento e snapshots](/pt/docs/storage-snapshot). Os snapshots de antes e depois da atualização são automáticos.

## A IA não inicia ou devolve coisas estranhas

- A IA roda sobre Vulkan (não ROCm) e **não deve ser usada junto com os jogos** (dividem GPU e memória).
- Se a saída sair corrompida, garanta que o cache KV está em **f16** (`q4_0` corrompe a saída no RADV). Veja [IA no aparelho](/pt/docs/ai-locale).

## Fontes

- [bc250.info](https://bc250.info) · [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- [Arch Wiki — Gamepad](https://wiki.archlinux.org/title/Gamepad)
- [PipeWire — solução de problemas](https://docs.pipewire.org/)

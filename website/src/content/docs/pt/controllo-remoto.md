---
title: Controle remoto — Remote Manager
description: O painel web do SkillFishOS para controlar a BC-250 pelo navegador ou pelo celular — telemetria, KVM, terminal, Tuner, loja de aplicativos e IA.
group: Uso
order: 4
---

O **SkillFishOS Remote Manager** é um painel web modular que permite controlar a BC-250 **de outro PC ou do celular**, na mesma rede local ou — pelo ZeroTier — de qualquer lugar do mundo. Você entra com as credenciais do sistema, tudo por HTTPS.

## Instalação

```bash
sudo apt update
sudo apt install skillfish-dashboard
```

O pacote instala o serviço, o aplicativo próprio **Remote Manager** (para ligar e desligar o painel e escolher os módulos) e todas as páginas web. As dependências opcionais (KVM, terminal, Wake-on-LAN) são *Recommends* e entram sozinhas quando estão disponíveis.

## Ativação

Abra o **SkillFishOS Remote Manager** pelo menu de aplicativos:

- **Interruptor principal** — inicia o serviço (de forma permanente, pelo systemd).
- **Caixas dos módulos** — escolha o que expor (telemetria, Tuner, Hub, KVM, terminal, IA…).
- Mostra o **endereço, um QR code e as credenciais** para conectar.

Ou por um terminal: `sudo systemctl enable --now skillfish-dashboard`.

> Por segurança, o painel **não sobe sozinho** depois da instalação — você o ativa quando quiser.

## Acesso

Abra **`https://<ip-da-placa>:8443`** no navegador (ou `https://BC-250.local:8443`). Como o certificado é autoassinado, na primeira vez o navegador vai avisar — é o esperado, siga em frente.

Entre com o **seu usuário e senha do sistema** (os mesmos do acesso ao SkillFishOS): a verificação usa PAM.

## Os módulos

O painel se monta com os módulos que você ativou:

- **Telemetria** — gráficos ao vivo de temperaturas, frequências, watts e carga de CPU e GPU, com os valores no eixo vertical e um painel de barras mostrando a **frequência por núcleo e thread** (as 16 threads, com as desligadas bem marcadas).
- **Estado do sistema** — nome da máquina, IP, kernel, tempo ligada, memória, disco, CU ativas, travamentos detectados.
- **Controles (Tuner)** — perfis rápidos mais o **Tuner completo** na web: CPU (frequência, undervolt, temperatura), GPU (frequência, tensão, governador), **controle das unidades de computação em tempo real** (grade WGP, sem reiniciar), ventoinha, VRAM, *Teste* e os assistentes **“Encontre meu máximo”**.
- **Programas e pacotes (Hub)** — uma **loja de aplicativos** de verdade (AppStream + Flatpak + Snap): navegar por categorias, buscar, instalar e remover, atualizar. Os **aplicativos do SkillFishOS** ficam em destaque no topo.
- **Área de trabalho (KVM)** — ver e controlar a área de trabalho real da placa pelo navegador (noVNC), sem hardware extra.
- **Terminal** — um console web (ttyd) dentro do painel.
- **IA no aparelho** — estado do motor Unsloth, aceleração Vulkan e uma conversa com o modelo local, rodando na GPU da BC-250.
- **AI-Ops** — o modelo local lê os registros e a telemetria e diagnostica os problemas para você.
- **Registros**, **regras automáticas** (baixar a frequência acima de um limite de °C), **Wake-on-LAN** e ligar e desligar programados.
- **ZeroTier** — para chegar ao painel **de qualquer lugar** (veja abaixo).

Os botões **Reiniciar** e **Desligar** ficam sempre na barra de cima. Os cartões podem ser **fechados, reabertos e arrastados**, e o **arranjo pode ser salvo**.

## Acesso à distância (ZeroTier)

O painel foi pensado para a **rede local**. Para usá-lo de fora, ative o módulo **ZeroTier**: entre numa das suas redes, autorize a placa em [my.zerotier.com](https://my.zerotier.com) e então abra o painel no endereço ZeroTier da placa — sem abrir nenhuma porta no roteador.

## Segurança

- **HTTPS** com certificado autoassinado (TLS 1.2 ou superior), gerado no primeiro início.
- **Entrada por PAM** com as suas credenciais, **sessões assinadas** (HMAC) e **limite de tentativas**.
- Feito para a **rede local**; para acesso remoto use o ZeroTier em vez de expor o painel direto na internet.

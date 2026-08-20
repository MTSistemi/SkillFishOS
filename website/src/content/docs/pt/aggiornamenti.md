---
title: Atualizações e repositório
description: Como o SkillFishOS se atualiza com segurança, sem ser quebrado pelo Debian sid.
group: Uso
order: 4
---

O SkillFishOS é baseado no **Debian sid** (*unstable*), o ramo de desenvolvimento do Debian: sempre atualizado, mas por natureza sujeito a regressões de vez em quando. Num hardware “exótico” como a BC-250, uma atualização ruim (do Mesa, do firmware ou do kernel) pode quebrar o sistema. O SkillFishOS enfrenta isso com duas ferramentas.

## 1. Componentes próprios, de um repositório dedicado

As partes mais delicadas são compiladas e distribuídas por **nós**, a partir de um **repositório APT próprio e assinado**:

- o **[kernel](/pt/docs/kernel)** otimizado (imagem e cabeçalhos);
- o **governador SMU** e as ferramentas de overclock;
- os **aplicativos próprios** [Tuner e AI](/pt/docs/app-native);
- o **visual steampunk** e a **identidade**;
- a configuração do sistema.

Publicar um componente pelo nosso próprio repositório significa que podemos **testá-lo antes** no hardware real e atualizá-lo **só quando traz benefício**, não toda vez que algo muda lá em cima.

## 2. “Fixar” os pacotes frágeis

Para os pacotes que vêm do Debian mas são sensíveis neste hardware, o SkillFishOS usa o **fixação do APT** (*pinning*): mantém-nos numa versão **verificada** até testarmos uma mais nova. Os principais candidatos à fixação são:

- **Mesa e os drivers Vulkan (RADV)** — uma atualização pode piorar o `gfx1013`;
- **firmware da AMD / `linux-firmware`** — microcódigo da GPU;
- **o kernel padrão do Debian** — para bloquear as versões sabidamente problemáticas (veja [kernel](/pt/docs/kernel));
- **KDE Plasma** — para não cair numa entrega instável.

Assim, as atualizações “normais” (a maior parte do sistema) continuam chegando com regularidade, enquanto o punhado de pacotes capaz de quebrar tudo fica parado em versões que sabemos que funcionam.

## Como atualizar

Como em qualquer sistema Debian, pelo terminal:

```bash
sudo apt update && sudo apt full-upgrade
```

…ou pelo aplicativo gráfico **Discover**, ou pelo **SkillFishOS Hub** — a nossa central de programas no estilo Discover, que instala, remove e atualiza num só lugar por **APT, Flatpak e Snap**, com navegação por categorias, páginas de aplicativo com carrossel de capturas e um “Atualizar tudo” de um clique. Graças aos ganchos do [Snapper](/pt/docs/storage-snapshot), um snapshot Btrfs é criado **antes e depois** de cada atualização: se algo der errado, a volta atrás pelo menu do GRUB restaura o estado anterior.

> Resumindo: **nós** damos um kernel, aplicativos e visual testados; o **Debian** dá o resto do software atualizado; a **fixação** evita surpresas; o **Btrfs** é a rede de segurança. Três camadas de proteção, para que atualizar não dê medo.

## O repositório oficial

O repositório APT do SkillFishOS está **no ar**, assinado com GPG e hospedado no **GitHub Pages** (suíte `aetherium`):

```bash
# 1. importar a chave de assinatura
sudo curl -fsSL https://mtsistemi.github.io/SkillFishOS/skillfishos-archive-keyring.gpg \
  -o /usr/share/keyrings/skillfishos-archive-keyring.gpg
# 2. acrescentar o repositório
echo "deb [signed-by=/usr/share/keyrings/skillfishos-archive-keyring.gpg] \
https://mtsistemi.github.io/SkillFishOS aetherium main" \
  | sudo tee /etc/apt/sources.list.d/skillfishos.list
# 3. instalar ou atualizar o kernel pelo apt
sudo apt update && sudo apt install skillfishos-kernel
```

As compilações recentes do SkillFishOS já vêm com ele **pré-configurado**; caso contrário, os comandos acima resolvem. O [kernel](/pt/docs/kernel) (imagem de 152 MB) é publicado como *release asset* do GitHub: o pequeno pacote `skillfishos-kernel` baixa e instala sozinho, então a atualização continua passando pelo `apt`. O repositório é gerenciado com o **[reprepro](https://salsa.debian.org/debian/reprepro)** e o cliente confere a assinatura pelo *keyring* dedicado.

## Fontes

- [Debian unstable (sid)](https://wiki.debian.org/DebianUnstable)
- [Fixação do APT — manual do Debian](https://wiki.debian.org/AptConfiguration)
- [reprepro](https://salsa.debian.org/debian/reprepro) — gestão do repositório APT
- [Snapper](http://snapper.io/) — snapshots antes e depois do APT

// Brazilian Portuguese UI strings. Any key missing here falls back to English
// (see t() in i18n.ts), so this file can grow without ever leaving a blank.
// Inline HTML and &nbsp; entities are part of the copy — keep them.
//
// Brazil is 9.5% of the last thirty days of downloads on SourceForge with the
// scraper day removed, steady across periods, and Portugal adds to it. This is
// pt-BR: "tela" not "ecrã", "arquivo" not "ficheiro", "mouse" not "rato".
//
// ⚠️ NOT reviewed by a native speaker. Written by the SkillFishOS team, like the
// Russian, Spanish and Ukrainian ones; the Polish is Cyryl Sochacki's.
// Corrections are welcome and cost one file: this one.
export const pt: Record<string, string> = {
  title: "SkillFishOS — Linux para jogar na AMD BC-250",
  "meta.desc":
    "SkillFishOS: o sistema operacional steampunk para jogar na placa AMD BC-250. Já ajustado e pronto, sem precisar mexer em nada. Emulação, Steam, IA no próprio aparelho. Baseado em Debian + KDE Plasma.",

  "nav.feat": "Recursos",
  "nav.shots": "Capturas",
  "nav.hw": "Hardware",
  "nav.download": "Baixar",
  "nav.docs": "Documentação",
  "nav.gallery": "Galeria",
  "nav.contact": "Contato",
  "nav.donate": "Apoie",
  "nav.news": "Novidades",
  "nav.road": "Planos",

  "hero.soon": "Versão 26.06 “Aetherium”",
  "hero.tag": "O sistema operacional para jogar, forjado para a <b>AMD BC-250</b>.",
  "hero.sub":
    "Linux steampunk, pronto para jogar desde o primeiro boot. Tudo já ajustado, sem precisar mexer em nada. Emulação, Steam e IA no próprio aparelho. Baseado em Debian e KDE&nbsp;Plasma.",
  "hero.btn1": "Ver funcionando",
  "hero.btn2": "O que tem dentro",
  "hero.pill": "APU AMD · Zen&nbsp;2 + RDNA&nbsp;2 · 16&nbsp;GB GDDR6",

  "intro.eye": "O que é",
  "intro.h2": "Um PC-console,<br>pronto para usar.",
  "intro.p1":
    "O SkillFishOS transforma a placa <strong>AMD BC-250</strong> — uma APU semipersonalizada da <strong>família AMD Zen&nbsp;2 + RDNA&nbsp;2</strong> (CPU “Oberon”, gráficos “Cyan&nbsp;Skillfish”, 16&nbsp;GB GDDR6) — em um sistema completo para jogar e trabalhar.",
  "intro.p2":
    "Governadores, patches de kernel, overclock e perfis térmicos vêm <strong>já ajustados</strong>: um sistema que roda no máximo <strong>sem precisar mexer em nada</strong>. Um visual <strong>steampunk</strong> coerente do boot até a área de trabalho, pensado também para que <strong>as crianças aprendam Linux</strong> enquanto jogam.",

  "feat.eye": "Recursos",
  "feat.h2": "Tudo pronto, é só ligar.",
  "feat.sub": "Não há nada para configurar na mão: o sistema já está ajustado para a BC-250.",

  "f1.t": "Pronto para jogar",
  "f1.d":
    "Steam, EmuDeck, ES-DE, Heroic e Proton prontos. O EmuDeck instala e configura os emuladores em alguns cliques — os jogos e as ROMs você traz.",
  "f2.t": "Kernel sob medida",
  "f2.d":
    "Um kernel tkg ajustado para a BC-250: <b>40 unidades de computação</b> destravadas, overclock de CPU e GPU e um governador SMU próprio para extrair cada TFLOPS.",
  "f3.t": "Pronto, sem mexer em nada",
  "f3.d":
    "Governadores, patches, overclock e proteção térmica <b>já configurados e testados</b>. Você liga e roda a toda velocidade: sem terminal e sem ajuste manual.",
  "f4.t": "Visual steampunk",
  "f4.d":
    "Uma área de trabalho KDE&nbsp;Plasma escura com estilo steampunk: ícones, cursores, papel de parede e um HUD do sistema com ar mecânico-vitoriano.",
  "f5.t": "Snapshots Btrfs",
  "f5.d":
    "Experimente sem medo: cada mudança fica protegida por snapshots automáticos. Quebrou alguma coisa? <b>Você volta com um clique</b> pelo menu de boot.",
  "f6.t": "IA no próprio aparelho",
  "f6.d":
    "<b>Unsloth Studio</b> acelerado por <b>Vulkan</b> na GPU integrada: <b>5,1×</b> mais rápido que na CPU, medido. Modelos de conversa e de programação rodando em casa, sem nuvem.",
  "f7.t": "Controle remoto",
  "f7.d":
    "<b>Remote Manager</b>: um painel web para controlar a placa pelo navegador ou pelo celular — telemetria, KVM, terminal, Tuner, loja de aplicativos e IA. Login com as contas do sistema por HTTPS, e de qualquer lugar com o ZeroTier.",

  "show.eye": "Capturas",
  "show.h2": "Bonito de ver, fácil de usar.",
  "s1.t": "A área de trabalho steampunk",
  "s1.d":
    "KDE Plasma com estilo steampunk: papel de parede temático, detalhes dourados e um HUD ao vivo com CPU, GPU, temperaturas, ventoinha e bateria do controle Bluetooth, sempre à vista.",
  "s2.t": "Emulação fácil com o EmuDeck",
  "s2.d":
    "O EmuDeck instala e configura os emuladores (RetroArch, Dolphin, PCSX2, PPSSPP, RPCS3 e outros) e a interface ES-DE em alguns cliques. O sistema dá as ferramentas: os jogos e as ROMs são seus.",
  "s4.t": "IA no aparelho, a um clique",
  "s4.d":
    "Um painel próprio liga e desliga o motor de IA local (Qwen na GPU via Vulkan). Conversa pela web, terminal para programar e gerenciamento: a IA roda em casa e libera a GPU na hora de jogar.",
  "s5.t": "Ajuste em um clique",
  "s5.d":
    "O Tuner ajusta frequências, undervolt, ventoinha e unidades de computação com quatro perfis prontos (Stock, Performance, Turbo, Crazy) e uma proteção térmica que cuida do hardware. Toda a potência, com segurança e sem linha de comando.",

  "hw.eye": "Hardware",
  "hw.h2": "Nascido para a AMD BC-250.",
  "hw.sub": "Toda a potência da família AMD Zen 2 + RDNA 2, liberada no Linux.",
  "hw.c1": "CPU “Oberon” · até 4,0 GHz",
  "hw.c2": "GPU “Cyan Skillfish” · 40 CU",
  "hw.c3": "FP32 · aceleração Vulkan",
  "hw.c4": "GDDR6 compartilhada",

  "cta.h2": "Ligue. <span class=\"gold-text\">Jogue.</span> Aprenda.",
  "cta.p":
    "Um sistema operacional de código aberto que transforma uma placa nua em um verdadeiro PC-console. Disponível em duas edições: AMD BC-250 e Generic (qualquer PC ou máquina virtual x86-64).",
  "cta.btn": "Baixar o SkillFishOS",
  "foot.based": "Código aberto · Baseado em Debian · KDE Plasma · © 2026 SkillFishOS",

  "dl.title": "Baixar — SkillFishOS",
  "dl.eye": "Baixar",
  "dl.h2": "Baixar o SkillFish<span class=\"gold-text\">OS</span>",
  "dl.sub":
    "As ISOs instaláveis, com a identidade do projeto e prontas para usar — para a AMD BC-250 e para qualquer PC x86-64.",
  "dl.badge": "26.06.4 “Aetherium”",
  "dl.notice":
    "A versão <strong>26.06.4 “Aetherium”</strong> do SkillFishOS vem em <strong>duas edições</strong>: <strong>BC-250</strong> (a placa da AMD) e <strong>Generic</strong> (qualquer PC ou máquina virtual x86-64). Completa e pronta para usar. Projeto de <strong>código aberto</strong>.",
  "dl.btnsoon": "ISO chega em breve",
  "dl.btn": "Baixar a ISO",
  "dl.ed.bc250": "BC-250",
  "dl.ed.generic": "Generic (PC/VM)",
  "dl.ed.slim": "Slim (BC-250)",
  "dl.ed.all": "Todos os arquivos no SourceForge →",
  "dl.size": "amd64 · ~{size} GB · btrfs + KDE Plasma · 2 edições no SourceForge",
  "dl.ver":
    "Versão <strong>26.06.4 “Aetherium”</strong> · <strong>2 edições</strong> (BC-250 · Generic) · inicia em inglês, o idioma é escolhido na instalação",
  "dl.fast.h": "O caminho mais rápido, a partir da Europa",
  "dl.fast.sub":
    "O Internet Archive guarda nossas ISOs e as serve dos próprios servidores. Medido de uma linha italiana: <strong>cerca de 5 MB/s</strong> contra 0,4 do SourceForge, que serve tudo de San Diego. Mesmo arquivo, mesma soma de verificação.",
  "dl.fast.bc250": "BC-250",
  "dl.fast.generic": "Generic (PC/VM)",
  "dl.sf.h": "Ou pelo SourceForge",
  "dl.sf.sub":
    "O espelho de sempre do projeto: mais lento a partir da Europa, mas é de lá que vêm nossos contadores de download.",
  "dl.tor.h": "Ou por torrent",
  "dl.tor.sub":
    "Mais rápido quando várias pessoas baixam ao mesmo tempo, e continua de onde parou. Funciona mesmo sem ninguém conectado: o torrent puxa direto dos nossos espelhos.",
  "dl.tor.bc250": "⇅ BC-250 · torrent",
  "dl.tor.generic": "⇅ Generic · torrent",
  "dl.tor.magnet": "magnet",
  "dl.bugs.h": "Encontrou um problema?",
  "dl.bugs.d":
    "O SkillFishOS melhora sem parar. Para relatar falhas ou problemas, abra uma <em>issue</em> no GitHub. (Em breve teremos também um e-mail.)",
  "dl.bugs.btn": "Relatar no GitHub",
  "dl.req.h": "Requisitos",
  "dl.req.d":
    "Uma placa <strong>AMD BC-250</strong> (APU Zen&nbsp;2 + RDNA&nbsp;2, 16&nbsp;GB GDDR6), um SSD ou NVMe, um monitor com <strong>DisplayPort</strong> e um pendrive de 8&nbsp;GB ou mais para o instalador.",
  "dl.inc.h": "O que vem junto",
  "dl.inc.d":
    "Um kernel otimizado (40&nbsp;CU, governador, OC), o visual steampunk completo, Steam + EmuDeck + ES-DE, IA local, snapshots Btrfs e as ferramentas Tuner e AI prontas para usar.",
  "dl.steps.h": "Instalação",
  "dl.step1": "Grave a ISO em um pendrive (Etcher, Ventoy ou <code>dd</code>).",
  "dl.step2": "Dê boot na BC-250 pelo pendrive e siga o instalador gráfico (Calamares).",
  "dl.step3": "No primeiro boot está tudo configurado: é só ligar e jogar.",
  "dl.repo.h": "Atualizações",
  "dl.repo.d":
    "O SkillFishOS se atualiza pelo <strong>repositório oficial</strong>: kernel, aplicativos e temas vêm de nós e são testados, então as atualizações do Debian sid não conseguem quebrar o sistema.",

  "news.title": "Novidades",
  "news.eye": "Sempre em dia",
  "news.h1": "O que mudou,<br>e quando",
  "news.sub":
    "Um projeto pequeno também é julgado pela frequência com que dá notícia. Aqui estão as novidades por data e o caminho à frente, com o estado de cada item — inclusive os que ainda não estão prontos.",
  "news.h.news": "Novidades",
  "news.h.road": "Planos",
  "news.road.sub":
    "No que estamos trabalhando, o que vem depois e o que já chegou. Não prometemos datas enquanto não as tivermos de verdade.",
  "news.foot":
    "Tem uma ideia ou está faltando alguma coisa? Pedidos são bem-vindos: escreva pela página de <a href=\"/pt/contact\">contato</a> ou abra uma discussão no GitHub. Construir o que alguém realmente precisa é melhor do que acertar por sorte.",
  "news.diroad": "Quer saber o que vem depois? Está nos <a href=\"/pt/roadmap\">planos</a>.",

  "road.title": "Planos",
  "road.eye": "Para onde estamos indo",
  "road.h1": "O que está por vir,<br>e o que já chegou",
  "road.sub":
    "Não prometemos datas enquanto não as tivermos de verdade. Os itens concluídos ficam no fim, porque respondem à pergunta que mais nos fazem: se o projeto está vivo.",
  "road.dinews": "Procurando o que mudou? Isso está nas <a href=\"/pt/news\">novidades</a>.",

  "gal.title": "Galeria — SkillFishOS",
  "gal.eye": "Galeria",
  "gal.h2": "Bonito de ver, fácil de usar.",
  "gal.sub": "O SkillFishOS em ação: área de trabalho, jogos, emulação e ferramentas.",
  "gal.desktop.t": "A área de trabalho steampunk",
  "gal.desktop.d": "KDE Plasma com o visual do sistema e um HUD ao vivo no canto superior direito.",
  "gal.about.t": "Informações do sistema",
  "gal.about.d": "Identidade completa: nome, logotipo e hardware reconhecidos como SkillFishOS.",
  "gal.emudeck.t": "EmuDeck",
  "gal.emudeck.d": "Instalação e configuração dos emuladores em alguns cliques.",
  "gal.esde1.t": "ES-DE — interface",
  "gal.esde1.d": "A interface ES-DE para navegar e abrir suas bibliotecas.",
  "gal.ai.t": "Painel de IA",
  "gal.ai.d": "Liga e desliga a IA local (Vulkan) com um clique.",
  "gal.tuner.t": "Tuner — unidades de computação ao vivo",
  "gal.tuner.d":
    "Grade de CU (verde = ativa, vermelho = desligada), perfis 24/32/40 e teste, sem reiniciar.",
  "gal.tunerctl.t": "Tuner — perfis, governador e assistentes",
  "gal.tunerctl.d":
    "Perfis Stock/Performance/Turbo/Crazy, o painel “Meu silício”, o modo de governador Balanced/Performance e os assistentes “Encontre meu máximo” para CPU e GPU.",
  "gal.monitor.t": "Telemetria ao vivo durante os testes",
  "gal.monitor.d": "Gráficos de temperatura, frequência, tensão e ventoinha em tempo real.",
  "gal.cutest.t": "Teste de CU — loteria do silício",
  "gal.cutest.d":
    "Verifica se todas as 40 CU aguentam a carga sem defeito (útil em chips de segunda mão).",
  "gal.wukong.t": "Black Myth: Wukong — 112 FPS",
  "gal.wukong.d": "Média em 1080p na BC-250 (máximo 128, 1% low 101).",
  "gal.super.t": "Unigine Superposition — 12.938",
  "gal.super.d": "1080p High: desempenho de uma Radeon RX 6600 em uma placa de uns 50 euros.",
  "gal.heaven.t": "Unigine Heaven — 113,7 FPS",
  "gal.heaven.d": "2865 pontos em 1080p Ultra, 8× AA, tesselagem Extreme.",
  "gal.boot.t": "Boot steampunk",
  "gal.boot.d": "Uma abertura em latão coerente do GRUB até a área de trabalho.",
  "gal.b1.t": "Mesmo hardware, +34% — contra o Bazzite",
  "gal.b1.d":
    "Superposition 1080p Extreme: a mesma BC-250 faz 4102 nas frequências de fábrica em outra distribuição; com o SkillFishOS chega a 5513. Tabela oficial da Unigine.",
  "gal.b2.t": "No nível de uma Radeon RX 6600",
  "gal.b2.d":
    "Superposition 1080p High: a BC-250 com SkillFishOS (12.938) empata com uma RX 6600/6600 XT de mais de 200 euros (12.454). Tabela oficial da Unigine.",

  "hwp.title": "Hardware AMD BC-250 — SkillFishOS",
  "hwp.eye": "Hardware",
  "hwp.h2": "Nascido para a <span class=\"gold-text\">AMD BC-250</span>.",
  "hwp.sub": "Uma APU semipersonalizada AMD Zen 2 + RDNA 2 com 16 GB de GDDR6, liberada no Linux.",
  "hwp.specs.h": "Especificações",
  "hwp.cpu.t": "CPU — 8× Zen 2",
  "hwp.cpu.d":
    "“Oberon”, <strong>8 núcleos / 16 threads</strong> (a placa mostra 6, o SkillFishOS destrava os outros dois pelo SMU: <strong>+20%</strong> medido), até <strong>4,0 GHz em todos os núcleos</strong> com overclock.",
  "hwp.gpu.t": "GPU — RDNA 2",
  "hwp.gpu.d": "“Cyan Skillfish” (gfx1013), até 40 unidades de computação destraváveis.",
  "hwp.mem.t": "Memória — 16 GB GDDR6",
  "hwp.mem.d":
    "Compartilhada (UMA) entre CPU e GPU; no Linux o GTT amplia a memória de vídeo.",
  "hwp.perf.t": "Computação — ~11 TFLOPS",
  "hwp.perf.d": "FP32 com 40 CU / 2000 MHz (vkpeak), com aceleração Vulkan.",
  "hwp.quirks.h": "Defeitos do hardware (e como resolvemos)",
  "hwp.q1.t": "HPD do DisplayPort quebrado",
  "hwp.q1.d":
    "A detecção do monitor não funciona → serviço dedicado + parâmetro de kernel <code>video=DP-1:e</code>.",
  "hwp.q2.t": "Suspensão quebrada",
  "hwp.q2.d": "A placa não acorda → todos os estados de sono desativados em definitivo.",
  "hwp.q3.t": "IOMMU instável",
  "hwp.q3.d": "Nunca deve ser ligado → o sistema sempre dá boot sem IOMMU.",
  "hwp.q4.t": "Refrigeração no limite",
  "hwp.q4.d":
    "Só sensor de borda, sem sensor de VRAM → uma proteção térmica de 85 °C sempre ativa.",
  "hwp.cta": "Mais detalhes na documentação →",

  "bm.h": "Desempenho medido",
  "bm.sub":
    "Medidas de vkpeak FP32-scalar (GFLOPS) na <strong>mesma</strong> BC-250, antes e depois do SkillFishOS.",
  "bm.bar1": "Base — XanMod, 24 CU",
  "bm.bar2": "tkg + governador, 24 CU",
  "bm.bar3": "SkillFishOS — tkg + governador + 40 CU",
  "bm.unit": "GFLOPS",
  "bm.note":
    "Medidas com <strong>vkpeak</strong> (computação Vulkan) na mesma placa, a frio e em repouso. Com as 40 CU ativas a GPU entrega <strong>1,84×</strong> mais que o sistema de partida. Em repouso o governador cai para 350 MHz; borda ~54 °C depois da carga de computação.",
  "bm.s1.l": "FP32 em relação à base",
  "bm.s2.l": "GFLOPS FP32 (≈11,3 TFLOPS)",
  "bm.s3.l": "GFLOPS FP16 (vec4)",
  "bm.s4.l": "GIOPS int8 (produto escalar)",
  "bm.src": "Fonte: medições do projeto em hardware real (vkpeak). Detalhes em",
  "bm.gpulink": "GPU, governador e overclock",

  "wk.h": "Carga real — Black Myth: Wukong (1080p)",
  "wk.note":
    "Cerca de 4 minutos de telemetria dentro do jogo: <strong>CPU e GPU seguram todo o overclock</strong> dentro do limite térmico de 85 °C — governador, OC e proteção térmica dão conta de um AAA pesado. (Wukong depende da <em>CPU e das chamadas de desenho</em>: aqui o que importa é a estabilidade sob carga, não a resolução.)",
  "wk.l.gpu": "GPU (ponto seguro)",
  "wk.l.gpuc": "Borda da GPU (máx. 81)",
  "wk.l.pwr": "Consumo (pico 182 W)",
  "wk.l.cpu": "CPU (overclock)",
  "wk.l.vram": "VRAM em uso",
  "wk.l.fan": "Ventoinha",

  "bs.h": "Capturas reais — feitas no nosso próprio hardware",
  "bs.sub":
    "Sem renders e sem maquetes: capturas de tela reais tiradas durante os testes, na <strong>nossa própria</strong> BC-250 com SkillFishOS. Toque em uma imagem para ampliar.",
  "bs.wk.c":
    "Black Myth: Wukong — <strong>112 FPS</strong> em média a 1080p (máximo 128, 1% low 101). APU AMD BC-250, GPU RADV gfx1013.",
  "bs.hv.c":
    "Unigine Heaven 4.0 — <strong>113,7 FPS</strong>, pontuação <strong>2865</strong> (1080p Ultra, 8× AA, tesselagem Extreme). Kernel 7.0.10-skillfishos (hoje entregamos o 7.2.0).",
  "bs.sc.c":
    "Unigine Heaven — a cena renderizada em tempo real na BC-250 durante o teste.",

  "gb.h": "Testes com jogos — resultados reais",
  "gb.sub":
    "Medido na BC-250 com SkillFishOS, a 1080p. Uma placa de <strong>uns 50 euros</strong> jogando no nível de uma <strong>Radeon RX&nbsp;6600</strong>.",
  "gb.wk.v": "112 FPS",
  "gb.wk.l": "Black Myth: Wukong · média a 1080p",
  "gb.hv.v": "2865",
  "gb.hv.l": "Unigine Heaven · 1080p Ultra/Extreme · 8× AA · 113 FPS",
  "gb.sp.v": "12.938",
  "gb.sp.l": "Unigine Superposition · 1080p High · (5513 em Extreme)",

  "cmp.os.h": "Mesmo hardware, +34% só trocando de sistema",
  "cmp.os.sub":
    "Superposition 1080p Extreme, na <strong>mesma BC-250</strong>: SkillFishOS contra outra distribuição nas frequências de fábrica.",
  "cmp.os.b1": "SkillFishOS — GPU 2230 · CPU 3900",
  "cmp.os.b2": "Outra distribuição (Bazzite) — GPU 2100 · CPU 3436",
  "cmp.os.note":
    "40 CU destravadas, um governador que leva a GPU a 2230 MHz e overclock com undervolt na CPU: <strong>+34% de desempenho real</strong> do mesmíssimo chip. Fonte: a tabela oficial da Unigine.",
  "cmp.gpu.h": "Cara a cara com as Radeon de mesa",
  "cmp.gpu.sub":
    "Superposition 1080p High: a BC-250 com SkillFishOS empata com uma <strong>RX&nbsp;6600/6600&nbsp;XT</strong> de mais de 200 euros.",
  "cmp.gpu.b1": "SkillFishOS — BC-250 (~50 €)",
  "cmp.gpu.b2": "Radeon RX 6600 / 6600 XT",
  "cmp.gpu.b3": "Radeon RX 6700 / 6750 XT",
  "cmp.gpu.note":
    "Computação bruta de uma RX&nbsp;6700 (~11,3 TFLOPS) e desempenho em jogos de uma RX&nbsp;6600/6600&nbsp;XT — em uma placa de uns 50 euros. Um <strong>chip RDNA&nbsp;2 semipersonalizado, de classe console</strong> (“Oberon”, gfx1013), liberado no Linux.",
  "cmp.axis": "Pontuação do Superposition",

  "oc.h": "Overclock e undervolt — caracterizados na mão",
  "oc.sub":
    "Curvas de tensão e frequência medidas pelo SMU na APU “Oberon”, com validação térmica real. Tudo controlável pelo <strong>Tuner</strong> com perfis prontos.",
  "oc.cpu.v": "4,0 GHz",
  "oc.cpu.l": "CPU de 8 núcleos, todos juntos · remedido passo a passo · 0 erros MCE",
  "oc.uv.v": "−194 mV",
  "oc.uv.l": "Undervolt da CPU a 3,7 GHz (1206→1012 mV) sem perda",
  "oc.gpu.v": "2230 MHz",
  "oc.gpu.l": "GPU · 40 CU · governador SMU próprio",
  "oc.cap.v": "85 °C",
  "oc.cap.l": "Limite térmico de CPU e GPU: baixa a frequência, nunca quebra",
  "oc.note":
    "Para cada frequência procuramos a <strong>menor tensão estável</strong>, lendo o VID real do SMU e validando com 120 s de estresse. Os perfis <strong>Stock · Performance · Turbo · Crazy</strong> aplicam esses ajustes com um clique; uma proteção térmica mantém tudo abaixo de 85 °C. Todos os detalhes na documentação.",

  "don.title": "Apoie — Pague um café para nós",
  "don.eye": "Apoie o projeto",
  "don.h2": "Ajude a forjar o <span class=\"gold-text\">futuro</span> do SkillFishOS",
  "don.sub":
    "O SkillFishOS é e vai continuar <strong>gratuito e de código aberto</strong>. Mas atrás dele há uma <strong>equipe pequena</strong> e uma única placa: uma contribuição pequena mantém o desenvolvimento rápido — e vivo.",
  "don.why.h": "Uma equipe pequena. Uma placa.",
  "don.why.p1":
    "Atrás do SkillFishOS há uma <strong>equipe pequena</strong> que desenvolve, testa e mantém tudo — kernel, aplicativos, tema, repositório e site — no tempo livre e <strong>inteiramente do próprio bolso</strong>. O sistema é e vai continuar gratuito e de código aberto: sem paywall e sem anúncios.",
  "don.why.p2":
    "Hoje temos <strong>uma única BC-250</strong>. Cada patch de kernel, governador ou overclock precisa ser testado na única placa que temos: se ela travar no meio do teste, o desenvolvimento para. Sem testes em paralelo, sem comparar chips diferentes (a “loteria do silício”), sem espaço para experimentar com tranquilidade. <strong>Sua ajuda muda tudo isso.</strong>",
  "don.use.h": "Para onde vai o dinheiro",
  "don.use.sub": "Transparência total: cada euro vira desenvolvimento mais rápido e melhor.",
  "don.u1.t": "Mais placas BC-250",
  "don.u1.d":
    "Mais placas = desenvolvimento mais rápido e seguro: testes em paralelo, comparação do silício e uma reserva caso uma morra.",
  "don.u2.t": "Gabinetes e dissipadores",
  "don.u2.d":
    "Refrigeração melhor para subir o overclock e a estabilidade — e para validar soluções térmicas que valha a pena recomendar a você.",
  "don.u3.t": "Infraestrutura",
  "don.u3.d":
    "Domínio, hospedagem, espelhos e integração contínua: os custos que mantêm no ar o site, o repositório APT e os downloads — hoje todos por nossa conta.",
  "don.u4.t": "Tempo de desenvolvimento",
  "don.u4.d":
    "Cada contribuição permite dedicar mais horas a novos recursos, correções e suporte, em vez de a outra coisa.",
  "don.give.h": "Pague um café para nós ",
  "don.give.p":
    "Escolha um valor: o PayPal abre com a quantia já preenchida. Mesmo <strong>1, 2 ou 5 €</strong> fazem uma diferença enorme.",
  "don.give.custom": "Qualquer valor",
  "don.give.or": "ou aponte o celular para o QR",
  "don.give.scan": "Aponte para doar",
  "don.give.note":
    "Doação única pelo <strong>PayPal</strong>: sem compromisso e sem assinatura. O SkillFishOS continua gratuito e de código aberto para sempre.",
  "don.thanks":
    "Obrigado, de verdade — cada contribuição acende mais uma peça deste console. ",

  "comm.h": "Não pode doar? Ajude do mesmo jeito — é de graça",
  "comm.sub": "Três gestos de um minuto que fazem o projeto crescer tanto quanto uma doação.",
  "comm.star.t": "Dê uma estrela no GitHub",
  "comm.star.d":
    "Mais estrelas = mais visibilidade = mais gente descobrindo o SkillFishOS e contribuindo. É o jeito mais rápido de ajudar.",
  "comm.star.btn": "Dar estrela ao repositório →",
  "comm.review.t": "Deixe uma avaliação",
  "comm.review.d":
    "Testou o SkillFishOS? Conte como foi no SourceForge: avaliações convencem quem está chegando e nos dizem o que melhorar.",
  "comm.review.btn": "Avaliar no SourceForge →",
  "comm.idea.t": "Sugira uma ideia",
  "comm.idea.d":
    "Qual recurso facilitaria sua vida? Abra uma discussão: as ideias de quem usa guiam as próximas versões do SkillFishOS.",
  "comm.idea.btn": "Sugerir um recurso →",

  "ct.title": "Contato — SkillFishOS",
  "ct.eye": "Contato",
  "ct.h2": "Fale com a gente",
  "ct.sub":
    "Suporte, informações ou qualquer outra coisa: preencha o formulário e respondemos por e-mail.",
  "ct.f.name": "Nome",
  "ct.f.email": "Seu e-mail",
  "ct.f.type": "Tipo de pedido",
  "ct.f.msg": "Mensagem",
  "ct.f.captcha": "Quanto é",
  "ct.type.support": "Suporte",
  "ct.type.info": "Informações",
  "ct.type.other": "Outro",
  "ct.send": "Enviar pedido",
  "ct.privacy":
    "Não publicamos nosso e-mail para reduzir spam: o formulário encaminha com segurança. Os dados que você digita são usados só para responder.",
  "ct.ok": "Mensagem enviada! Respondemos em breve.",
  "ct.err.captcha": "A verificação antispam falhou. Tente de novo.",
  "ct.err.fields":
    "Confira os campos: são necessários nome, um e-mail válido e uma mensagem.",
  "ct.err.send": "Não foi possível enviar. Tente mais tarde ou fale com a gente no GitHub.",
  "ct.err.generic": "Algo deu errado. Tente de novo.",
};

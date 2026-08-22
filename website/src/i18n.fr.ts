// French UI strings. Any key missing here falls back to English (see t() in
// i18n.ts), so this file can grow without ever leaving a blank on the page.
// Inline HTML and &nbsp; entities are part of the copy — keep them.
//
// France is not in our download top ten, and that is exactly why this file
// exists: nobody arrives from a country whose language the site does not speak.
// The five languages added before this one were all chosen from the numbers;
// this is the first one added ahead of them.
//
// Addressed as "vous": the site speaks to someone it has not met. The apps and
// the installer use "vous" as well, so the tone does not change halfway through.
//
// ⚠️ NOT reviewed by a native speaker. Written by the SkillFishOS team, like the
// Russian, Spanish, Portuguese, German and Ukrainian ones; the Polish is Cyryl
// Sochacki's. Corrections are welcome and cost one file: this one.
export const fr: Record<string, string> = {
  title: "SkillFishOS — Le Linux de jeu pour l'AMD BC-250",
  "meta.desc":
    "SkillFishOS : le système d'exploitation steampunk pour jouer sur la carte AMD BC-250. Réglé d'avance et prêt à l'emploi, sans bricolage. Émulation, Steam, IA sur la machine. Bâti sur Debian + KDE Plasma.",

  "nav.feat": "Fonctions",
  "nav.shots": "Captures",
  "nav.hw": "Matériel",
  "nav.download": "Télécharger",
  "nav.docs": "Documentation",
  "nav.gallery": "Galerie",
  "nav.contact": "Contact",
  "nav.donate": "Nous soutenir",
  "nav.news": "Actualités",
  "nav.road": "Feuille de route",

  "hero.soon": "Version 26.06 « Aetherium »",
  "hero.tag": "Le système d'exploitation de jeu forgé pour l'<b>AMD BC-250</b>.",
  "hero.sub":
    "Un Linux steampunk, prêt à jouer dès le premier démarrage. Tout est réglé d'avance, rien à bricoler. Émulation, Steam et IA sur la machine. Bâti sur Debian et KDE&nbsp;Plasma.",
  "hero.btn1": "Le voir à l'œuvre",
  "hero.btn2": "Ce qu'il y a dedans",
  "hero.pill": "APU AMD · Zen&nbsp;2 + RDNA&nbsp;2 · 16&nbsp;Go GDDR6",

  "intro.eye": "Ce que c'est",
  "intro.h2": "Un PC-console,<br>prêt à l'emploi.",
  "intro.p1":
    "SkillFishOS transforme la carte <strong>AMD BC-250</strong> — un APU semi-personnalisé de la <strong>famille AMD Zen&nbsp;2 + RDNA&nbsp;2</strong> (CPU « Oberon », partie graphique « Cyan&nbsp;Skillfish », 16&nbsp;Go de GDDR6) — en un système complet pour jouer et travailler.",
  "intro.p2":
    "Gouverneurs, correctifs du noyau, overclock et profils thermiques arrivent <strong>déjà réglés</strong> : un système qui donne son meilleur <strong>sans rien bricoler</strong>. Une allure <strong>steampunk</strong> cohérente du démarrage au bureau, pensée aussi pour que <strong>les enfants apprennent Linux</strong> en jouant.",

  "feat.eye": "Fonctions",
  "feat.h2": "Tout est prêt, dès la sortie de la boîte.",
  "feat.sub":
    "Rien à régler à la main : le système est déjà taillé pour la BC-250.",
  "f1.t": "Prêt à jouer",
  "f1.d":
    "Steam, EmuDeck, ES-DE, Heroic et Proton prêts à partir. EmuDeck installe et configure les émulateurs en quelques clics — les jeux et les ROM, c'est vous qui les apportez.",
  "f2.t": "Noyau sur mesure",
  "f2.d":
    "Un noyau tkg taillé pour la BC-250 : <b>40 unités de calcul</b> déverrouillées, overclock du CPU et du GPU et un gouverneur SMU dédié pour aller chercher chaque TFLOP.",
  "f3.t": "Prêt, sans bricolage",
  "f3.d":
    "Gouverneurs, correctifs, overclock et garde thermique <b>déjà configurés et testés</b>. On allume et ça tourne à plein régime : pas de terminal, pas de réglage à la main.",
  "f4.t": "Thème steampunk",
  "f4.d":
    "Un bureau KDE&nbsp;Plasma sombre, en style steampunk : icônes, curseurs, fond d'écran et affichage système dans un esprit mécanique victorien.",
  "f5.t": "Instantanés Btrfs",
  "f5.d":
    "Bricolez sans crainte : chaque changement est protégé par des instantanés automatiques. Quelque chose a cassé ? <b>Retour en arrière en un clic</b> depuis le menu de démarrage.",
  "f6.t": "IA sur la machine",
  "f6.d":
    "<b>Unsloth Studio</b> accéléré en <b>Vulkan</b> sur le GPU intégré : <b>5,1×</b> plus rapide que le CPU, mesuré. Des modèles de discussion et de programmation à la maison, sans nuage.",
  "f7.t": "Commande à distance",
  "f7.d":
    "<b>Remote Manager</b> : un tableau de bord web pour piloter la carte depuis le navigateur ou le téléphone — télémétrie, KVM, terminal, Tuner, logithèque et IA. Connexion système en HTTPS, et de n'importe où avec ZeroTier.",

  "show.eye": "Captures",
  "show.h2": "Beau à regarder, simple à utiliser.",
  "s1.t": "Le bureau steampunk",
  "s1.d":
    "KDE Plasma en style steampunk : fond d'écran assorti, touches dorées et un affichage en direct du CPU, du GPU, des températures, du ventilateur et de la batterie des manettes Bluetooth, toujours sous les yeux.",
  "s2.t": "L'émulation facile avec EmuDeck",
  "s2.d":
    "EmuDeck installe et configure les émulateurs (RetroArch, Dolphin, PCSX2, PPSSPP, RPCS3 et d'autres) ainsi que l'interface ES-DE en quelques clics. Le système fournit les outils : les jeux et les ROM, c'est vous qui les fournissez.",
  "s4.t": "L'IA sur la machine, à un clic",
  "s4.d":
    "Un panneau dédié allume et éteint le moteur d'IA local (Qwen sur le GPU Vulkan). Discussion web, terminal de programmation et gestion : l'IA tourne à la maison, et libère le GPU quand vient l'heure de jouer.",
  "s5.t": "Le réglage en un clic",
  "s5.d":
    "Le Tuner règle les fréquences, l'undervolt, le ventilateur et les unités de calcul avec quatre profils prêts (Stock, Performance, Turbo, Crazy) et une garde thermique qui protège le matériel. Toute la puissance, sans risque et sans ligne de commande.",

  "hw.eye": "Matériel",
  "hw.h2": "Née pour l'AMD BC-250.",
  "hw.sub":
    "Toute la puissance de la famille AMD Zen 2 + RDNA 2, libérée sous Linux.",
  "hw.c1": "CPU « Oberon » · jusqu'à 4,0 GHz",
  "hw.c2": "GPU « Cyan Skillfish » · 40 CU",
  "hw.c3": "FP32 · accélération Vulkan",
  "hw.c4": "GDDR6 partagée",

  "cta.h2": "Allumez. <span class=\"gold-text\">Jouez.</span> Apprenez.",
  "cta.p":
    "Un système d'exploitation libre qui transforme une carte nue en véritable PC-console. Disponible en deux éditions : AMD BC-250 et Générique (n'importe quel PC ou machine virtuelle x86-64).",
  "cta.btn": "Télécharger SkillFishOS",
  "foot.based":
    "Libre · Fondé sur Debian · KDE Plasma · © 2026 SkillFishOS",

  "dl.title": "Télécharger — SkillFishOS",
  "dl.eye": "Téléchargement",
  "dl.h2": "Télécharger SkillFish<span class=\"gold-text\">OS</span>",
  "dl.sub":
    "Les images ISO installables, à nos couleurs et prêtes à l'emploi — pour l'AMD BC-250 et pour n'importe quel PC x86-64.",
  "dl.badge": "26.06.4 « Aetherium »",
  "dl.notice":
    "La version <strong>26.06.4 « Aetherium »</strong> de SkillFishOS existe en <strong>deux éditions</strong> : <strong>BC-250</strong> (la carte AMD) et <strong>Générique</strong> (n'importe quel PC ou machine virtuelle x86-64). Complètes et prêtes à l'emploi. Projet <strong>libre</strong>.",
  "dl.btnsoon": "ISO bientôt disponible",
  "dl.btn": "Télécharger l'ISO",
  "dl.ed.bc250": "BC-250",
  "dl.ed.generic": "Générique (PC/VM)",
  "dl.ed.slim": "Slim (BC-250)",
  "dl.ed.all": "Tous les fichiers sur SourceForge →",
  "dl.size":
    "amd64 · ~{size} Go · btrfs + KDE Plasma · 2 éditions sur SourceForge",
  "dl.ver":
    "Version <strong>26.06.4 « Aetherium »</strong> · <strong>2 éditions</strong> (BC-250 · Générique) · démarre en anglais, la langue se choisit à l'installation",
  "dl.fast.h": "Le plus rapide, depuis l'Europe",
  "dl.fast.sub":
    "Internet Archive conserve nos images et les sert depuis ses propres serveurs. Mesuré sur une ligne italienne : <strong>environ 5 Mo/s</strong> contre 0,4 depuis SourceForge, qui sert tout depuis San Diego. Même fichier, même empreinte.",
  "dl.fast.bc250": "BC-250",
  "dl.fast.generic": "Générique (PC/VM)",
  "dl.sf.h": "Ou depuis SourceForge",
  "dl.sf.sub":
    "Le miroir historique du projet : plus lent depuis l'Europe, mais c'est de là que viennent nos compteurs de téléchargement.",
  "dl.tor.h": "Ou par torrent",
  "dl.tor.sub":
    "Plus rapide quand plusieurs personnes téléchargent en même temps, et il reprend là où il s'est arrêté. Il marche même sans personne d'autre de connecté : le torrent sait puiser directement dans nos miroirs.",
  "dl.tor.bc250": "⇅ BC-250 · torrent",
  "dl.tor.generic": "⇅ Générique · torrent",
  "dl.tor.magnet": "magnet",
  "dl.bugs.h": "Un problème ?",
  "dl.bugs.d":
    "SkillFishOS s'améliore sans arrêt. Pour signaler un bogue ou un souci, ouvrez une <em>issue</em> sur GitHub. (Une adresse de courrier arrive bientôt.)",
  "dl.bugs.btn": "Signaler sur GitHub",
  "dl.req.h": "Ce qu'il faut",
  "dl.req.d":
    "Une carte <strong>AMD BC-250</strong> (APU Zen&nbsp;2 + RDNA&nbsp;2, 16&nbsp;Go de GDDR6), un SSD ou NVMe, un écran <strong>DisplayPort</strong> et une clé USB d'au moins 8&nbsp;Go pour l'installateur.",
  "dl.inc.h": "Ce qu'il y a dedans",
  "dl.inc.d":
    "Un noyau optimisé (40&nbsp;CU, gouverneur, overclock), le thème steampunk complet, Steam + EmuDeck + ES-DE, une IA locale, les instantanés Btrfs et les outils Tuner et IA prêts à partir.",
  "dl.steps.h": "Installation",
  "dl.step1":
    "Écrivez l'ISO sur une clé USB (Etcher, Ventoy ou <code>dd</code>).",
  "dl.step2":
    "Démarrez la BC-250 sur la clé et suivez l'installateur graphique (Calamares).",
  "dl.step3":
    "Au premier démarrage tout est déjà en place : on allume et on joue.",
  "dl.repo.h": "Mises à jour",
  "dl.repo.d":
    "SkillFishOS se met à jour depuis son <strong>dépôt officiel</strong> : le noyau, les applications et les thèmes viennent de nous et sont testés, si bien que les mises à jour de Debian sid ne peuvent pas casser le système.",

  "news.title": "Actualités",
  "news.eye": "Tenu à jour",
  "news.h1": "Ce qui a changé,<br>et quand",
  "news.sub":
    "Un petit projet se juge en partie à la fréquence à laquelle il donne des nouvelles. Voici les actualités par date et la route qui vient, avec l'état de chaque point — y compris ceux qui ne sont pas prêts.",
  "news.h.news": "Actualités",
  "news.h.road": "Feuille de route",
  "news.road.sub":
    "Ce sur quoi nous travaillons, ce qui vient ensuite et ce qui est déjà là. Aucune date promise tant que nous ne l'avons pas vraiment.",
  "news.foot":
    "Une idée, ou quelque chose qui manque ? Les demandes sont les bienvenues : écrivez depuis la page <a href=\"/fr/contact\">contact</a> ou ouvrez une discussion sur GitHub. Construire ce dont quelqu'un a vraiment besoin vaut mieux que bien deviner.",
  "news.diroad":
    "Envie de savoir ce qui vient ensuite ? Il y a la <a href=\"/fr/roadmap\">feuille de route</a>.",

  "road.title": "Feuille de route",
  "road.eye": "Où nous allons",
  "road.h1": "Ce qui arrive,<br>et ce qui est déjà là",
  "road.sub":
    "Aucune date promise tant que nous ne l'avons pas vraiment. Les points terminés restent en bas, parce qu'ils répondent à la question qu'on nous pose le plus : savoir si le projet est vivant.",
  "road.dinews":
    "Vous cherchez plutôt ce qui a changé ? C'est dans les <a href=\"/fr/news\">actualités</a>.",

  "gal.title": "Galerie — SkillFishOS",
  "gal.eye": "Galerie",
  "gal.h2": "Beau à regarder, simple à utiliser.",
  "gal.sub":
    "Un aperçu de SkillFishOS à l'œuvre : bureau, jeux, émulation et outils.",
  "gal.desktop.t": "Le bureau steampunk",
  "gal.desktop.d":
    "KDE Plasma assorti, avec un affichage système en direct en haut à droite.",
  "gal.about.t": "Informations système",
  "gal.about.d":
    "Une identité complète : nom, logo et matériel reconnus comme SkillFishOS.",
  "gal.emudeck.t": "EmuDeck",
  "gal.emudeck.d":
    "Installation et réglage des émulateurs en quelques clics.",
  "gal.esde1.t": "ES-DE — Interface",
  "gal.esde1.d":
    "L'interface ES-DE pour parcourir et lancer vos bibliothèques.",
  "gal.ai.t": "Panneau d'IA",
  "gal.ai.d":
    "Allumez et éteignez l'IA locale (Vulkan) en un clic.",
  "gal.tuner.t": "Tuner — unités de calcul à chaud",
  "gal.tuner.d":
    "Grille des CU (vert = active, rouge = éteinte), profils 24/32/40 et test, sans redémarrer.",
  "gal.tunerctl.t": "Tuner — profils, gouverneur et assistants",
  "gal.tunerctl.d":
    "Les profils Stock/Performance/Turbo/Crazy, le panneau « Mon silicium », le mode du gouverneur Équilibré/Performance et les assistants « Trouver mon maximum » pour le CPU et le GPU.",
  "gal.monitor.t": "Télémétrie en direct pendant les tests",
  "gal.monitor.d":
    "Courbes de température, fréquence, tension et ventilateur en temps réel.",
  "gal.cutest.t": "Test des CU — loterie du silicium",
  "gal.cutest.d":
    "Vérifie que les 40 CU tiennent la charge sans défaut (utile sur des puces récupérées).",
  "gal.wukong.t": "Black Myth: Wukong — 112 FPS",
  "gal.wukong.d":
    "Moyenne en 1080p sur la BC-250 (max 128, 1 % bas 101).",
  "gal.super.t": "Unigine Superposition — 12 938",
  "gal.super.d":
    "1080p High : les performances d'une Radeon RX 6600 sur une carte à ~50 €.",
  "gal.heaven.t": "Unigine Heaven — 113,7 FPS",
  "gal.heaven.d":
    "Score 2865 en 1080p Ultra, anticrénelage 8×, tessellation Extreme.",
  "gal.boot.t": "Démarrage steampunk",
  "gal.boot.d":
    "Un habillage de laiton cohérent, de GRUB jusqu'au bureau.",
  "gal.b1.t": "Même matériel, +34 % — face à Bazzite",
  "gal.b1.d":
    "Superposition 1080p Extreme : la même BC-250 marque 4102 aux fréquences d'origine sur une autre distribution ; SkillFishOS atteint 5513. Classement officiel Unigine.",
  "gal.b2.t": "Au niveau d'une Radeon RX 6600",
  "gal.b2.d":
    "Superposition 1080p High : la BC-250 avec SkillFishOS (12 938) fait jeu égal avec une RX 6600/6600 XT à plus de 200 € (12 454). Classement officiel Unigine.",

  "hwp.title": "Le matériel AMD BC-250 — SkillFishOS",
  "hwp.eye": "Matériel",
  "hwp.h2": "Née pour l'<span class=\"gold-text\">AMD BC-250</span>.",
  "hwp.sub":
    "Un APU AMD Zen 2 + RDNA 2 semi-personnalisé avec 16 Go de GDDR6, libéré sous Linux.",
  "hwp.specs.h": "Caractéristiques",
  "hwp.cpu.t": "CPU — 8× Zen 2",
  "hwp.cpu.d":
    "« Oberon », <strong>8 cœurs / 16 fils</strong> (la carte en montre 6, SkillFishOS déverrouille les deux autres par la SMU : <strong>+20 %</strong> mesuré), jusqu'à <strong>4,0 GHz sur tous les cœurs</strong> en overclock.",
  "hwp.gpu.t": "GPU — RDNA 2",
  "hwp.gpu.d":
    "« Cyan Skillfish » (gfx1013), jusqu'à 40 unités de calcul déverrouillables.",
  "hwp.mem.t": "Mémoire — 16 Go GDDR6",
  "hwp.mem.d":
    "Partagée (UMA) entre le CPU et le GPU ; sous Linux le GTT agrandit la mémoire vidéo.",
  "hwp.perf.t": "Calcul — ~11 TFLOPS",
  "hwp.perf.d":
    "FP32 à 40 CU / 2000 MHz (vkpeak), avec l'accélération Vulkan.",
  "hwp.quirks.h": "Les défauts du matériel (et comment nous les rattrapons)",
  "hwp.q1.t": "HPD du DisplayPort cassé",
  "hwp.q1.d":
    "La détection de l'écran ne marche pas → service dédié + paramètre de noyau <code>video=DP-1:e</code>.",
  "hwp.q2.t": "Mise en veille cassée",
  "hwp.q2.d":
    "La carte ne se réveille pas → tous les états de veille désactivés pour de bon.",
  "hwp.q3.t": "IOMMU instable",
  "hwp.q3.d":
    "À ne jamais activer → le système démarre toujours sans IOMMU.",
  "hwp.q4.t": "Refroidissement juste",
  "hwp.q4.d":
    "Un seul capteur de bord, aucun pour la mémoire graphique → une garde thermique à 85 °C toujours active.",
  "hwp.cta": "En lire plus dans la documentation →",

  "bm.h": "Performances mesurées",
  "bm.sub":
    "vkpeak FP32 scalaire (GFLOPS) sur la <strong>même</strong> BC-250, avant et après SkillFishOS.",
  "bm.bar1": "Départ — XanMod, 24 CU",
  "bm.bar2": "tkg + gouverneur, 24 CU",
  "bm.bar3": "SkillFishOS — tkg + gouverneur + 40 CU",
  "bm.unit": "GFLOPS",
  "bm.note":
    "Mesures <strong>vkpeak</strong> (calcul Vulkan) sur la même carte, à froid et au repos. Avec les 40 CU actives le GPU rend <strong>1,84×</strong> le système de départ. Au repos le gouverneur redescend à 350 MHz ; bord à ~54 °C après la charge de calcul.",
  "bm.s1.l": "FP32 par rapport au départ",
  "bm.s2.l": "GFLOPS FP32 (≈11,3 TFLOPS)",
  "bm.s3.l": "GFLOPS FP16 (vec4)",
  "bm.s4.l": "GIOPS int8 (produit scalaire)",
  "bm.src":
    "Source : mesures du projet sur du matériel réel (vkpeak). Détails dans",
  "bm.gpulink": "GPU, gouverneur et overclock",

  "wk.h": "Charge réelle — Black Myth: Wukong (1080p)",
  "wk.note":
    "~4 minutes de télémétrie en jeu : <strong>le CPU et le GPU tiennent tout l'overclock</strong> sous le plafond thermique de 85 °C — gouverneur, overclock et garde thermique encaissent un titre AAA exigeant. (Wukong est limité par <em>le CPU et les appels de dessin</em> : ce qui compte ici c'est la stabilité en charge, pas la définition.)",
  "wk.l.gpu": "GPU (point sûr)",
  "wk.l.gpuc": "Bord du GPU (max 81)",
  "wk.l.pwr": "Consommation (pic 182 W)",
  "wk.l.cpu": "CPU (overclock)",
  "wk.l.vram": "Mémoire graphique utilisée",
  "wk.l.fan": "Ventilateur",

  "bs.h": "Captures réelles — prises sur notre propre matériel",
  "bs.sub":
    "Pas de rendus, pas de maquettes : de vraies captures d'écran prises pendant les mesures, sur <strong>notre</strong> BC-250 sous SkillFishOS. Touchez une image pour l'agrandir.",
  "bs.wk.c":
    "Black Myth: Wukong — <strong>112 FPS</strong> de moyenne en 1080p (max 128, 1 % bas 101). APU AMD BC-250, GPU RADV gfx1013.",
  "bs.hv.c":
    "Unigine Heaven 4.0 — <strong>113,7 FPS</strong>, score <strong>2865</strong> (1080p Ultra, anticrénelage 8×, tessellation Extreme). Noyau 7.0.10-skillfishos (nous livrons aujourd'hui le 7.2.0).",
  "bs.sc.c":
    "Unigine Heaven — la scène calculée en temps réel sur la BC-250 pendant l'essai.",

  "gb.h": "Mesures de jeu — des résultats réels",
  "gb.sub":
    "Mesuré sur la BC-250 sous SkillFishOS, en 1080p. Une carte à <strong>~50 €</strong> qui joue dans la catégorie de la <strong>Radeon RX&nbsp;6600</strong>.",
  "gb.wk.v": "112 FPS",
  "gb.wk.l": "Black Myth: Wukong · moyenne en 1080p",
  "gb.hv.v": "2865",
  "gb.hv.l":
    "Unigine Heaven · 1080p Ultra/Extreme · anticrénelage 8× · 113 FPS",
  "gb.sp.v": "12 938",
  "gb.sp.l": "Unigine Superposition · 1080p High · (5513 en Extreme)",

  "cmp.os.h": "Même matériel, +34 % rien qu'en changeant de système",
  "cmp.os.sub":
    "Superposition 1080p Extreme, sur la <strong>même BC-250</strong> : SkillFishOS contre une autre distribution aux fréquences d'origine.",
  "cmp.os.b1": "SkillFishOS — GPU 2230 · CPU 3900",
  "cmp.os.b2": "Autre distribution (Bazzite) — GPU 2100 · CPU 3436",
  "cmp.os.note":
    "40 CU déverrouillées, un gouverneur qui pousse le GPU à 2230 MHz et un overclock avec undervolt du CPU : <strong>+34 % de performances réelles</strong> tirées de la même puce. Source : le classement officiel Unigine.",
  "cmp.gpu.h": "Face aux Radeon de bureau",
  "cmp.gpu.sub":
    "Superposition 1080p High : la BC-250 sous SkillFishOS fait jeu égal avec une <strong>RX&nbsp;6600/6600&nbsp;XT</strong> à plus de 200 €.",
  "cmp.gpu.b1": "SkillFishOS — BC-250 (~50 €)",
  "cmp.gpu.b2": "Radeon RX 6600 / 6600 XT",
  "cmp.gpu.b3": "Radeon RX 6700 / 6750 XT",
  "cmp.gpu.note":
    "La puissance de calcul brute d'une RX&nbsp;6700 (~11,3 TFLOPS), les performances en jeu d'une RX&nbsp;6600/6600&nbsp;XT — sur une carte à ~50 €. Une <strong>puce RDNA&nbsp;2 semi-personnalisée, de classe console</strong> (« Oberon », gfx1013), libérée sous Linux.",
  "cmp.axis": "Score Superposition",

  "oc.h": "Overclock et undervolt — caractérisés à la main",
  "oc.sub":
    "Courbes tension/fréquence mesurées par la SMU sur l'APU « Oberon », avec une vraie validation thermique. Tout se pilote depuis le <strong>Tuner</strong> avec des profils prêts.",
  "oc.cpu.v": "4,0 GHz",
  "oc.cpu.l":
    "CPU 8 cœurs sur tous les cœurs · remesuré marche après marche · 0 erreur machine",
  "oc.uv.v": "−194 mV",
  "oc.uv.l": "Undervolt du CPU à 3,7 GHz (1206→1012 mV) sans rien perdre",
  "oc.gpu.v": "2230 MHz",
  "oc.gpu.l": "GPU · 40 CU · gouverneur SMU dédié",
  "oc.cap.v": "85 °C",
  "oc.cap.l":
    "Plafond thermique CPU+GPU : il bride la fréquence, il ne casse jamais",
  "oc.note":
    "Pour chaque fréquence nous avons cherché la <strong>tension stable la plus basse</strong> en lisant le VID réel dans la SMU et en validant par 120 s de charge. Les profils <strong>Stock · Performance · Turbo · Crazy</strong> appliquent ces réglages en un clic ; une garde thermique tient le tout sous 85 °C. Tous les détails dans la documentation.",

  "don.title": "Nous soutenir — Offrez-nous un café",
  "don.eye": "Soutenir le projet",
  "don.h2":
    "Aidez à forger l'<span class=\"gold-text\">avenir</span> de SkillFishOS",
  "don.sub":
    "SkillFishOS est et restera <strong>libre et gratuit</strong>. Mais derrière, il y a une <strong>petite équipe</strong> et une seule carte : une petite contribution garde le développement rapide — et vivant.",
  "don.why.h": "Une petite équipe. Une carte.",
  "don.why.p1":
    "Derrière SkillFishOS il y a une <strong>petite équipe</strong> qui développe, teste et entretient tout — noyau, applications, thème, dépôt et site — sur son temps libre et <strong>entièrement de sa poche</strong>. Le système est et restera libre et gratuit : pas de mur payant, pas de publicité.",
  "don.why.p2":
    "Aujourd'hui nous n'avons <strong>qu'une seule BC-250</strong>. Chaque correctif de noyau, de gouverneur ou d'overclock doit être testé sur la seule carte que nous ayons : si elle se fige en plein essai, le développement s'arrête. Pas de tests en parallèle, pas de comparaison entre puces différentes (la « loterie du silicium »), pas de marge pour expérimenter sans risque. <strong>Votre aide change tout cela.</strong>",
  "don.use.h": "Où va l'argent",
  "don.use.sub":
    "En toute transparence : chaque euro sert à développer plus vite et mieux.",
  "don.u1.t": "D'autres cartes BC-250",
  "don.u1.d":
    "Plus de cartes = un développement plus rapide et plus sûr : essais en parallèle, comparaison du silicium et une carte de rechange si l'une meurt.",
  "don.u2.t": "Boîtiers et dissipateurs",
  "don.u2.d":
    "Un meilleur refroidissement pour pousser l'overclock et la stabilité — et pour valider les solutions thermiques que nous pouvons vous conseiller.",
  "don.u3.t": "Infrastructure",
  "don.u3.d":
    "Domaine, hébergement, miroirs et intégration continue : les frais qui gardent en ligne le site, le dépôt APT et les téléchargements — aujourd'hui à notre charge.",
  "don.u4.t": "Du temps de développement",
  "don.u4.d":
    "Chaque contribution nous permet de mettre plus d'heures dans les nouveautés, les correctifs et l'aide aux utilisateurs, au lieu d'ailleurs.",
  "don.give.h": "Offrez-nous un café ",
  "don.give.p":
    "Choisissez un montant : PayPal s'ouvre avec la somme déjà prête. Même <strong>1 €, 2 € ou 5 €</strong> font une énorme différence.",
  "don.give.custom": "Montant libre",
  "don.give.or": "ou scannez le QR avec votre téléphone",
  "don.give.scan": "Scannez pour donner",
  "don.give.note":
    "Don ponctuel par <strong>PayPal</strong> : sans engagement, sans abonnement. SkillFishOS reste libre et gratuit pour toujours.",
  "don.thanks":
    "Merci, vraiment — chaque contribution allume un morceau de plus de cette console. ",

  "comm.h": "Vous ne pouvez pas donner ? Aidez quand même, c'est gratuit",
  "comm.sub":
    "Trois gestes d'une minute qui font grandir le projet autant qu'un don.",
  "comm.star.t": "Mettez une étoile sur GitHub",
  "comm.star.d":
    "Plus d'étoiles = plus de visibilité = plus de gens qui découvrent SkillFishOS et y contribuent. C'est la façon la plus rapide d'aider.",
  "comm.star.btn": "Mettre une étoile →",
  "comm.review.t": "Laissez un avis",
  "comm.review.d":
    "Vous avez essayé SkillFishOS ? Racontez comment ça s'est passé sur SourceForge : les avis décident les nouveaux venus à essayer, et nous disent quoi améliorer.",
  "comm.review.btn": "Donner un avis sur SourceForge →",
  "comm.idea.t": "Proposez une idée",
  "comm.idea.d":
    "Quelle fonction vous simplifierait la vie ? Ouvrez une discussion : les idées des utilisateurs guident les prochaines versions de SkillFishOS.",
  "comm.idea.btn": "Proposer une fonction →",

  "ct.title": "Contact — SkillFishOS",
  "ct.eye": "Contact",
  "ct.h2": "Écrivez-nous",
  "ct.sub":
    "Aide, renseignements ou autre chose : remplissez le formulaire et nous répondrons par courrier.",
  "ct.f.name": "Nom",
  "ct.f.email": "Votre adresse de courrier",
  "ct.f.type": "Type de demande",
  "ct.f.msg": "Message",
  "ct.f.captcha": "Combien font",
  "ct.type.support": "Aide",
  "ct.type.info": "Renseignements",
  "ct.type.other": "Autre",
  "ct.send": "Envoyer la demande",
  "ct.privacy":
    "Nous ne publions pas notre adresse pour limiter le pourriel : le formulaire la transmet en sécurité. Les données saisies servent uniquement à vous répondre.",
  "ct.ok": "Message envoyé ! Nous revenons vers vous bientôt.",
  "ct.err.captcha":
    "La vérification anti-pourriel a échoué. Réessayez, s'il vous plaît.",
  "ct.err.fields":
    "Vérifiez les champs : un nom, une adresse de courrier valable et un message sont nécessaires.",
  "ct.err.send":
    "L'envoi a échoué. Réessayez plus tard ou écrivez-nous sur GitHub.",
  "ct.err.generic": "Quelque chose s'est mal passé. Réessayez, s'il vous plaît.",
};

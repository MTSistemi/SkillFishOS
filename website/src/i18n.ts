// SkillFishOS i18n dictionary + helpers.
// Strings keep the original {it, en} shape ported from the legacy landing.
// Values may contain inline HTML → render with `set:html`.

export type Lang = 'it' | 'en';
export const defaultLang: Lang = 'it';
export const languages: Record<Lang, string> = { it: 'Italiano', en: 'English' };

// Centralized site config (download URL finalized later — see DESIGN notes).
export const SITE = {
  github: 'https://github.com/MTSistemi/SkillFishOS',
  domain: 'skillfishos.com',
  // Masked download URL: skillfishos.com/dl/... → 302 to Dropbox (see public/.htaccess).
  // Currently a fully-functional preview ISO hosted on Dropbox.
  isoUrl: '/dl/skillfishos-preview.iso',
  isoSizeGb: '5.78',
  repoUrl: 'http://192.168.5.22',
};

type Entry = Record<Lang, string>;

export const strings: Record<string, Entry> = {
  'title': { it: "SkillFishOs — Gaming Linux per l'AMD BC-250", en: "SkillFishOs — Gaming Linux for the AMD BC-250" },
  'meta.desc': {
    it: "SkillFishOs: il sistema operativo gaming steampunk per la scheda AMD BC-250. Tutto pronto e ottimizzato, senza smanettare. Emulazione, Steam, AI locale. Basato su Debian + KDE Plasma.",
    en: "SkillFishOs: the steampunk gaming operating system for the AMD BC-250 board. Pre-tuned and ready, no tinkering. Emulation, Steam, on-device AI. Built on Debian + KDE Plasma.",
  },

  'nav.feat': { it: "Funzioni", en: "Features" },
  'nav.shots': { it: "Screenshot", en: "Screenshots" },
  'nav.hw': { it: "Hardware", en: "Hardware" },
  'nav.download': { it: "Download", en: "Download" },
  'nav.docs': { it: "Documentazione", en: "Docs" },
  'nav.gallery': { it: "Galleria", en: "Gallery" },

  'hero.soon': { it: "Presto disponibile", en: "Coming soon" },
  'hero.tag': { it: "Il sistema operativo gaming forgiato per l'<b>AMD BC-250</b>.", en: "The gaming operating system forged for the <b>AMD BC-250</b>." },
  'hero.sub': { it: "Linux steampunk, pronto al gioco dal primo avvio. Tutto già ottimizzato, senza smanettare. Emulazione, Steam e AI locale. Basato su Debian e KDE&nbsp;Plasma.", en: "Steampunk Linux, ready to play from the first boot. Everything pre-tuned, no tinkering needed. Emulation, Steam and on-device AI. Built on Debian and KDE&nbsp;Plasma." },
  'hero.btn1': { it: "Guarda il sistema", en: "See it in action" },
  'hero.btn2': { it: "Cosa offre", en: "What's inside" },
  'hero.pill': { it: "APU AMD · Zen&nbsp;2 + RDNA&nbsp;2 · 16&nbsp;GB GDDR6", en: "AMD APU · Zen&nbsp;2 + RDNA&nbsp;2 · 16&nbsp;GB GDDR6" },

  'intro.eye': { it: "Che cos'è", en: "What it is" },
  'intro.h2': { it: "Una console-PC,<br>pronta all'uso.", en: "A console-PC,<br>ready to use." },
  'intro.p1': { it: "SkillFishOs trasforma la scheda <strong>AMD BC-250</strong> — un'APU semi-custom della famiglia <strong>AMD Zen&nbsp;2 + RDNA&nbsp;2</strong> (CPU «Oberon», grafica «Cyan&nbsp;Skillfish», 16&nbsp;GB GDDR6) — in un sistema completo per giocare e usare il PC.", en: "SkillFishOs turns the <strong>AMD BC-250</strong> board — a semi-custom APU from the <strong>AMD Zen&nbsp;2 + RDNA&nbsp;2 family</strong> (CPU “Oberon”, “Cyan&nbsp;Skillfish” graphics, 16&nbsp;GB GDDR6) — into a complete system to play and get things done." },
  'intro.p2': { it: "Governor, patch del kernel, overclock e profili termici sono <strong>già pronti e ottimizzati</strong>: un sistema che gira al massimo <strong>senza dover smanettare</strong>. Estetica <strong>steampunk</strong> coerente dal boot al desktop, pensata anche per far <strong>imparare Linux ai più piccoli</strong> mentre giocano.", en: "Governors, kernel patches, overclock and thermal profiles come <strong>pre-tuned and ready</strong>: a system that runs at its best <strong>with no tinkering</strong>. A consistent <strong>steampunk</strong> look from boot to desktop, also designed to help <strong>kids learn Linux</strong> while they play." },

  'feat.eye': { it: "Funzioni", en: "Features" },
  'feat.h2': { it: "Tutto pronto, fuori dalla scatola.", en: "Everything ready, out of the box." },
  'feat.sub': { it: "Niente da configurare a mano: il sistema è già ottimizzato per la BC-250.", en: "Nothing to set up by hand: the system is already tuned for the BC-250." },
  'f1.t': { it: "Gaming pronto", en: "Ready to game" },
  'f1.d': { it: "Steam, EmuDeck, ES-DE, Heroic e Proton pronti all'uso. Con EmuDeck installi e configuri gli emulatori in pochi clic — i tuoi giochi e le tue ROM li aggiungi tu.", en: "Steam, EmuDeck, ES-DE, Heroic and Proton ready to go. EmuDeck installs and configures the emulators in a few clicks — you bring your own games and ROMs." },
  'f2.t': { it: "Kernel su misura", en: "Tailored kernel" },
  'f2.d': { it: "Kernel tkg ottimizzato per la BC-250: <b>40 Compute Unit</b> sbloccate, overclock CPU/GPU e governor SMU dedicato per spremere ogni TFLOP.", en: "A tkg kernel tuned for the BC-250: <b>40 Compute Units</b> unlocked, CPU/GPU overclock and a dedicated SMU governor to squeeze every TFLOP." },
  'f3.t': { it: "Pronto, senza smanettare", en: "Ready, no tinkering" },
  'f3.d': { it: "Governor, patch, overclock e thermal-guard <b>già configurati e testati</b>. Accendi e funziona al massimo: niente terminale, niente tuning manuale.", en: "Governors, patches, overclock and a thermal-guard <b>already configured and tested</b>. Power on and it runs at full speed: no terminal, no manual tuning." },
  'f4.t': { it: "Tema Steampunk", en: "Steampunk theme" },
  'f4.d': { it: "Desktop KDE&nbsp;Plasma scuro a tema steampunk: icone, cursori, wallpaper e HUD di sistema in stile meccanico-vittoriano.", en: "A dark, steampunk-themed KDE&nbsp;Plasma desktop: icons, cursors, wallpaper and a system HUD in a mechanical-Victorian style." },
  'f5.t': { it: "Snapshot Btrfs", en: "Btrfs snapshots" },
  'f5.d': { it: "Smanetta senza paura: ogni modifica è protetta da snapshot automatici. Qualcosa va storto? <b>Rollback in un clic</b> dal menu di avvio.", en: "Tinker fearlessly: every change is protected by automatic snapshots. Something broke? <b>One-click rollback</b> from the boot menu." },
  'f6.t': { it: "AI in locale", en: "On-device AI" },
  'f6.d': { it: "Stack Ollama + OpenWebUI accelerato in <b>Vulkan</b> sulla GPU integrata. Modelli di chat e coding che girano in casa, senza cloud.", en: "An Ollama + OpenWebUI stack accelerated in <b>Vulkan</b> on the integrated GPU. Chat and coding models running at home, no cloud." },

  'show.eye': { it: "Screenshot", en: "Screenshots" },
  'show.h2': { it: "Bello da vedere, comodo da usare.", en: "Great to look at, easy to use." },
  's1.t': { it: "Il desktop steampunk", en: "The steampunk desktop" },
  's1.d': { it: "KDE Plasma in stile steampunk: wallpaper a tema, accenti dorati e un HUD live con CPU, GPU, temperature, ventola e batteria dei controller Bluetooth, sempre sott'occhio.", en: "Steampunk-styled KDE Plasma: themed wallpaper, golden accents and a live HUD with CPU, GPU, temperatures, fan and Bluetooth controller battery, always in view." },
  's2.t': { it: "Emulazione facile con EmuDeck", en: "Easy emulation with EmuDeck" },
  's2.d': { it: "Con EmuDeck installi e configuri gli emulatori (RetroArch, Dolphin, PCSX2, PPSSPP, RPCS3 e altri) e il frontend ES-DE in pochi clic. Il sistema offre gli strumenti: i giochi e le ROM li metti tu.", en: "EmuDeck installs and configures the emulators (RetroArch, Dolphin, PCSX2, PPSSPP, RPCS3 and more) and the ES-DE frontend in a few clicks. The system provides the tools: you supply the games and ROMs." },
  's4.t': { it: "AI in casa, con un clic", en: "On-device AI, one click away" },
  's4.d': { it: "Un pannello dedicato accende o spegne il motore AI locale (Qwen su GPU Vulkan). Chat web, terminale di coding e gestione: l'intelligenza artificiale gira in casa, e libera la GPU quando vuoi giocare.", en: "A dedicated panel turns the local AI engine (Qwen on the Vulkan GPU) on or off. Web chat, a coding terminal and management: AI runs at home, and frees the GPU when it's time to play." },
  's5.t': { it: "Tuning a portata di clic", en: "One-click tuning" },
  's5.d': { it: "Il Tuner regola frequenze, undervolt, ventola e Compute Unit con preset pronti (Stock, Performance, Crazy) e un thermal-guard che protegge l'hardware. Tutta la potenza, in sicurezza, senza riga di comando.", en: "The Tuner adjusts clocks, undervolt, fan and Compute Units with ready presets (Stock, Performance, Crazy) and a thermal-guard that protects the hardware. All the power, safely, with no command line." },

  'hw.eye': { it: "Hardware", en: "Hardware" },
  'hw.h2': { it: "Nato per l'AMD BC-250.", en: "Born for the AMD BC-250." },
  'hw.sub': { it: "Tutta la potenza della famiglia AMD Zen 2 + RDNA 2, liberata su Linux.", en: "All the power of the AMD Zen 2 + RDNA 2 family, unleashed on Linux." },
  'hw.c1': { it: 'CPU "Oberon" · fino a 3.7 GHz', en: '"Oberon" CPU · up to 3.7 GHz' },
  'hw.c2': { it: 'GPU "Cyan Skillfish" · 40 CU', en: '"Cyan Skillfish" GPU · 40 CU' },
  'hw.c3': { it: "FP32 · accelerazione Vulkan", en: "FP32 · Vulkan acceleration" },
  'hw.c4': { it: "GDDR6 condivisa", en: "shared GDDR6" },

  'cta.h2': { it: 'Accendi. <span class="gold-text">Gioca.</span> Impara.', en: 'Power on. <span class="gold-text">Play.</span> Learn.' },
  'cta.p': { it: "Un sistema operativo che rende una scheda essenziale una vera console-PC. Presto disponibili: la ISO installabile e gli aggiornamenti dedicati.", en: "An operating system that turns a bare board into a real console-PC. Coming soon: the installable ISO and dedicated updates." },
  'cta.btn': { it: "🚀 Presto disponibile", en: "🚀 Coming soon" },

  'foot.based': { it: "Basato su Debian · KDE Plasma · © 2026 SkillFishOs", en: "Based on Debian · KDE Plasma · © 2026 SkillFishOs" },

  // --- Download page ---
  'dl.title': { it: "Download — SkillFishOs", en: "Download — SkillFishOs" },
  'dl.eye': { it: "Download", en: "Download" },
  'dl.h2': { it: "Scarica SkillFish<span class=\"gold-text\">Os</span>", en: "Download SkillFish<span class=\"gold-text\">Os</span>" },
  'dl.sub': { it: "La ISO installabile, brandizzata e pronta all'uso per l'AMD BC-250.", en: "The installable, branded, ready-to-use ISO for the AMD BC-250." },
  'dl.badge': { it: "Preview", en: "Preview" },
  'dl.notice': { it: "Questa è una <strong>preview completamente funzionante</strong> di SkillFishOs: la installi e la usi davvero sulla tua BC-250.", en: "This is a <strong>fully-functional preview</strong> of SkillFishOs: you can really install and use it on your BC-250." },
  'dl.btnsoon': { it: "🚀 ISO in arrivo", en: "🚀 ISO coming soon" },
  'dl.btn': { it: "⬇ Scarica la ISO (Preview)", en: "⬇ Download the ISO (Preview)" },
  'dl.size': { it: "amd64 · ~{size} GB · btrfs + KDE Plasma · preview", en: "amd64 · ~{size} GB · btrfs + KDE Plasma · preview" },
  'dl.bugs.h': { it: "Hai trovato un problema?", en: "Found a problem?" },
  'dl.bugs.d': { it: "La preview è in continuo miglioramento. Per segnalare bug o problemi apri una <em>issue</em> su GitHub. (Presto aggiungeremo anche un indirizzo email.)", en: "The preview is continuously improving. To report bugs or problems, open an <em>issue</em> on GitHub. (We'll add an email address soon.)" },
  'dl.bugs.btn': { it: "🐛 Segnala su GitHub", en: "🐛 Report on GitHub" },

  'dl.req.h': { it: "Requisiti", en: "Requirements" },
  'dl.req.d': { it: "Una scheda <strong>AMD BC-250</strong> (APU Zen&nbsp;2 + RDNA&nbsp;2, 16&nbsp;GB GDDR6), un SSD/NVMe, un monitor <strong>DisplayPort</strong> e una chiavetta USB da almeno 8&nbsp;GB per l'installer.", en: "An <strong>AMD BC-250</strong> board (Zen&nbsp;2 + RDNA&nbsp;2 APU, 16&nbsp;GB GDDR6), an SSD/NVMe, a <strong>DisplayPort</strong> monitor and an 8&nbsp;GB+ USB stick for the installer." },
  'dl.inc.h': { it: "Cosa include", en: "What's included" },
  'dl.inc.d': { it: "Kernel ottimizzato (40&nbsp;CU, governor, OC), tema steampunk completo, Steam + EmuDeck + ES-DE, stack AI locale, snapshot Btrfs e i tool Tuner e AI già pronti.", en: "An optimized kernel (40&nbsp;CU, governor, OC), the full steampunk theme, Steam + EmuDeck + ES-DE, a local AI stack, Btrfs snapshots and the Tuner & AI tools ready to go." },
  'dl.steps.h': { it: "Installazione", en: "Installation" },
  'dl.step1': { it: "Scrivi la ISO su una chiavetta USB (Etcher, Ventoy o <code>dd</code>).", en: "Write the ISO to a USB stick (Etcher, Ventoy or <code>dd</code>)." },
  'dl.step2': { it: "Avvia la BC-250 da USB e segui l'installer grafico (Calamares).", en: "Boot the BC-250 from USB and follow the graphical installer (Calamares)." },
  'dl.step3': { it: "Al primo avvio è tutto già configurato: accendi e gioca.", en: "On first boot everything is set up: power on and play." },

  'dl.repo.h': { it: "Aggiornamenti", en: "Updates" },
  'dl.repo.d': { it: "SkillFishOs si aggiorna dal <strong>repository ufficiale</strong>: kernel, app e temi arrivano da noi e sono testati, così gli aggiornamenti di Debian sid non rompono il sistema.", en: "SkillFishOs updates from its <strong>official repository</strong>: kernel, apps and themes come from us and are tested, so Debian sid updates can't break the system." },

  // --- Gallery page ---
  'gal.title': { it: "Galleria — SkillFishOs", en: "Gallery — SkillFishOs" },
  'gal.eye': { it: "Galleria", en: "Gallery" },
  'gal.h2': { it: "Bello da vedere, comodo da usare.", en: "Great to look at, easy to use." },
  'gal.sub': { it: "Uno sguardo a SkillFishOs in azione: desktop, gaming, emulazione e strumenti.", en: "A look at SkillFishOs in action: desktop, gaming, emulation and tools." },
  'gal.desktop.t': { it: "Il desktop steampunk", en: "The steampunk desktop" },
  'gal.desktop.d': { it: "KDE Plasma a tema, con HUD di sistema live in alto a destra.", en: "Themed KDE Plasma, with a live system HUD in the top-right." },
  'gal.about.t': { it: "Informazioni di sistema", en: "System info" },
  'gal.about.d': { it: "Branding completo: nome, logo e hardware riconosciuti come SkillFishOs.", en: "Full branding: name, logo and hardware recognized as SkillFishOs." },
  'gal.emudeck.t': { it: "EmuDeck", en: "EmuDeck" },
  'gal.emudeck.d': { it: "Installazione e configurazione degli emulatori in pochi clic.", en: "Emulator install and setup in a few clicks." },
  'gal.esde1.t': { it: "ES-DE — Preferiti", en: "ES-DE — Favorites" },
  'gal.esde1.d': { it: "Il frontend ES-DE con la vista dei giochi preferiti.", en: "The ES-DE frontend with the favorites view." },
  'gal.esde2.t': { it: "ES-DE — Neo Geo", en: "ES-DE — Neo Geo" },
  'gal.esde2.d': { it: "Sfoglia le collezioni per sistema, con copertine e metadati.", en: "Browse collections by system, with cover art and metadata." },
  'gal.ai.t': { it: "Pannello AI", en: "AI panel" },
  'gal.ai.d': { it: "Accendi e spegni lo stack AI locale (Vulkan) con un clic.", en: "Turn the local AI stack (Vulkan) on and off with one click." },
  'gal.tuner.t': { it: "Tuner", en: "Tuner" },
  'gal.tuner.d': { it: "Controllo di CPU, GPU, ventola e Compute Unit, con test e rollback.", en: "Control CPU, GPU, fan and Compute Units, with test and rollback." },

  // --- Hardware page ---
  'hwp.title': { it: "Hardware AMD BC-250 — SkillFishOs", en: "AMD BC-250 hardware — SkillFishOs" },
  'hwp.eye': { it: "Hardware", en: "Hardware" },
  'hwp.h2': { it: "Nato per l'<span class=\"gold-text\">AMD BC-250</span>.", en: "Born for the <span class=\"gold-text\">AMD BC-250</span>." },
  'hwp.sub': { it: "Un'APU semi-custom AMD Zen 2 + RDNA 2 con 16 GB di GDDR6, liberata su Linux.", en: "A semi-custom AMD Zen 2 + RDNA 2 APU with 16 GB of GDDR6, unleashed on Linux." },
  'hwp.specs.h': { it: "Specifiche", en: "Specifications" },
  'hwp.cpu.t': { it: "CPU — 6× Zen 2", en: "CPU — 6× Zen 2" },
  'hwp.cpu.d': { it: '"Oberon", 6 core / 12 thread, fino a ~3.7 GHz in overclock.', en: '"Oberon", 6 cores / 12 threads, up to ~3.7 GHz overclocked.' },
  'hwp.gpu.t': { it: "GPU — RDNA 2", en: "GPU — RDNA 2" },
  'hwp.gpu.d': { it: '"Cyan Skillfish" (gfx1013), fino a 40 Compute Unit sbloccabili.', en: '"Cyan Skillfish" (gfx1013), up to 40 unlockable Compute Units.' },
  'hwp.mem.t': { it: "Memoria — 16 GB GDDR6", en: "Memory — 16 GB GDDR6" },
  'hwp.mem.d': { it: "Condivisa (UMA) tra CPU e GPU; su Linux il GTT estende la memoria video.", en: "Shared (UMA) between CPU and GPU; on Linux the GTT extends the video memory." },
  'hwp.perf.t': { it: "Potenza — ~11 TFLOPS", en: "Compute — ~11 TFLOPS" },
  'hwp.perf.d': { it: "FP32 a 40 CU / 2000 MHz (vkpeak), con accelerazione Vulkan.", en: "FP32 at 40 CU / 2000 MHz (vkpeak), with Vulkan acceleration." },
  'hwp.quirks.h': { it: "Difetti hardware (e come li risolviamo)", en: "Hardware flaws (and how we fix them)" },
  'hwp.q1.t': { it: "DisplayPort HPD rotto", en: "Broken DisplayPort HPD" },
  'hwp.q1.d': { it: "Il rilevamento del monitor non funziona → demone dedicato + parametro kernel <code>video=DP-1:e</code>.", en: "Monitor detection doesn't work → dedicated daemon + <code>video=DP-1:e</code> kernel parameter." },
  'hwp.q2.t': { it: "Sospensione guasta", en: "Broken suspend" },
  'hwp.q2.d': { it: "La scheda non si risveglia → tutti gli stati di sleep disabilitati in modo permanente.", en: "The board won't wake up → all sleep states permanently disabled." },
  'hwp.q3.t': { it: "IOMMU instabile", en: "Unstable IOMMU" },
  'hwp.q3.d': { it: "Da non abilitare mai → il sistema parte sempre senza IOMMU.", en: "Must never be enabled → the system always boots without IOMMU." },
  'hwp.q4.t': { it: "Raffreddamento marginale", en: "Marginal cooling" },
  'hwp.q4.d': { it: "Solo sensore edge, niente sensore VRAM → thermal-guard a 85 °C sempre attivo.", en: "Edge sensor only, no VRAM sensor → an 85 °C thermal-guard always active." },
  'hwp.cta': { it: "Approfondisci nella documentazione →", en: "Read more in the documentation →" },
};

export function t(key: string, lang: Lang): string {
  const e = strings[key];
  if (!e) return key;
  return e[lang] ?? e[defaultLang];
}

/** Locale-aware path helper: prefixes EN routes with /en. */
export function localePath(path: string, lang: Lang): string {
  const clean = path.startsWith('/') ? path : `/${path}`;
  if (lang === defaultLang) return clean;
  return `/en${clean === '/' ? '' : clean}`;
}

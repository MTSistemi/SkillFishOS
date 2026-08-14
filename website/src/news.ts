// Novità e roadmap del progetto.
//
// Perché i contenuti stanno qui e non dentro i18n.ts: sono voci che si
// aggiungono spesso, e una lista di oggetti si allunga con tre righe senza
// gonfiare il dizionario. Le stringhe possono contenere HTML: si rendono con
// `set:html`.
//
// Le lingue mancanti ripiegano sull'inglese, come tutto il resto del progetto:
// titoli ed etichette sono tradotti anche in polacco e ucraino, i testi lunghi
// dei post restano in inglese finché non li rivede un madrelingua.

import type { Lang } from './i18n';

type Testo = Partial<Record<Lang, string>>;

export function pick(x: Testo, lang: Lang): string {
  return x[lang] ?? x.en ?? x.it ?? '';
}

// ---------------------------------------------------------------- roadmap ---

export type Stato = 'fatto' | 'corso' | 'previsto';

export interface VoceRoadmap {
  stato: Stato;
  quando?: Testo;
  titolo: Testo;
  testo: Testo;
}

export const roadmap: VoceRoadmap[] = [
  {
    stato: 'previsto',
    quando: { it: 'dicembre 2026', en: 'December 2026', pl: 'grudzień 2026', uk: 'грудень 2026' },
    titolo: {
      it: 'Release 26.12 su Debian trixie + backports',
      en: 'Release 26.12 on Debian trixie + backports',
    },
    testo: {
      it: "La base passa da <strong>sid</strong> a <strong>trixie (stable)</strong> con i backports: sistema stabile, kernel e grafica recenti dove servono. È la risposta alla critica più fondata che ci hanno fatto — sid dà il software più nuovo ma può rompersi, e su una console di casa questo pesa.",
      en: "The base moves from <strong>sid</strong> to <strong>trixie (stable)</strong> plus backports: a stable system with a recent kernel and graphics where it matters. This answers the fairest criticism we have had — sid gives you the newest software but it can break, and on a home console that hurts.",
    },
  },
  {
    stato: 'corso',
    titolo: {
      it: 'Scaricamento via torrent',
      en: 'Torrent downloads',
    },
    testo: {
      it: "Da SourceForge in Europa si scarica a circa 250 kB/s: per un'immagine da 4,7 GB è inaccettabile, ed è la prima cosa in cui si imbatte chi ci prova. Stiamo preparando la distribuzione via torrent, con i mirror attuali come sorgente HTTP di riserva, così chi scarica non dipende da un solo specchio lento.",
      en: "From SourceForge in Europe you get around 250 kB/s: for a 4.7 GB image that is unacceptable, and it is the first thing anyone meets. We are preparing torrent distribution, with the current mirrors as HTTP fallback sources, so a download no longer depends on one slow mirror.",
    },
  },
  {
    stato: 'corso',
    titolo: {
      it: "Guida all'installazione con le immagini, in quattro lingue",
      en: 'Installation guide with screenshots, in four languages',
    },
    testo: {
      it: "Una guida passo passo con le schermate vere dell'installer, rifatte per ogni lingua: l'interfaccia cambia, quindi non basta tradurre le didascalie. Chi installa per la prima volta vede esattamente quello che ha davanti, nella sua lingua.",
      en: "A step-by-step guide with real installer screenshots, reshot for every language: the interface changes, so translating the captions is not enough. A first-time installer sees exactly what is in front of them, in their own language.",
    },
  },
  {
    stato: 'previsto',
    titolo: {
      it: 'Gestione degli snapshot con una finestra',
      en: 'Snapshot management in a window',
    },
    testo: {
      it: "Btrfs Assistant è già dentro il sistema: va messo nel menu, vestito col tema e tradotto, così elencare, creare e ripristinare uno snapshot non richiede il terminale. Chi preferisce la riga di comando continua a usare <code>skillfish-rollback</code>.",
      en: "Btrfs Assistant already ships with the system: it needs to be in the menu, themed and translated, so that listing, creating and restoring a snapshot needs no terminal. Anyone who prefers the command line keeps <code>skillfish-rollback</code>.",
    },
  },
  {
    stato: 'previsto',
    titolo: {
      it: 'Streaming dei giochi con Sunshine',
      en: 'Game streaming with Sunshine',
    },
    testo: {
      it: 'Giocare da un altro dispositivo, con la scheda che lavora in un angolo della casa. Il modulo è previsto nel pannello di controllo remoto, che già gestisce schermo, terminale e AI.',
      en: 'Play from another device while the board works away in a corner of the house. The module is planned for the remote panel, which already handles screen, terminal and AI.',
    },
  },
  {
    stato: 'previsto',
    titolo: {
      it: 'Giochi su un disco esterno',
      en: 'Games on an external drive',
    },
    testo: {
      it: "Un selettore per installare i giochi su un SSD USB invece che sul disco di sistema. Steam arriva come Flatpak, quindi non basta cambiare cartella: serve dare il permesso giusto al contenitore, ed è proprio il pezzo che vogliamo togliere di mezzo all'utente.",
      en: "A selector to install games on a USB SSD instead of the system disk. Steam ships as a Flatpak, so changing folder is not enough: the container needs the right permission, and that is exactly the part we want to take off the user's hands.",
    },
  },
  {
    stato: 'previsto',
    titolo: {
      it: 'HUD configurabile e curva della ventola',
      en: 'Configurable HUD and fan curve',
    },
    testo: {
      it: "Il pannello a schermo oggi è tarato sulla BC-250 e su altre macchine si nasconde. Diventerà un'applicazione che legge i sensori davvero presenti e si costruisce la configurazione da sola. Insieme arriva l'editor della curva della ventola dentro il Tuner.",
      en: "The on-screen panel is tuned for the BC-250 today and hides itself on other machines. It will become an application that reads the sensors actually present and builds its own configuration. The fan curve editor lands in the Tuner alongside it.",
    },
  },
  {
    stato: 'previsto',
    titolo: {
      it: "Revisione dell'ucraino da un madrelingua",
      en: 'Ukrainian reviewed by a native speaker',
    },
    testo: {
      it: "Il polacco è stato riletto da un madrelingua, e si vede. Cerchiamo qualcuno che faccia lo stesso con l'ucraino: se è la tua lingua e ti va di darci una mano, sei il benvenuto.",
      en: "Polish was reviewed by a native speaker, and it shows. We are looking for someone to do the same for Ukrainian: if that is your language and you fancy lending a hand, you are welcome.",
    },
  },
  {
    stato: 'fatto',
    quando: { it: 'agosto 2026', en: 'August 2026', pl: 'sierpień 2026', uk: 'серпень 2026' },
    titolo: {
      it: 'Punti di ripristino, e un comando per tornare indietro',
      en: 'Restore points, and one command to go back',
    },
    testo: {
      it: "Il sistema tiene cinque punti di ripristino, presi da solo prima di ogni aggiornamento, e li mostra nel menu di avvio. Con <code>skillfish-rollback</code> si torna a uno di essi per davvero, in un comando: la cartella personale non viene toccata.",
      en: "The system keeps five restore points, taken by itself before every upgrade, and lists them in the boot menu. <code>skillfish-rollback</code> takes you back to one of them for real, in a single command — your home directory is left alone.",
    },
  },
  {
    stato: 'fatto',
    quando: { it: 'agosto 2026', en: 'August 2026', pl: 'sierpień 2026', uk: 'серпень 2026' },
    titolo: {
      it: 'Quattro lingue, con ripiego sempre in inglese',
      en: 'Four languages, always falling back to English',
    },
    testo: {
      it: 'Italiano, inglese, polacco e ucraino nelle applicazioni, nella schermata di accesso, nel pannello web e nelle diapositive dell\'installer. E una regola: se una traduzione manca, esce l\'inglese, mai l\'italiano.',
      en: 'Italian, English, Polish and Ukrainian across the applications, the login screen, the web panel and the installer slideshow. Plus a rule: if a translation is missing you get English, never Italian.',
    },
  },
  {
    stato: 'fatto',
    quando: { it: 'giugno 2026', en: 'June 2026', pl: 'czerwiec 2026', uk: 'червень 2026' },
    titolo: {
      it: 'Otto core invece di sei',
      en: 'Eight cores instead of six',
    },
    testo: {
      it: 'La scheda si presenta come 6 core / 12 thread, ma i due mancanti sono spenti dalla configurazione, non difettosi. SkillFishOS li riaccende all\'avvio: <strong>+20% misurato</strong> sui carichi multi-thread, senza toccare il BIOS.',
      en: 'The board presents itself as 6 cores / 12 threads, but the two missing ones are switched off by configuration, not defective. SkillFishOS turns them back on at boot: <strong>+20% measured</strong> on multi-threaded work, with no BIOS changes.',
    },
  },
];

// ------------------------------------------------------------------- news ---

export interface Post {
  data: string;           // ISO, per l'ordinamento e l'attributo datetime
  quando: Testo;          // come si legge, per lingua
  etichetta?: Testo;      // release / aggiornamento / ...
  titolo: Testo;
  testo: Testo;
}

export const news: Post[] = [
  {
    data: '2026-08-11',
    quando: { it: '11 agosto 2026', en: '11 August 2026', pl: '11 sierpnia 2026', uk: '11 серпня 2026' },
    etichetta: { it: 'release', en: 'release', pl: 'wydanie', uk: 'реліз' },
    titolo: {
      it: 'SkillFishOS 26.06.3 «Aetherium»',
      en: 'SkillFishOS 26.06.3 “Aetherium”',
    },
    testo: {
      it: "Due edizioni, <strong>BC-250</strong> e <strong>Generic</strong>, per la scheda AMD e per qualsiasi PC o macchina virtuale x86-64.<br><br>La lingua che scegli vale adesso <strong>ovunque</strong>: interfaccia, schermata di accesso, pannello web e anche le diapositive dell'installer, che prima restavano in inglese. Italiano, inglese, polacco e ucraino, e se una traduzione manca esce l'inglese.<br><br>Sotto: kernel <strong>7.1.7</strong> con lo sblocco delle 40 Compute Unit e degli otto core, installazione su Btrfs con punti di ripristino attivi dal primo avvio, e AI locale su GPU. Un'installazione nuova parte con <strong>tutti i servizi a posto</strong>.<br><br>L'edizione <strong>Slim</strong> non esce più come immagine: il kernel slim resta nel repository per chi lo vuole.",
      en: "Two editions, <strong>BC-250</strong> and <strong>Generic</strong>, for the AMD board and for any x86-64 PC or virtual machine.<br><br>The language you choose now applies <strong>everywhere</strong>: interface, login screen, web panel and the installer slideshow too, which used to stay in English. Italian, English, Polish and Ukrainian — and if a translation is missing, you get English.<br><br>Underneath: kernel <strong>7.1.7</strong> with the 40 Compute Unit unlock and the eight-core unlock, Btrfs installs with restore points live from the first boot, and on-device AI on the GPU. A fresh install comes up with <strong>every service healthy</strong>.<br><br>The <strong>Slim</strong> edition is no longer shipped as an image: the slim kernel stays in the repository for anyone who wants it.",
    },
  },
  {
    data: '2026-08-11',
    quando: { it: '11 agosto 2026', en: '11 August 2026', pl: '11 sierpnia 2026', uk: '11 серпня 2026' },
    etichetta: { it: 'aggiornamento', en: 'update', pl: 'aktualizacja', uk: 'оновлення' },
    titolo: {
      it: 'Cinque punti di ripristino, e un comando per tornare indietro',
      en: 'Five restore points, and one command to go back',
    },
    testo: {
      it: "Il sistema si prende cura da solo dei punti di ripristino: ne fa uno <strong>prima</strong> e uno <strong>dopo</strong> ogni operazione di <code>apt</code>, ne tiene <strong>cinque</strong> — tre ordinari e due degli aggiornamenti importanti, quelli che toccano kernel o systemd — e li elenca nel menu di avvio, aggiornato a ogni transazione.<br><br>Dal menu di avvio ci si entra per guardare e recuperare file. Per ripartire davvero da uno di essi c'è un comando nuovo:<br><br><code>sudo skillfish-rollback 12</code><br><br>Al riavvio successivo il sistema è quello di allora. Il sistema di prima non viene cancellato: resta da parte, e <code>--annulla</code> lo rimette al suo posto. La <strong>cartella personale non viene mai toccata</strong>: torna indietro il sistema, i tuoi file restano quelli di adesso.<br><br>Arriva con <code>sudo apt update && sudo apt upgrade</code>, senza reinstallare niente.",
      en: "The system looks after its own restore points: it takes one <strong>before</strong> and one <strong>after</strong> every <code>apt</code> operation, keeps <strong>five</strong> — three ordinary ones and two from the important upgrades, the ones touching the kernel or systemd — and lists them in the boot menu, refreshed on every transaction.<br><br>From the boot menu you go in to look around and rescue files. To actually start again from one of them there is a new command:<br><br><code>sudo skillfish-rollback 12</code><br><br>At the next boot the system is the one from back then. The previous system is not deleted: it is set aside, and <code>--undo</code> puts it back. Your <strong>home directory is never touched</strong>: the system travels back, your files stay as they are.<br><br>It arrives with <code>sudo apt update && sudo apt upgrade</code> — no reinstall needed.",
    },
  },
  {
    data: '2026-08-10',
    quando: { it: 'agosto 2026', en: 'August 2026', pl: 'sierpień 2026', uk: 'серпень 2026' },
    etichetta: { it: 'AI', en: 'AI', pl: 'AI', uk: 'ШІ' },
    titolo: {
      it: "L'AI locale passa a Unsloth Studio",
      en: 'On-device AI moves to Unsloth Studio',
    },
    testo: {
      it: "Al posto di tre container Docker c'è <strong>un solo servizio nativo</strong>, con la chat e un'API compatibile OpenAI. Docker non è più installato.<br><br>Sulla scheda, con Qwen3-1.7B: <strong>210 token al secondo</strong> sulla GPU via Vulkan contro 41 sulla sola CPU, cioè cinque volte tanto. I modelli si prendono direttamente dal catalogo di Hugging Face. Il servizio ascolta solo in locale: da fuori ci si arriva attraverso il pannello remoto, che autentica con le credenziali di sistema.",
      en: "Instead of three Docker containers there is now <strong>a single native service</strong>, offering both the chat and an OpenAI-compatible API. Docker is no longer installed.<br><br>On the board, with Qwen3-1.7B: <strong>210 tokens per second</strong> on the GPU over Vulkan against 41 on the CPU alone — five times as fast. Models come straight from the Hugging Face catalogue. The service listens on loopback only: from outside you reach it through the remote panel, which authenticates against the system accounts.",
    },
  },
  {
    data: '2026-07-11',
    quando: { it: '11 luglio 2026', en: '11 July 2026', pl: '11 lipca 2026', uk: '11 липня 2026' },
    etichetta: { it: 'release', en: 'release', pl: 'wydanie', uk: 'реліз' },
    titolo: {
      it: 'SkillFishOS 26.06.2',
      en: 'SkillFishOS 26.06.2',
    },
    testo: {
      it: 'Immagini rigenerate con le correzioni raccolte dopo il primo mese: lingua della sessione live, AI sulla GPU, gruppi utente. Tre edizioni su SourceForge.',
      en: 'Images rebuilt with the fixes gathered over the first month: live session language, AI on the GPU, user groups. Three editions on SourceForge.',
    },
  },
  {
    data: '2026-06-06',
    quando: { it: '6 giugno 2026', en: '6 June 2026', pl: '6 czerwca 2026', uk: '6 червня 2026' },
    etichetta: { it: 'release', en: 'release', pl: 'wydanie', uk: 'реліз' },
    titolo: {
      it: 'La prima release pubblica: 26.06 «Aetherium»',
      en: 'The first public release: 26.06 “Aetherium”',
    },
    testo: {
      it: "Una scheda da mining comprata di seconda mano diventa una console-PC pronta all'uso: kernel su misura con lo sblocco delle 40 Compute Unit, governor SMU, profili di overclock con protezione termica, tema steampunk dal boot al desktop, Steam ed emulatori, AI locale.<br><br>Era nato per far usare e imparare Linux ai miei figli mentre giocano. Il gioco è la carota, gli snapshot sono la rete.",
      en: "A second-hand mining board becomes a ready-to-use console-PC: a custom kernel with the 40 Compute Unit unlock, an SMU governor, overclock profiles with a thermal guard, a steampunk theme from boot to desktop, Steam and emulators, on-device AI.<br><br>It started as a way to get my children using and learning Linux while they game. Gaming is the carrot, snapshots are the net.",
    },
  },
];

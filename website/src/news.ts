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
    stato: 'corso',
    titolo: {
      it: 'Ogni immagine provata su una scheda vera prima di uscire',
      en: 'Every image tested on real hardware before it ships',
      pl: 'Każdy obraz sprawdzony na prawdziwej płycie przed wydaniem',
      uk: 'Кожен образ перевірено на справжній платі перед випуском',
    },
    testo: {
      it: "Le due falle che potevano bloccare l'installazione della 26.06.3 le ha trovate chi ha installato su una BC-250 vera, non noi: in macchina virtuale erano <strong>invisibili per costruzione</strong>, perché il pezzo di codice che rompe l'hardware è proprio quello che una macchina virtuale non può eseguire. Da qui in avanti nessuna immagine esce senza un'installazione completa su una scheda vera, e la costruzione si rifiuta di produrre un'immagine se un controllo non passa.",
      en: "The two defects that could stop a 26.06.3 installation were found by someone installing on a real BC-250, not by us: in a virtual machine they were <strong>invisible by construction</strong>, because the code that breaks the hardware is exactly what a virtual machine cannot execute. From here on no image ships without a full install on a real board, and the build refuses to produce an image when a check fails.",
      pl: "Dwie usterki, które mogły zatrzymać instalację 26.06.3, znalazł ktoś instalujący na prawdziwym BC-250, a nie my: w maszynie wirtualnej były <strong>niewidoczne z założenia</strong>, bo kod psujący sprzęt to dokładnie ten, którego maszyna wirtualna nie potrafi wykonać. Od tej pory żaden obraz nie wychodzi bez pełnej instalacji na prawdziwej płycie, a budowanie odmawia stworzenia obrazu, gdy któraś kontrola nie przejdzie.",
      uk: "Дві вади, які могли зупинити встановлення 26.06.3, знайшов той, хто встановлював на справжню BC-250, а не ми: у віртуальній машині вони були <strong>невидимі за побудовою</strong>, бо код, що ламає залізо, — саме той, який віртуальна машина виконати не може. Відтепер жоден образ не виходить без повного встановлення на справжній платі, а збирання відмовляється створювати образ, якщо якась перевірка не проходить.",
    },
  },
  {
    stato: 'fatto',
    quando: { it: 'agosto 2026', en: 'August 2026', pl: 'sierpień 2026', uk: 'серпень 2026' },
    titolo: {
      it: 'Tutto il codice pubblicato, anche quello che non si vede',
      en: 'All the code published, including the part nobody sees',
      pl: 'Cały kod opublikowany, także ta część, której nie widać',
      uk: 'Увесь код оприлюднено, зокрема й той, якого не видно',
    },
    testo: {
      it: "Non solo le applicazioni: adesso è pubblica anche l'infrastruttura che trasforma una compilazione in qualcosa che si può installare — il repository apt firmato, il caricamento sui mirror, le statistiche, la pubblicazione del sito. Nessuno di quegli script contiene una credenziale: le leggono da file che restano fuori dal repository, e accanto ci sono i modelli da riempire. Chi vuole rifare la stessa catena a casa propria adesso può.",
      en: "Not just the applications: the infrastructure that turns a build into something installable is public too — the signed apt repository, the upload to the mirrors, the statistics, the website deploy. None of those scripts contains a credential: they read files that stay out of the repository, and the templates to fill in sit next to them. Anyone who wants to rebuild the same chain at home now can.",
      pl: "Nie tylko aplikacje: publiczna jest teraz także infrastruktura, która zmienia kompilację w coś, co da się zainstalować — podpisane repozytorium apt, wysyłka na serwery lustrzane, statystyki, publikacja strony. Żaden z tych skryptów nie zawiera danych logowania: czytają je z plików, które zostają poza repozytorium, a obok leżą wzorce do wypełnienia. Kto chce odtworzyć ten sam łańcuch u siebie, teraz może.",
      uk: "Не лише програми: тепер публічна й інфраструктура, яка перетворює збірку на щось, що можна встановити, — підписаний репозиторій apt, вивантаження на дзеркала, статистика, публікація сайту. Жоден із цих скриптів не містить облікових даних: вони читають файли, які лишаються поза репозиторієм, а поруч є шаблони для заповнення. Хто хоче відтворити той самий ланцюг у себе — тепер може.",
    },
  },
  {
    stato: 'previsto',
    quando: { it: 'dicembre 2026', en: 'December 2026', pl: 'grudzień 2026', uk: 'грудень 2026' },
    titolo: {
      it: 'Release 26.12 su Debian trixie + backports',
      en: 'Release 26.12 on Debian trixie + backports',
      pl: 'Wydanie 26.12 na Debianie trixie + backports',
      uk: 'Випуск 26.12 на Debian trixie + backports',
    },
    testo: {
      it: "La base passa da <strong>sid</strong> a <strong>trixie (stable)</strong> con i backports: sistema stabile, kernel e grafica recenti dove servono. È la risposta alla critica più fondata che ci hanno fatto — sid dà il software più nuovo ma può rompersi, e su una console di casa questo pesa.",
      en: "The base moves from <strong>sid</strong> to <strong>trixie (stable)</strong> plus backports: a stable system with a recent kernel and graphics where it matters. This answers the fairest criticism we have had — sid gives you the newest software but it can break, and on a home console that hurts.",
      pl: "Podstawa przechodzi z <strong>sid</strong> na <strong>trixie (stable)</strong> z backportami: stabilny system, a świeże jądro i grafika tam, gdzie to naprawdę ma znaczenie. To odpowiedź na najbardziej trafny zarzut, jaki usłyszeliśmy — sid daje najnowsze oprogramowanie, ale potrafi się popsuć, a na domowej konsoli to boli.",
      uk: "Основа переходить із <strong>sid</strong> на <strong>trixie (stable)</strong> з backports: стабільна система, а свіже ядро та графіка там, де це справді потрібно. Це відповідь на найсправедливіший закид, який ми чули — sid дає найновіше програмне забезпечення, але може зламатися, а на домашній консолі це болить.",
    },
  },
  {
    stato: 'fatto',
    quando: { it: 'agosto 2026', en: 'August 2026', pl: 'sierpień 2026', uk: 'серпень 2026' },
    titolo: {
      it: 'Scaricamento via torrent',
      en: 'Torrent downloads',
      pl: 'Pobieranie przez torrent',
      uk: 'Звантаження через торент',
    },
    testo: {
      it: "Fatto: ogni immagine esce anche come torrent, con un magnet accanto, e a seminarla è un nostro server acceso ventiquattro ore su ventiquattro. I mirror restano dentro il torrent come sorgente HTTP di riserva, quindi il download parte comunque anche quando non c'è nessun altro a condividere. Da SourceForge in Europa si scaricava a circa 250 kB/s: per un'immagine da 4,7 GB era la prima cosa che faceva desistere.",
      en: "Done: every image also ships as a torrent, with a magnet link beside it, seeded by a machine of ours that stays up around the clock. The mirrors remain inside the torrent as HTTP fallback sources, so a download starts even when nobody else is sharing. From SourceForge in Europe you got around 250 kB/s: on a 4.7 GB image that was the first thing that made people give up.",
      pl: "Zrobione: każdy obraz wychodzi także jako torrent, z linkiem magnet obok, a rozsiewa go nasza maszyna działająca całą dobę. Serwery lustrzane zostają w torrencie jako zapasowe źródło HTTP, więc pobieranie ruszy nawet wtedy, gdy nikt inny nie udostępnia. Z SourceForge w Europie schodziło około 250 kB/s: przy obrazie 4,7 GB to była pierwsza rzecz, która zniechęcała.",
      uk: "Зроблено: кожен образ виходить і як торент, із magnet-посиланням поруч, а роздає його наша машина, яка працює цілодобово. Дзеркала лишаються всередині торента запасним джерелом HTTP, тож звантаження почнеться навіть тоді, коли більше ніхто не роздає. Із SourceForge у Європі виходило близько 250 кБ/с: для образу на 4,7 ГБ саме це змушувало відмовитися.",
    },
  },
  {
    stato: 'corso',
    titolo: {
      it: "Guida all'installazione con le immagini, in quattro lingue",
      en: 'Installation guide with screenshots, in four languages',
      pl: 'Przewodnik instalacji ze zrzutami ekranu, w czterech językach',
      uk: 'Посібник зі встановлення зі знімками екрана, чотирма мовами',
    },
    testo: {
      it: "Una guida passo passo con le schermate vere dell'installer, rifatte per ogni lingua: l'interfaccia cambia, quindi non basta tradurre le didascalie. Chi installa per la prima volta vede esattamente quello che ha davanti, nella sua lingua.",
      en: "A step-by-step guide with real installer screenshots, reshot for every language: the interface changes, so translating the captions is not enough. A first-time installer sees exactly what is in front of them, in their own language.",
      pl: "Przewodnik krok po kroku z prawdziwymi zrzutami instalatora, robionymi od nowa dla każdego języka: interfejs się zmienia, więc przetłumaczenie podpisów nie wystarczy. Kto instaluje pierwszy raz, widzi dokładnie to, co ma przed sobą, we własnym języku.",
      uk: "Покроковий посібник зі справжніми знімками встановлювача, зробленими окремо для кожної мови: інтерфейс змінюється, тож перекласти самі підписи замало. Той, хто встановлює вперше, бачить саме те, що перед ним, своєю мовою.",
    },
  },
  {
    stato: 'previsto',
    titolo: {
      it: 'Gestione degli snapshot con una finestra',
      en: 'Snapshot management in a window',
      pl: 'Zarządzanie migawkami w oknie',
      uk: 'Керування знімками у вікні',
    },
    testo: {
      it: "Btrfs Assistant è già dentro il sistema: va messo nel menu, vestito col tema e tradotto, così elencare, creare e ripristinare uno snapshot non richiede il terminale. Chi preferisce la riga di comando continua a usare <code>skillfish-rollback</code>.",
      en: "Btrfs Assistant already ships with the system: it needs to be in the menu, themed and translated, so that listing, creating and restoring a snapshot needs no terminal. Anyone who prefers the command line keeps <code>skillfish-rollback</code>.",
      pl: "Btrfs Assistant jest już w systemie: trzeba go dodać do menu, ubrać w motyw i przetłumaczyć, żeby wypisanie, utworzenie i przywrócenie migawki nie wymagało terminala. Kto woli wiersz poleceń, dalej ma <code>skillfish-rollback</code>.",
      uk: "Btrfs Assistant уже є в системі: його треба додати до меню, вдягнути в тему й перекласти, щоб переглянути, створити та відновити знімок можна було без термінала. Хто надає перевагу командному рядку, і далі має <code>skillfish-rollback</code>.",
    },
  },
  {
    stato: 'previsto',
    titolo: {
      it: 'Streaming dei giochi con Sunshine',
      en: 'Game streaming with Sunshine',
      pl: 'Strumieniowanie gier przez Sunshine',
      uk: 'Трансляція ігор через Sunshine',
    },
    testo: {
      it: 'Giocare da un altro dispositivo, con la scheda che lavora in un angolo della casa. Il modulo è previsto nel pannello di controllo remoto, che già gestisce schermo, terminale e AI.',
      en: 'Play from another device while the board works away in a corner of the house. The module is planned for the remote panel, which already handles screen, terminal and AI.',
      pl: "Granie z innego urządzenia, podczas gdy płyta pracuje w kącie mieszkania. Moduł jest planowany w panelu zdalnym, który obsługuje już ekran, terminal i AI.",
      uk: "Гра з іншого пристрою, поки плата працює десь у кутку помешкання. Модуль заплановано у віддаленій панелі, яка вже дає екран, термінал і ШІ.",
    },
  },
  {
    stato: 'previsto',
    titolo: {
      it: 'Giochi su un disco esterno',
      en: 'Games on an external drive',
      pl: 'Gry na dysku zewnętrznym',
      uk: 'Ігри на зовнішньому диску',
    },
    testo: {
      it: "Un selettore per installare i giochi su un SSD USB invece che sul disco di sistema. Steam arriva come Flatpak, quindi non basta cambiare cartella: serve dare il permesso giusto al contenitore, ed è proprio il pezzo che vogliamo togliere di mezzo all'utente.",
      en: "A selector to install games on a USB SSD instead of the system disk. Steam ships as a Flatpak, so changing folder is not enough: the container needs the right permission, and that is exactly the part we want to take off the user's hands.",
      pl: "Wybór, żeby instalować gry na dysku SSD po USB zamiast na dysku systemowym. Steam jest Flatpakiem, więc zmiana katalogu nie wystarczy: kontener potrzebuje odpowiedniego uprawnienia — i właśnie tę część chcemy zdjąć z głowy użytkownikowi.",
      uk: "Перемикач, щоб встановлювати ігри на SSD через USB, а не на системний диск. Steam постачається як Flatpak, тож змінити теку замало: контейнерові потрібен відповідний дозвіл — і саме цю частину ми хочемо зняти з користувача.",
    },
  },
  {
    stato: 'previsto',
    titolo: {
      it: 'HUD configurabile e curva della ventola',
      en: 'Configurable HUD and fan curve',
      pl: 'Konfigurowalny HUD i krzywa wentylatora',
      uk: 'Налаштовний HUD і крива вентилятора',
    },
    testo: {
      it: "Il pannello a schermo oggi è tarato sulla BC-250 e su altre macchine si nasconde. Diventerà un'applicazione che legge i sensori davvero presenti e si costruisce la configurazione da sola. Insieme arriva l'editor della curva della ventola dentro il Tuner.",
      en: "The on-screen panel is tuned for the BC-250 today and hides itself on other machines. It will become an application that reads the sensors actually present and builds its own configuration. The fan curve editor lands in the Tuner alongside it.",
      pl: "Panel na ekranie jest dziś dopasowany do BC-250, a na innych maszynach po prostu się chowa. Stanie się aplikacją, która czyta faktycznie obecne czujniki i sama buduje sobie konfigurację. Razem z nim trafi do Tunera edytor krzywej wentylatora.",
      uk: "Екранна панель сьогодні налаштована під BC-250, а на інших машинах просто ховається. Вона стане програмою, яка читає наявні датчики й сама будує собі конфігурацію. Разом із нею в Tuner з'явиться редактор кривої вентилятора.",
    },
  },
  {
    stato: 'previsto',
    titolo: {
      it: "Revisione dell'ucraino da un madrelingua",
      en: 'Ukrainian reviewed by a native speaker',
      pl: 'Ukraiński przejrzany przez native speakera',
      uk: 'Українська в редакції носія мови',
    },
    testo: {
      it: "Il polacco è stato riletto da un madrelingua, e si vede. Cerchiamo qualcuno che faccia lo stesso con l'ucraino: se è la tua lingua e ti va di darci una mano, sei il benvenuto.",
      en: "Polish was reviewed by a native speaker, and it shows. We are looking for someone to do the same for Ukrainian: if that is your language and you fancy lending a hand, you are welcome.",
      pl: "Polski przejrzał native speaker i widać to od razu. Szukamy kogoś, kto zrobi to samo z ukraińskim: jeśli to twój język i masz ochotę pomóc, zapraszamy.",
      uk: "Польську переглянув носій мови, і це помітно. Шукаємо когось, хто зробить те саме з українською: якщо це ваша мова й маєте охоту допомогти — ласкаво просимо.",
    },
  },
  {
    stato: 'fatto',
    quando: { it: 'agosto 2026', en: 'August 2026', pl: 'sierpień 2026', uk: 'серпень 2026' },
    titolo: {
      it: 'Punti di ripristino, e un comando per tornare indietro',
      en: 'Restore points, and one command to go back',
      pl: 'Punkty przywracania i jedno polecenie, by cofnąć system',
      uk: 'Точки відновлення й одна команда, щоб повернутися',
    },
    testo: {
      it: "Il sistema tiene cinque punti di ripristino, presi da solo prima di ogni aggiornamento, e li mostra nel menu di avvio. Con <code>skillfish-rollback</code> si torna a uno di essi per davvero, in un comando: la cartella personale non viene toccata.",
      en: "The system keeps five restore points, taken by itself before every upgrade, and lists them in the boot menu. <code>skillfish-rollback</code> takes you back to one of them for real, in a single command — your home directory is left alone.",
      pl: "System trzyma pięć punktów przywracania, robionych samoczynnie przed każdą aktualizacją, i pokazuje je w menu startowym. <code>skillfish-rollback</code> naprawdę cofa system do jednego z nich, jednym poleceniem — katalog domowy zostaje nietknięty.",
      uk: "Система тримає п'ять точок відновлення, які створює сама перед кожним оновленням, і показує їх у меню завантаження. <code>skillfish-rollback</code> справді повертає систему до однієї з них, однією командою — домашня тека лишається недоторканою.",
    },
  },
  {
    stato: 'fatto',
    quando: { it: 'agosto 2026', en: 'August 2026', pl: 'sierpień 2026', uk: 'серпень 2026' },
    titolo: {
      it: 'Quattro lingue, con ripiego sempre in inglese',
      en: 'Four languages, always falling back to English',
      pl: 'Cztery języki, zawsze z angielskim jako zapasowym',
      uk: 'Чотири мови, із запасною завжди англійською',
    },
    testo: {
      it: 'Italiano, inglese, polacco e ucraino nelle applicazioni, nella schermata di accesso, nel pannello web e nelle diapositive dell\'installer. E una regola: se una traduzione manca, esce l\'inglese, mai l\'italiano.',
      en: 'Italian, English, Polish and Ukrainian across the applications, the login screen, the web panel and the installer slideshow. Plus a rule: if a translation is missing you get English, never Italian.',
      pl: "Włoski, angielski, polski i ukraiński w aplikacjach, na ekranie logowania, w panelu webowym i w pokazie slajdów instalatora. Do tego zasada: gdy brakuje tłumaczenia, pojawia się angielski, nigdy włoski.",
      uk: "Італійська, англійська, польська та українська — у програмах, на екрані входу, у вебпанелі й у слайдах встановлювача. Плюс правило: якщо перекладу немає, буде англійська, ніколи не італійська.",
    },
  },
  {
    stato: 'fatto',
    quando: { it: 'giugno 2026', en: 'June 2026', pl: 'czerwiec 2026', uk: 'червень 2026' },
    titolo: {
      it: 'Otto core invece di sei',
      en: 'Eight cores instead of six',
      pl: 'Osiem rdzeni zamiast sześciu',
      uk: 'Вісім ядер замість шести',
    },
    testo: {
      it: 'La scheda si presenta come 6 core / 12 thread, ma i due mancanti sono spenti dalla configurazione, non difettosi. SkillFishOS li riaccende all\'avvio: <strong>+20% misurato</strong> sui carichi multi-thread, senza toccare il BIOS.',
      en: 'The board presents itself as 6 cores / 12 threads, but the two missing ones are switched off by configuration, not defective. SkillFishOS turns them back on at boot: <strong>+20% measured</strong> on multi-threaded work, with no BIOS changes.',
      pl: "Płyta przedstawia się jako 6 rdzeni / 12 wątków, ale dwa brakujące są wyłączone konfiguracją, a nie uszkodzone. SkillFishOS włącza je z powrotem przy starcie: <strong>+20% zmierzone</strong> przy obciążeniach wielowątkowych, bez grzebania w BIOS-ie.",
      uk: "Плата подає себе як 6 ядер / 12 потоків, але два відсутні вимкнені конфігурацією, а не несправні. SkillFishOS вмикає їх назад під час запуску: <strong>+20% виміряно</strong> на багатопотокових навантаженнях, без жодних змін у BIOS.",
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
    data: '2026-08-17',
    quando: { it: '17 agosto 2026', en: '17 August 2026', pl: '17 sierpnia 2026', uk: '17 серпня 2026' },
    etichetta: { it: 'release', en: 'release', pl: 'wydanie', uk: 'реліз' },
    titolo: {
      it: 'SkillFishOS 26.06.4 «Aetherium»',
      en: 'SkillFishOS 26.06.4 “Aetherium”',
      pl: 'SkillFishOS 26.06.4 „Aetherium”',
      uk: 'SkillFishOS 26.06.4 «Aetherium»',
    },
    testo: {
      it: "Due difetti potevano impedire all'installazione di arrivare in fondo su una BC-250 vera. Adesso non ci sono più.<br><br>Il primo: lo sblocco degli otto core scriveva la maschera nella SMU e <strong>riavviava la scheda</strong>, anche dentro la sessione live. Se capitava mentre l'installatore stava copiando, l'installazione moriva lì. Adesso lo sblocco è disattivato di partenza e si chiede dal Tuner.<br><br>Il secondo: installando su <strong>Btrfs</strong> il sistema poteva non avviarsi, con <code>error: premature end of file</code> al prompt di GRUB. L'installatore copiava con <code>rsync -aHAXS</code> e il kernel arrivava a destinazione con un buco in coda; su Btrfs un buco non ha extent, e GRUB si ferma lì. Linux quel file lo legge benissimo, ed è per questo che non sembrava esserci niente di storto.<br><br>Corretti anche: il controllo del disco chiedeva 10 GiB quando al sistema ne servono 15, l'edizione BC-250 avviava il kernel <em>generico</em>, e le voci Safe Mode e Text Mode facevano esattamente la stessa cosa della voce normale.<br><br>Le immagini 26.06.x precedenti sono state <strong>sostituite</strong>: se ne hai una, scarica la 26.06.4.",
      en: "Two defects could stop the installation from finishing on a real BC-250. They are gone.<br><br>The first: the eight-core unlock wrote the SMU core mask and <strong>rebooted the board</strong>, including inside the live session. If that landed while the installer was copying, the installation died. The unlock is now off by default and opt-in from the Tuner.<br><br>The second: installing onto <strong>Btrfs</strong> could produce a system that would not boot, with <code>error: premature end of file</code> at the GRUB prompt. The installer copied with <code>rsync -aHAXS</code> and the kernel image landed with a hole at the tail; on Btrfs a hole has no extent, so GRUB stops there. Linux reads that file perfectly, which is why nothing looked wrong.<br><br>Also fixed: the disk check asked for 10 GiB when the system needs 15, the BC-250 edition booted the <em>generic</em> kernel, and Safe Mode and Text Mode did exactly the same thing as the normal boot entry.<br><br>Earlier 26.06.x images have been <strong>superseded</strong>: if you have one, download 26.06.4.",
      pl: "Dwie usterki mogły uniemożliwić dokończenie instalacji na prawdziwym BC-250. Już ich nie ma.<br><br>Pierwsza: odblokowanie ośmiu rdzeni zapisywało maskę rdzeni w SMU i <strong>ponownie uruchamiało płytę</strong> — również w sesji live. Jeśli trafiło to w moment kopiowania plików, instalacja umierała. Teraz odblokowanie jest domyślnie wyłączone i włącza się je z poziomu Tunera.<br><br>Druga: instalacja na <strong>Btrfs</strong> mogła dać system, który się nie uruchamia, z komunikatem <code>error: premature end of file</code> w GRUB-ie. Instalator kopiował przez <code>rsync -aHAXS</code>, a obraz jądra trafiał na dysk z dziurą na końcu; na Btrfs dziura nie ma ekstentu, więc GRUB zatrzymuje się w tym miejscu. Linux czyta ten plik bez problemu — dlatego nic nie wyglądało podejrzanie.<br><br>Poprawione też: instalator wymagał 10 GiB, choć system potrzebuje 15; edycja BC-250 uruchamiała jądro <em>generic</em>; a pozycje Safe Mode i Text Mode robiły dokładnie to samo co zwykły wpis startowy.<br><br>Wcześniejsze obrazy 26.06.x zostały <strong>zastąpione</strong>: jeśli masz któryś z nich, pobierz 26.06.4.",
      uk: "Дві вади могли завадити встановленню дійти до кінця на справжній BC-250. Їх більше немає.<br><br>Перша: розблокування восьми ядер записувало маску ядер у SMU і <strong>перезавантажувало плату</strong> — зокрема й у live-сеансі. Якщо це збігалося з копіюванням файлів, встановлення обривалося. Тепер розблокування типово вимкнене й вмикається з Tuner.<br><br>Друга: встановлення на <strong>Btrfs</strong> могло дати систему, яка не завантажується, з <code>error: premature end of file</code> у GRUB. Встановлювач копіював через <code>rsync -aHAXS</code>, і образ ядра потрапляв на диск із діркою в кінці; на Btrfs дірка не має екстента, тож GRUB зупиняється саме там. Linux читає цей файл бездоганно — тому нічого не виглядало підозрілим.<br><br>Також виправлено: перевірка диска вимагала 10 ГіБ, хоча системі потрібно 15; видання BC-250 завантажувало <em>загальне</em> ядро; а пункти Safe Mode і Text Mode робили те саме, що й звичайний пункт завантаження.<br><br>Попередні образи 26.06.x <strong>замінено</strong>: якщо у вас є котрийсь із них, звантажте 26.06.4.",
    },
  },
  {
    data: '2026-08-11',
    quando: { it: '11 agosto 2026', en: '11 August 2026', pl: '11 sierpnia 2026', uk: '11 серпня 2026' },
    etichetta: { it: 'sostituita', en: 'superseded', pl: 'zastąpione', uk: 'замінено' },
    titolo: {
      it: 'SkillFishOS 26.06.3 «Aetherium»',
      en: 'SkillFishOS 26.06.3 “Aetherium”',
      pl: 'SkillFishOS 26.06.3 „Aetherium”',
      uk: 'SkillFishOS 26.06.3 «Aetherium»',
    },
    testo: {
      it: "<strong>⚠️ Questa immagine è stata sostituita: usa la 26.06.4.</strong> Aveva due difetti che potevano bloccare l'installazione su una BC-250.<br><br>Due edizioni, <strong>BC-250</strong> e <strong>Generic</strong>, per la scheda AMD e per qualsiasi PC o macchina virtuale x86-64.<br><br>La lingua che scegli vale adesso <strong>ovunque</strong>: interfaccia, schermata di accesso, pannello web e anche le diapositive dell'installer, che prima restavano in inglese. Italiano, inglese, polacco e ucraino, e se una traduzione manca esce l'inglese.<br><br>Sotto: kernel <strong>7.1.7</strong> con lo sblocco delle 40 Compute Unit e degli otto core, installazione su Btrfs con punti di ripristino attivi dal primo avvio, e AI locale su GPU. Un'installazione nuova parte con <strong>tutti i servizi a posto</strong>.<br><br>L'edizione <strong>Slim</strong> non esce più come immagine: il kernel slim resta nel repository per chi lo vuole.",
      en: "<strong>⚠️ This image has been superseded: please use 26.06.4.</strong> It had two defects that could stop an installation on a BC-250.<br><br>Two editions, <strong>BC-250</strong> and <strong>Generic</strong>, for the AMD board and for any x86-64 PC or virtual machine.<br><br>The language you choose now applies <strong>everywhere</strong>: interface, login screen, web panel and the installer slideshow too, which used to stay in English. Italian, English, Polish and Ukrainian — and if a translation is missing, you get English.<br><br>Underneath: kernel <strong>7.1.7</strong> with the 40 Compute Unit unlock and the eight-core unlock, Btrfs installs with restore points live from the first boot, and on-device AI on the GPU. A fresh install comes up with <strong>every service healthy</strong>.<br><br>The <strong>Slim</strong> edition is no longer shipped as an image: the slim kernel stays in the repository for anyone who wants it.",
      pl: "<strong>⚠️ Ten obraz został zastąpiony: użyj 26.06.4.</strong> Miał dwie usterki, które mogły zatrzymać instalację na BC-250.<br><br>Dwie edycje, <strong>BC-250</strong> i <strong>Generic</strong>, dla płyty AMD i dla dowolnego peceta lub maszyny wirtualnej x86-64.<br><br>Wybrany język obowiązuje teraz <strong>wszędzie</strong>: interfejs, ekran logowania, panel webowy, a także slajdy instalatora, które wcześniej zostawały po angielsku. Włoski, angielski, polski i ukraiński — a gdy brakuje tłumaczenia, pojawia się angielski.<br><br>Pod spodem: jądro <strong>7.1.7</strong> z odblokowaniem 40 jednostek obliczeniowych i ośmiu rdzeni, instalacja na Btrfs z punktami przywracania działającymi od pierwszego uruchomienia oraz lokalne AI na GPU. Świeża instalacja startuje z <strong>wszystkimi usługami na chodzie</strong>.<br><br>Edycja <strong>Slim</strong> nie wychodzi już jako obraz: jądro slim zostaje w repozytorium dla chętnych.",
      uk: "<strong>⚠️ Цей образ замінено: скористайтеся 26.06.4.</strong> Він мав дві вади, які могли зупинити встановлення на BC-250.<br><br>Два видання, <strong>BC-250</strong> і <strong>Generic</strong>, для плати AMD та для будь-якого ПК чи віртуальної машини x86-64.<br><br>Обрана мова діє тепер <strong>усюди</strong>: інтерфейс, екран входу, вебпанель і навіть слайди встановлювача, які раніше лишалися англійськими. Італійська, англійська, польська та українська — а якщо перекладу бракує, буде англійська.<br><br>Усередині: ядро <strong>7.1.7</strong> з розблокуванням 40 обчислювальних блоків і восьми ядер, встановлення на Btrfs із точками відновлення від першого запуску та локальний ШІ на GPU. Свіже встановлення піднімається з <strong>усіма справними службами</strong>.<br><br>Видання <strong>Slim</strong> більше не виходить образом: ядро slim лишається в репозиторії для охочих.",
    },
  },
  {
    data: '2026-08-11',
    quando: { it: '11 agosto 2026', en: '11 August 2026', pl: '11 sierpnia 2026', uk: '11 серпня 2026' },
    etichetta: { it: 'aggiornamento', en: 'update', pl: 'aktualizacja', uk: 'оновлення' },
    titolo: {
      it: 'Cinque punti di ripristino, e un comando per tornare indietro',
      en: 'Five restore points, and one command to go back',
      pl: 'Pięć punktów przywracania i jedno polecenie, by cofnąć system',
      uk: 'П\'ять точок відновлення й одна команда, щоб повернутися',
    },
    testo: {
      it: "Il sistema si prende cura da solo dei punti di ripristino: ne fa uno <strong>prima</strong> e uno <strong>dopo</strong> ogni operazione di <code>apt</code>, ne tiene <strong>cinque</strong> — tre ordinari e due degli aggiornamenti importanti, quelli che toccano kernel o systemd — e li elenca nel menu di avvio, aggiornato a ogni transazione.<br><br>Dal menu di avvio ci si entra per guardare e recuperare file. Per ripartire davvero da uno di essi c'è un comando nuovo:<br><br><code>sudo skillfish-rollback 12</code><br><br>Al riavvio successivo il sistema è quello di allora. Il sistema di prima non viene cancellato: resta da parte, e <code>--annulla</code> lo rimette al suo posto. La <strong>cartella personale non viene mai toccata</strong>: torna indietro il sistema, i tuoi file restano quelli di adesso.<br><br>Arriva con <code>sudo apt update && sudo apt upgrade</code>, senza reinstallare niente.",
      en: "The system looks after its own restore points: it takes one <strong>before</strong> and one <strong>after</strong> every <code>apt</code> operation, keeps <strong>five</strong> — three ordinary ones and two from the important upgrades, the ones touching the kernel or systemd — and lists them in the boot menu, refreshed on every transaction.<br><br>From the boot menu you go in to look around and rescue files. To actually start again from one of them there is a new command:<br><br><code>sudo skillfish-rollback 12</code><br><br>At the next boot the system is the one from back then. The previous system is not deleted: it is set aside, and <code>--undo</code> puts it back. Your <strong>home directory is never touched</strong>: the system travels back, your files stay as they are.<br><br>It arrives with <code>sudo apt update && sudo apt upgrade</code> — no reinstall needed.",
      pl: "System sam dba o punkty przywracania: robi jeden <strong>przed</strong> i jeden <strong>po</strong> każdej operacji <code>apt</code>, trzyma <strong>pięć</strong> — trzy zwykłe i dwa z ważnych aktualizacji, tych ruszających jądro albo systemd — i wypisuje je w menu startowym, odświeżanym przy każdej transakcji.<br><br>Z menu startowego wchodzi się, żeby rozejrzeć się i uratować pliki. Żeby naprawdę wystartować od nowa z któregoś z nich, jest nowe polecenie:<br><br><code>sudo skillfish-rollback 12</code><br><br>Przy następnym uruchomieniu system jest tym sprzed. Poprzedni system nie zostaje skasowany: leży z boku, a <code>--undo</code> stawia go z powrotem. <strong>Katalog domowy nie jest nigdy ruszany</strong>: cofa się system, twoje pliki zostają takie, jakie są.<br><br>Przychodzi z <code>sudo apt update && sudo apt upgrade</code>, bez żadnej reinstalacji.",
      uk: "Система сама дбає про точки відновлення: створює одну <strong>перед</strong> і одну <strong>після</strong> кожної дії <code>apt</code>, тримає <strong>п'ять</strong> — три звичайні та дві з важливих оновлень, тих, що чіпають ядро або systemd, — і показує їх у меню завантаження, оновлюваному щоразу.<br><br>З меню завантаження заходять, щоб роздивитися і врятувати файли. Щоб справді почати знову з однієї з них, є нова команда:<br><br><code>sudo skillfish-rollback 12</code><br><br>Після наступного запуску система буде тією, що тоді. Попередню систему не вилучають: вона лишається збоку, а <code>--undo</code> повертає її на місце. <strong>Домашню теку не чіпають ніколи</strong>: назад повертається система, ваші файли лишаються теперішніми.<br><br>Приходить із <code>sudo apt update && sudo apt upgrade</code>, без перевстановлення.",
    },
  },
  {
    data: '2026-08-10',
    quando: { it: 'agosto 2026', en: 'August 2026', pl: 'sierpień 2026', uk: 'серпень 2026' },
    etichetta: { it: 'AI', en: 'AI', pl: 'AI', uk: 'ШІ' },
    titolo: {
      it: "L'AI locale passa a Unsloth Studio",
      en: 'On-device AI moves to Unsloth Studio',
      pl: 'Lokalne AI przechodzi na Unsloth Studio',
      uk: 'Локальний ШІ переходить на Unsloth Studio',
    },
    testo: {
      it: "Al posto di tre container Docker c'è <strong>un solo servizio nativo</strong>, con la chat e un'API compatibile OpenAI. Docker non è più installato.<br><br>Sulla scheda, con Qwen3-1.7B: <strong>210 token al secondo</strong> sulla GPU via Vulkan contro 41 sulla sola CPU, cioè cinque volte tanto. I modelli si prendono direttamente dal catalogo di Hugging Face. Il servizio ascolta solo in locale: da fuori ci si arriva attraverso il pannello remoto, che autentica con le credenziali di sistema.",
      en: "Instead of three Docker containers there is now <strong>a single native service</strong>, offering both the chat and an OpenAI-compatible API. Docker is no longer installed.<br><br>On the board, with Qwen3-1.7B: <strong>210 tokens per second</strong> on the GPU over Vulkan against 41 on the CPU alone — five times as fast. Models come straight from the Hugging Face catalogue. The service listens on loopback only: from outside you reach it through the remote panel, which authenticates against the system accounts.",
      pl: "Zamiast trzech kontenerów Dockera jest teraz <strong>jedna natywna usługa</strong>, z czatem i API zgodnym z OpenAI. Dockera nie ma już w systemie.<br><br>Na płycie, z Qwen3-1.7B: <strong>210 tokenów na sekundę</strong> na GPU przez Vulkan wobec 41 na samym procesorze — pięć razy szybciej. Modele bierze się wprost z katalogu Hugging Face. Usługa nasłuchuje tylko lokalnie: z zewnątrz dociera się do niej przez panel zdalny, który uwierzytelnia kontami systemowymi.",
      uk: "Замість трьох контейнерів Docker тепер <strong>одна нативна служба</strong> з чатом і сумісним з OpenAI API. Docker більше не встановлюється.<br><br>На платі з Qwen3-1.7B: <strong>210 токенів на секунду</strong> на GPU через Vulkan проти 41 на самому процесорі — уп'ятеро швидше. Моделі беруться просто з каталогу Hugging Face. Служба слухає лише локально: ззовні до неї дістаються через віддалену панель, яка автентифікує системними обліковими записами.",
    },
  },
  {
    data: '2026-07-11',
    quando: { it: '11 luglio 2026', en: '11 July 2026', pl: '11 lipca 2026', uk: '11 липня 2026' },
    etichetta: { it: 'release', en: 'release', pl: 'wydanie', uk: 'реліз' },
    titolo: {
      it: 'SkillFishOS 26.06.2',
      en: 'SkillFishOS 26.06.2',
      pl: 'SkillFishOS 26.06.2',
      uk: 'SkillFishOS 26.06.2',
    },
    testo: {
      it: 'Immagini rigenerate con le correzioni raccolte dopo il primo mese: lingua della sessione live, AI sulla GPU, gruppi utente. Tre edizioni su SourceForge.',
      en: 'Images rebuilt with the fixes gathered over the first month: live session language, AI on the GPU, user groups. Three editions on SourceForge.',
      pl: "Obrazy zbudowane na nowo z poprawkami zebranymi przez pierwszy miesiąc: język sesji live, AI na GPU, grupy użytkownika. Trzy edycje na SourceForge.",
      uk: "Образи перезібрані з виправленнями, зібраними за перший місяць: мова live-сеансу, ШІ на GPU, групи користувача. Три видання на SourceForge.",
    },
  },
  {
    data: '2026-06-06',
    quando: { it: '6 giugno 2026', en: '6 June 2026', pl: '6 czerwca 2026', uk: '6 червня 2026' },
    etichetta: { it: 'release', en: 'release', pl: 'wydanie', uk: 'реліз' },
    titolo: {
      it: 'La prima release pubblica: 26.06 «Aetherium»',
      en: 'The first public release: 26.06 “Aetherium”',
      pl: 'Pierwsze publiczne wydanie: 26.06 „Aetherium”',
      uk: 'Перший публічний випуск: 26.06 «Aetherium»',
    },
    testo: {
      it: "Una scheda da mining comprata di seconda mano diventa una console-PC pronta all'uso: kernel su misura con lo sblocco delle 40 Compute Unit, governor SMU, profili di overclock con protezione termica, tema steampunk dal boot al desktop, Steam ed emulatori, AI locale.<br><br>Era nato per far usare e imparare Linux ai miei figli mentre giocano. Il gioco è la carota, gli snapshot sono la rete.",
      en: "A second-hand mining board becomes a ready-to-use console-PC: a custom kernel with the 40 Compute Unit unlock, an SMU governor, overclock profiles with a thermal guard, a steampunk theme from boot to desktop, Steam and emulators, on-device AI.<br><br>It started as a way to get my children using and learning Linux while they game. Gaming is the carrot, snapshots are the net.",
      pl: "Kupiona z drugiej ręki płyta do kopania staje się gotową do użytku konsolą-pecetem: własne jądro z odblokowaniem 40 jednostek obliczeniowych, governor SMU, profile podkręcania z zabezpieczeniem termicznym, motyw steampunk od startu po pulpit, Steam i emulatory, lokalne AI.<br><br>Zaczęło się od tego, żeby moje dzieci używały Linuksa i uczyły się go przy graniu. Granie jest marchewką, migawki są siatką.",
      uk: "Вживана майнінгова плата стає готовою до вжитку консоллю-ПК: власне ядро з розблокуванням 40 обчислювальних блоків, governor SMU, профілі розгону з тепловим захистом, тема steampunk від завантаження до стільниці, Steam та емулятори, локальний ШІ.<br><br>Усе почалося з бажання привчити моїх дітей до Linux, поки вони грають. Гра — це морквина, знімки — сітка.",
    },
  },
];

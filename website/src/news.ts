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
    stato: 'fatto',
    titolo: {
      it: 'Il sistema nella lingua di chi lo usa',
      en: 'The system in the language of the people using it',
      pl: 'System w języku tych, którzy go używają',
      uk: 'Система мовою тих, хто нею користується',
      ru: 'Система на языке тех, кто ею пользуется',
      es: 'El sistema en el idioma de quien lo usa',
      pt: "O sistema no idioma de quem usa",
      de: "Das System in der Sprache derer, die es benutzen",
      fr: "Le système dans la langue de ceux qui s'en servent"
    },
    testo: {
      it: "Finora SkillFishOS parlava quattro lingue: italiano, inglese, polacco e ucraino. I download raccontano un'altra storia — negli ultimi trenta giorni Russia e Spagna insieme valgono quasi un terzo di chi scarica, con il Brasile subito dietro. Abbiamo aggiunto <strong>russo, spagnolo, portoghese brasiliano, tedesco e francese</strong>: applicazioni, installatore, schermata di accesso, voci di menu, pannello remoto e sito. Il francese non arriva dai numeri — la Francia non e' nella nostra classifica — ed e' proprio il motivo per cui c'e': da un paese la cui lingua il sito non parla non arriva nessuno, quindi leggere solo i download conferma per sempre le lingue che si hanno gia'. Le traduzioni sono uscite dal codice e vivono in un file per lingua, cosi' chi vuole correggerne una manda <strong>un file solo</strong> invece di modificare sei sorgenti che non ha mai visto. Il polacco l'ha scritto Cyryl Sochacki; per le lingue nuove non abbiamo madrelingua, quindi sono segnate come da rivedere e le correzioni sono benvenute.",
      en: "Until now SkillFishOS spoke four languages: Italian, English, Polish and Ukrainian. The downloads tell a different story — over the last thirty days Russia and Spain together account for nearly a third of them, with Brazil close behind. We have added <strong>Russian, Spanish, Brazilian Portuguese, German and French</strong>: applications, installer, login screen, menu entries, remote panel and website. French does not come from the numbers — France is not in our ranking — and that is exactly why it is here: nobody arrives from a country whose language the site does not speak, so reading the downloads alone only ever confirms the languages you already have. Translations have moved out of the code into one file per language, so anyone who wants to fix one sends <strong>a single file</strong> instead of editing six sources they have never seen. The Polish was written by Cyryl Sochacki; for the new languages we have no native speakers, so they are marked as needing review and corrections are welcome.",
      pl: "Do tej pory SkillFishOS mówił czterema językami: po włosku, angielsku, polsku i ukraińsku. Pobrania mówią co innego — w ciągu ostatnich trzydziestu dni Rosja i Hiszpania razem to prawie jedna trzecia, tuż za nimi Brazylia. Dodaliśmy <strong>rosyjski, hiszpański, portugalski brazylijski, niemiecki i francuski</strong>: aplikacje, instalator, ekran logowania, pozycje menu, panel zdalny i stronę. Francuski nie wynika z liczb — Francji nie ma w naszym zestawieniu — i właśnie dlatego tu jest: z kraju, którego języka strona nie zna, nikt nie przychodzi, więc samo czytanie pobrań na zawsze potwierdza języki, które już się ma. Tłumaczenia wyszły z kodu i mieszkają w jednym pliku na język, więc kto chce poprawić jedno z nich, wysyła <strong>jeden plik</strong>, zamiast zmieniać sześć źródeł, których nigdy nie widział. Polski napisał Cyryl Sochacki; dla nowych języków nie mamy rodzimych użytkowników, więc są oznaczone jako do sprawdzenia, a poprawki są mile widziane.",
      uk: "Досі SkillFishOS говорив чотирма мовами: італійською, англійською, польською та українською. Завантаження свідчать про інше — за останні тридцять днів Росія та Іспанія разом дають майже третину, одразу за ними Бразилія. Ми додали <strong>російську, іспанську, бразильську португальську, німецьку та французьку</strong>: програми, встановлювач, екран входу, пункти меню, віддалену панель і сайт. Французька не випливає з чисел — Франції немає в нашому переліку — і саме тому вона тут: із країни, мовою якої сайт не говорить, не приходить ніхто, тож саме читання завантажень назавжди підтверджує ті мови, які вже є. Переклади вийшли з коду й живуть в одному файлі на мову, тож той, хто хоче виправити один із них, надсилає <strong>один файл</strong>, а не змінює шість джерел, яких ніколи не бачив. Польську написав Cyryl Sochacki; для нових мов у нас немає носіїв, тому вони позначені як такі, що потребують перегляду, і виправлення вітаються.",
      ru: "До сих пор SkillFishOS говорил на четырёх языках: итальянском, английском, польском и украинском. Загрузки говорят об ином — за последние тридцать дней Россия и Испания вместе дают почти треть, сразу за ними Бразилия. Мы добавили <strong>русский, испанский, бразильский португальский, немецкий и французский</strong>: приложения, установщик, экран входа, пункты меню, удалённую панель и сайт. Французский не следует из чисел — Франции нет в нашем списке — и именно поэтому он здесь: из страны, на языке которой сайт не говорит, не приходит никто, так что одно лишь чтение загрузок навсегда подтверждает те языки, которые уже есть. Переводы вышли из кода и живут в одном файле на язык, так что желающий поправить один из них присылает <strong>один файл</strong>, а не правит шесть исходников, которых никогда не видел. Польский написал Cyryl Sochacki; для новых языков у нас нет носителей, поэтому они помечены как требующие проверки, и исправления приветствуются.",
      es: "Hasta ahora SkillFishOS hablaba cuatro idiomas: italiano, inglés, polaco y ucraniano. Las descargas cuentan otra cosa — en los últimos treinta días Rusia y España juntas suman casi un tercio, con Brasil justo detrás. Hemos añadido <strong>ruso, español, portugués brasileño, alemán y francés</strong>: aplicaciones, instalador, pantalla de acceso, entradas de menú, panel remoto y sitio web. El francés no sale de los números — Francia no está en nuestra clasificación — y ése es justo el motivo de que esté: de un país cuyo idioma el sitio no habla no llega nadie, así que leer sólo las descargas confirma para siempre los idiomas que ya se tienen. Las traducciones han salido del código y viven en un archivo por idioma, así quien quiera corregir una manda <strong>un solo archivo</strong> en vez de tocar seis fuentes que nunca ha visto. El polaco lo escribió Cyryl Sochacki; para los idiomas nuevos no tenemos hablantes nativos, así que están marcados como pendientes de revisión y las correcciones son bienvenidas.",
      pt: "Até agora o SkillFishOS falava quatro idiomas: italiano, inglês, polonês e ucraniano. Os downloads contam outra coisa — nos últimos trinta dias a Rússia e a Espanha juntas somam quase um terço, com o Brasil logo atrás. Acrescentamos <strong>russo, espanhol, português brasileiro, alemão e francês</strong>: aplicativos, instalador, tela de acesso, itens de menu, painel remoto e site. O francês não vem dos números — a França não está na nossa classificação — e é justamente por isso que ele está aqui: de um país cujo idioma o site não fala não chega ninguém, então ler só os downloads confirma para sempre os idiomas que já se tem. As traduções saíram do código e vivem num arquivo por idioma, então quem quiser corrigir uma manda <strong>um arquivo só</strong> em vez de mexer em seis fontes que nunca viu. O polonês foi escrito por Cyryl Sochacki; para os idiomas novos não temos falantes nativos, então estão marcados como pendentes de revisão e as correções são bem-vindas.",
      de: "Bisher sprach SkillFishOS vier Sprachen: Italienisch, Englisch, Polnisch und Ukrainisch. Die Downloads erzählen etwas anderes — in den letzten dreißig Tagen machen Russland und Spanien zusammen fast ein Drittel aus, Brasilien folgt dicht dahinter. Wir haben <strong>Russisch, Spanisch, brasilianisches Portugiesisch, Deutsch und Französisch</strong> hinzugefügt: Anwendungen, Installationsprogramm, Anmeldebildschirm, Menüeinträge, Fernsteuerung und Website. Französisch kommt nicht aus den Zahlen — Frankreich steht nicht in unserer Liste — und genau darum ist es dabei: aus einem Land, dessen Sprache die Website nicht spricht, kommt niemand, also bestätigt das bloße Lesen der Downloads für immer die Sprachen, die man schon hat. Die Übersetzungen sind aus dem Code herausgewandert und leben in einer Datei je Sprache, sodass jemand, der eine davon verbessern möchte, <strong>eine einzige Datei</strong> schickt, statt sechs Quelldateien zu ändern, die er nie gesehen hat. Das Polnische stammt von Cyryl Sochacki; für die neuen Sprachen haben wir keine Muttersprachler, deshalb sind sie als prüfbedürftig gekennzeichnet, und Korrekturen sind willkommen.",
      fr: "Jusqu'ici SkillFishOS parlait quatre langues : italien, anglais, polonais et ukrainien. Les téléchargements racontent autre chose — sur les trente derniers jours la Russie et l'Espagne réunies pèsent près d'un tiers, le Brésil juste derrière. Nous avons ajouté <strong>le russe, l'espagnol, le portugais brésilien, l'allemand et le français</strong> : applications, installateur, écran de connexion, entrées de menu, panneau à distance et site. Le français ne sort pas des chiffres — la France n'est pas dans notre classement — et c'est justement pour cela qu'il est là : d'un pays dont le site ne parle pas la langue, il n'arrive personne, si bien que lire les seuls téléchargements confirme pour toujours les langues qu'on a déjà. Les traductions sont sorties du code et vivent dans un fichier par langue, si bien que celui qui veut en corriger une envoie <strong>un seul fichier</strong> au lieu de modifier six sources qu'il n'a jamais vues. Le polonais a été écrit par Cyryl Sochacki ; pour les langues nouvelles nous n'avons pas de locuteurs natifs, elles sont donc marquées comme à relire, et les corrections sont les bienvenues."
    },
  },
  {
    stato: 'corso',
    titolo: {
      it: 'Ogni immagine provata su una scheda vera prima di uscire',
      en: 'Every image tested on real hardware before it ships',
      pl: 'Każdy obraz sprawdzony na prawdziwej płycie przed wydaniem',
      uk: 'Кожен образ перевірено на справжній платі перед випуском',
      ru: "Каждый образ проверен на настоящей плате перед выпуском",
      es: "Cada imagen probada en una placa real antes de salir",
      pt: "Cada imagem testada numa placa de verdade antes de sair",
      de: "Jedes Abbild auf einer echten Platine geprüft, bevor es erscheint",
      fr: "Chaque image essayée sur du vrai matériel avant de sortir"
    },
    testo: {
      it: "Le due falle che potevano bloccare l'installazione della 26.06.3 le ha trovate chi ha installato su una BC-250 vera, non noi: in macchina virtuale erano <strong>invisibili per costruzione</strong>, perché il pezzo di codice che rompe l'hardware è proprio quello che una macchina virtuale non può eseguire. Da qui in avanti nessuna immagine esce senza un'installazione completa su una scheda vera, e la costruzione si rifiuta di produrre un'immagine se un controllo non passa.",
      en: "The two defects that could stop a 26.06.3 installation were found by someone installing on a real BC-250, not by us: in a virtual machine they were <strong>invisible by construction</strong>, because the code that breaks the hardware is exactly what a virtual machine cannot execute. From here on no image ships without a full install on a real board, and the build refuses to produce an image when a check fails.",
      pl: "Dwie usterki, które mogły zatrzymać instalację 26.06.3, znalazł ktoś instalujący na prawdziwym BC-250, a nie my: w maszynie wirtualnej były <strong>niewidoczne z założenia</strong>, bo kod psujący sprzęt to dokładnie ten, którego maszyna wirtualna nie potrafi wykonać. Od tej pory żaden obraz nie wychodzi bez pełnej instalacji na prawdziwej płycie, a budowanie odmawia stworzenia obrazu, gdy któraś kontrola nie przejdzie.",
      uk: "Дві вади, які могли зупинити встановлення 26.06.3, знайшов той, хто встановлював на справжню BC-250, а не ми: у віртуальній машині вони були <strong>невидимі за побудовою</strong>, бо код, що ламає залізо, — саме той, який віртуальна машина виконати не може. Відтепер жоден образ не виходить без повного встановлення на справжній платі, а збирання відмовляється створювати образ, якщо якась перевірка не проходить.",
      ru: "Две неполадки, которые могли остановить установку 26.06.3, нашёл тот, кто ставил систему на настоящую BC-250, а не мы: в виртуальной машине они были <strong>невидимы по построению</strong>, потому что код, ломающий железо, — это ровно тот код, который виртуальная машина выполнить не может. Отныне ни один образ не выходит без полной установки на настоящую плату, а сборка отказывается делать образ, если хоть одна проверка не прошла.",
      es: "Los dos fallos que podían detener la instalación de la 26.06.3 los encontró alguien que instalaba en una BC-250 real, no nosotros: en una máquina virtual eran <strong>invisibles por construcción</strong>, porque el código que rompe el hardware es justo el que una máquina virtual no puede ejecutar. A partir de ahora ninguna imagen sale sin una instalación completa en una placa real, y la compilación se niega a producir una imagen si alguna comprobación falla.",
      pt: "As duas falhas que podiam travar a instalação da 26.06.3 foram encontradas por quem instalou numa BC-250 de verdade, não por nós: numa máquina virtual elas eram <strong>invisíveis por construção</strong>, porque o código que quebra o hardware é justamente o que uma máquina virtual não consegue executar. Daqui em diante nenhuma imagem sai sem uma instalação completa numa placa real, e a compilação se recusa a produzir uma imagem quando alguma verificação falha.",
      de: "Die beiden Fehler, die eine Installation von 26.06.3 stoppen konnten, hat jemand gefunden, der auf einer echten BC-250 installiert hat, nicht wir: in einer virtuellen Maschine waren sie <strong>von vornherein unsichtbar</strong>, weil genau der Code, der die Hardware lahmlegt, in einer virtuellen Maschine nicht ausgeführt werden kann. Von jetzt an erscheint kein Abbild ohne eine vollständige Installation auf einer echten Platine, und der Bauvorgang weigert sich, ein Abbild zu erzeugen, wenn eine Prüfung fehlschlägt.",
      fr: "Les deux défauts qui pouvaient arrêter une installation de la 26.06.3 ont été trouvés par quelqu'un qui installait sur une vraie BC-250, pas par nous : dans une machine virtuelle ils étaient <strong>invisibles par construction</strong>, parce que le code qui casse le matériel est exactement celui qu'une machine virtuelle ne peut pas exécuter. Désormais aucune image ne sort sans une installation complète sur une vraie carte, et la fabrication refuse de produire une image quand un contrôle échoue."
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
      ru: "Весь код опубликован, включая ту часть, которой не видно",
      es: "Todo el código publicado, también la parte que no se ve",
      pt: "Todo o código publicado, inclusive a parte que ninguém vê",
      de: "Der ganze Code veröffentlicht, auch der Teil, den niemand sieht",
      fr: "Tout le code publié, y compris la partie que personne ne voit"
    },
    testo: {
      it: "Non solo le applicazioni: adesso è pubblica anche l'infrastruttura che trasforma una compilazione in qualcosa che si può installare — il repository apt firmato, il caricamento sui mirror, le statistiche, la pubblicazione del sito. Nessuno di quegli script contiene una credenziale: le leggono da file che restano fuori dal repository, e accanto ci sono i modelli da riempire. Chi vuole rifare la stessa catena a casa propria adesso può.",
      en: "Not just the applications: the infrastructure that turns a build into something installable is public too — the signed apt repository, the upload to the mirrors, the statistics, the website deploy. None of those scripts contains a credential: they read files that stay out of the repository, and the templates to fill in sit next to them. Anyone who wants to rebuild the same chain at home now can.",
      pl: "Nie tylko aplikacje: publiczna jest teraz także infrastruktura, która zmienia kompilację w coś, co da się zainstalować — podpisane repozytorium apt, wysyłka na serwery lustrzane, statystyki, publikacja strony. Żaden z tych skryptów nie zawiera danych logowania: czytają je z plików, które zostają poza repozytorium, a obok leżą wzorce do wypełnienia. Kto chce odtworzyć ten sam łańcuch u siebie, teraz może.",
      uk: "Не лише програми: тепер публічна й інфраструктура, яка перетворює збірку на щось, що можна встановити, — підписаний репозиторій apt, вивантаження на дзеркала, статистика, публікація сайту. Жоден із цих скриптів не містить облікових даних: вони читають файли, які лишаються поза репозиторієм, а поруч є шаблони для заповнення. Хто хоче відтворити той самий ланцюг у себе — тепер може.",
      ru: "Не только программы: теперь публична и инфраструктура, которая превращает сборку в то, что можно установить, — подписанный репозиторий apt, выгрузка на зеркала, статистика, публикация сайта. Ни в одном из этих скриптов нет учётных данных: они читают файлы, которые остаются вне репозитория, а рядом лежат шаблоны для заполнения. Кто хочет повторить ту же цепочку у себя, теперь может.",
      es: "No solo las aplicaciones: ahora también es pública la infraestructura que convierte una compilación en algo instalable — el repositorio apt firmado, la subida a los espejos, las estadísticas, la publicación de la web. Ninguno de esos scripts contiene credenciales: leen archivos que quedan fuera del repositorio, y al lado están las plantillas para rellenar. Quien quiera rehacer la misma cadena en su casa, ahora puede.",
      pt: "Não só os aplicativos: agora também é pública a infraestrutura que transforma uma compilação em algo instalável — o repositório apt assinado, o envio aos espelhos, as estatísticas, a publicação do site. Nenhum desses scripts contém credenciais: eles leem arquivos que ficam fora do repositório, e ao lado estão os modelos para preencher. Quem quiser refazer a mesma cadeia em casa, agora pode.",
      de: "Nicht nur die Anwendungen: Jetzt ist auch die Infrastruktur öffentlich, die aus einem Bauvorgang etwas Installierbares macht — die signierte apt-Paketquelle, das Hochladen auf die Spiegelserver, die Statistik, die Veröffentlichung der Website. Keines dieser Skripte enthält Zugangsdaten: Sie lesen Dateien, die außerhalb des Repositorys bleiben, und daneben liegen die Vorlagen zum Ausfüllen. Wer dieselbe Kette bei sich zu Hause nachbauen will, kann das jetzt.",
      fr: "Pas seulement les applications : l'infrastructure qui transforme une compilation en quelque chose d'installable est publique elle aussi — le dépôt apt signé, l'envoi vers les miroirs, les statistiques, la publication du site. Aucun de ces scripts ne contient d'identifiant : ils lisent des fichiers qui restent hors du dépôt, et les modèles à remplir sont juste à côté. Qui veut refaire la même chaîne chez lui peut maintenant le faire."
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
      ru: "Выпуск 26.12 на Debian trixie + backports",
      es: "Versión 26.12 sobre Debian trixie + backports",
      pt: "Versão 26.12 sobre Debian trixie + backports",
      de: "Version 26.12 auf Debian trixie + Backports",
      fr: "Version 26.12 sur Debian trixie + backports"
    },
    testo: {
      it: "La base passa da <strong>sid</strong> a <strong>trixie (stable)</strong> con i backports: sistema stabile, kernel e grafica recenti dove servono. È la risposta alla critica più fondata che ci hanno fatto — sid dà il software più nuovo ma può rompersi, e su una console di casa questo pesa.",
      en: "The base moves from <strong>sid</strong> to <strong>trixie (stable)</strong> plus backports: a stable system with a recent kernel and graphics where it matters. This answers the fairest criticism we have had — sid gives you the newest software but it can break, and on a home console that hurts.",
      pl: "Podstawa przechodzi z <strong>sid</strong> na <strong>trixie (stable)</strong> z backportami: stabilny system, a świeże jądro i grafika tam, gdzie to naprawdę ma znaczenie. To odpowiedź na najbardziej trafny zarzut, jaki usłyszeliśmy — sid daje najnowsze oprogramowanie, ale potrafi się popsuć, a na domowej konsoli to boli.",
      uk: "Основа переходить із <strong>sid</strong> на <strong>trixie (stable)</strong> з backports: стабільна система, а свіже ядро та графіка там, де це справді потрібно. Це відповідь на найсправедливіший закид, який ми чули — sid дає найновіше програмне забезпечення, але може зламатися, а на домашній консолі це болить.",
      ru: "Основа переезжает с <strong>sid</strong> на <strong>trixie (стабильную)</strong> плюс backports: стабильная система со свежим ядром и графикой там, где это важно. Это ответ на самую справедливую критику в наш адрес — в sid софт новее, но система может сломаться, а на домашней консоли это больно.",
      es: "La base pasa de <strong>sid</strong> a <strong>trixie (estable)</strong> más backports: un sistema estable con núcleo y gráficos recientes donde importa. Esto responde a la crítica más justa que nos han hecho — sid trae el software más nuevo pero puede romperse, y en una consola de casa eso duele.",
      pt: "A base sai do <strong>sid</strong> e passa para o <strong>trixie (estável)</strong> mais backports: um sistema estável com kernel e gráficos recentes onde importa. Isso responde à crítica mais justa que recebemos — o sid traz o software mais novo, mas pode quebrar, e num console de casa isso dói.",
      de: "Die Basis wechselt von <strong>sid</strong> auf <strong>trixie (stabil)</strong> plus Backports: ein stabiles System mit aktuellem Kernel und aktueller Grafik dort, wo es zählt. Das ist die Antwort auf die berechtigtste Kritik, die wir bekommen haben — sid liefert die neueste Software, kann aber kaputtgehen, und auf einer Konsole zu Hause tut das weh.",
      fr: "La base passe de <strong>sid</strong> à <strong>trixie (stable)</strong> plus les backports : un système stable avec un noyau et une partie graphique récents là où cela compte. C'est la réponse à la critique la plus juste qu'on nous ait faite — sid donne les logiciels les plus récents mais peut casser, et sur une console de salon cela fait mal."
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
      ru: "Загрузка через торрент",
      es: "Descargas por torrent",
      pt: "Downloads por torrent",
      de: "Downloads per Torrent",
      fr: "Téléchargement par torrent"
    },
    testo: {
      it: "Fatto: ogni immagine esce anche come torrent, con un magnet accanto, e a seminarla è un nostro server acceso ventiquattro ore su ventiquattro. I mirror restano dentro il torrent come sorgente HTTP di riserva, quindi il download parte comunque anche quando non c'è nessun altro a condividere. Da SourceForge in Europa si scaricava a circa 250 kB/s: per un'immagine da 4,7 GB era la prima cosa che faceva desistere.",
      en: "Done: every image also ships as a torrent, with a magnet link beside it, seeded by a machine of ours that stays up around the clock. The mirrors remain inside the torrent as HTTP fallback sources, so a download starts even when nobody else is sharing. From SourceForge in Europe you got around 250 kB/s: on a 4.7 GB image that was the first thing that made people give up.",
      pl: "Zrobione: każdy obraz wychodzi także jako torrent, z linkiem magnet obok, a rozsiewa go nasza maszyna działająca całą dobę. Serwery lustrzane zostają w torrencie jako zapasowe źródło HTTP, więc pobieranie ruszy nawet wtedy, gdy nikt inny nie udostępnia. Z SourceForge w Europie schodziło około 250 kB/s: przy obrazie 4,7 GB to była pierwsza rzecz, która zniechęcała.",
      uk: "Зроблено: кожен образ виходить і як торент, із magnet-посиланням поруч, а роздає його наша машина, яка працює цілодобово. Дзеркала лишаються всередині торента запасним джерелом HTTP, тож звантаження почнеться навіть тоді, коли більше ніхто не роздає. Із SourceForge у Європі виходило близько 250 кБ/с: для образу на 4,7 ГБ саме це змушувало відмовитися.",
      ru: "Сделано: каждый образ выходит и торрентом, с magnet-ссылкой рядом, а раздаёт его наша машина, которая работает круглые сутки. Зеркала остаются внутри торрента как запасные HTTP-источники, поэтому загрузка начинается, даже когда больше никто не раздаёт. С SourceForge в Европе выходило около 250 кБ/с: на образе в 4,7 ГБ именно это первым заставляло людей бросить.",
      es: "Hecho: cada imagen sale también como torrent, con su enlace magnet al lado, y la comparte una máquina nuestra encendida las veinticuatro horas. Los espejos siguen dentro del torrent como fuentes HTTP de respaldo, así la descarga arranca aunque no haya nadie más compartiendo. Desde SourceForge en Europa se sacaban unos 250 kB/s: en una imagen de 4,7 GB, eso era lo primero que hacía abandonar a la gente.",
      pt: "Feito: cada imagem sai também como torrent, com o link magnet ao lado, semeada por uma máquina nossa que fica ligada o dia inteiro. Os espelhos continuam dentro do torrent como fontes HTTP de reserva, então o download começa mesmo sem mais ninguém compartilhando. Pelo SourceForge na Europa saíam cerca de 250 kB/s: numa imagem de 4,7 GB, era a primeira coisa que fazia as pessoas desistirem.",
      de: "Erledigt: Jedes Abbild erscheint auch als Torrent, mit einem Magnet-Link daneben, verteilt von einer Maschine von uns, die rund um die Uhr läuft. Die Spiegelserver bleiben als HTTP-Reserve im Torrent enthalten, sodass ein Download auch dann startet, wenn sonst niemand teilt. Von SourceForge kamen in Europa etwa 250 kB/s an: bei einem Abbild von 4,7 GB war das das Erste, was die Leute aufgeben ließ.",
      fr: "Fait : chaque image sort aussi en torrent, avec un lien magnet à côté, semée par une de nos machines qui reste allumée jour et nuit. Les miroirs restent dans le torrent comme sources HTTP de secours, si bien qu'un téléchargement démarre même quand personne d'autre ne partage. Depuis SourceForge en Europe on tournait autour de 250 ko/s : sur une image de 4,7 Go, c'était la première chose qui faisait abandonner."
    },
  },
  {
    stato: 'corso',
    titolo: {
      it: "Guida all'installazione con le immagini, in quattro lingue",
      en: 'Installation guide with screenshots, in four languages',
      pl: 'Przewodnik instalacji ze zrzutami ekranu, w czterech językach',
      uk: 'Посібник зі встановлення зі знімками екрана, чотирма мовами',
      ru: "Руководство по установке со снимками экрана, на четырёх языках",
      es: "Guía de instalación con capturas, en cuatro idiomas",
      pt: "Guia de instalação com capturas, em quatro idiomas",
      de: "Installationsanleitung mit Bildschirmfotos, in vier Sprachen",
      fr: "Guide d'installation en images, en quatre langues"
    },
    testo: {
      it: "Una guida passo passo con le schermate vere dell'installer, rifatte per ogni lingua: l'interfaccia cambia, quindi non basta tradurre le didascalie. Chi installa per la prima volta vede esattamente quello che ha davanti, nella sua lingua.",
      en: "A step-by-step guide with real installer screenshots, reshot for every language: the interface changes, so translating the captions is not enough. A first-time installer sees exactly what is in front of them, in their own language.",
      pl: "Przewodnik krok po kroku z prawdziwymi zrzutami instalatora, robionymi od nowa dla każdego języka: interfejs się zmienia, więc przetłumaczenie podpisów nie wystarczy. Kto instaluje pierwszy raz, widzi dokładnie to, co ma przed sobą, we własnym języku.",
      uk: "Покроковий посібник зі справжніми знімками встановлювача, зробленими окремо для кожної мови: інтерфейс змінюється, тож перекласти самі підписи замало. Той, хто встановлює вперше, бачить саме те, що перед ним, своєю мовою.",
      ru: "Пошаговое руководство с настоящими снимками установщика, переснятыми для каждого языка: интерфейс меняется, поэтому перевести подписи недостаточно. Тот, кто ставит систему впервые, видит ровно то, что у него перед глазами, и на своём языке.",
      es: "Una guía paso a paso con capturas reales del instalador, rehechas para cada idioma: la interfaz cambia, así que traducir los pies de foto no basta. Quien instala por primera vez ve exactamente lo que tiene delante, y en su idioma.",
      pt: "Um guia passo a passo com capturas reais do instalador, refeitas para cada idioma: a interface muda, então traduzir as legendas não basta. Quem instala pela primeira vez vê exatamente o que está na frente dele, e no próprio idioma.",
      de: "Eine Schritt-für-Schritt-Anleitung mit echten Bildschirmfotos des Installationsprogramms, für jede Sprache neu aufgenommen: die Oberfläche ändert sich, also reicht es nicht, die Bildunterschriften zu übersetzen. Wer zum ersten Mal installiert, sieht genau das, was vor ihm liegt, und zwar in seiner Sprache.",
      fr: "Un guide pas à pas avec de vraies captures de l'installateur, reprises pour chaque langue : l'interface change, traduire les légendes ne suffit pas. Celui qui installe pour la première fois voit exactement ce qu'il a devant lui, dans sa langue."
    },
  },
  {
    stato: 'fatto',
    titolo: {
      it: 'Gestione degli snapshot con una finestra',
      en: 'Snapshot management in a window',
      pl: 'Zarządzanie migawkami w oknie',
      uk: 'Керування знімками у вікні',
      ru: "Управление снимками в окне",
      es: "Gestión de instantáneas en una ventana",
      pt: "Gerenciamento de snapshots numa janela",
      de: "Schnappschüsse in einem Fenster verwalten",
      fr: "La gestion des instantanés dans une fenêtre"
    },
    testo: {
      it: "L'abbiamo scritta noi. Btrfs Assistant è un buon programma, ma parla la lingua del filesystem: sottovolumi, qgroup, configurazioni di snapper, schede separate. Chi vuole solo tornare a ieri sera perché un aggiornamento ha rotto qualcosa deve prima imparare tutto quello. <strong>SkillFishOS Snapshot</strong> risponde a tre domande e basta: che snapshot ho, fammene uno adesso, riportami lì. Chi preferisce la riga di comando continua a usare <code>skillfish-rollback</code>.",
      en: "We wrote our own. Btrfs Assistant is a good program, but it speaks the language of the filesystem: subvolumes, qgroups, snapper configurations, separate tabs. Someone who just wants to go back to last night because an update broke something has to learn all of that first. <strong>SkillFishOS Snapshots</strong> answers three questions and stops there: which snapshots do I have, make me one now, take me back to that one. Anyone who prefers the command line keeps <code>skillfish-rollback</code>.",
      pl: "Napisaliśmy własną. Btrfs Assistant to dobry program, ale mówi językiem systemu plików: podwoluminy, qgroup, konfiguracje snappera, osobne zakładki. Kto chce tylko wrócić do wczorajszego wieczoru, bo aktualizacja coś zepsuła, musi się tego wszystkiego najpierw nauczyć. <strong>SkillFishOS Migawki</strong> odpowiada na trzy pytania i na tym koniec: jakie mam migawki, zrób mi jedną teraz, cofnij mnie do tamtej. Kto woli wiersz poleceń, dalej ma <code>skillfish-rollback</code>.",
      uk: "Ми написали власний. Btrfs Assistant — добра програма, але говорить мовою файлової системи: підтоми, qgroup, конфігурації snapper, окремі вкладки. Той, хто просто хоче повернутися до вчорашнього вечора, бо оновлення щось зламало, мусить спершу все це вивчити. <strong>SkillFishOS Знімки</strong> відповідає на три питання й на тому спиняється: які знімки я маю, зроби один зараз, поверни мене до того. Хто надає перевагу командному рядку, і далі має <code>skillfish-rollback</code>.",
      ru: "Мы написали своё. Btrfs Assistant — хорошая программа, но говорит на языке файловой системы: подтома, qgroup, конфигурации snapper, отдельные вкладки. Тому, кто просто хочет вернуться ко вчерашнему вечеру, потому что обновление что-то сломало, придётся сначала всё это выучить. <strong>SkillFishOS Снимки</strong> отвечает на три вопроса и на этом останавливается: какие снимки у меня есть, сделай один сейчас, верни меня к тому. Кто предпочитает командную строку, сохраняет <code>skillfish-rollback</code>.",
      es: "La hemos escrito nosotros. Btrfs Assistant es un buen programa, pero habla el idioma del sistema de archivos: subvolúmenes, qgroups, configuraciones de snapper, pestañas separadas. Quien solo quiere volver a anoche porque una actualización rompió algo tiene que aprenderse todo eso antes. <strong>SkillFishOS Instantáneas</strong> responde a tres preguntas y ahí se queda: qué instantáneas tengo, hazme una ahora, llévame de vuelta a aquella. Quien prefiera la línea de comandos conserva <code>skillfish-rollback</code>.",
      pt: "Escrevemos a nossa. O Btrfs Assistant é um bom programa, mas fala a língua do sistema de ficheiros: subvolumes, qgroups, configurações do snapper, separadores distintos. Quem só quer voltar a ontem à noite porque uma atualização estragou alguma coisa tem de aprender tudo isso primeiro. O <strong>SkillFishOS Snapshots</strong> responde a três perguntas e fica por aí: que snapshots tenho, faz-me um agora, leva-me de volta àquele. Quem prefere a linha de comando continua com o <code>skillfish-rollback</code>.",
      de: "Wir haben eine eigene geschrieben. Btrfs Assistant ist ein gutes Programm, spricht aber die Sprache des Dateisystems: Subvolumes, Qgroups, Snapper-Konfigurationen, getrennte Reiter. Wer nur zu gestern Abend zurück will, weil ein Update etwas zerschossen hat, muss das alles erst lernen. <strong>SkillFishOS Schnappschüsse</strong> beantwortet drei Fragen und hört dann auf: welche Schnappschüsse habe ich, mach mir jetzt einen, bring mich dorthin zurück. Wer die Kommandozeile bevorzugt, behält <code>skillfish-rollback</code>.",
      fr: "Nous avons écrit la nôtre. Btrfs Assistant est un bon programme, mais il parle la langue du système de fichiers : sous-volumes, qgroups, configurations de snapper, onglets séparés. Qui veut seulement revenir à hier soir parce qu'une mise à jour a cassé quelque chose doit d'abord apprendre tout cela. <strong>SkillFishOS Instantanés</strong> répond à trois questions et s'arrête là : quels instantanés ai-je, fais-m'en un maintenant, ramène-moi à celui-là. Qui préfère la ligne de commande garde <code>skillfish-rollback</code>."
    },
  },
  {
    stato: 'previsto',
    titolo: {
      it: 'Streaming dei giochi con Sunshine',
      en: 'Game streaming with Sunshine',
      pl: 'Strumieniowanie gier przez Sunshine',
      uk: 'Трансляція ігор через Sunshine',
      ru: "Стриминг игр через Sunshine",
      es: "Juego en streaming con Sunshine",
      pt: "Jogos em streaming com o Sunshine",
      de: "Spiele-Streaming mit Sunshine",
      fr: "Le jeu en streaming avec Sunshine"
    },
    testo: {
      it: 'Giocare da un altro dispositivo, con la scheda che lavora in un angolo della casa. Il modulo è previsto nel pannello di controllo remoto, che già gestisce schermo, terminale e AI.',
      en: 'Play from another device while the board works away in a corner of the house. The module is planned for the remote panel, which already handles screen, terminal and AI.',
      pl: "Granie z innego urządzenia, podczas gdy płyta pracuje w kącie mieszkania. Moduł jest planowany w panelu zdalnym, który obsługuje już ekran, terminal i AI.",
      uk: "Гра з іншого пристрою, поки плата працює десь у кутку помешкання. Модуль заплановано у віддаленій панелі, яка вже дає екран, термінал і ШІ.",
      ru: "Играть с другого устройства, пока плата трудится в углу комнаты. Модуль запланирован для панели удалённого управления, которая уже умеет экран, терминал и ИИ.",
      es: "Jugar desde otro dispositivo mientras la placa trabaja en un rincón de la casa. El módulo está previsto para el panel remoto, que ya se ocupa de pantalla, terminal e IA.",
      pt: "Jogar de outro aparelho enquanto a placa trabalha num canto da casa. O módulo está previsto para o painel remoto, que já cuida de tela, terminal e IA.",
      de: "Von einem anderen Gerät aus spielen, während die Platine in einer Ecke der Wohnung arbeitet. Das Modul ist für die Fernsteuerung vorgesehen, die sich schon um Bildschirm, Terminal und KI kümmert.",
      fr: "Jouer depuis un autre appareil pendant que la carte travaille dans un coin de la maison. Le module est prévu pour le panneau à distance, qui gère déjà l'écran, le terminal et l'IA."
    },
  },
  {
    stato: 'previsto',
    titolo: {
      it: 'Giochi su un disco esterno',
      en: 'Games on an external drive',
      pl: 'Gry na dysku zewnętrznym',
      uk: 'Ігри на зовнішньому диску',
      ru: "Игры на внешнем диске",
      es: "Juegos en un disco externo",
      pt: "Jogos num disco externo",
      de: "Spiele auf einem externen Laufwerk",
      fr: "Les jeux sur un disque externe"
    },
    testo: {
      it: "Un selettore per installare i giochi su un SSD USB invece che sul disco di sistema. Steam arriva come Flatpak, quindi non basta cambiare cartella: serve dare il permesso giusto al contenitore, ed è proprio il pezzo che vogliamo togliere di mezzo all'utente.",
      en: "A selector to install games on a USB SSD instead of the system disk. Steam ships as a Flatpak, so changing folder is not enough: the container needs the right permission, and that is exactly the part we want to take off the user's hands.",
      pl: "Wybór, żeby instalować gry na dysku SSD po USB zamiast na dysku systemowym. Steam jest Flatpakiem, więc zmiana katalogu nie wystarczy: kontener potrzebuje odpowiedniego uprawnienia — i właśnie tę część chcemy zdjąć z głowy użytkownikowi.",
      uk: "Перемикач, щоб встановлювати ігри на SSD через USB, а не на системний диск. Steam постачається як Flatpak, тож змінити теку замало: контейнерові потрібен відповідний дозвіл — і саме цю частину ми хочемо зняти з користувача.",
      ru: "Выбор, куда ставить игры: на USB-SSD вместо системного диска. Steam поставляется как Flatpak, поэтому сменить папку недостаточно — контейнеру нужно выдать правильное разрешение, и именно это мы хотим снять с пользователя.",
      es: "Un selector para instalar los juegos en un SSD por USB en vez de en el disco del sistema. Steam viene como Flatpak, así que cambiar de carpeta no basta: hay que dar el permiso correcto al contenedor, y es justo esa parte la que queremos quitarle de encima al usuario.",
      pt: "Um seletor para instalar os jogos num SSD por USB em vez do disco do sistema. O Steam vem como Flatpak, então trocar de pasta não basta: é preciso dar a permissão certa ao contêiner, e é exatamente essa parte que queremos tirar das costas do usuário.",
      de: "Eine Auswahl, um Spiele auf einer USB-SSD statt auf der Systemplatte zu installieren. Steam kommt als Flatpak, deshalb reicht ein anderer Ordner nicht: der Container braucht die richtige Berechtigung, und genau diesen Teil wollen wir den Nutzern abnehmen.",
      fr: "Un sélecteur pour installer les jeux sur un SSD USB plutôt que sur le disque système. Steam est livré en Flatpak, donc changer de dossier ne suffit pas : il faut donner la bonne permission au conteneur, et c'est précisément ce que nous voulons enlever des mains de l'utilisateur."
    },
  },
  {
    stato: 'fatto',
    titolo: {
      it: 'HUD configurabile e curva della ventola',
      en: 'Configurable HUD and fan curve',
      pl: 'Konfigurowalny HUD i krzywa wentylatora',
      uk: 'Налаштовний HUD і крива вентилятора',
      ru: "Настраиваемый HUD и кривая вентилятора",
      es: "HUD configurable y curva del ventilador",
      pt: "HUD configurável e curva da ventoinha",
      de: "Einstellbares HUD und Lüfterkurve",
      fr: "Affichage réglable et courbe du ventilateur"
    },
    testo: {
      it: "Fatte tutte e due, ma non dove erano state promesse: sono due applicazioni loro, non due schede del Tuner. <strong>SkillFishOS HUD</strong> chiede alla macchina quali sensori ha davvero, tiene solo quelli che rispondono e si scrive la configurazione da sé, così su una BC-250 esce il pannello di sempre e su un portatile qualunque escono CPU, RAM e disco invece di sparire. <strong>SkillFishOS Fan Control</strong> ha l'editor della curva, con l'anticipo che fa partire la ventola prima che il calore arrivi.",
      en: "Both done, though not where they were promised: they are two applications of their own, not two tabs in the Tuner. <strong>SkillFishOS HUD</strong> asks the machine which sensors it actually has, keeps only the ones that answer and writes its own configuration, so a BC-250 gets the panel it always had and any laptop gets CPU, RAM and disk instead of nothing at all. <strong>SkillFishOS Fan Control</strong> has the curve editor, with the lead that starts the fan before the heat arrives.",
      pl: "Obie gotowe, choć nie tam, gdzie obiecywaliśmy: to dwie osobne aplikacje, a nie dwie zakładki Tunera. <strong>SkillFishOS HUD</strong> pyta maszynę, jakie czujniki naprawdę ma, zostawia tylko te, które odpowiadają, i sam pisze sobie konfigurację, więc na BC-250 wychodzi ten sam panel co zawsze, a na dowolnym laptopie procesor, pamięć i dysk zamiast pustki. <strong>SkillFishOS Fan Control</strong> ma edytor krzywej, z wyprzedzeniem, które uruchamia wentylator, zanim nadejdzie ciepło.",
      uk: "Обидві зроблено, хоч і не там, де обіцяли: це два окремі застосунки, а не дві вкладки Tuner. <strong>SkillFishOS HUD</strong> питає машину, які датчики вона справді має, лишає тільки ті, що відповідають, і сам пише собі конфігурацію, тож на BC-250 виходить та сама панель, а на будь-якому ноутбуці — процесор, пам'ять і диск замість порожнечі. <strong>SkillFishOS Fan Control</strong> має редактор кривої з випередженням, яке запускає вентилятор раніше, ніж прийде тепло.",
      ru: "Обе сделаны, хотя и не там, где обещали: это два отдельных приложения, а не две вкладки Tuner. <strong>SkillFishOS HUD</strong> спрашивает у машины, какие датчики у неё есть на самом деле, оставляет только отвечающие и сам пишет себе настройку, так что на BC-250 выходит та же панель, а на любом ноутбуке — процессор, память и диск вместо пустоты. <strong>SkillFishOS Fan Control</strong> имеет редактор кривой с упреждением, которое запускает вентилятор раньше, чем придёт тепло.",
      es: "Las dos hechas, aunque no donde se habían prometido: son dos aplicaciones propias, no dos pestañas del Tuner. <strong>SkillFishOS HUD</strong> le pregunta a la máquina qué sensores tiene de verdad, se queda solo con los que responden y se escribe la configuración solo, así que en una BC-250 sale el panel de siempre y en cualquier portátil salen CPU, RAM y disco en vez de nada. <strong>SkillFishOS Fan Control</strong> tiene el editor de la curva, con la anticipación que arranca el ventilador antes de que llegue el calor.",
      pt: "Ambas feitas, embora não onde tinham sido prometidas: são duas aplicações próprias, não dois separadores do Tuner. O <strong>SkillFishOS HUD</strong> pergunta à máquina que sensores tem mesmo, fica só com os que respondem e escreve a configuração sozinho, por isso numa BC-250 sai o painel de sempre e num portátil qualquer saem CPU, RAM e disco em vez de nada. O <strong>SkillFishOS Fan Control</strong> tem o editor da curva, com a antecipação que põe a ventoinha a andar antes de o calor chegar.",
      de: "Beide fertig, wenn auch nicht dort, wo sie versprochen waren: es sind zwei eigene Anwendungen, keine zwei Reiter im Tuner. <strong>SkillFishOS HUD</strong> fragt die Maschine, welche Sensoren sie wirklich hat, behält nur die antwortenden und schreibt sich die Konfiguration selbst, also bekommt eine BC-250 die gewohnte Anzeige und ein beliebiges Notebook CPU, RAM und Platte statt gar nichts. <strong>SkillFishOS Fan Control</strong> hat den Kurveneditor, mit dem Vorlauf, der den Lüfter startet, bevor die Wärme kommt.",
      fr: "Les deux sont faites, mais pas là où elles avaient été promises : ce sont deux applications à part, pas deux onglets du Tuner. <strong>SkillFishOS HUD</strong> demande à la machine quels capteurs elle a vraiment, ne garde que ceux qui répondent et écrit sa configuration tout seul, si bien qu'une BC-250 retrouve son panneau habituel et qu'un portable quelconque obtient processeur, mémoire et disque au lieu de rien. <strong>SkillFishOS Fan Control</strong> a l'éditeur de courbe, avec l'avance qui lance le ventilateur avant que la chaleur n'arrive."
    },
  },
  {
    stato: 'previsto',
    titolo: {
      it: "Revisione dell'ucraino da un madrelingua",
      en: 'Ukrainian reviewed by a native speaker',
      pl: 'Ukraiński przejrzany przez native speakera',
      uk: 'Українська в редакції носія мови',
      ru: "Украинский с проверкой носителем языка",
      es: "Ucraniano revisado por un hablante nativo",
      pt: "Ucraniano revisado por um falante nativo",
      de: "Ukrainisch von einem Muttersprachler geprüft",
      fr: "L'ukrainien relu par un locuteur natif"
    },
    testo: {
      it: "Il polacco è stato riletto da un madrelingua, e si vede. Cerchiamo qualcuno che faccia lo stesso con l'ucraino: se è la tua lingua e ti va di darci una mano, sei il benvenuto.",
      en: "Polish was reviewed by a native speaker, and it shows. We are looking for someone to do the same for Ukrainian: if that is your language and you fancy lending a hand, you are welcome.",
      pl: "Polski przejrzał native speaker i widać to od razu. Szukamy kogoś, kto zrobi to samo z ukraińskim: jeśli to twój język i masz ochotę pomóc, zapraszamy.",
      uk: "Польську переглянув носій мови, і це помітно. Шукаємо когось, хто зробить те саме з українською: якщо це ваша мова й маєте охоту допомогти — ласкаво просимо.",
      ru: "Польский проверил носитель языка, и это видно. Мы ищем того, кто сделает то же самое для украинского: если это ваш язык и хочется помочь — будем рады.",
      es: "El polaco lo revisó un hablante nativo, y se nota. Buscamos a alguien que haga lo mismo con el ucraniano: si es tu idioma y te apetece echar una mano, eres bienvenido.",
      pt: "O polonês foi revisado por um falante nativo, e dá para notar. Estamos procurando alguém que faça o mesmo com o ucraniano: se esse é o seu idioma e você quiser dar uma mão, será bem-vindo.",
      de: "Das Polnische hat ein Muttersprachler geprüft, und das merkt man. Wir suchen jemanden, der dasselbe für Ukrainisch tut: wenn das deine Sprache ist und du Lust hast mitzuhelfen, bist du willkommen.",
      fr: "Le polonais a été relu par un locuteur natif, et cela se voit. Nous cherchons quelqu'un pour faire de même avec l'ukrainien : si c'est votre langue et que l'idée vous tente, vous êtes le bienvenu."
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
      ru: "Точки восстановления и одна команда, чтобы вернуться",
      es: "Puntos de restauración, y un comando para volver atrás",
      pt: "Pontos de restauração, e um comando para voltar",
      de: "Wiederherstellungspunkte, und ein Befehl zurück",
      fr: "Des points de restauration, et une commande pour revenir en arrière"
    },
    testo: {
      it: "Il sistema tiene cinque punti di ripristino, presi da solo prima di ogni aggiornamento, e li mostra nel menu di avvio. Con <code>skillfish-rollback</code> si torna a uno di essi per davvero, in un comando: la cartella personale non viene toccata.",
      en: "The system keeps five restore points, taken by itself before every upgrade, and lists them in the boot menu. <code>skillfish-rollback</code> takes you back to one of them for real, in a single command — your home directory is left alone.",
      pl: "System trzyma pięć punktów przywracania, robionych samoczynnie przed każdą aktualizacją, i pokazuje je w menu startowym. <code>skillfish-rollback</code> naprawdę cofa system do jednego z nich, jednym poleceniem — katalog domowy zostaje nietknięty.",
      uk: "Система тримає п'ять точок відновлення, які створює сама перед кожним оновленням, і показує їх у меню завантаження. <code>skillfish-rollback</code> справді повертає систему до однієї з них, однією командою — домашня тека лишається недоторканою.",
      ru: "Система держит пять точек восстановления, снятых ею самой перед каждым обновлением, и показывает их в загрузочном меню. <code>skillfish-rollback</code> действительно возвращает вас к одной из них одной командой — домашний каталог при этом не трогается.",
      es: "El sistema guarda cinco puntos de restauración, tomados por él mismo antes de cada actualización, y los lista en el menú de arranque. <code>skillfish-rollback</code> te devuelve de verdad a uno de ellos con un solo comando — tu carpeta personal no se toca.",
      pt: "O sistema guarda cinco pontos de restauração, tirados por ele mesmo antes de cada atualização, e os lista no menu de boot. O <code>skillfish-rollback</code> leva você de volta a um deles de verdade, com um único comando — sua pasta pessoal não é tocada.",
      de: "Das System hält fünf Wiederherstellungspunkte bereit, die es vor jeder Aktualisierung selbst anlegt, und listet sie im Startmenü auf. <code>skillfish-rollback</code> bringt dich mit einem einzigen Befehl wirklich zu einem davon zurück — dein persönlicher Ordner bleibt unangetastet.",
      fr: "Le système garde cinq points de restauration, pris tout seul avant chaque mise à jour, et les affiche dans le menu de démarrage. <code>skillfish-rollback</code> vous ramène vraiment à l'un d'eux, en une seule commande — votre dossier personnel n'est pas touché."
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
      ru: "Четыре языка, с откатом на английский",
      es: "Cuatro idiomas, con vuelta al inglés",
      pt: "Quatro idiomas, sempre com volta ao inglês",
      de: "Vier Sprachen, immer mit Rückfall auf Englisch",
      fr: "Quatre langues, avec toujours l'anglais en secours"
    },
    testo: {
      it: 'Italiano, inglese, polacco e ucraino nelle applicazioni, nella schermata di accesso, nel pannello web e nelle diapositive dell\'installer. E una regola: se una traduzione manca, esce l\'inglese, mai l\'italiano.',
      en: 'Italian, English, Polish and Ukrainian across the applications, the login screen, the web panel and the installer slideshow. Plus a rule: if a translation is missing you get English, never Italian.',
      pl: "Włoski, angielski, polski i ukraiński w aplikacjach, na ekranie logowania, w panelu webowym i w pokazie slajdów instalatora. Do tego zasada: gdy brakuje tłumaczenia, pojawia się angielski, nigdy włoski.",
      uk: "Італійська, англійська, польська та українська — у програмах, на екрані входу, у вебпанелі й у слайдах встановлювача. Плюс правило: якщо перекладу немає, буде англійська, ніколи не італійська.",
      ru: "Итальянский, английский, польский и украинский — в программах, на экране входа, в веб-панели и в презентации установщика. Плюс правило: если перевода нет, показывается английский, а не итальянский.",
      es: "Italiano, inglés, polaco y ucraniano en las aplicaciones, la pantalla de acceso, el panel web y la presentación del instalador. Y una regla: si falta una traducción sale el inglés, nunca el italiano.",
      pt: "Italiano, inglês, polonês e ucraniano nos aplicativos, na tela de acesso, no painel web e na apresentação do instalador. E uma regra: se faltar uma tradução aparece o inglês, nunca o italiano.",
      de: "Italienisch, Englisch, Polnisch und Ukrainisch in den Anwendungen, im Anmeldebildschirm, in der Weboberfläche und in der Präsentation des Installationsprogramms. Dazu eine Regel: fehlt eine Übersetzung, kommt Englisch, niemals Italienisch.",
      fr: "Italien, anglais, polonais et ukrainien dans les applications, l'écran de connexion, le panneau web et la présentation de l'installateur. Plus une règle : si une traduction manque, vous avez l'anglais, jamais l'italien."
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
      ru: "Восемь ядер вместо шести",
      es: "Ocho núcleos en lugar de seis",
      pt: "Oito núcleos em vez de seis",
      de: "Acht Kerne statt sechs",
      fr: "Huit cœurs au lieu de six"
    },
    testo: {
      it: 'La scheda si presenta come 6 core / 12 thread, ma i due mancanti sono spenti dalla configurazione, non difettosi. SkillFishOS li riaccende all\'avvio: <strong>+20% misurato</strong> sui carichi multi-thread, senza toccare il BIOS.',
      en: 'The board presents itself as 6 cores / 12 threads, but the two missing ones are switched off by configuration, not defective. SkillFishOS turns them back on at boot: <strong>+20% measured</strong> on multi-threaded work, with no BIOS changes.',
      pl: "Płyta przedstawia się jako 6 rdzeni / 12 wątków, ale dwa brakujące są wyłączone konfiguracją, a nie uszkodzone. SkillFishOS włącza je z powrotem przy starcie: <strong>+20% zmierzone</strong> przy obciążeniach wielowątkowych, bez grzebania w BIOS-ie.",
      uk: "Плата подає себе як 6 ядер / 12 потоків, але два відсутні вимкнені конфігурацією, а не несправні. SkillFishOS вмикає їх назад під час запуску: <strong>+20% виміряно</strong> на багатопотокових навантаженнях, без жодних змін у BIOS.",
      ru: "Плата представляется как 6 ядер / 12 потоков, но двух недостающих нет из-за конфигурации, а не из-за дефекта. SkillFishOS включает их при загрузке: <strong>+20% по измерениям</strong> в многопоточных задачах, без правки BIOS.",
      es: "La placa se presenta como 6 núcleos / 12 hilos, pero los dos que faltan están apagados por configuración, no defectuosos. SkillFishOS los vuelve a encender en el arranque: <strong>+20% medido</strong> en trabajo multihilo, sin tocar la BIOS.",
      pt: "A placa se apresenta como 6 núcleos / 12 threads, mas os dois que faltam estão desligados por configuração, não com defeito. O SkillFishOS os liga de novo no boot: <strong>+20% medido</strong> em trabalho multithread, sem mexer na BIOS.",
      de: "Die Platine gibt sich als 6 Kerne / 12 Threads aus, aber die beiden fehlenden sind per Konfiguration abgeschaltet, nicht defekt. SkillFishOS schaltet sie beim Start wieder ein: <strong>+20% gemessen</strong> bei mehrfädiger Arbeit, ohne Eingriff ins BIOS.",
      fr: "La carte se présente avec 6 cœurs / 12 fils, mais les deux qui manquent sont éteints par la configuration, pas défectueux. SkillFishOS les rallume au démarrage : <strong>+20 % mesuré</strong> sur les charges multifils, sans toucher au BIOS."
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
    data: '2026-08-23',
    quando: { it: '23 agosto 2026', en: '23 August 2026', pl: '23 sierpnia 2026', uk: '23 серпня 2026', ru: '23 августа 2026', es: '23 de agosto de 2026', pt: '23 de agosto de 2026', de: '23. August 2026', fr: '23 août 2026' },
    etichetta: { it: 'aggiornamento', en: 'update', pl: 'aktualizacja', uk: 'оновлення', ru: 'обновление', es: 'actualización', pt: 'atualização', de: 'Update', fr: 'mise à jour' },
    titolo: {
      it: "Il kernel 7.2.0 arriva con l'aggiornamento",
      en: "Kernel 7.2.0 arrives with an update",
      pl: "Jądro 7.2.0 przychodzi z aktualizacją",
      uk: "Ядро 7.2.0 приходить з оновленням",
      ru: "Ядро 7.2.0 приходит с обновлением",
      es: "El núcleo 7.2.0 llega con la actualización",
      pt: "O kernel 7.2.0 chega com a atualização",
      de: "Kernel 7.2.0 kommt mit einem Update",
      fr: "Le noyau 7.2.0 arrive avec une mise à jour"
    },
    testo: {
      it: "Il kernel <strong>7.2.0</strong> ora arriva con un normale aggiornamento. Prima stava solo fra i file da scaricare a mano su GitHub. Non è più veloce del 7.1.7, le differenze che abbiamo misurato stanno dentro il rumore. Serve a stare al passo con il kernel di riferimento e con i driver.",
      en: "Kernel <strong>7.2.0</strong> now arrives with an ordinary update. Until now it only sat among the files you download by hand on GitHub. It is not faster than 7.1.7, the differences we measured are inside the noise. The point is keeping up with the upstream kernel and its drivers.",
      pl: "Jądro <strong>7.2.0</strong> przychodzi teraz ze zwykłą aktualizacją. Wcześniej leżało tylko wśród plików do ręcznego pobrania na GitHubie. Nie jest szybsze od 7.1.7, zmierzone różnice mieszczą się w szumie. Chodzi o to, by nadążać za jądrem źródłowym i jego sterownikami.",
      uk: "Ядро <strong>7.2.0</strong> тепер приходить зі звичайним оновленням. Раніше воно лежало тільки серед файлів, які завантажують вручну на GitHub. Воно не швидше за 7.1.7, виміряні відмінності лежать у межах похибки. Сенс у тому, щоб не відставати від основного ядра та його драйверів.",
      ru: "Ядро <strong>7.2.0</strong> теперь приходит с обычным обновлением. Раньше оно лежало только среди файлов, которые скачивают вручную на GitHub. Оно не быстрее 7.1.7, измеренные различия лежат в пределах шума. Смысл в том, чтобы не отставать от основного ядра и его драйверов.",
      es: "El núcleo <strong>7.2.0</strong> llega ahora con una actualización normal. Hasta ahora estaba solo entre los archivos que se descargan a mano en GitHub. No es más rápido que el 7.1.7, las diferencias que medimos caen dentro del ruido. Sirve para ir al paso del núcleo de referencia y sus controladores.",
      pt: "O kernel <strong>7.2.0</strong> chega agora com uma atualização normal. Até aqui estava apenas entre os ficheiros que se descarregam à mão no GitHub. Não é mais rápido do que o 7.1.7, as diferenças que medimos ficam dentro do ruído. Serve para acompanhar o kernel de referência e os seus controladores.",
      de: "Kernel <strong>7.2.0</strong> kommt jetzt mit einem gewöhnlichen Update. Bisher lag er nur bei den Dateien, die man auf GitHub von Hand herunterlädt. Er ist nicht schneller als 7.1.7, die gemessenen Unterschiede liegen im Rauschen. Es geht darum, mit dem Referenzkernel und seinen Treibern Schritt zu halten.",
      fr: "Le noyau <strong>7.2.0</strong> arrive maintenant avec une mise à jour ordinaire. Jusqu'ici il ne se trouvait que parmi les fichiers à télécharger à la main sur GitHub. Il n'est pas plus rapide que le 7.1.7, les écarts que nous avons mesurés restent dans le bruit. Il s'agit de suivre le noyau de référence et ses pilotes."
    },
  },
  {
    data: '2026-08-22',
    quando: { it: '22 agosto 2026', en: '22 August 2026', pl: '22 sierpnia 2026', uk: '22 серпня 2026' },
    etichetta: { it: 'aggiornamento', en: 'update', pl: 'aktualizacja', uk: 'оновлення' },
    titolo: {
      it: 'Il Tuner dice i millivolt, e gli aggiornamenti si vedono prima',
      en: 'The Tuner speaks in millivolts, and updates show up sooner',
      pl: 'Tuner mówi w miliwoltach, a aktualizacje widać wcześniej',
      uk: 'Tuner говорить у мілівольтах, а оновлення видно раніше',
      ru: 'Tuner говорит в милливольтах, а обновления видно раньше',
      es: 'El Tuner habla en milivoltios, y las actualizaciones se ven antes',
      pt: 'O Tuner fala em milivolts, e as atualizações aparecem mais cedo',
      de: 'Der Tuner spricht in Millivolt, und Updates zeigen sich früher',
      fr: 'Le Tuner parle en millivolts, et les mises à jour arrivent plus tôt'
    },
    testo: {
      it: "Nel Tuner l'undervolt della CPU si leggeva «-24». Era il numero che vuole il firmware, non uno che significhi qualcosa per chi guarda — e subito accanto la GPU diceva «1000 mV». Adesso dice <strong>-150 mV</strong>, e la riga di riepilogo mostra le due tensioni nello stesso modo.<br><br>La conversione non è stimata: è misurata sulla scheda, leggendo la tensione vera dal firmware sotto carico. Uno scalino vale <strong>6,25 mV</strong>, e la tabella misurata mette -24 esattamente 150 mV sotto la curva di fabbrica.<br><br>L'altra cosa riguarda tutti. Il controllo degli aggiornamenti girava una volta al giorno, con fino a quattro ore di ritardo casuale: fra l'uscita di una correzione e il momento in cui la macchina se ne accorgeva poteva passare più di un giorno. Adesso guarda <strong>ogni ora</strong>. Non significa più avvisi: la notifica parla solo quando i numeri cambiano, e non ripete la stessa cosa per una settimana.",
      en: "In the Tuner the CPU undervolt read “-24”. That is the number the firmware wants, not one that means anything to a person — and right beside it the GPU said “1000 mV”. It now reads <strong>-150 mV</strong>, and the summary line shows both voltages the same way.<br><br>The conversion is measured rather than estimated: read back from the firmware on the board, under load. One step is <strong>6.25 mV</strong>, and the measured table puts -24 exactly 150 mV below the factory curve.<br><br>The other change affects everyone. The update check ran once a day with up to four hours of random delay, so more than a day could pass between a fix leaving the archive and the machine noticing. It now looks <strong>every hour</strong>. That does not mean more notifications: the notice appears only when the numbers change, and it does not repeat itself for a week.",
      pl: "W Tunerze undervolt procesora pokazywał „-24”. To liczba, której chce firmware, a nie taka, która cokolwiek mówi człowiekowi — a tuż obok GPU pokazywało „1000 mV”. Teraz jest <strong>-150 mV</strong>, a wiersz podsumowania pokazuje obie wartości tak samo.<br><br>Przelicznik jest zmierzony, nie oszacowany: odczytany z firmware'u na płycie, pod obciążeniem. Jeden krok to <strong>6,25 mV</strong>, a zmierzona tabela stawia -24 dokładnie 150 mV poniżej fabrycznej krzywej.<br><br>Druga zmiana dotyczy wszystkich. Sprawdzanie aktualizacji działało raz dziennie, z opóźnieniem losowym do czterech godzin: od wydania poprawki do chwili, gdy maszyna ją zauważyła, mijał czasem ponad dzień. Teraz sprawdza <strong>co godzinę</strong>. To nie znaczy więcej powiadomień: komunikat pojawia się tylko wtedy, gdy liczby się zmieniają, i nie powtarza się przez tydzień.",
      uk: "У Tuner андервольт процесора показував «-24». Це число, якого хоче мікропрограма, а не таке, що щось означає для людини — а поруч ГП показував «1000 мВ». Тепер там <strong>-150 мВ</strong>, і підсумковий рядок показує обидві напруги однаково.<br><br>Перетворення виміряне, а не оцінене: зчитане з мікропрограми на платі, під навантаженням. Один щабель — це <strong>6,25 мВ</strong>, і виміряна таблиця ставить -24 рівно на 150 мВ нижче заводської кривої.<br><br>Друга зміна стосується всіх. Перевірка оновлень працювала раз на добу з випадковою затримкою до чотирьох годин: від виходу виправлення до миті, коли машина його помічала, могло минути більше доби. Тепер вона дивиться <strong>щогодини</strong>. Це не означає більше сповіщень: повідомлення з'являється лише тоді, коли числа змінюються, і не повторюється тиждень.",
      ru: "В Tuner андервольт процессора показывал «-24». Это число, которое нужно прошивке, а не то, что что-то значит для человека — а рядом ГП показывал «1000 мВ». Теперь там <strong>-150 мВ</strong>, и строка сводки показывает оба напряжения одинаково.<br><br>Пересчёт измерен, а не прикинут: считан из прошивки на плате, под нагрузкой. Один шаг — <strong>6,25 мВ</strong>, и измеренная таблица ставит -24 ровно на 150 мВ ниже заводской кривой.<br><br>Второе изменение касается всех. Проверка обновлений работала раз в сутки со случайной задержкой до четырёх часов: между выходом исправления и моментом, когда машина его замечала, могло пройти больше суток. Теперь она смотрит <strong>каждый час</strong>. Это не значит больше уведомлений: сообщение появляется только когда числа меняются, и не повторяется неделю.",
      es: "En el Tuner el undervolt de la CPU se leía «-24». Es el número que quiere el firmware, no uno que signifique algo para una persona — y justo al lado la GPU decía «1000 mV». Ahora pone <strong>-150 mV</strong>, y la línea de resumen muestra los dos voltajes igual.<br><br>La conversión está medida, no estimada: leída del firmware en la placa, bajo carga. Un paso vale <strong>6,25 mV</strong>, y la tabla medida sitúa -24 exactamente 150 mV por debajo de la curva de fábrica.<br><br>El otro cambio afecta a todos. La comprobación de actualizaciones se hacía una vez al día, con hasta cuatro horas de retraso aleatorio: entre la salida de una corrección y el momento en que la máquina se enteraba podía pasar más de un día. Ahora mira <strong>cada hora</strong>. No significa más avisos: el aviso aparece solo cuando cambian los números, y no se repite en una semana.",
      pt: "No Tuner o undervolt da CPU aparecia como “-24”. É o número que o firmware quer, não um que signifique alguma coisa para uma pessoa — e logo ao lado a GPU dizia “1000 mV”. Agora diz <strong>-150 mV</strong>, e a linha de resumo mostra as duas tensões da mesma forma.<br><br>A conversão é medida, não estimada: lida do firmware na placa, sob carga. Um passo vale <strong>6,25 mV</strong>, e a tabela medida coloca -24 exatamente 150 mV abaixo da curva de fábrica.<br><br>A outra mudança é para todos. A verificação de atualizações corria uma vez por dia, com até quatro horas de atraso aleatório: entre a saída de uma correção e o momento em que a máquina reparava podia passar mais de um dia. Agora olha <strong>a cada hora</strong>. Não quer dizer mais avisos: o aviso só aparece quando os números mudam, e não se repete durante uma semana.",
      de: "Im Tuner stand beim CPU-Undervolting „-24“. Das ist die Zahl, die die Firmware will, keine, die einem Menschen etwas sagt — und direkt daneben stand bei der GPU „1000 mV“. Jetzt steht dort <strong>-150 mV</strong>, und die Übersichtszeile zeigt beide Spannungen gleich.<br><br>Die Umrechnung ist gemessen, nicht geschätzt: aus der Firmware auf der Platine ausgelesen, unter Last. Ein Schritt sind <strong>6,25 mV</strong>, und die gemessene Tabelle legt -24 genau 150 mV unter die Werkskurve.<br><br>Die andere Änderung betrifft alle. Die Update-Prüfung lief einmal am Tag, mit bis zu vier Stunden zufälliger Verzögerung: zwischen dem Erscheinen einer Korrektur und dem Moment, in dem die Maschine sie bemerkte, konnte mehr als ein Tag liegen. Jetzt schaut sie <strong>stündlich</strong> nach. Das heißt nicht mehr Meldungen: die Meldung kommt nur, wenn sich die Zahlen ändern, und wiederholt sich eine Woche lang nicht.",
      fr: "Dans le Tuner, l'undervolt du processeur affichait « -24 ». C'est le nombre que veut le micrologiciel, pas un nombre qui signifie quelque chose pour quelqu'un — et juste à côté, le GPU affichait « 1000 mV ». Il affiche désormais <strong>-150 mV</strong>, et la ligne de résumé montre les deux tensions de la même façon.<br><br>La conversion est mesurée et non estimée : relue depuis le micrologiciel sur la carte, en charge. Un palier vaut <strong>6,25 mV</strong>, et le tableau mesuré place -24 exactement 150 mV sous la courbe d'usine.<br><br>L'autre changement concerne tout le monde. La vérification des mises à jour tournait une fois par jour, avec jusqu'à quatre heures de décalage aléatoire : entre la sortie d'un correctif et le moment où la machine s'en apercevait, il pouvait s'écouler plus d'une journée. Elle regarde maintenant <strong>toutes les heures</strong>. Cela ne veut pas dire plus de notifications : l'avis n'apparaît que lorsque les chiffres changent, et ne se répète pas avant une semaine."
    },
  },
  {
    data: '2026-08-17',
    quando: { it: '17 agosto 2026', en: '17 August 2026', pl: '17 sierpnia 2026', uk: '17 серпня 2026' },
    etichetta: { it: 'release', en: 'release', pl: 'wydanie', uk: 'реліз' },
    titolo: {
      it: 'SkillFishOS 26.06.4 «Aetherium»',
      en: 'SkillFishOS 26.06.4 “Aetherium”',
      pl: 'SkillFishOS 26.06.4 „Aetherium”',
      uk: 'SkillFishOS 26.06.4 «Aetherium»',
      ru: "SkillFishOS 26.06.4 «Aetherium»",
      es: "SkillFishOS 26.06.4 «Aetherium»",
      pt: "SkillFishOS 26.06.4 “Aetherium”",
      de: "SkillFishOS 26.06.4 „Aetherium“",
      fr: "SkillFishOS 26.06.4 « Aetherium »"
    },
    testo: {
      it: "Due difetti potevano impedire all'installazione di arrivare in fondo su una BC-250 vera. Adesso non ci sono più.<br><br>Il primo: lo sblocco degli otto core scriveva la maschera nella SMU e <strong>riavviava la scheda</strong>, anche dentro la sessione live. Se capitava mentre l'installatore stava copiando, l'installazione moriva lì. Adesso lo sblocco è disattivato di partenza e si chiede dal Tuner.<br><br>Il secondo: installando su <strong>Btrfs</strong> il sistema poteva non avviarsi, con <code>error: premature end of file</code> al prompt di GRUB. L'installatore copiava con <code>rsync -aHAXS</code> e il kernel arrivava a destinazione con un buco in coda; su Btrfs un buco non ha extent, e GRUB si ferma lì. Linux quel file lo legge benissimo, ed è per questo che non sembrava esserci niente di storto.<br><br>Corretti anche: il controllo del disco chiedeva 10 GiB quando al sistema ne servono 15, l'edizione BC-250 avviava il kernel <em>generico</em>, e le voci Safe Mode e Text Mode facevano esattamente la stessa cosa della voce normale.<br><br>Le immagini 26.06.x precedenti sono state <strong>sostituite</strong>: se ne hai una, scarica la 26.06.4.",
      en: "Two defects could stop the installation from finishing on a real BC-250. They are gone.<br><br>The first: the eight-core unlock wrote the SMU core mask and <strong>rebooted the board</strong>, including inside the live session. If that landed while the installer was copying, the installation died. The unlock is now off by default and opt-in from the Tuner.<br><br>The second: installing onto <strong>Btrfs</strong> could produce a system that would not boot, with <code>error: premature end of file</code> at the GRUB prompt. The installer copied with <code>rsync -aHAXS</code> and the kernel image landed with a hole at the tail; on Btrfs a hole has no extent, so GRUB stops there. Linux reads that file perfectly, which is why nothing looked wrong.<br><br>Also fixed: the disk check asked for 10 GiB when the system needs 15, the BC-250 edition booted the <em>generic</em> kernel, and Safe Mode and Text Mode did exactly the same thing as the normal boot entry.<br><br>Earlier 26.06.x images have been <strong>superseded</strong>: if you have one, download 26.06.4.",
      pl: "Dwie usterki mogły uniemożliwić dokończenie instalacji na prawdziwym BC-250. Już ich nie ma.<br><br>Pierwsza: odblokowanie ośmiu rdzeni zapisywało maskę rdzeni w SMU i <strong>ponownie uruchamiało płytę</strong> — również w sesji live. Jeśli trafiło to w moment kopiowania plików, instalacja umierała. Teraz odblokowanie jest domyślnie wyłączone i włącza się je z poziomu Tunera.<br><br>Druga: instalacja na <strong>Btrfs</strong> mogła dać system, który się nie uruchamia, z komunikatem <code>error: premature end of file</code> w GRUB-ie. Instalator kopiował przez <code>rsync -aHAXS</code>, a obraz jądra trafiał na dysk z dziurą na końcu; na Btrfs dziura nie ma ekstentu, więc GRUB zatrzymuje się w tym miejscu. Linux czyta ten plik bez problemu — dlatego nic nie wyglądało podejrzanie.<br><br>Poprawione też: instalator wymagał 10 GiB, choć system potrzebuje 15; edycja BC-250 uruchamiała jądro <em>generic</em>; a pozycje Safe Mode i Text Mode robiły dokładnie to samo co zwykły wpis startowy.<br><br>Wcześniejsze obrazy 26.06.x zostały <strong>zastąpione</strong>: jeśli masz któryś z nich, pobierz 26.06.4.",
      uk: "Дві вади могли завадити встановленню дійти до кінця на справжній BC-250. Їх більше немає.<br><br>Перша: розблокування восьми ядер записувало маску ядер у SMU і <strong>перезавантажувало плату</strong> — зокрема й у live-сеансі. Якщо це збігалося з копіюванням файлів, встановлення обривалося. Тепер розблокування типово вимкнене й вмикається з Tuner.<br><br>Друга: встановлення на <strong>Btrfs</strong> могло дати систему, яка не завантажується, з <code>error: premature end of file</code> у GRUB. Встановлювач копіював через <code>rsync -aHAXS</code>, і образ ядра потрапляв на диск із діркою в кінці; на Btrfs дірка не має екстента, тож GRUB зупиняється саме там. Linux читає цей файл бездоганно — тому нічого не виглядало підозрілим.<br><br>Також виправлено: перевірка диска вимагала 10 ГіБ, хоча системі потрібно 15; видання BC-250 завантажувало <em>загальне</em> ядро; а пункти Safe Mode і Text Mode робили те саме, що й звичайний пункт завантаження.<br><br>Попередні образи 26.06.x <strong>замінено</strong>: якщо у вас є котрийсь із них, звантажте 26.06.4.",
      ru: "Две неполадки могли не дать установке завершиться на настоящей BC-250. Их больше нет.<br><br>Первая: разблокировка восьми ядер записывала маску ядер в SMU и <strong>перезагружала плату</strong>, в том числе внутри live-сессии. Если это происходило, пока установщик копировал файлы, установка умирала. Теперь разблокировка выключена по умолчанию и включается вручную из Tuner.<br><br>Вторая: установка на <strong>Btrfs</strong> могла дать систему, которая не загружается, с <code>error: premature end of file</code> в приглашении GRUB. Установщик копировал через <code>rsync -aHAXS</code>, и образ ядра оказывался с дырой в хвосте; на Btrfs у дыры нет экстента, поэтому GRUB на ней останавливается. Linux читает такой файл прекрасно — потому и не выглядело, будто что-то не так.<br><br>Ещё исправлено: проверка диска требовала 10 ГиБ, тогда как системе нужно 15; издание BC-250 загружало <em>generic</em>-ядро; а Safe Mode и Text Mode делали ровно то же, что и обычный пункт загрузки.<br><br>Прежние образы 26.06.x <strong>заменены</strong>: если у вас один из них, скачайте 26.06.4.",
      es: "Dos fallos podían impedir que la instalación terminara en una BC-250 real. Ya no están.<br><br>El primero: el desbloqueo de los ocho núcleos escribía la máscara de núcleos en el SMU y <strong>reiniciaba la placa</strong>, también dentro de la sesión en vivo. Si eso caía mientras el instalador copiaba, la instalación moría. El desbloqueo ahora está desactivado de fábrica y se activa a mano desde el Tuner.<br><br>El segundo: instalar sobre <strong>Btrfs</strong> podía dar un sistema que no arrancaba, con <code>error: premature end of file</code> en el prompt de GRUB. El instalador copiaba con <code>rsync -aHAXS</code> y la imagen del núcleo acababa con un hueco al final; en Btrfs un hueco no tiene extent, así que GRUB se para ahí. Linux lee ese archivo perfectamente, y por eso nada parecía ir mal.<br><br>También corregido: la comprobación de disco pedía 10 GiB cuando el sistema necesita 15, la edición BC-250 arrancaba el núcleo <em>generic</em>, y Safe Mode y Text Mode hacían exactamente lo mismo que la entrada normal.<br><br>Las imágenes 26.06.x anteriores quedan <strong>sustituidas</strong>: si tienes una, descarga la 26.06.4.",
      pt: "Duas falhas podiam impedir a instalação de terminar numa BC-250 de verdade. Elas acabaram.<br><br>A primeira: o destravamento dos oito núcleos escrevia a máscara de núcleos no SMU e <strong>reiniciava a placa</strong>, inclusive dentro da sessão ao vivo. Se isso caísse enquanto o instalador copiava, a instalação morria. O destravamento agora vem desligado e é ligado à mão pelo Tuner.<br><br>A segunda: instalar em <strong>Btrfs</strong> podia gerar um sistema que não dava boot, com <code>error: premature end of file</code> no prompt do GRUB. O instalador copiava com <code>rsync -aHAXS</code> e a imagem do kernel ficava com um buraco no fim; no Btrfs um buraco não tem extent, então o GRUB para ali. O Linux lê esse arquivo perfeitamente, e por isso nada parecia errado.<br><br>Também corrigido: a checagem de disco pedia 10 GiB quando o sistema precisa de 15, a edição BC-250 dava boot no kernel <em>generic</em>, e Safe Mode e Text Mode faziam exatamente o mesmo que a entrada normal.<br><br>As imagens 26.06.x anteriores foram <strong>substituídas</strong>: se você tem uma, baixe a 26.06.4.",
      de: "Zwei Fehler konnten verhindern, dass die Installation auf einer echten BC-250 zu Ende läuft. Sie sind weg.<br><br>Der erste: Das Freischalten der acht Kerne schrieb die Kernmaske in die SMU und <strong>startete die Platine neu</strong>, auch innerhalb der Live-Sitzung. Traf das ein, während das Installationsprogramm kopierte, war die Installation tot. Das Freischalten ist jetzt standardmäßig aus und wird im Tuner von Hand eingeschaltet.<br><br>Der zweite: Eine Installation auf <strong>Btrfs</strong> konnte ein System ergeben, das nicht startet, mit <code>error: premature end of file</code> an der GRUB-Eingabe. Das Installationsprogramm kopierte mit <code>rsync -aHAXS</code>, und das Kernel-Abbild landete mit einem Loch am Ende; auf Btrfs hat ein Loch keinen Extent, also bleibt GRUB dort stehen. Linux liest diese Datei einwandfrei, und deshalb sah nichts falsch aus.<br><br>Ebenfalls behoben: Die Plattenprüfung verlangte 10 GiB, obwohl das System 15 braucht, die BC-250-Ausgabe startete den <em>generic</em>-Kernel, und Safe Mode und Text Mode taten genau dasselbe wie der normale Starteintrag.<br><br>Frühere 26.06.x-Abbilder sind <strong>überholt</strong>: wenn du eines hast, lade 26.06.4 herunter.",
      fr: "Deux défauts pouvaient empêcher l'installation d'aller au bout sur une vraie BC-250. Ils ont disparu.<br><br>Le premier : le déverrouillage des huit cœurs écrivait le masque des cœurs dans la SMU et <strong>redémarrait la carte</strong>, y compris depuis la session live. Si cela tombait pendant que l'installateur copiait, l'installation mourait. Le déverrouillage est maintenant éteint par défaut et se demande depuis le Tuner.<br><br>Le second : installer sur <strong>Btrfs</strong> pouvait donner un système qui ne démarrait pas, avec <code>error: premature end of file</code> à l'invite de GRUB. L'installateur copiait avec <code>rsync -aHAXS</code> et l'image du noyau arrivait avec un trou à la fin ; sur Btrfs un trou n'a pas d'extent, donc GRUB s'arrête là. Linux lit ce fichier parfaitement, et c'est pour cela que rien ne paraissait anormal.<br><br>Corrigé aussi : le contrôle du disque demandait 10 Gio alors que le système en veut 15, l'édition BC-250 démarrait sur le noyau <em>générique</em>, et les modes Safe et Text faisaient exactement la même chose que l'entrée normale.<br><br>Les images 26.06.x précédentes sont <strong>remplacées</strong> : si vous en avez une, téléchargez la 26.06.4."
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
      ru: "SkillFishOS 26.06.3 «Aetherium»",
      es: "SkillFishOS 26.06.3 «Aetherium»",
      pt: "SkillFishOS 26.06.3 “Aetherium”",
      de: "SkillFishOS 26.06.3 „Aetherium“",
      fr: "SkillFishOS 26.06.3 « Aetherium »"
    },
    testo: {
      it: "<strong>⚠️ Questa immagine è stata sostituita: usa la 26.06.4.</strong> Aveva due difetti che potevano bloccare l'installazione su una BC-250.<br><br>Due edizioni, <strong>BC-250</strong> e <strong>Generic</strong>, per la scheda AMD e per qualsiasi PC o macchina virtuale x86-64.<br><br>La lingua che scegli vale adesso <strong>ovunque</strong>: interfaccia, schermata di accesso, pannello web e anche le diapositive dell'installer, che prima restavano in inglese. Italiano, inglese, polacco e ucraino, e se una traduzione manca esce l'inglese.<br><br>Sotto: kernel <strong>7.1.7</strong> con lo sblocco delle 40 Compute Unit e degli otto core, installazione su Btrfs con punti di ripristino attivi dal primo avvio, e AI locale su GPU. Un'installazione nuova parte con <strong>tutti i servizi a posto</strong>.<br><br>L'edizione <strong>Slim</strong> non esce più come immagine: il kernel slim resta nel repository per chi lo vuole.",
      en: "<strong>⚠️ This image has been superseded: please use 26.06.4.</strong> It had two defects that could stop an installation on a BC-250.<br><br>Two editions, <strong>BC-250</strong> and <strong>Generic</strong>, for the AMD board and for any x86-64 PC or virtual machine.<br><br>The language you choose now applies <strong>everywhere</strong>: interface, login screen, web panel and the installer slideshow too, which used to stay in English. Italian, English, Polish and Ukrainian — and if a translation is missing, you get English.<br><br>Underneath: kernel <strong>7.1.7</strong> with the 40 Compute Unit unlock and the eight-core unlock, Btrfs installs with restore points live from the first boot, and on-device AI on the GPU. A fresh install comes up with <strong>every service healthy</strong>.<br><br>The <strong>Slim</strong> edition is no longer shipped as an image: the slim kernel stays in the repository for anyone who wants it.",
      pl: "<strong>⚠️ Ten obraz został zastąpiony: użyj 26.06.4.</strong> Miał dwie usterki, które mogły zatrzymać instalację na BC-250.<br><br>Dwie edycje, <strong>BC-250</strong> i <strong>Generic</strong>, dla płyty AMD i dla dowolnego peceta lub maszyny wirtualnej x86-64.<br><br>Wybrany język obowiązuje teraz <strong>wszędzie</strong>: interfejs, ekran logowania, panel webowy, a także slajdy instalatora, które wcześniej zostawały po angielsku. Włoski, angielski, polski i ukraiński — a gdy brakuje tłumaczenia, pojawia się angielski.<br><br>Pod spodem: jądro <strong>7.1.7</strong> z odblokowaniem 40 jednostek obliczeniowych i ośmiu rdzeni, instalacja na Btrfs z punktami przywracania działającymi od pierwszego uruchomienia oraz lokalne AI na GPU. Świeża instalacja startuje z <strong>wszystkimi usługami na chodzie</strong>.<br><br>Edycja <strong>Slim</strong> nie wychodzi już jako obraz: jądro slim zostaje w repozytorium dla chętnych.",
      uk: "<strong>⚠️ Цей образ замінено: скористайтеся 26.06.4.</strong> Він мав дві вади, які могли зупинити встановлення на BC-250.<br><br>Два видання, <strong>BC-250</strong> і <strong>Generic</strong>, для плати AMD та для будь-якого ПК чи віртуальної машини x86-64.<br><br>Обрана мова діє тепер <strong>усюди</strong>: інтерфейс, екран входу, вебпанель і навіть слайди встановлювача, які раніше лишалися англійськими. Італійська, англійська, польська та українська — а якщо перекладу бракує, буде англійська.<br><br>Усередині: ядро <strong>7.1.7</strong> з розблокуванням 40 обчислювальних блоків і восьми ядер, встановлення на Btrfs із точками відновлення від першого запуску та локальний ШІ на GPU. Свіже встановлення піднімається з <strong>усіма справними службами</strong>.<br><br>Видання <strong>Slim</strong> більше не виходить образом: ядро slim лишається в репозиторії для охочих.",
      ru: "<strong>⚠️ Этот образ заменён: пользуйтесь 26.06.4.</strong> В нём было две неполадки, способные остановить установку на BC-250.<br><br>Два издания, <strong>BC-250</strong> и <strong>Generic</strong>, для платы AMD и для любого ПК или виртуальной машины на x86-64.<br><br>Выбранный язык теперь применяется <strong>везде</strong>: интерфейс, экран входа, веб-панель и презентация установщика, которая раньше оставалась английской. Итальянский, английский, польский и украинский — а если перевода нет, показывается английский.<br><br>Внутри: ядро <strong>7.1.7</strong> с разблокировкой 40 вычислительных блоков и восьми ядер, установка на Btrfs с точками восстановления, живыми с первой загрузки, и ИИ на самом устройстве, на GPU. Свежая установка поднимается со <strong>всеми службами в порядке</strong>.<br><br>Издание <strong>Slim</strong> больше не выходит образом: облегчённое ядро остаётся в репозитории для тех, кому оно нужно.",
      es: "<strong>⚠️ Esta imagen ha quedado sustituida: usa la 26.06.4.</strong> Tenía dos fallos que podían detener una instalación en una BC-250.<br><br>Dos ediciones, <strong>BC-250</strong> y <strong>Generic</strong>, para la placa de AMD y para cualquier PC o máquina virtual x86-64.<br><br>El idioma que eliges se aplica ahora <strong>en todas partes</strong>: interfaz, pantalla de acceso, panel web y también la presentación del instalador, que antes se quedaba en inglés. Italiano, inglés, polaco y ucraniano — y si falta una traducción, sale el inglés.<br><br>Por debajo: núcleo <strong>7.1.7</strong> con el desbloqueo de las 40 unidades de cómputo y el de los ocho núcleos, instalación en Btrfs con puntos de restauración vivos desde el primer arranque, e IA en el propio equipo sobre la GPU. Una instalación nueva levanta con <strong>todos los servicios en orden</strong>.<br><br>La edición <strong>Slim</strong> ya no sale como imagen: el núcleo ligero sigue en el repositorio para quien lo quiera.",
      pt: "<strong>⚠️ Esta imagem foi substituída: use a 26.06.4.</strong> Ela tinha duas falhas que podiam travar uma instalação numa BC-250.<br><br>Duas edições, <strong>BC-250</strong> e <strong>Generic</strong>, para a placa da AMD e para qualquer PC ou máquina virtual x86-64.<br><br>O idioma escolhido agora vale <strong>em tudo</strong>: interface, tela de acesso, painel web e também a apresentação do instalador, que antes ficava em inglês. Italiano, inglês, polonês e ucraniano — e se faltar uma tradução, aparece o inglês.<br><br>Por baixo: kernel <strong>7.1.7</strong> com o destravamento das 40 unidades de computação e o dos oito núcleos, instalação em Btrfs com pontos de restauração vivos desde o primeiro boot, e IA no próprio aparelho pela GPU. Uma instalação nova sobe com <strong>todos os serviços saudáveis</strong>.<br><br>A edição <strong>Slim</strong> não sai mais como imagem: o kernel enxuto continua no repositório para quem quiser.",
      de: "<strong>⚠️ Dieses Abbild ist überholt: bitte 26.06.4 verwenden.</strong> Es hatte zwei Fehler, die eine Installation auf einer BC-250 stoppen konnten.<br><br>Zwei Ausgaben, <strong>BC-250</strong> und <strong>Generic</strong>, für die AMD-Platine und für jeden x86-64-PC oder jede virtuelle Maschine.<br><br>Die gewählte Sprache gilt jetzt <strong>überall</strong>: Oberfläche, Anmeldebildschirm, Weboberfläche und auch die Präsentation des Installationsprogramms, die früher auf Englisch blieb. Italienisch, Englisch, Polnisch und Ukrainisch — und fehlt eine Übersetzung, kommt Englisch.<br><br>Darunter: Kernel <strong>7.1.7</strong> mit der Freischaltung der 40 Recheneinheiten und der acht Kerne, Btrfs-Installationen mit Wiederherstellungspunkten ab dem ersten Start, und KI auf dem Gerät über die GPU. Eine frische Installation kommt mit <strong>lauter gesunden Diensten</strong> hoch.<br><br>Die Ausgabe <strong>Slim</strong> erscheint nicht mehr als Abbild: der schlanke Kernel bleibt für alle, die ihn möchten, in der Paketquelle.",
      fr: "<strong>⚠️ Cette image est remplacée : utilisez la 26.06.4.</strong> Elle avait deux défauts qui pouvaient arrêter une installation sur une BC-250.<br><br>Deux éditions, <strong>BC-250</strong> et <strong>Générique</strong>, pour la carte AMD et pour n'importe quel PC ou machine virtuelle x86-64.<br><br>La langue que vous choisissez s'applique désormais <strong>partout</strong> : interface, écran de connexion, panneau web et présentation de l'installateur elle aussi, qui restait en anglais. Italien, anglais, polonais et ukrainien — et si une traduction manque, vous avez l'anglais.<br><br>Dessous : noyau <strong>7.1.7</strong> avec le déverrouillage des 40 unités de calcul et celui des huit cœurs, installation sur Btrfs avec des points de restauration actifs dès le premier démarrage, et l'IA sur le GPU. Une installation neuve démarre avec <strong>tous les services en bonne santé</strong>.<br><br>L'édition <strong>Slim</strong> n'est plus livrée en image : le noyau slim reste dans le dépôt pour qui le veut."
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
      ru: "Пять точек восстановления и одна команда, чтобы вернуться",
      es: "Cinco puntos de restauración, y un comando para volver atrás",
      pt: "Cinco pontos de restauração, e um comando para voltar",
      de: "Fünf Wiederherstellungspunkte, und ein Befehl zurück",
      fr: "Cinq points de restauration, et une commande pour revenir en arrière"
    },
    testo: {
      it: "Il sistema si prende cura da solo dei punti di ripristino: ne fa uno <strong>prima</strong> e uno <strong>dopo</strong> ogni operazione di <code>apt</code>, ne tiene <strong>cinque</strong> — tre ordinari e due degli aggiornamenti importanti, quelli che toccano kernel o systemd — e li elenca nel menu di avvio, aggiornato a ogni transazione.<br><br>Dal menu di avvio ci si entra per guardare e recuperare file. Per ripartire davvero da uno di essi c'è un comando nuovo:<br><br><code>sudo skillfish-rollback 12</code><br><br>Al riavvio successivo il sistema è quello di allora. Il sistema di prima non viene cancellato: resta da parte, e <code>--annulla</code> lo rimette al suo posto. La <strong>cartella personale non viene mai toccata</strong>: torna indietro il sistema, i tuoi file restano quelli di adesso.<br><br>Arriva con <code>sudo apt update && sudo apt upgrade</code>, senza reinstallare niente.",
      en: "The system looks after its own restore points: it takes one <strong>before</strong> and one <strong>after</strong> every <code>apt</code> operation, keeps <strong>five</strong> — three ordinary ones and two from the important upgrades, the ones touching the kernel or systemd — and lists them in the boot menu, refreshed on every transaction.<br><br>From the boot menu you go in to look around and rescue files. To actually start again from one of them there is a new command:<br><br><code>sudo skillfish-rollback 12</code><br><br>At the next boot the system is the one from back then. The previous system is not deleted: it is set aside, and <code>--undo</code> puts it back. Your <strong>home directory is never touched</strong>: the system travels back, your files stay as they are.<br><br>It arrives with <code>sudo apt update && sudo apt upgrade</code> — no reinstall needed.",
      pl: "System sam dba o punkty przywracania: robi jeden <strong>przed</strong> i jeden <strong>po</strong> każdej operacji <code>apt</code>, trzyma <strong>pięć</strong> — trzy zwykłe i dwa z ważnych aktualizacji, tych ruszających jądro albo systemd — i wypisuje je w menu startowym, odświeżanym przy każdej transakcji.<br><br>Z menu startowego wchodzi się, żeby rozejrzeć się i uratować pliki. Żeby naprawdę wystartować od nowa z któregoś z nich, jest nowe polecenie:<br><br><code>sudo skillfish-rollback 12</code><br><br>Przy następnym uruchomieniu system jest tym sprzed. Poprzedni system nie zostaje skasowany: leży z boku, a <code>--undo</code> stawia go z powrotem. <strong>Katalog domowy nie jest nigdy ruszany</strong>: cofa się system, twoje pliki zostają takie, jakie są.<br><br>Przychodzi z <code>sudo apt update && sudo apt upgrade</code>, bez żadnej reinstalacji.",
      uk: "Система сама дбає про точки відновлення: створює одну <strong>перед</strong> і одну <strong>після</strong> кожної дії <code>apt</code>, тримає <strong>п'ять</strong> — три звичайні та дві з важливих оновлень, тих, що чіпають ядро або systemd, — і показує їх у меню завантаження, оновлюваному щоразу.<br><br>З меню завантаження заходять, щоб роздивитися і врятувати файли. Щоб справді почати знову з однієї з них, є нова команда:<br><br><code>sudo skillfish-rollback 12</code><br><br>Після наступного запуску система буде тією, що тоді. Попередню систему не вилучають: вона лишається збоку, а <code>--undo</code> повертає її на місце. <strong>Домашню теку не чіпають ніколи</strong>: назад повертається система, ваші файли лишаються теперішніми.<br><br>Приходить із <code>sudo apt update && sudo apt upgrade</code>, без перевстановлення.",
      ru: "Система сама следит за своими точками восстановления: снимает одну <strong>до</strong> и одну <strong>после</strong> каждой операции <code>apt</code>, хранит <strong>пять</strong> — три обычные и две от важных обновлений, тех, что затрагивают ядро или systemd, — и показывает их в загрузочном меню, обновляя список при каждой транзакции.<br><br>Из загрузочного меню можно зайти осмотреться и спасти файлы. А чтобы действительно начать заново с одной из них, появилась новая команда:<br><br><code>sudo skillfish-rollback 12</code><br><br>При следующей загрузке система будет та, что была тогда. Прежняя не удаляется: она отложена в сторону, и <code>--undo</code> возвращает её обратно. Домашний каталог <strong>не трогается никогда</strong>: назад едет система, ваши файлы остаются как есть.<br><br>Приходит с <code>sudo apt update && sudo apt upgrade</code> — переустанавливать ничего не нужно.",
      es: "El sistema se ocupa solo de sus puntos de restauración: toma uno <strong>antes</strong> y otro <strong>después</strong> de cada operación de <code>apt</code>, guarda <strong>cinco</strong> — tres normales y dos de las actualizaciones importantes, las que tocan el núcleo o systemd — y los lista en el menú de arranque, actualizándolos en cada transacción.<br><br>Desde el menú de arranque puedes entrar a mirar y rescatar archivos. Para empezar de nuevo de verdad desde uno de ellos hay un comando nuevo:<br><br><code>sudo skillfish-rollback 12</code><br><br>En el siguiente arranque el sistema es el de entonces. El anterior no se borra: queda apartado, y <code>--undo</code> lo devuelve. Tu <strong>carpeta personal no se toca nunca</strong>: el sistema viaja atrás, tus archivos se quedan como están.<br><br>Llega con <code>sudo apt update && sudo apt upgrade</code> — no hace falta reinstalar.",
      pt: "O sistema cuida sozinho dos seus pontos de restauração: tira um <strong>antes</strong> e um <strong>depois</strong> de cada operação do <code>apt</code>, guarda <strong>cinco</strong> — três comuns e dois das atualizações importantes, as que mexem no kernel ou no systemd — e os lista no menu de boot, atualizado a cada transação.<br><br>Pelo menu de boot dá para entrar, olhar e resgatar arquivos. Para de fato recomeçar a partir de um deles existe um comando novo:<br><br><code>sudo skillfish-rollback 12</code><br><br>No boot seguinte o sistema é o daquela época. O anterior não é apagado: fica guardado de lado, e o <code>--undo</code> o traz de volta. Sua <strong>pasta pessoal nunca é tocada</strong>: o sistema volta no tempo, seus arquivos ficam como estão.<br><br>Chega com <code>sudo apt update && sudo apt upgrade</code> — não precisa reinstalar.",
      de: "Das System kümmert sich selbst um seine Wiederherstellungspunkte: Es legt einen <strong>vor</strong> und einen <strong>nach</strong> jeder <code>apt</code>-Aktion an, behält <strong>fünf</strong> — drei gewöhnliche und zwei von den wichtigen Aktualisierungen, denen am Kernel oder an systemd — und listet sie im Startmenü auf, bei jeder Transaktion aufgefrischt.<br><br>Aus dem Startmenü kannst du hineinschauen und Dateien retten. Um wirklich von einem davon aus neu zu beginnen, gibt es einen neuen Befehl:<br><br><code>sudo skillfish-rollback 12</code><br><br>Beim nächsten Start ist das System das von damals. Das vorherige wird nicht gelöscht: es wird beiseitegelegt, und <code>--undo</code> holt es zurück. Dein <strong>persönlicher Ordner wird nie angerührt</strong>: das System reist zurück, deine Dateien bleiben, wie sie sind.<br><br>Es kommt mit <code>sudo apt update && sudo apt upgrade</code> — neu installieren ist nicht nötig.",
      fr: "Le système s'occupe tout seul de ses points de restauration : il en prend un <strong>avant</strong> et un <strong>après</strong> chaque opération <code>apt</code>, en garde <strong>cinq</strong> — trois ordinaires et deux venant des mises à jour importantes, celles qui touchent au noyau ou à systemd — et les affiche dans le menu de démarrage, rafraîchis à chaque transaction.<br><br>Depuis le menu de démarrage vous entrez pour regarder et récupérer des fichiers. Pour repartir vraiment de l'un d'eux il y a une commande nouvelle :<br><br><code>sudo skillfish-rollback 12</code><br><br>Au démarrage suivant le système est celui d'alors. Le système précédent n'est pas effacé : il est mis de côté, et <code>--undo</code> le remet en place. Votre <strong>dossier personnel n'est jamais touché</strong> : le système remonte le temps, vos fichiers restent tels quels.<br><br>Cela arrive avec <code>sudo apt update && sudo apt upgrade</code> — sans réinstaller."
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
      ru: "ИИ на устройстве переезжает на Unsloth Studio",
      es: "La IA local se muda a Unsloth Studio",
      pt: "A IA local muda para o Unsloth Studio",
      de: "Die KI auf dem Gerät zieht zu Unsloth Studio um",
      fr: "L'IA sur la machine passe à Unsloth Studio"
    },
    testo: {
      it: "Al posto di tre container Docker c'è <strong>un solo servizio nativo</strong>, con la chat e un'API compatibile OpenAI. Docker non è più installato.<br><br>Sulla scheda, con Qwen3-1.7B: <strong>210 token al secondo</strong> sulla GPU via Vulkan contro 41 sulla sola CPU, cioè cinque volte tanto. I modelli si prendono direttamente dal catalogo di Hugging Face. Il servizio ascolta solo in locale: da fuori ci si arriva attraverso il pannello remoto, che autentica con le credenziali di sistema.",
      en: "Instead of three Docker containers there is now <strong>a single native service</strong>, offering both the chat and an OpenAI-compatible API. Docker is no longer installed.<br><br>On the board, with Qwen3-1.7B: <strong>210 tokens per second</strong> on the GPU over Vulkan against 41 on the CPU alone — five times as fast. Models come straight from the Hugging Face catalogue. The service listens on loopback only: from outside you reach it through the remote panel, which authenticates against the system accounts.",
      pl: "Zamiast trzech kontenerów Dockera jest teraz <strong>jedna natywna usługa</strong>, z czatem i API zgodnym z OpenAI. Dockera nie ma już w systemie.<br><br>Na płycie, z Qwen3-1.7B: <strong>210 tokenów na sekundę</strong> na GPU przez Vulkan wobec 41 na samym procesorze — pięć razy szybciej. Modele bierze się wprost z katalogu Hugging Face. Usługa nasłuchuje tylko lokalnie: z zewnątrz dociera się do niej przez panel zdalny, który uwierzytelnia kontami systemowymi.",
      uk: "Замість трьох контейнерів Docker тепер <strong>одна нативна служба</strong> з чатом і сумісним з OpenAI API. Docker більше не встановлюється.<br><br>На платі з Qwen3-1.7B: <strong>210 токенів на секунду</strong> на GPU через Vulkan проти 41 на самому процесорі — уп'ятеро швидше. Моделі беруться просто з каталогу Hugging Face. Служба слухає лише локально: ззовні до неї дістаються через віддалену панель, яка автентифікує системними обліковими записами.",
      ru: "Вместо трёх контейнеров Docker теперь <strong>одна родная служба</strong>, дающая и чат, и API, совместимый с OpenAI. Docker больше не устанавливается.<br><br>На плате, с Qwen3-1.7B: <strong>210 токенов в секунду</strong> на GPU через Vulkan против 41 на одном процессоре — впятеро быстрее. Модели берутся прямо из каталога Hugging Face. Служба слушает только петлевой интерфейс: снаружи к ней попадают через панель удалённого управления, которая проверяет системные учётные записи.",
      es: "En lugar de tres contenedores Docker hay ahora <strong>un único servicio nativo</strong>, que ofrece tanto el chat como una API compatible con OpenAI. Docker ya no se instala.<br><br>En la placa, con Qwen3-1.7B: <strong>210 tokens por segundo</strong> en la GPU con Vulkan frente a 41 solo en CPU — cinco veces más rápido. Los modelos vienen directamente del catálogo de Hugging Face. El servicio escucha solo en loopback: desde fuera se llega por el panel remoto, que autentica con las cuentas del sistema.",
      pt: "No lugar de três contêineres Docker existe agora <strong>um único serviço nativo</strong>, que oferece tanto a conversa quanto uma API compatível com a da OpenAI. O Docker não é mais instalado.<br><br>Na placa, com o Qwen3-1.7B: <strong>210 tokens por segundo</strong> na GPU via Vulkan contra 41 só na CPU — cinco vezes mais rápido. Os modelos vêm direto do catálogo do Hugging Face. O serviço escuta apenas em loopback: de fora chega-se a ele pelo painel remoto, que autentica com as contas do sistema.",
      de: "Statt drei Docker-Containern gibt es jetzt <strong>einen einzigen nativen Dienst</strong>, der sowohl den Chat als auch eine zu OpenAI kompatible Schnittstelle anbietet. Docker wird nicht mehr installiert.<br><br>Auf der Platine, mit Qwen3-1.7B: <strong>210 Token pro Sekunde</strong> auf der GPU über Vulkan gegenüber 41 allein auf der CPU — fünfmal so schnell. Die Modelle kommen direkt aus dem Katalog von Hugging Face. Der Dienst lauscht nur auf dem Loopback: von außen erreicht man ihn über die Fernsteuerung, die sich gegen die Systemkonten anmeldet.",
      fr: "À la place de trois conteneurs Docker il y a maintenant <strong>un seul service natif</strong>, qui offre à la fois la discussion et une interface compatible OpenAI. Docker n'est plus installé.<br><br>Sur la carte, avec Qwen3-1.7B : <strong>210 jetons par seconde</strong> sur le GPU via Vulkan contre 41 sur le CPU seul — cinq fois plus vite. Les modèles viennent directement du catalogue Hugging Face. Le service n'écoute que sur l'interface locale : de l'extérieur on l'atteint par le panneau à distance, qui vérifie les comptes du système."
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
      ru: "SkillFishOS 26.06.2",
      es: "SkillFishOS 26.06.2",
      pt: "SkillFishOS 26.06.2",
      de: "SkillFishOS 26.06.2",
      fr: "SkillFishOS 26.06.2"
    },
    testo: {
      it: 'Immagini rigenerate con le correzioni raccolte dopo il primo mese: lingua della sessione live, AI sulla GPU, gruppi utente. Tre edizioni su SourceForge.',
      en: 'Images rebuilt with the fixes gathered over the first month: live session language, AI on the GPU, user groups. Three editions on SourceForge.',
      pl: "Obrazy zbudowane na nowo z poprawkami zebranymi przez pierwszy miesiąc: język sesji live, AI na GPU, grupy użytkownika. Trzy edycje na SourceForge.",
      uk: "Образи перезібрані з виправленнями, зібраними за перший місяць: мова live-сеансу, ШІ на GPU, групи користувача. Три видання на SourceForge.",
      ru: "Образы пересобраны с исправлениями, накопившимися за первый месяц: язык live-сессии, ИИ на GPU, группы пользователя. Три издания на SourceForge.",
      es: "Imágenes recompiladas con los arreglos reunidos durante el primer mes: idioma de la sesión en vivo, IA en la GPU, grupos del usuario. Tres ediciones en SourceForge.",
      pt: "Imagens recompiladas com as correções reunidas no primeiro mês: idioma da sessão ao vivo, IA na GPU, grupos do usuário. Três edições no SourceForge.",
      de: "Abbilder mit den Korrekturen des ersten Monats neu gebaut: Sprache der Live-Sitzung, KI auf der GPU, Benutzergruppen. Drei Ausgaben auf SourceForge.",
      fr: "Images refaites avec les corrections rassemblées pendant le premier mois : langue de la session live, IA sur le GPU, groupes d'utilisateurs. Trois éditions sur SourceForge."
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
      ru: "Первый публичный выпуск: 26.06 «Aetherium»",
      es: "La primera versión pública: 26.06 «Aetherium»",
      pt: "A primeira versão pública: 26.06 “Aetherium”",
      de: "Die erste öffentliche Version: 26.06 „Aetherium“",
      fr: "La première version publique : 26.06 « Aetherium »"
    },
    testo: {
      it: "Una scheda da mining comprata di seconda mano diventa una console-PC pronta all'uso: kernel su misura con lo sblocco delle 40 Compute Unit, governor SMU, profili di overclock con protezione termica, tema steampunk dal boot al desktop, Steam ed emulatori, AI locale.<br><br>Era nato per far usare e imparare Linux ai miei figli mentre giocano. Il gioco è la carota, gli snapshot sono la rete.",
      en: "A second-hand mining board becomes a ready-to-use console-PC: a custom kernel with the 40 Compute Unit unlock, an SMU governor, overclock profiles with a thermal guard, a steampunk theme from boot to desktop, Steam and emulators, on-device AI.<br><br>It started as a way to get my children using and learning Linux while they game. Gaming is the carrot, snapshots are the net.",
      pl: "Kupiona z drugiej ręki płyta do kopania staje się gotową do użytku konsolą-pecetem: własne jądro z odblokowaniem 40 jednostek obliczeniowych, governor SMU, profile podkręcania z zabezpieczeniem termicznym, motyw steampunk od startu po pulpit, Steam i emulatory, lokalne AI.<br><br>Zaczęło się od tego, żeby moje dzieci używały Linuksa i uczyły się go przy graniu. Granie jest marchewką, migawki są siatką.",
      uk: "Вживана майнінгова плата стає готовою до вжитку консоллю-ПК: власне ядро з розблокуванням 40 обчислювальних блоків, governor SMU, профілі розгону з тепловим захистом, тема steampunk від завантаження до стільниці, Steam та емулятори, локальний ШІ.<br><br>Усе почалося з бажання привчити моїх дітей до Linux, поки вони грають. Гра — це морквина, знімки — сітка.",
      ru: "Подержанная майнинговая плата становится готовым к работе консоль-компьютером: своё ядро с разблокировкой 40 вычислительных блоков, регулятор SMU, профили разгона с тепловой защитой, стимпанк-оформление от загрузки до рабочего стола, Steam и эмуляторы, ИИ на самом устройстве.<br><br>Всё началось с желания приучить моих детей к Linux — чтобы они им пользовались и учились, пока играют. Игры — это морковка, снимки — страховочная сетка.",
      es: "Una placa de minería de segunda mano se convierte en un PC-consola listo para usar: un núcleo propio con el desbloqueo de las 40 unidades de cómputo, un gobernador SMU, perfiles de overclock con protección térmica, estética steampunk desde el arranque hasta el escritorio, Steam y emuladores, IA en el propio equipo.<br><br>Empezó como una forma de que mis hijos usaran y aprendieran Linux mientras juegan. Los juegos son la zanahoria; las instantáneas, la red de seguridad.",
      pt: "Uma placa de mineração de segunda mão vira um PC-console pronto para usar: um kernel próprio com o destravamento das 40 unidades de computação, um governador SMU, perfis de overclock com proteção térmica, visual steampunk do boot até a área de trabalho, Steam e emuladores, IA no próprio aparelho.<br><br>Começou como um jeito de fazer meus filhos usarem e aprenderem Linux enquanto jogam. Os jogos são a cenoura; os snapshots, a rede de segurança.",
      de: "Aus einer gebrauchten Mining-Platine wird ein sofort nutzbarer Konsolen-PC: ein eigener Kernel mit der Freischaltung der 40 Recheneinheiten, ein SMU-Governor, Übertaktungsprofile mit Temperaturschutz, eine Steampunk-Gestaltung vom Start bis zum Schreibtisch, Steam und Emulatoren, KI auf dem Gerät selbst.<br><br>Angefangen hat es als Weg, meine Kinder dazu zu bringen, Linux zu benutzen und zu lernen, während sie spielen. Die Spiele sind die Karotte, die Schnappschüsse das Netz.",
      fr: "Une carte de minage d'occasion devient un PC-console prêt à l'emploi : un noyau sur mesure avec le déverrouillage des 40 unités de calcul, un gouverneur SMU, des profils d'overclock avec une garde thermique, un thème steampunk du démarrage au bureau, Steam et les émulateurs, l'IA sur la machine.<br><br>Tout est parti de l'envie de faire utiliser et apprendre Linux à mes enfants pendant qu'ils jouent. Le jeu est la carotte, les instantanés sont le filet."
    },
  },
];

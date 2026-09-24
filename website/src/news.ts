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
      it: "Nessuna immagine esce senza un'installazione completa su una BC-250 vera, dal primo avvio fino al desktop, e la costruzione si rifiuta di produrre un'immagine se un controllo non passa. Una macchina virtuale non basta: il codice che parla all'hardware della scheda è proprio quello che una macchina virtuale non può eseguire, quindi quello che riguarda la scheda si vede solo sulla scheda.",
      en: "No image ships without a full install on a real BC-250, from the first boot to the desktop, and the build refuses to produce an image when a check fails. A virtual machine is not enough: the code that talks to the board's hardware is exactly what a virtual machine cannot run, so anything that concerns the board shows up only on the board.",
      pl: "Żaden obraz nie wychodzi bez pełnej instalacji na prawdziwej BC-250, od pierwszego uruchomienia po pulpit, a budowanie odmawia wydania obrazu, gdy któryś test nie przejdzie. Maszyna wirtualna nie wystarczy: kod, który rozmawia ze sprzętem płyty, to dokładnie ten, którego maszyna wirtualna nie potrafi wykonać, więc to, co dotyczy płyty, widać tylko na płycie.",
      uk: "Жоден образ не виходить без повного встановлення на справжній BC-250, від першого запуску до стільниці, і збірка відмовляється видати образ, якщо якась перевірка не пройшла. Віртуальної машини замало: код, який говорить із залізом плати, це саме той, який віртуальна машина виконати не може, тож усе, що стосується плати, видно лише на платі.",
      ru: "Ни один образ не выходит без полной установки на настоящую BC-250, от первого запуска до рабочего стола, и сборка отказывается выдать образ, если какая-то проверка не прошла. Виртуальной машины мало: код, который говорит с железом платы, это как раз тот, который виртуальная машина выполнить не может, поэтому всё, что касается платы, видно только на плате.",
      es: "Ninguna imagen sale sin una instalación completa en una BC-250 de verdad, desde el primer arranque hasta el escritorio, y la construcción se niega a producir una imagen si una comprobación no pasa. Una máquina virtual no basta: el código que habla con el hardware de la placa es justamente el que una máquina virtual no puede ejecutar, así que lo que atañe a la placa se ve solo en la placa.",
      pt: "Nenhuma imagem sai sem uma instalação completa numa BC-250 a sério, do primeiro arranque até ao ambiente de trabalho, e a construção recusa-se a produzir uma imagem se uma verificação não passar. Uma máquina virtual não chega: o código que fala com o hardware da placa é precisamente aquele que uma máquina virtual não consegue executar, por isso o que diz respeito à placa vê-se só na placa.",
      de: "Kein Abbild geht raus ohne eine vollständige Installation auf einer echten BC-250, vom ersten Start bis zum Desktop, und der Bau weigert sich, ein Abbild zu erzeugen, wenn eine Prüfung nicht besteht. Eine virtuelle Maschine reicht nicht: der Code, der mit der Hardware der Karte spricht, ist genau der, den eine virtuelle Maschine nicht ausführen kann, also zeigt sich alles, was die Karte betrifft, nur auf der Karte.",
      fr: "Aucune image ne sort sans une installation complète sur une vraie BC-250, du premier démarrage jusqu'au bureau, et la construction refuse de produire une image si un contrôle ne passe pas. Une machine virtuelle ne suffit pas : le code qui parle au matériel de la carte est justement celui qu'une machine virtuelle ne peut pas exécuter, donc ce qui concerne la carte ne se voit que sur la carte.",
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
    // aggiornamento-26-09-48-2026-09-24
    data: '2026-09-24',
    quando: {"it": "24 settembre 2026", "en": "24 September 2026", "pl": "24 września 2026", "uk": "24 вересня 2026", "ru": "24 сентября 2026", "es": "24 de septiembre de 2026", "pt": "24 de setembro de 2026", "de": "24. September 2026", "fr": "24 septembre 2026"},
    etichetta: {"it": "avviso", "en": "warning", "pl": "ostrzeżenie", "uk": "попередження", "ru": "предупреждение", "es": "aviso", "pt": "aviso", "de": "Warnung", "fr": "avertissement"},
    titolo: {
      it: "La BC-250 che si blocca da ferma: installate la 26.09.48",
      en: "A BC-250 that freezes when idle: install 26.09.48",
      pl: "BC-250 zawiesza się bezczynnie: zainstalujcie 26.09.48",
      uk: "BC-250 зависає без діла: встановіть 26.09.48",
      ru: "BC-250 зависает без дела: установите 26.09.48",
      es: "La BC-250 que se bloquea en reposo: instalad la 26.09.48",
      pt: "A BC-250 que bloqueia parada: instalem a 26.09.48",
      de: "Die BC-250 friert im Leerlauf ein: installiert 26.09.48",
      fr: "La BC-250 qui se fige au repos : installez la 26.09.48"
    },
    testo: {
      it: "Lasciata inattiva per un quarto d'ora, la scheda si bloccava e ripartiva solo togliendo corrente. Era il desktop che la mandava in sospensione, e la BC-250 dalla sospensione non si risveglia. Con la <strong>26.09.48</strong> sulla BC-250 la sospensione è spenta; gli altri computer la mantengono. Aggiornate dall'Hub.",
      en: "Left idle for a quarter of an hour, the board froze and came back only after cutting the power. The desktop was putting it to sleep, and the BC-250 does not wake up from sleep. With <strong>26.09.48</strong> sleep is switched off on the BC-250; other computers keep it. Update from the Hub.",
      pl: "Pozostawiona bezczynnie na kwadrans płyta zawieszała się i wracała dopiero po odłączeniu zasilania. To pulpit ją usypiał, a BC-250 nie budzi się z uśpienia. W <strong>26.09.48</strong> usypianie na BC-250 jest wyłączone; inne komputery je zachowują. Zaktualizujcie system z Huba.",
      uk: "Залишена без діла на чверть години, плата зависала й оживала лише після вимкнення живлення. Це робочий стіл переводив її в сон, а BC-250 зі сну не прокидається. У <strong>26.09.48</strong> сон на BC-250 вимкнено; інші комп'ютери його зберігають. Оновіться через Hub.",
      ru: "Оставленная без дела на четверть часа, плата зависала и оживала только после отключения питания. Это рабочий стол отправлял её в сон, а BC-250 из сна не просыпается. В <strong>26.09.48</strong> сон на BC-250 отключён; другие компьютеры его сохраняют. Обновитесь через Hub.",
      es: "Inactiva durante un cuarto de hora, la placa se bloqueaba y solo volvía quitándole la corriente. Era el escritorio el que la suspendía, y la BC-250 no despierta de la suspensión. Con la <strong>26.09.48</strong> la suspensión está desactivada en la BC-250; los demás ordenadores la conservan. Actualizad desde el Hub.",
      pt: "Deixada ociosa durante um quarto de hora, a placa bloqueava e só voltava cortando a corrente. Era o ambiente de trabalho que a suspendia, e a BC-250 não acorda da suspensão. Com a <strong>26.09.48</strong> a suspensão está desligada na BC-250; os outros computadores mantêm-na. Atualizem a partir do Hub.",
      de: "Eine Viertelstunde untätig, fror die Platine ein und kam erst nach Trennen vom Strom zurück. Der Desktop schickte sie in den Ruhezustand, und aus dem wacht die BC-250 nicht auf. Mit <strong>26.09.48</strong> ist der Ruhezustand auf der BC-250 abgeschaltet; andere Computer behalten ihn. Aktualisiert im Hub.",
      fr: "Laissée inactive un quart d'heure, la carte se figeait et ne repartait qu'en coupant le courant. C'était le bureau qui la mettait en veille, et la BC-250 ne sort pas de la veille. Avec la <strong>26.09.48</strong> la veille est désactivée sur la BC-250 ; les autres ordinateurs la conservent. Mettez à jour depuis le Hub."
    },
  },
  {
    // aggiornamento-26-09-46-2026-09-22
    data: '2026-09-22',
    quando: {"it": "22 settembre 2026", "en": "22 September 2026", "pl": "22 września 2026", "uk": "22 вересня 2026", "ru": "22 сентября 2026", "es": "22 de septiembre de 2026", "pt": "22 de setembro de 2026", "de": "22. September 2026", "fr": "22 septembre 2026"},
    etichetta: {"it": "avviso", "en": "warning", "pl": "ostrzeżenie", "uk": "попередження", "ru": "предупреждение", "es": "aviso", "pt": "aviso", "de": "Warnung", "fr": "avertissement"},
    titolo: {
      it: "Giochi che non partono dopo l'aggiornamento: installate la 26.09.46",
      en: "Games not starting after the update: install 26.09.46",
      pl: "Gry nie startują po aktualizacji: zainstalujcie 26.09.46",
      uk: "Ігри не запускаються після оновлення: встановіть 26.09.46",
      ru: "Игры не запускаются после обновления: установите 26.09.46",
      es: "Juegos que no arrancan tras la actualización: instalad la 26.09.46",
      pt: "Jogos que não arrancam depois da atualização: instalem a 26.09.46",
      de: "Spiele starten nach dem Update nicht: installiert 26.09.46",
      fr: "Jeux qui ne démarrent plus après la mise à jour : installez la 26.09.46"
    },
    testo: {
      it: "Se dopo gli ultimi aggiornamenti i giochi di Steam si chiudono subito e la sessione Wayland non parte, aggiornate dall'Hub alla <strong>26.09.46</strong> e riavviate. Se l'Hub non si apre, da terminale basta <code>sudo apt install libllvm21</code>. Con la stessa versione le 40 unità di calcolo si accendono a ogni avvio anche sui sistemi installati da una ISO, e Applica nella pagina CPU del Tuner funziona ovunque.",
      en: "If after the latest updates your Steam games close straight away and the Wayland session does not start, update to <strong>26.09.46</strong> from the Hub and reboot. If the Hub does not open, <code>sudo apt install libllvm21</code> in a terminal is enough. The same version switches the 40 compute units on at every boot on systems installed from an ISO too, and Apply on the Tuner's CPU page works everywhere.",
      pl: "Jeśli po ostatnich aktualizacjach gry ze Steama od razu się zamykają, a sesja Wayland nie startuje, zaktualizujcie system z Huba do <strong>26.09.46</strong> i uruchomcie go ponownie. Jeśli Hub się nie otwiera, wystarczy w terminalu <code>sudo apt install libllvm21</code>. Ta sama wersja włącza 40 jednostek obliczeniowych przy każdym starcie także w systemach zainstalowanych z ISO, a Zastosuj na stronie CPU w Tunerze działa wszędzie.",
      uk: "Якщо після останніх оновлень ігри зі Steam одразу закриваються, а сеанс Wayland не запускається, оновіться через Hub до <strong>26.09.46</strong> і перезавантажтеся. Якщо Hub не відкривається, достатньо в терміналі <code>sudo apt install libllvm21</code>. Та сама версія вмикає 40 обчислювальних блоків під час кожного завантаження і в системах, встановлених з ISO, а «Застосувати» на сторінці CPU у Tuner працює скрізь.",
      ru: "Если после последних обновлений игры из Steam сразу закрываются, а сеанс Wayland не запускается, обновитесь через Hub до <strong>26.09.46</strong> и перезагрузитесь. Если Hub не открывается, достаточно в терминале <code>sudo apt install libllvm21</code>. Та же версия включает 40 вычислительных блоков при каждой загрузке и в системах, установленных с ISO, а «Применить» на странице CPU в Tuner работает везде.",
      es: "Si tras las últimas actualizaciones los juegos de Steam se cierran enseguida y la sesión Wayland no arranca, actualizad desde el Hub a la <strong>26.09.46</strong> y reiniciad. Si el Hub no se abre, basta con <code>sudo apt install libllvm21</code> en un terminal. La misma versión enciende las 40 unidades de cómputo en cada arranque también en los sistemas instalados desde una ISO, y Aplicar en la página CPU del Tuner funciona en todas partes.",
      pt: "Se depois das últimas atualizações os jogos do Steam fecham logo e a sessão Wayland não arranca, atualizem a partir do Hub para a <strong>26.09.46</strong> e reiniciem. Se o Hub não abrir, basta <code>sudo apt install libllvm21</code> num terminal. A mesma versão liga as 40 unidades de computação em cada arranque também nos sistemas instalados a partir de uma ISO, e Aplicar na página CPU do Tuner funciona em todo o lado.",
      de: "Wenn sich eure Steam-Spiele nach den letzten Updates sofort schließen und die Wayland-Sitzung nicht startet, aktualisiert im Hub auf <strong>26.09.46</strong> und startet neu. Öffnet sich der Hub nicht, genügt <code>sudo apt install libllvm21</code> im Terminal. Dieselbe Version schaltet die 40 Recheneinheiten bei jedem Start auch auf Systemen ein, die von einer ISO installiert wurden, und Anwenden auf der CPU-Seite des Tuners funktioniert überall.",
      fr: "Si après les dernières mises à jour vos jeux Steam se ferment aussitôt et la session Wayland ne démarre pas, mettez à jour vers la <strong>26.09.46</strong> depuis le Hub et redémarrez. Si le Hub ne s'ouvre pas, <code>sudo apt install libllvm21</code> dans un terminal suffit. La même version active les 40 unités de calcul à chaque démarrage aussi sur les systèmes installés depuis une ISO, et Appliquer sur la page CPU du Tuner fonctionne partout."
    },
  },
  {
    // vaapi-decodifica-2026-09-22
    data: '2026-09-22',
    quando: {"it": "22 settembre 2026", "en": "22 September 2026", "pl": "22 września 2026", "uk": "22 вересня 2026", "ru": "22 сентября 2026", "es": "22 de septiembre de 2026", "pt": "22 de setembro de 2026", "de": "22. September 2026", "fr": "22 septembre 2026"},
    etichetta: { it: "novità", en: "new", pl: "nowość", uk: "новинка", ru: "новинка", es: "novedad", pt: "novidade", de: "Neu", fr: "nouveauté" },
    titolo: {
      it: "H.264 e H.265 attraverso VA-API sulla BC-250",
      en: "H.264 and H.265 through VA-API on the BC-250",
      pl: "H.264 i H.265 przez VA-API na BC-250",
      uk: "H.264 і H.265 через VA-API на BC-250",
      ru: "H.264 и H.265 через VA-API на BC-250",
      es: "H.264 y H.265 a través de VA-API en la BC-250",
      pt: "H.264 e H.265 através de VA-API na BC-250",
      de: "H.264 und H.265 über VA-API auf der BC-250",
      fr: "H.264 et H.265 via VA-API sur la BC-250"
    },
    testo: {
      it: "Il driver video di SkillFishOS decodifica H.264 e H.265 attraverso VA-API, così un lettore o uno strumento di streaming che cerca l'accelerazione hardware ne trova una su una scheda dove nessun altro driver VA-API si avvia. Misurato sulla scheda in 1920x1080: 119 fotogrammi al secondo con H.264 e 96 con H.265, e ogni immagine esce campione per campione come la fa il decoder di riferimento. Arriva con l'aggiornamento di oggi, nel pacchetto skillfish-vaapi-encoder.",
      en: "The SkillFishOS video driver decodes H.264 and H.265 through VA-API, so a player or a streaming tool looking for hardware acceleration finds some on a board where no other VA-API driver starts at all. Measured on the board at 1920x1080: 119 frames per second with H.264 and 96 with H.265, and every picture comes out sample for sample as the reference decoder makes it. It arrives with today's update, in the skillfish-vaapi-encoder package.",
      pl: "Sterownik wideo SkillFishOS dekoduje H.264 i H.265 przez VA-API, więc odtwarzacz albo narzędzie do transmisji szukające akceleracji sprzętowej znajduje ją na karcie, na której żaden inny sterownik VA-API się nie uruchamia. Zmierzone na karcie w 1920x1080: 119 klatek na sekundę z H.264 i 96 z H.265, a każdy obraz wychodzi próbka po próbce taki, jaki robi go dekoder referencyjny. Przychodzi z dzisiejszą aktualizacją, w pakiecie skillfish-vaapi-encoder.",
      uk: "Відеодрайвер SkillFishOS декодує H.264 і H.265 через VA-API, тож програвач або засіб трансляції, що шукає апаратне прискорення, знаходить його на платі, де жоден інший драйвер VA-API не запускається. Виміряно на платі в 1920x1080: 119 кадрів на секунду з H.264 і 96 з H.265, і кожне зображення виходить відлік за відліком таким, яким його робить еталонний декодер. Надходить із сьогоднішнім оновленням, у пакунку skillfish-vaapi-encoder.",
      ru: "Видеодрайвер SkillFishOS декодирует H.264 и H.265 через VA-API, так что проигрыватель или средство трансляции, ищущее аппаратное ускорение, находит его на плате, где ни один другой драйвер VA-API не запускается. Измерено на плате в 1920x1080: 119 кадров в секунду с H.264 и 96 с H.265, и каждое изображение выходит отсчёт за отсчётом таким, каким его делает эталонный декодер. Приходит с сегодняшним обновлением, в пакете skillfish-vaapi-encoder.",
      es: "El controlador de vídeo de SkillFishOS decodifica H.264 y H.265 a través de VA-API, así un reproductor o una herramienta de emisión que busca aceleración por hardware la encuentra en una placa donde ningún otro controlador VA-API arranca. Medido en la placa a 1920x1080: 119 fotogramas por segundo con H.264 y 96 con H.265, y cada imagen sale muestra a muestra como la hace el decodificador de referencia. Llega con la actualización de hoy, en el paquete skillfish-vaapi-encoder.",
      pt: "O controlador de vídeo do SkillFishOS descodifica H.264 e H.265 através de VA-API, por isso um reprodutor ou uma ferramenta de transmissão que procura aceleração por hardware encontra-a numa placa onde nenhum outro controlador VA-API arranca. Medido na placa a 1920x1080: 119 imagens por segundo com H.264 e 96 com H.265, e cada imagem sai amostra a amostra como a faz o descodificador de referência. Chega com a atualização de hoje, no pacote skillfish-vaapi-encoder.",
      de: "Der Videotreiber von SkillFishOS dekodiert H.264 und H.265 über VA-API, damit ein Abspieler oder ein Streaming-Werkzeug, das Hardwarebeschleunigung sucht, auf einer Karte welche findet, auf der sonst gar kein VA-API-Treiber startet. Auf der Karte bei 1920x1080 gemessen: 119 Bilder pro Sekunde mit H.264 und 96 mit H.265, und jedes Bild kommt Abtastwert für Abtastwert so heraus, wie der Referenzdekoder es macht. Kommt mit dem heutigen Update, im Paket skillfish-vaapi-encoder.",
      fr: "Le pilote vidéo de SkillFishOS décode H.264 et H.265 via VA-API : un lecteur ou un outil de diffusion qui cherche une accélération matérielle en trouve une sur une carte où aucun autre pilote VA-API ne démarre. Mesuré sur la carte en 1920x1080 : 119 images par seconde en H.264 et 96 en H.265, et chaque image sort échantillon par échantillon comme la fait le décodeur de référence. Il arrive avec la mise à jour d'aujourd'hui, dans le paquet skillfish-vaapi-encoder."
    },
  },
  {
    // discover-rimuove-kde-2026-09-21
    data: '2026-09-21',
    quando: {"it": "21 settembre 2026", "en": "21 September 2026", "pl": "21 września 2026", "uk": "21 вересня 2026", "ru": "21 сентября 2026", "es": "21 de septiembre de 2026", "pt": "21 de setembro de 2026", "de": "21. September 2026", "fr": "21 septembre 2026"},
    etichetta: {"it": "avviso", "en": "warning", "pl": "ostrzeżenie", "uk": "попередження", "ru": "предупреждение", "es": "aviso", "pt": "aviso", "de": "Warnung", "fr": "avertissement"},
    titolo: {
      it: "Aggiornate dall'Hub, non da Discover",
      en: "Update from the Hub, not from Discover",
      pl: "Aktualizujcie z Huba, nie z Discover",
      uk: "Оновлюйтеся через Hub, а не Discover",
      ru: "Обновляйтесь через Hub, а не Discover",
      es: "Actualizad desde el Hub, no desde Discover",
      pt: "Atualizem pelo Hub, não pelo Discover",
      de: "Aktualisiert über den Hub, nicht über Discover",
      fr: "Mettez à jour depuis le Hub, pas depuis Discover"
    },
    testo: {
      it: "Debian sta ricompilando Qt e KDE, e in questi giorni Discover può proporre un aggiornamento che rimuove l'intero desktop KDE Plasma insieme a circa 170 pacchetti. Se vedete quella lista, premete Annulla. Il pacchetto skillfish-desktop-guard, che arriva con l'aggiornamento di oggi, adesso fa rifiutare quell'operazione; l'Hub non l'ha mai proposta. Discover esce dalla prossima immagine di installazione. Se è già successo, <a href=\"/docs/risoluzione-problemi\">la pagina dei problemi</a> spiega come riavere il desktop, anche senza snapshot.",
      en: "Debian is rebuilding Qt and KDE, and these days Discover can offer an update that removes the whole KDE Plasma desktop along with about 170 packages. If you see that list, press Cancel. The skillfish-desktop-guard package, which arrives with today's update, now makes that operation fail; the Hub never offered it. Discover leaves the next installation image. If it already happened, <a href=\"/en/docs/risoluzione-problemi\">the troubleshooting page</a> explains how to get the desktop back, even without snapshots.",
      pl: "Debian przebudowuje Qt i KDE i w tych dniach Discover może zaproponować aktualizację, która usuwa cały pulpit KDE Plasma razem z około 170 pakietami. Jeśli zobaczycie taką listę, naciśnijcie Anuluj. Pakiet skillfish-desktop-guard, który przychodzi z dzisiejszą aktualizacją, sprawia teraz, że ta operacja zostaje odrzucona; Hub nigdy jej nie proponował. Discover znika z następnego obrazu instalacyjnego. Jeśli to już się stało, <a href=\"/pl/docs/risoluzione-problemi\">strona rozwiązywania problemów</a> wyjaśnia, jak odzyskać pulpit, także bez migawek.",
      uk: "Debian перезбирає Qt і KDE, і в ці дні Discover може запропонувати оновлення, що видаляє весь робочий стіл KDE Plasma разом із приблизно 170 пакунками. Якщо побачите такий список, натисніть «Скасувати». Пакунок skillfish-desktop-guard, що приходить із сьогоднішнім оновленням, тепер змушує відхилити цю операцію; Hub її ніколи не пропонував. Discover прибираємо з наступного інсталяційного образу. Якщо це вже сталося, <a href=\"/uk/docs/risoluzione-problemi\">сторінка усунення проблем</a> пояснює, як повернути робочий стіл, навіть без знімків.",
      ru: "Debian пересобирает Qt и KDE, и в эти дни Discover может предложить обновление, которое удаляет весь рабочий стол KDE Plasma вместе примерно со 170 пакетами. Если увидите такой список, нажмите «Отмена». Пакет skillfish-desktop-guard, который приходит с сегодняшним обновлением, теперь заставляет отклонить эту операцию; Hub её никогда не предлагал. Discover убираем из следующего установочного образа. Если это уже случилось, <a href=\"/ru/docs/risoluzione-problemi\">страница решения проблем</a> объясняет, как вернуть рабочий стол, даже без снимков.",
      es: "Debian está recompilando Qt y KDE, y estos días Discover puede proponer una actualización que elimina todo el escritorio KDE Plasma junto con unos 170 paquetes. Si veis esa lista, pulsad Cancelar. El paquete skillfish-desktop-guard, que llega con la actualización de hoy, hace ahora que esa operación se rechace; el Hub nunca la propuso. Discover sale de la próxima imagen de instalación. Si ya ha pasado, <a href=\"/es/docs/risoluzione-problemi\">la página de problemas</a> explica cómo recuperar el escritorio, incluso sin instantáneas.",
      pt: "O Debian está a recompilar o Qt e o KDE, e nestes dias o Discover pode propor uma atualização que remove todo o ambiente KDE Plasma junto com cerca de 170 pacotes. Se virem essa lista, carreguem em Cancelar. O pacote skillfish-desktop-guard, que chega com a atualização de hoje, faz agora com que essa operação seja recusada; o Hub nunca a propôs. O Discover sai da próxima imagem de instalação. Se já aconteceu, <a href=\"/pt/docs/risoluzione-problemi\">a página de resolução de problemas</a> explica como recuperar o ambiente de trabalho, mesmo sem snapshots.",
      de: "Debian baut gerade Qt und KDE neu, und in diesen Tagen kann Discover ein Update anbieten, das den ganzen KDE-Plasma-Desktop samt rund 170 Paketen entfernt. Wer diese Liste sieht, drückt Abbrechen. Das Paket skillfish-desktop-guard, das mit dem heutigen Update kommt, lässt diesen Vorgang jetzt scheitern; der Hub hat ihn nie angeboten. Discover fehlt im nächsten Installationsabbild. Wenn es schon passiert ist, erklärt <a href=\"/de/docs/risoluzione-problemi\">die Seite zur Fehlerbehebung</a>, wie der Desktop zurückkommt, auch ohne Schnappschüsse.",
      fr: "Debian reconstruit Qt et KDE, et ces jours-ci Discover peut proposer une mise à jour qui supprime tout le bureau KDE Plasma avec environ 170 paquets. Si vous voyez cette liste, appuyez sur Annuler. Le paquet skillfish-desktop-guard, qui arrive avec la mise à jour d'aujourd'hui, fait désormais échouer cette opération ; le Hub ne l'a jamais proposée. Discover quitte la prochaine image d'installation. Si c'est déjà arrivé, <a href=\"/fr/docs/risoluzione-problemi\">la page de dépannage</a> explique comment récupérer le bureau, même sans instantanés."
    },
  },
  {
    // codifica-hardware-2026-09-21
    data: '2026-09-21',
    quando: { it: "21 settembre 2026", en: "21 September 2026", pl: "21 września 2026", uk: "21 вересня 2026", ru: "21 сентября 2026", es: "21 de septiembre de 2026", pt: "21 de setembro de 2026", de: "21. September 2026", fr: "21 septembre 2026" },
    etichetta: { it: "novità", en: "new", pl: "nowość", uk: "новинка", ru: "новинка", es: "novedad", pt: "novidade", de: "Neu", fr: "nouveauté" },
    titolo: {
      it: "Codifica H.264 e HEVC sulla scheda",
      en: "H.264 and HEVC encoding on the board",
      pl: "Kodowanie H.264 i HEVC na płycie",
      uk: "Кодування H.264 і HEVC на платі",
      ru: "Кодирование H.264 и HEVC на плате",
      es: "Codificación H.264 y HEVC en la placa",
      pt: "Codificação H.264 e HEVC na placa",
      de: "H.264- und HEVC-Kodierung auf der Platine",
      fr: "Encodage H.264 et HEVC sur la carte"
    },
    testo: {
      it: "La BC-250 non ha un motore video: finora registrare una partita o trasmetterla toccava al processore, e si sentiva. Adesso c'è un driver che comprime in H.264 e in HEVC usando le 40 unità di calcolo della scheda. Con un gioco davvero in corso, registrare gli costa il 13 per cento, e la registrazione tiene i 60 fotogrammi al secondo senza perderne. Arriva con l'aggiornamento e si accende da solo, ma soltanto su una BC-250.",
      en: "The BC-250 has no video engine: until now, recording a game or streaming it fell to the processor, and you could tell. There is now a driver that compresses in H.264 and in HEVC using the board's 40 compute units. With a game actually running, recording costs it 13 per cent, and the recording holds 60 frames a second without dropping any. It arrives with the update and switches itself on, but only on a BC-250.",
      pl: "BC-250 nie ma silnika wideo: dotąd nagrywanie gry albo jej transmisja spadały na procesor i było to słychać. Teraz jest sterownik, który kompresuje w H.264 i w HEVC na 40 jednostkach obliczeniowych płyty. Przy naprawdę działającej grze nagrywanie kosztuje ją 13 procent, a nagranie trzyma 60 klatek na sekundę, nie gubiąc żadnej. Przychodzi z aktualizacją i włącza się sam, ale wyłącznie na BC-250.",
      uk: "У BC-250 немає відеорушія: досі запис гри або її трансляція лягали на процесор, і це було помітно. Тепер є драйвер, який стискає у H.264 і в HEVC на 40 обчислювальних блоках плати. За реально запущеної гри запис коштує їй 13 відсотків, а сам запис тримає 60 кадрів на секунду, не втрачаючи жодного. Він приходить з оновленням і вмикається сам, але лише на BC-250.",
      ru: "У BC-250 нет видеодвижка: до сих пор запись игры или её трансляция ложились на процессор, и это было заметно. Теперь есть драйвер, который сжимает в H.264 и в HEVC на 40 вычислительных блоках платы. При реально идущей игре запись стоит ей 13 процентов, а сама запись держит 60 кадров в секунду, не теряя ни одного. Он приходит с обновлением и включается сам, но только на BC-250.",
      es: "La BC-250 no tiene motor de vídeo: hasta ahora grabar una partida o retransmitirla le tocaba al procesador, y se notaba. Ahora hay un controlador que comprime en H.264 y en HEVC usando las 40 unidades de cálculo de la placa. Con un juego funcionando de verdad, grabar le cuesta un 13 por ciento, y la grabación mantiene 60 imágenes por segundo sin perder ninguna. Llega con la actualización y se enciende solo, pero únicamente en una BC-250.",
      pt: "A BC-250 não tem motor de vídeo: até agora gravar um jogo ou transmiti-lo cabia ao processador, e notava-se. Agora há um controlador que comprime em H.264 e em HEVC usando as 40 unidades de cálculo da placa. Com um jogo a correr a sério, gravar custa-lhe 13 por cento, e a gravação aguenta 60 imagens por segundo sem perder nenhuma. Chega com a atualização e liga-se sozinho, mas só numa BC-250.",
      de: "Die BC-250 hat keine Video-Engine: bisher blieb das Aufzeichnen eines Spiels oder sein Streamen am Prozessor hängen, und das merkte man. Jetzt gibt es einen Treiber, der in H.264 und in HEVC auf den 40 Recheneinheiten der Platine komprimiert. Während ein Spiel wirklich läuft, kostet ihn das Aufzeichnen 13 Prozent, und die Aufnahme hält 60 Bilder pro Sekunde, ohne eines zu verlieren. Er kommt mit dem Update und schaltet sich selbst ein, aber nur auf einer BC-250.",
      fr: "La BC-250 n'a pas de moteur vidéo : jusqu'ici, enregistrer une partie ou la diffuser revenait au processeur, et cela se voyait. Il existe maintenant un pilote qui compresse en H.264 et en HEVC sur les 40 unités de calcul de la carte. Avec un jeu réellement en cours, l'enregistrement lui coûte 13 pour cent, et il tient 60 images par seconde sans en perdre une. Il arrive avec la mise à jour et s'active tout seul, mais uniquement sur une BC-250."
    },
  },
  {
    // limite-termico-95-2026-09-20
    data: '2026-09-20',
    quando: { it: "20 settembre 2026", en: "20 September 2026", pl: "20 września 2026", uk: "20 вересня 2026", ru: "20 сентября 2026", es: "20 de septiembre de 2026", pt: "20 de setembro de 2026", de: "20. September 2026", fr: "20 septembre 2026" },
    etichetta: { it: "novità", en: "new", pl: "nowość", uk: "новинка", ru: "новинка", es: "novedad", pt: "novidade", de: "Neu", fr: "nouveauté" },
    titolo: {
      it: "La scheda rallentava dieci gradi troppo presto",
      en: "The board was slowing down ten degrees too early",
      pl: "Płyta zwalniała o dziesięć stopni za wcześnie",
      uk: "Плата сповільнювалася на десять градусів зарано",
      ru: "Плата замедлялась на десять градусов раньше времени",
      es: "La placa frenaba diez grados antes de tiempo",
      pt: "A placa abrandava dez graus cedo demais",
      de: "Die Platine bremste zehn Grad zu früh",
      fr: "La carte ralentissait dix degrés trop tôt"
    },
    testo: {
      it: "SkillFishOS teneva il processore a 85 gradi, mentre il firmware della BC-250 ne chiede 95: era la nostra impostazione a scrivere sopra quella della scheda, a ogni avvio. Adesso il limite è 95 nel Tuner, nella pagina del Remote Manager e in tutti i profili pronti. Una macchina già installata ci passa da sola al primo aggiornamento, a meno che quel numero non sia stato cambiato a mano. Sotto carico il processore tiene la frequenza fino a dieci gradi più a lungo prima che la guardia termica intervenga.",
      en: "SkillFishOS held the processor to 85 degrees while the BC-250's own firmware asks for 95: it was our setting writing over the board's, at every boot. The limit is now 95 in the Tuner, on the Remote Manager page and in every preset. A machine already installed moves over by itself at the first update, unless that number had been changed by hand. Under load the processor keeps its clock for up to ten degrees longer before the thermal guard steps in.",
      pl: "SkillFishOS trzymał procesor na 85 stopniach, podczas gdy oprogramowanie układowe BC-250 żąda 95: to nasze ustawienie nadpisywało ustawienie płyty przy każdym starcie. Teraz granica to 95 w Tunerze, na stronie Remote Managera i we wszystkich gotowych profilach. Maszyna już zainstalowana przechodzi na nią sama przy pierwszej aktualizacji, chyba że ta liczba została zmieniona ręcznie. Pod obciążeniem procesor utrzymuje zegar nawet o dziesięć stopni dłużej, zanim wkroczy strażnik termiczny.",
      uk: "SkillFishOS тримав процесор на 85 градусах, тоді як прошивка BC-250 просить 95: це наше налаштування переписувало налаштування плати при кожному завантаженні. Тепер межа становить 95 у Tuner, на сторінці Remote Manager і в усіх готових профілях. Уже встановлена машина переходить сама при першому оновленні, якщо тільки це число не змінювали вручну. Під навантаженням процесор тримає частоту до десяти градусів довше, перш ніж втрутиться теплова охорона.",
      ru: "SkillFishOS держал процессор на 85 градусах, тогда как прошивка BC-250 просит 95: это наша настройка переписывала настройку платы при каждой загрузке. Теперь предел составляет 95 в Tuner, на странице Remote Manager и во всех готовых профилях. Уже установленная машина переходит сама при первом обновлении, если только это число не меняли вручную. Под нагрузкой процессор держит частоту до десяти градусов дольше, прежде чем вмешается тепловая защита.",
      es: "SkillFishOS mantenía el procesador a 85 grados, mientras que el firmware de la BC-250 pide 95: era nuestro ajuste el que escribía encima del de la placa, en cada arranque. Ahora el límite es 95 en el Tuner, en la página del Remote Manager y en todos los perfiles preparados. Una máquina ya instalada pasa a él sola en la primera actualización, salvo que ese número se hubiera cambiado a mano. Bajo carga el procesador mantiene la frecuencia hasta diez grados más antes de que intervenga la guardia térmica.",
      pt: "O SkillFishOS mantinha o processador a 85 graus, enquanto o firmware da BC-250 pede 95: era a nossa definição a escrever por cima da da placa, em cada arranque. Agora o limite é 95 no Tuner, na página do Remote Manager e em todos os perfis prontos. Uma máquina já instalada passa a ele sozinha na primeira atualização, a não ser que esse número tenha sido mudado à mão. Sob carga o processador mantém a frequência até dez graus mais tempo antes de a guarda térmica intervir.",
      de: "SkillFishOS hielt den Prozessor bei 85 Grad, während die Firmware der BC-250 selbst 95 verlangt: unsere Einstellung überschrieb die der Platine, bei jedem Start. Jetzt liegt die Grenze bei 95 im Tuner, auf der Seite des Remote Manager und in allen Voreinstellungen. Eine bereits installierte Maschine wechselt beim ersten Update von selbst, es sei denn, die Zahl wurde von Hand geändert. Unter Last hält der Prozessor seinen Takt bis zu zehn Grad länger, bevor der Temperaturwächter eingreift.",
      fr: "SkillFishOS tenait le processeur à 85 degrés alors que le micrologiciel de la BC-250 en demande 95 : c'était notre réglage qui écrasait celui de la carte, à chaque démarrage. La limite est désormais de 95 dans le Tuner, sur la page du Remote Manager et dans tous les préréglages. Une machine déjà installée y passe d'elle-même à la première mise à jour, sauf si ce nombre avait été changé à la main. En charge le processeur garde sa fréquence jusqu'à dix degrés plus longtemps avant que la garde thermique n'intervienne."
    },
  },
  {
    // gddr6-temperature-2026-09-20
    data: '2026-09-20',
    quando: { it: "20 settembre 2026", en: "20 September 2026", pl: "20 września 2026", uk: "20 вересня 2026", ru: "20 сентября 2026", es: "20 de septiembre de 2026", pt: "20 de setembro de 2026", de: "20. September 2026", fr: "20 septembre 2026" },
    etichetta: { it: "novità", en: "new", pl: "nowość", uk: "новинка", ru: "новинка", es: "novedad", pt: "novidade", de: "Neu", fr: "nouveauté" },
    titolo: {
      it: "La temperatura della memoria, che non si poteva leggere",
      en: "The memory temperature nobody could read",
      pl: "Temperatura pamięci, której nie dało się odczytać",
      uk: "Температура пам'яті, яку не можна було прочитати",
      ru: "Температура памяти, которую нельзя было прочитать",
      es: "La temperatura de la memoria que no se podía leer",
      pt: "A temperatura da memória que não se conseguia ler",
      de: "Die Speichertemperatur, die niemand auslesen konnte",
      fr: "La température de la mémoire qu'on ne pouvait pas lire"
    },
    testo: {
      it: "Ogni chip di memoria della BC-250 ha dentro un sensore di temperatura, ma non compare fra i sensori del sistema: risponde soltanto alla SMU. Adesso si leggono tutti e otto, dal Monitor, dal Control Center e dal browser, sul disegno della scheda vera con il punto più caldo evidenziato. La lettura si accende quando la chiedi e si ferma quando lo dici tu. A riposo la memoria sta sui 44 gradi, sotto gioco sui 49 con punte di 60.",
      en: "Every memory chip on the BC-250 has a temperature sensor inside it, but it does not show up among the system's sensors: it answers only to the SMU. All eight can be read now, from the Monitor, from the Control Center and from a browser, on a drawing of the real board with the hottest one called out. The reading starts when you ask for it and stops when you say so. At rest the memory sits around 44 degrees, under a game around 49 with peaks of 60.",
      pl: "Każdy układ pamięci w BC-250 ma w środku czujnik temperatury, ale nie pojawia się on wśród czujników systemu: odpowiada tylko SMU. Teraz można odczytać wszystkie osiem, z Monitora, z Centrum sterowania i z przeglądarki, na rysunku prawdziwej płyty z wyróżnionym najgorętszym. Odczyt włącza się, gdy o niego poprosisz, i kończy, gdy powiesz. W spoczynku pamięć ma około 44 stopni, w grze około 49 ze szczytami 60.",
      uk: "Кожна мікросхема пам'яті на BC-250 має всередині датчик температури, але він не з'являється серед системних датчиків: він відповідає лише SMU. Тепер можна читати всі вісім — з Монітора, з Центру керування і з браузера — на рисунку справжньої плати з виділеною найгарячішою. Читання вмикається, коли ви його просите, і зупиняється, коли скажете. У спокої пам'ять тримає близько 44 градусів, у грі близько 49 з піками до 60.",
      ru: "У каждой микросхемы памяти на BC-250 внутри есть датчик температуры, но он не появляется среди системных датчиков: он отвечает только SMU. Теперь можно прочитать все восемь — из Монитора, из Центра управления и из браузера — на рисунке настоящей платы с выделенной самой горячей. Чтение включается, когда вы его просите, и останавливается, когда скажете. В покое память держит около 44 градусов, в игре около 49 с пиками до 60.",
      es: "Cada chip de memoria de la BC-250 lleva dentro un sensor de temperatura, pero no aparece entre los sensores del sistema: solo responde a la SMU. Ahora se pueden leer los ocho, desde el Monitor, desde el Centro de control y desde el navegador, sobre un dibujo de la placa real con el más caliente destacado. La lectura se enciende cuando la pides y se para cuando tú lo dices. En reposo la memoria ronda los 44 grados, jugando unos 49 con picos de 60.",
      pt: "Cada chip de memória da BC-250 tem lá dentro um sensor de temperatura, mas não aparece entre os sensores do sistema: só responde à SMU. Agora podem ler-se os oito, a partir do Monitor, do Centro de controlo e do navegador, sobre um desenho da placa real com o mais quente destacado. A leitura liga-se quando a pede e para quando o disser. Em repouso a memória anda pelos 44 graus, a jogar uns 49 com picos de 60.",
      de: "Jeder Speicherbaustein der BC-250 hat innen einen Temperatursensor, der aber unter den Sensoren des Systems nicht auftaucht: er antwortet nur der SMU. Jetzt lassen sich alle acht auslesen, im Monitor, im Kontrollzentrum und im Browser, auf einer Zeichnung der echten Platine mit hervorgehobenem heißesten Baustein. Die Messung startet, wenn Sie sie anfordern, und hört auf, wenn Sie es sagen. Im Leerlauf liegt der Speicher bei etwa 44 Grad, im Spiel bei etwa 49 mit Spitzen von 60.",
      fr: "Chaque puce mémoire de la BC-250 contient un capteur de température, mais il n'apparaît pas parmi les capteurs du système : il ne répond qu'au SMU. Les huit se lisent désormais, depuis le Monitor, depuis le Centre de contrôle et depuis un navigateur, sur un dessin de la carte réelle avec la plus chaude mise en évidence. La lecture démarre quand vous la demandez et s'arrête quand vous le dites. Au repos la mémoire tourne autour de 44 degrés, en jeu autour de 49 avec des pointes à 60."
    },
  },
  {
    // watt-separati-2026-09-20
    data: '2026-09-20',
    quando: { it: "20 settembre 2026", en: "20 September 2026", pl: "20 września 2026", uk: "20 вересня 2026", ru: "20 сентября 2026", es: "20 de septiembre de 2026", pt: "20 de setembro de 2026", de: "20. September 2026", fr: "20 septembre 2026" },
    etichetta: { it: "correzione", en: "fix", pl: "poprawka", uk: "виправлення", ru: "исправление", es: "corrección", pt: "correção", de: "Korrektur", fr: "correctif" },
    titolo: {
      it: "I watt della GPU erano quelli di tutta la scheda",
      en: "The GPU's watts were the whole board's",
      pl: "Waty GPU były watami całej płyty",
      uk: "Вати GPU були ватами всієї плати",
      ru: "Ватты GPU были ваттами всей платы",
      es: "Los vatios de la GPU eran los de toda la placa",
      pt: "Os watts da GPU eram os da placa inteira",
      de: "Die Watt der GPU waren die der ganzen Platine",
      fr: "Les watts du GPU étaient ceux de toute la carte"
    },
    testo: {
      it: "Il Monitor scriveva «GPU» accanto a un numero che era il consumo di tutta la scheda: trenta watt a riposo, mentre la grafica ne tira quattro. Adesso i numeri sono tre e separati, e si leggono nel Monitor, nel Control Center e dal browser: la scheda intera, la CPU e la GPU. Sull'HUD in gioco resta quello che conta lì, il consumo di tutta la scheda, e adesso c'è scritto APU. Già che c'eravamo, i grafici hanno smesso di esagerare: una ventola che gira regolare non riempie più il riquadro come un ottovolante per trenta giri di differenza.",
      en: "The Monitor wrote «GPU» next to a number that was the whole board's draw: thirty watts at idle, while the graphics were pulling four. There are three separate numbers now, in the Monitor, in the Control Center and from a browser: the whole board, the CPU and the GPU. The in-game HUD keeps the one that matters there, what the whole board draws, and now it says APU. While we were at it the charts stopped exaggerating: a fan running steadily no longer fills its box like a rollercoaster over thirty RPM.",
      pl: "Monitor pisał „GPU” obok liczby, która była poborem całej płyty: trzydzieści watów na biegu jałowym, podczas gdy grafika brała cztery. Teraz liczby są trzy i osobne, w Monitorze, w Centrum sterowania i z przeglądarki: cała płyta, procesor i grafika. HUD w grze zachowuje tę, która tam się liczy, czyli pobór całej płyty, i teraz pisze APU. Przy okazji wykresy przestały wyolbrzymiać: równo pracujący wentylator nie wypełnia już całego pola jak kolejka górska przez trzydzieści obrotów różnicy.",
      uk: "Монітор писав «GPU» біля числа, яке було споживанням усієї плати: тридцять ватів у спокої, тоді як графіка брала чотири. Тепер чисел три і вони окремі: уся плата, процесор і відеоядро — у Моніторі, у Центрі керування і з браузера. HUD у грі залишає те, що там важливе, тобто споживання всієї плати, і тепер пише APU. Заодно графіки перестали перебільшувати: рівно працюючий вентилятор більше не заповнює весь квадрат через тридцять обертів різниці.",
      ru: "Монитор писал «GPU» рядом с числом, которое было потреблением всей платы: тридцать ватт в покое, тогда как графика брала четыре. Теперь чисел три и они разделены: вся плата, процессор и видеоядро — в Мониторе, в Центре управления и из браузера. HUD в игре оставляет то, что там важно, то есть потребление всей платы, и теперь пишет APU. Заодно графики перестали преувеличивать: ровно работающий вентилятор больше не заполняет весь квадрат из-за тридцати оборотов разницы.",
      es: "El Monitor escribía «GPU» junto a un número que era el consumo de toda la placa: treinta vatios en reposo, mientras la gráfica tiraba cuatro. Ahora los números son tres y separados, en el Monitor, en el Centro de control y desde el navegador: la placa entera, la CPU y la GPU. El HUD en el juego mantiene el que allí importa, el consumo de toda la placa, y ahora pone APU. Ya puestos, las gráficas han dejado de exagerar: un ventilador que gira regular ya no llena el recuadro como una montaña rusa por treinta revoluciones de diferencia.",
      pt: "O Monitor escrevia «GPU» ao lado de um número que era o consumo da placa inteira: trinta watts em repouso, enquanto a gráfica puxava quatro. Agora os números são três e separados, no Monitor, no Centro de controlo e a partir do navegador: a placa inteira, o CPU e a GPU. O HUD no jogo mantém aquele que ali interessa, o consumo da placa inteira, e agora diz APU. Já agora, os gráficos deixaram de exagerar: uma ventoinha que roda certa já não enche o quadro como uma montanha-russa por trinta rotações de diferença.",
      de: "Der Monitor schrieb «GPU» neben eine Zahl, die der Verbrauch der ganzen Platine war: dreißig Watt im Leerlauf, während die Grafik vier zog. Jetzt sind es drei getrennte Zahlen, im Monitor, im Kontrollzentrum und im Browser: die ganze Platine, die CPU und die GPU. Das HUD im Spiel behält die, auf die es dort ankommt, den Verbrauch der ganzen Platine, und schreibt nun APU. Bei der Gelegenheit haben die Diagramme aufgehört zu übertreiben: ein gleichmäßig laufender Lüfter füllt sein Feld nicht mehr wie eine Achterbahn wegen dreißig Umdrehungen Unterschied.",
      fr: "Le Monitor écrivait « GPU » à côté d'un nombre qui était la consommation de toute la carte : trente watts au repos, alors que la partie graphique en tirait quatre. Il y a maintenant trois nombres séparés, dans le Monitor, dans le Centre de contrôle et depuis un navigateur : la carte entière, le processeur et le GPU. Le HUD en jeu garde celui qui compte là, la consommation de toute la carte, et affiche désormais APU. Au passage, les graphiques ont cessé d'exagérer : un ventilateur qui tourne régulier ne remplit plus son cadre comme des montagnes russes pour trente tours d'écart."
    },
  },
  {
    // flatpak-elenco-2026-09-18
    data: '2026-09-18',
    quando: { it: "18 settembre 2026", en: "18 September 2026", pl: "18 września 2026", uk: "18 вересня 2026", ru: "18 сентября 2026", es: "18 de septiembre de 2026", pt: "18 de setembro de 2026", de: "18. September 2026", fr: "18 septembre 2026" },
    etichetta: { it: "correzione", en: "fix", pl: "poprawka", uk: "виправлення", ru: "исправление", es: "corrección", pt: "correção", de: "Korrektur", fr: "correctif" },
    titolo: {
      it: "Gli aggiornamenti flatpak che non se ne andavano mai",
      en: "The flatpak updates that never went away",
      pl: "Aktualizacje flatpaka, które nigdy nie znikały",
      uk: "Оновлення flatpak, які ніколи не зникали",
      ru: "Обновления flatpak, которые никогда не исчезали",
      es: "Las actualizaciones de flatpak que nunca se iban",
      pt: "As atualizações flatpak que nunca desapareciam",
      de: "Die Flatpak-Aktualisierungen, die nie verschwanden",
      fr: "Les mises à jour flatpak qui ne partaient jamais"
    },
    testo: {
      it: "Aggiornamenti che non se ne andavano mai. Flatpak tiene due archivi separati: quello di sistema e uno per ogni utente, e i programmi installati per il tuo utente — per esempio gli emulatori — stanno nel secondo. «Aggiorna tutto» girava con i permessi di sistema e toccava solo il primo, così quelle voci tornavano a ogni controllo per quante volte le si aggiornasse. Adesso vengono aggiornati tutti e due, i componenti che non usa più nessun programma vengono tolti dopo, e nell'elenco accanto al nome c'è la versione, perché due righe che sembravano uguali erano due versioni diverse della stessa cosa.",
      en: "Updates that never went away. Flatpak keeps two separate stores: the system one and one for each user, and the programs installed for your own user — the emulators, for instance — live in the second. «Update all» ran with system privileges and only ever touched the first, so those entries came back at every check no matter how many times they were updated. Both are updated now, components no program uses any more are removed afterwards, and the list shows the version beside the name, because two rows that looked identical were two different versions of the same thing.",
      pl: "Aktualizacje, które nigdy nie znikały. Flatpak prowadzi dwa osobne magazyny: systemowy i po jednym dla każdego użytkownika, a programy zainstalowane dla twojego użytkownika — na przykład emulatory — są w tym drugim. „Zaktualizuj wszystko” działało z uprawnieniami systemu i ruszało tylko pierwszy, więc te wpisy wracały przy każdym sprawdzeniu, ile razy by ich nie aktualizować. Teraz aktualizowane są oba, składniki, z których nie korzysta już żaden program, są potem usuwane, a lista pokazuje wersję obok nazwy, bo dwa wiersze wyglądające tak samo były dwiema różnymi wersjami tej samej rzeczy.",
      uk: "Оновлення, які ніколи не зникали. Flatpak веде два окремі сховища: системне і по одному на кожного користувача, а програми, встановлені для вашого користувача — наприклад емулятори — лежать у другому. «Оновити все» виконувалося із системними правами й чіпало лише перше, тож ті записи поверталися під час кожної перевірки, скільки б разів їх не оновлювали. Тепер оновлюються обидва, компоненти, якими більше не користується жодна програма, потім прибираються, а список показує версію поряд з назвою: два однакові на вигляд рядки були двома різними версіями того самого.",
      ru: "Обновления, которые никогда не исчезали. Flatpak держит два отдельных хранилища: системное и по одному на каждого пользователя, а программы, установленные для вашего пользователя, — например эмуляторы — лежат во втором. «Обновить всё» выполнялось с системными правами и трогало только первое, поэтому те записи возвращались при каждой проверке, сколько бы раз их ни обновляли. Теперь обновляются оба, компоненты, которыми больше не пользуется ни одна программа, затем удаляются, а список показывает версию рядом с именем: две одинаковые на вид строки были двумя разными версиями одного и того же.",
      es: "Actualizaciones que nunca se iban. Flatpak mantiene dos almacenes separados: el del sistema y uno por cada usuario, y los programas instalados para tu usuario —los emuladores, por ejemplo— están en el segundo. «Actualizar todo» se ejecutaba con permisos del sistema y solo tocaba el primero, así que esas entradas volvían en cada comprobación por muchas veces que se actualizara. Ahora se actualizan los dos, después se quitan los componentes que ya no usa ningún programa, y la lista muestra la versión junto al nombre, porque dos filas que parecían iguales eran dos versiones distintas de lo mismo.",
      pt: "Atualizações que nunca desapareciam. O flatpak mantém dois arquivos separados: o do sistema e um para cada utilizador, e os programas instalados para o seu utilizador — os emuladores, por exemplo — estão no segundo. O «Atualizar tudo» corria com permissões de sistema e só mexia no primeiro, por isso aquelas entradas voltavam em cada verificação por mais vezes que se atualizasse. Agora são atualizados os dois, os componentes que já nenhum programa usa são retirados a seguir, e a lista mostra a versão ao lado do nome, porque duas linhas que pareciam iguais eram duas versões diferentes da mesma coisa.",
      de: "Aktualisierungen, die nie verschwanden. Flatpak führt zwei getrennte Ablagen: die des Systems und eine je Benutzer, und die für Ihren Benutzer installierten Programme — etwa die Emulatoren — liegen in der zweiten. «Alles aktualisieren» lief mit Systemrechten und rührte nur die erste an, also kamen diese Einträge bei jeder Prüfung zurück, so oft man auch aktualisierte. Jetzt werden beide aktualisiert, danach werden Komponenten entfernt, die kein Programm mehr nutzt, und die Liste zeigt die Version neben dem Namen, denn zwei gleich aussehende Zeilen waren zwei verschiedene Versionen derselben Sache.",
      fr: "Des mises à jour qui ne partaient jamais. Flatpak tient deux dépôts séparés : celui du système et un par utilisateur, et les programmes installés pour votre utilisateur — les émulateurs, par exemple — sont dans le second. « Tout mettre à jour » s'exécutait avec les droits du système et ne touchait que le premier : ces entrées revenaient donc à chaque vérification, quel que soit le nombre de mises à jour lancées. Les deux sont désormais mis à jour, les composants que plus aucun programme n'utilise sont ensuite retirés, et la liste affiche la version à côté du nom, car deux lignes identiques étaient deux versions différentes de la même chose."
    },
  },
  {
    // mesa-di-sistema-2026-09-18
    data: '2026-09-18',
    quando: { it: "18 settembre 2026", en: "18 September 2026", pl: "18 września 2026", uk: "18 вересня 2026", ru: "18 сентября 2026", es: "18 de septiembre de 2026", pt: "18 de setembro de 2026", de: "18. September 2026", fr: "18 septembre 2026" },
    etichetta: { it: "novità", en: "new", pl: "nowość", uk: "новинка", ru: "новинка", es: "novedad", pt: "novidade", de: "Neu", fr: "nouveauté" },
    titolo: {
      it: "La nostra Mesa diventa il driver di tutta la scheda",
      en: "Our Mesa becomes the driver of the whole board",
      pl: "Nasza Mesa staje się sterownikiem całej płyty",
      uk: "Наша Mesa стає драйвером усієї плати",
      ru: "Наша Mesa становится драйвером всей платы",
      es: "Nuestra Mesa pasa a ser el controlador de toda la placa",
      pt: "A nossa Mesa passa a ser o driver de toda a placa",
      de: "Unsere Mesa wird zum Treiber der ganzen Platine",
      fr: "Notre Mesa devient le pilote de toute la carte"
    },
    testo: {
      it: "Fino a ieri la Mesa che compiliamo noi la usavano solo i giochi, e tutto il resto della BC-250, desktop compreso, girava su quella della distribuzione. Da questo aggiornamento, su una BC-250 con il nostro kernel, <strong>è il driver della macchina fin dall'avvio</strong>, e Steam e Heroic ci vengono indirizzati da soli, senza accendere niente. I fotogrammi nei giochi restano gli stessi, misurati: 92,3 contro 92,6 in Cyberpunk 2077. Su un PC che non è una BC-250 non cambia nulla, perché il sistema lo riconosce dal firmware e lascia al suo posto il driver di serie: e quella decisione la rifà a ogni avvio, non una volta sola quando si installa.",
      en: "Until yesterday the Mesa we build was used by the games only, and everything else on the BC-250, desktop included, ran on the distribution's one. From this update, on a BC-250 running our kernel, <strong>it is the driver of the machine from the moment it boots</strong>, and Steam and Heroic are pointed at it by themselves, with nothing to switch on. The frame rate in games is the same, measured: 92.3 against 92.6 in Cyberpunk 2077. On a PC that is not a BC-250 nothing changes, because the system recognises the machine from its firmware and leaves the stock driver where it is: and that decision is taken again at every boot, not once at installation.",
      pl: "Do wczoraj Mesa, którą kompilujemy, była używana tylko przez gry, a cała reszta BC-250, łącznie z pulpitem, działała na tej z dystrybucji. Od tej aktualizacji, na BC-250 z naszym jądrem, <strong>jest sterownikiem maszyny od samego startu</strong>, a Steam i Heroic są na nią kierowane same, bez włączania czegokolwiek. Liczba klatek w grach zostaje taka sama, zmierzona: 92,3 wobec 92,6 w Cyberpunk 2077. Na pececie, który nie jest BC-250, nic się nie zmienia, bo system rozpoznaje maszynę po firmware i zostawia fabryczny sterownik na miejscu — a tę decyzję podejmuje przy każdym starcie, nie raz przy instalacji.",
      uk: "До вчора Mesa, яку ми збираємо, використовували лише ігри, а решта BC-250, разом зі стільницею, працювала на дистрибутивній. Від цього оновлення на BC-250 з нашим ядром <strong>вона є драйвером машини від самого запуску</strong>, а Steam і Heroic спрямовуються на неї самі, без вмикання чогось. Кадри в іграх лишаються ті самі, виміряно: 92,3 проти 92,6 у Cyberpunk 2077. На ПК, який не є BC-250, нічого не змінюється, бо система впізнає машину за мікропрограмою і лишає штатний драйвер на місці — і це рішення вона ухвалює під час кожного запуску, а не один раз під час встановлення.",
      ru: "До вчерашнего дня собранную нами Mesa использовали только игры, а всё остальное на BC-250, включая рабочий стол, работало на дистрибутивной. С этим обновлением на BC-250 с нашим ядром <strong>она становится драйвером машины с самого запуска</strong>, а Steam и Heroic направляются на неё сами, ничего включать не нужно. Кадры в играх остаются прежними, по замерам: 92,3 против 92,6 в Cyberpunk 2077. На ПК, который не является BC-250, ничего не меняется: система узнаёт машину по прошивке и оставляет штатный драйвер на месте, и это решение принимается при каждом запуске, а не один раз при установке.",
      es: "Hasta ayer la Mesa que compilamos la usaban solo los juegos, y todo lo demás de la BC-250, escritorio incluido, funcionaba con la de la distribución. Desde esta actualización, en una BC-250 con nuestro kernel, <strong>es el controlador de la máquina desde el arranque</strong>, y Steam y Heroic quedan apuntados a él solos, sin activar nada. Los fotogramas en los juegos se quedan igual, medidos: 92,3 frente a 92,6 en Cyberpunk 2077. En un PC que no es una BC-250 no cambia nada, porque el sistema reconoce la máquina por su firmware y deja el controlador de serie donde está: y esa decisión se vuelve a tomar en cada arranque, no una sola vez al instalar.",
      pt: "Até ontem a Mesa que compilamos era usada só pelos jogos, e todo o resto da BC-250, ambiente de trabalho incluído, corria com a da distribuição. A partir desta atualização, numa BC-250 com o nosso kernel, <strong>é o driver da máquina desde o arranque</strong>, e o Steam e o Heroic ficam apontados para ele sozinhos, sem ligar nada. Os fotogramas nos jogos ficam iguais, medidos: 92,3 contra 92,6 no Cyberpunk 2077. Num PC que não é uma BC-250 nada muda, porque o sistema reconhece a máquina pelo firmware e deixa o driver de série onde está — e essa decisão é refeita em cada arranque, não uma só vez na instalação.",
      de: "Bis gestern nutzten nur die Spiele die Mesa, die wir bauen, und alles andere auf der BC-250, Desktop eingeschlossen, lief mit der aus der Distribution. Mit diesem Update ist sie auf einer BC-250 mit unserem Kernel <strong>ab dem Start der Treiber der Maschine</strong>, und Steam und Heroic werden von selbst darauf gelenkt, ohne dass etwas eingeschaltet wird. Die Bildrate in Spielen bleibt gleich, gemessen: 92,3 gegenüber 92,6 in Cyberpunk 2077. Auf einem PC, der keine BC-250 ist, ändert sich nichts, denn das System erkennt die Maschine an ihrer Firmware und lässt den Serientreiber, wo er ist — und diese Entscheidung fällt bei jedem Start neu, nicht einmal bei der Installation.",
      fr: "Jusqu'à hier, la Mesa que nous compilons ne servait qu'aux jeux, et tout le reste de la BC-250, bureau compris, tournait avec celle de la distribution. À partir de cette mise à jour, sur une BC-250 avec notre noyau, <strong>c'est le pilote de la machine dès le démarrage</strong>, et Steam et Heroic y sont dirigés tout seuls, sans rien activer. Le nombre d'images dans les jeux reste le même, mesuré : 92,3 contre 92,6 dans Cyberpunk 2077. Sur un PC qui n'est pas une BC-250, rien ne change, car le système reconnaît la machine à son micrologiciel et laisse le pilote d'origine en place : et ce choix est refait à chaque démarrage, pas une seule fois à l'installation."
    },
  },
  {
    // cmdline-pulita-2026-09-17
    data: '2026-09-17',
    quando: { it: "17 settembre 2026", en: "17 September 2026", pl: "17 września 2026", uk: "17 вересня 2026", ru: "17 сентября 2026", es: "17 de septiembre de 2026", pt: "17 de setembro de 2026", de: "17. September 2026", fr: "17 septembre 2026" },
    etichetta: { it: "correzione", en: "fix", pl: "poprawka", uk: "виправлення", ru: "исправление", es: "corrección", pt: "correção", de: "Korrektur", fr: "correctif" },
    titolo: {
      it: "Su un PC normale sparisce la memoria bloccata a 6 GB",
      en: "On an ordinary PC the 6 GB memory cap goes away",
      pl: "Na zwykłym pececie znika pamięć zablokowana na 6 GB",
      uk: "На звичайному ПК зникає пам'ять, замкнена на 6 ГБ",
      ru: "На обычном ПК исчезает память, зажатая на 6 ГБ",
      es: "En un PC normal desaparece la memoria limitada a 6 GB",
      pt: "Num PC normal desaparece a memória travada em 6 GB",
      de: "Auf einem normalen PC verschwindet die 6-GB-Speichergrenze",
      fr: "Sur un PC ordinaire, la mémoire bloquée à 6 Go disparaît"
    },
    testo: {
      it: "Chi ha installato SkillFishOS su un PC che non è una BC-250 partiva con impostazioni pensate per la scheda. La più fastidiosa limitava a <strong>6 GB fissi</strong> la memoria utilizzabile dalla parte grafica, mentre il valore giusto è <strong>metà della RAM</strong>: troppo su un PC da 8 GB, troppo poco su uno da 32. Arrivava dall'immagine di installazione, che porta con sé una copia della configurazione di una scheda, quindi ce l'avevano tutti. Adesso il sistema se ne accorge da solo e le toglie, tenendo una copia del file prima di cambiarlo; su una BC-250 vera non cambia niente.",
      en: "Anyone who installed SkillFishOS on a PC that is not a BC-250 was booting with settings meant for the board. The awkward one capped the memory the graphics part may use at a fixed <strong>6 GB</strong>, where the right figure is <strong>half of the RAM</strong>: too much on an 8 GB PC, too little on a 32 GB one. It came from the installation image, which carries a copy of a board's configuration, so every such PC had it. The system now notices by itself and removes them, keeping a copy of the file first; on a real BC-250 nothing changes.",
      pl: "Kto zainstalował SkillFishOS na pececie, który nie jest BC-250, startował z ustawieniami przeznaczonymi dla płyty. Najbardziej dokuczliwe ograniczało pamięć dostępną dla części graficznej do sztywnych <strong>6 GB</strong>, podczas gdy właściwa wartość to <strong>połowa pamięci</strong>: za dużo na pececie z 8 GB, za mało na tym z 32. Brało się to z obrazu instalacyjnego, który niesie kopię konfiguracji płyty, więc miały je wszystkie. Teraz system sam to zauważa i usuwa, zachowując wcześniej kopię pliku; na prawdziwej BC-250 nic się nie zmienia.",
      uk: "Ті, хто встановив SkillFishOS на ПК, який не є BC-250, запускалися з налаштуваннями, призначеними для плати. Найприкріше обмежувало пам'ять для графічної частини жорсткими <strong>6 ГБ</strong>, тоді як правильне значення — <strong>половина оперативної пам'яті</strong>: забагато для ПК з 8 ГБ і замало для ПК із 32. Це приходило зі встановлювального образу, який несе копію налаштувань плати, тож воно було в усіх. Тепер система помічає це сама й прибирає, попередньо зберігши копію файлу; на справжній BC-250 нічого не змінюється.",
      ru: "Те, кто установил SkillFishOS на ПК, который не является BC-250, запускались с настройками, предназначенными для платы. Самая досадная ограничивала память для графической части жёсткими <strong>6 ГБ</strong>, тогда как правильное значение — <strong>половина оперативной памяти</strong>: много для ПК с 8 ГБ и мало для ПК с 32. Это приходило из установочного образа, который несёт копию настроек платы, так что она была у всех. Теперь система замечает это сама и убирает их, предварительно сохранив копию файла; на настоящей BC-250 ничего не меняется.",
      es: "Quien instaló SkillFishOS en un PC que no es una BC-250 arrancaba con ajustes pensados para la placa. El más molesto limitaba a <strong>6 GB fijos</strong> la memoria que puede usar la parte gráfica, cuando el valor correcto es <strong>la mitad de la RAM</strong>: demasiado en un PC de 8 GB, demasiado poco en uno de 32. Venía de la imagen de instalación, que lleva consigo una copia de la configuración de una placa, así que lo tenían todos. Ahora el sistema se da cuenta solo y los quita, guardando antes una copia del archivo; en una BC-250 de verdad no cambia nada.",
      pt: "Quem instalou o SkillFishOS num PC que não é uma BC-250 arrancava com definições pensadas para a placa. A mais incómoda limitava a <strong>6 GB fixos</strong> a memória utilizável pela parte gráfica, quando o valor certo é <strong>metade da RAM</strong>: demasiado num PC de 8 GB, pouco num de 32. Vinha da imagem de instalação, que leva consigo uma cópia da configuração de uma placa, por isso toda a gente a tinha. Agora o sistema dá por isso sozinho e retira-as, guardando antes uma cópia do ficheiro; numa BC-250 a sério não muda nada.",
      de: "Wer SkillFishOS auf einem PC installiert hat, der keine BC-250 ist, startete mit Einstellungen für die Platine. Die unangenehmste begrenzte den Speicher, den der Grafikteil nutzen darf, auf feste <strong>6 GB</strong>, während der richtige Wert <strong>die Hälfte des Arbeitsspeichers</strong> ist: zu viel auf einem 8-GB-PC, zu wenig auf einem mit 32. Sie kam aus dem Installationsabbild, das eine Kopie der Konfiguration einer Platine mitbringt, also hatte sie jeder. Jetzt merkt das System es selbst und nimmt sie heraus, wobei vorher eine Kopie der Datei aufbewahrt wird; auf einer echten BC-250 ändert sich nichts.",
      fr: "Ceux qui ont installé SkillFishOS sur un PC qui n'est pas une BC-250 démarraient avec des réglages prévus pour la carte. Le plus gênant plafonnait à <strong>6 Go fixes</strong> la mémoire utilisable par la partie graphique, alors que la bonne valeur est <strong>la moitié de la RAM</strong> : trop sur un PC de 8 Go, trop peu sur un de 32. Cela venait de l'image d'installation, qui emporte une copie de la configuration d'une carte, donc tout le monde l'avait. Le système s'en aperçoit désormais tout seul et les retire, en conservant d'abord une copie du fichier ; sur une vraie BC-250, rien ne change."
    },
  },
  {
    // kernel-726-2026-09-17
    data: '2026-09-17',
    quando: { it: "17 settembre 2026", en: "17 September 2026", pl: "17 września 2026", uk: "17 вересня 2026", ru: "17 сентября 2026", es: "17 de septiembre de 2026", pt: "17 de setembro de 2026", de: "17. September 2026", fr: "17 septembre 2026" },
    etichetta: { it: "aggiornamento", en: "update", pl: "aktualizacja", uk: "оновлення", ru: "обновление", es: "actualización", pt: "atualização", de: "Aktualisierung", fr: "mise à jour" },
    titolo: {
      it: "Il kernel passa alla 7.2.6",
      en: "The kernel moves up to 7.2.6",
      pl: "Jądro przechodzi na 7.2.6",
      uk: "Ядро переходить на 7.2.6",
      ru: "Ядро переходит на 7.2.6",
      es: "El núcleo pasa a la 7.2.6",
      pt: "O núcleo passa para a 7.2.6",
      de: "Der Kernel geht auf 7.2.6",
      fr: "Le noyau passe à la 7.2.6"
    },
    testo: {
      it: "Il kernel di SkillFishOS passa alla <strong>7.2.6</strong>, l'ultima stabile. Porta <strong>1816 correzioni</strong> da monte rispetto alla 7.2.5, diciassette delle quali nel driver grafico AMD, e nessuna delle quarantatré patch che teniamo per la BC-250 è cambiata. Non c'è niente di nuovo da provare: è manutenzione, e serve perché una scheda lasciata in pace continui a ricevere le correzioni di sicurezza come tutti gli altri. Si aggiorna con <code>apt</code>, e il pacchetto sceglie da sé fra la versione per la BC-250 e quella per qualunque altro PC x86-64.",
      en: "The SkillFishOS kernel moves up to <strong>7.2.6</strong>, the current stable release. It brings <strong>1816 fixes</strong> from upstream over 7.2.5, seventeen of them in the AMD graphics driver, and none of the forty-three patches we carry for the BC-250 has changed. There is nothing new to try: this is maintenance, and it is what keeps a board left alone receiving the same security fixes as everybody else. Update with <code>apt</code>; the package picks by itself between the BC-250 build and the one for any other x86-64 PC.",
      pl: "Jądro SkillFishOS przechodzi na <strong>7.2.6</strong>, obecne stabilne wydanie. Przynosi <strong>1816 poprawek</strong> z góry względem 7.2.5, siedemnaście z nich w sterowniku graficznym AMD, i żadna z czterdziestu trzech łat, które utrzymujemy dla BC-250, się nie zmieniła. Nie ma tu nic nowego do wypróbowania: to konserwacja i dzięki niej płyta, której się nie rusza, wciąż dostaje te same poprawki bezpieczeństwa co wszyscy. Aktualizuje się przez <code>apt</code>, a pakiet sam wybiera między wersją dla BC-250 a tą dla dowolnego innego peceta x86-64.",
      uk: "Ядро SkillFishOS переходить на <strong>7.2.6</strong>, поточний стабільний випуск. Воно приносить <strong>1816 виправлень</strong> згори порівняно з 7.2.5, сімнадцять із них у графічному драйвері AMD, і жодна з сорока трьох латок, які ми тримаємо для BC-250, не змінилася. Тут немає нічого нового, що можна спробувати: це обслуговування, і саме воно дає змогу платі, яку не чіпають, і далі отримувати ті самі виправлення безпеки, що й усі. Оновлюється через <code>apt</code>, а пакунок сам обирає між збіркою для BC-250 і тією, що для будь-якого іншого ПК x86-64.",
      ru: "Ядро SkillFishOS переходит на <strong>7.2.6</strong>, текущий стабильный выпуск. Оно приносит <strong>1816 исправлений</strong> сверху по сравнению с 7.2.5, семнадцать из них в графическом драйвере AMD, и ни одна из сорока трёх заплаток, которые мы держим для BC-250, не изменилась. Пробовать тут нечего: это обслуживание, и именно оно позволяет плате, которую не трогают, и дальше получать те же исправления безопасности, что и все. Обновляется через <code>apt</code>, а пакет сам выбирает между сборкой для BC-250 и той, что для любого другого ПК x86-64.",
      es: "El núcleo de SkillFishOS pasa a la <strong>7.2.6</strong>, la estable actual. Trae <strong>1816 correcciones</strong> de aguas arriba respecto a la 7.2.5, diecisiete de ellas en el controlador gráfico de AMD, y ninguno de los cuarenta y tres parches que mantenemos para la BC-250 ha cambiado. No hay nada nuevo que probar: es mantenimiento, y es lo que hace que una placa a la que no se toca siga recibiendo las mismas correcciones de seguridad que todos. Se actualiza con <code>apt</code>, y el paquete elige solo entre la versión para la BC-250 y la de cualquier otro PC x86-64.",
      pt: "O núcleo do SkillFishOS passa para a <strong>7.2.6</strong>, a estável atual. Traz <strong>1816 correções</strong> de montante em relação à 7.2.5, dezassete delas no controlador gráfico da AMD, e nenhum dos quarenta e três patches que mantemos para a BC-250 mudou. Não há nada de novo para experimentar: é manutenção, e é o que faz com que uma placa deixada em paz continue a receber as mesmas correções de segurança que toda a gente. Atualiza-se com <code>apt</code>, e o pacote escolhe sozinho entre a versão para a BC-250 e a de qualquer outro PC x86-64.",
      de: "Der SkillFishOS-Kernel geht auf <strong>7.2.6</strong>, die aktuelle stabile Ausgabe. Er bringt <strong>1816 Korrekturen</strong> von oben gegenüber 7.2.5, siebzehn davon im AMD-Grafiktreiber, und keiner der dreiundvierzig Patches, die wir für die BC-250 pflegen, hat sich geändert. Es gibt nichts Neues auszuprobieren: das ist Wartung, und sie sorgt dafür, dass eine Platine, die man in Ruhe lässt, weiterhin dieselben Sicherheitskorrekturen bekommt wie alle anderen. Aktualisiert wird mit <code>apt</code>, und das Paket wählt selbst zwischen dem Build für die BC-250 und dem für jeden anderen x86-64-PC.",
      fr: "Le noyau de SkillFishOS passe à la <strong>7.2.6</strong>, la version stable actuelle. Il apporte <strong>1816 corrections</strong> venues de l'amont par rapport à la 7.2.5, dont dix-sept dans le pilote graphique AMD, et aucun des quarante-trois correctifs que nous gardons pour la BC-250 n'a changé. Il n'y a rien de nouveau à essayer : c'est de l'entretien, et c'est ce qui permet à une carte qu'on laisse tranquille de continuer à recevoir les mêmes corrections de sécurité que tout le monde. La mise à jour se fait avec <code>apt</code>, et le paquet choisit tout seul entre la version pour la BC-250 et celle pour n'importe quel autre PC x86-64."
    },
  },
  {
    // cu-pavimento-2026-09-17
    data: '2026-09-17',
    quando: { it: "17 settembre 2026", en: "17 September 2026", pl: "17 września 2026", uk: "17 вересня 2026", ru: "17 сентября 2026", es: "17 de septiembre de 2026", pt: "17 de setembro de 2026", de: "17. September 2026", fr: "17 septembre 2026" },
    etichetta: { it: "novità", en: "new", pl: "nowość", uk: "новинка", ru: "новинка", es: "novedad", pt: "novidade", de: "Neu", fr: "nouveauté" },
    titolo: {
      it: "Anche le prime tre coppie di CU si possono spegnere",
      en: "The first three CU pairs can be switched off too",
      pl: "Trzy pierwsze pary CU też można wyłączyć",
      uk: "Перші три пари CU теж можна вимкнути",
      ru: "Первые три пары CU тоже можно выключить",
      es: "Los tres primeros pares de CU también se pueden apagar",
      pt: "Os três primeiros pares de CU também se podem desligar",
      de: "Auch die ersten drei CU-Paare lassen sich abschalten",
      fr: "Les trois premières paires de CU peuvent aussi être éteintes",
    },
    testo: {
      it: "Il pannello delle Compute Unit teneva grigie le prime tre coppie, perché un nostro commento diceva che le tiene accese il driver. Non è vero, e l'abbiamo misurato sulla scheda: si spengono, e le prestazioni calano in proporzione esatta. Adesso <strong>si spengono tutte</strong>, con almeno una coppia accesa per riga, e la scelta si può <strong>mantenere all'avvio</strong>: serve a chi ha una Compute Unit guasta e la vuole lasciare spenta. Nello stesso giro il pannello CPU ha smesso di proporre frequenze che la scheda rifiuta e adesso dice quale valore non va, e la casella del Governor risponde anche per il prossimo avvio invece che solo per adesso. La segnalazione è di tom lima, che ci ha anche trovato un difetto nel codice delle maschere.",
      en: "The Compute Unit panel kept the first three pairs greyed out, because a comment of ours said the driver holds them on. It does not, and we measured it on the board: they switch off, and the performance drops in exact proportion. Now <strong>every pair can be switched off</strong>, with at least one left on per row, and the choice can be <strong>kept at boot</strong>: that is what you need when a Compute Unit is faulty and has to stay off. In the same round the CPU panel stopped offering clocks the board refuses and now says which value is wrong, and the Governor box answers for the next boot as well, not just for right now. Reported by tom lima, who also found a bug of ours in the mask code.",
      pl: "Panel Compute Unit trzymał trzy pierwsze pary wyszarzone, bo nasz komentarz twierdził, że sterownik trzyma je włączone. Tak nie jest, i zmierzyliśmy to na płycie: wyłączają się, a wydajność spada dokładnie proporcjonalnie. Teraz <strong>można wyłączyć każdą parę</strong>, zostawiając co najmniej jedną włączoną w wierszu, a wybór można <strong>zachować przy starcie</strong>: tego potrzebuje ktoś, kto ma uszkodzoną Compute Unit i chce ją zostawić wyłączoną. W tej samej turze panel CPU przestał proponować taktowania, które płyta odrzuca, i mówi teraz, która wartość jest zła, a pole Governora odpowiada też za następny start, nie tylko za teraz. Zgłosił to tom lima, który znalazł u nas również błąd w kodzie masek.",
      uk: "Панель Compute Unit тримала перші три пари сірими, бо наш коментар стверджував, що драйвер тримає їх увімкненими. Це не так, і ми виміряли це на платі: вони вимикаються, а продуктивність падає точно пропорційно. Тепер <strong>можна вимкнути будь-яку пару</strong>, лишивши щонайменше одну ввімкненою в рядку, а вибір можна <strong>зберегти при завантаженні</strong>: саме це потрібно тому, у кого несправна Compute Unit і хто хоче лишити її вимкненою. У цьому ж заході панель CPU перестала пропонувати частоти, які плата відхиляє, і тепер каже, яке значення не годиться, а прапорець Governor відповідає й за наступне завантаження, а не лише за зараз. Про це повідомив tom lima, який знайшов у нас також помилку в коді масок.",
      ru: "Панель Compute Unit держала первые три пары серыми, потому что наш комментарий утверждал, что драйвер держит их включёнными. Это не так, и мы измерили это на плате: они выключаются, а производительность падает строго пропорционально. Теперь <strong>можно выключить любую пару</strong>, оставив хотя бы одну включённой в строке, а выбор можно <strong>сохранить при загрузке</strong>: именно это нужно тому, у кого неисправна Compute Unit и кто хочет оставить её выключенной. В том же заходе панель CPU перестала предлагать частоты, которые плата отклоняет, и теперь говорит, какое значение не годится, а флажок Governor отвечает и за следующую загрузку, а не только за сейчас. Сообщил об этом tom lima, который нашёл у нас и ошибку в коде масок.",
      es: "El panel de Compute Units mantenía en gris los tres primeros pares, porque un comentario nuestro decía que el controlador los mantiene encendidos. No es así, y lo medimos en la placa: se apagan, y el rendimiento baja en proporción exacta. Ahora <strong>se puede apagar cualquier par</strong>, dejando al menos uno encendido por fila, y la elección se puede <strong>mantener al arranque</strong>: eso es lo que hace falta cuando una Compute Unit está defectuosa y tiene que quedarse apagada. En la misma tanda el panel de CPU dejó de ofrecer frecuencias que la placa rechaza y ahora dice qué valor no vale, y la casilla del Governor responde también por el próximo arranque, no sólo por ahora. Lo avisó tom lima, que además nos encontró un fallo en el código de las máscaras.",
      pt: "O painel das Compute Units mantinha a cinzento os três primeiros pares, porque um comentário nosso dizia que o controlador os mantém ligados. Não é verdade, e medimo-lo na placa: desligam-se, e o desempenho cai em proporção exata. Agora <strong>pode desligar-se qualquer par</strong>, deixando pelo menos um ligado por linha, e a escolha pode ser <strong>mantida no arranque</strong>: é isso que faz falta quando uma Compute Unit está defeituosa e tem de ficar desligada. Na mesma volta o painel da CPU deixou de oferecer frequências que a placa recusa e agora diz que valor não serve, e a caixa do Governor responde também pelo próximo arranque, não só por agora. Avisou-nos tom lima, que também nos encontrou um defeito no código das máscaras.",
      de: "Die Compute-Unit-Karte hielt die ersten drei Paare ausgegraut, weil ein Kommentar von uns behauptete, der Treiber halte sie an. Das stimmt nicht, und wir haben es auf der Karte gemessen: sie lassen sich abschalten, und die Leistung sinkt genau proportional. Jetzt <strong>lässt sich jedes Paar abschalten</strong>, mindestens eines bleibt je Zeile an, und die Auswahl kann <strong>beim Start erhalten bleiben</strong>: genau das braucht man, wenn eine Compute Unit defekt ist und aus bleiben muss. In derselben Runde bietet die CPU-Karte keine Takte mehr an, die die Karte ablehnt, und sagt jetzt, welcher Wert nicht geht, und das Governor-Kästchen antwortet auch für den nächsten Start, nicht nur für jetzt. Gemeldet hat es tom lima, der bei uns außerdem einen Fehler im Masken-Code gefunden hat.",
      fr: "Le panneau des Compute Units gardait les trois premières paires en grisé, parce qu'un commentaire de notre part affirmait que le pilote les maintient allumées. C'est faux, et nous l'avons mesuré sur la carte : elles s'éteignent, et les performances baissent exactement en proportion. Désormais <strong>toute paire peut être éteinte</strong>, avec au moins une allumée par ligne, et le choix peut être <strong>conservé au démarrage</strong> : c'est ce qu'il faut quand une Compute Unit est défectueuse et doit rester éteinte. Dans la même série, le panneau CPU a cessé de proposer des fréquences que la carte refuse et dit maintenant quelle valeur ne convient pas, et la case du Governor répond aussi pour le prochain démarrage, pas seulement pour l'instant. C'est tom lima qui l'a signalé, et qui nous a aussi trouvé un défaut dans le code des masques.",
    },
  },
  {
    // coreunlock-efi-2026-09-15
    data: '2026-09-15',
    quando: { it: "15 settembre 2026", en: "15 September 2026", pl: "15 września 2026", uk: "15 вересня 2026", ru: "15 сентября 2026", es: "15 de septiembre de 2026", pt: "15 de setembro de 2026", de: "15. September 2026", fr: "15 septembre 2026" },
    etichetta: { it: "novità", en: "new", pl: "nowość", uk: "новинка", ru: "новинка", es: "novedad", pt: "novidade", de: "Neu", fr: "nouveauté" },
    titolo: {
      it: "Gli 8 core senza il riavvio in più",
      en: "The 8 cores without the extra reboot",
      pl: "Osiem rdzeni bez dodatkowego restartu",
      uk: "Вісім ядер без зайвого перезавантаження",
      ru: "Восемь ядер без лишней перезагрузки",
      es: "Los 8 núcleos sin el reinicio de más",
      pt: "Os 8 núcleos sem o reinício a mais",
      de: "Die 8 Kerne ohne den zusätzlichen Neustart",
      fr: "Les 8 cœurs sans le redémarrage en plus",
    },
    testo: {
      it: "Chi ha acceso lo sblocco degli 8 core sulla BC-250 si prendeva un riavvio in più a ogni accensione da spenta. Adesso lo sblocco avviene <strong>prima del caricatore di avvio</strong>, quindi la scheda parte in un avvio solo. Arriva con l'aggiornamento, non c'è niente da fare. Chi lo sblocco non l'ha acceso non vede nessuna differenza.",
      en: "If you had turned on the 8-core unlock on the BC-250, the board took one extra reboot on every cold start. Now the unlock happens <strong>before the boot loader</strong>, so the board comes up in a single boot. It arrives with the update, there is nothing to do. If you never turned the unlock on, nothing changes for you.",
      pl: "Kto włączył odblokowanie ośmiu rdzeni na BC-250, dostawał dodatkowy restart przy każdym zimnym starcie. Teraz odblokowanie dzieje się <strong>przed programem rozruchowym</strong>, więc płyta wstaje za jednym razem. Przychodzi z aktualizacją, nie trzeba nic robić. Kto nie włączył odblokowania, nie zobaczy różnicy.",
      uk: "Хто увімкнув розблокування восьми ядер на BC-250, отримував зайве перезавантаження за кожного холодного старту. Тепер розблокування відбувається <strong>перед завантажувачем</strong>, тож плата стартує за один раз. Надходить з оновленням, робити нічого не треба. Хто розблокування не вмикав, різниці не побачить.",
      ru: "Кто включил разблокировку восьми ядер на BC-250, получал лишнюю перезагрузку при каждом холодном старте. Теперь разблокировка происходит <strong>до загрузчика</strong>, поэтому плата стартует за один раз. Приходит с обновлением, делать ничего не нужно. Кто разблокировку не включал, разницы не увидит.",
      es: "Quien había encendido el desbloqueo de los 8 núcleos en la BC-250 se llevaba un reinicio de más en cada arranque en frío. Ahora el desbloqueo ocurre <strong>antes del cargador de arranque</strong>, así que la placa arranca de una sola vez. Llega con la actualización, no hay nada que hacer. Quien no lo encendió no nota ninguna diferencia.",
      pt: "Quem tinha ligado o desbloqueio dos 8 núcleos na BC-250 levava um reinício a mais em cada arranque a frio. Agora o desbloqueio acontece <strong>antes do carregador de arranque</strong>, por isso a placa arranca de uma só vez. Chega com a atualização, não há nada a fazer. Quem não o ligou não nota diferença.",
      de: "Wer die Freischaltung der 8 Kerne auf der BC-250 eingeschaltet hatte, bekam bei jedem Kaltstart einen zusätzlichen Neustart. Jetzt geschieht die Freischaltung <strong>vor dem Bootloader</strong>, also startet die Karte in einem Durchgang. Es kommt mit dem Update, zu tun ist nichts. Wer sie nie eingeschaltet hat, merkt keinen Unterschied.",
      fr: "Qui avait activé le déverrouillage des 8 cœurs sur la BC-250 subissait un redémarrage en plus à chaque démarrage à froid. Maintenant le déverrouillage se fait <strong>avant le chargeur d'amorçage</strong>, donc la carte démarre en une seule fois. Cela arrive avec la mise à jour, il n'y a rien à faire. Qui ne l'a jamais activé ne voit aucune différence.",
    },
  },
  {
    // hub-73-2026-09-15
    data: '2026-09-15',
    quando: { it: "15 settembre 2026", en: "15 September 2026", pl: "15 września 2026", uk: "15 вересня 2026", ru: "15 сентября 2026", es: "15 de septiembre de 2026", pt: "15 de setembro de 2026", de: "15. September 2026", fr: "15 septembre 2026" },
    etichetta: { it: "correzione", en: "fix", pl: "poprawka", uk: "виправлення", ru: "исправление", es: "corrección", pt: "correção", de: "Korrektur", fr: "correction" },
    titolo: {
      it: "L'Hub non si chiude più se clicchi mentre carica",
      en: "The Hub no longer closes if you click while it loads",
      pl: "Hub nie zamyka się już, gdy klikniesz podczas wczytywania",
      uk: "Hub більше не закривається, якщо клацнути під час завантаження",
      ru: "Hub больше не закрывается, если нажать во время загрузки",
      es: "El Hub ya no se cierra si haces clic mientras carga",
      pt: "O Hub já não se fecha se clicares enquanto carrega",
      de: "Der Hub schließt sich nicht mehr, wenn man beim Laden klickt",
      fr: "Le Hub ne se ferme plus si vous cliquez pendant le chargement",
    },
    testo: {
      it: "All'apertura l'Hub riempie l'elenco dei programmi in sottofondo. Cliccando una voce del menù in quei primi secondi la finestra spariva. Adesso il menù aspetta, e le voci restano spente finché non è pronto, così si vede perché. Segnalata da un utente: <strong>grazie</strong>.",
      en: "When it opens, the Hub fills its list of programs in the background. Clicking a menu entry during those first seconds made the window disappear. Now the menu waits, and the entries stay off until it is ready, so you can see why. Reported by a user: <strong>thank you</strong>.",
      pl: "Po otwarciu Hub wypełnia listę programów w tle. Kliknięcie pozycji menu w tych pierwszych sekundach powodowało zniknięcie okna. Teraz menu czeka, a pozycje pozostają wyłączone, dopóki nie będzie gotowe, więc widać dlaczego. Zgłoszone przez użytkownika: <strong>dziękujemy</strong>.",
      uk: "Після відкриття Hub заповнює список програм у фоні. Натискання пункту меню в ті перші секунди призводило до зникнення вікна. Тепер меню чекає, а пункти лишаються вимкненими, доки воно не готове, тож видно чому. Повідомив користувач: <strong>дякуємо</strong>.",
      ru: "При открытии Hub заполняет список программ в фоне. Нажатие пункта меню в эти первые секунды приводило к исчезновению окна. Теперь меню ждёт, а пункты остаются выключенными, пока оно не готово, так что видно почему. Сообщил пользователь: <strong>спасибо</strong>.",
      es: "Al abrirse, el Hub llena su lista de programas en segundo plano. Hacer clic en una entrada del menú en esos primeros segundos hacía desaparecer la ventana. Ahora el menú espera, y las entradas siguen apagadas hasta que está listo, así se ve por qué. Avisado por un usuario: <strong>gracias</strong>.",
      pt: "Ao abrir, o Hub enche a lista de programas em segundo plano. Clicar numa entrada do menu nesses primeiros segundos fazia a janela desaparecer. Agora o menu espera, e as entradas ficam apagadas até estar pronto, para se ver porquê. Comunicado por um utilizador: <strong>obrigado</strong>.",
      de: "Beim Öffnen füllt der Hub seine Programmliste im Hintergrund. Ein Klick auf einen Menüeintrag in diesen ersten Sekunden ließ das Fenster verschwinden. Jetzt wartet das Menü, und die Einträge bleiben aus, bis es bereit ist, damit man sieht warum. Von einem Benutzer gemeldet: <strong>danke</strong>.",
      fr: "À l'ouverture, le Hub remplit sa liste de programmes en arrière-plan. Cliquer une entrée du menu pendant ces premières secondes faisait disparaître la fenêtre. Maintenant le menu attend, et les entrées restent éteintes jusqu'à ce qu'il soit prêt, pour qu'on voie pourquoi. Signalé par un utilisateur : <strong>merci</strong>.",
    },
  },
  {
    // cluster-ai-2026-09-13
    data: '2026-09-13',
    quando: { it: "13 settembre 2026", en: "13 September 2026", pl: "13 września 2026", uk: "13 вересня 2026", ru: "13 сентября 2026", es: "13 de septiembre de 2026", pt: "13 de setembro de 2026", de: "13. September 2026", fr: "13 septembre 2026" },
    etichetta: { it: "novità", en: "new", pl: "nowość", uk: "новинка", ru: "новинка", es: "novedad", pt: "novidade", de: "Neu", fr: "nouveauté" },
    titolo: {
      it: "Due BC-250 insieme fanno girare i modelli grandi",
      en: "Two BC-250 boards together run the big models",
      pl: "Dwie płyty BC-250 razem uruchamiają duże modele",
      uk: "Дві плати BC-250 разом запускають великі моделі",
      ru: "Две платы BC-250 вместе запускают большие модели",
      es: "Dos BC-250 juntas ejecutan los modelos grandes",
      pt: "Duas BC-250 juntas executam os modelos grandes",
      de: "Zwei BC-250 zusammen lassen die großen Modelle laufen",
      fr: "Deux BC-250 ensemble font tourner les grands modèles",
    },
    testo: {
      it: "Più schede si uniscono per tenere in memoria un modello che su una sola non ci sta. Un <b>27B da 22 GB</b> su una BC-250 non parte proprio; su due gira a <b>7,57 token al secondo</b>. Serve a questo, e va detto chiaro: non rende più veloci i modelli che già giravano, perché ogni passaggio fra una scheda e l'altra viaggia sulla rete. Il nodo si accende quando serve, sulla tua rete locale.",
      en: "Several boards join up to hold a model that does not fit on one. A <b>22 GB 27B</b> will not even start on a single BC-250; on two it runs at <b>7.57 tokens per second</b>. That is what it is for, and it is worth saying plainly: it does not speed up models that already ran, because every step between boards travels over the network. The node is switched on when you need it, on your own local network.",
      pl: "Kilka płyt łączy się, by pomieścić model, który nie mieści się na jednej. <b>27B o rozmiarze 22 GB</b> na pojedynczej BC-250 w ogóle nie startuje; na dwóch działa z prędkością <b>7,57 tokena na sekundę</b>. Do tego służy i trzeba to powiedzieć wprost: nie przyspiesza modeli, które już działały, bo każdy krok między płytami idzie przez sieć. Węzeł włącza się wtedy, gdy jest potrzebny, w twojej sieci lokalnej.",
      uk: "Кілька плат об'єднуються, щоб умістити модель, яка не влазить в одну. <b>27B на 22 ГБ</b> на одній BC-250 взагалі не запускається; на двох працює зі швидкістю <b>7,57 токена за секунду</b>. Саме для цього він і потрібен, і варто сказати прямо: він не пришвидшує моделі, які вже працювали, бо кожен крок між платами йде мережею. Вузол вмикається тоді, коли потрібен, у вашій локальній мережі.",
      ru: "Несколько плат объединяются, чтобы вместить модель, которая не помещается на одной. <b>27B на 22 ГБ</b> на одной BC-250 вообще не запускается; на двух работает со скоростью <b>7,57 токена в секунду</b>. Именно для этого он и нужен, и стоит сказать прямо: он не ускоряет модели, которые и так работали, потому что каждый шаг между платами идёт по сети. Узел включается тогда, когда нужен, в вашей локальной сети.",
      es: "Varias placas se unen para albergar un modelo que no cabe en una sola. Un <b>27B de 22 GB</b> en una sola BC-250 ni siquiera arranca; en dos funciona a <b>7,57 tokens por segundo</b>. Para eso sirve, y conviene decirlo claro: no acelera los modelos que ya funcionaban, porque cada paso entre placas viaja por la red. El nodo se enciende cuando hace falta, en tu red local.",
      pt: "Várias placas juntam-se para albergar um modelo que não cabe numa só. Um <b>27B de 22 GB</b> numa única BC-250 nem sequer arranca; em duas corre a <b>7,57 tokens por segundo</b>. É para isso que serve, e convém dizê-lo com clareza: não acelera os modelos que já corriam, porque cada passo entre placas viaja pela rede. O nó liga-se quando é preciso, na tua rede local.",
      de: "Mehrere Karten schließen sich zusammen, um ein Modell zu halten, das auf einer allein nicht hineinpasst. Ein <b>27B mit 22 GB</b> startet auf einer einzelnen BC-250 gar nicht; auf zweien läuft es mit <b>7,57 Token pro Sekunde</b>. Dafür ist es da, und das gehört klar gesagt: es beschleunigt keine Modelle, die schon liefen, denn jeder Schritt zwischen den Karten geht über das Netz. Der Knoten wird eingeschaltet, wenn man ihn braucht, im eigenen lokalen Netz.",
      fr: "Plusieurs cartes s'associent pour héberger un modèle qui ne tient pas sur une seule. Un <b>27B de 22 Go</b> ne démarre même pas sur une seule BC-250 ; sur deux, il tourne à <b>7,57 jetons par seconde</b>. C'est à cela qu'il sert, et autant le dire clairement : il n'accélère pas les modèles qui tournaient déjà, car chaque étape entre les cartes passe par le réseau. Le nœud s'allume quand on en a besoin, sur votre réseau local.",
    },
  },
  {
    // release-2606-5-2026-09-13
    data: '2026-09-13',
    quando: { it: "13 settembre 2026", en: "13 September 2026", pl: "13 września 2026", uk: "13 вересня 2026", ru: "13 сентября 2026", es: "13 de septiembre de 2026", pt: "13 de setembro de 2026", de: "13. September 2026", fr: "13 septembre 2026" },
    etichetta: { it: "rilascio", en: "release", pl: "wydanie", uk: "випуск", ru: "выпуск", es: "lanzamiento", pt: "lançamento", de: "Veröffentlichung", fr: "sortie" },
    titolo: {
      it: "È uscita la 26.06.5 «Aetherium»",
      en: "26.06.5 “Aetherium” is out",
      pl: "Wyszła wersja 26.06.5 „Aetherium”",
      uk: "Вийшла 26.06.5 «Aetherium»",
      ru: "Вышла 26.06.5 «Aetherium»",
      es: "Ya está disponible la 26.06.5 «Aetherium»",
      pt: "Saiu a 26.06.5 «Aetherium»",
      de: "26.06.5 „Aetherium“ ist da",
      fr: "La 26.06.5 « Aetherium » est sortie",
    },
    testo: {
      it: "Due edizioni, <b>BC-250</b> e <b>Generic</b>, con kernel <b>7.2.5</b>. Il disco si può cifrare in installazione con <b>LUKS</b>, e il sistema parte anche con <b>Secure Boot acceso</b>. Al primo accesso scegli tu cosa installare, browser compreso. La versione del sistema sale con gli aggiornamenti, e la modalità AI libera la memoria della scheda per far girare un modello in locale.",
      en: "Two editions, <b>BC-250</b> and <b>Generic</b>, on kernel <b>7.2.5</b>. The disk can be encrypted at install with <b>LUKS</b>, and the system boots with <b>Secure Boot enabled</b>. At the first login you choose what to install, the browser included. The system version rises with your updates, and AI mode frees the board's memory to run a model locally.",
      pl: "Dwie edycje, <b>BC-250</b> i <b>Generic</b>, z jądrem <b>7.2.5</b>. Dysk można zaszyfrować przy instalacji za pomocą <b>LUKS</b>, a system startuje także z włączonym <b>Secure Boot</b>. Przy pierwszym logowaniu sam wybierasz, co zainstalować, łącznie z przeglądarką. Wersja systemu rośnie wraz z aktualizacjami, a tryb AI zwalnia pamięć płyty, by uruchomić model lokalnie.",
      uk: "Дві редакції, <b>BC-250</b> і <b>Generic</b>, з ядром <b>7.2.5</b>. Диск можна зашифрувати під час встановлення за допомогою <b>LUKS</b>, і система запускається навіть з увімкненим <b>Secure Boot</b>. Під час першого входу ви самі обираєте, що встановити, зокрема браузер. Версія системи зростає з оновленнями, а режим ШІ звільняє пам'ять плати для локальної моделі.",
      ru: "Две редакции, <b>BC-250</b> и <b>Generic</b>, с ядром <b>7.2.5</b>. Диск можно зашифровать при установке с помощью <b>LUKS</b>, и система запускается даже с включённым <b>Secure Boot</b>. При первом входе вы сами выбираете, что установить, включая браузер. Версия системы растёт вместе с обновлениями, а режим ИИ освобождает память платы для локальной модели.",
      es: "Dos ediciones, <b>BC-250</b> y <b>Generic</b>, con núcleo <b>7.2.5</b>. El disco se puede cifrar en la instalación con <b>LUKS</b>, y el sistema arranca también con <b>Secure Boot activado</b>. En el primer acceso eliges tú qué instalar, navegador incluido. La versión del sistema sube con las actualizaciones, y el modo IA libera la memoria de la placa para ejecutar un modelo en local.",
      pt: "Duas edições, <b>BC-250</b> e <b>Generic</b>, com kernel <b>7.2.5</b>. O disco pode ser cifrado na instalação com <b>LUKS</b>, e o sistema arranca mesmo com <b>Secure Boot ativado</b>. No primeiro acesso escolhes tu o que instalar, navegador incluído. A versão do sistema sobe com as atualizações, e o modo IA liberta a memória da placa para correr um modelo localmente.",
      de: "Zwei Ausgaben, <b>BC-250</b> und <b>Generic</b>, mit Kernel <b>7.2.5</b>. Die Platte lässt sich bei der Installation mit <b>LUKS</b> verschlüsseln, und das System startet auch mit eingeschaltetem <b>Secure Boot</b>. Bei der ersten Anmeldung wählen Sie, was installiert wird, den Browser eingeschlossen. Die Systemversion steigt mit den Aktualisierungen, und der KI-Modus gibt den Speicher der Karte frei, um ein Modell lokal laufen zu lassen.",
      fr: "Deux éditions, <b>BC-250</b> et <b>Generic</b>, avec le noyau <b>7.2.5</b>. Le disque peut être chiffré à l'installation avec <b>LUKS</b>, et le système démarre aussi avec <b>Secure Boot activé</b>. À la première connexion, c'est vous qui choisissez quoi installer, navigateur compris. La version du système monte avec les mises à jour, et le mode IA libère la mémoire de la carte pour faire tourner un modèle en local.",
    },
  },
  {
    // versione-sale-con-apt-2026-09-13
    data: '2026-09-13',
    quando: { it: "13 settembre 2026", en: "13 September 2026", pl: "13 września 2026", uk: "13 вересня 2026", ru: "13 сентября 2026", es: "13 de septiembre de 2026", pt: "13 de setembro de 2026", de: "13. September 2026", fr: "13 septembre 2026" },
    etichetta: { it: "aggiornamento", en: "update", pl: "aktualizacja", uk: "оновлення", ru: "обновление", es: "actualización", pt: "atualização", de: "Aktualisierung", fr: "mise à jour" },
    titolo: {
      it: "La versione del sistema sale con gli aggiornamenti",
      en: "The system version rises with the updates",
      pl: "Wersja systemu rośnie wraz z aktualizacjami",
      uk: "Версія системи зростає разом з оновленнями",
      ru: "Версия системы растёт вместе с обновлениями",
      es: "La versión del sistema sube con las actualizaciones",
      pt: "A versão do sistema sobe com as atualizações",
      de: "Die Systemversion steigt mit den Aktualisierungen",
      fr: "La version du système monte avec les mises à jour",
    },
    testo: {
      it: "Finora la versione la scriveva solo l'immagine di installazione: chi aveva installato dalla 26.06.4 restava 26.06.4 per sempre, anche dopo aver scaricato tutti gli aggiornamenti. Adesso il numero viaggia dentro i pacchetti, quindi sale da solo.",
      en: "Until now the version was written only by the install image: whoever installed from 26.06.4 stayed 26.06.4 for ever, however many updates they downloaded. The number now travels inside the packages, so it rises by itself.",
      pl: "Dotąd wersję zapisywał tylko obraz instalacyjny: kto zainstalował z 26.06.4, zostawał przy 26.06.4 na zawsze, choćby pobrał wszystkie aktualizacje. Teraz numer jedzie w pakietach, więc rośnie sam.",
      uk: "Досі версію записував лише інсталяційний образ: хто встановив із 26.06.4, лишався на 26.06.4 назавжди, хоч би скільки оновлень завантажив. Тепер номер їде всередині пакунків, тож зростає сам.",
      ru: "До сих пор версию записывал только установочный образ: кто установил с 26.06.4, оставался на 26.06.4 навсегда, сколько бы обновлений ни скачал. Теперь номер едет внутри пакетов, поэтому растёт сам.",
      es: "Hasta ahora la versión la escribía sólo la imagen de instalación: quien instaló desde la 26.06.4 se quedaba en 26.06.4 para siempre, por muchas actualizaciones que descargara. Ahora el número viaja dentro de los paquetes, así que sube solo.",
      pt: "Até agora a versão era escrita só pela imagem de instalação: quem instalou a partir da 26.06.4 ficava em 26.06.4 para sempre, por mais atualizações que descarregasse. Agora o número viaja dentro dos pacotes, por isso sobe sozinho.",
      de: "Bisher schrieb nur das Installationsabbild die Version: wer von 26.06.4 installiert hatte, blieb für immer 26.06.4, wie viele Aktualisierungen er auch lud. Die Nummer reist jetzt in den Paketen mit und steigt daher von selbst.",
      fr: "Jusqu'ici la version n'était écrite que par l'image d'installation : qui avait installé depuis la 26.06.4 restait en 26.06.4 pour toujours, quel que soit le nombre de mises à jour téléchargées. Le numéro voyage désormais dans les paquets, donc il monte tout seul.",
    },
  },
  {
    // primo-avvio-parte-2026-09-13
    data: '2026-09-13',
    quando: { it: "13 settembre 2026", en: "13 September 2026", pl: "13 września 2026", uk: "13 вересня 2026", ru: "13 сентября 2026", es: "13 de septiembre de 2026", pt: "13 de setembro de 2026", de: "13. September 2026", fr: "13 septembre 2026" },
    etichetta: { it: "aggiornamento", en: "update", pl: "aktualizacja", uk: "оновлення", ru: "обновление", es: "actualización", pt: "atualização", de: "Aktualisierung", fr: "mise à jour" },
    titolo: {
      it: "Al primo avvio scegli tu cosa installare",
      en: "At the first boot you choose what gets installed",
      pl: "Przy pierwszym uruchomieniu sam wybierasz, co zainstalować",
      uk: "Під час першого запуску ви самі обираєте, що встановити",
      ru: "При первом запуске вы сами выбираете, что установить",
      es: "En el primer arranque eliges tú qué instalar",
      pt: "No primeiro arranque escolhes tu o que instalar",
      de: "Beim ersten Start wählen Sie, was installiert wird",
      fr: "Au premier démarrage, c'est vous qui choisissez",
    },
    testo: {
      it: "Una finestra ti chiede cosa vuoi sul tuo sistema: Steam, Heroic, Lutris, gli emulatori, OnlyOffice e il browser che preferisci fra Firefox, Chrome, Chromium e Brave. Niente è preinstallato e niente è deciso al posto tuo. Ogni programma si scarica con la sua barra, e puoi spegnere a metà senza perdere niente: riprende da solo al riavvio.",
      en: "A window asks what you want on your system: Steam, Heroic, Lutris, the emulators, OnlyOffice and whichever browser you prefer among Firefox, Chrome, Chromium and Brave. Nothing is preinstalled and nothing is decided for you. Each program downloads with its own progress bar, and you can shut down halfway without losing anything: it picks up by itself at the next boot.",
      pl: "Okno pyta, co chcesz mieć w systemie: Steam, Heroic, Lutris, emulatory, OnlyOffice i przeglądarkę do wyboru spośród Firefoksa, Chrome, Chromium i Brave. Nic nie jest preinstalowane i nic nie jest decydowane za ciebie. Każdy program pobiera się z własnym paskiem, a wyłączenie w połowie niczego nie niszczy: wznawia się przy następnym starcie.",
      uk: "Вікно запитує, що ви хочете мати в системі: Steam, Heroic, Lutris, емулятори, OnlyOffice і браузер на вибір із Firefox, Chrome, Chromium та Brave. Нічого не встановлено заздалегідь і нічого не вирішено за вас. Кожна програма завантажується зі своєю смужкою, а вимкнення посеред процесу нічого не втрачає: воно продовжиться за наступного запуску.",
      ru: "Окно спрашивает, что вы хотите в системе: Steam, Heroic, Lutris, эмуляторы, OnlyOffice и браузер на выбор из Firefox, Chrome, Chromium и Brave. Ничего не предустановлено и ничего не решено за вас. Каждая программа скачивается со своей полосой, а выключение на половине ничего не теряет: всё продолжится при следующем запуске.",
      es: "Una ventana te pregunta qué quieres en tu sistema: Steam, Heroic, Lutris, los emuladores, OnlyOffice y el navegador que prefieras entre Firefox, Chrome, Chromium y Brave. No hay nada preinstalado ni nada decidido por ti. Cada programa se descarga con su propia barra, y puedes apagar a medias sin perder nada: continúa solo al siguiente arranque.",
      pt: "Uma janela pergunta o que queres no teu sistema: Steam, Heroic, Lutris, os emuladores, o OnlyOffice e o navegador que preferires entre Firefox, Chrome, Chromium e Brave. Nada vem preinstalado e nada é decidido por ti. Cada programa descarrega com a sua própria barra, e podes desligar a meio sem perder nada: recomeça sozinho no arranque seguinte.",
      de: "Ein Fenster fragt, was Sie auf Ihrem System haben möchten: Steam, Heroic, Lutris, die Emulatoren, OnlyOffice und den Browser Ihrer Wahl unter Firefox, Chrome, Chromium und Brave. Nichts ist vorinstalliert und nichts wird für Sie entschieden. Jedes Programm lädt mit einem eigenen Balken, und ein Herunterfahren mittendrin verliert nichts: es macht beim nächsten Start von selbst weiter.",
      fr: "Une fenêtre vous demande ce que vous voulez sur votre système : Steam, Heroic, Lutris, les émulateurs, OnlyOffice et le navigateur de votre choix parmi Firefox, Chrome, Chromium et Brave. Rien n'est préinstallé et rien n'est décidé à votre place. Chaque programme se télécharge avec sa propre barre, et éteindre en cours de route ne perd rien : cela reprend tout seul au démarrage suivant.",
    },
  },
  {
    // ai-mode-levels-2026-09-13
    data: '2026-09-13',
    quando: { it: "13 settembre 2026", en: "13 September 2026", pl: "13 września 2026", uk: "13 вересня 2026", ru: "13 сентября 2026", es: "13 de septiembre de 2026", pt: "13 de setembro de 2026", de: "13. September 2026", fr: "13 septembre 2026" },
    etichetta: { it: "aggiornamento", en: "update", pl: "aktualizacja", uk: "оновлення", ru: "обновление", es: "actualización", pt: "atualização", de: "Aktualisierung", fr: "mise à jour" },
    titolo: {
      it: "La modalità AI a tre livelli, e lo schermo che dice cosa sta facendo",
      en: "AI mode in three levels, and a screen that says what it is doing",
      pl: "Tryb AI na trzech poziomach i ekran, który mówi, co robi",
      uk: "Режим ШІ на трьох рівнях і екран, який каже, що робить",
      ru: "Режим ИИ на трёх уровнях и экран, который говорит, что делает",
      es: "El modo IA en tres niveles, y una pantalla que dice qué está haciendo",
      pt: "O modo IA em três níveis, e um ecrã que diz o que está a fazer",
      de: "Der KI-Modus in drei Stufen, und ein Bildschirm, der sagt, was er tut",
      fr: "Le mode IA en trois niveaux, et un écran qui dit ce qu'il fait",
    },
    testo: {
      it: "La modalità AI ha tre livelli, scelti dal Control Center o dal Remote Manager: si spegne solo il desktop, oppure anche Unsloth Studio e resta <b>llama-server da solo sulla porta 8888</b>, con la stessa API e la stessa chiave. Col modello caricato il sistema passa da 567 a <b>115 MB</b>. A desktop spento lo schermo non è più nero: una console mostra gli indirizzi della scheda e come tornare indietro, e nel Remote Manager c'è un pulsante <b>AI-Mode On/Off</b>.",
      en: "AI mode has three levels, chosen from the Control Center or the Remote Manager: shut down the desktop alone, or Unsloth Studio as well and leave <b>llama-server by itself on port 8888</b>, with the same API and the same key. With a model loaded the system goes from 567 to <b>115 MB</b>. With the desktop down the screen is no longer black: a console shows the board's addresses and the way back, and the Remote Manager has an <b>AI-Mode On/Off</b> button.",
      pl: "Tryb AI ma trzy poziomy, wybierane z Control Center albo z Remote Managera: wyłącza się sam pulpit albo także Unsloth Studio i zostaje <b>sam llama-server na porcie 8888</b>, z tym samym API i kluczem. Z załadowanym modelem system schodzi z 567 do <b>115 MB</b>. Przy wyłączonym pulpicie ekran nie jest już czarny: konsola pokazuje adresy płyty i drogę powrotną, a w Remote Managerze jest przycisk <b>AI-Mode On/Off</b>.",
      uk: "Режим ШІ має три рівні, які обираються з Control Center або з Remote Manager: вимикається лише стільниця або й Unsloth Studio, і залишається <b>сам llama-server на порту 8888</b>, з тим самим API і ключем. Із завантаженою моделлю система переходить із 567 до <b>115 МБ</b>. З вимкненою стільницею екран уже не чорний: консоль показує адреси плати і шлях назад, а в Remote Manager є кнопка <b>AI-Mode On/Off</b>.",
      ru: "У режима ИИ три уровня, которые выбираются из Control Center или из Remote Manager: выключается только рабочий стол или и Unsloth Studio, и остаётся <b>один llama-server на порту 8888</b>, с тем же API и ключом. С загруженной моделью система переходит с 567 на <b>115 МБ</b>. С выключенным рабочим столом экран больше не чёрный: консоль показывает адреса платы и путь назад, а в Remote Manager есть кнопка <b>AI-Mode On/Off</b>.",
      es: "El modo IA tiene tres niveles, que se eligen desde el Control Center o el Remote Manager: se apaga solo el escritorio, o también Unsloth Studio y queda <b>llama-server solo en el puerto 8888</b>, con la misma API y la misma clave. Con el modelo cargado el sistema pasa de 567 a <b>115 MB</b>. Con el escritorio apagado la pantalla ya no está negra: una consola muestra las direcciones de la placa y cómo volver, y en el Remote Manager hay un botón <b>AI-Mode On/Off</b>.",
      pt: "O modo IA tem três níveis, escolhidos no Control Center ou no Remote Manager: desliga-se só a área de trabalho, ou também o Unsloth Studio e fica <b>o llama-server sozinho na porta 8888</b>, com a mesma API e a mesma chave. Com o modelo carregado o sistema passa de 567 para <b>115 MB</b>. Com a área de trabalho desligada o ecrã já não é preto: uma consola mostra os endereços da placa e como voltar, e no Remote Manager há um botão <b>AI-Mode On/Off</b>.",
      de: "Der KI-Modus hat drei Stufen, gewählt im Control Center oder im Remote Manager: nur der Desktop geht aus, oder auch Unsloth Studio, und <b>llama-server bleibt allein auf Port 8888</b>, mit derselben API und demselben Schlüssel. Mit geladenem Modell geht das System von 567 auf <b>115 MB</b>. Bei heruntergefahrenem Desktop ist der Bildschirm nicht mehr schwarz: eine Konsole zeigt die Adressen der Karte und den Weg zurück, und im Remote Manager gibt es eine Schaltfläche <b>AI-Mode On/Off</b>.",
      fr: "Le mode IA a trois niveaux, choisis depuis le Control Center ou le Remote Manager : on éteint le bureau seul, ou aussi Unsloth Studio et <b>llama-server reste seul sur le port 8888</b>, avec la même API et la même clé. Avec un modèle chargé, le système passe de 567 à <b>115 Mo</b>. Bureau éteint, l'écran n'est plus noir : une console affiche les adresses de la carte et le chemin du retour, et le Remote Manager a un bouton <b>AI-Mode On/Off</b>.",
    },
  },
  {
    // ai-control-center-2026-09
    data: '2026-09-12',
    quando: { it: "12 settembre 2026", en: "12 September 2026", pl: "12 września 2026", uk: "12 вересня 2026", ru: "12 сентября 2026", es: "12 de septiembre de 2026", pt: "12 de setembro de 2026", de: "12. September 2026", fr: "12 septembre 2026" },
    etichetta: { it: "aggiornamento", en: "update", pl: "aktualizacja", uk: "оновлення", ru: "обновление", es: "actualización", pt: "atualização", de: "Aktualisierung", fr: "mise à jour" },
    titolo: {
      it: "La sezione AI pilota Unsloth Studio",
      en: "The AI section drives Unsloth Studio",
      pl: "Sekcja AI steruje Unsloth Studio",
      uk: "Розділ ШІ керує Unsloth Studio",
      ru: "Раздел ИИ управляет Unsloth Studio",
      es: "La sección IA pilota Unsloth Studio",
      pt: "A secção IA pilota o Unsloth Studio",
      de: "Der KI-Bereich steuert Unsloth Studio",
      fr: "La section IA pilote Unsloth Studio",
    },
    testo: {
      it: "La sezione AI del Control Center pilota Unsloth Studio invece di limitarsi ad accenderlo: aggiornamento in un clic, primo accesso e chiave API da qui, i modelli sul disco, il download dei GGUF dall'Hub di Hugging Face, una chat di prova con i token al secondo misurati e il motore apribile sulla rete locale. Le stesse cose nel Remote Manager, dal browser. Nel Tuner la VRAM guadagna i preset da 512 MB e 1 GB.",
      en: "The AI section of the Control Center drives Unsloth Studio instead of only switching it on: update in one click, first sign-in and API key from here, the models on disk, GGUF downloads from the Hugging Face Hub, a chat test with the measured tokens per second, and the engine opened to the local network. The same from a browser in the Remote Manager. In the Tuner the VRAM gains 512 MB and 1 GB presets.",
      pl: "Sekcja AI w Control Center steruje Unsloth Studio, a nie tylko go włącza: aktualizacja jednym kliknięciem, pierwsze logowanie i klucz API stąd, modele na dysku, pobieranie GGUF z Hubu Hugging Face, próbny czat ze zmierzonymi tokenami na sekundę i silnik otwierany na sieć lokalną. To samo z przeglądarki w Remote Managerze. W Tunerze VRAM dostaje presety 512 MB i 1 GB.",
      uk: "Розділ ШІ в Control Center керує Unsloth Studio, а не лише вмикає його: оновлення в один клік, перший вхід і ключ API звідси, моделі на диску, завантаження GGUF з Hub Hugging Face, проба чату з виміряними токенами за секунду та рушій, відкритий у локальну мережу. Те саме з браузера в Remote Manager. У Tuner VRAM отримує пресети 512 МБ і 1 ГБ.",
      ru: "Раздел ИИ в Control Center управляет Unsloth Studio, а не просто включает его: обновление в один клик, первый вход и ключ API отсюда, модели на диске, загрузка GGUF из Hub Hugging Face, проба чата с измеренными токенами в секунду и движок, открытый в локальную сеть. То же самое из браузера в Remote Manager. В Тюнере VRAM получает пресеты 512 МБ и 1 ГБ.",
      es: "La sección IA del Control Center pilota Unsloth Studio en vez de solo encenderlo: actualización en un clic, primer acceso y clave API desde aquí, los modelos en disco, la descarga de GGUF del Hub de Hugging Face, una prueba de chat con los tokens por segundo medidos y el motor abierto a la red local. Lo mismo desde el navegador en el Remote Manager. En el Tuner la VRAM gana los preajustes de 512 MB y 1 GB.",
      pt: "A secção IA do Control Center pilota o Unsloth Studio em vez de apenas o ligar: atualização num clique, primeiro acesso e chave API daqui, os modelos em disco, a transferência de GGUF do Hub da Hugging Face, um teste de chat com os tokens por segundo medidos e o motor aberto à rede local. O mesmo pelo navegador no Remote Manager. No Tuner a VRAM ganha as predefinições de 512 MB e 1 GB.",
      de: "Der KI-Bereich des Control Center steuert Unsloth Studio, statt ihn nur einzuschalten: Aktualisierung in einem Klick, erste Anmeldung und API-Schlüssel von hier, die Modelle auf der Platte, GGUF-Downloads aus dem Hugging-Face-Hub, ein Chat-Test mit den gemessenen Token pro Sekunde und die Maschine im lokalen Netz erreichbar. Dasselbe im Browser über den Remote Manager. Im Tuner bekommt der VRAM die Vorgaben 512 MB und 1 GB.",
      fr: "La section IA du Control Center pilote Unsloth Studio au lieu de se contenter de l'allumer : mise à jour en un clic, première connexion et clé API depuis ici, les modèles sur le disque, le téléchargement des GGUF depuis le Hub Hugging Face, un essai de chat avec les tokens par seconde mesurés et le moteur ouvert au réseau local. La même chose depuis le navigateur dans le Remote Manager. Dans le Tuner, la VRAM gagne les préréglages 512 Mo et 1 Go.",
    },
  },
  {
    // community-2026-09
    data: '2026-09-11',
    quando: { it: "11 settembre 2026", en: "11 September 2026", pl: "11 września 2026", uk: "11 вересня 2026", ru: "11 сентября 2026", es: "11 de septiembre de 2026", pt: "11 de setembro de 2026", de: "11. September 2026", fr: "11 septembre 2026" },
    etichetta: { it: "community", en: "community", pl: "społeczność", uk: "спільнота", ru: "сообщество", es: "comunidad", pt: "comunidade", de: "Community", fr: "communauté" },
    titolo: {
      it: "Quello che abbiamo preso dalla community BC-250, e quello che no",
      en: "What we took from the BC-250 community, and what we did not",
      pl: "Co wzięliśmy od społeczności BC-250, a czego nie",
      uk: "Що ми взяли від спільноти BC-250, а що ні",
      ru: "Что мы взяли у сообщества BC-250, а что нет",
      es: "Lo que hemos tomado de la comunidad BC-250, y lo que no",
      pt: "O que tirámos da comunidade BC-250, e o que não",
      de: "Was wir von der BC-250-Community übernommen haben, und was nicht",
      fr: "Ce que nous avons pris à la communauté BC-250, et ce que nous n'avons pas pris"
    },
    testo: {
      it: "Abbiamo provato sulla nostra scheda quello che la community della BC-250 ha pubblicato negli ultimi mesi. Entrano nella distribuzione: il Control Center guidabile <strong>col controller</strong>, l'esportazione del Monitor in CSV, la tabella ACPI con i metodi mancanti, l'heap unificato per RADV con la cache degli shader a 10 GB, lo <strong>sblocco degli 8 core prima di GRUB</strong>, e due patch del kernel per il DualSense dietro un bridge e per lo YCbCr 4:4:4 sui dongle DisplayPort-HDMI. Il registro completo è in <code>docs/COMMUNITY.md</code>.",
      en: "We tried on our own board what the BC-250 community has published over the past months. Going into the distribution: the Control Center driven <strong>with a controller</strong>, Monitor recordings exported to CSV, the ACPI table with the missing methods, the unified memory heap for RADV with a 10 GB shader cache, <strong>unlocking the 8 cores before GRUB</strong>, and two kernel patches, for the DualSense behind a bridge and for YCbCr 4:4:4 on DisplayPort-HDMI dongles. The full log is in <code>docs/COMMUNITY.md</code>.",
      pl: "Sprawdziliśmy na własnej płycie to, co społeczność BC-250 opublikowała w ostatnich miesiącach. Do dystrybucji wchodzą: Control Center obsługiwane <strong>padem</strong>, eksport zapisów Monitora do CSV, tablica ACPI z brakującymi metodami, wspólna sterta pamięci dla RADV z 10 GB cache shaderów, <strong>odblokowanie 8 rdzeni przed GRUB-em</strong> oraz dwie łatki jądra: dla DualSense za mostkiem i dla YCbCr 4:4:4 na przejściówkach DisplayPort-HDMI. Pełny rejestr jest w <code>docs/COMMUNITY.md</code>.",
      uk: "Ми перевірили на власній платі те, що спільнота BC-250 опублікувала за останні місяці. У дистрибутив входять: Control Center, керований <strong>геймпадом</strong>, експорт записів Monitor у CSV, таблиця ACPI з відсутніми методами, спільна купа пам'яті для RADV з кешем шейдерів на 10 ГБ, <strong>розблокування 8 ядер до GRUB</strong> і дві латки ядра: для DualSense за мостом і для YCbCr 4:4:4 на перехідниках DisplayPort-HDMI. Повний перелік у <code>docs/COMMUNITY.md</code>.",
      ru: "Мы проверили на своей плате то, что сообщество BC-250 опубликовало за последние месяцы. В дистрибутив входят: Control Center с управлением <strong>геймпадом</strong>, экспорт записей Monitor в CSV, таблица ACPI с недостающими методами, общая куча памяти для RADV с кэшем шейдеров на 10 ГБ, <strong>разблокировка 8 ядер до GRUB</strong> и две заплатки ядра: для DualSense за мостом и для YCbCr 4:4:4 на переходниках DisplayPort-HDMI. Полный перечень в <code>docs/COMMUNITY.md</code>.",
      es: "Hemos probado en nuestra placa lo que la comunidad de la BC-250 ha publicado en los últimos meses. Entran en la distribución: el Control Center manejable <strong>con el mando</strong>, la exportación del Monitor a CSV, la tabla ACPI con los métodos que faltaban, el montón de memoria unificado para RADV con caché de shaders de 10 GB, el <strong>desbloqueo de los 8 núcleos antes de GRUB</strong>, y dos parches del kernel, para el DualSense detrás de un puente y para el YCbCr 4:4:4 en los adaptadores DisplayPort-HDMI. El registro completo está en <code>docs/COMMUNITY.md</code>.",
      pt: "Experimentámos na nossa placa aquilo que a comunidade da BC-250 publicou nos últimos meses. Entram na distribuição: o Control Center guiável <strong>com o comando</strong>, a exportação do Monitor para CSV, a tabela ACPI com os métodos em falta, a pilha de memória unificada para o RADV com cache de shaders de 10 GB, o <strong>desbloqueio dos 8 núcleos antes do GRUB</strong>, e dois patches do kernel, para o DualSense atrás de uma ponte e para o YCbCr 4:4:4 nos adaptadores DisplayPort-HDMI. O registo completo está em <code>docs/COMMUNITY.md</code>.",
      de: "Wir haben auf unserer eigenen Karte ausprobiert, was die BC-250-Gemeinschaft in den letzten Monaten veröffentlicht hat. In die Distribution kommen: das Control Center <strong>mit dem Controller</strong> bedienbar, der Export der Monitor-Aufzeichnungen als CSV, die ACPI-Tabelle mit den fehlenden Methoden, der vereinheitlichte Speicher-Heap für RADV mit 10 GB Shader-Cache, das <strong>Freischalten der 8 Kerne vor GRUB</strong> und zwei Kernel-Patches, für den DualSense hinter einer Brücke und für YCbCr 4:4:4 an DisplayPort-HDMI-Adaptern. Das vollständige Protokoll steht in <code>docs/COMMUNITY.md</code>.",
      fr: "Nous avons essayé sur notre propre carte ce que la communauté BC-250 a publié ces derniers mois. Entrent dans la distribution : le Control Center pilotable <strong>à la manette</strong>, l'export des enregistrements du Monitor en CSV, la table ACPI avec les méthodes manquantes, le tas mémoire unifié pour RADV avec 10 Go de cache de shaders, le <strong>déverrouillage des 8 cœurs avant GRUB</strong>, et deux correctifs noyau, pour la DualSense derrière un pont et pour le YCbCr 4:4:4 sur les adaptateurs DisplayPort-HDMI. Le relevé complet est dans <code>docs/COMMUNITY.md</code>.",
    },
  },
  {
    // control-center-2026-09
    data: '2026-09-11',
    quando: { it: "11 settembre 2026", en: "11 September 2026", pl: "11 września 2026", uk: "11 вересня 2026", ru: "11 сентября 2026", es: "11 de septiembre de 2026", pt: "11 de setembro de 2026", de: "11. September 2026", fr: "11 septembre 2026" },
    etichetta: { it: "novità", en: "new", pl: "nowość", uk: "новинка", ru: "новое", es: "novedad", pt: "novidade", de: "Neu", fr: "nouveauté" },
    titolo: {
      it: "Tutti gli strumenti in una finestra: il Control Center",
      en: "Every tool in one window: the Control Center",
      pl: "Wszystkie narzędzia w jednym oknie: Control Center",
      uk: "Усі інструменти в одному вікні: Control Center",
      ru: "Все инструменты в одном окне: Control Center",
      es: "Todas las herramientas en una ventana: el Control Center",
      pt: "Todas as ferramentas numa janela: o Control Center",
      de: "Alle Werkzeuge in einem Fenster: das Control Center",
      fr: "Tous les outils dans une fenêtre : le Control Center"
    },
    testo: {
      it: "Le sette finestre di SkillFishOS diventano <strong>una sola</strong>, con dodici sezioni, e dentro ci sono anche cose che prima si facevano da terminale: la nostra Mesa per Steam o per tutto il sistema, lo schedulatore dei giochi, GE-Proton 11, i profili. Il Tuner è riscritto attorno alla curva del governor: quindici punti da trascinare e un Applica che <strong>mette la curva in prova</strong> con un conto alla rovescia, così una curva sbagliata non ti lascia a piedi. Le stesse sezioni sono nel Remote Manager.",
      en: "The seven SkillFishOS windows become <strong>one</strong>, with twelve sections, and it now covers things that used to need a terminal: our Mesa for Steam or system-wide, the scheduler that starts with games, GE-Proton 11, the profiles. The Tuner is rewritten around the governor curve: fifteen points you drag and an Apply that <strong>puts the curve on trial</strong> with a countdown, so a bad curve does not leave you stranded. The same sections are in the Remote Manager.",
      pl: "Siedem okien SkillFishOS staje się <strong>jednym</strong>, z dwunastoma sekcjami, a w środku są też rzeczy, które wcześniej robiło się z terminala: nasza Mesa dla Steama albo dla całego systemu, planista uruchamiany z grami, GE-Proton 11, profile. Tuner napisano na nowo wokół krzywej governora: piętnaście punktów do przeciągania i Zastosuj, które <strong>wystawia krzywą na próbę</strong> z odliczaniem, więc zła krzywa nie zostawia cię na lodzie. Te same sekcje są w Remote Managerze.",
      uk: "Сім вікон SkillFishOS стають <strong>одним</strong>, з дванадцятьма розділами, і всередині є й те, що раніше робилося з термінала: наша Mesa для Steam або для всієї системи, планувальник, що стартує з іграми, GE-Proton 11, профілі. Tuner переписано навколо кривої governor: п'ятнадцять точок, які перетягуються, і «Застосувати», що <strong>ставить криву на пробу</strong> зі зворотним відліком, тож хибна крива не лишить вас ні з чим. Ті самі розділи є в Remote Manager.",
      ru: "Семь окон SkillFishOS становятся <strong>одним</strong>, с двенадцатью разделами, и внутри есть то, что раньше делалось из терминала: наша Mesa для Steam или для всей системы, планировщик, стартующий с играми, GE-Proton 11, профили. Тюнер переписан вокруг кривой governor: пятнадцать точек, которые перетаскиваются, и «Применить», которое <strong>ставит кривую на пробу</strong> с обратным отсчётом, так что неудачная кривая не оставит вас ни с чем. Те же разделы есть в Remote Manager.",
      es: "Las siete ventanas de SkillFishOS se convierten en <strong>una sola</strong>, con doce secciones, y dentro hay también cosas que antes se hacían desde el terminal: nuestra Mesa para Steam o para todo el sistema, el planificador que arranca con los juegos, GE-Proton 11, los perfiles. El Tuner está reescrito en torno a la curva del governor: quince puntos que se arrastran y un Aplicar que <strong>pone la curva a prueba</strong> con una cuenta atrás, así una curva mala no te deja tirado. Las mismas secciones están en el Remote Manager.",
      pt: "As sete janelas do SkillFishOS passam a ser <strong>uma só</strong>, com doze secções, e lá dentro há também coisas que antes se faziam no terminal: a nossa Mesa para o Steam ou para todo o sistema, o escalonador que arranca com os jogos, o GE-Proton 11, os perfis. O Tuner foi reescrito à volta da curva do governor: quinze pontos que se arrastam e um Aplicar que <strong>põe a curva à prova</strong> com uma contagem decrescente, para que uma curva errada não te deixe a pé. As mesmas secções estão no Remote Manager.",
      de: "Aus den sieben Fenstern von SkillFishOS wird <strong>eines</strong>, mit zwölf Bereichen, und darin steckt auch, was früher das Terminal brauchte: unsere Mesa für Steam oder systemweit, der Scheduler, der mit Spielen startet, GE-Proton 11, die Profile. Der Tuner ist um die Governor-Kurve herum neu geschrieben: fünfzehn Punkte zum Ziehen und ein Anwenden, das <strong>die Kurve auf Probe stellt</strong>, mit Countdown, damit eine falsche Kurve Sie nicht stehen lässt. Dieselben Bereiche gibt es im Remote Manager.",
      fr: "Les sept fenêtres de SkillFishOS n'en font plus qu'<strong>une</strong>, avec douze sections, et on y trouve aussi ce qui demandait le terminal : notre Mesa pour Steam ou pour tout le système, l'ordonnanceur qui démarre avec les jeux, GE-Proton 11, les profils. Le Tuner est réécrit autour de la courbe du governor : quinze points à faire glisser et un Appliquer qui <strong>met la courbe à l'essai</strong> avec un compte à rebours, pour qu'une mauvaise courbe ne vous laisse pas en plan. Les mêmes sections sont dans le Remote Manager.",
    },
  },
  {
    data: '2026-08-27',
    quando: { it: "27 agosto 2026", en: "27 August 2026", pl: "27 sierpnia 2026", uk: "27 серпня 2026", ru: "27 августа 2026", es: "27 de agosto de 2026", pt: "27 de agosto de 2026", de: "27. August 2026", fr: "27 août 2026" },
    etichetta: { it: "aggiornamento", en: "update", pl: "aktualizacja", uk: "оновлення", ru: "обновление", es: "actualización", pt: "atualização", de: "Update", fr: "mise à jour" },
    titolo: {
      it: "La guardia termica restituisce i megahertz",
      en: "The thermal guard gives the megahertz back",
      pl: "Strażnik termiczny oddaje megaherce",
      uk: "Тепловий вартовий повертає мегагерци",
      ru: "Тепловой страж возвращает мегагерцы",
      es: "El guardián térmico devuelve los megahercios",
      pt: "O guarda térmico devolve os megahertz",
      de: "Der Temperaturwächter gibt die Megahertz zurück",
      fr: "Le garde thermique rend les mégahertz"
    },
    testo: {
      it: "Sulla BC-250 una guardia tiene d'occhio la temperatura e toglie 100 MHz al processore quando la scheda scalda troppo. Adesso <strong>glieli restituisce</strong>: appena la scheda si raffredda la frequenza risale, e si ferma dove era partita. Col nostro banco di prova vale <strong>1,2% di fotogrammi</strong> su una macchina che abbia giocato con la ventola al limite. Se la frequenza l'hai abbassata tu resta dove l'hai messa: la guardia disfa soltanto quello che ha fatto lei. Arriva con <code>sudo apt update &amp;&amp; sudo apt upgrade</code>.",
      en: "On the BC-250 a guard watches the temperature and takes 100 MHz off the processor when the board runs hot. It now <strong>gives them back</strong>: as soon as the board cools down the frequency climbs again, and stops where it started. On our bench that is worth <strong>1.2% of the frames</strong> on a machine that has played with the fan at its limit. If you lowered the frequency yourself it stays where you put it: the guard only undoes its own work. It arrives with <code>sudo apt update &amp;&amp; sudo apt upgrade</code>.",
      pl: "Na BC-250 strażnik pilnuje temperatury i zabiera procesorowi 100 MHz, gdy płyta za bardzo się grzeje. Teraz <strong>je oddaje</strong>: gdy tylko płyta ostygnie, częstotliwość wraca i zatrzymuje się tam, skąd wyszła. Na naszym stanowisku to <strong>1,2% klatek</strong> na maszynie, która grała z wentylatorem na granicy. Jeśli częstotliwość obniżyłeś sam, zostaje tam, gdzie ją ustawiłeś: strażnik cofa tylko to, co zrobił sam. Przychodzi z <code>sudo apt update &amp;&amp; sudo apt upgrade</code>.",
      uk: "На BC-250 сторож стежить за температурою і забирає в процесора 100 МГц, коли плата надто гріється. Тепер він <strong>їх повертає</strong>: щойно плата охолоне, частота підіймається і спиняється там, звідки вийшла. На нашому стенді це <strong>1,2% кадрів</strong> на машині, яка грала з вентилятором на межі. Якщо частоту знизили ви самі, вона лишається там, де ви її поставили: сторож скасовує лише те, що зробив сам. Надходить із <code>sudo apt update &amp;&amp; sudo apt upgrade</code>.",
      ru: "На BC-250 сторож следит за температурой и снимает с процессора 100 МГц, когда плата слишком греется. Теперь он <strong>их возвращает</strong>: как только плата остывает, частота поднимается и останавливается там, откуда ушла. На нашем стенде это <strong>1,2% кадров</strong> на машине, которая играла с вентилятором на пределе. Если частоту снизили вы сами, она остаётся там, где вы её поставили: сторож отменяет только то, что сделал сам. Приходит с <code>sudo apt update &amp;&amp; sudo apt upgrade</code>.",
      es: "En la BC-250 un guardia vigila la temperatura y le quita 100 MHz al procesador cuando la placa se calienta demasiado. Ahora <strong>se los devuelve</strong>: en cuanto la placa se enfría la frecuencia vuelve a subir, y se para donde había empezado. En nuestro banco son <strong>1,2% de fotogramas</strong> en una máquina que haya jugado con el ventilador al límite. Si la frecuencia la bajaste tú, se queda donde la pusiste: el guardia deshace solo lo que ha hecho él. Llega con <code>sudo apt update &amp;&amp; sudo apt upgrade</code>.",
      pt: "Na BC-250 um guarda vigia a temperatura e tira 100 MHz ao processador quando a placa aquece demais. Agora <strong>devolve-os</strong>: assim que a placa arrefece a frequência volta a subir, e para onde tinha começado. No nosso banco são <strong>1,2% dos fotogramas</strong> numa máquina que tenha jogado com a ventoinha no limite. Se foste tu a baixar a frequência, fica onde a puseste: o guarda desfaz só o que fez ele. Chega com <code>sudo apt update &amp;&amp; sudo apt upgrade</code>.",
      de: "Auf der BC-250 wacht ein Wächter über die Temperatur und nimmt dem Prozessor 100 MHz weg, wenn die Karte zu heiß wird. Jetzt <strong>gibt er sie zurück</strong>: sobald die Karte abkühlt, steigt der Takt wieder und bleibt dort stehen, wo er losgegangen ist. Auf unserem Prüfstand sind das <strong>1,2% der Bilder</strong> auf einer Maschine, die einmal mit dem Lüfter am Anschlag gespielt hat. Wenn Sie den Takt selbst gesenkt haben, bleibt er, wo Sie ihn hingesetzt haben: der Wächter macht nur seine eigene Arbeit rückgängig. Kommt mit <code>sudo apt update &amp;&amp; sudo apt upgrade</code>.",
      fr: "Sur la BC-250, une garde surveille la température et retire 100 MHz au processeur quand la carte chauffe trop. Elle les <strong>rend</strong> désormais : dès que la carte refroidit, la fréquence remonte et s'arrête là où elle était partie. Sur notre banc, cela vaut <strong>1,2% des images</strong> sur une machine ayant joué avec le ventilateur à la limite. Si c'est vous qui avez baissé la fréquence, elle reste où vous l'avez mise : la garde ne défait que son propre travail. Arrive avec <code>sudo apt update &amp;&amp; sudo apt upgrade</code>.",
    },
  },
  {
    data: '2026-08-26',
    quando: { it: "26 agosto 2026", en: "26 August 2026", pl: "26 sierpnia 2026", uk: "26 серпня 2026", ru: "26 августа 2026", es: "26 de agosto de 2026", pt: "26 de agosto de 2026", de: "26. August 2026", fr: "26 août 2026" },
    etichetta: { it: "aggiornamento", en: "update", pl: "aktualizacja", uk: "оновлення", ru: "обновление", es: "actualización", pt: "atualização", de: "Update", fr: "mise à jour" },
    titolo: {
      it: "SkillFishOS parte con Secure Boot acceso",
      en: "SkillFishOS starts with Secure Boot on",
      pl: "SkillFishOS uruchamia się z włączonym Secure Boot",
      uk: "SkillFishOS запускається з увімкненим Secure Boot",
      ru: "SkillFishOS запускается с включённым Secure Boot",
      es: "SkillFishOS arranca con Secure Boot activado",
      pt: "O SkillFishOS arranca com o Secure Boot ligado",
      de: "SkillFishOS startet mit eingeschaltetem Secure Boot",
      fr: "SkillFishOS démarre avec Secure Boot activé"
    },
    testo: {
      it: "SkillFishOS parte con Secure Boot acceso, come esce di fabbrica quasi ogni PC. Il kernel lo compiliamo noi e lo firmiamo noi: <strong>skillfish-secureboot</strong> fa registrare la nostra chiave nel firmware del tuo computer, una volta sola, con una conferma al riavvio. <strong>Il primo avvio dalla chiavetta vuole ancora Secure Boot spento</strong>, perché la chiave non si può registrare prima.",
      en: "SkillFishOS boots with Secure Boot on, the way almost every PC leaves the factory. We build the kernel and we sign it: <strong>skillfish-secureboot</strong> gets our key enrolled in your computer's firmware, once, with a confirmation at the next restart. <strong>The first boot from the USB stick still wants Secure Boot off</strong>, because the key cannot be enrolled before that.",
      pl: "SkillFishOS uruchamia się z włączonym Secure Boot, tak jak niemal każdy komputer wychodzi z fabryki. Jądro kompilujemy i podpisujemy my: <strong>skillfish-secureboot</strong> rejestruje nasz klucz w firmware twojego komputera, raz, z potwierdzeniem przy ponownym uruchomieniu. <strong>Pierwszy start z pendrive'a nadal wymaga wyłączonego Secure Boot</strong>, bo wcześniej klucza nie da się zarejestrować.",
      uk: "SkillFishOS запускається з увімкненим Secure Boot, як майже кожен ПК виходить із заводу. Ядро збираємо і підписуємо ми: <strong>skillfish-secureboot</strong> реєструє наш ключ у мікропрограмі вашого комп'ютера, один раз, із підтвердженням при перезавантаженні. <strong>Перший запуск із флешки все ще потребує вимкненого Secure Boot</strong>, бо раніше ключ зареєструвати не можна.",
      ru: "SkillFishOS запускается с включённым Secure Boot, как почти каждый ПК выходит с завода. Ядро собираем и подписываем мы: <strong>skillfish-secureboot</strong> регистрирует наш ключ в прошивке вашего компьютера, один раз, с подтверждением при перезагрузке. <strong>Первый запуск с флешки всё ещё требует выключенного Secure Boot</strong>, потому что раньше ключ зарегистрировать нельзя.",
      es: "SkillFishOS arranca con Secure Boot encendido, tal como sale de fábrica casi cualquier PC. El kernel lo compilamos y lo firmamos nosotros: <strong>skillfish-secureboot</strong> registra nuestra clave en el firmware de tu ordenador, una sola vez, con una confirmación al reiniciar. <strong>El primer arranque desde el pendrive sigue queriendo Secure Boot apagado</strong>, porque antes la clave no se puede registrar.",
      pt: "O SkillFishOS arranca com o Secure Boot ligado, tal como quase todos os PCs saem de fábrica. O kernel somos nós que o compilamos e assinamos: o <strong>skillfish-secureboot</strong> regista a nossa chave no firmware do teu computador, uma só vez, com uma confirmação ao reiniciar. <strong>O primeiro arranque a partir da pen ainda quer o Secure Boot desligado</strong>, porque antes disso a chave não se pode registar.",
      de: "SkillFishOS startet mit eingeschaltetem Secure Boot, so wie fast jeder PC das Werk verlässt. Den Kernel bauen und signieren wir: <strong>skillfish-secureboot</strong> trägt unseren Schlüssel in die Firmware Ihres Rechners ein, einmal, mit einer Bestätigung beim Neustart. <strong>Der erste Start vom USB-Stick will Secure Boot weiterhin aus</strong>, denn vorher lässt sich der Schlüssel nicht eintragen.",
      fr: "SkillFishOS démarre avec Secure Boot activé, comme presque tous les PC sortent d'usine. Le noyau, nous le compilons et le signons : <strong>skillfish-secureboot</strong> fait enregistrer notre clé dans le firmware de votre ordinateur, une seule fois, avec une confirmation au redémarrage. <strong>Le premier démarrage depuis la clé USB veut toujours Secure Boot désactivé</strong>, car la clé ne peut pas être enregistrée avant.",
    },
  },
  {
    data: '2026-08-23',
    quando: { it: "23 agosto 2026", en: "23 August 2026", pl: "23 sierpnia 2026", uk: "23 серпня 2026", ru: "23 августа 2026", es: "23 de agosto de 2026", pt: "23 de agosto de 2026", de: "23. August 2026", fr: "23 août 2026" },
    etichetta: { it: "aggiornamento", en: "update", pl: "aktualizacja", uk: "оновлення", ru: "обновление", es: "actualización", pt: "atualização", de: "Update", fr: "mise à jour" },
    titolo: {
      it: "Un kernel anche per i PC normali",
      en: "A kernel for ordinary PCs too",
      pl: "Jądro także dla zwykłych pecetów",
      uk: "Ядро й для звичайних ПК",
      ru: "Ядро и для обычных ПК",
      es: "Un núcleo también para los PC normales",
      pt: "Um kernel também para os PC normais",
      de: "Ein Kernel auch für gewöhnliche PCs",
      fr: "Un noyau aussi pour les PC ordinaires"
    },
    testo: {
      it: "Il pacchetto del kernel guarda la macchina prima di scaricare: su una BC-250 prende il kernel della scheda, su un PC qualunque una versione <strong>-x64</strong>, compilata per un processore generico e con i firmware e i driver che servono a un portatile. Nello stesso giro i servizi che hanno senso solo sulla scheda controllano da soli su cosa stanno girando, così su un PC normale non partono affatto invece di provarci a ogni avvio.",
      en: "The kernel package looks at the machine before downloading: on a BC-250 it takes the board's kernel, on an ordinary PC an <strong>-x64</strong> build, made for a generic processor and carrying the firmware and drivers a laptop needs. In the same pass, the services that only make sense on the board now check for themselves what they are running on, so on an ordinary PC they do not start at all instead of trying at every boot.",
      pl: "Pakiet jądra sprawdza maszynę przed pobraniem: na BC-250 bierze jądro płyty, na zwykłym pececie wersję <strong>-x64</strong>, skompilowaną pod ogólny procesor i z firmware oraz sterownikami potrzebnymi laptopowi. Przy okazji usługi, które mają sens tylko na płycie, same sprawdzają, na czym działają, więc na zwykłym pececie w ogóle nie startują, zamiast próbować przy każdym uruchomieniu.",
      uk: "Пакет ядра дивиться на машину перед завантаженням: на BC-250 бере ядро плати, на звичайному ПК версію <strong>-x64</strong>, зібрану під загальний процесор і з мікропрограмами та драйверами, потрібними ноутбуку. Заразом служби, які мають сенс лише на платі, самі перевіряють, на чому працюють, тож на звичайному ПК вони взагалі не запускаються замість того, щоб пробувати за кожного завантаження.",
      ru: "Пакет ядра смотрит на машину перед загрузкой: на BC-250 берёт ядро платы, на обычном ПК версию <strong>-x64</strong>, собранную под общий процессор и с прошивками и драйверами, нужными ноутбуку. Заодно службы, которые имеют смысл только на плате, сами проверяют, на чём работают, поэтому на обычном ПК они вовсе не запускаются, вместо того чтобы пытаться при каждой загрузке.",
      es: "El paquete del kernel mira la máquina antes de descargar: en una BC-250 toma el kernel de la placa, en un PC cualquiera una versión <strong>-x64</strong>, compilada para un procesador genérico y con los firmwares y controladores que necesita un portátil. En la misma pasada, los servicios que solo tienen sentido en la placa comprueban por sí mismos sobre qué están corriendo, así que en un PC normal no arrancan en absoluto en vez de intentarlo en cada inicio.",
      pt: "O pacote do kernel olha para a máquina antes de descarregar: numa BC-250 leva o kernel da placa, num PC qualquer uma versão <strong>-x64</strong>, compilada para um processador genérico e com os firmwares e controladores de que um portátil precisa. Na mesma passagem, os serviços que só fazem sentido na placa verificam eles próprios sobre o que estão a correr, por isso num PC normal não arrancam de todo em vez de tentarem a cada arranque.",
      de: "Das Kernel-Paket sieht sich die Maschine an, bevor es lädt: auf einer BC-250 nimmt es den Kernel der Karte, auf einem gewöhnlichen PC eine <strong>-x64</strong>-Ausgabe, für einen generischen Prozessor gebaut und mit der Firmware und den Treibern, die ein Notebook braucht. Im selben Zug prüfen die Dienste, die nur auf der Karte Sinn ergeben, selbst nach, worauf sie laufen: auf einem gewöhnlichen PC starten sie gar nicht erst, statt es bei jedem Start zu versuchen.",
      fr: "Le paquet du noyau regarde la machine avant de télécharger : sur une BC-250 il prend le noyau de la carte, sur un PC ordinaire une version <strong>-x64</strong>, compilée pour un processeur générique et avec les firmwares et pilotes dont un portable a besoin. Dans la foulée, les services qui n'ont de sens que sur la carte vérifient eux-mêmes sur quoi ils tournent : sur un PC ordinaire ils ne démarrent pas du tout, au lieu d'essayer à chaque démarrage.",
    },
  },
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
      it: "Il kernel <strong>7.2.0</strong> ora arriva con un normale aggiornamento. Prima stava solo fra i file da scaricare a mano su GitHub. Non è più veloce del 7.1.7, le differenze che abbiamo misurato stanno dentro il rumore. Serve a stare al passo con il kernel di riferimento e con i driver. Il driver grafico intanto è alla <strong>Mesa 26.1.6</strong>, la stessa versione che montano le distribuzioni da gioco più aggiornate. Arriva da Debian, non la compiliamo noi.",
      en: "Kernel <strong>7.2.0</strong> now arrives with an ordinary update. Until now it only sat among the files you download by hand on GitHub. It is not faster than 7.1.7, the differences we measured are inside the noise. The point is keeping up with the upstream kernel and its drivers. The graphics driver meanwhile is at <strong>Mesa 26.1.6</strong>, the same version the most up-to-date gaming distributions carry. It comes from Debian; we do not build it.",
      pl: "Jądro <strong>7.2.0</strong> przychodzi teraz ze zwykłą aktualizacją. Wcześniej leżało tylko wśród plików do ręcznego pobrania na GitHubie. Nie jest szybsze od 7.1.7, zmierzone różnice mieszczą się w szumie. Chodzi o to, by nadążać za jądrem źródłowym i jego sterownikami. Sterownik graficzny jest tymczasem w wersji <strong>Mesa 26.1.6</strong>, tej samej, którą mają najbardziej aktualne dystrybucje do grania. Pochodzi z Debiana, nie budujemy go sami.",
      uk: "Ядро <strong>7.2.0</strong> тепер приходить зі звичайним оновленням. Раніше воно лежало тільки серед файлів, які завантажують вручну на GitHub. Воно не швидше за 7.1.7, виміряні відмінності лежать у межах похибки. Сенс у тому, щоб не відставати від основного ядра та його драйверів. Графічний драйвер тим часом має версію <strong>Mesa 26.1.6</strong> — ту саму, що й найсвіжіші ігрові дистрибутиви. Він приходить з Debian, ми його не збираємо.",
      ru: "Ядро <strong>7.2.0</strong> теперь приходит с обычным обновлением. Раньше оно лежало только среди файлов, которые скачивают вручную на GitHub. Оно не быстрее 7.1.7, измеренные различия лежат в пределах шума. Смысл в том, чтобы не отставать от основного ядра и его драйверов. Графический драйвер тем временем — <strong>Mesa 26.1.6</strong>, та же версия, что и в самых свежих игровых дистрибутивах. Он приходит из Debian, мы его не собираем.",
      es: "El núcleo <strong>7.2.0</strong> llega ahora con una actualización normal. Hasta ahora estaba solo entre los archivos que se descargan a mano en GitHub. No es más rápido que el 7.1.7, las diferencias que medimos caen dentro del ruido. Sirve para ir al paso del núcleo de referencia y sus controladores. El controlador gráfico está mientras tanto en <strong>Mesa 26.1.6</strong>, la misma versión que llevan las distribuciones de juego más al día. Viene de Debian, no la compilamos nosotros.",
      pt: "O kernel <strong>7.2.0</strong> chega agora com uma atualização normal. Até aqui estava apenas entre os ficheiros que se descarregam à mão no GitHub. Não é mais rápido do que o 7.1.7, as diferenças que medimos ficam dentro do ruído. Serve para acompanhar o kernel de referência e os seus controladores. O controlador gráfico está entretanto na <strong>Mesa 26.1.6</strong>, a mesma versão que as distribuições de jogo mais atuais levam. Vem do Debian, não somos nós que a compilamos.",
      de: "Kernel <strong>7.2.0</strong> kommt jetzt mit einem gewöhnlichen Update. Bisher lag er nur bei den Dateien, die man auf GitHub von Hand herunterlädt. Er ist nicht schneller als 7.1.7, die gemessenen Unterschiede liegen im Rauschen. Es geht darum, mit dem Referenzkernel und seinen Treibern Schritt zu halten. Der Grafiktreiber ist inzwischen bei <strong>Mesa 26.1.6</strong>, derselben Fassung, die die aktuellsten Spieldistributionen mitbringen. Sie kommt von Debian, wir bauen sie nicht selbst.",
      fr: "Le noyau <strong>7.2.0</strong> arrive maintenant avec une mise à jour ordinaire. Jusqu'ici il ne se trouvait que parmi les fichiers à télécharger à la main sur GitHub. Il n'est pas plus rapide que le 7.1.7, les écarts que nous avons mesurés restent dans le bruit. Il s'agit de suivre le noyau de référence et ses pilotes. Le pilote graphique en est entre-temps à <strong>Mesa 26.1.6</strong>, la même version que celle des distributions de jeu les plus à jour. Elle vient de Debian, ce n'est pas nous qui la compilons."
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
      it: "Nel Tuner l'undervolt della CPU si legge in millivolt: <strong>-150 mV</strong> invece di «-24», che era il numero del firmware, e la riga di riepilogo mostra le due tensioni nello stesso modo. La conversione è misurata sulla scheda: uno scalino vale <strong>6,25 mV</strong>. Il controllo degli aggiornamenti passa da una volta al giorno a <strong>ogni ora</strong>, e la notifica parla solo quando i numeri cambiano.",
      en: "In the Tuner the CPU undervolt reads in millivolts: <strong>-150 mV</strong> instead of «-24», which was the firmware's number, and the summary line shows both voltages the same way. The conversion is measured on the board: one step is <strong>6.25 mV</strong>. The update check goes from once a day to <strong>every hour</strong>, and the notification only speaks when the numbers change.",
      pl: "W Tunerze undervolt procesora czyta się w miliwoltach: <strong>-150 mV</strong> zamiast „-24”, czyli liczby firmware'u, a wiersz podsumowania pokazuje obie wartości tak samo. Przelicznik zmierzono na płycie: jeden stopień to <strong>6,25 mV</strong>. Sprawdzanie aktualizacji przechodzi z raz dziennie na <strong>co godzinę</strong>, a powiadomienie odzywa się tylko wtedy, gdy liczby się zmieniają.",
      uk: "У Tuner андервольт процесора читається в мілівольтах: <strong>-150 мВ</strong> замість «-24», числа мікропрограми, а рядок підсумку показує обидві напруги однаково. Перерахунок виміряно на платі: один щабель це <strong>6,25 мВ</strong>. Перевірка оновлень переходить із раз на день на <strong>щогодини</strong>, а сповіщення озивається лише тоді, коли числа змінюються.",
      ru: "В Тюнере андервольт процессора читается в милливольтах: <strong>-150 мВ</strong> вместо «-24», числа прошивки, а строка сводки показывает оба напряжения одинаково. Пересчёт измерен на плате: одна ступень это <strong>6,25 мВ</strong>. Проверка обновлений переходит с раза в день на <strong>каждый час</strong>, а уведомление подаёт голос только тогда, когда числа меняются.",
      es: "En el Tuner el undervolt de la CPU se lee en milivoltios: <strong>-150 mV</strong> en vez de «-24», que era el número del firmware, y la línea de resumen muestra las dos tensiones igual. La conversión está medida en la placa: un escalón vale <strong>6,25 mV</strong>. La comprobación de actualizaciones pasa de una vez al día a <strong>cada hora</strong>, y la notificación solo habla cuando los números cambian.",
      pt: "No Tuner o undervolt do CPU lê-se em milivolts: <strong>-150 mV</strong> em vez de «-24», que era o número do firmware, e a linha de resumo mostra as duas tensões da mesma maneira. A conversão é medida na placa: um degrau vale <strong>6,25 mV</strong>. A verificação de atualizações passa de uma vez por dia a <strong>cada hora</strong>, e a notificação só fala quando os números mudam.",
      de: "Im Tuner steht die CPU-Untervoltung in Millivolt: <strong>-150 mV</strong> statt »-24«, der Zahl der Firmware, und die Übersichtszeile zeigt beide Spannungen gleich. Die Umrechnung ist auf der Karte gemessen: eine Stufe sind <strong>6,25 mV</strong>. Die Aktualisierungsprüfung geht von einmal täglich auf <strong>stündlich</strong>, und die Meldung spricht nur, wenn sich die Zahlen ändern.",
      fr: "Dans le Tuner, le sous-voltage du processeur se lit en millivolts : <strong>-150 mV</strong> au lieu de « -24 », le chiffre du firmware, et la ligne de résumé affiche les deux tensions de la même façon. La conversion est mesurée sur la carte : un cran vaut <strong>6,25 mV</strong>. La vérification des mises à jour passe d'une fois par jour à <strong>toutes les heures</strong>, et la notification ne parle que quand les chiffres changent.",
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
      it: "Le immagini 26.06.x precedenti sono state <strong>sostituite</strong>: se ne hai una, scarica la 26.06.4. Sulla BC-250 l'installazione arriva in fondo e il sistema installato su <strong>Btrfs</strong> si avvia. Lo sblocco degli otto core parte disattivato e si chiede dal Tuner a macchina installata.",
      en: "The earlier 26.06.x images have been <strong>replaced</strong>: if you have one, download 26.06.4. On the BC-250 the install reaches the end and a system installed on <strong>Btrfs</strong> boots. Unlocking the eight cores starts out switched off and is asked for from the Tuner once the machine is installed.",
      pl: "Wcześniejsze obrazy 26.06.x zostały <strong>zastąpione</strong>: jeśli masz któryś, pobierz 26.06.4. Na BC-250 instalacja dochodzi do końca, a system zainstalowany na <strong>Btrfs</strong> uruchamia się. Odblokowanie ośmiu rdzeni jest domyślnie wyłączone i włącza się je z Tunera, gdy maszyna jest już zainstalowana.",
      uk: "Попередні образи 26.06.x <strong>замінено</strong>: якщо у вас є котрийсь, завантажте 26.06.4. На BC-250 встановлення доходить до кінця, а система, встановлена на <strong>Btrfs</strong>, запускається. Розблокування восьми ядер початково вимкнене і вмикається з Tuner, коли машина вже встановлена.",
      ru: "Прежние образы 26.06.x <strong>заменены</strong>: если у вас есть какой-то из них, скачайте 26.06.4. На BC-250 установка доходит до конца, а система, установленная на <strong>Btrfs</strong>, запускается. Разблокировка восьми ядер изначально выключена и включается из Tuner, когда машина уже установлена.",
      es: "Las imágenes 26.06.x anteriores han sido <strong>sustituidas</strong>: si tienes una, descarga la 26.06.4. En la BC-250 la instalación llega hasta el final y el sistema instalado en <strong>Btrfs</strong> arranca. El desbloqueo de los ocho núcleos viene desactivado y se pide desde el Tuner con la máquina ya instalada.",
      pt: "As imagens 26.06.x anteriores foram <strong>substituídas</strong>: se tens uma, descarrega a 26.06.4. Na BC-250 a instalação chega ao fim e o sistema instalado em <strong>Btrfs</strong> arranca. O desbloqueio dos oito núcleos começa desativado e pede-se a partir do Tuner com a máquina já instalada.",
      de: "Die früheren 26.06.x-Abbilder wurden <strong>ersetzt</strong>: wenn Sie eines haben, laden Sie 26.06.4 herunter. Auf der BC-250 kommt die Installation bis zum Ende durch, und ein auf <strong>Btrfs</strong> installiertes System startet. Das Freischalten der acht Kerne ist zunächst aus und wird im Tuner angefordert, wenn die Maschine installiert ist.",
      fr: "Les images 26.06.x précédentes ont été <strong>remplacées</strong> : si vous en avez une, téléchargez la 26.06.4. Sur la BC-250, l'installation va jusqu'au bout et un système installé sur <strong>Btrfs</strong> démarre. Le déverrouillage des huit cœurs part désactivé et se demande depuis le Tuner, une fois la machine installée.",
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
      it: "<strong>⚠️ Questa immagine è stata sostituita: usa la 26.06.4.</strong><br><br>Due edizioni, <strong>BC-250</strong> e <strong>Generic</strong>, per la scheda AMD e per qualsiasi PC o macchina virtuale x86-64. La lingua che scegli vale <strong>ovunque</strong>: interfaccia, accesso, pannello web e diapositive dell'installatore. Sotto: kernel <strong>7.1.7</strong> con 40 Compute Unit e otto core, Btrfs con punti di ripristino dal primo avvio, AI locale su GPU.",
      en: "<strong>⚠️ This image has been replaced: use 26.06.4.</strong><br><br>Two editions, <strong>BC-250</strong> and <strong>Generic</strong>, for the AMD board and for any x86-64 PC or virtual machine. The language you pick now applies <strong>everywhere</strong>: interface, login screen, web panel and the installer's slides. Underneath: kernel <strong>7.1.7</strong> with 40 Compute Units and eight cores, Btrfs with restore points from the first boot, local AI on the GPU.",
      pl: "<strong>⚠️ Ten obraz został zastąpiony: użyj 26.06.4.</strong><br><br>Dwie edycje, <strong>BC-250</strong> i <strong>Generic</strong>, dla płyty AMD i dla dowolnego peceta lub maszyny wirtualnej x86-64. Wybrany język obowiązuje <strong>wszędzie</strong>: interfejs, ekran logowania, panel webowy i slajdy instalatora. Pod spodem: jądro <strong>7.1.7</strong> z 40 Compute Unitami i ośmioma rdzeniami, Btrfs z punktami przywracania od pierwszego uruchomienia, lokalne AI na GPU.",
      uk: "<strong>⚠️ Цей образ замінено: використовуйте 26.06.4.</strong><br><br>Два видання, <strong>BC-250</strong> і <strong>Generic</strong>, для плати AMD і для будь-якого ПК чи віртуальної машини x86-64. Обрана мова діє <strong>всюди</strong>: інтерфейс, екран входу, вебпанель і слайди встановлювача. Під сподом: ядро <strong>7.1.7</strong> з 40 Compute Unit і вісьмома ядрами, Btrfs із точками відновлення від першого запуску, локальний ШІ на GPU.",
      ru: "<strong>⚠️ Этот образ заменён: используйте 26.06.4.</strong><br><br>Два издания, <strong>BC-250</strong> и <strong>Generic</strong>, для платы AMD и для любого ПК или виртуальной машины x86-64. Выбранный язык действует <strong>везде</strong>: интерфейс, экран входа, веб-панель и слайды установщика. Под капотом: ядро <strong>7.1.7</strong> с 40 Compute Unit и восемью ядрами, Btrfs с точками восстановления с первого запуска, локальный ИИ на GPU.",
      es: "<strong>⚠️ Esta imagen ha sido sustituida: usa la 26.06.4.</strong><br><br>Dos ediciones, <strong>BC-250</strong> y <strong>Generic</strong>, para la placa AMD y para cualquier PC o máquina virtual x86-64. El idioma que elijas vale <strong>en todas partes</strong>: interfaz, pantalla de acceso, panel web y diapositivas del instalador. Debajo: kernel <strong>7.1.7</strong> con 40 Compute Units y ocho núcleos, Btrfs con puntos de restauración desde el primer arranque, IA local en la GPU.",
      pt: "<strong>⚠️ Esta imagem foi substituída: usa a 26.06.4.</strong><br><br>Duas edições, <strong>BC-250</strong> e <strong>Generic</strong>, para a placa AMD e para qualquer PC ou máquina virtual x86-64. O idioma que escolhes vale <strong>em todo o lado</strong>: interface, ecrã de acesso, painel web e diapositivos do instalador. Por baixo: kernel <strong>7.1.7</strong> com 40 Compute Units e oito núcleos, Btrfs com pontos de restauro desde o primeiro arranque, IA local na GPU.",
      de: "<strong>⚠️ Dieses Abbild wurde ersetzt: nehmen Sie 26.06.4.</strong><br><br>Zwei Ausgaben, <strong>BC-250</strong> und <strong>Generic</strong>, für die AMD-Karte und für jeden x86-64-PC oder jede virtuelle Maschine. Die gewählte Sprache gilt <strong>überall</strong>: Oberfläche, Anmeldebildschirm, Webpanel und die Folien des Installationsprogramms. Darunter: Kernel <strong>7.1.7</strong> mit 40 Compute Units und acht Kernen, Btrfs mit Wiederherstellungspunkten ab dem ersten Start, lokale KI auf der GPU.",
      fr: "<strong>⚠️ Cette image a été remplacée : utilisez la 26.06.4.</strong><br><br>Deux éditions, <strong>BC-250</strong> et <strong>Generic</strong>, pour la carte AMD et pour n'importe quel PC ou machine virtuelle x86-64. La langue choisie vaut <strong>partout</strong> : interface, écran de connexion, panneau web et diapositives de l'installateur. Dessous : noyau <strong>7.1.7</strong> avec 40 Compute Units et huit cœurs, Btrfs avec points de restauration dès le premier démarrage, IA locale sur le GPU.",
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
      it: "Il sistema fa un punto di ripristino <strong>prima</strong> e uno <strong>dopo</strong> ogni operazione di <code>apt</code>, ne tiene cinque e li elenca nel menu di avvio. Per tornare indietro davvero c'è <code>sudo skillfish-rollback 12</code>: al riavvio il sistema è quello di allora, e <code>--annulla</code> rimette le cose com'erano. La <strong>cartella personale non viene mai toccata</strong>.",
      en: "The system takes a restore point <strong>before</strong> and one <strong>after</strong> every <code>apt</code> operation, keeps five of them and lists them in the boot menu. To actually go back there is <code>sudo skillfish-rollback 12</code>: at the next restart the system is the one from then, and <code>--annulla</code> puts things back. Your <strong>home directory is never touched</strong>.",
      pl: "System robi punkt przywracania <strong>przed</strong> i <strong>po</strong> każdej operacji <code>apt</code>, trzyma pięć i wypisuje je w menu startowym. Żeby naprawdę cofnąć się, jest <code>sudo skillfish-rollback 12</code>: po ponownym uruchomieniu system jest tym sprzed, a <code>--annulla</code> przywraca stan poprzedni. <strong>Katalog domowy nie jest nigdy ruszany</strong>.",
      uk: "Система робить точку відновлення <strong>перед</strong> і <strong>після</strong> кожної операції <code>apt</code>, тримає п'ять і перелічує їх у меню завантаження. Щоб справді повернутися назад, є <code>sudo skillfish-rollback 12</code>: після перезавантаження система така, як була тоді, а <code>--annulla</code> повертає все як було. <strong>Домашню теку ніколи не чіпають</strong>.",
      ru: "Система делает точку восстановления <strong>до</strong> и <strong>после</strong> каждой операции <code>apt</code>, держит пять и перечисляет их в меню загрузки. Чтобы действительно вернуться назад, есть <code>sudo skillfish-rollback 12</code>: после перезагрузки система такая, какой была тогда, а <code>--annulla</code> возвращает всё обратно. <strong>Домашний каталог никогда не трогают</strong>.",
      es: "El sistema hace un punto de restauración <strong>antes</strong> y otro <strong>después</strong> de cada operación de <code>apt</code>, guarda cinco y los lista en el menú de arranque. Para volver atrás de verdad está <code>sudo skillfish-rollback 12</code>: al reiniciar el sistema es el de entonces, y <code>--annulla</code> deja las cosas como estaban. La <strong>carpeta personal no se toca nunca</strong>.",
      pt: "O sistema faz um ponto de restauro <strong>antes</strong> e outro <strong>depois</strong> de cada operação do <code>apt</code>, guarda cinco e lista-os no menu de arranque. Para voltar atrás a sério há <code>sudo skillfish-rollback 12</code>: ao reiniciar o sistema é o de então, e <code>--annulla</code> repõe tudo. A <strong>pasta pessoal nunca é tocada</strong>.",
      de: "Das System legt <strong>vor</strong> und <strong>nach</strong> jedem <code>apt</code>-Vorgang einen Wiederherstellungspunkt an, behält fünf davon und führt sie im Startmenü auf. Um wirklich zurückzugehen, gibt es <code>sudo skillfish-rollback 12</code>: beim nächsten Neustart ist das System das von damals, und <code>--annulla</code> stellt alles zurück. Das <strong>Benutzerverzeichnis wird nie angefasst</strong>.",
      fr: "Le système prend un point de restauration <strong>avant</strong> et un <strong>après</strong> chaque opération d'<code>apt</code>, en garde cinq et les liste dans le menu de démarrage. Pour revenir en arrière pour de vrai, il y a <code>sudo skillfish-rollback 12</code> : au redémarrage le système est celui d'alors, et <code>--annulla</code> remet les choses comme elles étaient. Le <strong>dossier personnel n'est jamais touché</strong>.",
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

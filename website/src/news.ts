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
    // ai-level-allowlist-2026-09-13
    data: '2026-09-13',
    quando: { it: "13 settembre 2026", en: "13 September 2026", pl: "13 września 2026", uk: "13 вересня 2026", ru: "13 сентября 2026", es: "13 de septiembre de 2026", pt: "13 de setembro de 2026", de: "13. September 2026", fr: "13 septembre 2026" },
    etichetta: { it: "aggiornamento", en: "update", pl: "aktualizacja", uk: "оновлення", ru: "обновление", es: "actualización", pt: "atualização", de: "Aktualisierung", fr: "mise à jour" },
    titolo: {
      it: "Il pannello AI accetta solo quello che esiste",
      en: "The AI panel only accepts what exists",
      pl: "Panel AI przyjmuje tylko to, co istnieje",
      uk: "Панель ШІ приймає лише те, що існує",
      ru: "Панель ИИ принимает только то, что существует",
      es: "El panel IA solo acepta lo que existe",
      pt: "O painel IA só aceita o que existe",
      de: "Die KI-Seite nimmt nur an, was es gibt",
      fr: "Le panneau IA n'accepte que ce qui existe",
    },
    testo: {
      it: "Il livello e il modello della modalità AI si scelgono da un elenco chiuso: il Remote Manager e il Control Center passano al motore solo quello che esiste davvero sulla scheda. Una richiesta costruita a mano non può più far aprire a <b>llama-server</b> un file qualsiasi del disco. È nei pacchetti <b>26.09.18</b>, si prende con il normale aggiornamento.",
      en: "The AI-mode level and model are picked from a closed list: the Remote Manager and the Control Center only hand the engine what really exists on the board. A request built by hand can no longer make <b>llama-server</b> open any file on the disk. It is in the <b>26.09.18</b> packages, and comes with the usual update.",
      pl: "Poziom i model trybu AI wybiera się z zamkniętej listy: Remote Manager i Control Center przekazują silnikowi tylko to, co naprawdę jest na płycie. Ręcznie spreparowane żądanie nie każe już <b>llama-server</b> otworzyć dowolnego pliku na dysku. Jest w pakietach <b>26.09.18</b>, przychodzi ze zwykłą aktualizacją.",
      uk: "Рівень і модель режиму ШІ обираються із закритого переліку: Remote Manager і Control Center передають рушію лише те, що справді є на платі. Запит, складений вручну, більше не змусить <b>llama-server</b> відкрити довільний файл на диску. Це в пакунках <b>26.09.18</b>, приходить зі звичайним оновленням.",
      ru: "Уровень и модель режима ИИ выбираются из закрытого списка: Remote Manager и Control Center передают движку только то, что действительно есть на плате. Запрос, составленный вручную, больше не заставит <b>llama-server</b> открыть произвольный файл на диске. Это в пакетах <b>26.09.18</b>, приходит с обычным обновлением.",
      es: "El nivel y el modelo del modo IA se eligen de una lista cerrada: el Remote Manager y el Control Center sólo pasan al motor lo que existe de verdad en la placa. Una petición hecha a mano ya no puede hacer que <b>llama-server</b> abra cualquier archivo del disco. Está en los paquetes <b>26.09.18</b>, llega con la actualización normal.",
      pt: "O nível e o modelo do modo IA escolhem-se de uma lista fechada: o Remote Manager e o Control Center só passam ao motor o que existe mesmo na placa. Um pedido feito à mão já não faz o <b>llama-server</b> abrir um ficheiro qualquer do disco. Está nos pacotes <b>26.09.18</b>, chega com a atualização normal.",
      de: "Stufe und Modell des KI-Modus werden aus einer geschlossenen Liste gewählt: Remote Manager und Control Center geben der Maschine nur weiter, was auf der Karte wirklich vorhanden ist. Eine von Hand gebaute Anfrage kann <b>llama-server</b> keine beliebige Datei der Platte mehr öffnen lassen. Es steckt in den Paketen <b>26.09.18</b> und kommt mit der gewöhnlichen Aktualisierung.",
      fr: "Le niveau et le modèle du mode IA se choisissent dans une liste fermée : le Remote Manager et le Control Center ne transmettent au moteur que ce qui existe vraiment sur la carte. Une requête fabriquée à la main ne peut plus faire ouvrir à <b>llama-server</b> n'importe quel fichier du disque. C'est dans les paquets <b>26.09.18</b>, et cela arrive avec la mise à jour habituelle.",
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

import QtQuick 2.0;
import calamares.slideshow 1.0;

/*
 * Presentazione mostrata durante l'installazione.
 *
 * PERCHE' E' STATA RIFATTA
 * I testi erano cablati in italiano. Chi installava in polacco — o in
 * qualunque altra lingua — si guardava cinque schermate in una lingua che
 * magari non conosce, proprio nel momento in cui il sistema si presenta.
 * Le diapositive NON sono immagini con il testo dentro (lo sfondo e' uno solo,
 * background.png): i testi stanno qui, quindi bastava tradurli.
 *
 * PERCHE' USCIVA COMUNQUE IN INGLESE
 * Prima la lingua stava in un binding scritto cosi':
 *
 *     property string lang: { var n = Qt.locale().name; ... }
 *
 * Qt.locale() NON e' una proprieta' reattiva: il binding si calcola una volta
 * sola, alla creazione del componente. E il componente nasce all'avvio di
 * Calamares, cioe' PRIMA che l'utente scelga la lingua. Il valore restava
 * inchiodato alla lingua della sessione live (inglese) e non cambiava piu',
 * qualunque cosa scegliesse l'utente. Le traduzioni c'erano tutte: nessuno le
 * andava mai a prendere.
 *
 * Adesso la lingua si ricava da due fonti indipendenti:
 *   1. Qt.uiLanguage — questa SI' che e' reattiva: quando Calamares installa il
 *      traduttore della lingua scelta, i binding che la leggono si ricalcolano;
 *   2. una nuova lettura dentro onActivate(), che Calamares chiama quando la
 *      presentazione parte davvero, cioe' a scelta ormai fatta.
 *
 * Regola uguale a quella delle app: se una lingua manca, si ricade sull'inglese
 * invece di mostrare una stringa vuota.
 *
 * ⚠️ Ucraino, russo, spagnolo, portoghese e tedesco NON sono rivisti da
 * madrelingua: li ha scritti il team. Il polacco invece e' di Cyryl Sochacki.
 * Correzioni benvenute.
 */
Presentation {
    id: presentation

    // it / pl / uk / ru / es / pt / de / en, con l'inglese come base
    property string lang: presentation.linguaDa(Qt.uiLanguage ? Qt.uiLanguage : Qt.locale().name)

    // accetta sia "pl_PL" sia "pl-PL" sia "pl"
    function linguaDa(n) {
        if (!n) return "en";
        var s = String(n).replace("-", "_");
        if (s.indexOf("it") === 0) return "it";
        if (s.indexOf("pl") === 0) return "pl";
        if (s.indexOf("uk") === 0 || s.indexOf("ua") === 0) return "uk";
        if (s.indexOf("ru") === 0) return "ru";
        if (s.indexOf("es") === 0) return "es";
        // il portoghese e' scritto per il Brasile, ma vale anche per pt_PT:
        // meglio del ripiego inglese.
        if (s.indexOf("pt") === 0) return "pt";
        if (s.indexOf("de") === 0) return "de";
        return "en";
    }

    function tr(s) { return s[presentation.lang] !== undefined ? s[presentation.lang] : s["en"]; }

    property var s1: {
        "en": "<h1 style='color:#d8a849'>SkillFishOS</h1><h2>The Linux console that plays and teaches</h2><p>Built to get kids using and learning Linux — while they game.</p>",
        "it": "<h1 style='color:#d8a849'>SkillFishOS</h1><h2>La console Linux che gioca e insegna</h2><p>Pensata per far usare e imparare Linux ai più piccoli, mentre giocano.</p>",
        "pl": "<h1 style='color:#d8a849'>SkillFishOS</h1><h2>Konsola z Linuksem, która gra i uczy</h2><p>Stworzona po to, by dzieci używały Linuksa i uczyły się go — grając.</p>",
        "uk": "<h1 style='color:#d8a849'>SkillFishOS</h1><h2>Консоль на Linux, яка грає і навчає</h2><p>Створена, щоб діти користувалися Linux і вчилися його — граючи.</p>",
        "ru": "<h1 style='color:#d8a849'>SkillFishOS</h1><h2>Linux-консоль, которая играет и учит</h2><p>Создана, чтобы дети пользовались Linux и учились ему — играя.</p>",
        "es": "<h1 style='color:#d8a849'>SkillFishOS</h1><h2>La consola Linux que juega y enseña</h2><p>Pensada para que los más pequeños usen Linux y lo aprendan — mientras juegan.</p>",
        "pt": "<h1 style='color:#d8a849'>SkillFishOS</h1><h2>O console Linux que joga e ensina</h2><p>Feito para as crianças usarem Linux e aprenderem — enquanto jogam.</p>",
        "de": "<h1 style='color:#d8a849'>SkillFishOS</h1><h2>Die Linux-Konsole, die spielt und lehrt</h2><p>Gemacht, damit Kinder Linux benutzen und lernen — beim Spielen.</p>"
    }
    property var s2: {
        "en": "<h2 style='color:#d8a849'>Gaming, no compromises</h2><h3>Steam, Heroic, emulators and gamescope</h3><p>All 40 Compute Units unlocked, PlayStation and Switch controllers ready out of the box.</p>",
        "it": "<h2 style='color:#d8a849'>Gaming senza compromessi</h2><h3>Steam, Heroic, emulatori e gamescope</h3><p>Tutte e 40 le Compute Unit sbloccate, controller PlayStation e Switch pronti all'uso.</p>",
        "pl": "<h2 style='color:#d8a849'>Granie bez kompromisów</h2><h3>Steam, Heroic, emulatory i gamescope</h3><p>Wszystkie 40 jednostek obliczeniowych odblokowane, pady PlayStation i Switch działają od ręki.</p>",
        "uk": "<h2 style='color:#d8a849'>Ігри без компромісів</h2><h3>Steam, Heroic, емулятори та gamescope</h3><p>Усі 40 обчислювальних блоків розблоковані, геймпади PlayStation і Switch працюють одразу.</p>",
        "ru": "<h2 style='color:#d8a849'>Игры без компромиссов</h2><h3>Steam, Heroic, эмуляторы и gamescope</h3><p>Все 40 вычислительных блоков разблокированы, геймпады PlayStation и Switch работают сразу.</p>",
        "es": "<h2 style='color:#d8a849'>Juegos sin concesiones</h2><h3>Steam, Heroic, emuladores y gamescope</h3><p>Las 40 unidades de cómputo desbloqueadas, mandos de PlayStation y Switch listos nada más empezar.</p>",
        "pt": "<h2 style='color:#d8a849'>Jogos sem concessões</h2><h3>Steam, Heroic, emuladores e gamescope</h3><p>As 40 unidades de computação liberadas, controles de PlayStation e Switch prontos de cara.</p>",
        "de": "<h2 style='color:#d8a849'>Spielen ohne Abstriche</h2><h3>Steam, Heroic, Emulatoren und gamescope</h3><p>Alle 40 Recheneinheiten freigeschaltet, PlayStation- und Switch-Controller sofort einsatzbereit.</p>"
    }
    property var s3: {
        "en": "<h2 style='color:#d8a849'>Eight cores, not six</h2><h3>The two the board hides</h3><p>The BC-250 ships as 6 cores / 12 threads. The missing two are switched off by configuration, not by defect: SkillFishOS turns them back on at boot. <b>+20% measured</b> on multi-threaded work.</p>",
        "it": "<h2 style='color:#d8a849'>Otto core, non sei</h2><h3>I due che la scheda nasconde</h3><p>La BC-250 si presenta come 6 core / 12 thread. I due mancanti sono spenti dalla configurazione, non difettosi: SkillFishOS li riaccende all'avvio. <b>+20% misurato</b> nei carichi multi-thread.</p>",
        "pl": "<h2 style='color:#d8a849'>Osiem rdzeni, nie sześć</h2><h3>Te dwa, które płyta ukrywa</h3><p>BC-250 zgłasza się jako 6 rdzeni / 12 wątków. Brakujące dwa są wyłączone przez konfigurację, a nie uszkodzone: SkillFishOS włącza je przy starcie. <b>+20% zmierzone</b> w zadaniach wielowątkowych.</p>",
        "uk": "<h2 style='color:#d8a849'>Вісім ядер, а не шість</h2><h3>Ті два, які плата приховує</h3><p>BC-250 представляється як 6 ядер / 12 потоків. Двох бракує через конфігурацію, а не через дефект: SkillFishOS вмикає їх при завантаженні. <b>+20% виміряно</b> в багатопотокових задачах.</p>",
        "ru": "<h2 style='color:#d8a849'>Восемь ядер, а не шесть</h2><h3>Те два, которые плата прячет</h3><p>BC-250 представляется как 6 ядер / 12 потоков. Двух не хватает из-за конфигурации, а не из-за дефекта: SkillFishOS включает их при загрузке. <b>+20% измерено</b> в многопоточных задачах.</p>",
        "es": "<h2 style='color:#d8a849'>Ocho núcleos, no seis</h2><h3>Los dos que la placa esconde</h3><p>La BC-250 se presenta como 6 núcleos / 12 hilos. Los dos que faltan están apagados por configuración, no por defecto de fábrica: SkillFishOS los vuelve a encender al arrancar. <b>+20% medido</b> en cargas multihilo.</p>",
        "pt": "<h2 style='color:#d8a849'>Oito núcleos, não seis</h2><h3>Os dois que a placa esconde</h3><p>A BC-250 se apresenta como 6 núcleos / 12 threads. Os dois que faltam estão desligados por configuração, não por defeito: o SkillFishOS os religa no boot. <b>+20% medido</b> em cargas multithread.</p>",
        "de": "<h2 style='color:#d8a849'>Acht Kerne, nicht sechs</h2><h3>Die zwei, die die Platine verbirgt</h3><p>Die BC-250 meldet sich mit 6 Kernen / 12 Threads. Die fehlenden zwei sind durch die Einrichtung abgeschaltet, nicht defekt: SkillFishOS schaltet sie beim Start wieder ein. <b>+20% gemessen</b> bei Last über viele Threads.</p>"
    }
    property var s4: {
        "en": "<h2 style='color:#d8a849'>Tinker without fear</h2><h3>Automatic Btrfs snapshots</h3><p>Every change gets a safety net: if something goes wrong, you roll back in seconds — straight from the boot menu.</p>",
        "it": "<h2 style='color:#d8a849'>Smanetta senza paura</h2><h3>Snapshot Btrfs automatici</h3><p>Ogni modifica ha la sua rete di salvataggio: se qualcosa va storto, torni indietro in un attimo — dal menu di avvio.</p>",
        "pl": "<h2 style='color:#d8a849'>Eksperymentuj bez obaw</h2><h3>Automatyczne migawki Btrfs</h3><p>Każda zmiana ma siatkę bezpieczeństwa: jeśli coś pójdzie nie tak, cofniesz się w kilka sekund — prosto z menu startowego.</p>",
        "uk": "<h2 style='color:#d8a849'>Експериментуйте без страху</h2><h3>Автоматичні знімки Btrfs</h3><p>Кожна зміна має страхувальну сітку: якщо щось піде не так, ви повернетеся назад за секунди — просто з меню завантаження.</p>",
        "ru": "<h2 style='color:#d8a849'>Экспериментируйте без страха</h2><h3>Автоматические снимки Btrfs</h3><p>У каждого изменения есть страховка: если что-то пойдёт не так, вы вернётесь назад за секунды — прямо из загрузочного меню.</p>",
        "es": "<h2 style='color:#d8a849'>Trastea sin miedo</h2><h3>Instantáneas Btrfs automáticas</h3><p>Cada cambio tiene su red de seguridad: si algo sale mal, vuelves atrás en segundos — desde el propio menú de arranque.</p>",
        "pt": "<h2 style='color:#d8a849'>Mexa sem medo</h2><h3>Snapshots Btrfs automáticos</h3><p>Cada mudança tem a sua rede de segurança: se algo der errado, você volta atrás em segundos — direto do menu de boot.</p>",
        "de": "<h2 style='color:#d8a849'>Bastle ohne Angst</h2><h3>Selbsttätige Btrfs-Schnappschüsse</h3><p>Jede Änderung hat ihr Sicherheitsnetz: geht etwas schief, bist du in Sekunden wieder zurück — direkt aus dem Startmenü.</p>"
    }
    property var s5: {
        "en": "<h2 style='color:#d8a849'>Almost there...</h2><h3>Installing</h3><p>We are setting up your SkillFishOS. Time to play, shortly.</p>",
        "it": "<h2 style='color:#d8a849'>Ci siamo quasi...</h2><h3>Installazione in corso</h3><p>Stiamo preparando il tuo SkillFishOS. Tra poco si gioca!</p>",
        "pl": "<h2 style='color:#d8a849'>Już prawie...</h2><h3>Trwa instalacja</h3><p>Przygotowujemy Twój SkillFishOS. Za chwilę zaczynamy grę!</p>",
        "uk": "<h2 style='color:#d8a849'>Майже готово...</h2><h3>Триває встановлення</h3><p>Готуємо ваш SkillFishOS. Скоро можна грати!</p>",
        "ru": "<h2 style='color:#d8a849'>Уже почти…</h2><h3>Идёт установка</h3><p>Готовим ваш SkillFishOS. Совсем скоро можно играть!</p>",
        "es": "<h2 style='color:#d8a849'>Ya casi...</h2><h3>Instalando</h3><p>Estamos preparando tu SkillFishOS. ¡En nada se juega!</p>",
        "pt": "<h2 style='color:#d8a849'>Quase lá...</h2><h3>Instalando</h3><p>Estamos preparando o seu SkillFishOS. Daqui a pouco é só jogar!</p>",
        "de": "<h2 style='color:#d8a849'>Gleich geschafft ...</h2><h3>Wird installiert</h3><p>Wir richten dein SkillFishOS ein. Gleich geht es ans Spielen!</p>"
    }

    function nextSlide() { presentation.goToNextSlide(); }
    Timer { interval: 8000; running: true; repeat: true; onTriggered: presentation.nextSlide() }

    Rectangle { anchors.fill: parent; color: "#16100a"; z: -2 }

    Slide {
        Image { anchors.fill: parent; source: "background.png"; fillMode: Image.PreserveAspectCrop; opacity: 0.55 }
        Rectangle { anchors.centerIn: parent; width: parent.width * 0.82; height: t1.height + 56; color: "#160f06"; opacity: 0.82; radius: 16; border.color: "#d8a849"; border.width: 2 }
        Text { id: t1; anchors.centerIn: parent; width: parent.width * 0.76; horizontalAlignment: Text.AlignHCenter; wrapMode: Text.WordWrap; textFormat: Text.RichText; color: "#f1e3c6"; font.family: "Helvetica"; font.pixelSize: 22
            text: presentation.tr(presentation.s1) }
    }
    Slide {
        Image { anchors.fill: parent; source: "background.png"; fillMode: Image.PreserveAspectCrop; opacity: 0.55 }
        Rectangle { anchors.centerIn: parent; width: parent.width * 0.82; height: t2.height + 56; color: "#160f06"; opacity: 0.82; radius: 16; border.color: "#d8a849"; border.width: 2 }
        Text { id: t2; anchors.centerIn: parent; width: parent.width * 0.76; horizontalAlignment: Text.AlignHCenter; wrapMode: Text.WordWrap; textFormat: Text.RichText; color: "#f1e3c6"; font.family: "Helvetica"; font.pixelSize: 22
            text: presentation.tr(presentation.s2) }
    }
    Slide {
        Image { anchors.fill: parent; source: "background.png"; fillMode: Image.PreserveAspectCrop; opacity: 0.55 }
        Rectangle { anchors.centerIn: parent; width: parent.width * 0.82; height: t3.height + 56; color: "#160f06"; opacity: 0.82; radius: 16; border.color: "#d8a849"; border.width: 2 }
        Text { id: t3; anchors.centerIn: parent; width: parent.width * 0.76; horizontalAlignment: Text.AlignHCenter; wrapMode: Text.WordWrap; textFormat: Text.RichText; color: "#f1e3c6"; font.family: "Helvetica"; font.pixelSize: 22
            text: presentation.tr(presentation.s3) }
    }
    Slide {
        Image { anchors.fill: parent; source: "background.png"; fillMode: Image.PreserveAspectCrop; opacity: 0.55 }
        Rectangle { anchors.centerIn: parent; width: parent.width * 0.82; height: t4.height + 56; color: "#160f06"; opacity: 0.82; radius: 16; border.color: "#d8a849"; border.width: 2 }
        Text { id: t4; anchors.centerIn: parent; width: parent.width * 0.76; horizontalAlignment: Text.AlignHCenter; wrapMode: Text.WordWrap; textFormat: Text.RichText; color: "#f1e3c6"; font.family: "Helvetica"; font.pixelSize: 22
            text: presentation.tr(presentation.s4) }
    }
    Slide {
        Image { anchors.fill: parent; source: "background.png"; fillMode: Image.PreserveAspectCrop; opacity: 0.55 }
        Rectangle { anchors.centerIn: parent; width: parent.width * 0.82; height: t5.height + 56; color: "#160f06"; opacity: 0.82; radius: 16; border.color: "#d8a849"; border.width: 2 }
        Text { id: t5; anchors.centerIn: parent; width: parent.width * 0.76; horizontalAlignment: Text.AlignHCenter; wrapMode: Text.WordWrap; textFormat: Text.RichText; color: "#f1e3c6"; font.family: "Helvetica"; font.pixelSize: 22
            text: presentation.tr(presentation.s5) }
    }

    // Calamares chiama onActivate() quando la presentazione entra in scena:
    // l'installazione sta partendo, quindi la lingua e' gia' stata scelta da un
    // pezzo. E' il momento buono per rileggerla. L'assegnazione rompe il binding
    // qui sopra, ed e' voluto: da qui in poi la lingua non cambia piu'.
    function onActivate() {
        presentation.lang = presentation.linguaDa(Qt.uiLanguage ? Qt.uiLanguage : Qt.locale().name);
        presentation.currentSlide = 0;
    }
}

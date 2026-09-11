#!/usr/bin/env python3
"""The "on-device AI" page of the website: the two sections that still
described a separate AI panel are rewritten around the AI section of the
Control Center, in the nine languages.

    docs-sito-ai-locale.py <repo>

Everything else on that page (why Vulkan and not ROCm, the engine, the
measured numbers) is still true and is left alone. The sections are found by
position, not by title: each language names them in its own words.
"""
import os
import re
import sys

repo = sys.argv[1] if len(sys.argv) > 1 else "."
DOCS = os.path.join(repo, "website", "src", "content", "docs")

# (title of the models section, body, title of the engine-control section, body)
T = {
"it": ("## I modelli", """I modelli sono file **GGUF** del catalogo di Hugging Face, e si scaricano da due posti: dalla sezione **AI** del [Control Center](/docs/control-center), scrivendo il nome del repository (per esempio `unsloth/Qwen3-4B-GGUF`) e scegliendo la variante dall'elenco, che riporta le dimensioni; oppure dall'Hub dentro Unsloth Studio, che ha la ricerca e le schede complete.

Regola pratica su questa scheda: i 16 GB di GDDR6 sono condivisi tra sistema e GPU, quindi conviene stare sotto gli ~11 GB di pesi per lasciare respiro al resto.""",
       "## Accensione, aggiornamento e chiave", """La sezione **AI** del [Control Center](/docs/control-center) accende e spegne il motore, lo abilita all'avvio e mostra la versione con l'aggiornamento in un clic. Lo stesso c'è nel [Remote Manager](/docs/controllo-remoto), dal browser.

Unsloth genera una password a caso quando si installa, e **si spegne da solo dopo un'ora** se non viene cambiata. Quel passaggio lo fa la sezione AI: scegli la password di Studio e la chiave API viene creata insieme. La chiave serve alla finestra e al Remote Manager per parlare col motore; i modelli sul disco, la memoria (VRAM, GTT, RAM, swap) e una prova di chat con i token al secondo misurati stanno lì accanto.

Tieni presente che:

- **AI e giochi non vanno usati insieme**: condividono la stessa GPU e la stessa memoria;
- a motore spento, GPU e RAM tornano completamente disponibili per il gaming."""),

"en": ("## Models", """Models are **GGUF** files from the Hugging Face catalogue, and they come from two places: the **AI** section of the [Control Center](/en/docs/control-center), where you type the repository name (for example `unsloth/Qwen3-4B-GGUF`) and pick the variant from the list, sizes included; or the Hub inside Unsloth Studio, which has the search and the full model pages.

Rule of thumb on this board: the 16 GB of GDDR6 are shared between system and GPU, so staying under ~11 GB of weights leaves room for everything else.""",
       "## Switch, update and key", """The **AI** section of the [Control Center](/en/docs/control-center) starts and stops the engine, enables it at boot and shows the version with a one-click update. The same is in the [Remote Manager](/en/docs/controllo-remoto), from a browser.

Unsloth generates a random password when it installs, and **shuts itself down after an hour** if that password is not changed. The AI section does that step for you: choose the Studio password and the API key is created with it. The key is how the window and the Remote Manager talk to the engine; the models on disk, the memory (VRAM, GTT, RAM, swap) and a chat test with the measured tokens per second sit next to it.

Bear in mind:

- **AI and games should not run together**: they share the same GPU and the same memory;
- with the engine off, GPU and RAM are fully available for gaming again."""),

"es": ("## Los modelos", """Los modelos son archivos **GGUF** del catálogo de Hugging Face, y se descargan desde dos sitios: la sección **IA** del [Control Center](/es/docs/control-center), escribiendo el nombre del repositorio (por ejemplo `unsloth/Qwen3-4B-GGUF`) y eligiendo la variante de la lista, con los tamaños; o el Hub dentro de Unsloth Studio, que tiene la búsqueda y las fichas completas.

Regla práctica en esta placa: los 16 GB de GDDR6 se comparten entre sistema y GPU, así que conviene quedarse por debajo de unos 11 GB de pesos para dejar aire al resto.""",
       "## Encendido, actualización y clave", """La sección **IA** del [Control Center](/es/docs/control-center) enciende y apaga el motor, lo habilita al arrancar y muestra la versión con la actualización en un clic. Lo mismo está en el [Remote Manager](/es/docs/controllo-remoto), desde el navegador.

Unsloth genera una contraseña al azar al instalarse, y **se apaga solo al cabo de una hora** si no se cambia. Ese paso lo hace la sección IA: eliges la contraseña de Studio y la clave API se crea a la vez. La clave es como la ventana y el Remote Manager hablan con el motor; los modelos en disco, la memoria (VRAM, GTT, RAM, swap) y una prueba de chat con los tokens por segundo medidos están al lado.

Ten en cuenta que:

- **IA y juegos no se usan a la vez**: comparten la misma GPU y la misma memoria;
- con el motor apagado, GPU y RAM vuelven a estar del todo disponibles para jugar."""),

"pt": ("## Os modelos", """Os modelos são ficheiros **GGUF** do catálogo da Hugging Face, e chegam de dois sítios: a secção **IA** do [Control Center](/pt/docs/control-center), onde escreves o nome do repositório (por exemplo `unsloth/Qwen3-4B-GGUF`) e escolhes a variante da lista, com os tamanhos; ou o Hub dentro do Unsloth Studio, que tem a pesquisa e as fichas completas.

Regra prática nesta placa: os 16 GB de GDDR6 são partilhados entre sistema e GPU, por isso convém ficar abaixo dos ~11 GB de pesos para deixar espaço ao resto.""",
       "## Ligar, atualizar e a chave", """A secção **IA** do [Control Center](/pt/docs/control-center) liga e desliga o motor, ativa-o no arranque e mostra a versão com a atualização num clique. O mesmo está no [Remote Manager](/pt/docs/controllo-remoto), pelo navegador.

O Unsloth gera uma senha ao acaso quando se instala, e **desliga-se sozinho ao fim de uma hora** se essa senha não for mudada. Esse passo é feito pela secção IA: escolhes a senha do Studio e a chave API é criada com ela. A chave é como a janela e o Remote Manager falam com o motor; os modelos em disco, a memória (VRAM, GTT, RAM, swap) e um teste de chat com os tokens por segundo medidos ficam ao lado.

Tem em conta que:

- **IA e jogos não se usam juntos**: partilham a mesma GPU e a mesma memória;
- com o motor desligado, GPU e RAM voltam a estar totalmente disponíveis para jogar."""),

"de": ("## Die Modelle", """Die Modelle sind **GGUF**-Dateien aus dem Katalog von Hugging Face und kommen aus zwei Quellen: aus dem Bereich **KI** des [Control Center](/de/docs/control-center), wo du den Namen des Repositorys eingibst (zum Beispiel `unsloth/Qwen3-4B-GGUF`) und die Variante aus der Liste mit den Größen wählst; oder aus dem Hub in Unsloth Studio, der die Suche und die vollständigen Modellseiten hat.

Faustregel auf dieser Platine: die 16 GB GDDR6 teilen sich System und GPU, also bleibt man besser unter etwa 11 GB Gewichten, damit für den Rest Luft bleibt.""",
       "## Einschalten, aktualisieren, Schlüssel", """Der Bereich **KI** des [Control Center](/de/docs/control-center) startet und stoppt den Motor, schaltet ihn beim Systemstart ein und zeigt die Version mit der Aktualisierung in einem Klick. Dasselbe steht im [Remote Manager](/de/docs/controllo-remoto), im Browser.

Unsloth erzeugt bei der Installation ein zufälliges Passwort und **schaltet sich nach einer Stunde selbst ab**, wenn es nicht geändert wird. Diesen Schritt erledigt der KI-Bereich: du wählst das Studio-Passwort, und der API-Schlüssel entsteht dabei. Über den Schlüssel sprechen das Fenster und der Remote Manager mit dem Motor; die Modelle auf der Platte, der Speicher (VRAM, GTT, RAM, Swap) und ein Chat-Test mit den gemessenen Token pro Sekunde stehen daneben.

Denk daran:

- **KI und Spiele gehören nicht gleichzeitig benutzt**: sie teilen sich dieselbe GPU und denselben Speicher;
- mit ausgeschaltetem Motor stehen GPU und RAM wieder ganz zum Spielen bereit."""),

"fr": ("## Les modèles", """Les modèles sont des fichiers **GGUF** du catalogue Hugging Face, et ils arrivent de deux endroits : la section **IA** du [Control Center](/fr/docs/control-center), où tu écris le nom du dépôt (par exemple `unsloth/Qwen3-4B-GGUF`) et choisis la variante dans la liste, tailles comprises ; ou le Hub dans Unsloth Studio, qui a la recherche et les fiches complètes.

Règle pratique sur cette carte : les 16 Go de GDDR6 sont partagés entre le système et le GPU, donc mieux vaut rester sous ~11 Go de poids pour laisser de l'air au reste.""",
       "## Allumage, mise à jour et clé", """La section **IA** du [Control Center](/fr/docs/control-center) allume et éteint le moteur, l'active au démarrage et affiche la version avec la mise à jour en un clic. La même chose se trouve dans le [Remote Manager](/fr/docs/controllo-remoto), depuis le navigateur.

Unsloth génère un mot de passe au hasard à l'installation, et **s'éteint tout seul au bout d'une heure** s'il n'est pas changé. Cette étape, la section IA la fait : tu choisis le mot de passe de Studio et la clé API est créée en même temps. La clé est le moyen pour la fenêtre et le Remote Manager de parler au moteur ; les modèles sur le disque, la mémoire (VRAM, GTT, RAM, swap) et un essai de chat avec les tokens par seconde mesurés sont juste à côté.

Garde en tête que :

- **IA et jeux ne vont pas ensemble** : ils partagent le même GPU et la même mémoire ;
- moteur éteint, le GPU et la RAM redeviennent entièrement disponibles pour le jeu."""),

"pl": ("## Modele", """Modele to pliki **GGUF** z katalogu Hugging Face i pochodzą z dwóch miejsc: z sekcji **SI** [Control Center](/pl/docs/control-center), gdzie wpisujesz nazwę repozytorium (na przykład `unsloth/Qwen3-4B-GGUF`) i wybierasz wariant z listy, z rozmiarami; albo z Hubu w Unsloth Studio, który ma wyszukiwarkę i pełne karty modeli.

Praktyczna zasada na tej płycie: 16 GB GDDR6 dzieli system z GPU, więc lepiej zostać poniżej ~11 GB wag, żeby reszcie zostało miejsce.""",
       "## Włączanie, aktualizacja i klucz", """Sekcja **SI** w [Control Center](/pl/docs/control-center) włącza i wyłącza silnik, włącza go przy starcie i pokazuje wersję z aktualizacją jednym kliknięciem. To samo jest w [Remote Managerze](/pl/docs/controllo-remoto), z przeglądarki.

Unsloth przy instalacji tworzy losowe hasło i **wyłącza się sam po godzinie**, jeśli hasło nie zostanie zmienione. Ten krok wykonuje sekcja SI: wybierasz hasło do Studio, a klucz API powstaje razem z nim. Kluczem okno i Remote Manager rozmawiają z silnikiem; modele na dysku, pamięć (VRAM, GTT, RAM, swap) i próbny czat ze zmierzonymi tokenami na sekundę są obok.

Pamiętaj, że:

- **SI i gry nie chodzą razem**: dzielą to samo GPU i tę samą pamięć;
- przy wyłączonym silniku GPU i RAM wracają w całości do grania."""),

"ru": ("## Модели", """Модели это файлы **GGUF** из каталога Hugging Face, и берутся они из двух мест: из раздела **ИИ** в [Control Center](/ru/docs/control-center), где вы пишете имя репозитория (например `unsloth/Qwen3-4B-GGUF`) и выбираете вариант из списка с размерами; или из Hub внутри Unsloth Studio, где есть поиск и полные карточки моделей.

Практическое правило на этой плате: 16 ГБ GDDR6 делят система и GPU, поэтому лучше держаться ниже ~11 ГБ весов, чтобы остальному хватило места.""",
       "## Включение, обновление и ключ", """Раздел **ИИ** в [Control Center](/ru/docs/control-center) включает и выключает движок, включает его при запуске и показывает версию с обновлением в один клик. То же самое есть в [Remote Manager](/ru/docs/controllo-remoto), из браузера.

Unsloth создаёт случайный пароль при установке и **выключается сам через час**, если пароль не сменить. Этот шаг делает раздел ИИ: вы выбираете пароль Studio, и ключ API создаётся вместе с ним. Через ключ окно и Remote Manager общаются с движком; модели на диске, память (VRAM, GTT, RAM, swap) и проба чата с измеренными токенами в секунду находятся рядом.

Учтите:

- **ИИ и игры вместе не работают**: они делят один GPU и одну память;
- при выключенном движке GPU и RAM снова полностью свободны для игр."""),

"uk": ("## Моделі", """Моделі це файли **GGUF** з каталогу Hugging Face, і беруться вони з двох місць: із розділу **ШІ** в [Control Center](/uk/docs/control-center), де ви пишете назву репозиторію (наприклад `unsloth/Qwen3-4B-GGUF`) і вибираєте варіант зі списку з розмірами; або з Hub усередині Unsloth Studio, де є пошук і повні картки моделей.

Практичне правило на цій платі: 16 ГБ GDDR6 ділять система і GPU, тому краще лишатися нижче ~11 ГБ ваг, щоб решті вистачило місця.""",
       "## Увімкнення, оновлення і ключ", """Розділ **ШІ** в [Control Center](/uk/docs/control-center) вмикає і вимикає рушій, вмикає його при запуску і показує версію з оновленням в один клік. Те саме є в [Remote Manager](/uk/docs/controllo-remoto), із браузера.

Unsloth створює випадковий пароль під час встановлення і **вимикається сам через годину**, якщо пароль не змінити. Цей крок робить розділ ШІ: ви вибираєте пароль Studio, і ключ API створюється разом із ним. Через ключ вікно і Remote Manager спілкуються з рушієм; моделі на диску, пам'ять (VRAM, GTT, RAM, swap) і проба чату з виміряними токенами за секунду поруч.

Майте на увазі:

- **ШІ та ігри разом не працюють**: вони ділять той самий GPU і ту саму пам'ять;
- з вимкненим рушієм GPU і RAM знову цілком вільні для ігор."""),
}

IMG = {"it": "Sezione AI del Control Center: motore, modelli, memoria e una prova di chat",
       "en": "The AI section of the Control Center: engine, models, memory and a chat test",
       "es": "Sección IA del Control Center: motor, modelos, memoria y una prueba de chat",
       "pt": "Secção IA do Control Center: motor, modelos, memória e um teste de chat",
       "de": "Der KI-Bereich des Control Center: Motor, Modelle, Speicher und ein Chat-Test",
       "fr": "La section IA du Control Center : moteur, modèles, mémoire et un essai de chat",
       "pl": "Sekcja SI w Control Center: silnik, modele, pamięć i próbny czat",
       "ru": "Раздел ИИ в Control Center: движок, модели, память и проба чата",
       "uk": "Розділ ШІ в Control Center: рушій, моделі, пам'ять і проба чату"}

for lingua, (t_mod, c_mod, t_mot, c_mot) in T.items():
    p = os.path.join(DOCS, lingua, "ai-locale.md")
    with open(p, encoding="utf-8") as f:
        s = f.read()
    # the old screenshot showed the separate panel
    s = re.sub(r"!\[[^\]]*\]\(/img/ai-panel\.jpg\)",
               "![%s](/img/control-center-ai.png)" % IMG[lingua], s)
    # the sections, found by position: ... models, engine control, sources
    pezzi = re.split(r"\n(?=## )", s)
    if len(pezzi) < 4:
        raise SystemExit("%s: %d sezioni, me ne aspettavo almeno 4" % (p, len(pezzi)))
    pezzi[-3] = t_mod + "\n\n" + c_mod + "\n"
    pezzi[-2] = t_mot + "\n\n" + c_mot + "\n"
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(pezzi))
    print(lingua, "ok")

# The note about the migration away from Ollama: it was written for 26.06.3,
# in September 2026 nobody is migrating any more and it named an "AI panel"
# that no longer exists. Out, in every language.
import glob
tolte = 0
for p in sorted(glob.glob(os.path.join(DOCS, "*", "ai-locale.md"))):
    with open(p, encoding="utf-8") as f:
        s = f.read()
    nuovo = re.sub(r"\n> [^\n]*\n", "\n", s, count=1)
    if nuovo != s:
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(nuovo)
        tolte += 1
print("nota sulla migrazione tolta da %d pagine" % tolte)

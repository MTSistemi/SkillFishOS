#!/usr/bin/env python3
"""Adds the AI section to the generator of the Control Center documentation
page, in the nine languages, and the VRAM presets to the Tuner section.

    patch-docs-cc-ai.py <repo>

It edits apps/control-center/strumenti/docs-sito-control-center.py in place
(one language block at a time), then runs it.
"""
import os
import re
import subprocess
import sys

repo = sys.argv[1] if len(sys.argv) > 1 else "."
GEN = os.path.join(repo, "apps", "control-center", "strumenti", "docs-sito-control-center.py")

# per language: heading, body, the AI line of the section list, the sentence
# added to the VRAM bullet
AI = {
"it": ("## AI", """Il motore è **Unsloth Studio**: fa girare i modelli GGUF con llama.cpp sul backend **Vulkan**, che sulla gfx1013 della BC-250 è l'unica strada accelerata, perché ROCm non la supporta. Misurato sulla scheda con Qwen3-1.7B Q4_K_M: 210 token al secondo contro i 41 della sola CPU.

- **Motore**: acceso, spento, all'avvio. Acceso tiene la memoria della GPU, quindi si spegne prima di giocare. Accanto stanno la versione, il controllo degli aggiornamenti e *Aggiorna*, che rilancia l'installatore ufficiale con il pacchetto Vulkan di llama.cpp.
- **Accesso**: Unsloth genera una password a caso quando si installa, e si spegne da solo dopo un'ora se non viene cambiata. Il primo accesso si fa da qui: scegli la password di Studio e la chiave API viene creata insieme, e condivisa con il Remote Manager.
- **Modelli**: quelli sul disco con quantizzazione e dimensione. Per scaricarne uno serve il nome del repository su Hugging Face (per esempio `unsloth/Qwen3-4B-GGUF`) e la variante scelta dall'elenco, che riporta le dimensioni.
- **Chat**: una prova rapida sull'API compatibile OpenAI (`http://127.0.0.1:8888/v1`), con i token al secondo misurati. La chat completa, con i file e la ricerca, è dentro Studio.
- **Memoria**: VRAM, GTT, RAM, swap e il budget del modello. Il limite del GTT è un parametro del kernel: vale dal riavvio.
- **Rete**: aperto sulla rete locale, Studio risponde anche agli altri dispositivi di casa, con il suo utente e la sua password. Le chat in parallelo sono i posti di llama-server.""",
       "Unsloth Studio su Vulkan: motore, aggiornamento, modelli dall'Hub di Hugging Face, chat di prova, memoria e rete.",
       " Va da 512 MB a 12 GB, con i preset 512 MB, 1, 2, 4, 6 e 8 GB."),

"en": ("## AI", """The engine is **Unsloth Studio**: it runs GGUF models through llama.cpp on the **Vulkan** backend, which on the BC-250's gfx1013 is the only accelerated path, because ROCm does not support it. Measured on the board with Qwen3-1.7B Q4_K_M: 210 tokens per second against 41 on the CPU alone.

- **Engine**: on, off, at boot. On, it holds GPU memory, so turn it off before gaming. Beside it sit the version, the update check and *Update*, which reruns the official installer with the Vulkan bundle of llama.cpp.
- **Access**: Unsloth generates a random password when it installs, and shuts itself down after an hour if that password is not changed. The first sign-in happens here: choose the Studio password and the API key is created with it, and shared with the Remote Manager.
- **Models**: the ones on disk with quantization and size. To download one you need the repository name on Hugging Face (for example `unsloth/Qwen3-4B-GGUF`) and the variant picked from the list, sizes included.
- **Chat**: a quick run over the OpenAI-compatible API (`http://127.0.0.1:8888/v1`), with the measured tokens per second. The full chat, with files and search, is inside Studio.
- **Memory**: VRAM, GTT, RAM, swap and the model budget. The GTT limit is a kernel parameter: it takes effect at the next boot.
- **Network**: open on the local network, Studio answers the other devices at home too, with its own user and password. Parallel chats are llama-server's slots.""",
       "Unsloth Studio on Vulkan: engine, update, models from the Hugging Face Hub, a chat test, memory and network.",
       " Anything from 512 MB to 12 GB, with presets at 512 MB, 1, 2, 4, 6 and 8 GB."),

"de": ("## KI", """Der Motor ist **Unsloth Studio**: er führt GGUF-Modelle mit llama.cpp über das **Vulkan**-Backend aus, das auf der gfx1013 der BC-250 der einzige beschleunigte Weg ist, denn ROCm unterstützt sie nicht. Auf der Platine mit Qwen3-1.7B Q4_K_M gemessen: 210 Token pro Sekunde gegenüber 41 auf der CPU allein.

- **Motor**: an, aus, beim Systemstart. Eingeschaltet belegt er GPU-Speicher, vor dem Spielen also ausschalten. Daneben stehen die Version, die Aktualisierungsprüfung und *Aktualisieren*, das den offiziellen Installer mit dem Vulkan-Paket von llama.cpp erneut ausführt.
- **Zugang**: Unsloth erzeugt bei der Installation ein zufälliges Passwort und schaltet sich nach einer Stunde selbst ab, wenn es nicht geändert wird. Die erste Anmeldung geschieht hier: du wählst das Studio-Passwort, der API-Schlüssel entsteht dabei und wird mit dem Remote Manager geteilt.
- **Modelle**: die auf der Platte, mit Quantisierung und Größe. Zum Herunterladen brauchst du den Namen des Repositorys auf Hugging Face (zum Beispiel `unsloth/Qwen3-4B-GGUF`) und die Variante aus der Liste, Größen inklusive.
- **Chat**: ein schneller Lauf über die OpenAI-kompatible API (`http://127.0.0.1:8888/v1`), mit den gemessenen Token pro Sekunde. Der volle Chat, mit Dateien und Suche, steckt in Studio.
- **Speicher**: VRAM, GTT, RAM, Swap und das Budget des Modells. Die GTT-Grenze ist ein Kernel-Parameter: sie gilt ab dem nächsten Start.
- **Netz**: im lokalen Netz geöffnet antwortet Studio auch den anderen Geräten zu Hause, mit eigenem Benutzer und Passwort. Parallele Chats sind die Slots von llama-server.""",
       "Unsloth Studio über Vulkan: Motor, Aktualisierung, Modelle aus dem Hugging-Face-Hub, Chat-Test, Speicher und Netz.",
       " Von 512 MB bis 12 GB, mit den Vorgaben 512 MB, 1, 2, 4, 6 und 8 GB."),

"fr": ("## IA", """Le moteur est **Unsloth Studio** : il fait tourner les modèles GGUF avec llama.cpp sur le backend **Vulkan**, qui sur le gfx1013 de la BC-250 est la seule voie accélérée, car ROCm ne le prend pas en charge. Mesuré sur la carte avec Qwen3-1.7B Q4_K_M : 210 tokens par seconde contre 41 sur le seul CPU.

- **Moteur** : allumé, éteint, au démarrage. Allumé, il garde la mémoire du GPU : éteins-le avant de jouer. À côté se trouvent la version, la vérification des mises à jour et *Mettre à jour*, qui relance l'installateur officiel avec le paquet Vulkan de llama.cpp.
- **Accès** : Unsloth génère un mot de passe au hasard à l'installation, et s'éteint tout seul au bout d'une heure s'il n'est pas changé. La première connexion se fait ici : tu choisis le mot de passe de Studio, la clé API est créée en même temps et partagée avec le Remote Manager.
- **Modèles** : ceux qui sont sur le disque, avec quantification et taille. Pour en télécharger un, il faut le nom du dépôt sur Hugging Face (par exemple `unsloth/Qwen3-4B-GGUF`) et la variante choisie dans la liste, tailles comprises.
- **Chat** : un essai rapide sur l'API compatible OpenAI (`http://127.0.0.1:8888/v1`), avec les tokens par seconde mesurés. Le chat complet, avec les fichiers et la recherche, est dans Studio.
- **Mémoire** : VRAM, GTT, RAM, swap et le budget du modèle. La limite du GTT est un paramètre du noyau : elle s'applique au redémarrage.
- **Réseau** : ouvert sur le réseau local, Studio répond aussi aux autres appareils de la maison, avec son propre utilisateur et mot de passe. Les chats en parallèle sont les slots de llama-server.""",
       "Unsloth Studio sur Vulkan : moteur, mise à jour, modèles depuis le Hub Hugging Face, essai de chat, mémoire et réseau.",
       " De 512 Mo à 12 Go, avec les préréglages 512 Mo, 1, 2, 4, 6 et 8 Go."),

"es": ("## IA", """El motor es **Unsloth Studio**: ejecuta modelos GGUF con llama.cpp sobre el backend **Vulkan**, que en la gfx1013 de la BC-250 es el único camino acelerado, porque ROCm no la soporta. Medido en la placa con Qwen3-1.7B Q4_K_M: 210 tokens por segundo frente a 41 solo con la CPU.

- **Motor**: encendido, apagado, al arrancar. Encendido retiene memoria de la GPU, así que se apaga antes de jugar. Al lado están la versión, la comprobación de actualizaciones y *Actualizar*, que vuelve a ejecutar el instalador oficial con el paquete Vulkan de llama.cpp.
- **Acceso**: Unsloth genera una contraseña al azar al instalarse, y se apaga solo al cabo de una hora si no se cambia. El primer acceso se hace aquí: eliges la contraseña de Studio y la clave API se crea a la vez, y se comparte con el Remote Manager.
- **Modelos**: los que hay en disco, con cuantización y tamaño. Para descargar uno hace falta el nombre del repositorio en Hugging Face (por ejemplo `unsloth/Qwen3-4B-GGUF`) y la variante elegida de la lista, con los tamaños.
- **Chat**: una prueba rápida sobre la API compatible con OpenAI (`http://127.0.0.1:8888/v1`), con los tokens por segundo medidos. El chat completo, con archivos y búsqueda, está dentro de Studio.
- **Memoria**: VRAM, GTT, RAM, swap y el presupuesto del modelo. El límite del GTT es un parámetro del kernel: vale desde el siguiente arranque.
- **Red**: abierto en la red local, Studio responde también a los demás dispositivos de casa, con su propio usuario y contraseña. Los chats en paralelo son los slots de llama-server.""",
       "Unsloth Studio sobre Vulkan: motor, actualización, modelos del Hub de Hugging Face, prueba de chat, memoria y red.",
       " De 512 MB a 12 GB, con los preajustes 512 MB, 1, 2, 4, 6 y 8 GB."),

"pt": ("## IA", """O motor é o **Unsloth Studio**: corre modelos GGUF com o llama.cpp sobre o backend **Vulkan**, que na gfx1013 da BC-250 é o único caminho acelerado, porque o ROCm não a suporta. Medido na placa com Qwen3-1.7B Q4_K_M: 210 tokens por segundo contra 41 só com a CPU.

- **Motor**: ligado, desligado, no arranque. Ligado ocupa memória da GPU, por isso desliga-se antes de jogar. Ao lado estão a versão, a verificação de atualizações e *Atualizar*, que executa de novo o instalador oficial com o pacote Vulkan do llama.cpp.
- **Acesso**: o Unsloth gera uma senha ao acaso quando se instala, e desliga-se sozinho ao fim de uma hora se ela não for mudada. O primeiro acesso faz-se aqui: escolhes a senha do Studio e a chave API é criada com ela, e partilhada com o Remote Manager.
- **Modelos**: os que estão em disco, com quantização e tamanho. Para transferir um é preciso o nome do repositório na Hugging Face (por exemplo `unsloth/Qwen3-4B-GGUF`) e a variante escolhida da lista, com os tamanhos.
- **Chat**: um teste rápido sobre a API compatível com OpenAI (`http://127.0.0.1:8888/v1`), com os tokens por segundo medidos. O chat completo, com ficheiros e pesquisa, está dentro do Studio.
- **Memória**: VRAM, GTT, RAM, swap e o orçamento do modelo. O limite do GTT é um parâmetro do kernel: vale a partir do próximo arranque.
- **Rede**: aberto na rede local, o Studio responde também aos outros dispositivos de casa, com o seu próprio utilizador e senha. Os chats em paralelo são os slots do llama-server.""",
       "Unsloth Studio em Vulkan: motor, atualização, modelos do Hub da Hugging Face, teste de chat, memória e rede.",
       " Vai de 512 MB a 12 GB, com as predefinições 512 MB, 1, 2, 4, 6 e 8 GB."),

"pl": ("## AI", """Silnikiem jest **Unsloth Studio**: uruchamia modele GGUF przez llama.cpp na backendzie **Vulkan**, który na gfx1013 w BC-250 jest jedyną przyspieszaną drogą, bo ROCm jej nie obsługuje. Zmierzone na płycie z Qwen3-1.7B Q4_K_M: 210 tokenów na sekundę wobec 41 na samym CPU.

- **Silnik**: włączony, wyłączony, przy starcie. Włączony zajmuje pamięć GPU, więc wyłącza się go przed graniem. Obok są wersja, sprawdzanie aktualizacji i *Aktualizuj*, które ponownie uruchamia oficjalny instalator z pakietem Vulkan dla llama.cpp.
- **Dostęp**: Unsloth przy instalacji tworzy losowe hasło i wyłącza się sam po godzinie, jeśli hasło nie zostanie zmienione. Pierwsze logowanie odbywa się tutaj: wybierasz hasło do Studio, a klucz API powstaje razem z nim i trafia też do Remote Managera.
- **Modele**: te na dysku, z kwantyzacją i rozmiarem. Żeby pobrać model, potrzebna jest nazwa repozytorium na Hugging Face (na przykład `unsloth/Qwen3-4B-GGUF`) i wariant wybrany z listy, z rozmiarami.
- **Czat**: szybka próba na API zgodnym z OpenAI (`http://127.0.0.1:8888/v1`), ze zmierzonymi tokenami na sekundę. Pełny czat, z plikami i wyszukiwaniem, jest w Studio.
- **Pamięć**: VRAM, GTT, RAM, swap i budżet modelu. Limit GTT to parametr jądra: działa od następnego startu.
- **Sieć**: otwarty w sieci lokalnej Studio odpowiada też innym urządzeniom w domu, z własnym użytkownikiem i hasłem. Równoległe czaty to sloty llama-server.""",
       "Unsloth Studio na Vulkanie: silnik, aktualizacja, modele z Hubu Hugging Face, próbny czat, pamięć i sieć.",
       " Od 512 MB do 12 GB, z gotowymi wartościami 512 MB, 1, 2, 4, 6 i 8 GB."),

"ru": ("## ИИ", """Движок это **Unsloth Studio**: он запускает модели GGUF через llama.cpp на бэкенде **Vulkan**, который на gfx1013 в BC-250 единственный ускоренный путь, потому что ROCm её не поддерживает. Измерено на плате с Qwen3-1.7B Q4_K_M: 210 токенов в секунду против 41 на одном CPU.

- **Движок**: включён, выключен, при запуске. Включённый держит память GPU, поэтому перед играми его выключают. Рядом версия, проверка обновлений и *Обновить*, которая заново запускает официальный установщик с пакетом Vulkan для llama.cpp.
- **Доступ**: Unsloth создаёт случайный пароль при установке и выключается сам через час, если пароль не сменить. Первый вход делается здесь: вы выбираете пароль Studio, ключ API создаётся вместе с ним и передаётся Remote Manager.
- **Модели**: те, что на диске, с квантованием и размером. Чтобы скачать модель, нужно имя репозитория на Hugging Face (например `unsloth/Qwen3-4B-GGUF`) и вариант из списка, с размерами.
- **Чат**: быстрая проба на API, совместимом с OpenAI (`http://127.0.0.1:8888/v1`), с измеренными токенами в секунду. Полный чат, с файлами и поиском, внутри Studio.
- **Память**: VRAM, GTT, RAM, swap и бюджет модели. Предел GTT это параметр ядра: действует со следующей загрузки.
- **Сеть**: открытый в локальной сети, Studio отвечает и другим устройствам дома, со своим пользователем и паролем. Параллельные чаты это слоты llama-server.""",
       "Unsloth Studio на Vulkan: движок, обновление, модели из Hub Hugging Face, проба чата, память и сеть.",
       " От 512 МБ до 12 ГБ, с готовыми значениями 512 МБ, 1, 2, 4, 6 и 8 ГБ."),

"uk": ("## ШІ", """Рушій це **Unsloth Studio**: він запускає моделі GGUF через llama.cpp на бекенді **Vulkan**, який на gfx1013 у BC-250 є єдиним прискореним шляхом, бо ROCm її не підтримує. Виміряно на платі з Qwen3-1.7B Q4_K_M: 210 токенів за секунду проти 41 на самому CPU.

- **Рушій**: увімкнений, вимкнений, при запуску. Увімкнений тримає пам'ять GPU, тому перед іграми його вимикають. Поруч версія, перевірка оновлень і *Оновити*, яка знову запускає офіційний інсталятор із пакетом Vulkan для llama.cpp.
- **Доступ**: Unsloth створює випадковий пароль під час встановлення і вимикається сам через годину, якщо пароль не змінити. Перший вхід робиться тут: ви вибираєте пароль Studio, ключ API створюється разом із ним і передається Remote Manager.
- **Моделі**: ті, що на диску, з квантуванням і розміром. Щоб завантажити модель, потрібна назва репозиторію на Hugging Face (наприклад `unsloth/Qwen3-4B-GGUF`) і варіант зі списку, з розмірами.
- **Чат**: швидка проба на API, сумісному з OpenAI (`http://127.0.0.1:8888/v1`), із виміряними токенами за секунду. Повний чат, із файлами і пошуком, усередині Studio.
- **Пам'ять**: VRAM, GTT, RAM, swap і бюджет моделі. Межа GTT це параметр ядра: діє з наступного завантаження.
- **Мережа**: відкритий у локальній мережі, Studio відповідає й іншим пристроям удома, зі своїм користувачем і паролем. Паралельні чати це слоти llama-server.""",
       "Unsloth Studio на Vulkan: рушій, оновлення, моделі з Hub Hugging Face, проба чату, пам'ять і мережа.",
       " Від 512 МБ до 12 ГБ, із готовими значеннями 512 МБ, 1, 2, 4, 6 і 8 ГБ."),
}

with open(GEN, encoding="utf-8") as f:
    s = f.read()

# one language block at a time. Two shapes in this file: the first two
# languages live inside the T = { ... } literal, the other seven are
# assigned afterwards as T["de"] = dict(...).
INIZIO = r'(?:"[a-z]{2}": dict\(|T\["[a-z]{2}"\] = dict\()'
blocchi = re.split(r'(?m)^(?=%s)' % INIZIO, s)
fuori = []
for b in blocchi:
    m = re.match(r'(?:"([a-z]{2})": dict\(|T\["([a-z]{2})"\] = dict\()', b)
    lingua = (m.group(1) or m.group(2)) if m else None
    if not lingua or lingua not in AI or "\n    ai_t=" in b:
        fuori.append(b)
        continue
    titolo, corpo, voce, vram = AI[lingua]
    # the AI line of the section list
    nome = titolo[3:]
    b2, n = re.subn(r'\(\s*"%s",\s*"[^"]*"\)' % re.escape(nome), '("%s", "%s")' % (nome, voce), b, count=1)
    if not n:
        raise SystemExit("%s: voce AI non trovata nell'elenco" % lingua)
    # the VRAM bullet gains the presets
    b2, n = re.subn(r'(?m)^(- \*\*VRAM\*\*\s?:.*?)$', lambda mm: mm.group(1) + vram, b2, count=1)
    if not n:
        raise SystemExit("%s: riga VRAM non trovata" % lingua)
    # the section itself, before the closing one
    b2, n = re.subn(r'(?m)^(    fine_t=)', '    ai_t=%r,\n    ai="""%s""",\n\\1' % (titolo, corpo), b2, count=1)
    if not n:
        raise SystemExit("%s: fine_t non trovato" % lingua)
    fuori.append(b2)
s = "".join(fuori)
# and into the page, between Games and the closing section
s = s.replace('d["giochi_t"], d["giochi"], d["fine_t"], d["fine"]))',
              'd["giochi_t"], d["giochi"], d["ai_t"], d["ai"], d["fine_t"], d["fine"]))')
s = s.replace('%s\\n\\n%s\\n\\n%s\\n\\n%s\\n\\n%s\\n\\n%s\\n\\n%s\\n\\n%s\\n\\n%s\\n\\n%s\\n\\n%s\\n"',
              '%s\\n\\n%s\\n\\n%s\\n\\n%s\\n\\n%s\\n\\n%s\\n\\n%s\\n\\n%s\\n\\n%s\\n\\n%s\\n\\n%s\\n\\n%s\\n\\n%s\\n"')
with open(GEN, "w", encoding="utf-8", newline="\n") as f:
    f.write(s)
print("generatore aggiornato")

subprocess.run([sys.executable, GEN, repo], check=True)

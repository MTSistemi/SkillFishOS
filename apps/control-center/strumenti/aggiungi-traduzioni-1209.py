#!/usr/bin/env python3
"""The AI section rebuilt on 2026-09-12, plus a few strings the dictionaries
never had (tooltips of the knot buttons, short card titles): the seven
dictionaries, then the merge into the shared ones.

    aggiungi-traduzioni-1209.py <repo>
"""
import json
import os
import subprocess
import sys

repo = sys.argv[1]
d = os.path.join(repo, "apps", "control-center", "i18n")
L = ("de", "es", "fr", "pl", "pt", "ru", "uk")


def T(*tr):
    return dict(zip(L, tr))


NUOVE = {
    "A Studio key starts with sk-.": T(
        "Ein Studio-Schlüssel beginnt mit sk-.", "Una clave de Studio empieza por sk-.", "Une clé Studio commence par sk-.",
        "Klucz Studio zaczyna się od sk-.", "Uma chave do Studio começa por sk-.", "Ключ Studio начинается с sk-.", "Ключ Studio починається з sk-."),
    "A quick run over the API: the reply comes with the measured tokens per second. The full chat, with files and search, is inside Studio.": T(
        "Ein schneller Lauf über die API: die Antwort kommt mit den gemessenen Token pro Sekunde. Der volle Chat, mit Dateien und Suche, ist in Studio.",
        "Una prueba rápida por la API: la respuesta llega con los tokens por segundo medidos. El chat completo, con archivos y búsqueda, está dentro de Studio.",
        "Un essai rapide par l'API : la réponse arrive avec les tokens par seconde mesurés. Le chat complet, avec fichiers et recherche, est dans Studio.",
        "Szybka próba przez API: odpowiedź przychodzi ze zmierzonymi tokenami na sekundę. Pełny czat, z plikami i wyszukiwaniem, jest w Studio.",
        "Um teste rápido pela API: a resposta chega com os tokens por segundo medidos. O chat completo, com ficheiros e pesquisa, está dentro do Studio.",
        "Быстрая проба через API: ответ приходит с измеренными токенами в секунду. Полный чат, с файлами и поиском, внутри Studio.",
        "Швидка проба через API: відповідь приходить із виміряними токенами за секунду. Повний чат, із файлами й пошуком, усередині Studio."),
    "API key": T("API-Schlüssel", "Clave API", "Clé API", "Klucz API", "Chave API", "Ключ API", "Ключ API"),
    "Access": T("Zugang", "Acceso", "Accès", "Dostęp", "Acesso", "Доступ", "Доступ"),
    "Add a knot after the selected one": T(
        "Einen Knoten nach dem gewählten einfügen", "Añadir un punto después del seleccionado", "Ajouter un point après celui sélectionné",
        "Dodaj punkt za zaznaczonym", "Adicionar um ponto depois do selecionado", "Добавить точку после выбранной", "Додати точку після вибраної"),
    "Address": T("Adresse", "Dirección", "Adresse", "Adres", "Endereço", "Адрес", "Адреса"),
    "Applied; the engine was restarted if it was on.": T(
        "Angewendet; der Motor wurde neu gestartet, falls er lief.", "Aplicado; el motor se reinició si estaba encendido.", "Appliqué ; le moteur a redémarré s'il tournait.",
        "Zastosowano; silnik zrestartowano, jeśli był włączony.", "Aplicado; o motor reiniciou se estava ligado.", "Применено; движок перезапущен, если был включён.", "Застосовано; рушій перезапущено, якщо був увімкнений."),
    "At least 8 characters.": T("Mindestens 8 Zeichen.", "Al menos 8 caracteres.", "Au moins 8 caractères.", "Co najmniej 8 znaków.", "Pelo menos 8 caracteres.", "Не меньше 8 символов.", "Щонайменше 8 символів."),
    "Create the key": T("Schlüssel erzeugen", "Crear la clave", "Créer la clé", "Utwórz klucz", "Criar a chave", "Создать ключ", "Створити ключ"),
    "Download": T("Herunterladen", "Descargar", "Télécharger", "Pobierz", "Transferir", "Скачать", "Завантажити"),
    "Download a model first.": T("Lade zuerst ein Modell herunter.", "Descarga un modelo primero.", "Télécharge d'abord un modèle.", "Najpierw pobierz model.", "Transfere primeiro um modelo.", "Сначала скачайте модель.", "Спочатку завантажте модель."),
    "Download finished.": T("Download abgeschlossen.", "Descarga terminada.", "Téléchargement terminé.", "Pobieranie zakończone.", "Transferência concluída.", "Загрузка завершена.", "Завантаження завершено."),
    "Download started.": T("Download gestartet.", "Descarga iniciada.", "Téléchargement lancé.", "Pobieranie rozpoczęte.", "Transferência iniciada.", "Загрузка началась.", "Завантаження почалося."),
    "Downloading Unsloth Studio (Vulkan backend)…": T(
        "Lade Unsloth Studio herunter (Vulkan-Backend)…", "Descargando Unsloth Studio (backend Vulkan)…", "Téléchargement d'Unsloth Studio (backend Vulkan)…",
        "Pobieranie Unsloth Studio (backend Vulkan)…", "A transferir o Unsloth Studio (backend Vulkan)…", "Скачиваю Unsloth Studio (бэкенд Vulkan)…", "Завантажую Unsloth Studio (бекенд Vulkan)…"),
    "Engine": T("Motor", "Motor", "Moteur", "Silnik", "Motor", "Движок", "Рушій"),
    "First sign-in: choose the Studio password. The API key is created with it.": T(
        "Erste Anmeldung: wähle das Studio-Passwort. Der API-Schlüssel entsteht dabei.", "Primer acceso: elige la contraseña de Studio. La clave API se crea a la vez.",
        "Première connexion : choisis le mot de passe de Studio. La clé API est créée en même temps.", "Pierwsze logowanie: wybierz hasło do Studio. Klucz API powstaje razem z nim.",
        "Primeiro acesso: escolhe a senha do Studio. A chave API é criada com ela.", "Первый вход: выберите пароль Studio. Ключ API создаётся вместе с ним.",
        "Перший вхід: виберіть пароль Studio. Ключ API створюється разом із ним."),
    "Forget the key": T("Schlüssel vergessen", "Olvidar la clave", "Oublier la clé", "Zapomnij klucz", "Esquecer a chave", "Забыть ключ", "Забути ключ"),
    "Forget the key here and in the Remote Manager? It stays valid in Studio.": T(
        "Den Schlüssel hier und im Remote Manager vergessen? In Studio bleibt er gültig.", "¿Olvidar la clave aquí y en el Remote Manager? En Studio sigue valiendo.",
        "Oublier la clé ici et dans le Remote Manager ? Elle reste valable dans Studio.", "Zapomnieć klucz tutaj i w Remote Managerze? W Studio pozostaje ważny.",
        "Esquecer a chave aqui e no Remote Manager? No Studio continua válida.", "Забыть ключ здесь и в Remote Manager? В Studio он остаётся действительным.",
        "Забути ключ тут і в Remote Manager? У Studio він лишається чинним."),
    "GTT limit": T("GTT-Grenze", "Límite GTT", "Limite GTT", "Limit GTT", "Limite GTT", "Предел GTT", "Межа GTT"),
    "Give the repository as user/name.": T(
        "Gib das Repository als benutzer/name an.", "Indica el repositorio como usuario/nombre.", "Indique le dépôt sous la forme utilisateur/nom.",
        "Podaj repozytorium jako użytkownik/nazwa.", "Indica o repositório como utilizador/nome.", "Укажите репозиторий как пользователь/имя.", "Вкажіть репозиторій як користувач/назва."),
    "Key created and saved.": T("Schlüssel erzeugt und gespeichert.", "Clave creada y guardada.", "Clé créée et enregistrée.", "Klucz utworzony i zapisany.", "Chave criada e guardada.", "Ключ создан и сохранён.", "Ключ створено й збережено."),
    "Key saved.": T("Schlüssel gespeichert.", "Clave guardada.", "Clé enregistrée.", "Klucz zapisany.", "Chave guardada.", "Ключ сохранён.", "Ключ збережено."),
    "Look up": T("Suchen", "Buscar", "Chercher", "Szukaj", "Procurar", "Найти", "Знайти"),
    "Maximum": T("Maximum", "Máximo", "Maximum", "Maksimum", "Máximo", "Максимум", "Максимум"),
    "Models": T("Modelle", "Modelos", "Modèles", "Modele", "Modelos", "Модели", "Моделі"),
    "Needs the engine on and the key.": T(
        "Braucht den laufenden Motor und den Schlüssel.", "Hace falta el motor encendido y la clave.", "Il faut le moteur allumé et la clé.",
        "Potrzebny włączony silnik i klucz.", "Precisa do motor ligado e da chave.", "Нужны включённый движок и ключ.", "Потрібні увімкнений рушій і ключ."),
    "New": T("Neu", "Nueva", "Nouveau", "Nowy", "Nova", "Новый", "Новий"),
    "On the BC-250 VRAM and RAM are the same chip: the GTT is the share of RAM the model may use on top of VRAM. Kernel parameter: a reboot is needed.": T(
        "Auf der BC-250 sind VRAM und RAM derselbe Chip: das GTT ist der Anteil des RAM, den das Modell zusätzlich zum VRAM nutzen darf. Kernel-Parameter: ein Neustart ist nötig.",
        "En la BC-250 VRAM y RAM son el mismo chip: el GTT es la parte de RAM que el modelo puede usar además de la VRAM. Parámetro del kernel: hace falta reiniciar.",
        "Sur la BC-250 VRAM et RAM sont la même puce : le GTT est la part de RAM que le modèle peut utiliser en plus de la VRAM. Paramètre du noyau : un redémarrage est nécessaire.",
        "Na BC-250 VRAM i RAM to ten sam układ: GTT to część RAM, którą model może użyć poza VRAM. Parametr jądra: potrzebny restart.",
        "Na BC-250 VRAM e RAM são o mesmo chip: o GTT é a parte da RAM que o modelo pode usar além da VRAM. Parâmetro do kernel: é preciso reiniciar.",
        "На BC-250 VRAM и RAM один и тот же чип: GTT — доля RAM, которую модель может использовать сверх VRAM. Параметр ядра: нужна перезагрузка.",
        "На BC-250 VRAM і RAM це той самий чип: GTT — частка RAM, яку модель може використати понад VRAM. Параметр ядра: потрібне перезавантаження."),
    "On, it holds GPU memory: turn it off before gaming. Update reruns the official installer.": T(
        "Eingeschaltet belegt er GPU-Speicher: vor dem Spielen ausschalten. Aktualisieren führt den offiziellen Installer erneut aus.",
        "Encendido retiene memoria de la GPU: apágalo antes de jugar. Actualizar vuelve a ejecutar el instalador oficial.",
        "Allumé, il garde la mémoire GPU : éteins-le avant de jouer. Mettre à jour relance l'installateur officiel.",
        "Włączony zajmuje pamięć GPU: wyłącz go przed graniem. Aktualizacja uruchamia ponownie oficjalny instalator.",
        "Ligado ocupa memória da GPU: desliga-o antes de jogar. Atualizar executa de novo o instalador oficial.",
        "Включённый держит память GPU: выключите перед играми. Обновить запускает официальный установщик заново.",
        "Увімкнений тримає пам'ять GPU: вимкніть перед іграми. Оновити запускає офіційний інсталятор знову."),
    "Open Studio": T("Studio öffnen", "Abrir Studio", "Ouvrir Studio", "Otwórz Studio", "Abrir o Studio", "Открыть Studio", "Відкрити Studio"),
    "Open on the local network, Studio answers the other devices at home too, with its own user and password. Parallel chats are llama-server's slots.": T(
        "Im lokalen Netz geöffnet antwortet Studio auch den anderen Geräten zu Hause, mit eigenem Benutzer und Passwort. Parallele Chats sind die Slots von llama-server.",
        "Abierto en la red local, Studio responde también a los demás dispositivos de casa, con su propio usuario y contraseña. Los chats en paralelo son los slots de llama-server.",
        "Ouvert sur le réseau local, Studio répond aussi aux autres appareils de la maison, avec son propre utilisateur et mot de passe. Les chats en parallèle sont les slots de llama-server.",
        "Otwarty w sieci lokalnej Studio odpowiada też innym urządzeniom w domu, z własnym użytkownikiem i hasłem. Równoległe czaty to sloty llama-server.",
        "Aberto na rede local, o Studio responde também aos outros dispositivos de casa, com o seu próprio utilizador e senha. Os chats em paralelo são os slots do llama-server.",
        "Открытый в локальной сети, Studio отвечает и другим устройствам дома, со своим пользователем и паролем. Параллельные чаты — это слоты llama-server.",
        "Відкритий у локальній мережі, Studio відповідає й іншим пристроям удома, зі своїм користувачем і паролем. Паралельні чати — це слоти llama-server."),
    "Parallel chats": T("Parallele Chats", "Chats en paralelo", "Chats en parallèle", "Równoległe czaty", "Chats em paralelo", "Параллельные чаты", "Паралельні чати"),
    "Quantization": T("Quantisierung", "Cuantización", "Quantification", "Kwantyzacja", "Quantização", "Квантование", "Квантування"),
    "Reachable from the local network": T(
        "Im lokalen Netz erreichbar", "Accesible desde la red local", "Joignable depuis le réseau local", "Dostępny w sieci lokalnej",
        "Acessível na rede local", "Доступен из локальной сети", "Доступний з локальної мережі"),
    "Refresh the list": T("Liste aktualisieren", "Actualizar la lista", "Actualiser la liste", "Odśwież listę", "Atualizar a lista", "Обновить список", "Оновити список"),
    "Remove the selected knot": T("Den gewählten Knoten entfernen", "Quitar el punto seleccionado", "Retirer le point sélectionné", "Usuń zaznaczony punkt", "Remover o ponto selecionado", "Убрать выбранную точку", "Прибрати вибрану точку"),
    "Rerun the official Unsloth installer (a few GB, the engine restarts)?": T(
        "Den offiziellen Unsloth-Installer erneut ausführen (einige GB, der Motor startet neu)?", "¿Volver a ejecutar el instalador oficial de Unsloth (varios GB, el motor se reinicia)?",
        "Relancer l'installateur officiel d'Unsloth (quelques Go, le moteur redémarre) ?", "Uruchomić ponownie oficjalny instalator Unsloth (kilka GB, silnik się zrestartuje)?",
        "Executar de novo o instalador oficial do Unsloth (alguns GB, o motor reinicia)?", "Запустить официальный установщик Unsloth заново (несколько ГБ, движок перезапустится)?",
        "Запустити офіційний інсталятор Unsloth знову (кілька ГБ, рушій перезапуститься)?"),
    "Save": T("Speichern", "Guardar", "Enregistrer", "Zapisz", "Guardar", "Сохранить", "Зберегти"),
    "Scheduler": T("Scheduler", "Planificador", "Ordonnanceur", "Scheduler", "Escalonador", "Планировщик", "Планувальник"),
    "Send": T("Senden", "Enviar", "Envoyer", "Wyślij", "Enviar", "Отправить", "Надіслати"),
    "Set and create the key": T("Setzen und Schlüssel erzeugen", "Fijar y crear la clave", "Définir et créer la clé", "Ustaw i utwórz klucz", "Definir e criar a chave", "Задать и создать ключ", "Задати і створити ключ"),
    "Status": T("Status", "Estado", "État", "Stan", "Estado", "Состояние", "Стан"),
    "Studio did not accept the download": T(
        "Studio hat den Download nicht angenommen", "Studio no ha aceptado la descarga", "Studio n'a pas accepté le téléchargement",
        "Studio nie przyjęło pobierania", "O Studio não aceitou a transferência", "Studio не приняло загрузку", "Studio не прийняло завантаження"),
    "Studio did not issue the key": T(
        "Studio hat keinen Schlüssel ausgestellt", "Studio no ha emitido la clave", "Studio n'a pas délivré la clé",
        "Studio nie wydało klucza", "O Studio não emitiu a chave", "Studio не выдало ключ", "Studio не видало ключ"),
    "Studio has its own user. The API key is how this window and the Remote Manager talk to the engine.": T(
        "Studio hat einen eigenen Benutzer. Über den API-Schlüssel sprechen dieses Fenster und der Remote Manager mit dem Motor.",
        "Studio tiene su propio usuario. La clave API es como esta ventana y el Remote Manager hablan con el motor.",
        "Studio a son propre utilisateur. La clé API est le moyen pour cette fenêtre et le Remote Manager de parler au moteur.",
        "Studio ma własnego użytkownika. Klucz API to sposób, w jaki to okno i Remote Manager rozmawiają z silnikiem.",
        "O Studio tem o seu próprio utilizador. A chave API é como esta janela e o Remote Manager falam com o motor.",
        "У Studio свой пользователь. Через ключ API это окно и Remote Manager общаются с движком.",
        "У Studio свій користувач. Через ключ API це вікно і Remote Manager спілкуються з рушієм."),
    "Studio password": T("Studio-Passwort", "contraseña de Studio", "mot de passe Studio", "hasło Studio", "senha do Studio", "пароль Studio", "пароль Studio"),
    "Studio password not accepted": T(
        "Studio-Passwort nicht angenommen", "contraseña de Studio no aceptada", "mot de passe Studio refusé",
        "hasło Studio nie przyjęte", "senha do Studio não aceite", "пароль Studio не принят", "пароль Studio не прийнято"),
    "The GGUFs downloaded from the Hugging Face Hub. Up to about 11 GB of weights fit; past that the rest of the system suffers.": T(
        "Die vom Hugging-Face-Hub geladenen GGUFs. Bis etwa 11 GB Gewichte passen; darüber leidet der Rest des Systems.",
        "Los GGUF descargados del Hub de Hugging Face. Caben hasta unos 11 GB de pesos; más allá, el resto del sistema sufre.",
        "Les GGUF téléchargés depuis le Hub Hugging Face. Jusqu'à environ 11 Go de poids tiennent ; au-delà, le reste du système souffre.",
        "GGUF-y pobrane z Hubu Hugging Face. Mieści się do około 11 GB wag; powyżej cierpi reszta systemu.",
        "Os GGUF transferidos do Hub da Hugging Face. Cabem até cerca de 11 GB de pesos; além disso, o resto do sistema sofre.",
        "GGUF, скачанные с Hub Hugging Face. Помещается до примерно 11 ГБ весов; дальше страдает остальная система.",
        "GGUF, завантажені з Hub Hugging Face. Вміщається до приблизно 11 ГБ ваг; далі страждає решта системи."),
    "The reply appears here.": T("Die Antwort erscheint hier.", "La respuesta aparece aquí.", "La réponse apparaît ici.", "Odpowiedź pojawi się tutaj.", "A resposta aparece aqui.", "Ответ появится здесь.", "Відповідь з'явиться тут."),
    "The two passwords do not match.": T(
        "Die Passwörter stimmen nicht überein.", "Las dos contraseñas no coinciden.", "Les deux mots de passe ne correspondent pas.",
        "Hasła się różnią.", "As duas senhas não coincidem.", "Пароли не совпадают.", "Паролі не збігаються."),
    "Type and press Enter": T("Schreiben und Enter drücken", "Escribe y pulsa Intro", "Écris et appuie sur Entrée", "Wpisz i naciśnij Enter", "Escreve e carrega em Enter", "Введите и нажмите Enter", "Введіть і натисніть Enter"),
    "Unsloth Studio on the GPU, llama.cpp on Vulkan: models, chat and API stay on this machine.": T(
        "Unsloth Studio auf der GPU, llama.cpp über Vulkan: Modelle, Chat und API bleiben auf dieser Maschine.",
        "Unsloth Studio en la GPU, llama.cpp sobre Vulkan: modelos, chat y API se quedan en esta máquina.",
        "Unsloth Studio sur le GPU, llama.cpp sur Vulkan : modèles, chat et API restent sur cette machine.",
        "Unsloth Studio na GPU, llama.cpp na Vulkanie: modele, czat i API zostają na tej maszynie.",
        "Unsloth Studio na GPU, llama.cpp em Vulkan: modelos, chat e API ficam nesta máquina.",
        "Unsloth Studio на GPU, llama.cpp на Vulkan: модели, чат и API остаются на этой машине.",
        "Unsloth Studio на GPU, llama.cpp на Vulkan: моделі, чат і API лишаються на цій машині."),
    "User": T("Benutzer", "Usuario", "Utilisateur", "Użytkownik", "Utilizador", "Пользователь", "Користувач"),
    "after the first sign-in": T("nach der ersten Anmeldung", "tras el primer acceso", "après la première connexion", "po pierwszym logowaniu", "após o primeiro acesso", "после первого входа", "після першого входу"),
    "already downloaded": T("schon geladen", "ya descargado", "déjà téléchargé", "już pobrany", "já transferido", "уже скачан", "уже завантажено"),
    "available": T("verfügbar", "disponible", "disponible", "dostępna", "disponível", "доступна", "доступна"),
    "initial password not found": T("Anfangspasswort nicht gefunden", "contraseña inicial no encontrada", "mot de passe initial introuvable", "nie znaleziono hasła początkowego", "senha inicial não encontrada", "начальный пароль не найден", "початковий пароль не знайдено"),
    "loaded": T("geladen", "en memoria", "chargé", "w pamięci", "em memória", "в памяти", "у пам'яті"),
    "looking up…": T("suche…", "buscando…", "recherche…", "szukam…", "a procurar…", "ищу…", "шукаю…"),
    "needs the key": T("Schlüssel nötig", "hace falta la clave", "clé requise", "potrzebny klucz", "precisa da chave", "нужен ключ", "потрібен ключ"),
    "new password": T("neues Passwort", "nueva contraseña", "nouveau mot de passe", "nowe hasło", "nova senha", "новый пароль", "новий пароль"),
    "no GGUF found": T("kein GGUF gefunden", "ningún GGUF encontrado", "aucun GGUF trouvé", "nie znaleziono GGUF", "nenhum GGUF encontrado", "GGUF не найден", "GGUF не знайдено"),
    "no model downloaded": T("kein Modell geladen", "ningún modelo descargado", "aucun modèle téléchargé", "brak pobranych modeli", "nenhum modelo transferido", "модели не скачаны", "жодної моделі не завантажено"),
    "no reply": T("keine Antwort", "sin respuesta", "pas de réponse", "brak odpowiedzi", "sem resposta", "нет ответа", "немає відповіді"),
    "none": T("keiner", "ninguno", "aucun", "brak", "nenhum", "нет", "немає"),
    "or paste a key sk-unsloth-…": T("oder einen Schlüssel sk-unsloth-… einfügen", "o pega una clave sk-unsloth-…", "ou colle une clé sk-unsloth-…", "albo wklej klucz sk-unsloth-…", "ou cola uma chave sk-unsloth-…", "или вставьте ключ sk-unsloth-…", "або вставте ключ sk-unsloth-…"),
    "password change refused": T("Passwortänderung abgelehnt", "cambio de contraseña rechazado", "changement de mot de passe refusé", "zmiana hasła odrzucona", "mudança de senha recusada", "смена пароля отклонена", "зміну пароля відхилено"),
    "repeat": T("wiederholen", "repite", "répéter", "powtórz", "repete", "повторите", "повторіть"),
    "set": T("gesetzt", "configurada", "définie", "ustawiony", "definida", "задан", "задано"),
    "the initial password is no longer valid: sign in to Studio": T(
        "das Anfangspasswort gilt nicht mehr: melde dich in Studio an", "la contraseña inicial ya no vale: entra en Studio",
        "le mot de passe initial n'est plus valable : connecte-toi à Studio", "hasło początkowe już nie działa: zaloguj się do Studio",
        "a senha inicial já não é válida: entra no Studio", "начальный пароль больше не действует: войдите в Studio",
        "початковий пароль більше не дійсний: увійдіть у Studio"),
    "used": T("belegt", "usado", "utilisé", "użyte", "usado", "занято", "зайнято"),
}

for lang in L:
    p = os.path.join(d, lang + ".json")
    with open(p, encoding="utf-8") as f:
        j = json.load(f)
    n = 0
    for en, tr in NUOVE.items():
        if en not in j:
            j[en] = tr[lang]
            n += 1
    with open(p, "w", encoding="utf-8") as f:
        json.dump(j, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print(lang, "+%d" % n, "totale", len(j))

subprocess.run([sys.executable, os.path.join(repo, "apps", "control-center", "strumenti", "unisci-i18n.py"),
                os.path.join(repo, "apps", "control-center"),
                os.path.join(repo, "system", "usr", "share", "skillfish", "i18n")], check=True)

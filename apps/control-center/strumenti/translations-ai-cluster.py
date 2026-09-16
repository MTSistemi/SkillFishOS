#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Translations for the AI page strings that had none: AI mode levels, the
Studio password reset, model search and the BC-250 cluster card.

Runs ON the build VM, inside ~/sfx-src.

    python3 translations-ai-cluster.py

Terms are the ones already in the shared dictionaries, so the message and the
control it talks about use the same word: board (Karte, placa, carte, płyta,
плата), engine (Motor, Moteur, Silnik, Движок, Рушій), desktop, API key, sign
in. Placeholders are copied as they are: unisci-i18n.py refuses a mismatch.
"""
import io
import json
import os

ROOT = os.path.expanduser("~/sfx-src/apps/control-center/i18n")

THIS_ONE = "  (this one)"
STALE = "  ·  stale for %d s"
N_MODELS = "%d models"
AI_MODE = "AI mode"
AI_MODE_FAILED = "AI mode did not come on. Over ssh, `skillfish-ai-mode on` says why."
ADD_BOARD = "Add a board"
CHANGING = "Changing the password…"
CHOOSE_PW = ("Choose the new password for Unsloth Studio (user unsloth).\n\n"
             "The current one stops working right away and anyone using Studio is signed out.\n"
             "Leave empty to have a random one generated.")
CLUSTER = "Cluster"
COPY = "Copy"
DONE_PW = "Done. Sign in to Studio with user unsloth and the password you chose."
ENGINE_API = "Engine only, API only"
ENGINE_WEB = "Engine only, with web page"
FOUND = "Found"
LEVEL = "Level"
PW_UNREADABLE = "Password changed, but I could not read it from the command output:\n\n%s"
RESET_PW = "Reset the password"
SEARCH_MODELS = "Search models"
CLUSTER_HELP = ("Several BC-250 boards sharing a model too large for one. It is NOT faster: "
                "the network costs. It is for models that do not fit on a single board.")
SHUT_BUTTON = "Shut the desktop down for AI"
SHUT_ASK = ("Shut the desktop down?\n\n"
            "Everything you have open closes without saving, and about half a gigabyte goes to "
            "the model. The screen goes black.\n\n"
            "To come back: from the Remote Manager on another computer, or `skillfish-ai-mode off` over ssh.")
START_NODES = "Start the nodes"
STOP_NODES = "Stop the nodes"
STUDIO_ON = "Studio on (everything)"
NO_RPC = ("The board is in the list, but the RPC node is not there yet: it has to be installed "
          "on that machine in /opt/skillfish-rpc.")
NEW_PW = "The new password is:\n\n%s\n\nUser: unsloth"
OTHER_PW = "The password was changed, but NOT to the one you chose:\n\n%s\n\nUse the one below."
NOT_STORED = "We do not store it anywhere."
ADDRESS = "address, e.g. 192.168.1.40"
CHECKING = "checking..."
COULD_NOT = "could not do it"
DESKTOP_RUNNING = "desktop running"
FREE_OF = "free of %.1f GB · %d boards · %d W%s"
NO_BOARD = "no board"
NO_LONGER_VALID = "no longer valid"
NO_MODEL = "no model found"
STARTED_ON = "nodes started on %d boards"
STOPPED_ON = "nodes stopped on %d boards"
PW_ONCE = "password (needed once)"
REPEAT = "repeat it"
SEARCH_HF = "search Hugging Face: qwen, llama, gemma, coder..."
SEARCHING = "searching..."
KEY_MISSING = "the API key is missing: sign in above"
KEY_INVALID = "the API key is no longer valid: sign in again"
PW_MISMATCH = "the two passwords do not match"
TYPE_SOMETHING = "type something to look for"
USER = "user"

ENTRIES = {
    "de": {
        THIS_ONE: "  (diese)",
        STALE: "  ·  seit %d s nicht aktualisiert",
        N_MODELS: "%d Modelle",
        AI_MODE: "KI-Modus",
        AI_MODE_FAILED: "Der KI-Modus ist nicht angegangen. Per ssh sagt `skillfish-ai-mode on`, warum.",
        ADD_BOARD: "Karte hinzufügen",
        CHANGING: "Passwort wird geändert…",
        CHOOSE_PW: "Wähle das neue Passwort für Unsloth Studio (Benutzer unsloth).\n\n"
                   "Das jetzige gilt sofort nicht mehr, und wer Studio gerade benutzt, wird abgemeldet.\n"
                   "Leer lassen, um ein zufälliges erzeugen zu lassen.",
        CLUSTER: "Cluster",
        DONE_PW: "Fertig. Melde dich in Studio mit dem Benutzer unsloth und dem gewählten Passwort an.",
        ENGINE_API: "Nur der Motor, nur API",
        ENGINE_WEB: "Nur der Motor, mit Webseite",
        FOUND: "Gefunden",
        LEVEL: "Stufe",
        PW_UNREADABLE: "Passwort geändert, aber ich konnte es nicht aus der Ausgabe des Befehls lesen:\n\n%s",
        RESET_PW: "Passwort zurücksetzen",
        SEARCH_MODELS: "Modelle suchen",
        CLUSTER_HELP: "Mehrere BC-250-Karten teilen sich ein Modell, das für eine allein zu groß ist. Es ist NICHT "
                      "schneller: das Netzwerk kostet. Es ist für Modelle, die nicht auf eine Karte passen.",
        SHUT_BUTTON: "Desktop für die KI beenden",
        SHUT_ASK: "Desktop beenden?\n\n"
                  "Alles, was du offen hast, wird ohne Speichern geschlossen, und etwa ein halbes Gigabyte geht "
                  "an das Modell. Der Bildschirm wird schwarz.\n\n"
                  "Zurück geht es über den Remote Manager auf einem anderen Computer oder mit "
                  "`skillfish-ai-mode off` per ssh.",
        START_NODES: "Knoten starten",
        STOP_NODES: "Knoten stoppen",
        STUDIO_ON: "Studio an (alles)",
        NO_RPC: "Die Karte steht in der Liste, aber der RPC-Knoten fehlt noch: er muss auf dieser Maschine "
                "in /opt/skillfish-rpc installiert werden.",
        NEW_PW: "Das neue Passwort lautet:\n\n%s\n\nBenutzer: unsloth",
        OTHER_PW: "Das Passwort wurde geändert, aber NICHT in das gewählte:\n\n%s\n\nNimm das hier unten.",
        NOT_STORED: "Wir speichern es nirgends.",
        ADDRESS: "Adresse, z. B. 192.168.1.40",
        CHECKING: "wird geprüft...",
        COULD_NOT: "hat nicht geklappt",
        DESKTOP_RUNNING: "Desktop läuft",
        FREE_OF: "frei von %.1f GB · %d Karten · %d W%s",
        NO_BOARD: "keine Karte",
        NO_LONGER_VALID: "gilt nicht mehr",
        NO_MODEL: "kein Modell gefunden",
        STARTED_ON: "Knoten auf %d Karten gestartet",
        STOPPED_ON: "Knoten auf %d Karten gestoppt",
        PW_ONCE: "Passwort (nur einmal nötig)",
        REPEAT: "wiederholen",
        SEARCH_HF: "auf Hugging Face suchen: qwen, llama, gemma, coder...",
        SEARCHING: "wird gesucht...",
        KEY_MISSING: "der API-Schlüssel fehlt: melde dich oben an",
        KEY_INVALID: "der API-Schlüssel gilt nicht mehr: melde dich erneut an",
        PW_MISMATCH: "die beiden Passwörter stimmen nicht überein",
        TYPE_SOMETHING: "gib etwas zum Suchen ein",
        USER: "Benutzer",
    },
    "es": {
        THIS_ONE: "  (esta)",
        STALE: "  ·  sin actualizar desde hace %d s",
        N_MODELS: "%d modelos",
        AI_MODE: "Modo IA",
        AI_MODE_FAILED: "El modo IA no se ha activado. Por ssh, `skillfish-ai-mode on` dice por qué.",
        ADD_BOARD: "Añadir una placa",
        CHANGING: "Cambiando la contraseña…",
        CHOOSE_PW: "Elige la nueva contraseña de Unsloth Studio (usuario unsloth).\n\n"
                   "La actual deja de funcionar enseguida y quien esté usando Studio se desconecta.\n"
                   "Déjala vacía para que se genere una al azar.",
        CLUSTER: "Clúster",
        DONE_PW: "Hecho. Entra en Studio con el usuario unsloth y la contraseña que has elegido.",
        ENGINE_API: "Solo el motor, solo API",
        ENGINE_WEB: "Solo el motor, con página web",
        FOUND: "Encontrados",
        LEVEL: "Nivel",
        PW_UNREADABLE: "Contraseña cambiada, pero no he podido leerla en la salida del comando:\n\n%s",
        RESET_PW: "Restablecer la contraseña",
        SEARCH_MODELS: "Buscar modelos",
        CLUSTER_HELP: "Varias placas BC-250 que se reparten un modelo demasiado grande para una sola. NO va más "
                      "rápido: la red cuesta. Sirve para los modelos que no caben en una placa.",
        SHUT_BUTTON: "Apagar el escritorio para la IA",
        SHUT_ASK: "¿Apagar el escritorio?\n\n"
                  "Se cierra todo lo que tienes abierto, sin guardar, y queda medio giga más para el modelo. "
                  "La pantalla se pone negra.\n\n"
                  "Para volver: desde el Remote Manager en otro ordenador, o `skillfish-ai-mode off` por ssh.",
        START_NODES: "Encender los nodos",
        STOP_NODES: "Apagar los nodos",
        STUDIO_ON: "Studio encendido (todo)",
        NO_RPC: "La placa está en la lista, pero el nodo RPC todavía no: hay que instalarlo en esa máquina "
                "en /opt/skillfish-rpc.",
        NEW_PW: "La nueva contraseña es:\n\n%s\n\nUsuario: unsloth",
        OTHER_PW: "La contraseña se ha cambiado, pero NO por la que has elegido:\n\n%s\n\nUsa la de abajo.",
        NOT_STORED: "No la guardamos en ningún sitio.",
        ADDRESS: "dirección, p. ej. 192.168.1.40",
        CHECKING: "comprobando...",
        COULD_NOT: "no lo he conseguido",
        DESKTOP_RUNNING: "escritorio en marcha",
        FREE_OF: "libres de %.1f GB · %d placas · %d W%s",
        NO_BOARD: "ninguna placa",
        NO_LONGER_VALID: "ya no vale",
        NO_MODEL: "ningún modelo encontrado",
        STARTED_ON: "nodos encendidos en %d placas",
        STOPPED_ON: "nodos apagados en %d placas",
        PW_ONCE: "contraseña (hace falta una sola vez)",
        REPEAT: "repítela",
        SEARCH_HF: "buscar en Hugging Face: qwen, llama, gemma, coder...",
        SEARCHING: "buscando...",
        KEY_MISSING: "falta la clave API: entra aquí arriba",
        KEY_INVALID: "la clave API ya no vale: vuelve a entrar",
        PW_MISMATCH: "las dos contraseñas no coinciden",
        TYPE_SOMETHING: "escribe algo que buscar",
        USER: "usuario",
    },
    "fr": {
        THIS_ONE: "  (celle-ci)",
        STALE: "  ·  pas mis à jour depuis %d s",
        N_MODELS: "%d modèles",
        AI_MODE: "Mode IA",
        AI_MODE_FAILED: "Le mode IA ne s'est pas activé. Par ssh, `skillfish-ai-mode on` dit pourquoi.",
        ADD_BOARD: "Ajouter une carte",
        CHANGING: "Changement du mot de passe…",
        CHOOSE_PW: "Choisis le nouveau mot de passe d'Unsloth Studio (utilisateur unsloth).\n\n"
                   "L'actuel cesse de fonctionner tout de suite et quiconque utilise Studio est déconnecté.\n"
                   "Laisse vide pour en faire générer un au hasard.",
        CLUSTER: "Cluster",
        DONE_PW: "C'est fait. Connecte-toi à Studio avec l'utilisateur unsloth et le mot de passe choisi.",
        ENGINE_API: "Moteur seul, API seule",
        ENGINE_WEB: "Moteur seul, avec page web",
        FOUND: "Trouvés",
        LEVEL: "Niveau",
        PW_UNREADABLE: "Mot de passe changé, mais je n'ai pas pu le lire dans la sortie de la commande :\n\n%s",
        RESET_PW: "Réinitialiser le mot de passe",
        SEARCH_MODELS: "Rechercher des modèles",
        CLUSTER_HELP: "Plusieurs cartes BC-250 qui se partagent un modèle trop gros pour une seule. Ce n'est PAS "
                      "plus rapide : le réseau coûte. C'est pour les modèles qui ne tiennent pas sur une carte.",
        SHUT_BUTTON: "Arrêter le bureau pour l'IA",
        SHUT_ASK: "Arrêter le bureau ?\n\n"
                  "Tout ce que tu as ouvert se ferme sans enregistrer, et environ un demi-gigaoctet va au modèle. "
                  "L'écran devient noir.\n\n"
                  "Pour revenir : depuis le Remote Manager sur un autre ordinateur, ou `skillfish-ai-mode off` par ssh.",
        START_NODES: "Démarrer les nœuds",
        STOP_NODES: "Arrêter les nœuds",
        STUDIO_ON: "Studio allumé (tout)",
        NO_RPC: "La carte est dans la liste, mais le nœud RPC n'y est pas encore : il faut l'installer sur "
                "cette machine dans /opt/skillfish-rpc.",
        NEW_PW: "Le nouveau mot de passe est :\n\n%s\n\nUtilisateur : unsloth",
        OTHER_PW: "Le mot de passe a été changé, mais PAS pour celui que tu as choisi :\n\n%s\n\n"
                  "Utilise celui ci-dessous.",
        NOT_STORED: "Nous ne l'enregistrons nulle part.",
        ADDRESS: "adresse, p. ex. 192.168.1.40",
        CHECKING: "vérification...",
        COULD_NOT: "je n'y suis pas arrivé",
        DESKTOP_RUNNING: "bureau allumé",
        FREE_OF: "libres sur %.1f GB · %d cartes · %d W%s",
        NO_BOARD: "aucune carte",
        NO_LONGER_VALID: "n'est plus valable",
        NO_MODEL: "aucun modèle trouvé",
        STARTED_ON: "nœuds démarrés sur %d cartes",
        STOPPED_ON: "nœuds arrêtés sur %d cartes",
        PW_ONCE: "mot de passe (une seule fois)",
        REPEAT: "répète-le",
        SEARCH_HF: "chercher sur Hugging Face : qwen, llama, gemma, coder...",
        SEARCHING: "recherche...",
        KEY_MISSING: "la clé API manque : connecte-toi ci-dessus",
        KEY_INVALID: "la clé API n'est plus valable : reconnecte-toi",
        PW_MISMATCH: "les deux mots de passe ne correspondent pas",
        TYPE_SOMETHING: "écris quelque chose à chercher",
        USER: "utilisateur",
    },
    "pl": {
        THIS_ONE: "  (ta)",
        STALE: "  ·  nieaktualne od %d s",
        N_MODELS: "liczba modeli: %d",
        AI_MODE: "Tryb AI",
        AI_MODE_FAILED: "Tryb AI się nie włączył. Przez ssh `skillfish-ai-mode on` powie dlaczego.",
        ADD_BOARD: "Dodaj płytę",
        CHANGING: "Zmieniam hasło…",
        CHOOSE_PW: "Wybierz nowe hasło do Unsloth Studio (użytkownik unsloth).\n\n"
                   "Obecne od razu przestaje działać, a kto używa Studio, zostaje wylogowany.\n"
                   "Zostaw puste, żeby wygenerować losowe.",
        CLUSTER: "Klaster",
        COPY: "Kopiuj",
        DONE_PW: "Gotowe. Zaloguj się do Studio jako użytkownik unsloth z wybranym hasłem.",
        ENGINE_API: "Tylko silnik, tylko API",
        ENGINE_WEB: "Tylko silnik, ze stroną WWW",
        FOUND: "Znalezione",
        LEVEL: "Poziom",
        PW_UNREADABLE: "Hasło zmienione, ale nie udało mi się go odczytać z wyjścia polecenia:\n\n%s",
        RESET_PW: "Zresetuj hasło",
        SEARCH_MODELS: "Szukaj modeli",
        CLUSTER_HELP: "Kilka płyt BC-250 dzieli model za duży na jedną. To NIE jest szybsze: sieć kosztuje. "
                      "Służy do modeli, które nie mieszczą się na jednej płycie.",
        SHUT_BUTTON: "Wyłącz pulpit dla AI",
        SHUT_ASK: "Wyłączyć pulpit?\n\n"
                  "Wszystko, co masz otwarte, zamknie się bez zapisywania, a około pół gigabajta trafi do modelu. "
                  "Ekran zrobi się czarny.\n\n"
                  "Powrót: z Remote Managera na innym komputerze albo `skillfish-ai-mode off` przez ssh.",
        START_NODES: "Uruchom węzły",
        STOP_NODES: "Zatrzymaj węzły",
        STUDIO_ON: "Studio włączone (wszystko)",
        NO_RPC: "Płyta jest na liście, ale węzła RPC jeszcze nie ma: trzeba go zainstalować na tej maszynie "
                "w /opt/skillfish-rpc.",
        NEW_PW: "Nowe hasło to:\n\n%s\n\nUżytkownik: unsloth",
        OTHER_PW: "Hasło zostało zmienione, ale NIE na wybrane przez ciebie:\n\n%s\n\nUżyj tego poniżej.",
        NOT_STORED: "Nigdzie go nie zapisujemy.",
        ADDRESS: "adres, np. 192.168.1.40",
        CHECKING: "sprawdzam...",
        COULD_NOT: "nie udało się",
        DESKTOP_RUNNING: "pulpit działa",
        FREE_OF: "wolne z %.1f GB · płyt: %d · %d W%s",
        NO_BOARD: "brak płyt",
        NO_LONGER_VALID: "już nie działa",
        NO_MODEL: "nie znaleziono modelu",
        STARTED_ON: "węzły uruchomione na %d płytach",
        STOPPED_ON: "węzły zatrzymane na %d płytach",
        PW_ONCE: "hasło (potrzebne tylko raz)",
        REPEAT: "powtórz je",
        SEARCH_HF: "szukaj na Hugging Face: qwen, llama, gemma, coder...",
        SEARCHING: "szukam...",
        KEY_MISSING: "brak klucza API: zaloguj się powyżej",
        KEY_INVALID: "klucz API już nie działa: zaloguj się ponownie",
        PW_MISMATCH: "hasła nie są takie same",
        TYPE_SOMETHING: "wpisz coś do wyszukania",
        USER: "użytkownik",
    },
    "pt": {
        THIS_ONE: "  (esta)",
        STALE: "  ·  sem atualizar há %d s",
        N_MODELS: "%d modelos",
        AI_MODE: "Modo IA",
        AI_MODE_FAILED: "O modo IA não se ativou. Por ssh, `skillfish-ai-mode on` diz porquê.",
        ADD_BOARD: "Adicionar uma placa",
        CHANGING: "A mudar a senha…",
        CHOOSE_PW: "Escolhe a nova senha do Unsloth Studio (utilizador unsloth).\n\n"
                   "A atual deixa de funcionar logo e quem estiver a usar o Studio é desligado.\n"
                   "Deixa vazio para gerar uma ao acaso.",
        CLUSTER: "Cluster",
        DONE_PW: "Feito. Entra no Studio com o utilizador unsloth e a senha que escolheste.",
        ENGINE_API: "Só o motor, só API",
        ENGINE_WEB: "Só o motor, com página web",
        FOUND: "Encontrados",
        LEVEL: "Nível",
        PW_UNREADABLE: "Senha mudada, mas não consegui lê-la na saída do comando:\n\n%s",
        RESET_PW: "Repor a senha",
        SEARCH_MODELS: "Procurar modelos",
        CLUSTER_HELP: "Várias placas BC-250 a dividir um modelo grande demais para uma só. NÃO é mais rápido: "
                      "a rede custa. Serve para os modelos que não cabem numa placa.",
        SHUT_BUTTON: "Desligar o ambiente de trabalho para a IA",
        SHUT_ASK: "Desligar o ambiente de trabalho?\n\n"
                  "Fecha-se tudo o que tens aberto, sem guardar, e cerca de meio giga vai para o modelo. "
                  "O ecrã fica preto.\n\n"
                  "Para voltar: a partir do Remote Manager noutro computador, ou `skillfish-ai-mode off` por ssh.",
        START_NODES: "Ligar os nós",
        STOP_NODES: "Desligar os nós",
        STUDIO_ON: "Studio ligado (tudo)",
        NO_RPC: "A placa está na lista, mas o nó RPC ainda não está lá: tem de ser instalado nessa máquina "
                "em /opt/skillfish-rpc.",
        NEW_PW: "A nova senha é:\n\n%s\n\nUtilizador: unsloth",
        OTHER_PW: "A senha foi mudada, mas NÃO para a que escolheste:\n\n%s\n\nUsa a de baixo.",
        NOT_STORED: "Não a guardamos em lado nenhum.",
        ADDRESS: "endereço, p. ex. 192.168.1.40",
        CHECKING: "a verificar...",
        COULD_NOT: "não consegui",
        DESKTOP_RUNNING: "ambiente de trabalho ligado",
        FREE_OF: "livres de %.1f GB · %d placas · %d W%s",
        NO_BOARD: "nenhuma placa",
        NO_LONGER_VALID: "já não é válida",
        NO_MODEL: "nenhum modelo encontrado",
        STARTED_ON: "nós ligados em %d placas",
        STOPPED_ON: "nós desligados em %d placas",
        PW_ONCE: "senha (só é precisa uma vez)",
        REPEAT: "repete-a",
        SEARCH_HF: "procurar no Hugging Face: qwen, llama, gemma, coder...",
        SEARCHING: "a procurar...",
        KEY_MISSING: "falta a chave API: entra aqui em cima",
        KEY_INVALID: "a chave API já não é válida: entra outra vez",
        PW_MISMATCH: "as duas senhas não coincidem",
        TYPE_SOMETHING: "escreve algo para procurar",
        USER: "utilizador",
    },
    "ru": {
        THIS_ONE: "  (эта)",
        STALE: "  ·  не обновлялись %d с",
        N_MODELS: "моделей: %d",
        AI_MODE: "Режим ИИ",
        AI_MODE_FAILED: "Режим ИИ не включился. По ssh команда `skillfish-ai-mode on` скажет почему.",
        ADD_BOARD: "Добавить плату",
        CHANGING: "Меняем пароль…",
        CHOOSE_PW: "Выберите новый пароль для Unsloth Studio (пользователь unsloth).\n\n"
                   "Текущий сразу перестаёт работать, и все, кто сейчас в Studio, будут отключены.\n"
                   "Оставьте пустым, чтобы сгенерировать случайный.",
        CLUSTER: "Кластер",
        DONE_PW: "Готово. Войдите в Studio как пользователь unsloth с выбранным паролем.",
        ENGINE_API: "Только движок, только API",
        ENGINE_WEB: "Только движок, с веб-страницей",
        FOUND: "Найдено",
        LEVEL: "Уровень",
        PW_UNREADABLE: "Пароль изменён, но прочитать его из вывода команды не удалось:\n\n%s",
        RESET_PW: "Сбросить пароль",
        SEARCH_MODELS: "Искать модели",
        CLUSTER_HELP: "Несколько плат BC-250 делят модель, слишком большую для одной. Это НЕ быстрее: сеть "
                      "стоит своё. Это для моделей, которые не помещаются на одну плату.",
        SHUT_BUTTON: "Выключить рабочий стол ради ИИ",
        SHUT_ASK: "Выключить рабочий стол?\n\n"
                  "Всё открытое закроется без сохранения, и около полугигабайта уйдёт модели. "
                  "Экран станет чёрным.\n\n"
                  "Чтобы вернуться: из Remote Manager на другом компьютере или `skillfish-ai-mode off` по ssh.",
        START_NODES: "Запустить узлы",
        STOP_NODES: "Остановить узлы",
        STUDIO_ON: "Studio включено (всё)",
        NO_RPC: "Плата есть в списке, но узла RPC на ней ещё нет: его нужно установить на той машине "
                "в /opt/skillfish-rpc.",
        NEW_PW: "Новый пароль:\n\n%s\n\nПользователь: unsloth",
        OTHER_PW: "Пароль изменён, но НЕ на выбранный вами:\n\n%s\n\nИспользуйте тот, что ниже.",
        NOT_STORED: "Мы его нигде не сохраняем.",
        ADDRESS: "адрес, напр. 192.168.1.40",
        CHECKING: "проверяем...",
        COULD_NOT: "не получилось",
        DESKTOP_RUNNING: "рабочий стол работает",
        FREE_OF: "свободно из %.1f GB · плат: %d · %d W%s",
        NO_BOARD: "нет плат",
        NO_LONGER_VALID: "больше не действует",
        NO_MODEL: "модель не найдена",
        STARTED_ON: "узлы запущены на платах: %d",
        STOPPED_ON: "узлы остановлены на платах: %d",
        PW_ONCE: "пароль (нужен один раз)",
        REPEAT: "повторите",
        SEARCH_HF: "искать на Hugging Face: qwen, llama, gemma, coder...",
        SEARCHING: "ищем...",
        KEY_MISSING: "нет ключа API: войдите выше",
        KEY_INVALID: "ключ API больше не действует: войдите снова",
        PW_MISMATCH: "пароли не совпадают",
        TYPE_SOMETHING: "введите, что искать",
        USER: "пользователь",
    },
    "uk": {
        THIS_ONE: "  (ця)",
        STALE: "  ·  не оновлювалися %d с",
        N_MODELS: "моделей: %d",
        AI_MODE: "Режим ШІ",
        AI_MODE_FAILED: "Режим ШІ не ввімкнувся. Через ssh команда `skillfish-ai-mode on` скаже чому.",
        ADD_BOARD: "Додати плату",
        CHANGING: "Змінюємо пароль…",
        CHOOSE_PW: "Виберіть новий пароль для Unsloth Studio (користувач unsloth).\n\n"
                   "Поточний одразу перестає працювати, і всіх, хто зараз у Studio, буде від'єднано.\n"
                   "Залиште порожнім, щоб згенерувати випадковий.",
        CLUSTER: "Кластер",
        COPY: "Копіювати",
        DONE_PW: "Готово. Увійдіть у Studio як користувач unsloth з вибраним паролем.",
        ENGINE_API: "Лише рушій, лише API",
        ENGINE_WEB: "Лише рушій, з вебсторінкою",
        FOUND: "Знайдено",
        LEVEL: "Рівень",
        PW_UNREADABLE: "Пароль змінено, але прочитати його з виводу команди не вдалося:\n\n%s",
        RESET_PW: "Скинути пароль",
        SEARCH_MODELS: "Шукати моделі",
        CLUSTER_HELP: "Кілька плат BC-250 ділять модель, завелику для однієї. Це НЕ швидше: мережа коштує. "
                      "Це для моделей, які не вміщуються на одну плату.",
        SHUT_BUTTON: "Вимкнути стільницю заради ШІ",
        SHUT_ASK: "Вимкнути стільницю?\n\n"
                  "Усе відкрите закриється без збереження, і близько пів гігабайта піде моделі. "
                  "Екран стане чорним.\n\n"
                  "Щоб повернутися: з Remote Manager на іншому комп'ютері або `skillfish-ai-mode off` через ssh.",
        START_NODES: "Запустити вузли",
        STOP_NODES: "Зупинити вузли",
        STUDIO_ON: "Studio увімкнено (усе)",
        NO_RPC: "Плата є у списку, але вузла RPC на ній ще немає: його треба встановити на тій машині "
                "в /opt/skillfish-rpc.",
        NEW_PW: "Новий пароль:\n\n%s\n\nКористувач: unsloth",
        OTHER_PW: "Пароль змінено, але НЕ на вибраний вами:\n\n%s\n\nВикористайте той, що нижче.",
        NOT_STORED: "Ми його ніде не зберігаємо.",
        ADDRESS: "адреса, напр. 192.168.1.40",
        CHECKING: "перевіряємо...",
        COULD_NOT: "не вдалося",
        DESKTOP_RUNNING: "стільниця працює",
        FREE_OF: "вільно з %.1f GB · плат: %d · %d W%s",
        NO_BOARD: "немає плат",
        NO_LONGER_VALID: "більше не дійсний",
        NO_MODEL: "модель не знайдено",
        STARTED_ON: "вузли запущено на платах: %d",
        STOPPED_ON: "вузли зупинено на платах: %d",
        PW_ONCE: "пароль (потрібен один раз)",
        REPEAT: "повторіть",
        SEARCH_HF: "шукати на Hugging Face: qwen, llama, gemma, coder...",
        SEARCHING: "шукаємо...",
        KEY_MISSING: "немає ключа API: увійдіть вище",
        KEY_INVALID: "ключ API більше не дійсний: увійдіть знову",
        PW_MISMATCH: "паролі не збігаються",
        TYPE_SOMETHING: "введіть, що шукати",
        USER: "користувач",
    },
}

for lang, new in sorted(ENTRIES.items()):
    path = os.path.join(ROOT, lang + ".json")
    with io.open(path, encoding="utf-8") as f:
        d = json.load(f)
    added = [k for k in new if k not in d]
    d.update({k: v for k, v in new.items() if k not in d})
    with io.open(path, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(d.items(), key=lambda kv: kv[0].lower())), f,
                  ensure_ascii=False, indent=1)
        f.write("\n")
    print("%s: +%d (total %d)" % (lang, len(added), len(d)))

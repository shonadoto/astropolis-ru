# Astropolis RU

Неофициальная русская редакция модпака [Astropolis 2.2](https://www.curseforge.com/minecraft/modpacks/astropolis) от benbenlaw для Minecraft 1.19.2 и Forge 43.3.9.

## Что переведено

- вся книга FTB Quests: 31 файл, 631 отображаемая строка;
- названия предметов и блока, добавленных сборкой через KubeJS;
- статусы измерений для Simple Discord Rich Presence;
- названия глав, заданий, таблиц наград и внутриигровые подсказки.

ID заданий, зависимости, условия, награды, рецепты и баланс оригинальной сборки не изменены. Названия модов и имена собственные сохранены там, где перевод исказил бы узнаваемость. Единые варианты терминов зафиксированы в [глоссарии](docs/GLOSSARY.md).

## Установка клиента

1. Скачайте [готовый архив Astropolis-RU-2.2-ru.1.zip](https://github.com/shonadoto/astropolis-ru/raw/main/dist/Astropolis-RU-2.2-ru.1.zip) или соберите его командой `./tools/build.sh`.
2. В CurseForge App выберите **Minecraft → My Modpacks → Import**.
3. Укажите `Astropolis-RU-2.2-ru.1.zip`.
4. В настройках Minecraft выберите язык **Русский (Россия)**.

Архив содержит только manifest и overrides. Файлы модов лаунчер скачивает с CurseForge по их project/file ID.

## Автоматический ресурспак

Клиентские языковые файлы можно собрать в отдельный ресурспак:

```bash
python3 tools/build_resource_pack.py
```

Архив создаётся в `dist/Astropolis-RU-ResourcePack-2.2-ru.1.zip`. Он содержит все файлы
`overrides/kubejs/assets/*/lang/ru_ru.json` и подходит для автоматической раздачи через
параметры `resource-pack`, `resource-pack-sha1` и `require-resource-pack` выделенного сервера.

Изменения русских языковых файлов в ветке `main` автоматически обновляют постоянный релиз
`resourcepack-latest` в GitHub Releases.

## Выделенный сервер

На Linux сервер устанавливается и управляется единым скриптом:

```bash
./serverctl install
./serverctl start
./serverctl status
./serverctl logs
```

Остановка, перезапуск, консольная команда и резервная копия:

```bash
./serverctl stop
./serverctl restart
./serverctl console "say Сервер скоро перезапустится"
./serverctl backup
```

По умолчанию сервер использует 4–10 ГБ памяти, работает на порту `25565`, создаёт мир с preset `skyblockbuilder:skyblock` и хранит его в локальном каталоге `server/`. Настройки можно переопределить в `.server.env` по образцу [.server.env.example](.server.env.example).

Команда установки записывает `eula=true`; запускающий её владелец сервера должен принять [Minecraft EULA](https://aka.ms/MinecraftEULA).

## Проверка перевода

```bash
python3 tools/validate_translation.py
```

Проверка гарантирует, что перевод не изменил квестовые ID, предметы, зависимости или награды. Каталог исходных и русских строк находится в `translation/quest_strings.tsv`, а редакторские решения — в `tools/review_quest_translation.py`.

## Статус

Первая редакция перевода готова для игрового тестирования. Текст на кнопках кастомного главного меню зашит в PNG оригинальной сборки и пока остаётся английским; это не влияет на квесты и игровой процесс.

## Авторство

Astropolis и его оригинальные материалы принадлежат benbenlaw и соответствующим авторам модов. Этот репозиторий распространяет неофициальный перевод и не включает JAR-файлы модов.

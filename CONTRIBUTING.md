# Как предложить исправление перевода

1. Проверьте выбранный термин в `docs/GLOSSARY.md`.
2. Измените русский вариант в `translation/quest_strings.tsv` и синхронный exact override в `tools/review_quest_translation.py`.
3. Запустите `python3 tools/apply_quest_translation.py`.
4. Запустите `python3 tools/validate_translation.py`.

При спорном названии предмета укажите мод и фактическую строку из его `ru_ru.json`. Не переводите registry ID, команды, URL и названия модов.

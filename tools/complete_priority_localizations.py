#!/usr/bin/env python3
"""Apply manually reviewed translations left after the official-source import."""

from __future__ import annotations

import json
import re
import zipfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "overrides/kubejs/assets"
PLACEHOLDER_RE = re.compile(r"%(?:\d+\$)?([a-zA-Z%])")

MANUAL = {
    "ae2": {
        "ae2.rei_jei_integration.flowing_fluid_name": "%s (течение)",
        "ae2.rei_jei_integration.silk_touch_causes_less_decay": "«Шёлковое касание» уменьшает распад",
        "ae2.rei_jei_integration.spatial_io_causes_none": "Пространственный ввод-вывод не вызывает распада",
        "chat.ae2.ChannelModeCurrent": "Текущий режим каналов: %s",
        "chat.ae2.TestWorldNotInSuperflatVoid": "Тестовый мир можно создать только в плоском мире с шаблоном «Пустота»!",
        "gui.ae2.SearchSettingsSearchTooltips": "Искать в подсказках",
        "gui.ae2.SearchTooltipIncludingTooltips": "Искать в названиях и подсказках",
        "gui.ae2.units.rf": "RF",
        "gui.tooltips.ae2.ShowAll": "Показать всё",
        "gui.tooltips.ae2.ShowFluidsOnly": "Показать только жидкости",
        "gui.tooltips.ae2.ShowItemsOnly": "Показать только предметы",
    },
    "quark": {
        "quark.jei.hint.echorang": "Эхоранг действует как пикаранг, но постоянно создаёт вибрации и летит дольше, если слышит скалк-крикуна.",
        "quark.jei.hint.gold_tool_fortune": "Золотые инструменты имеют встроенные чары «Удача %s» или эффект «Добыча». Они не складываются с наложенными чарами: применяется только самый высокий уровень.",
        "quark.jei.hint.head_sfx": "Голову любого монстра можно установить сбоку от нотного блока: при получении сигнала он воспроизведёт звук этого монстра.",
        "quark.jei.hint.minecraft.jukebox": "Используйте раздатчик, чтобы автоматически вставлять пластинки в проигрыватель.",
        "quark.jei.hint.pink_blossom_sapling": "Можно найти в горах.",
        "quark.jei.hint.runes": "Объедините руну с зачарованным предметом на наковальне, чтобы изменить цвет его блеска. Это только визуальный эффект.",
        "quark.jei.hint_preamble": "[Quark]\n",
        "tag.item.quark.runes": "Руны",
        "tag.item.quark.runes_lootable": "Руны в добыче",
    },
    "fancymenu": {
        "fancymenu.animation.choose": "Выбор анимации",
        "fancymenu.animation.choose.available_animations": "Доступные анимации",
        "fancymenu.animation.choose.no_animation_selected": "§xСначала выберите анимацию!",
        "fancymenu.animation.choose.no_animations": "§xАнимации не найдены!",
        "fancymenu.animation.choose.preview": "Предпросмотр анимации",
        "fancymenu.background.animation": "Анимация",
        "fancymenu.background.animation.configure": "Настройка анимированного фона",
        "fancymenu.background.animation.configure.choose_animation": "Выбрать анимацию",
        "fancymenu.background.animation.configure.no_animation_chosen": "§xСначала выберите анимацию!",
        "fancymenu.background.animation.configure.restart_on_load.off": "Перезапускать анимацию при открытии экрана: §xОтключено",
        "fancymenu.background.animation.configure.restart_on_load.on": "Перезапускать анимацию при открытии экрана: §yВключено",
        "fancymenu.background.animation.desc": "Анимированный фон.\nПодробности: docs.fancymenu.net.",
        "fancymenu.background.image.desc": "Обычное изображение.\nПоддерживает JPEG, PNG, APNG и другие форматы,\nа также локальные файлы и веб-ссылки.",
        "fancymenu.background.slideshow": "Слайд-шоу",
        "fancymenu.customization.items.slider.editor.range.set_max_range_value": "Задать максимальное значение",
        "fancymenu.customization.items.slider.editor.range.set_min_range_value": "Задать минимальное значение",
        "fancymenu.customization.items.slider.editor.set_label_prefix": "Задать префикс подписи",
        "fancymenu.customization.items.slider.editor.set_label_suffix": "Задать суффикс подписи",
        "fancymenu.customization.items.text.scrolling.off": "Прокрутка: §xОтключена",
        "fancymenu.customization.items.text.scrolling.on": "Прокрутка: §yВключена",
        "fancymenu.customization.items.text.shadow.off": "Тень: §xОтключена",
        "fancymenu.customization.items.text.shadow.on": "Тень: §yВключена",
        "fancymenu.customization.items.ticker.async.off": "Асинхронность: §xОтключена",
        "fancymenu.customization.items.ticker.async.on": "Асинхронность: §yВключена",
        "fancymenu.editor.action.screens.add_action.desc": "Добавить новое действие.",
        "fancymenu.editor.action.screens.edit_action": "Изменить",
        "fancymenu.editor.action.screens.edit_action.desc": "Изменить выбранную запись.",
        "fancymenu.editor.action.screens.finish.no_action_selected": "§xСначала выберите действие!",
        "fancymenu.editor.action.screens.remove_action": "Удалить",
        "fancymenu.editor.action.screens.remove_action.confirm": "§x§lВы уверены?\n\nДействительно §xудалить §rвыбранное действие?\nЭто нельзя отменить!",
        "fancymenu.editor.action.screens.remove_action.desc": "Удалить выбранную запись.",
        "fancymenu.editor.actions.execute_terminal_command.edit": "Изменить команды терминала",
        "fancymenu.editor.actions.execute_terminal_command.edit.desc.line1": "Команды задаются отдельно для каждой ОС.",
        "fancymenu.editor.actions.execute_terminal_command.edit.desc.line2": "Действие выполняется только в ОС, для которой задана команда.",
        "fancymenu.editor.actions.execute_terminal_command.edit.desc.line3": "Для неизвестной ОС будет использована команда Linux.",
        "fancymenu.editor.actions.execute_terminal_command.linux": "Команда Linux:",
        "fancymenu.editor.actions.execute_terminal_command.macos": "Команда macOS:",
        "fancymenu.editor.actions.execute_terminal_command.windows": "Команда Windows:",
        "fancymenu.editor.add.animation": "Анимация",
        "fancymenu.editor.add.animation.desc": "Анимация похожа на GIF, но имеет более высокое разрешение.\n\nПодробности: docs.fancymenu.net.",
        "fancymenu.editor.add.slideshow": "Слайд-шоу",
        "fancymenu.editor.custombutton.config.actiontype.copyfile": "Копировать файл или папку",
        "fancymenu.editor.custombutton.config.actiontype.copyfile.desc": "Копирует файл или папку.",
        "fancymenu.editor.custombutton.config.actiontype.copyfile.desc.value": "Путь к файлу или папке + путь назначения [через ';']",
        "fancymenu.editor.custombutton.config.actiontype.deletefile": "Удалить файл или папку",
        "fancymenu.editor.custombutton.config.actiontype.deletefile.desc": "Удаляет файл или папку.",
        "fancymenu.editor.custombutton.config.actiontype.downloadfile": "Скачать файл",
        "fancymenu.editor.custombutton.config.actiontype.downloadfile.desc": "Скачивает файл.",
        "fancymenu.editor.custombutton.config.actiontype.downloadfile.desc.value": "URL + путь назначения [через ';']",
        "fancymenu.editor.custombutton.config.actiontype.mimicbutton.desc": "Имитирует нажатие обычной кнопки Minecraft или другого мода.\n\nНужен §lлокатор кнопки§r. Чтобы получить его, щёлкните кнопку ПКМ в редакторе. Вне редактора включите отладочный оверлей и щёлкните кнопку ПКМ.",
        "fancymenu.editor.custombutton.config.actiontype.mimicbutton.desc.value": "Локатор кнопки",
        "fancymenu.editor.custombutton.config.actiontype.movefile": "Переместить файл или папку",
        "fancymenu.editor.custombutton.config.actiontype.movefile.desc": "Перемещает файл или папку.",
        "fancymenu.editor.custombutton.config.actiontype.movefile.desc.value": "Старый путь + новый путь [через ';']",
        "fancymenu.editor.custombutton.config.actiontype.openfile": "Открыть файл или папку",
        "fancymenu.editor.custombutton.config.actiontype.openfile.desc": "Открывает файл или папку.",
        "fancymenu.editor.custombutton.config.actiontype.openfile.desc.value": "Путь к файлу или папке",
        "fancymenu.editor.custombutton.config.actiontype.quitgame.desc": "Выйти из Minecraft.",
        "fancymenu.editor.custombutton.config.actiontype.renamefile": "Переименовать файл или папку",
        "fancymenu.editor.custombutton.config.actiontype.renamefile.desc": "Переименовывает файл или папку.",
        "fancymenu.editor.custombutton.config.actiontype.renamefile.desc.value": "Путь + новое имя файла или папки [через ';']",
        "fancymenu.editor.custombutton.config.actiontype.runcmd": "Выполнить команду CMD или терминала",
        "fancymenu.editor.custombutton.config.actiontype.runcmd.desc": "Выполняет команду CMD или терминала.\nПоддерживает отдельные команды для разных ОС.",
        "fancymenu.editor.custombutton.config.actiontype.runscript": "Запустить сценарий кнопки",
        "fancymenu.editor.custombutton.config.actiontype.runscript.desc": "Запускает сценарий кнопки.",
        "fancymenu.editor.custombutton.config.actiontype.runscript.desc.value": "Имя файла сценария",
        "fancymenu.editor.custombutton.config.actiontype.unpackzip": "Распаковать ZIP-архив",
        "fancymenu.editor.custombutton.config.actiontype.unpackzip.desc": "Распаковывает ZIP-архив.",
        "fancymenu.editor.custombutton.config.actiontype.unpackzip.desc.value": "Путь к архиву + путь назначения [через ';']",
        "fancymenu.editor.items.button.btndescription.desc": "Подсказка, отображаемая при наведении на элемент.",
        "fancymenu.editor.items.button.clicksound": "Звук нажатия",
        "fancymenu.editor.items.setorientation": "Точка привязки",
        "fancymenu.editor.items.splash.basecolor": "Задать цвет текста",
        "fancymenu.editor.items.splash.bounce.off": "Подпрыгивание: §xОтключено",
        "fancymenu.editor.items.splash.bounce.on": "Подпрыгивание: §yВключено",
        "fancymenu.editor.items.splash.refresh.off": "Обновлять при открытии экрана: §xОтключено",
        "fancymenu.editor.items.splash.refresh.on": "Обновлять при открытии экрана: §yВключено",
        "fancymenu.editor.items.splash.rotation": "Задать поворот",
        "fancymenu.editor.loading_requirement.screens.build_screen.requirement_mode.normal": "Режим условия: §zОБЫЧНЫЙ",
        "fancymenu.editor.loading_requirement.screens.build_screen.requirement_mode.opposite": "Режим условия: §zОБРАТНЫЙ",
        "fancymenu.editor.loading_requirement.screens.manage_screen.edit.generic": "Изменить",
        "fancymenu.editor.loading_requirement.screens.manage_screen.manage": "Управление условиями загрузки",
        "fancymenu.editor.loading_requirement.screens.manage_screen.remove.generic": "Удалить",
        "fancymenu.editor.loading_requirement.screens.remove_group.confirm": "§x§lВы уверены?\n\nДействительно §xудалить §rвыбранную группу?\nЭто действие нельзя отменить!",
        "fancymenu.editor.loading_requirement.screens.remove_requirement.confirm": "§x§lВы уверены?\n\nДействительно §xудалить §rвыбранное условие?\nЭто действие нельзя отменить!",
        "fancymenu.editor.loading_requirement.screens.requirement.info.mode.normal": "Обычный",
        "fancymenu.element.general.appearance_delay.fade_in.off": "Плавное появление: §xОтключено",
        "fancymenu.element.general.appearance_delay.fade_in.on": "Плавное появление: §yВключено",
        "fancymenu.elements.animation.restore_aspect_ratio": "Восстановить соотношение сторон",
        "fancymenu.elements.animation.set_animation": "Задать анимацию",
        "fancymenu.elements.splash.shadow.off": "Тень: §xОтключена",
        "fancymenu.elements.splash.shadow.on": "Тень: §yВключена",
        "fancymenu.fancymenu.editor.dynamicvariabletextfield.categories.advanced": "Дополнительно",
        "fancymenu.fancymenu.editor.dynamicvariabletextfield.categories.realtime": "Реальное время",
        "fancymenu.fancymenu.editor.dynamicvariabletextfield.variables.local.desc": "Переводит текст по заданному ключу.\n\nЗамените 'localization.key' в заполнителе нужным ключом локализации.\n\n§xИнструкции по добавлению переводов: §ldocs.fancymenu.net§r.",
        "fancymenu.fancymenu.editor.dynamicvariabletextfield.variables.randomtext": "Случайная строка из TXT-файла",
        "fancymenu.fancymenu.editor.dynamicvariabletextfield.variables.randomtext.desc": "Выбирает случайную строку из TXT-файла.\n\nПоддерживает настраиваемый интервал смены строк. Замените 'randomtexts.txt' путём к своему файлу, а '10' — интервалом в секундах. При интервале 0 строка выбирается один раз за сеанс.",
        "fancymenu.fancymenu.editor.dynamicvariabletextfield.variables.realtimeday": "День",
        "fancymenu.fancymenu.editor.dynamicvariabletextfield.variables.realtimehour": "Час",
        "fancymenu.fancymenu.editor.dynamicvariabletextfield.variables.realtimeminute": "Минута",
        "fancymenu.fancymenu.editor.dynamicvariabletextfield.variables.realtimemonth": "Месяц",
        "fancymenu.fancymenu.editor.dynamicvariabletextfield.variables.realtimesecond": "Секунда",
        "fancymenu.fancymenu.editor.dynamicvariabletextfield.variables.realtimeyear": "Год",
        "fancymenu.guicomponents.reset": "Сбросить",
        "fancymenu.guicomponents.set": "Задать",
        "fancymenu.helper.buttonaction.paste_to_chat.desc": "Вставляет текст в поле чата.",
        "fancymenu.helper.buttonaction.variables.clearall": "Очистить все переменные",
        "fancymenu.helper.buttonaction.variables.clearall.desc": "Удаляет ВСЕ сохранённые переменные.",
        "fancymenu.helper.buttonaction.variables.set": "Задать значение переменной",
        "fancymenu.helper.buttonaction.variables.set.desc": "Сохраняет переменные для использования в заполнителях и условиях загрузки.",
        "fancymenu.helper.editor.element.vanilla.deepcustomization.titlescreen.realmsnotification": "Значок уведомлений Realms",
        "fancymenu.helper.editor.items.buttons.buttonbackground.set": "Задать",
        "fancymenu.helper.editor.items.loadingrequirement.file_exists.desc": "Проверяет существование файла или папки.",
        "fancymenu.helper.editor.items.playerentity.baby.off": "Детёныш: §xНет",
        "fancymenu.helper.editor.items.playerentity.baby.on": "Детёныш: §yДа",
        "fancymenu.helper.editor.items.playerentity.cape.auto.off": "Автовыбор плаща: §xОтключён",
        "fancymenu.helper.editor.items.playerentity.cape.auto.on": "Автовыбор плаща: §yВключён",
        "fancymenu.helper.editor.items.playerentity.copy_client_player.off": "Копировать игрока клиента: §xОтключено",
        "fancymenu.helper.editor.items.playerentity.copy_client_player.on": "Копировать игрока клиента: §yВключено",
        "fancymenu.helper.editor.items.playerentity.crouching.off": "Крадётся: §xНет",
        "fancymenu.helper.editor.items.playerentity.crouching.on": "Крадётся: §yДа",
        "fancymenu.helper.editor.items.playerentity.parrot.off": "Попугай: §xНет",
        "fancymenu.helper.editor.items.playerentity.parrot.on": "Попугай: §yДа",
        "fancymenu.helper.editor.items.playerentity.parrot_left.off": "Попугай на левом плече: §xНет",
        "fancymenu.helper.editor.items.playerentity.parrot_left.on": "Попугай на левом плече: §yДа",
        "fancymenu.helper.editor.items.playerentity.show_name.off": "Показывать имя игрока: §xНет",
        "fancymenu.helper.editor.items.playerentity.show_name.on": "Показывать имя игрока: §yДа",
        "fancymenu.helper.editor.items.playerentity.skin.auto.off": "Автовыбор скина: §xОтключён",
        "fancymenu.helper.editor.items.playerentity.skin.auto.on": "Автовыбор скина: §yВключён",
        "fancymenu.helper.editor.items.playerentity.slim.off": "Тонкая модель: §xНет",
        "fancymenu.helper.editor.items.playerentity.slim.on": "Тонкая модель: §yДа",
        "fancymenu.helper.editor.items.visibilityrequirements.guiscale.desc": "Проверяет текущий масштаб интерфейса.\n\nПоддерживаются больше ('>'), меньше ('<') и точное равенство. Например: '<3.20', '1.0' или '>2.20' (без кавычек).",
        "fancymenu.helper.editor.items.visibilityrequirements.is_any_button_hovered": "Курсор наведён на ЛЮБУЮ кнопку",
        "fancymenu.helper.editor.items.visibilityrequirements.is_any_element_hovered": "Курсор наведён на ЛЮБОЙ элемент",
        "fancymenu.helper.placeholder.get_variable": "Получить сохранённую переменную",
        "fancymenu.helper.placeholder.get_variable.desc": "Возвращает значение сохранённой переменной.\n\nЗамените 'some_variable' настоящим именем переменной.",
        "fancymenu.helper.placeholder.json.desc": "Разбирает JSON и возвращает значение.\n\nЗамените 'path_or_link_to_json' путём или ссылкой на JSON-файл, а '$.some.json.path' — путём JSON до нужного значения.\n\n§zПодробнее о путях JSON: §ljson.fancymenu.net§r§z.",
        "fancymenu.helper.visibilityrequirement.is_variable_value.desc": "Проверяет, равно ли значение сохранённой переменной X. Поддерживаются только собственные переменные FancyMenu, но не переменные других модов или Minecraft.",
        "fancymenu.overlay.menu_bar.user_interface.ui_scale": "Масштаб интерфейса: %s",
        "fancymenu.overlay.menu_bar.user_interface.ui_text_shadow": "Тень текста интерфейса: %s",
    },
}


def english_for(namespace: str) -> dict[str, str]:
    wanted = f"assets/{namespace}/lang/en_us.json"
    for jar in sorted((ROOT / "server/mods").glob("*.jar")):
        try:
            with zipfile.ZipFile(jar) as archive:
                if wanted in archive.namelist():
                    return json.loads(archive.read(wanted).decode("utf-8-sig"))
        except zipfile.BadZipFile:
            continue
    raise SystemExit(f"English language file for {namespace} not found")


def placeholders(value: str) -> Counter[str]:
    return Counter(PLACEHOLDER_RE.findall(value))


def main() -> None:
    for namespace, translations in MANUAL.items():
        english = english_for(namespace)
        unknown = set(translations) - set(english)
        if unknown:
            raise SystemExit(f"Unknown {namespace} keys: {sorted(unknown)}")
        for key, russian in translations.items():
            if placeholders(english[key]) != placeholders(russian):
                raise SystemExit(f"Placeholder mismatch in {key}")
        output = ASSETS / namespace / "lang/ru_ru.json"
        current = json.loads(output.read_text(encoding="utf-8-sig")) if output.exists() else {}
        current.update(translations)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{namespace}: applied {len(translations)} reviewed strings")


if __name__ == "__main__":
    main()

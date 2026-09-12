#!/usr/bin/env python3
"""Generate the consistent Russian Rechiseled block-name catalogue.

Rechiseled has hundreds of mechanically generated names.  Keeping the material
and pattern dictionaries separate prevents the same texture pattern from being
translated differently for every material.
"""

from __future__ import annotations

import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "overrides/kubejs/assets/rechiseled/lang/ru_ru.json"

MATERIALS = {
    "amethyst_block": "аметистового блока",
    "acacia_planks": "акациевых досок",
    "andesite": "андезита",
    "basalt": "базальта",
    "birch_planks": "берёзовых досок",
    "blackstone": "чернита",
    "blue_ice": "синего льда",
    "bone_block": "костного блока",
    "coal_block": "угольного блока",
    "cobbled_deepslate": "колотого глубинного сланца",
    "cobblestone": "булыжника",
    "copper_block": "медного блока",
    "crimson_planks": "багровых досок",
    "dark_oak_planks": "досок тёмного дуба",
    "dark_prismarine": "тёмного призмарина",
    "diamond_block": "алмазного блока",
    "diorite": "диорита",
    "dirt": "земли",
    "emerald_block": "изумрудного блока",
    "end_stone": "эндерняка",
    "glowstone": "светокамня",
    "gold_block": "золотого блока",
    "granite": "гранита",
    "iron_block": "железного блока",
    "jungle_planks": "досок тропического дерева",
    "lapis_block": "лазуритового блока",
    "mangrove_planks": "мангровых досок",
    "mossy_cobblestone": "замшелого булыжника",
    "nether_bricks": "незерских кирпичей",
    "netherite_block": "незеритового блока",
    "netherrack": "незерака",
    "oak_planks": "дубовых досок",
    "obsidian": "обсидиана",
    "prismarine_bricks": "призмариновых кирпичей",
    "prismarine": "призмарина",
    "purpur": "пурпура",
    "quartz_block": "кварцевого блока",
    "red_nether_bricks": "красных незерских кирпичей",
    "red_sandstone": "красного песчаника",
    "redstone_block": "редстоунового блока",
    "sandstone": "песчаника",
    "spruce_planks": "еловых досок",
    "stone": "камня",
    "warped_planks": "искажённых досок",
}

PATTERNS = {
    "tiles": "Плитка",
    "rotated_bricks": "Повёрнутые кирпичи",
    "brick_paving": "Кирпичная кладка",
    "small_tiles": "Мелкая плитка",
    "bricks": "Кирпичи",
    "brick_pattern": "Кирпичный узор",
    "squares": "Квадраты",
    "beams": "Балки",
    "large_tiles": "Крупная плитка",
    "diagonal_tiles": "Диагональная плитка",
    "polished": "Полированный блок",
    "dotted": "Точечный узор",
    "pattern": "Узор",
    "small_bricks": "Мелкие кирпичи",
    "wavy": "Волнистый узор",
    "pillar": "Колонна",
    "woven": "Плетёный узор",
    "diagonal_bricks": "Диагональные кирпичи",
    "bordered": "Окаймлённый блок",
    "chiseled": "Резной блок",
    "crate": "Ящик",
    "diagonal_stripes": "Диагональные полосы",
    "flooring": "Настил",
    "smooth": "Гладкий блок",
    "paving": "Мощение",
    "stripes": "Полосы",
    "patterned": "Узорчатый блок",
    "mosaic": "Мозаика",
    "scales": "Чешуя",
    "crushed": "Дроблёный блок",
    "chiseled_squares": "Резные квадраты",
    "circles": "Круги",
    "worn_stripes": "Потёртые полосы",
    "dented": "Вмятины",
    "lines": "Линии",
    "rows": "Ряды",
    "connecting": "Соединённый блок",
    "decorated": "Декорированный блок",
    "pulverized": "Измельчённый блок",
    "crosses": "Кресты",
    "slanted_tiles": "Наклонная плитка",
    "inverted_tiles": "Инвертированная плитка",
    "compacted": "Уплотнённый блок",
    "inverted_dented": "Инвертированные вмятины",
    "gears": "Шестерни",
    "fabric": "Тканый узор",
    "blobs": "Пятна",
    "striped": "Полосатый блок",
    "spiral_pattern": "Спиральный узор",
    "large_bricks": "Крупные кирпичи",
    "chiseled_circles": "Резные круги",
    "pillars": "Колонны",
    "shiny": "Блестящий блок",
    "cobbled": "Булыжная кладка",
    "bordered_diagonal_tiles": "Окаймлённая диагональная плитка",
    "cut": "Огранённый блок",
    "edged": "Блок с окантовкой",
    "jewel": "Драгоценный блок",
    "bordered_polished": "Окаймлённый полированный блок",
    "chiseled_piglin": "Резное изображение пиглина",
    "cone": "Конус",
    "cracked": "Потрескавшийся блок",
    "rocky": "Каменистый блок",
    "bundled": "Связанный блок",
    "decorated_bordered": "Окаймлённый декорированный блок",
    "rib": "Рёбра",
    "skull": "Череп",
    "carved": "Высеченный блок",
    "ovals": "Овалы",
    "chiseled_border": "Резная кайма",
    "large_squares": "Крупные квадраты",
    "sheared": "Стёсанный блок",
    "bars": "Прутья",
    "shafts": "Валы",
    "chiseled_cubes": "Резные кубы",
    "grid": "Решётка",
    "jewel_block": "Драгоценный блок",
    "rhombuses": "Ромбы",
    "shiny_bordered": "Окаймлённый блестящий блок",
    "chunks": "Глыбы",
    "clumps": "Комья",
    "grooves": "Борозды",
    "muddy": "Грязный блок",
    "smooth_clumps": "Гладкие комья",
    "soil": "Почва",
    "tilled": "Вспаханный блок",
    "bordered_crosses": "Окаймлённые кресты",
    "bordered_plating": "Окаймлённые пластины",
    "clovers": "Клевер",
    "crystal": "Кристаллический блок",
    "patterned_squares": "Узорчатые квадраты",
    "plating": "Пластины",
    "waxed": "Вощёный блок",
    "mesh": "Сетка",
    "framed": "Каркасный блок",
    "pipes": "Трубы",
    "plated": "Обшитый пластинами блок",
    "processed": "Обработанный блок",
    "reinforced": "Укреплённый блок",
    "sheets": "Листы",
    "glossy": "Глянцевый блок",
    "swirling": "Вихревой узор",
    "indented": "Углублённый блок",
    "meteoric": "Метеоритный блок",
    "chiseled_creeper": "Резное изображение крипера",
    "chiseled_skeleton": "Резное изображение скелета",
    "dark": "Тёмный блок",
    "spots": "Пятна",
    "jagged_pattern": "Зубчатый узор",
    "organic_pattern": "Органический узор",
    "chiseled_pillar": "Резная колонна",
    "brick_bordered": "Окаймлённая кирпичная кладка",
    "chiseled_clovers": "Резной клевер",
    "compressed": "Сжатый блок",
    "big_tiles": "Большая плитка",
    "chiseled_bricks": "Резные кирпичи",
    "path": "Дорожка",
    "slated": "Плиточный узор",
    "smooth_brick_paving": "Гладкая кирпичная кладка",
    "smooth_large_tiles": "Крупная гладкая плитка",
    "smooth_rotated_bricks": "Гладкие повёрнутые кирпичи",
    "smooth_tiles": "Гладкая плитка",
    "waves": "Волны",
}

UI = {
    "rechiseled.item_group": "Rechiseled",
    "rechiseled": "Rechiseled",
    "rechiseled.tooltip.connecting": "Соединяемая текстура",
    "rechiseled.chiseling.preview.mode_0": "Предпросмотр 1 × 1",
    "rechiseled.chiseling.preview.mode_1": "Предпросмотр 3 × 1",
    "rechiseled.chiseling.preview.mode_2": "Предпросмотр 3 × 3",
    "rechiseled.chiseling.connecting": "Соединяемые текстуры: %s",
    "rechiseled.chiseling.connecting.on": "Вкл.",
    "rechiseled.chiseling.connecting.off": "Выкл.",
    "rechiseled.chiseling.chisel_all": "Обработать всё",
    "rechiseled.chiseling.select_block": "Выбрать %s",
    "rechiseled.chiseling.preview": "Предпросмотр блока",
    "rechiseled.jei_category.title": "Обработка резцом",
    "rechiseled.item.chisel": "Резец",
}


def find_jar() -> Path:
    for path in sorted((ROOT / "server/mods").glob("*.jar")):
        try:
            with zipfile.ZipFile(path) as archive:
                if "assets/rechiseled/lang/en_us.json" in archive.namelist():
                    return path
        except zipfile.BadZipFile:
            continue
    raise SystemExit("Rechiseled jar not found in server/mods")


def main() -> None:
    with zipfile.ZipFile(find_jar()) as archive:
        english = json.loads(archive.read("assets/rechiseled/lang/en_us.json"))

    russian = dict(UI)
    for key in english:
        if not key.startswith("rechiseled.block."):
            continue
        block_id = key.removeprefix("rechiseled.block.")
        base_id = block_id.removesuffix("_connecting")
        for material in sorted(MATERIALS, key=len, reverse=True):
            prefix = material + "_"
            if base_id.startswith(prefix):
                pattern = base_id.removeprefix(prefix)
                if pattern not in PATTERNS:
                    raise SystemExit(f"Unknown pattern {pattern!r} in {key}")
                russian[key] = f"{PATTERNS[pattern]} из {MATERIALS[material]}"
                break
        else:
            raise SystemExit(f"Unknown material in {key}")

    missing = set(english) - set(russian)
    extra = set(russian) - set(english)
    if missing or extra:
        raise SystemExit(f"Key mismatch: missing={sorted(missing)}, extra={sorted(extra)}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(russian, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(russian)} strings to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Add reviewed translations for runtime description IDs absent from mod lang files."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "overrides" / "kubejs" / "assets"
TRANSLATIONS: dict[str, dict[str, str]] = defaultdict(dict)


def add(namespace: str, key: str, value: str) -> None:
    TRANSLATIONS[namespace][key] = value


# More Mekanism Processing registers the items below but supplies only dynamic
# naming fragments. Explicit names read naturally in Russian and also prevent
# JEI from ever exposing their raw description IDs.
MMP_MATERIALS = {
    "aluminum": "алюминия",
    "amethyst": "аметиста",
    "apatite": "апатита",
    "azure_silver": "лазурного серебра",
    "bismuth": "висмута",
    "bort": "борта",
    "calorite": "калорита",
    "cinnabar": "киновари",
    "coal": "угля",
    "cobalt": "кобальта",
    "crimson_iron": "багрового железа",
    "desh": "деша",
    "diamond": "алмаза",
    "dilithium": "дилития",
    "draconium": "дракония",
    "electrotine": "электротина",
    "emerald": "изумруда",
    "green_sapphire": "зелёного сапфира",
    "iridium": "иридия",
    "lapis": "лазурита",
    "lithium": "лития",
    "nickel": "никеля",
    "niter": "селитры",
    "ostrum": "острума",
    "peridot": "перидота",
    "platinum": "платины",
    "quartz": "незер-кварца",
    "redstone": "редстоуна",
    "ruby": "рубина",
    "sapphire": "сапфира",
    "silver": "серебра",
    "sulfur": "серы",
    "titanium": "титана",
    "tungsten": "вольфрама",
    "zinc": "цинка",
}
MMP_FORMS = {
    "clump": ("Глыба {}", set(MMP_MATERIALS)),
    "crystal": ("Кристалл {}", set(MMP_MATERIALS)),
    "dirty_dust": ("Загрязнённая пыль {}", set(MMP_MATERIALS)),
    "shard": ("Осколок {}", set(MMP_MATERIALS)),
    "dust": (
        "Пыль {}",
        set(MMP_MATERIALS) - {"coal", "diamond", "emerald", "lapis", "lithium", "quartz", "redstone", "sulfur"},
    ),
    "gem": ("Самоцвет {}", {"apatite", "bort", "cinnabar", "dilithium", "green_sapphire", "niter", "peridot", "ruby", "sapphire"}),
    "ingot": ("Слиток {}", {"aluminum", "azure_silver", "bismuth", "calorite", "cobalt", "crimson_iron", "desh", "draconium", "iridium", "lithium", "nickel", "ostrum", "platinum", "silver", "titanium", "tungsten", "zinc"}),
    "nugget": ("Кусочек {}", {"aluminum", "azure_silver", "bismuth", "calorite", "cobalt", "crimson_iron", "desh", "draconium", "iridium", "lithium", "nickel", "ostrum", "platinum", "silver", "titanium", "tungsten", "zinc"}),
}
for form, (template, materials) in MMP_FORMS.items():
    for material in sorted(materials):
        path = f"{material}_{form}" if form in {"ingot", "nugget"} else f"{form}_{material}"
        add("moremekanismprocessing", f"item.moremekanismprocessing.{path}", template.format(MMP_MATERIALS[material]))


# Maiden's Merry Making contains real registered component blocks and item
# variants for which the mod accidentally omitted language entries.
MAIDEN_WOODS = {
    "acacia": "акации",
    "aged_pine": "старой сосны",
    "birch": "берёзы",
    "crimson": "багрового стебля",
    "dark_oak": "тёмного дуба",
    "exposed_pine": "потемневшей сосны",
    "jungle": "тропического дерева",
    "mangrove": "мангрового дерева",
    "oak": "дуба",
    "pine": "сосны",
    "spruce": "ели",
    "warped": "искажённого стебля",
    "weathered_pine": "обветренной сосны",
}
for wood, russian in MAIDEN_WOODS.items():
    prefix = f"block.maidensmerrymaking.mantel_{wood}"
    add("maidensmerrymaking", f"{prefix}_leg_left", f"Левая ножка каминной полки из {russian}")
    add("maidensmerrymaking", f"{prefix}_leg_right", f"Правая ножка каминной полки из {russian}")
    for position, position_ru in (("left", "левая"), ("middle", "средняя"), ("right", "правая")):
        add(
            "maidensmerrymaking",
            f"{prefix}_top_{position}_stocking",
            f"Верхняя {position_ru} часть каминной полки из {russian} с чулком",
        )

for tree, russian in (
    ("christmas_pine", "рождественской сосны"),
    ("christmas_tree", "рождественской ёлки"),
    ("white_christmas_tree", "белой рождественской ёлки"),
):
    for part, part_ru in (("bottom", "Нижняя"), ("middle", "Средняя"), ("top", "Верхняя")):
        add("maidensmerrymaking", f"block.maidensmerrymaking.{tree}_{part}", f"{part_ru} часть {russian}")

MAIDEN_DIRECT = {
    "block.maidensmerrymaking.lamp_post_bottom": "Основание фонарного столба",
    "block.maidensmerrymaking.lamp_post_pole": "Стойка фонарного столба",
    "block.maidensmerrymaking.lamp_post_pole_bow": "Стойка фонарного столба с бантом",
    "block.maidensmerrymaking.lamp_post_pole_wreath": "Стойка фонарного столба с венком",
    "block.maidensmerrymaking.lamp_post_pole_wreath_multi": "Стойка фонарного столба с разноцветным светящимся венком",
    "block.maidensmerrymaking.lamp_post_pole_wreath_white": "Стойка фонарного столба с белым светящимся венком",
    "block.maidensmerrymaking.mkeka_corn_1": "Мкека с одним початком кукурузы",
    "block.maidensmerrymaking.mkeka_corn_2": "Мкека с двумя початками кукурузы",
    "block.maidensmerrymaking.mkeka_corn_3": "Мкека с тремя початками кукурузы",
    "block.maidensmerrymaking.mkeka_with_chalice": "Мкека с чашей единства",
    "block.maidensmerrymaking.mkeka_with_kinara": "Мкека с кинарой",
    "block.maidensmerrymaking.mkeka_with_kinara_lit": "Мкека с зажжённой кинарой",
    "item.maidensmerrymaking.bunny_face": "Маска пасхального кролика",
    "item.maidensmerrymaking.lucky_hat": "Шляпа лепрекона",
    "item.maidensmerrymaking.mob_santa_hat": "Шапка Санты для мобов",
    "item.maidensmerrymaking.white_christmas_tree": "Белая рождественская ёлка",
}
for key, value in MAIDEN_DIRECT.items():
    add("maidensmerrymaking", key, value)
for color, color_ru in (("pink", "розового"), ("blue", "синего"), ("yellow", "жёлтого"), ("purple", "фиолетового"), ("cyan", "бирюзового")):
    for size, size_ru in (("small", "маленького"), ("large", "большого")):
        add(
            "maidensmerrymaking",
            f"item.maidensmerrymaking.{color}_bunny_{size}_spawn_egg",
            f"Яйцо призыва {size_ru} {color_ru} кролика",
        )


# Supplementaries generates compatibility blocks at runtime. Direct entries
# avoid English material fallbacks and preserve Russian genitive agreement.
SUPP_WOODS = {
    "pine": "сосны",
    "exposed_pine": "потемневшей сосны",
    "weathered_pine": "обветренной сосны",
    "aged_pine": "старой сосны",
    "preserved_pine": "вощёной сосны",
    "preserved_exposed_pine": "вощёной потемневшей сосны",
    "preserved_weathered_pine": "вощёной обветренной сосны",
    "preserved_aged_pine": "вощёной старой сосны",
}
for wood, russian in SUPP_WOODS.items():
    add("supplementaries", f"wood_type.maidensmerrymaking.{wood}", russian)
    add("supplementaries", f"block.supplementaries.maidensmerrymaking.hanging_sign_{wood}", f"Висячая табличка из {russian}")
    add("supplementaries", f"item.supplementaries.maidensmerrymaking.sign_post_{wood}", f"Знак из {russian}")

QUARK_WOODS = {
    "ancient": "старинного дерева",
    "azalea": "азалии",
    "bamboo": "бамбука",
    "blossom": "цветущего дерева",
}
for wood, russian in QUARK_WOODS.items():
    add("supplementaries", f"wood_type.quark.{wood}", russian)
    add("supplementaries", f"block.supplementaries.quark.hanging_sign_{wood}", f"Висячая табличка из {russian}")
    add("supplementaries", f"item.supplementaries.quark.sign_post_{wood}", f"Знак из {russian}")
add("supplementaries", "wood_type.deeperdarker.echo", "эхо-древесины")
add("supplementaries", "block.supplementaries.deeperdarker.hanging_sign_echo", "Висячая табличка из эхо-древесины")
add("supplementaries", "item.supplementaries.deeperdarker.sign_post_echo", "Знак из эхо-древесины")
for key, value in {
    "block.supplementaries.block_generator": "Генератор блоков (служебный)",
    "block.supplementaries.rope_chandelier": "Верёвочная люстра",
    "block.supplementaries.rope_soul_chandelier": "Верёвочная люстра душ",
    "block.supplementaries.sconce_wall_ender": "Настенное эндер-бра",
    "block.supplementaries.sconce_wall_glow": "Настенное светящееся бра",
    "block.supplementaries.sconce_wall_green": "Настенное зелёное бра",
    "block.supplementaries.sconce_wall_nether_brass": "Настенное незерское латунное бра",
    "block.supplementaries.skull_candle_soul": "Свеча душ на черепе",
    "block.supplementaries.skull_candle_soul_wall": "Настенная свеча душ на черепе",
    "block.supplementaries.skull_candle_wall": "Настенная свеча на черепе",
}.items():
    add("supplementaries", key, value)


IE_DIRECT = {
    "block.immersiveengineering.acetaldehyde_fluid_block": "Ацетальдегид",
    "block.immersiveengineering.biodiesel_fluid_block": "Биодизель",
    "block.immersiveengineering.concrete_fluid_block": "Жидкий бетон",
    "block.immersiveengineering.creosote_fluid_block": "Креозот",
    "block.immersiveengineering.ethanol_fluid_block": "Этанол",
    "block.immersiveengineering.fake_light": "Невидимый источник света (служебный)",
    "block.immersiveengineering.herbicide_fluid_block": "Гербицид",
    "block.immersiveengineering.phenolic_resin_fluid_block": "Фенольная смола",
    "block.immersiveengineering.plantoil_fluid_block": "Растительное масло",
    "block.immersiveengineering.post_transformer": "Трансформаторная опора",
    "block.immersiveengineering.potted_hemp": "Промышленная конопля в горшке",
    "block.immersiveengineering.redstone_acid_fluid_block": "Редстоуновая кислота",
    "block.immersiveengineering.shader_banner": "Знамя с шейдером",
    "block.immersiveengineering.shader_banner_wall": "Настенное знамя с шейдером",
    "block.immersiveengineering.toolbox_block": "Ящик с инструментами",
    "item.immersiveengineering.armor_piercing": "Бронебойный патрон",
    "item.immersiveengineering.buckshot": "Патрон с картечью",
    "item.immersiveengineering.casull": "Патрон «Касулл»",
    "item.immersiveengineering.dragons_breath": "Патрон «Дыхание дракона»",
    "item.immersiveengineering.fake_icon_birthday": "Значок «День рождения» (служебный)",
    "item.immersiveengineering.fake_icon_bttf": "Значок «Назад в будущее» (служебный)",
    "item.immersiveengineering.fake_icon_drillbreak": "Значок поломки бура (служебный)",
    "item.immersiveengineering.fake_icon_fried": "Значок поражения током (служебный)",
    "item.immersiveengineering.fake_icon_lucky": "Счастливый значок (служебный)",
    "item.immersiveengineering.fake_icon_ravenholm": "Значок Рейвенхольма (служебный)",
    "item.immersiveengineering.firework": "Фейерверочный патрон",
    "item.immersiveengineering.flare": "Сигнальный патрон",
    "item.immersiveengineering.he": "Фугасный патрон",
    "item.immersiveengineering.homing": "Самонаводящийся патрон",
    "item.immersiveengineering.potion": "Патрон с зельем",
    "item.immersiveengineering.silver": "Серебряный патрон",
    "item.immersiveengineering.wolfpack": "Патрон «Волчья стая»",
}
for key, value in IE_DIRECT.items():
    add("immersiveengineering", key, value)


for number in range(14):
    add("tombstone", f"tombstone.item.advancement_{number}", f"Значок достижения №{number + 1} (служебный)")

for namespace, entries in {
    "compactmachines": {
        "block.compactmachines.machine_void_air": "Пустотный воздух компактной машины",
        "item.compactmachines.chunkloader_upgrade": "Улучшение загрузки чанков",
    },
    "engineersdecor": {
        "block.engineersdecor.test_block": "Тестовый блок ED (НЕ ИСПОЛЬЗОВАТЬ)",
    },
    "rftoolsstorage": {
        "block.rftoolsstorage.crafting_manager": "Менеджер крафта (в разработке)",
    },
    "rftoolsutility": {
        "block.rftoolsutility.screen_hitblock": "Область взаимодействия с экраном (служебная)",
        "item.rftoolsutility.teleport_probe": "Зонд телепорта",
    },
    "essence": {
        "block.essence.lightning_water_block": "Грозовая вода",
    },
    "decorative_blocks": {
        "item.decorative_blocks.blockstate_copy_item": "Копировщик состояния блока (служебный)",
    },
}.items():
    for key, value in entries.items():
        add(namespace, key, value)


def main() -> None:
    total = 0
    for namespace, translations in sorted(TRANSLATIONS.items()):
        output = ASSETS / namespace / "lang" / "ru_ru.json"
        current = json.loads(output.read_text(encoding="utf-8-sig")) if output.exists() else {}
        current.update(translations)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        total += len(translations)
        print(f"{namespace}: applied {len(translations)} runtime translations")
    print(f"Total: {total}")


if __name__ == "__main__":
    main()

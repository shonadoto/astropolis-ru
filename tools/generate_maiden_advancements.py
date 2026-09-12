#!/usr/bin/env python3
"""Create Russian overrides for Maiden's Merrymaking advancements."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "overrides/kubejs/data/maidensmerrymaking/advancements"

TRANSLATIONS = {
    "Here Comes Peter Cottontail!": "А вот и Питер Пушистый Хвост!",
    "Collect or craft all 4 pieces of the Bunny Suit Armor": "Соберите или создайте все 4 части брони костюма кролика",
    "Chick Magnet": "Цыплячий магнит",
    "Breed two Yellow Chickens": "Разведите двух жёлтых куриц",
    "Colors of Spring": "Краски весны",
    "Find all 3 new Spring flowers": "Найдите все 3 новых весенних цветка",
    "A Tisket, A Tasket...": "Корзинка найдётся...",
    "Find an Easter Basket": "Найдите пасхальную корзину",
    "A Gift From The Past": "Подарок из прошлого",
    "Find an old Easter Card in a chest somewhere.": "Найдите в одном из сундуков старую пасхальную открытку.",
    "Egg-celent Taste": "Яйц-ключительный вкус",
    "Collect all 4 colored egg drops from the Yellow Chickens": "Соберите яйца всех 4 цветов, выпадающие из жёлтых куриц",
    "Egg-Hunger, Extraordinaire!": "Яичный голод — высший класс!",
    "Find all the different types of Easter Eggs!": "Найдите все разновидности пасхальных яиц!",
    "Find all the Two-Colored Eggs": "Найдите все двухцветные яйца",
    "Find all the Flowered Eggs": "Найдите все яйца с цветочным узором",
    "Find all the Dotted Eggs": "Найдите все яйца в горошек",
    "Find the Pastel Rainbow Egg": "Найдите пастельное радужное яйцо",
    "Find all the Striped Eggs": "Найдите все полосатые яйца",
    "Find all the Chevron Eggs": "Найдите все яйца с узором «шеврон»",
    "Description": "Соберите яйца этого вида",
    "It's So Fluffy!": "Какой пушистый!",
    "Find a Pet Bunny in an Easter Basket and make it your pet.": "Найдите ручного кролика в пасхальной корзине и приручите его.",
    "Nice Buns You've Got There!": "Отличные кролики!",
    "Tame all 5 colors of Bunny Pets.": "Приручите кроликов всех 5 окрасов.",
    "Easter": "Пасха",
    "Unlock the Easter Advancements Tab": "Откройте вкладку пасхальных достижений",
    "Bride Costume": "Костюм невесты",
    "Find all the pieces to the Bride Costume (Diamond Tier)": "Найдите все части костюма невесты (алмазный уровень)",
    "Frankenstein Costume": "Костюм Франкенштейна",
    "Find all the pieces to the Frankenstein Costume (Diamond Tier)": "Найдите все части костюма Франкенштейна (алмазный уровень)",
    "Mermaid Costume": "Костюм русалки",
    "Find all the pieces to the Mermaid Costume (Diamond Tier)": "Найдите все части костюма русалки (алмазный уровень)",
    "Merman Costume": "Костюм водяного",
    "Find all the pieces to the Merman Costume (Diamond Tier)": "Найдите все части костюма водяного (алмазный уровень)",
    "Mummy Costume": "Костюм мумии",
    "Find all the pieces to the Mummy Costume (Diamond Tier)": "Найдите все части костюма мумии (алмазный уровень)",
    "Pirate Costume": "Костюм пирата",
    "Find all the pieces to the Pirate Costume (Diamond Tier)": "Найдите все части костюма пирата (алмазный уровень)",
    "I See Dead People": "Я вижу мёртвых",
    "Replace a Gravestone. You are 99% sure it isn't haunted.": "Замените надгробие. Вы на 99% уверены, что оно не проклято.",
    "Frightfully Fashionable": "Ужасно модный",
    "Collect all the Halloween Costumes! (Diamond Tier)": "Соберите все костюмы для Хэллоуина! (алмазный уровень)",
    "Give Me Something Good to Eat!": "Дайте чего-нибудь вкусного!",
    "Sample all of the Halloween Treats": "Попробуйте все угощения для Хэллоуина",
    "Make Some Noise!": "Пошумим!",
    "Find a Noisemaker inside a Trick-or-Treat bag.": "Найдите трещотку в мешочке «Сладость или гадость».",
    "Halloween": "Хэллоуин",
    "Unlock the Halloween Achievements Tab": "Откройте вкладку достижений Хэллоуина",
    "Trick or Treat!": "Сладость или гадость!",
    "Collect a Trick-or-Treat bag from a Costumed Monster.": "Получите мешочек «Сладость или гадость» от монстра в костюме.",
    "Take A Pitcher, It'll Last Longer!": "Берите кувшин — его хватит надолго!",
    "Drink Green Beer until you can't see straight.": "Пейте зелёное пиво, пока всё перед глазами не поплывёт.",
    "Fields of Clover": "Клеверные поля",
    "Walk through a patch of clover.": "Пройдите через заросли клевера.",
    "Getting Lucky!": "Повезло!",
    "Find and use a Four Leaf Clover to bring yourself good luck.": "Найдите и используйте четырёхлистный клевер, чтобы привлечь удачу.",
    "St. Patrick's Day": "День святого Патрика",
    "Unlock the St. Patrick's Day Achievements Tab": "Откройте вкладку достижений ко Дню святого Патрика",
}


def find_jar() -> Path:
    for path in sorted((ROOT / "server/mods").glob("*.jar")):
        try:
            with zipfile.ZipFile(path) as archive:
                if "assets/maidensmerrymaking/lang/en_us.json" in archive.namelist():
                    return path
        except zipfile.BadZipFile:
            continue
    raise SystemExit("Maiden's Merrymaking jar not found in server/mods")


def translated_component(component: object, context: str) -> None:
    if not isinstance(component, dict) or "text" not in component:
        return
    english = component["text"]
    if english not in TRANSLATIONS:
        raise SystemExit(f"Missing translation for {english!r} in {context}")
    component["text"] = TRANSLATIONS[english]


def main() -> None:
    prefix = "data/maidensmerrymaking/advancements/"
    count = 0
    with zipfile.ZipFile(find_jar()) as archive:
        for name in sorted(archive.namelist()):
            if not name.startswith(prefix) or not name.endswith(".json"):
                continue
            data = json.loads(archive.read(name))
            display = data.get("display")
            if not isinstance(display, dict):
                continue
            translated_component(display.get("title"), name)
            translated_component(display.get("description"), name)
            relative = Path(name.removeprefix(prefix))
            destination = OUTPUT / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(
                json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            count += 1
    print(f"Wrote {count} translated advancements to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

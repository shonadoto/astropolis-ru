#!/usr/bin/env python3
"""Import unambiguous Russian strings from newer official mod revisions.

The Astropolis jars are old enough that some bundled Russian files lag behind
their English files.  This tool only imports an official translation when the
key still exists, or when the exact English value maps to exactly one Russian
value in the pinned upstream revision.
"""

from __future__ import annotations

import json
import re
import urllib.request
import zipfile
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "overrides/kubejs/assets"
PLACEHOLDER_RE = re.compile(r"%(?:\d+\$)?([a-zA-Z%])")

SOURCES = {
    "fancymenu": {
        "commit": "34c623142e03fc751be9ce67c206c33d2546d1a0",
        "repo": "Keksuccino/FancyMenu",
        "en": "common/src/main/resources/assets/fancymenu/lang/en_us.json",
        "ru": "common/src/main/resources/assets/fancymenu/lang/ru_ru.json",
    },
    "quark": {
        "commit": "33bb3db8c6dafbc00bc782d41bdd294fc85d0dcf",
        "repo": "VazkiiMods/Quark",
        "en": "src/main/resources/assets/quark/lang/en_us.json",
        "ru": "src/main/resources/assets/quark/lang/ru_ru.json",
    },
    "ae2": {
        "commit": "32a748f00ccfd0c54f4e5c7b4ecd1a712eccbc34",
        "repo": "AppliedEnergistics/Applied-Energistics-2",
        "en": "src/generated/resources/assets/ae2/lang/en_us.json",
        "ru": "src/main/resources/assets/ae2/lang/ru_ru.json",
    },
    "ftbchunks": {
        "commit": "cae1dc98b6386805ca7c6f29f7951173b1a3b35b",
        "repo": "FTBTeam/FTB-Chunks",
        "en": "common/src/main/resources/assets/ftbchunks/lang/en_us.json",
        "ru": "common/src/main/resources/assets/ftbchunks/lang/ru_ru.json",
    },
    "ftbquests": {
        "commit": "8d2f978559099300ea486c1596dda8c88bdc6e62",
        "repo": "FTBTeam/FTB-Quests",
        "en": "common/src/main/resources/assets/ftbquests/lang/en_us.json",
        "ru": "common/src/main/resources/assets/ftbquests/lang/ru_ru.json",
    },
    "jade": {
        "commit": "ce70ec223b32dbc898d86ae501ece2ca0ff8dafd",
        "repo": "Snownee/Jade",
        "en": "src/main/resources/assets/jade/lang/en_us.json",
        "ru": "src/main/resources/assets/jade/lang/ru_ru.json",
    },
    "immersiveengineering": {
        "commit": "a9c6b6dfffde1460ccb76033e2c6942ee5a342aa",
        "repo": "BluSunrize/ImmersiveEngineering",
        "en": "src/main/resources/assets/immersiveengineering/lang/en_us.json",
        "ru": "src/main/resources/assets/immersiveengineering/lang/ru_ru.json",
    },
    "supplementaries": {
        "commit": "fb7073e114a8a94f166c28098b840b40d81d510f",
        "repo": "MehVahdJukaar/Supplementaries",
        "en": "src/main/resources/assets/supplementaries/lang/en_us.json",
        "ru": "src/main/resources/assets/supplementaries/lang/ru_ru.json",
    },
    "sophisticatedcore": {
        "commit": "aadb8a2483ace15a5b62d9f793c8523834615b42",
        "repo": "P3pp3rF1y/SophisticatedCore",
        "en": "src/main/resources/assets/sophisticatedcore/lang/en_us.json",
        "ru": "src/main/resources/assets/sophisticatedcore/lang/ru_ru.json",
    },
    "nochatreports": {
        "commit": "86c5bb74e15867d0dfa555a8b5374879c4ae787b",
        "repo": "Aizistral-Studios/No-Chat-Reports",
        "en": "src/main/resources/assets/nochatreports/lang/en_us.json",
        "ru": "src/main/resources/assets/nochatreports/lang/ru_ru.json",
    },
    "blockcarpentry": {
        "commit": "4fc95c67e0d4922b389662901b0eb392d71df751",
        "repo": "PianoManu/BlockCarpentry",
        "en": "src/main/resources/assets/blockcarpentry/lang/en_us.json",
        "ru": "src/main/resources/assets/blockcarpentry/lang/ru_ru.json",
    },
    "creativecore": {
        "commit": "2c4be4546e55b09ffc744f22913b188100539083",
        "repo": "CreativeMD/CreativeCore",
        "en": "src/main/resources/assets/creativecore/lang/en_us.json",
        "ru": "src/main/resources/assets/creativecore/lang/ru_ru.json",
    },
    "extendedcrafting": {
        "commit": "59f8a2c649c72e1f4482603f0336837932ff9698",
        "repo": "BlakeBr0/ExtendedCrafting",
        "en": "src/main/resources/assets/extendedcrafting/lang/en_us.json",
        "ru": "src/main/resources/assets/extendedcrafting/lang/ru_ru.json",
    },
}


def fetch_json(repo: str, commit: str, path: str) -> dict[str, str]:
    url = f"https://raw.githubusercontent.com/{repo}/{commit}/{path}"
    with urllib.request.urlopen(url) as response:
        value = json.loads(response.read().decode("utf-8-sig"))
    if not isinstance(value, dict):
        raise SystemExit(f"Expected an object at {url}")
    return value


def find_jar(namespace: str) -> Path:
    wanted = f"assets/{namespace}/lang/en_us.json"
    for path in sorted((ROOT / "server/mods").glob("*.jar")):
        try:
            with zipfile.ZipFile(path) as archive:
                if wanted in archive.namelist():
                    return path
        except zipfile.BadZipFile:
            continue
    raise SystemExit(f"Jar for {namespace} not found")


def read_pack(namespace: str) -> dict[str, str]:
    path = ASSETS / namespace / "lang/ru_ru.json"
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else {}


def conversion_types(value: object) -> Counter[str]:
    if not isinstance(value, str):
        return Counter()
    return Counter(PLACEHOLDER_RE.findall(value))


def main() -> None:
    for namespace, source in SOURCES.items():
        source_en = fetch_json(source["repo"], source["commit"], source["en"])
        source_ru = fetch_json(source["repo"], source["commit"], source["ru"])
        by_english: dict[str, set[str]] = defaultdict(set)
        for key, english in source_en.items():
            if key in source_ru and isinstance(english, str) and isinstance(source_ru[key], str):
                by_english[english].add(source_ru[key])

        with zipfile.ZipFile(find_jar(namespace)) as archive:
            names = set(archive.namelist())
            english = json.loads(archive.read(f"assets/{namespace}/lang/en_us.json"))
            built_in_path = f"assets/{namespace}/lang/ru_ru.json"
            built_in = json.loads(archive.read(built_in_path)) if built_in_path in names else {}

        custom = read_pack(namespace)
        missing = set(english) - set(built_in) - set(custom)
        imported: dict[str, str] = {}
        skipped_placeholders = 0
        for key in sorted(missing):
            candidate = source_ru.get(key)
            if candidate is None:
                candidates = by_english.get(english[key], set())
                candidate = next(iter(candidates)) if len(candidates) == 1 else None
            if not isinstance(candidate, str):
                continue
            if conversion_types(english[key]) != conversion_types(candidate):
                skipped_placeholders += 1
                continue
            imported[key] = candidate

        custom.update(imported)
        output = ASSETS / namespace / "lang/ru_ru.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(custom, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(
            f"{namespace}: imported {len(imported)} official strings, "
            f"skipped {skipped_placeholders} placeholder mismatch(es)"
        )


if __name__ == "__main__":
    main()

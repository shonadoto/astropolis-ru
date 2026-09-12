#!/usr/bin/env python3
"""Audit complete Russian localization coverage in the installed mod set."""

from __future__ import annotations

import csv
import json
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MODS_DIR = ROOT / "server" / "mods"
QUESTS_DIR = ROOT / "overrides" / "config" / "ftbquests" / "quests"
PACK_ASSETS = ROOT / "overrides" / "kubejs" / "assets"
OUTPUT = ROOT / "translation" / "mod_inventory.tsv"

REGISTRY_ID_RE = re.compile(r'(?<![\w.-])([a-z0-9_.-]+):([a-z0-9_./-]+)')
MOD_ID_RE = re.compile(r'^\s*modId\s*=\s*["\']([^"\']+)', re.MULTILINE)
DISPLAY_NAME_RE = re.compile(r'^\s*displayName\s*=\s*["\']([^"\']+)', re.MULTILINE)
CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
LATIN_WORD_RE = re.compile(r"\b[A-Za-z]{3,}\b")


def read_json(raw: bytes) -> dict[str, str]:
    try:
        value = json.loads(raw.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def item_block_keys(values: dict[str, str], namespace: str) -> set[str]:
    prefixes = (f"item.{namespace}.", f"block.{namespace}.")
    # Rechiseled 1.19.2 uses the legacy inverse form `rechiseled.block.*`.
    if namespace == "rechiseled":
        prefixes += ("rechiseled.item.", "rechiseled.block.")
    return {key for key in values if key.startswith(prefixes)}


def quest_references() -> tuple[Counter[str], dict[str, set[str]]]:
    counts: Counter[str] = Counter()
    ids: dict[str, set[str]] = defaultdict(set)
    for path in QUESTS_DIR.rglob("*.snbt"):
        text = path.read_text(encoding="utf-8")
        for namespace, registry_path in REGISTRY_ID_RE.findall(text):
            counts[namespace] += 1
            ids[namespace].add(f"{namespace}:{registry_path}")
    return counts, ids


def pack_ru(namespace: str) -> dict[str, str]:
    path = PACK_ASSETS / namespace / "lang" / "ru_ru.json"
    if not path.exists():
        return {}
    return read_json(path.read_bytes())


def main() -> None:
    if not MODS_DIR.is_dir():
        raise SystemExit(f"Installed mods not found: {MODS_DIR}")

    quest_counts, quest_ids = quest_references()
    rows: list[dict[str, str | int]] = []

    for jar in sorted(MODS_DIR.glob("*.jar")):
        try:
            with zipfile.ZipFile(jar) as archive:
                names = set(archive.namelist())
                metadata = ""
                if "META-INF/mods.toml" in names:
                    metadata = archive.read("META-INF/mods.toml").decode("utf-8", "replace")
                mod_ids = MOD_ID_RE.findall(metadata)
                display_names = DISPLAY_NAME_RE.findall(metadata)
                fallback_name = display_names[0] if display_names else (mod_ids[0] if mod_ids else jar.stem)

                namespaces = sorted({
                    name.split("/", 2)[1]
                    for name in names
                    if name.startswith("assets/") and name.endswith("/lang/en_us.json")
                })
                for namespace in namespaces:
                    en_path = f"assets/{namespace}/lang/en_us.json"
                    ru_path = f"assets/{namespace}/lang/ru_ru.json"
                    en = read_json(archive.read(en_path))
                    upstream_ru = read_json(archive.read(ru_path)) if ru_path in names else {}
                    custom_ru = pack_ru(namespace)
                    en_keys = item_block_keys(en, namespace)
                    upstream_keys = item_block_keys(upstream_ru, namespace)
                    custom_keys = item_block_keys(custom_ru, namespace)
                    covered_item_blocks = upstream_keys | custom_keys
                    missing_item_blocks = en_keys - covered_item_blocks
                    merged_ru = {**upstream_ru, **custom_ru}
                    covered_all = set(merged_ru)
                    missing_all = set(en) - covered_all
                    equal_item_blocks = {
                        key for key in en_keys & upstream_keys
                        if isinstance(en.get(key), str)
                        and en.get(key) == upstream_ru.get(key)
                    }
                    equal_all = {
                        key for key in set(en) & covered_all
                        if isinstance(en.get(key), str)
                        and en.get(key) == merged_ru.get(key)
                    }
                    mixed = {
                        key for key, value in merged_ru.items()
                        if key in en
                        and isinstance(value, str)
                        and CYRILLIC_RE.search(value)
                        and LATIN_WORD_RE.search(value)
                    }
                    refs = quest_ids.get(namespace, set())
                    quest_missing = {
                        registry_id for registry_id in refs
                        if not any(
                            key in covered_item_blocks
                            for key in ((
                                f"item.{namespace}.{registry_id.split(':', 1)[1].replace('/', '.')}",
                                f"block.{namespace}.{registry_id.split(':', 1)[1].replace('/', '.')}",
                            ) + ((
                                f"rechiseled.item.{registry_id.split(':', 1)[1].replace('/', '.')}",
                                f"rechiseled.block.{registry_id.split(':', 1)[1].replace('/', '.')}",
                            ) if namespace == "rechiseled" else ()))
                        )
                    }
                    if quest_missing:
                        priority = "P0"
                    elif missing_all and refs:
                        priority = "P1"
                    elif missing_all:
                        priority = "P2"
                    elif mixed:
                        priority = "REVIEW"
                    else:
                        priority = "DONE"
                    rows.append({
                        "priority": priority,
                        "namespace": namespace,
                        "mod_name": fallback_name,
                        "jar": jar.name,
                        "quest_refs": quest_counts.get(namespace, 0),
                        "quest_ids": len(refs),
                        "quest_ids_without_ru": len(quest_missing),
                        "en_item_block_keys": len(en_keys),
                        "upstream_ru_keys": len(upstream_keys),
                        "pack_ru_keys": len(custom_keys),
                        "missing_ru_keys": len(missing_item_blocks),
                        "upstream_equal_to_en": len(equal_item_blocks),
                        "en_all_keys": len(en),
                        "covered_all_keys": len(set(en) & covered_all),
                        "missing_all_keys": len(missing_all),
                        "equal_to_en_all": len(equal_all),
                        "mixed_ru_en": len(mixed),
                    })
        except zipfile.BadZipFile:
            continue

    order = {"P0": 0, "P1": 1, "P2": 2, "REVIEW": 3, "DONE": 4}
    rows.sort(key=lambda row: (order[str(row["priority"])], -int(row["quest_refs"]), str(row["namespace"])))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0]) if rows else []
    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, dialect="excel-tab", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    totals = Counter(str(row["priority"]) for row in rows)
    print(f"Wrote {OUTPUT}")
    print("Namespaces: " + ", ".join(f"{key}={totals[key]}" for key in ("P0", "P1", "P2", "REVIEW", "DONE")))
    print(f"Missing item/block keys: {sum(int(row['missing_ru_keys']) for row in rows)}")
    all_keys = sum(int(row["en_all_keys"]) for row in rows)
    missing_all = sum(int(row["missing_all_keys"]) for row in rows)
    print(f"All language keys: {all_keys - missing_all}/{all_keys} covered ({missing_all} missing)")
    print(f"Covered strings equal to English: {sum(int(row['equal_to_en_all']) for row in rows)}")
    print(f"Mixed Cyrillic/Latin strings to review: {sum(int(row['mixed_ru_en']) for row in rows)}")


if __name__ == "__main__":
    main()

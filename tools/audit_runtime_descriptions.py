#!/usr/bin/env python3
"""Compare live Minecraft description IDs from the diagnostic log with lang keys."""

from __future__ import annotations

import json
import re
import zipfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "server" / "logs" / "latest.log"
LINE_RE = re.compile(r"\[translation-audit\] (item|block)\t([^\t]+)\t(\S+)")


def read_json(raw: bytes) -> dict[str, str]:
    try:
        value = json.loads(raw.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def main() -> None:
    if not LOG.exists():
        raise SystemExit(f"Runtime log not found: {LOG}")
    descriptions: dict[tuple[str, str], str] = {}
    for line in LOG.read_text(encoding="utf-8", errors="replace").splitlines():
        match = LINE_RE.search(line)
        if match:
            descriptions[(match.group(1), match.group(2))] = match.group(3)
    if not descriptions:
        raise SystemExit("No [translation-audit] description dump found in the current server log")

    language_keys: set[str] = set()
    for jar in (ROOT / "mods").glob("*.jar"):
        try:
            with zipfile.ZipFile(jar) as archive:
                for name in archive.namelist():
                    if "/lang/" in name and name.endswith(".json"):
                        language_keys.update(read_json(archive.read(name)))
        except zipfile.BadZipFile:
            continue
    for path in (ROOT / "overrides" / "kubejs" / "assets").glob("*/lang/ru_ru.json"):
        language_keys.update(read_json(path.read_bytes()))

    missing = sorted(
        (kind, registry_id, description)
        for (kind, registry_id), description in descriptions.items()
        if registry_id.split(":", 1)[0] != "minecraft" and description not in language_keys
    )
    namespaces = Counter(registry_id.split(":", 1)[0] for _, registry_id, _ in missing)
    print(f"Runtime descriptions checked: {len(descriptions)}")
    print(f"Missing non-vanilla description occurrences: {len(missing)}")
    print(f"Missing unique keys: {len({description for _, _, description in missing})}")
    if namespaces:
        print("By namespace: " + ", ".join(f"{key}={value}" for key, value in namespaces.most_common()))
        for kind, registry_id, description in missing:
            print(f"{kind}\t{registry_id}\t{description}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

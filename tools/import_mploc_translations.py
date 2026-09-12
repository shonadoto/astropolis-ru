#!/usr/bin/env python3
"""Import exact-key Russian translations from the pinned MPLOCmods release."""

from __future__ import annotations

import hashlib
import json
import re
import urllib.request
import zipfile
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "downloads/MPLOCmods_v40.1.zip"
URL = "https://cdn.modrinth.com/data/xeqX6g8g/versions/EBQQC2KB/MPLOCmods_v40.1.zip"
SHA256 = "3e604621a6c9356fb2e676d7b8038cb07c8abdd430abdfe1eccc9afae99dcb90"
PLACEHOLDER_RE = re.compile(r"%(?:\d+\$)?([a-zA-Z%])")


def ensure_archive() -> None:
    if not ARCHIVE.exists() or hashlib.sha256(ARCHIVE.read_bytes()).hexdigest() != SHA256:
        ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(URL) as response:
            payload = response.read()
        if hashlib.sha256(payload).hexdigest() != SHA256:
            raise SystemExit("Unexpected MPLOCmods archive checksum")
        ARCHIVE.write_bytes(payload)


def placeholders(value: object) -> Counter[str]:
    return Counter(PLACEHOLDER_RE.findall(value)) if isinstance(value, str) else Counter()


def installed_languages() -> dict[str, tuple[dict[str, str], dict[str, str]]]:
    result: dict[str, tuple[dict[str, str], dict[str, str]]] = defaultdict(lambda: ({}, {}))
    for jar in sorted((ROOT / "server/mods").glob("*.jar")):
        try:
            with zipfile.ZipFile(jar) as archive:
                names = set(archive.namelist())
                for name in names:
                    if not name.startswith("assets/") or not name.endswith("/lang/en_us.json"):
                        continue
                    namespace = name.split("/")[1]
                    english, russian = result[namespace]
                    english.update(json.loads(archive.read(name).decode("utf-8-sig")))
                    ru_name = f"assets/{namespace}/lang/ru_ru.json"
                    if ru_name in names:
                        russian.update(json.loads(archive.read(ru_name).decode("utf-8-sig")))
        except (zipfile.BadZipFile, json.JSONDecodeError, UnicodeDecodeError):
            continue
    return result


def main() -> None:
    ensure_archive()
    total = 0
    skipped = 0
    with zipfile.ZipFile(ARCHIVE) as mploc:
        available = set(mploc.namelist())
        for namespace, (english, built_in) in sorted(installed_languages().items()):
            source_name = f"assets/{namespace}/lang/ru_ru.json"
            if source_name not in available:
                continue
            source = json.loads(mploc.read(source_name).decode("utf-8-sig"))
            output = ROOT / f"overrides/kubejs/assets/{namespace}/lang/ru_ru.json"
            custom = json.loads(output.read_text(encoding="utf-8-sig")) if output.exists() else {}
            imported = {}
            missing = set(english) - set(built_in) - set(custom)
            untranslated_built_in = {
                key
                for key in set(english) & set(built_in) - set(custom)
                if built_in[key] == english[key]
            }
            for key in sorted(missing | untranslated_built_in):
                candidate = source.get(key)
                if not isinstance(candidate, str):
                    continue
                if candidate == english[key]:
                    continue
                if placeholders(english[key]) != placeholders(candidate):
                    skipped += 1
                    continue
                imported[key] = candidate
            if imported:
                custom.update(imported)
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(
                    json.dumps(custom, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                print(f"{namespace}: imported {len(imported)} MPLOCmods strings")
                total += len(imported)
    print(f"Imported {total} strings; skipped {skipped} placeholder mismatch(es)")


if __name__ == "__main__":
    main()

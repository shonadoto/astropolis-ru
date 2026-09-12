#!/usr/bin/env python3
"""Apply reviewed translations from translation/quest_strings.tsv."""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "overrides/config/ftbquests/quests"
CATALOGUE = ROOT / "translation/quest_strings.tsv"


def escape_snbt(value: str) -> str:
    return value.replace("\\", r"\\").replace('"', r'\"')


def main() -> None:
    with CATALOGUE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))

    pending = [row for row in rows if row["status"] != "reviewed"]
    if pending:
        raise SystemExit(f"Refusing to apply: {len(pending)} strings are not reviewed")

    mapping = {escape_snbt(row["english"]): escape_snbt(row["russian"]) for row in rows}
    changed = 0
    for path in sorted(QUESTS.rglob("*.snbt")):
        relative = str(path.relative_to(ROOT))
        raw = subprocess.run(
            ["git", "show", f"HEAD:{relative}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        has_bom = raw.startswith(b"\xef\xbb\xbf")
        source = raw.decode("utf-8-sig")
        translated = source
        for english, russian in mapping.items():
            translated = translated.replace(f'"{english}"', f'"{russian}"')
        if translated != source:
            encoded = translated.encode("utf-8")
            path.write_bytes((b"\xef\xbb\xbf" if has_bom else b"") + encoded)
            changed += 1
    print(f"Updated {changed} quest files")


if __name__ == "__main__":
    main()

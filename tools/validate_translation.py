#!/usr/bin/env python3
"""Structural and editorial checks for the Astropolis Russian quest book."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "overrides/config/ftbquests/quests"
DISPLAY_FIELD = re.compile(r"\b(?:title|subtitle|description)\s*:")
DISPLAY_VALUE = re.compile(
    r'(\b(?:title|subtitle)\s*:)\s*"(?:\\.|[^"\\])*"'
    r'|(\bdescription\s*:)\s*\[(?:[^\]"\\]|"(?:\\.|[^"\\])*")*\]',
    re.S,
)
CYRILLIC = re.compile(r"[А-Яа-яЁё]")
ENGLISH_WORD = re.compile(r"\b(?:used|made|create|crafted|collected|stores?|allows?|requires?|welcome|quest|from|with|into|inside|when|can|will|the|and|your|you)\b", re.I)


def main() -> None:
    failures: list[str] = []
    warnings: list[str] = []

    # Translation must never alter quest topology or registry references.
    def without_display_text(text: str) -> str:
        return DISPLAY_VALUE.sub(lambda m: f"{m.group(1) or m.group(2)} <DISPLAY_TEXT>", text).replace("\r\n", "\n")

    for path in sorted(QUESTS.rglob("*.snbt")):
        relative = str(path.relative_to(ROOT))
        original = subprocess.run(
            ["git", "show", f"HEAD:{relative}"], cwd=ROOT, check=True, capture_output=True
        ).stdout.decode("utf-8-sig")
        current = path.read_bytes().decode("utf-8-sig")
        if without_display_text(original) != without_display_text(current):
            failures.append(f"Non-text quest change: {relative}")

    for path in sorted(QUESTS.rglob("*.snbt")):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if DISPLAY_FIELD.search(line) and ENGLISH_WORD.search(line):
                warnings.append(f"Possible English at {path.relative_to(ROOT)}:{line_no}: {line.strip()}")
            if DISPLAY_FIELD.search(line) and '"' in line and not CYRILLIC.search(line):
                # Proper names and formatting-only values are expected; keep this visible for review.
                warnings.append(f"No Cyrillic at {path.relative_to(ROOT)}:{line_no}: {line.strip()}")

    if warnings:
        print("WARNINGS")
        print("\n".join(dict.fromkeys(warnings)))
    if failures:
        print("FAILURES")
        print("\n".join(failures))
        raise SystemExit(1)
    print(f"Validation passed with {len(warnings)} review warning(s)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Create a reviewable EN -> RU catalogue for Astropolis FTB Quests.

This is deliberately a drafting tool.  It never edits quest files.  The reviewed
catalogue is applied by apply_quest_translation.py.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

import ctranslate2
import sentencepiece as spm


ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "overrides/config/ftbquests/quests"
MODEL = ROOT / ".tools/argos-model/translate-en_ru-1_9"
OUTPUT = ROOT / "translation/quest_strings.tsv"

# Terms whose pack-specific meaning must not be guessed by a generic model.
GLOSSARY = {
    "Space Mart": "Космомаркет",
    "B Bucks": "B-баксы",
    "Immersive Engineering": "Immersive Engineering",
    "Applied Energistics 2": "Applied Energistics 2",
    "Mekanism": "Mekanism",
    "FTB Quests": "FTB Quests",
    "FTB Ultimine": "FTB Ultimine",
    "Astropolis": "Astropolis",
}

STRING_RE = re.compile(r'"((?:\\.|[^"\\])*)"')
FIELD_VALUE_RE = re.compile(
    r'\b(?:title|subtitle)\s*:\s*("(?:\\.|[^"\\])*")'
    r'|\bdescription\s*:\s*(\[(?:[^\]"\\]|"(?:\\.|[^"\\])*")*\])',
    re.S,
)
PROTECTED_RE = re.compile(r"https?://\S+|/[a-zA-Z][a-zA-Z0-9_:-]*(?:\s+[^\s,\]\"]+)*|&[0-9a-fk-or]", re.I)


def unescape_snbt(value: str) -> str:
    return value.replace(r"\"", '"').replace(r"\\", "\\")


def protect(text: str) -> tuple[str, dict[str, str]]:
    replacements: dict[str, str] = {}

    def stash(value: str) -> str:
        key = f"ZXQ{len(replacements)}QXZ"
        replacements[key] = value
        return key

    text = PROTECTED_RE.sub(lambda m: stash(m.group(0)), text)
    for english, russian in sorted(GLOSSARY.items(), key=lambda pair: -len(pair[0])):
        text = re.sub(re.escape(english), lambda _m: stash(russian), text)
    return text, replacements


def restore(text: str, replacements: dict[str, str]) -> str:
    # SentencePiece sometimes inserts spaces inside an unknown placeholder.
    compact = re.sub(r"Z\s*X\s*Q\s*(\d+)\s*Q\s*X\s*[ZX]", r"ZXQ\1QXZ", text, flags=re.I)
    for key, value in replacements.items():
        compact = compact.replace(key, value).replace(key.lower(), value)
    return compact.strip()


def collect() -> list[tuple[str, int, str]]:
    rows: list[tuple[str, int, str]] = []
    seen: set[str] = set()
    for path in sorted(QUESTS.rglob("*.snbt")):
        text = path.read_text(encoding="utf-8-sig")
        for field in FIELD_VALUE_RE.finditer(text):
            line_no = text.count("\n", 0, field.start()) + 1
            value_source = field.group(1) or field.group(2)
            for match in STRING_RE.finditer(value_source):
                value = unescape_snbt(match.group(1))
                if value and value not in seen:
                    seen.add(value)
                    rows.append((str(path.relative_to(ROOT)), line_no, value))
    return rows


def main() -> None:
    rows = collect()
    sp = spm.SentencePieceProcessor(model_file=str(MODEL / "sentencepiece.model"))
    translator = ctranslate2.Translator(str(MODEL / "model"), device="cpu")

    prepared: list[str] = []
    replacement_sets: list[dict[str, str]] = []
    for _, _, source in rows:
        text, replacements = protect(source)
        prepared.append(text)
        replacement_sets.append(replacements)

    token_batches = [sp.encode(text, out_type=str) for text in prepared]
    results = translator.translate_batch(token_batches, beam_size=4, max_batch_size=32)
    drafts = [
        restore(sp.decode(result.hypotheses[0]), replacements)
        for result, replacements in zip(results, replacement_sets, strict=True)
    ]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("file", "line", "english", "russian", "status"))
        for (path, line_no, source), draft in zip(rows, drafts, strict=True):
            writer.writerow((path, line_no, source, draft, "draft"))
    print(f"Wrote {len(rows)} unique strings to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the client-side Astropolis RU language resource pack."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "overrides" / "kubejs" / "assets"
OUTPUT = ROOT / "dist" / "Astropolis-RU-ResourcePack-2.2-ru.1.zip"


def zip_info(name: str) -> ZipInfo:
    info = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    return info


def main() -> None:
    language_files = sorted(
        path for path in ASSETS.rglob("ru_ru.json") if path.parent.name == "lang"
    )
    if not language_files:
        raise SystemExit("No ru_ru.json language files found")

    for path in language_files:
        json.loads(path.read_text(encoding="utf-8"))

    pack_meta = {
        "pack": {
            "pack_format": 9,
            "description": "Astropolis RU — русский перевод",
        }
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUTPUT, "w") as archive:
        archive.writestr(
            zip_info("pack.mcmeta"),
            json.dumps(pack_meta, ensure_ascii=False, indent=2).encode("utf-8") + b"\n",
        )
        for path in language_files:
            archive.writestr(
                zip_info((Path("assets") / path.relative_to(ASSETS)).as_posix()),
                path.read_bytes(),
            )

    digest = hashlib.sha1(OUTPUT.read_bytes()).hexdigest()
    print(f"Built {OUTPUT}")
    print(f"SHA-1 {digest}")


if __name__ == "__main__":
    main()

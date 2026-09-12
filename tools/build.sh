#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dist_dir="$root_dir/dist"
archive="$dist_dir/Astropolis-RU-2.2-ru.1.zip"

mkdir -p "$dist_dir"
python3 "$root_dir/tools/validate_translation.py"

cd "$root_dir"
zip -q -r "$archive" manifest.json modlist.html overrides
unzip -tq "$archive"
printf 'Built %s\n' "$archive"

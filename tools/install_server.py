#!/usr/bin/env python3
"""Install the Astropolis dedicated server from the CurseForge manifest."""

from __future__ import annotations

import concurrent.futures
import json
import os
import shutil
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"
MOD_CACHE = ROOT / "mods"
DOWNLOADS = ROOT / "downloads"
RUNTIME = ROOT / "runtime"
SERVER = Path(os.environ.get("ASTROPOLIS_SERVER_DIR", ROOT / "server")).resolve()
WORKERS = int(os.environ.get("DOWNLOAD_WORKERS", "8"))
SERVER_EXCLUDE = ROOT / "server-exclude.txt"


def run(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True)


def valid_zip(path: Path) -> bool:
    try:
        with zipfile.ZipFile(path) as archive:
            return archive.testzip() is None
    except (OSError, zipfile.BadZipFile):
        return False


def java_major(java: Path) -> int | None:
    try:
        result = subprocess.run(
            [str(java), "-version"], capture_output=True, text=True, check=False
        )
        first = (result.stderr or result.stdout).splitlines()[0]
        version = first.split('"')[1]
        return int(version.split(".")[0])
    except (IndexError, OSError, ValueError):
        return None


def find_java() -> Path | None:
    configured = os.environ.get("JAVA_BIN")
    candidates: list[Path] = []
    if configured:
        candidates.append(Path(configured).expanduser())
    system_java = shutil.which("java")
    if system_java:
        candidates.append(Path(system_java))
    candidates.extend(sorted(RUNTIME.glob("*/bin/java"), reverse=True))
    for candidate in candidates:
        if candidate.is_file() and os.access(candidate, os.X_OK) and java_major(candidate) == 17:
            return candidate.resolve()
    return None


def install_java() -> Path:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    archive = DOWNLOADS / "temurin17.tar.gz"
    if not archive.exists():
        print("[install] Downloading Eclipse Temurin Java 17 JRE")
        run(
            "curl",
            "-fL",
            "--retry",
            "5",
            "--retry-all-errors",
            "-o",
            str(archive) + ".part",
            "https://api.adoptium.net/v3/binary/latest/17/ga/linux/x64/jre/hotspot/normal/eclipse",
        )
        Path(str(archive) + ".part").replace(archive)
    try:
        with tarfile.open(archive) as tar:
            tar.extractall(RUNTIME, filter="data")
    except TypeError:  # Python < 3.12
        with tarfile.open(archive) as tar:
            tar.extractall(RUNTIME)
    java = find_java()
    if not java:
        raise RuntimeError("Java 17 was downloaded but could not be found")
    return java


def download_mod(entry: dict[str, object]) -> tuple[str, bool]:
    project = int(entry["projectID"])
    file_id = int(entry["fileID"])
    name = f"{project}-{file_id}.jar"
    target = MOD_CACHE / name
    if valid_zip(target):
        return name, False
    target.unlink(missing_ok=True)
    partial = Path(str(target) + ".part")
    partial.unlink(missing_ok=True)
    url = resolve_mod_url(project, file_id)
    run(
        "curl",
        "-fL",
        "--retry",
        "6",
        "--retry-delay",
        "2",
        "--retry-all-errors",
        "--connect-timeout",
        "20",
        "-sS",
        "-o",
        str(partial),
        url,
    )
    if not valid_zip(partial):
        partial.unlink(missing_ok=True)
        raise RuntimeError(f"downloaded file is not a valid JAR: {name}")
    partial.replace(target)
    return name, True


def curl_json(url: str) -> dict[str, object]:
    result = subprocess.run(
        ["curl", "-fLsS", "--retry", "3", "--max-time", "30", url],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def resolve_mod_url(project: int, file_id: int) -> str:
    """Resolve the immutable ForgeCDN URL, including archived CurseForge files."""
    prefix, suffix = divmod(file_id, 1000)
    metadata_url = f"https://www.curseforge.com/api/v1/mods/{project}/files/{file_id}"
    try:
        metadata = curl_json(metadata_url).get("data")
        if isinstance(metadata, dict) and metadata.get("fileName"):
            filename = quote(str(metadata["fileName"]))
            return f"https://mediafilez.forgecdn.net/files/{prefix}/{suffix}/{filename}"
    except (json.JSONDecodeError, subprocess.CalledProcessError):
        pass

    # CurseForge can remove metadata for an old file while retaining the file on
    # ForgeCDN. The FTB manifest cache preserves that original immutable URL.
    try:
        cached = curl_json(f"https://api.modpacks.ch/public/curseforge/{project}/{file_id}")
        manifest_url = cached.get("manifestUrl")
        if isinstance(manifest_url, str) and manifest_url:
            return manifest_url.replace("https://edge.forgecdn.net/", "https://mediafilez.forgecdn.net/")
    except (json.JSONDecodeError, subprocess.CalledProcessError):
        pass
    return f"https://www.curseforge.com/api/v1/mods/{project}/files/{file_id}/download"


def install_mods(manifest: dict[str, object]) -> None:
    MOD_CACHE.mkdir(parents=True, exist_ok=True)
    entries = manifest["files"]
    assert isinstance(entries, list)
    print(f"[install] Checking {len(entries)} CurseForge mod files")
    downloaded = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(download_mod, entry): entry for entry in entries}
        for index, future in enumerate(concurrent.futures.as_completed(futures), 1):
            name, changed = future.result()
            downloaded += int(changed)
            state = "downloaded" if changed else "cached"
            print(f"[mods {index:03d}/{len(entries):03d}] {state}: {name}", flush=True)
    print(f"[install] Mods ready: {len(entries)} total, {downloaded} downloaded")


def install_forge(java: Path, forge_version: str) -> Path:
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    SERVER.mkdir(parents=True, exist_ok=True)
    installer = DOWNLOADS / f"forge-{forge_version}-installer.jar"
    if not valid_zip(installer):
        installer.unlink(missing_ok=True)
        url = (
            "https://maven.minecraftforge.net/net/minecraftforge/forge/"
            f"{forge_version}/forge-{forge_version}-installer.jar"
        )
        print(f"[install] Downloading Forge {forge_version}")
        run("curl", "-fL", "--retry", "5", "-o", str(installer) + ".part", url)
        partial = Path(str(installer) + ".part")
        if not valid_zip(partial):
            partial.unlink(missing_ok=True)
            raise RuntimeError("Forge installer download is invalid")
        partial.replace(installer)
    args_file = SERVER / "libraries" / "net" / "minecraftforge" / "forge" / forge_version / "unix_args.txt"
    if not args_file.exists():
        print(f"[install] Installing Forge {forge_version}")
        run(str(java), "-jar", str(installer), "--installServer", cwd=SERVER)
    if not args_file.exists():
        raise RuntimeError(f"Forge args file was not created: {args_file}")
    return args_file


def deploy_pack() -> None:
    print(f"[install] Deploying overrides to {SERVER}")
    shutil.copytree(ROOT / "overrides", SERVER, dirs_exist_ok=True)
    mods_dir = SERVER / "mods"
    if mods_dir.is_symlink() and mods_dir.resolve() == MOD_CACHE.resolve():
        mods_dir.unlink()
    elif mods_dir.is_symlink():
        raise RuntimeError(f"Refusing to replace existing symlink {mods_dir}")
    mods_dir.mkdir(parents=True, exist_ok=True)

    excluded = {
        line.split("#", 1)[0].strip()
        for line in SERVER_EXCLUDE.read_text(encoding="utf-8").splitlines()
        if line.split("#", 1)[0].strip()
    }
    for path in mods_dir.iterdir():
        if path.is_symlink() and path.resolve().parent == MOD_CACHE.resolve():
            path.unlink()
    deployed = 0
    for jar in sorted(MOD_CACHE.glob("*.jar")):
        if jar.name in excluded:
            print(f"[install] Server exclusion: {jar.name}")
            continue
        (mods_dir / jar.name).symlink_to(jar)
        deployed += 1
    print(f"[install] Server mod set: {deployed} JAR files ({len(excluded)} excluded)")

    eula = SERVER / "eula.txt"
    eula.write_text(
        "# By running this installer, the server owner accepts the Minecraft EULA.\n"
        "# https://aka.ms/MinecraftEULA\n"
        "eula=true\n",
        encoding="utf-8",
    )
    properties = SERVER / "server.properties"
    if not properties.exists():
        properties.write_text(
            "# Astropolis RU dedicated server\n"
            "allow-flight=true\n"
            "enable-command-block=true\n"
            "enable-rcon=false\n"
            "enforce-secure-profile=true\n"
            "gamemode=survival\n"
            "level-name=world\n"
            "max-players=20\n"
            "motd=Astropolis RU 2.2\n"
            "online-mode=true\n"
            "server-ip=\n"
            "server-port=25565\n"
            "view-distance=10\n"
            "simulation-distance=8\n",
            encoding="utf-8",
        )


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    loader = next(item["id"] for item in manifest["minecraft"]["modLoaders"] if item["primary"])
    if not loader.startswith("forge-"):
        raise RuntimeError(f"unsupported loader: {loader}")
    forge_version = f"{manifest['minecraft']['version']}-{loader.removeprefix('forge-')}"
    java = find_java() or install_java()
    print(f"[install] Java: {java}")
    install_mods(manifest)
    install_forge(java, forge_version)
    deploy_pack()
    (SERVER / ".astropolis-java").write_text(str(java) + "\n", encoding="utf-8")
    (SERVER / ".astropolis-forge").write_text(forge_version + "\n", encoding="utf-8")
    print("[install] Astropolis server installation is ready")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[install] ERROR: {exc}", file=sys.stderr)
        raise

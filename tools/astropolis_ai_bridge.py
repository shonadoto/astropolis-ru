#!/usr/bin/env python3
"""Loopback-only AI bridge for the Astropolis KubeJS /ai command."""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import secrets
import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
HOST = os.environ.get("AI_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.environ.get("AI_BRIDGE_PORT", "8765"))
MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.4-mini")
API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()
API_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
ALLOWED_PLAYERS = {
    name.strip().lower()
    for name in os.environ.get("AI_ALLOWED_PLAYERS", "shonadoto").split(",")
    if name.strip()
}
COOLDOWN = max(1, int(os.environ.get("AI_COOLDOWN_SECONDS", "8")))
MAX_QUESTION = 700
MAX_CONTEXT = 14_000
RESULT_TTL = 300

WORD_RE = re.compile(r"[a-zA-Zа-яА-ЯёЁ0-9_:-]{2,}")
TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"[ \t]+")
SAFE_ID_RE = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")
NUMBER_RE = re.compile(r"^-?(?:\d+(?:\.\d+)?|\.\d+)$")


@dataclass(frozen=True)
class Document:
    source: str
    text: str
    words: frozenset[str]


def words(text: str) -> set[str]:
    return {word.lower() for word in WORD_RE.findall(text)}


def compact_text(text: str) -> str:
    text = html.unescape(TAG_RE.sub(" ", text))
    return "\n".join(
        SPACE_RE.sub(" ", line).strip()
        for line in text.splitlines()
        if line.strip()
    )


def chunk_text(source: str, text: str, limit: int = 3500) -> list[Document]:
    cleaned = compact_text(text)
    chunks: list[Document] = []
    for offset in range(0, len(cleaned), limit):
        chunk = cleaned[offset : offset + limit]
        chunks.append(Document(source, chunk, frozenset(words(chunk))))
    return chunks


def build_documents() -> list[Document]:
    paths: list[Path] = [ROOT / "README.md", ROOT / "manifest.json", ROOT / "modlist.html"]
    patterns = (
        "server/config/ftbquests/quests/**/*.snbt",
        "overrides/config/ftbquests/quests/**/*.snbt",
        "overrides/kubejs/server_scripts/*.js",
        "overrides/kubejs/data/**/*.json",
        "overrides/kubejs/assets/*/lang/ru_ru.json",
        "translation/**/*.tsv",
        "translation/**/*.md",
        "server/kubejs/exported/kubejs-server-export.json",
    )
    for pattern in patterns:
        paths.extend(ROOT.glob(pattern))

    documents: list[Document] = []
    seen: set[str] = set()
    for path in paths:
        if not path.is_file():
            continue
        relative = str(path.relative_to(ROOT))
        # The installed server and source overrides contain the same quests.
        canonical = relative.replace("server/config/", "overrides/config/")
        if canonical in seen:
            continue
        seen.add(canonical)
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        documents.extend(chunk_text(relative, text))
    return documents


DOCUMENTS = build_documents()
HISTORY: dict[str, deque[tuple[str, str]]] = defaultdict(lambda: deque(maxlen=8))
JOBS: dict[str, dict[str, object]] = {}
JOBS_LOCK = threading.Lock()
LAST_REQUEST: dict[str, float] = {}


def retrieve(question: str, limit: int = 7) -> str:
    query_words = words(question)
    if not query_words:
        return ""
    scored: list[tuple[int, Document]] = []
    for document in DOCUMENTS:
        overlap = query_words & document.words
        if not overlap:
            continue
        score = sum(4 if ":" in word or "_" in word else 1 for word in overlap)
        score += min(3, len(overlap))
        scored.append((score, document))
    scored.sort(key=lambda item: item[0], reverse=True)

    output: list[str] = []
    size = 0
    for _, document in scored[:limit]:
        section = f"\n--- {document.source} ---\n{document.text}"
        if size + len(section) > MAX_CONTEXT:
            break
        output.append(section)
        size += len(section)
    return "".join(output)


def is_number(value: str) -> bool:
    return bool(NUMBER_RE.fullmatch(value))


def validate_command(command: str, player: str) -> str | None:
    """Return a normalized, tightly allowlisted command or None."""
    command = command.strip().lstrip("/")
    if not command or len(command) > 180 or any(c in command for c in "\r\n;|&"):
        return None
    parts = command.split()
    root = parts[0].lower()
    target = player.lower()

    if root == "give" and 3 <= len(parts) <= 4:
        if parts[1].lower() != target or not SAFE_ID_RE.fullmatch(parts[2]):
            return None
        if len(parts) == 4 and (not parts[3].isdigit() or not 1 <= int(parts[3]) <= 64):
            return None
    elif root == "effect" and len(parts) >= 3:
        mode = parts[1].lower()
        if parts[2].lower() != target or mode not in {"give", "clear"}:
            return None
        if mode == "give":
            if not 4 <= len(parts) <= 7 or not SAFE_ID_RE.fullmatch(parts[3]):
                return None
            if len(parts) >= 5 and (not parts[4].isdigit() or int(parts[4]) > 3600):
                return None
            if len(parts) >= 6 and (not parts[5].isdigit() or int(parts[5]) > 4):
                return None
        elif len(parts) > 4 or (len(parts) == 4 and not SAFE_ID_RE.fullmatch(parts[3])):
            return None
    elif root == "gamemode" and len(parts) == 3:
        if parts[1].lower() not in {"survival", "creative", "adventure", "spectator"}:
            return None
        if parts[2].lower() != target:
            return None
    elif root == "tp" and len(parts) in {5, 7}:
        if parts[1].lower() != target or not all(is_number(value) for value in parts[2:]):
            return None
    elif root == "clear" and 2 <= len(parts) <= 4:
        if parts[1].lower() != target:
            return None
        if len(parts) >= 3 and not SAFE_ID_RE.fullmatch(parts[2]):
            return None
        if len(parts) == 4 and (not parts[3].isdigit() or int(parts[3]) > 4096):
            return None
    elif root == "kill" and len(parts) == 2:
        if parts[1].lower() != target:
            return None
    elif root == "spawnpoint" and len(parts) in {2, 5, 6}:
        if parts[1].lower() != target or not all(is_number(value) for value in parts[2:5]):
            return None
    elif root == "time" and len(parts) == 3 and parts[1].lower() == "set":
        if parts[2].lower() not in {"day", "night", "noon", "midnight"} and not parts[2].isdigit():
            return None
    elif root == "weather" and 2 <= len(parts) <= 3:
        if parts[1].lower() not in {"clear", "rain", "thunder"}:
            return None
        if len(parts) == 3 and (not parts[2].isdigit() or int(parts[2]) > 1_000_000):
            return None
    elif root == "difficulty" and len(parts) == 2:
        if parts[1].lower() not in {"peaceful", "easy", "normal", "hard"}:
            return None
    elif root == "gamerule" and len(parts) == 3:
        allowed_rules = {"keepinventory", "dodaylightcycle", "doweathercycle", "mobgriefing"}
        if parts[1].lower() not in allowed_rules or parts[2].lower() not in {"true", "false"}:
            return None
    elif root == "setworldspawn" and len(parts) in {1, 4, 5}:
        if not all(is_number(value) for value in parts[1:4]):
            return None
    else:
        return None
    return " ".join(parts)


RESPONSE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "reply": {"type": "string"},
        "commands": {
            "type": "array",
            "maxItems": 3,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "command": {"type": "string"},
                    "reason": {"type": "string"},
                },
                "required": ["command", "reason"],
            },
        },
    },
    "required": ["reply", "commands"],
}


INSTRUCTIONS = """Ты — компактный игровой помощник администратора Astropolis 2.2 для Minecraft 1.19.2 Forge.
Отвечай по-русски, дружелюбно и не длиннее 700 символов. Используй приложенные выдержки из квестов,
рецептов, модлиста и конфигов. Если данных недостаточно — честно скажи это, не выдумывай рецепт.

Ты можешь ПРЕДЛОЖИТЬ серверные команды только когда игрок явно просит выполнить действие. Команды
никогда не выполняются сразу: игрок увидит их и подтвердит через /ai confirm. Разрешены только:
give PLAYER namespace:item [1..64]; effect give/clear PLAYER; gamemode MODE PLAYER; tp PLAYER x y z;
clear PLAYER [item] [count]; kill PLAYER; spawnpoint PLAYER [x y z]; time set; weather; difficulty;
gamerule keepInventory/doDaylightCycle/doWeatherCycle/mobGriefing; setworldspawn. Не используй селекторы
(@a, @e и т. п.), execute, function, op, whitelist, ban, kick, stop или shell. Для предметов всегда
используй точный namespace:id из контекста. Если точный ID неизвестен, спроси или дай инструкцию,
но не создавай команду. Любой PLAYER должен совпадать с именем текущего игрока.
"""


def call_openai(player: str, question: str, live_context: str) -> dict[str, object]:
    if not API_KEY:
        raise RuntimeError(
            "AI ещё не подключён: добавь OPENAI_API_KEY в .server.env и перезапусти сервер"
        )
    history = "\n".join(
        f"{role}: {message}" for role, message in HISTORY[player.lower()]
    )
    knowledge = retrieve(question)
    prompt = (
        f"Текущий игрок: {player}\n"
        f"Состояние в игре: {live_context or 'не передано'}\n"
        f"Недавний диалог:\n{history or 'пусто'}\n"
        f"Вопрос/просьба: {question}\n"
        f"Релевантный контекст сборки:{knowledge or ' ничего не найдено'}"
    )
    payload = {
        "model": MODEL,
        "instructions": INSTRUCTIONS,
        "input": prompt,
        "max_output_tokens": 900,
        "store": False,
        "safety_identifier": hashlib.sha256(player.lower().encode()).hexdigest()[:32],
        "text": {
            "verbosity": "low",
            "format": {
                "type": "json_schema",
                "name": "astropolis_assistant_reply",
                "strict": True,
                "schema": RESPONSE_SCHEMA,
            },
        },
    }
    request = Request(
        f"{API_BASE_URL}/responses",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=90) as response:
            raw = json.load(response)
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"OpenAI API вернул HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"не удалось связаться с OpenAI API: {exc.reason}") from exc

    output_text = ""
    for item in raw.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                output_text += content.get("text", "")
    if not output_text:
        raise RuntimeError("модель вернула пустой ответ")
    answer = json.loads(output_text)
    reply = str(answer.get("reply", "")).strip()[:700]
    commands: list[dict[str, str]] = []
    for candidate in answer.get("commands", [])[:3]:
        normalized = validate_command(str(candidate.get("command", "")), player)
        if normalized:
            commands.append(
                {
                    "command": normalized,
                    "reason": str(candidate.get("reason", "")).strip()[:180],
                }
            )
    HISTORY[player.lower()].append(("Игрок", question))
    HISTORY[player.lower()].append(("Ассистент", reply))
    return {"ok": True, "reply": reply or "Готово.", "commands": commands}


def run_job(job_id: str, player: str, question: str, live_context: str) -> None:
    try:
        result = call_openai(player, question, live_context)
    except Exception as exc:  # surfaced to the authorized player, not the public socket
        result = {"ok": False, "error": str(exc)[:700]}
    result["finished_at"] = time.time()
    with JOBS_LOCK:
        JOBS[job_id] = result


def purge_jobs() -> None:
    cutoff = time.time() - RESULT_TTL
    with JOBS_LOCK:
        stale = [
            job_id
            for job_id, result in JOBS.items()
            if float(result.get("finished_at", time.time())) < cutoff
        ]
        for job_id in stale:
            JOBS.pop(job_id, None)


class Handler(BaseHTTPRequestHandler):
    server_version = "AstropolisAIBridge/1.0"

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"[ai-bridge] {self.address_string()} {fmt % args}", flush=True)

    def send_json(self, status: int, payload: dict[str, object]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self.send_json(
                200,
                {
                    "ok": True,
                    "configured": bool(API_KEY),
                    "model": MODEL,
                    "documents": len(DOCUMENTS),
                },
            )
            return
        if self.path.startswith("/result/"):
            purge_jobs()
            job_id = self.path.removeprefix("/result/")
            with JOBS_LOCK:
                result = JOBS.get(job_id)
                if result and "finished_at" in result:
                    result = JOBS.pop(job_id)
            if result is None:
                self.send_json(404, {"ok": False, "error": "запрос не найден или мост был перезапущен"})
            elif "finished_at" not in result:
                self.send_json(202, {"ok": True, "pending": True})
            else:
                result.pop("finished_at", None)
                self.send_json(200, result)
            return
        self.send_json(404, {"ok": False, "error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/ask":
            self.send_json(404, {"ok": False, "error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 20_000:
                raise ValueError("invalid body length")
            data = json.loads(self.rfile.read(length))
            player = str(data.get("player", "")).strip()
            question = str(data.get("message", "")).strip()
            live_context = str(data.get("context", "")).strip()[:1500]
            if player.lower() not in ALLOWED_PLAYERS:
                self.send_json(403, {"ok": False, "error": "нет доступа к /ai"})
                return
            if not question or len(question) > MAX_QUESTION:
                self.send_json(400, {"ok": False, "error": "сообщение должно быть от 1 до 700 символов"})
                return
            now = time.monotonic()
            remaining = COOLDOWN - (now - LAST_REQUEST.get(player.lower(), 0))
            if remaining > 0:
                self.send_json(429, {"ok": False, "error": f"подожди ещё {remaining:.0f} сек."})
                return
            LAST_REQUEST[player.lower()] = now
            job_id = secrets.token_urlsafe(18)
            with JOBS_LOCK:
                JOBS[job_id] = {"ok": True, "pending": True}
            threading.Thread(
                target=run_job,
                args=(job_id, player, question, live_context),
                daemon=True,
                name=f"ai-{player}",
            ).start()
            self.send_json(202, {"ok": True, "job_id": job_id})
        except (ValueError, json.JSONDecodeError) as exc:
            self.send_json(400, {"ok": False, "error": str(exc)})


def main() -> None:
    print(
        f"[ai-bridge] listening on http://{HOST}:{PORT}; model={MODEL}; "
        f"documents={len(DOCUMENTS)}; configured={'yes' if API_KEY else 'no'}",
        flush=True,
    )
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()

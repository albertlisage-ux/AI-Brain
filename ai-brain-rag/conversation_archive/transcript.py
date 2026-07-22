from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class NormalizedMessage:
    role: str
    text: str


@dataclass(frozen=True)
class NormalizedTranscript:
    session_id: str
    created_at: datetime
    messages: tuple[NormalizedMessage, ...]
    content_hash: str
    source_path: Path | None = None


def _parse_time(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _event_message(payload: dict[str, Any]) -> NormalizedMessage | None:
    event_type = payload.get("type")
    roles = {"user_message": "user", "agent_message": "assistant"}
    role = roles.get(event_type)
    text = payload.get("message")
    if role and isinstance(text, str) and text.strip():
        return NormalizedMessage(role=role, text=text.strip())
    return None


def _response_message(payload: dict[str, Any]) -> NormalizedMessage | None:
    if payload.get("type") != "message" or payload.get("role") not in {
        "user",
        "assistant",
    }:
        return None
    content = payload.get("content")
    if not isinstance(content, list):
        return None
    visible_types = {"input_text", "output_text", "text"}
    parts = [
        item["text"].strip()
        for item in content
        if isinstance(item, dict)
        and item.get("type") in visible_types
        and isinstance(item.get("text"), str)
        and item["text"].strip()
    ]
    if not parts:
        return None
    return NormalizedMessage(role=payload["role"], text="\n".join(parts))


def parse_transcript(path: Path, sessions_root: Path) -> NormalizedTranscript:
    resolved_root = Path(sessions_root).expanduser().resolve(strict=True)
    resolved_path = Path(path).expanduser().resolve(strict=True)
    if not resolved_path.is_relative_to(resolved_root):
        raise ValueError("transcript path is outside configured sessions root")
    if not resolved_path.is_file():
        raise ValueError("transcript path is not a file")

    session_id = resolved_path.stem
    created_at: datetime | None = None
    messages: list[NormalizedMessage] = []
    with resolved_path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                record = json.loads(line)
            except (json.JSONDecodeError, TypeError):
                continue
            if not isinstance(record, dict):
                continue
            payload = record.get("payload")
            if not isinstance(payload, dict):
                continue
            record_type = record.get("type")
            if record_type == "session_meta":
                identifier = payload.get("id")
                if isinstance(identifier, str) and identifier.strip():
                    session_id = identifier.strip()
                created_at = (
                    _parse_time(payload.get("timestamp"))
                    or _parse_time(record.get("timestamp"))
                    or created_at
                )
            elif record_type == "event_msg":
                message = _event_message(payload)
                if message:
                    messages.append(message)
            elif record_type == "response_item":
                message = _response_message(payload)
                if message:
                    messages.append(message)

    if created_at is None:
        created_at = datetime.fromtimestamp(resolved_path.stat().st_mtime, timezone.utc)
    canonical = json.dumps(
        [{"role": item.role, "text": item.text} for item in messages],
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    content_hash = hashlib.sha256(canonical).hexdigest()
    return NormalizedTranscript(
        session_id=session_id,
        created_at=created_at,
        messages=tuple(messages),
        content_hash=content_hash,
        source_path=resolved_path,
    )

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
from typing import IO, Any, Mapping

from .config import ArchiveConfig
from .store import ArchiveStore, HookEvent as StoreHookEvent


class HookEvent(StoreHookEvent):
    @classmethod
    def from_json(
        cls, value: object, *, now: datetime | None = None
    ) -> "HookEvent":
        if not isinstance(value, dict):
            raise ValueError("hook input must be an object")
        session_id = value.get("session_id") or value.get("sessionId")
        transcript_path = value.get("transcript_path") or value.get("transcriptPath")
        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError("session_id is required")
        if not isinstance(transcript_path, str) or not transcript_path.strip():
            raise ValueError("transcript_path is required")
        turn = value.get("turn_id") or value.get("turnId")
        if turn is not None and not isinstance(turn, str):
            raise ValueError("turn_id must be a string")
        occurred_at = now or datetime.now(timezone.utc)
        supplied_time = value.get("occurred_at") or value.get("occurredAt")
        if supplied_time is not None:
            if not isinstance(supplied_time, str):
                raise ValueError("occurred_at must be an ISO timestamp")
            occurred_at = datetime.fromisoformat(supplied_time.replace("Z", "+00:00"))
        return cls(
            session_id=session_id.strip(),
            transcript_path=Path(transcript_path).expanduser(),
            occurred_at=occurred_at,
            turn_id=turn,
        )


def ingest_payload(
    payload: object, store: ArchiveStore, *, now: datetime | None = None
) -> bool:
    try:
        event = HookEvent.from_json(payload, now=now)
    except (TypeError, ValueError):
        return False
    store.enqueue(event)
    return True


def merge_stop_hook(existing: dict[str, Any], command: str) -> dict[str, Any]:
    if not command.startswith("/"):
        raise ValueError("hook command must begin with an absolute path")
    merged = deepcopy(existing)
    hooks = merged.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError("hooks must be an object")
    stop_hooks = hooks.setdefault("Stop", [])
    if not isinstance(stop_hooks, list):
        raise ValueError("hooks.Stop must be a list")
    if not any(
        isinstance(entry, dict) and entry.get("command") == command
        for entry in stop_hooks
    ):
        stop_hooks.append({"type": "command", "command": command})
    return merged


def main(
    *,
    stdin: IO[str] | None = None,
    stderr: IO[str] | None = None,
    environ: Mapping[str, str] | None = None,
) -> int:
    input_stream = sys.stdin if stdin is None else stdin
    error_stream = sys.stderr if stderr is None else stderr
    source = os.environ if environ is None else environ
    try:
        config = ArchiveConfig.from_env(source)
        store = ArchiveStore(config.database_path, config.quiet_period)
    except Exception as exc:
        print(f"conversation archive hook unavailable: {type(exc).__name__}", file=error_stream)
        return 0
    accepted = 0
    try:
        for line in input_stream:
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                print("conversation archive hook ignored malformed JSON", file=error_stream)
                continue
            try:
                accepted += int(ingest_payload(payload, store))
            except Exception as exc:
                print(
                    f"conversation archive hook enqueue failed: {type(exc).__name__}",
                    file=error_stream,
                )
    finally:
        store.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sqlite3


UTC = timezone.utc


def _timestamp(value: datetime) -> str:
    if value.tzinfo is None:
        raise ValueError("timestamps must be timezone-aware")
    return value.astimezone(UTC).isoformat()


def _datetime(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None


@dataclass(frozen=True)
class HookEvent:
    session_id: str
    transcript_path: Path
    occurred_at: datetime
    turn_id: str | None = None


@dataclass(frozen=True)
class QueueItem:
    session_id: str
    transcript_path: Path
    occurred_at: datetime
    turn_id: str | None
    status: str
    attempts: int
    retry_at: datetime | None
    last_error: str | None
    content_hash: str | None
    note_path: Path | None


class ArchiveStore:
    def __init__(self, database_path: Path, quiet_period: timedelta) -> None:
        self.database_path = Path(database_path)
        self.quiet_period = quiet_period
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self.database_path)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA journal_mode=WAL")
        self._create_schema()

    def _create_schema(self) -> None:
        with self._connection:
            self._connection.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    transcript_path TEXT NOT NULL,
                    occurred_at TEXT NOT NULL,
                    turn_id TEXT,
                    status TEXT NOT NULL DEFAULT 'pending',
                    attempts INTEGER NOT NULL DEFAULT 0,
                    retry_at TEXT,
                    last_error TEXT,
                    content_hash TEXT,
                    note_path TEXT
                )
                """
            )

    def enqueue(self, event: HookEvent) -> None:
        if not event.session_id.strip():
            raise ValueError("session_id is required")
        occurred_at = _timestamp(event.occurred_at)
        with self._connection:
            self._connection.execute(
                """
                INSERT INTO sessions (
                    session_id, transcript_path, occurred_at, turn_id, status
                ) VALUES (?, ?, ?, ?, 'pending')
                ON CONFLICT(session_id) DO UPDATE SET
                    transcript_path = excluded.transcript_path,
                    occurred_at = excluded.occurred_at,
                    turn_id = excluded.turn_id,
                    status = 'pending',
                    attempts = 0,
                    retry_at = NULL,
                    last_error = NULL
                WHERE excluded.occurred_at >= sessions.occurred_at
                """,
                (
                    event.session_id,
                    str(event.transcript_path),
                    occurred_at,
                    event.turn_id,
                ),
            )

    def eligible(self, now: datetime, limit: int = 100) -> list[QueueItem]:
        quiet_before = _timestamp(now - self.quiet_period)
        current = _timestamp(now)
        rows = self._connection.execute(
            """
            SELECT * FROM sessions
            WHERE status IN ('pending', 'failed')
              AND occurred_at <= ?
              AND (retry_at IS NULL OR retry_at <= ?)
            ORDER BY occurred_at ASC
            LIMIT ?
            """,
            (quiet_before, current, limit),
        ).fetchall()
        return [self._item(row) for row in rows]

    def mark_success(self, session_id: str, content_hash: str, note_path: Path) -> None:
        with self._connection:
            self._connection.execute(
                """
                UPDATE sessions
                SET status = 'succeeded', attempts = 0, retry_at = NULL,
                    last_error = NULL, content_hash = ?, note_path = ?
                WHERE session_id = ?
                """,
                (content_hash, str(note_path), session_id),
            )

    def mark_failure(self, session_id: str, error: str, retry_at: datetime) -> None:
        with self._connection:
            self._connection.execute(
                """
                UPDATE sessions
                SET status = 'failed', attempts = attempts + 1,
                    retry_at = ?, last_error = ?
                WHERE session_id = ?
                """,
                (_timestamp(retry_at), error[:1000], session_id),
            )

    def get(self, session_id: str) -> QueueItem | None:
        row = self._connection.execute(
            "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
        ).fetchone()
        return self._item(row) if row else None

    def count(self) -> int:
        row = self._connection.execute("SELECT COUNT(*) AS count FROM sessions").fetchone()
        return int(row["count"])

    def successful_session_ids(self) -> set[str]:
        rows = self._connection.execute(
            "SELECT session_id FROM sessions WHERE status = 'succeeded'"
        ).fetchall()
        return {str(row["session_id"]) for row in rows}

    def close(self) -> None:
        self._connection.close()

    def __enter__(self) -> "ArchiveStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    @staticmethod
    def _item(row: sqlite3.Row) -> QueueItem:
        return QueueItem(
            session_id=row["session_id"],
            transcript_path=Path(row["transcript_path"]),
            occurred_at=_datetime(row["occurred_at"]),  # type: ignore[arg-type]
            turn_id=row["turn_id"],
            status=row["status"],
            attempts=row["attempts"],
            retry_at=_datetime(row["retry_at"]),
            last_error=row["last_error"],
            content_hash=row["content_hash"],
            note_path=Path(row["note_path"]) if row["note_path"] else None,
        )

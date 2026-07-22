from datetime import datetime, timedelta, timezone
from pathlib import Path

from conversation_archive.store import ArchiveStore, HookEvent


UTC = timezone.utc


def event(session_id: str, path: Path, at: datetime, turn_id: str) -> HookEvent:
    return HookEvent(
        session_id=session_id,
        transcript_path=path,
        occurred_at=at,
        turn_id=turn_id,
    )


def test_repeated_events_coalesce_and_newest_turn_wins(tmp_path: Path) -> None:
    database = tmp_path / "archive.sqlite3"
    store = ArchiveStore(database, quiet_period=timedelta(minutes=5))
    first = datetime(2026, 7, 22, 10, 0, tzinfo=UTC)

    store.enqueue(event("session-1", tmp_path / "old.jsonl", first, "turn-1"))
    store.enqueue(
        event(
            "session-1",
            tmp_path / "new.jsonl",
            first + timedelta(minutes=1),
            "turn-2",
        )
    )

    queued = store.get("session-1")
    assert queued is not None
    assert queued.transcript_path == tmp_path / "new.jsonl"
    assert queued.turn_id == "turn-2"
    assert store.count() == 1


def test_eligible_requires_five_minutes_of_quiet(tmp_path: Path) -> None:
    store = ArchiveStore(tmp_path / "archive.sqlite3", quiet_period=timedelta(minutes=5))
    occurred = datetime(2026, 7, 22, 10, 0, tzinfo=UTC)
    store.enqueue(event("session-1", tmp_path / "session.jsonl", occurred, "turn-1"))

    assert store.eligible(occurred + timedelta(minutes=4, seconds=59)) == []
    assert [item.session_id for item in store.eligible(occurred + timedelta(minutes=5))] == [
        "session-1"
    ]


def test_retry_state_survives_reopening_database(tmp_path: Path) -> None:
    database = tmp_path / "archive.sqlite3"
    occurred = datetime(2026, 7, 22, 10, 0, tzinfo=UTC)
    store = ArchiveStore(database, quiet_period=timedelta(minutes=5))
    store.enqueue(event("session-1", tmp_path / "session.jsonl", occurred, "turn-1"))
    retry_at = occurred + timedelta(minutes=15)
    store.mark_failure("session-1", "temporary failure", retry_at=retry_at)
    store.close()

    reopened = ArchiveStore(database, quiet_period=timedelta(minutes=5))
    queued = reopened.get("session-1")
    assert queued is not None
    assert queued.attempts == 1
    assert queued.last_error == "temporary failure"
    assert queued.retry_at == retry_at
    assert reopened.eligible(retry_at - timedelta(seconds=1)) == []
    assert [item.session_id for item in reopened.eligible(retry_at)] == ["session-1"]


def test_success_state_survives_newer_events(tmp_path: Path) -> None:
    database = tmp_path / "archive.sqlite3"
    occurred = datetime(2026, 7, 22, 10, 0, tzinfo=UTC)
    store = ArchiveStore(database, quiet_period=timedelta(minutes=5))
    store.enqueue(event("session-1", tmp_path / "session.jsonl", occurred, "turn-1"))
    store.mark_success("session-1", content_hash="abc", note_path=tmp_path / "note.md")

    store.enqueue(
        event(
            "session-1",
            tmp_path / "session.jsonl",
            occurred + timedelta(minutes=1),
            "turn-2",
        )
    )
    queued = store.get("session-1")
    assert queued is not None
    assert queued.status == "pending"
    assert queued.content_hash == "abc"
    assert queued.note_path == tmp_path / "note.md"
    assert queued.attempts == 0

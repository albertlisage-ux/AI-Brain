from datetime import datetime, timezone
import io
import json
from pathlib import Path

from conversation_archive.hook import HookEvent, ingest_payload, main
from conversation_archive.store import ArchiveStore


def test_valid_stop_input_is_enqueued(tmp_path: Path) -> None:
    transcript = tmp_path / "session.jsonl"
    transcript.touch()
    store = ArchiveStore(tmp_path / "state.sqlite3", quiet_period=__import__("datetime").timedelta(seconds=60))

    accepted = ingest_payload(
        {
            "session_id": "session-1",
            "transcript_path": str(transcript),
            "turn_id": "turn-2",
        },
        store,
        now=datetime(2026, 7, 22, 12, 0, tzinfo=timezone.utc),
    )

    assert accepted is True
    assert store.get("session-1").turn_id == "turn-2"  # type: ignore[union-attr]


def test_hook_event_rejects_missing_transcript_path() -> None:
    try:
        HookEvent.from_json({"session_id": "session-1"})
    except ValueError as exc:
        assert "transcript_path" in str(exc)
    else:
        raise AssertionError("missing transcript path was accepted")


def test_malformed_json_returns_success_without_writing(tmp_path: Path) -> None:
    database = tmp_path / "state.sqlite3"
    stderr = io.StringIO()

    result = main(
        stdin=io.StringIO("{not-json"),
        stderr=stderr,
        environ={
            "CONVERSATION_ARCHIVE_DB": str(database),
            "CONVERSATION_QUIET_SECONDS": "60",
        },
    )

    assert result == 0
    store = ArchiveStore(database, quiet_period=__import__("datetime").timedelta(seconds=60))
    assert store.count() == 0
    assert "{not-json" not in stderr.getvalue()


def test_duplicate_events_coalesce(tmp_path: Path) -> None:
    transcript = tmp_path / "session.jsonl"
    transcript.touch()
    payload = {"session_id": "session-1", "transcript_path": str(transcript)}
    stdin = io.StringIO("\n".join((json.dumps(payload), json.dumps(payload))))

    assert main(
        stdin=stdin,
        stderr=io.StringIO(),
        environ={
            "CONVERSATION_ARCHIVE_DB": str(tmp_path / "state.sqlite3"),
            "CONVERSATION_QUIET_SECONDS": "60",
        },
    ) == 0

    store = ArchiveStore(tmp_path / "state.sqlite3", quiet_period=__import__("datetime").timedelta(seconds=60))
    assert store.count() == 1

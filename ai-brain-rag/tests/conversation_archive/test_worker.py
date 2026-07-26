from datetime import datetime, timedelta, timezone
from pathlib import Path

from conversation_archive.config import ArchiveConfig
from conversation_archive.store import ArchiveStore, HookEvent
from conversation_archive.summarizer import SummaryError
from conversation_archive.transcript import NormalizedTranscript
from conversation_archive.worker import process_once


NOW = datetime(2026, 7, 22, 12, 0, tzinfo=timezone.utc)


def config(tmp_path: Path) -> ArchiveConfig:
    return ArchiveConfig.from_env({
        "OBSIDIAN_VAULT": str(tmp_path / "vault"),
        "CODEX_SESSIONS_ROOT": str(tmp_path / "sessions"),
        "CONVERSATION_ARCHIVE_DB": str(tmp_path / "state.sqlite3"),
        "CONVERSATION_QUIET_SECONDS": "60",
        "DEEPSEEK_API_KEY": "test-key",
    })


def queued(tmp_path: Path) -> tuple[ArchiveStore, ArchiveConfig, Path]:
    cfg = config(tmp_path)
    cfg.sessions_root.mkdir()
    source = cfg.sessions_root / "session.jsonl"
    source.write_text("fixture")
    store = ArchiveStore(cfg.database_path, cfg.quiet_period)
    store.enqueue(HookEvent("session-1", source, NOW - timedelta(minutes=6)))
    return store, cfg, source


def parsed(source: Path, content_hash: str = "hash-1") -> NormalizedTranscript:
    return NormalizedTranscript("session-1", NOW, (), content_hash, source)


def test_unchanged_hash_is_noop(tmp_path: Path) -> None:
    store, cfg, source = queued(tmp_path)
    note = tmp_path / "existing.md"
    note.write_text("existing")
    store.mark_success("session-1", "hash-1", note)
    store.enqueue(HookEvent("session-1", source, NOW - timedelta(minutes=6)))
    called = []

    result = process_once(
        store, cfg, now=NOW,
        parser=lambda *_: parsed(source),
        summarizer=lambda *_: called.append("summary"),
        writer=lambda *_: called.append("write"),
    )

    assert result.unchanged == 1
    assert called == []
    assert note.read_text() == "existing"


def test_successful_note_update_marks_hash(tmp_path: Path) -> None:
    store, cfg, source = queued(tmp_path)
    note = tmp_path / "note.md"

    def write(*_args) -> Path:
        note.write_text("new")
        return note

    result = process_once(
        store, cfg, now=NOW,
        parser=lambda *_: parsed(source, "new-hash"),
        summarizer=lambda *_: object(),
        writer=write,
    )

    assert result.succeeded == 1
    assert store.get("session-1").content_hash == "new-hash"  # type: ignore[union-attr]


def test_failure_is_retried_with_bounded_exponential_backoff(tmp_path: Path) -> None:
    store, cfg, source = queued(tmp_path)

    result = process_once(
        store, cfg, now=NOW,
        parser=lambda *_: parsed(source),
        summarizer=lambda *_: (_ for _ in ()).throw(SummaryError("temporary")),
        writer=lambda *_: Path("unused"),
    )

    item = store.get("session-1")
    assert result.failed == 1
    assert item is not None and item.attempts == 1
    assert item.retry_at == NOW + timedelta(seconds=60)
    assert item.last_error == "SummaryError"


def test_existing_note_is_preserved_when_summary_fails(tmp_path: Path) -> None:
    store, cfg, source = queued(tmp_path)
    note = tmp_path / "note.md"
    note.write_text("old")
    store.mark_success("session-1", "old-hash", note)
    store.enqueue(HookEvent("session-1", source, NOW - timedelta(minutes=6)))

    process_once(
        store, cfg, now=NOW,
        parser=lambda *_: parsed(source, "new-hash"),
        summarizer=lambda *_: (_ for _ in ()).throw(SummaryError("temporary")),
        writer=lambda *_: (_ for _ in ()).throw(AssertionError("must not write")),
    )
    assert note.read_text() == "old"

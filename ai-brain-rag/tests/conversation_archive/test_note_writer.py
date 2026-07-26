from datetime import datetime, timezone
from pathlib import Path

from conversation_archive.config import ArchiveConfig
from conversation_archive.note_writer import note_path_for, write_note
from conversation_archive.summarizer import ConversationSummary
from conversation_archive.transcript import NormalizedMessage, NormalizedTranscript


def config(tmp_path: Path) -> ArchiveConfig:
    return ArchiveConfig.from_env(
        {
            "OBSIDIAN_VAULT": str(tmp_path / "vault"),
            "CODEX_SESSIONS_ROOT": str(tmp_path / "sessions"),
            "CONVERSATION_ARCHIVE_DB": str(tmp_path / "state.sqlite3"),
            "CONVERSATION_QUIET_SECONDS": "60",
        }
    )


def transcript() -> NormalizedTranscript:
    return NormalizedTranscript(
        session_id="session/unsafe id",
        created_at=datetime(2026, 7, 22, 10, 0, tzinfo=timezone.utc),
        messages=(NormalizedMessage("user", "raw transcript must not be copied"),),
        content_hash="abc123",
    )


def summary() -> ConversationSummary:
    return ConversationSummary(
        title='Indexer: "safe" update',
        summary="Updated the indexer.",
        decisions=("Use deterministic IDs",),
        completed_work=("Added replacement behavior",),
        actions=("Run deployment",),
        unresolved_questions=("When to deploy?",),
        solutions=("Delete by filepath",),
        projects_files=("ai-brain-rag/indexer/indexer.py",),
        tags=("rag", "codex archive"),
    )


def test_session_filename_and_month_are_deterministic(tmp_path: Path) -> None:
    expected = (
        tmp_path
        / "vault/02 Projects/Codex Conversations/2026/07/2026-07-22-session-unsafe-id.md"
    )
    assert note_path_for(transcript(), config(tmp_path)) == expected
    assert note_path_for(transcript(), config(tmp_path)) == expected


def test_note_contains_summary_metadata_but_not_raw_conversation(tmp_path: Path) -> None:
    path = write_note(summary(), transcript(), config(tmp_path))
    body = path.read_text()

    assert 'title: "Indexer: \\"safe\\" update"' in body
    assert 'original_transcript: "' in body
    assert "Decisions" in body
    assert "Use deterministic IDs" in body
    assert "raw transcript must not be copied" not in body


def test_existing_note_is_unchanged_if_rendering_fails(tmp_path: Path) -> None:
    path = note_path_for(transcript(), config(tmp_path))
    path.parent.mkdir(parents=True)
    path.write_text("existing note")
    invalid = summary().__class__(**{**summary().__dict__, "tags": (object(),)})

    try:
        write_note(invalid, transcript(), config(tmp_path))
    except (TypeError, ValueError):
        pass
    else:
        raise AssertionError("invalid summary unexpectedly rendered")
    assert path.read_text() == "existing note"

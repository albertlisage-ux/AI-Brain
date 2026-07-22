from __future__ import annotations

import json
from pathlib import Path
import re
import tempfile

from .config import ArchiveConfig
from .summarizer import ConversationSummary
from .transcript import NormalizedTranscript


def _safe_session_id(value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-.")
    return safe[:120] or "unknown-session"


def note_path_for(transcript: NormalizedTranscript, config: ArchiveConfig) -> Path:
    date = transcript.created_at.astimezone().date()
    filename = f"{date.isoformat()}-{_safe_session_id(transcript.session_id)}.md"
    return (
        config.vault_path
        / "02 Projects/Codex Conversations"
        / f"{date.year:04d}"
        / f"{date.month:02d}"
        / filename
    )


def _yaml(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("frontmatter values must be strings")
    return json.dumps(value, ensure_ascii=False)


def _section(title: str, items: tuple[str, ...]) -> str:
    if any(not isinstance(item, str) for item in items):
        raise TypeError(f"{title} entries must be strings")
    body = "\n".join(f"- {item}" for item in items) if items else "- None"
    return f"## {title}\n\n{body}"


def _render(
    summary: ConversationSummary,
    transcript: NormalizedTranscript,
    config: ArchiveConfig,
) -> str:
    transcript_path = getattr(transcript, "source_path", None)
    if transcript_path is None:
        transcript_path = config.sessions_root / f"{transcript.session_id}.jsonl"
    tags = [_yaml(tag) for tag in summary.tags]
    sections = [
        _section("Decisions", summary.decisions),
        _section("Completed Work", summary.completed_work),
        _section("Action Items", summary.actions),
        _section("Unresolved Questions", summary.unresolved_questions),
        _section("Solutions", summary.solutions),
        _section("Projects and Files", summary.projects_files),
    ]
    return "\n".join(
        [
            "---",
            f"title: {_yaml(summary.title)}",
            f"session_id: {_yaml(transcript.session_id)}",
            f"created_at: {_yaml(transcript.created_at.isoformat())}",
            f"content_hash: {_yaml(transcript.content_hash)}",
            f"original_transcript: {_yaml(str(transcript_path))}",
            "tags: [" + ", ".join(tags) + "]",
            "---",
            "",
            f"# {summary.title}",
            "",
            summary.summary,
            "",
            "\n\n".join(sections),
            "",
        ]
    )


def write_note(
    summary: ConversationSummary,
    transcript: NormalizedTranscript,
    config: ArchiveConfig,
) -> Path:
    content = _render(summary, transcript, config)
    destination = note_path_for(transcript, config)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=destination.parent, delete=False
        ) as handle:
            handle.write(content)
            handle.flush()
            temporary = Path(handle.name)
        temporary.replace(destination)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return destination

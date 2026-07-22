from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import tempfile


@dataclass(frozen=True)
class CapacitySnapshot:
    captured_at: datetime
    total_bytes: int
    file_count: int
    unsummarized_count: int


def collect_capacity(
    root: Path,
    summarized_session_ids: set[str] | None = None,
    *,
    now: datetime | None = None,
) -> CapacitySnapshot:
    summarized = summarized_session_ids or set()
    total = 0
    count = 0
    unsummarized = 0
    for path in Path(root).rglob("*"):
        if not path.is_file():
            continue
        try:
            total += path.stat().st_size
        except OSError:
            continue
        count += 1
        if path.stem not in summarized:
            unsummarized += 1
    return CapacitySnapshot(
        captured_at=now or datetime.now(timezone.utc),
        total_bytes=total,
        file_count=count,
        unsummarized_count=unsummarized,
    )


def write_monthly_report(
    snapshot: CapacitySnapshot,
    destination: Path,
    *,
    previous: CapacitySnapshot | None = None,
    size_warning_bytes: int = 5 * 1024**3,
    growth_warning_percent: int = 20,
) -> Path:
    warnings: list[str] = []
    if snapshot.total_bytes >= size_warning_bytes:
        warnings.append("WARNING: transcript storage is at or above 5 GiB.")
    growth: float | None = None
    if previous and previous.total_bytes > 0:
        growth = (snapshot.total_bytes - previous.total_bytes) / previous.total_bytes * 100
        if growth >= growth_warning_percent:
            warnings.append(f"WARNING: transcript storage grew by at least {growth_warning_percent}%.")
    lines = [
        "---",
        f'month: "{snapshot.captured_at:%Y-%m}"',
        f'captured_at: "{snapshot.captured_at.isoformat()}"',
        f"total_bytes: {snapshot.total_bytes}",
        f"file_count: {snapshot.file_count}",
        f"unsummarized_count: {snapshot.unsummarized_count}",
        "---",
        "",
        f"# Codex Session Capacity — {snapshot.captured_at:%Y-%m}",
        "",
        f"- Total bytes: {snapshot.total_bytes}",
        f"- Files: {snapshot.file_count}",
        f"- Unsummarized: {snapshot.unsummarized_count}",
        f"- Growth: {growth:.1f}%" if growth is not None else "- Growth: unavailable",
        "",
        *(warnings or ["No capacity warning thresholds were reached."]),
        "",
        "This report is read-only. No transcript was compressed, moved, or deleted.",
        "",
    ]
    content = "\n".join(lines)
    destination = Path(destination)
    if destination.exists() and destination.read_text(encoding="utf-8") == content:
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=destination.parent, delete=False
        ) as handle:
            handle.write(content)
            temporary = Path(handle.name)
        temporary.replace(destination)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return destination

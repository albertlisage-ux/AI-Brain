from datetime import datetime, timezone
from pathlib import Path

from conversation_archive.capacity import CapacitySnapshot, collect_capacity, write_monthly_report


NOW = datetime(2026, 7, 22, 12, 0, tzinfo=timezone.utc)


def test_collect_capacity_is_read_only_and_counts_unsummarized(tmp_path: Path) -> None:
    root = tmp_path / "sessions"
    root.mkdir()
    first = root / "one.jsonl"
    second = root / "two.jsonl"
    first.write_bytes(b"123")
    second.write_bytes(b"12345")
    before = {path: (path.stat().st_mtime_ns, path.read_bytes()) for path in (first, second)}

    snapshot = collect_capacity(root, summarized_session_ids={"one"}, now=NOW)

    assert snapshot.total_bytes == 8
    assert snapshot.file_count == 2
    assert snapshot.unsummarized_count == 1
    assert before == {path: (path.stat().st_mtime_ns, path.read_bytes()) for path in (first, second)}


def test_monthly_report_is_idempotent_and_warns_on_thresholds(tmp_path: Path) -> None:
    report = tmp_path / "2026-07.md"
    current = CapacitySnapshot(NOW, 6 * 1024**3, 20, 3)
    previous = CapacitySnapshot(NOW, 4 * 1024**3, 10, 1)

    write_monthly_report(current, report, previous=previous)
    first_mtime = report.stat().st_mtime_ns
    body = report.read_text()
    write_monthly_report(current, report, previous=previous)

    assert report.stat().st_mtime_ns == first_mtime
    assert "WARNING" in body
    assert "5 GiB" in body
    assert "20%" in body

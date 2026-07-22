from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import signal
import time
from typing import Any, Callable

from .capacity import collect_capacity, write_monthly_report
from .config import ArchiveConfig
from .note_writer import note_path_for, write_note
from .store import ArchiveStore
from .summarizer import summarize
from .transcript import parse_transcript


@dataclass(frozen=True)
class ProcessResult:
    examined: int = 0
    succeeded: int = 0
    unchanged: int = 0
    failed: int = 0


def process_once(
    store: ArchiveStore,
    config: ArchiveConfig,
    *,
    now: datetime | None = None,
    parser: Callable[..., Any] = parse_transcript,
    summarizer: Callable[..., Any] = summarize,
    writer: Callable[..., Any] = write_note,
) -> ProcessResult:
    current = now or datetime.now(timezone.utc)
    succeeded = unchanged = failed = 0
    items = store.eligible(current)
    for item in items:
        try:
            transcript = parser(item.transcript_path, config.sessions_root)
            if item.content_hash == transcript.content_hash:
                destination = item.note_path or note_path_for(transcript, config)
                store.mark_success(item.session_id, transcript.content_hash, destination)
                unchanged += 1
                continue
            summary = summarizer(transcript, config)
            destination = writer(summary, transcript, config)
            store.mark_success(item.session_id, transcript.content_hash, destination)
            succeeded += 1
        except Exception as exc:
            delay_seconds = min(3600, 60 * (2**item.attempts))
            store.mark_failure(
                item.session_id,
                type(exc).__name__,
                retry_at=current + timedelta(seconds=delay_seconds),
            )
            failed += 1
    return ProcessResult(len(items), succeeded, unchanged, failed)


def generate_monthly_capacity_report(
    store: ArchiveStore, config: ArchiveConfig, *, now: datetime | None = None
) -> None:
    current = now or datetime.now(timezone.utc)
    destination = config.reports_path / f"{current:%Y-%m}.md"
    if destination.exists():
        return
    snapshot = collect_capacity(
        config.sessions_root,
        store.successful_session_ids(),
        now=current,
    )
    write_monthly_report(
        snapshot,
        destination,
        size_warning_bytes=config.capacity_report_threshold_bytes,
        growth_warning_percent=config.capacity_growth_warning_percent,
    )


def run_forever(config: ArchiveConfig, poll_seconds: int = 30) -> None:
    stopping = False

    def stop(*_: object) -> None:
        nonlocal stopping
        stopping = True

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    with ArchiveStore(config.database_path, config.quiet_period) as store:
        while not stopping:
            process_once(store, config)
            generate_monthly_capacity_report(store, config)
            for _ in range(max(1, poll_seconds)):
                if stopping:
                    break
                time.sleep(1)


def main() -> int:
    run_forever(ArchiveConfig.from_env())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

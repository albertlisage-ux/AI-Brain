from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import os
from pathlib import Path
from typing import Mapping


def _path(value: str) -> Path:
    return Path(value).expanduser().resolve()


def _positive_int(source: Mapping[str, str], name: str, default: int) -> int:
    raw = source.get(name, str(default))
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


@dataclass(frozen=True)
class ArchiveConfig:
    vault_path: Path
    sessions_root: Path
    database_path: Path
    quiet_period: timedelta
    deepseek_api_key: str
    deepseek_api_base: str
    deepseek_model: str
    capacity_report_threshold_bytes: int
    capacity_growth_warning_percent: int
    reports_path: Path

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "ArchiveConfig":
        source = os.environ if environ is None else environ
        project_root = Path(__file__).resolve().parent.parent
        vault = _path(
            source.get(
                "OBSIDIAN_VAULT",
                source.get("OBSIDIAN_VAULT_PATH", str(project_root.parent)),
            )
        )
        return cls(
            vault_path=vault,
            sessions_root=_path(
                source.get("CODEX_SESSIONS_ROOT", str(Path.home() / ".codex/sessions"))
            ),
            database_path=_path(
                source.get(
                    "CONVERSATION_ARCHIVE_DB",
                    str(project_root / "data/conversation-archive/state.sqlite3"),
                )
            ),
            quiet_period=timedelta(
                seconds=_positive_int(source, "CONVERSATION_QUIET_SECONDS", 300)
            ),
            deepseek_api_key=source.get("DEEPSEEK_API_KEY", ""),
            deepseek_api_base=source.get(
                "DEEPSEEK_API_BASE", "https://api.deepseek.com/v1"
            ).rstrip("/"),
            deepseek_model=source.get("DEEPSEEK_MODEL", "deepseek-chat"),
            capacity_report_threshold_bytes=_positive_int(
                source, "CODEX_CAPACITY_WARNING_BYTES", 5 * 1024**3
            ),
            capacity_growth_warning_percent=_positive_int(
                source, "CODEX_CAPACITY_GROWTH_PERCENT", 20
            ),
            reports_path=_path(
                source.get(
                    "CODEX_CAPACITY_REPORTS_PATH",
                    str(vault / "02 Projects/Codex Conversations/Reports"),
                )
            ),
        )

from datetime import timedelta

from conversation_archive.config import ArchiveConfig


def test_default_quiet_period_is_one_minute(tmp_path) -> None:
    config = ArchiveConfig.from_env(
        {
            "OBSIDIAN_VAULT": str(tmp_path / "vault"),
            "CODEX_SESSIONS_ROOT": str(tmp_path / "sessions"),
            "CONVERSATION_ARCHIVE_DB": str(tmp_path / "state.sqlite3"),
        }
    )

    assert config.quiet_period == timedelta(seconds=60)

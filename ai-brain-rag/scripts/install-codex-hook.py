#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from conversation_archive.hook import merge_stop_hook  # noqa: E402


def install(config_path: Path, command: str) -> None:
    existing = json.loads(config_path.read_text()) if config_path.exists() else {}
    merged = merge_stop_hook(existing, command)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=config_path.parent, delete=False
    ) as handle:
        json.dump(merged, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temporary = Path(handle.name)
    temporary.replace(config_path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path.home() / ".codex/hooks.json")
    parser.add_argument("--command", required=True)
    args = parser.parse_args()
    install(args.config.expanduser(), args.command)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

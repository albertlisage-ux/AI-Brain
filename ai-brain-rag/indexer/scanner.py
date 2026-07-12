"""Scan the Obsidian vault for markdown files, computing content hashes."""

import hashlib
import os
from pathlib import Path
from config import OBSIDIAN_VAULT, EXCLUDE_DIRS, EXCLUDE_FILES


def _should_exclude(path: Path, vault_root: str) -> bool:
    """Check if a path should be excluded."""
    rel = path.relative_to(vault_root)
    parts = rel.parts
    for part in parts:
        if part in EXCLUDE_DIRS:
            return True
    return False


def scan_vault() -> dict[str, dict]:
    """
    Walk the vault and return a dict of:
      {relative_path: {"mtime": float, "hash": str, "size": int}}
    """
    vault_root = os.path.abspath(OBSIDIAN_VAULT)
    files = {}

    for root, dirs, filenames in os.walk(vault_root):
        root_path = Path(root)

        # Prune excluded dirs in-place (modifying dirs affects os.walk)
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for fn in filenames:
            if fn in EXCLUDE_FILES or not fn.endswith(".md"):
                continue
            fp = root_path / fn
            rel = str(fp.relative_to(vault_root))
            if _should_exclude(fp, vault_root):
                continue

            stat = fp.stat()
            content = fp.read_bytes()
            h = hashlib.sha256(content).hexdigest()

            files[rel] = {
                "mtime": stat.st_mtime,
                "hash": h,
                "size": stat.st_size,
            }

    return files

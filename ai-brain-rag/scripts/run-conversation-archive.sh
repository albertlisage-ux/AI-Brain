#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ -f "$PROJECT_ROOT/.env.local" ]]; then
  set -a
  source "$PROJECT_ROOT/.env.local"
  set +a
fi

PYTHON="${AI_BRAIN_PYTHON:-$PROJECT_ROOT/.venv/bin/python}"
if [[ ! -x "$PYTHON" ]]; then
  echo "AI-Brain virtual environment is missing: $PYTHON" >&2
  exit 1
fi

cd "$PROJECT_ROOT"
if [[ "${1:-}" == "--hook" ]]; then
  exec "$PYTHON" -m conversation_archive.hook
fi
exec "$PYTHON" -m conversation_archive.worker

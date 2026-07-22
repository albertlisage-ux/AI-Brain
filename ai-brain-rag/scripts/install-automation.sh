#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_HOME="${AI_BRAIN_TARGET_HOME:-$HOME}"
AGENTS_DIR="$TARGET_HOME/Library/LaunchAgents"
LOG_DIR="$PROJECT_ROOT/data/logs"

mkdir -p "$AGENTS_DIR" "$LOG_DIR"

render() {
  local template="$1"
  local destination="$2"
  sed \
    -e "s|__PROJECT_ROOT__|$PROJECT_ROOT|g" \
    -e "s|__LOG_DIR__|$LOG_DIR|g" \
    "$template" > "$destination"
  plutil -lint "$destination" >/dev/null
}

render \
  "$PROJECT_ROOT/launchd/com.yuanzhe.ai-brain-conversation-archive.plist.template" \
  "$AGENTS_DIR/com.yuanzhe.ai-brain-conversation-archive.plist"
render \
  "$PROJECT_ROOT/launchd/com.yuanzhe.ai-brain-indexer.plist.template" \
  "$AGENTS_DIR/com.yuanzhe.ai-brain-indexer.plist"

if [[ "${AI_BRAIN_SKIP_HOOK:-0}" != "1" ]]; then
  "$PROJECT_ROOT/.venv/bin/python" "$PROJECT_ROOT/scripts/install-codex-hook.py" \
    --config "$TARGET_HOME/.codex/hooks.json" \
    --command "$PROJECT_ROOT/scripts/run-conversation-archive.sh --hook"
fi

if [[ "${AI_BRAIN_SKIP_LAUNCHD:-0}" != "1" ]]; then
  domain="gui/$(id -u)"
  for label in com.yuanzhe.ai-brain-conversation-archive com.yuanzhe.ai-brain-indexer; do
    plist="$AGENTS_DIR/$label.plist"
    launchctl bootout "$domain/$label" >/dev/null 2>&1 || true
    launchctl bootstrap "$domain" "$plist"
  done
fi

echo "Installed AI-Brain conversation archive and indexer automation."

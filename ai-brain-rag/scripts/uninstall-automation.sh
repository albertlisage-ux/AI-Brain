#!/bin/bash
set -euo pipefail

TARGET_HOME="${AI_BRAIN_TARGET_HOME:-$HOME}"
AGENTS_DIR="$TARGET_HOME/Library/LaunchAgents"
domain="gui/$(id -u)"

for label in com.yuanzhe.ai-brain-conversation-archive com.yuanzhe.ai-brain-indexer; do
  launchctl bootout "$domain/$label" >/dev/null 2>&1 || true
  rm -f "$AGENTS_DIR/$label.plist"
done

echo "Unloaded project LaunchAgents. Hook, summaries, reports, and state were preserved."

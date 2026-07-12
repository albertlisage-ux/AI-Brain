#!/bin/bash
# AI-Brain Indexer — Host mode (macOS native, Ollama Metal GPU)
# Run this on your Mac instead of the Docker indexer for 5-10x faster indexing.
# Prerequisites: brew install ollama && ollama pull nomic-embed-text

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

export OLLAMA_HOST="http://localhost:11434"
export OLLAMA_EMBED_MODEL="nomic-embed-text"
export QDRANT_HOST="localhost"
export QDRANT_PORT="6333"
export QDRANT_COLLECTION="ai-brain"
export OBSIDIAN_VAULT="$PROJECT_DIR"
export SCAN_INTERVAL="30"
export CHUNK_SIZE="500"
export CHUNK_OVERLAP="50"

echo "🧠 AI-Brain Indexer (Host Mode)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Vault: $OBSIDIAN_VAULT"
echo "Qdrant: $QDRANT_HOST:$QDRANT_PORT"
echo "Ollama: $OLLAMA_HOST ($OLLAMA_EMBED_MODEL)"
echo ""

# Check Ollama is running
if ! curl -sf http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama is not running. Start it with: brew services start ollama"
    exit 1
fi

# Check Qdrant is running (from Docker)
if ! curl -sf http://localhost:6333/healthz > /dev/null 2>&1; then
    echo "❌ Qdrant is not running. Start it with:"
    echo "   cd ai-brain-rag && docker compose --env-file .env.local up -d qdrant"
    exit 1
fi

echo "✅ Ollama connected"
echo "✅ Qdrant connected"
echo ""

# Create venv if needed
VENV_DIR="$SCRIPT_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv "$VENV_DIR"
    "$VENV_DIR/bin/pip" install -q qdrant-client
fi

echo "🚀 Starting indexer..."
cd "$SCRIPT_DIR"
exec "$VENV_DIR/bin/python" -u indexer/indexer.py

import os

QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "ai-brain")
OBSIDIAN_VAULT = os.getenv("OBSIDIAN_VAULT", "/vault")
SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL", "30"))
INDEXER_STATE_FILE = os.getenv("INDEXER_STATE_FILE", "data/indexer/state.json")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))

EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "768"))

EXCLUDE_DIRS = {
    ".obsidian", ".git", "__pycache__", "node_modules",
    "99 Archive", "Attachments", "data", "ai-brain-rag",
}

EXCLUDE_FILES = {".DS_Store", "README.md"}

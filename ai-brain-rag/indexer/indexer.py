#!/usr/bin/env python3
"""
AI-Brain Indexer

Scans the Obsidian vault, chunks markdown files, generates embeddings,
and upserts them into Qdrant. Runs on a timer loop.
"""

import json
import logging
import os
import sys
import time
import traceback
import uuid
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
    Filter,
    FieldCondition,
    MatchValue,
    HasIdCondition,
)

from chunker import chunk_markdown
from config import (
    QDRANT_HOST,
    QDRANT_PORT,
    QDRANT_COLLECTION,
    EMBEDDING_DIM,
    OBSIDIAN_VAULT,
    SCAN_INTERVAL,
    EXCLUDE_DIRS,
)
from embedder import embed_texts
from scanner import scan_vault

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("indexer")

# State file to track file hashes across restarts
STATE_FILE = "/tmp/indexer_state.json"


def _get_file_id(filepath: str, chunk_index: int) -> str:
    """Generate a unique ID for a chunk."""
    rel = filepath.replace(str(OBSIDIAN_VAULT), "").lstrip("/")
    return f"{rel}::chunk_{chunk_index}"


def _get_point(file_id: str, vector: list[float], payload: dict) -> PointStruct:
    return PointStruct(id=file_id, vector=vector, payload=payload)


def ensure_collection(client: QdrantClient):
    """Create the collection if it doesn't exist."""
    collections = client.get_collections().collections
    names = [c.name for c in collections]
    if QDRANT_COLLECTION not in names:
        logger.info("Creating collection '%s' (dim=%d)", QDRANT_COLLECTION, EMBEDDING_DIM)
        client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
        )


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def index_vault(client: QdrantClient):
    """Main indexing logic — process one file at a time."""
    vault_root = os.path.abspath(OBSIDIAN_VAULT)
    logger.info("Scanning vault: %s", vault_root)

    current_files = scan_vault()
    prev_state = load_state()

    changed = [rel for rel, info in current_files.items()
               if rel not in prev_state or prev_state[rel]["hash"] != info["hash"]]
    deleted = [rel for rel in prev_state if rel not in current_files]

    if not changed and not deleted:
        logger.info("No changes. Next scan in %ds.", SCAN_INTERVAL)
        return

    logger.info("Changed: %d  Deleted: %d", len(changed), len(deleted))

    # --- Delete removed files ---
    for rel in deleted:
        try:
            points, _ = client.scroll(
                collection_name=QDRANT_COLLECTION,
                scroll_filter=Filter(must=[
                    FieldCondition(key="_filepath", match=MatchValue(value=rel))
                ]),
                limit=1000,
            )
            ids = [p.id for p in points]
            if ids:
                client.delete(collection_name=QDRANT_COLLECTION, points_selector=ids)
                logger.info("  🗑 Deleted %d points for '%s'", len(ids), rel)
        except Exception:
            logger.warning("  Failed to delete '%s': %s", rel, traceback.format_exc())

    # --- Process each changed file independently ---
    total_files = len(changed)
    total_chunks = 0
    total_time = 0.0

    for idx, rel in enumerate(changed, 1):
        abs_path = os.path.join(vault_root, rel)
        logger.info("  [%d/%d] %s", idx, total_files, rel)

        # 1. Chunk
        try:
            chunks = chunk_markdown(abs_path)
        except Exception as e:
            logger.warning("  ⚠ SKIP (chunk): %s", e)
            continue

        if not chunks:
            logger.info("    → 0 chunks, skipped")
            continue

        # 2. Embed
        texts = [c["content"] for c in chunks]
        t0 = time.time()
        try:
            vectors = embed_texts(texts)
        except Exception as e:
            logger.warning("  ⚠ SKIP (embed): %s", e)
            continue

        elapsed = time.time() - t0
        total_time += elapsed

        # 3. Upsert
        points = []
        for ci, (chunk, vec) in enumerate(zip(chunks, vectors)):
            fid = str(uuid.uuid4())
            folder = str(Path(rel).parent)
            title = Path(rel).stem
            points.append(_get_point(fid, vec, {
                "filepath": rel, "title": title, "folder": folder,
                "heading": chunk["heading"], "content": chunk["content"],
                "chunk_index": ci,
            }))

        BATCH = 100
        for i in range(0, len(points), BATCH):
            client.upsert(collection_name=QDRANT_COLLECTION, points=points[i:i+BATCH])

        total_chunks += len(chunks)
        avg = elapsed / len(chunks) * 1000
        logger.info("    → %d chunks, %.1fs (%.0f ms/chunk) ✅", len(chunks), elapsed, avg)

    # --- Summary ---
    if total_chunks:
        logger.info("─" * 40)
        logger.info("Done: %d files, %d chunks, %.1fs total", total_files, total_chunks, total_time)

    save_state(current_files)
    # Explicit flush so logs appear immediately
    for h in logger.handlers:
        h.flush()


def main():
    logger.info("AI-Brain Indexer starting...")

    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    ensure_collection(client)

    logger.info("Connected to Qdrant at %s:%s", QDRANT_HOST, QDRANT_PORT)
    logger.info("Ollama embedder | Dim: %d | Scan interval: %ds",
                EMBEDDING_DIM, SCAN_INTERVAL)

    while True:
        try:
            index_vault(client)
        except KeyboardInterrupt:
            logger.info("Shutting down.")
            break
        except Exception:
            logger.error("Indexer error: %s", traceback.format_exc())

        time.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    main()

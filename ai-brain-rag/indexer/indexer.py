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
from embedder import embed_texts, get_model
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
    """Main indexing logic."""
    vault_root = os.path.abspath(OBSIDIAN_VAULT)
    logger.info("Scanning vault: %s", vault_root)

    current_files = scan_vault()
    prev_state = load_state()

    # Determine which files are new or changed
    changed_files = []
    deleted_files = []

    for rel, info in current_files.items():
        prev = prev_state.get(rel)
        if prev is None or prev["hash"] != info["hash"]:
            changed_files.append(rel)

    for rel in prev_state:
        if rel not in current_files:
            deleted_files.append(rel)

    if not changed_files and not deleted_files:
        logger.info("No changes detected. Next scan in %ds.", SCAN_INTERVAL)
        return

    logger.info("Changed: %d  Deleted: %d", len(changed_files), len(deleted_files))

    # Delete removed files' points
    if deleted_files:
        deleted_ids = []
        for rel in deleted_files:
            # We stored chunks as rel::chunk_N; delete all matching
            prefix = rel.replace(str(OBSIDIAN_VAULT), "").lstrip("/") + "::chunk_"
            # Use scroll to find all points with this prefix
            try:
                points, _ = client.scroll(
                    collection_name=QDRANT_COLLECTION,
                    scroll_filter=Filter(
                        must=[
                            FieldCondition(
                                key="_filepath",
                                match=MatchValue(value=rel),
                            )
                        ]
                    ),
                    limit=1000,
                )
                ids = [p.id for p in points]
                if ids:
                    client.delete(
                        collection_name=QDRANT_COLLECTION,
                        points_selector=ids,
                    )
                    logger.info("Deleted %d points for '%s'", len(ids), rel)
            except Exception:
                logger.warning("Failed to delete points for '%s': %s", rel, traceback.format_exc())

    # Index changed files
    if changed_files:
        all_chunks = []
        for rel in changed_files:
            abs_path = os.path.join(vault_root, rel)
            try:
                chunks = chunk_markdown(abs_path)
                for c in chunks:
                    # Add filepath as payload field for filtering
                    c["_filepath"] = rel
                    c["_title"] = Path(rel).stem
                    c["_folder"] = str(Path(rel).parent)
                all_chunks.extend(chunks)
                logger.info("  → %s: %d chunks", rel, len(chunks))
            except Exception:
                logger.warning("  → %s: SKIP (%s)", rel, traceback.format_exc())

        if all_chunks:
            logger.info("Generating embeddings for %d chunks...", len(all_chunks))
            texts = [c["content"] for c in all_chunks]
            vectors = embed_texts(texts)

            points = []
            for chunk, vec in zip(all_chunks, vectors):
                fid = _get_file_id(chunk["filepath"], chunk["chunk_index"])
                payload = {
                    "filepath": chunk["_filepath"],
                    "title": chunk["_title"],
                    "folder": chunk["_folder"],
                    "heading": chunk["heading"],
                    "content": chunk["content"],
                    "chunk_index": chunk["chunk_index"],
                }
                points.append(_get_point(fid, vec, payload))

            # Upsert in batches
            BATCH = 100
            for i in range(0, len(points), BATCH):
                batch = points[i : i + BATCH]
                client.upsert(collection_name=QDRANT_COLLECTION, points=batch)
            logger.info("Upserted %d points to Qdrant.", len(points))

    # Update state
    save_state(current_files)
    logger.info("Indexing complete. Next scan in %ds.", SCAN_INTERVAL)


def main():
    logger.info("AI-Brain Indexer starting...")

    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    ensure_collection(client)
    get_model()  # preload model

    logger.info("Connected to Qdrant at %s:%s", QDRANT_HOST, QDRANT_PORT)
    logger.info("Model: %s  Dim: %d  Scan interval: %ds",
                os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5"),
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

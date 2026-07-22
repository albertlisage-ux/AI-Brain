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
import tempfile
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
    Filter,
    FieldCondition,
    MatchValue,
    FilterSelector,
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
    INDEXER_STATE_FILE,
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
STATE_FILE = INDEXER_STATE_FILE
POINT_NAMESPACE = uuid.UUID("ed6d7bea-1a17-56b7-b2a4-e180d93fdbfa")


def _point_id(rel_path: str, chunk_index: int) -> str:
    """Generate the stable Qdrant UUID for one relative-path chunk."""
    return str(uuid.uuid5(POINT_NAMESPACE, f"{rel_path}::chunk_{chunk_index}"))


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
    destination = Path(STATE_FILE)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=destination.parent, delete=False
        ) as handle:
            json.dump(state, handle, sort_keys=True)
            handle.write("\n")
            temporary = Path(handle.name)
        temporary.replace(destination)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def _delete_file_points(client: QdrantClient, rel_path: str) -> None:
    """Delete every prior vector for a relative Vault path."""
    client.delete(
        collection_name=QDRANT_COLLECTION,
        points_selector=FilterSelector(
            filter=Filter(
                must=[FieldCondition(key="filepath", match=MatchValue(value=rel_path))]
            )
        ),
        wait=True,
    )


def index_vault(client: QdrantClient):
    """Main indexing logic — process one file at a time."""
    vault_root = os.path.abspath(OBSIDIAN_VAULT)
    logger.info("Scanning vault: %s", vault_root)

    current_files = scan_vault()
    prev_state = load_state()

    changed = sorted(
        rel
        for rel, info in current_files.items()
        if rel not in prev_state or prev_state[rel]["hash"] != info["hash"]
    )
    deleted = sorted(rel for rel in prev_state if rel not in current_files)

    if not changed and not deleted:
        logger.info("No changes. Next scan in %ds.", SCAN_INTERVAL)
        return

    logger.info("Changed: %d  Deleted: %d", len(changed), len(deleted))

    next_state = dict(prev_state)

    # --- Delete removed files ---
    for rel in deleted:
        try:
            _delete_file_points(client, rel)
            next_state.pop(rel, None)
            logger.info("  Deleted prior points for '%s'", rel)
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
            try:
                _delete_file_points(client, rel)
            except Exception as e:
                logger.warning("  SKIP (delete empty): %s", e)
                continue
            next_state[rel] = current_files[rel]
            logger.info("    → 0 chunks, prior points removed")
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
            fid = _point_id(rel, ci)
            folder = str(Path(rel).parent)
            title = Path(rel).stem
            points.append(_get_point(fid, vec, {
                "filepath": rel, "title": title, "folder": folder,
                "heading": chunk["heading"], "content": chunk["content"],
                "chunk_index": ci,
            }))

        try:
            _delete_file_points(client, rel)
            BATCH = 100
            for i in range(0, len(points), BATCH):
                client.upsert(
                    collection_name=QDRANT_COLLECTION,
                    points=points[i:i+BATCH],
                    wait=True,
                )
        except Exception as e:
            logger.warning("  SKIP (Qdrant replace): %s", e)
            continue

        next_state[rel] = current_files[rel]

        total_chunks += len(chunks)
        avg = elapsed / len(chunks) * 1000
        logger.info("    → %d chunks, %.1fs (%.0f ms/chunk) ✅", len(chunks), elapsed, avg)

    # --- Summary ---
    if total_chunks:
        logger.info("─" * 40)
        logger.info("Done: %d files, %d chunks, %.1fs total", total_files, total_chunks, total_time)

    save_state(next_state)
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

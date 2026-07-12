"""Generate embeddings using Ollama API (native macOS, Metal GPU accelerated)."""

import json
import logging
import os
import urllib.request
import urllib.error

logger = logging.getLogger("embedder")

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
BATCH_SIZE = 10


def _call_ollama(texts: list[str]) -> list[list[float]]:
    """Send a batch of texts to Ollama and return embeddings."""
    url = f"{OLLAMA_HOST}/api/embed"
    payload = json.dumps({"model": OLLAMA_MODEL, "input": texts}).encode()

    req = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read())
    return data["embeddings"]


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Generate embeddings in batches via Ollama API."""
    all_embeddings = []
    total = len(texts)
    logger.info("Embedding %d texts via Ollama (batch size=%d)...", total, BATCH_SIZE)

    for i in range(0, total, BATCH_SIZE):
        batch = texts[i : i + BATCH_SIZE]
        try:
            embeddings = _call_ollama(batch)
            all_embeddings.extend(embeddings)
            logger.info("  Ollama progress: %d/%d (%.0f%%)",
                        min(i + BATCH_SIZE, total), total,
                        min(i + BATCH_SIZE, total) / total * 100)
        except Exception as e:
            logger.error("  Ollama batch %d failed: %s", i // BATCH_SIZE, e)
            raise

    logger.info("Ollama embedding complete: %d vectors", len(all_embeddings))
    return all_embeddings


def embed_text(text: str) -> list[float]:
    return embed_texts([text])[0]

"""Retrieve relevant chunks from Qdrant."""

import json
import os
import urllib.request
from functools import lru_cache
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

from config import QDRANT_HOST, QDRANT_PORT, QDRANT_COLLECTION

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")


@lru_cache(maxsize=1)
def get_client() -> QdrantClient:
    return QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


def _ollama_embed(text: str) -> list[float]:
    url = f"{OLLAMA_HOST}/api/embed"
    payload = json.dumps({"model": OLLAMA_MODEL, "input": [text]}).encode()
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    return data["embeddings"][0]


def _build_filter(filters: dict | None) -> Filter | None:
    """Build a Qdrant filter from a dict like {"folder": "Skills"}."""
    if not filters:
        return None
    conditions = []
    for key, value in filters.items():
        conditions.append(FieldCondition(key=key, match=MatchValue(value=value)))
    return Filter(must=conditions) if conditions else None


def search_qdrant(question: str, top_k: int = 5, filters: dict | None = None) -> list[dict]:
    """Search Qdrant for chunks relevant to the question."""
    client = get_client()

    query_vec = _ollama_embed(question)
    qdrant_filter = _build_filter(filters)

    hits = client.query_points(
        collection_name=QDRANT_COLLECTION,
        query=query_vec,
        limit=top_k,
        query_filter=qdrant_filter,
        with_payload=True,
    ).points

    results = []
    for hit in hits:
        p = hit.payload
        results.append({
            "filepath": p.get("filepath", ""),
            "title": p.get("title", ""),
            "folder": p.get("folder", ""),
            "heading": p.get("heading", ""),
            "content": p.get("content", ""),
            "score": hit.score,
            "chunk_index": p.get("chunk_index", 0),
        })

    return results

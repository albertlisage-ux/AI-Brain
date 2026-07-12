"""Retrieve relevant chunks from Qdrant."""

from functools import lru_cache
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer

from config import QDRANT_HOST, QDRANT_PORT, QDRANT_COLLECTION, EMBEDDING_MODEL


@lru_cache(maxsize=1)
def get_client() -> QdrantClient:
    return QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


@lru_cache(maxsize=1)
def get_embedder():
    return SentenceTransformer(EMBEDDING_MODEL, trust_remote_code=True)


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
    embedder = get_embedder()

    query_vec = embedder.encode(question, normalize_embeddings=True).tolist()
    qdrant_filter = _build_filter(filters)

    hits = client.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=query_vec,
        limit=top_k,
        query_filter=qdrant_filter,
        with_payload=True,
    )

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

"""MCP tool implementations for querying the AI-Brain knowledge base."""

import json
import os
import urllib.request
from functools import lru_cache
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

from config import QDRANT_HOST, QDRANT_PORT, QDRANT_COLLECTION, OBSIDIAN_VAULT

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")


@lru_cache(maxsize=1)
def get_qdrant() -> QdrantClient:
    return QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


def _ollama_embed(text: str) -> list[float]:
    url = f"{OLLAMA_HOST}/api/embed"
    payload = json.dumps({"model": OLLAMA_MODEL, "input": [text]}).encode()
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    return data["embeddings"][0]


def _build_filter(folder: str | None = None) -> Filter | None:
    if not folder:
        return None
    return Filter(must=[FieldCondition(key="folder", match=MatchValue(value=folder))])


def search_knowledge(query: str, top_k: int = 5, folder: str | None = None) -> list[dict]:
    """Search the knowledge base for relevant chunks."""
    client = get_qdrant()

    query_vec = _ollama_embed(query)
    qdrant_filter = _build_filter(folder)

    hits = client.query_points(
        collection_name=QDRANT_COLLECTION,
        query=query_vec,
        limit=top_k,
        query_filter=qdrant_filter,
        with_payload=True,
    ).points

    return [
        {
            "filepath": h.payload.get("filepath", ""),
            "title": h.payload.get("title", ""),
            "folder": h.payload.get("folder", ""),
            "heading": h.payload.get("heading", ""),
            "content": h.payload.get("content", ""),
            "score": round(h.score, 4),
        }
        for h in hits
    ]


def read_note(filepath: str) -> str | None:
    """Read the full content of a note by its relative path."""
    abs_path = os.path.join(OBSIDIAN_VAULT, filepath)
    if not os.path.isfile(abs_path) or not filepath.endswith(".md"):
        return None
    try:
        with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return None


def list_notes(folder: str | None = None) -> list[dict]:
    """List all markdown notes, optionally filtered by folder."""
    vault_root = os.path.abspath(OBSIDIAN_VAULT)
    notes = []
    exclude_dirs = {".obsidian", ".git", "__pycache__", "node_modules"}

    for root, dirs, filenames in os.walk(vault_root):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            rel = str(Path(root).relative_to(vault_root) / fn)
            if folder and not rel.startswith(folder):
                continue
            fp = Path(root) / fn
            stat = fp.stat()
            notes.append({
                "filepath": rel,
                "title": fn.replace(".md", ""),
                "folder": str(Path(rel).parent),
                "size": stat.st_size,
                "mtime": stat.st_mtime,
            })

    return sorted(notes, key=lambda x: x["filepath"])


def get_project_context(project_name: str, top_k: int = 8) -> list[dict]:
    """Get context from all notes related to a specific project."""
    folder = f"02 Projects/{project_name}"
    return search_knowledge(query=project_name, top_k=top_k, folder=folder)


def get_skill(skill_name: str) -> dict | None:
    """Retrieve a skill document and its related content."""
    filepath = f"03 Skills/{skill_name}.md"
    content = read_note(filepath)
    if content is None:
        return None
    return {"filepath": filepath, "content": content}

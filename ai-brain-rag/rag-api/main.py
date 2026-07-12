"""RAG API — FastAPI application."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from qdrant_client import QdrantClient

from config import QDRANT_HOST, QDRANT_PORT, QDRANT_COLLECTION, EMBEDDING_MODEL, DEEPSEEK_API_KEY, DEEPSEEK_MODEL
from models import (
    SearchRequest, SearchResponse, AskRequest, AskResponse,
    ChunkResult, HealthResponse, StatsResponse,
)
from retriever import search_qdrant, get_embedder
from responder import ask_deepseek

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s %(message)s")
logger = logging.getLogger("rag-api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("RAG API starting...")
    # Warm up embedder on startup
    try:
        get_embedder()
        logger.info("Embedding model loaded.")
    except Exception as e:
        logger.warning("Failed to load embedding model: %s", e)
    yield
    logger.info("RAG API shutting down.")


app = FastAPI(title="AI-Brain RAG API", version="1.0.0", lifespan=lifespan)


@app.get("/health", response_model=HealthResponse)
async def health():
    qdrant_ok = False
    try:
        client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, timeout=3)
        client.get_collections()
        qdrant_ok = True
    except Exception:
        pass

    model_ok = False
    try:
        get_embedder()
        model_ok = True
    except Exception:
        pass

    return HealthResponse(
        status="ok" if qdrant_ok else "degraded",
        qdrant_connected=qdrant_ok,
        model_loaded=model_ok,
        deepseek_configured=bool(DEEPSEEK_API_KEY),
    )


@app.get("/stats", response_model=StatsResponse)
async def stats():
    try:
        client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, timeout=5)
        collection_info = client.get_collection(collection_name=QDRANT_COLLECTION)
        total = collection_info.points_count
    except Exception:
        total = 0

    return StatsResponse(
        total_points=total,
        collections=[QDRANT_COLLECTION],
        embedding_model=EMBEDDING_MODEL,
        deepseek_model=DEEPSEEK_MODEL,
    )


@app.post("/search", response_model=SearchResponse)
async def search(req: SearchRequest):
    """Search the knowledge base without calling DeepSeek."""
    try:
        results = search_qdrant(req.question, req.top_k, req.filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return SearchResponse(
        question=req.question,
        results=[ChunkResult(**r) for r in results],
    )


@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    """Search + ask DeepSeek for a natural language answer."""
    try:
        chunks = search_qdrant(req.question, req.top_k, req.filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")

    if not chunks:
        return AskResponse(
            question=req.question,
            answer="No relevant notes found in the knowledge base.",
            references=[],
        )

    try:
        answer = await ask_deepseek(req.question, chunks)
    except Exception as e:
        answer = f"Error calling DeepSeek API: {e}"

    return AskResponse(
        question=req.question,
        answer=answer,
        references=[ChunkResult(**r) for r in chunks],
    )


@app.post("/reindex")
async def reindex():
    """Trigger a reindex by sending a signal (stub — actual reindex runs in indexer container)."""
    return {"message": "Reindex trigger acknowledged. The indexer will pick up changes on its next scan cycle."}

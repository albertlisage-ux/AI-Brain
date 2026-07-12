from pydantic import BaseModel
from typing import Optional


class SearchRequest(BaseModel):
    question: str
    top_k: int = 5
    filters: Optional[dict] = None


class AskRequest(BaseModel):
    question: str
    top_k: int = 5
    filters: Optional[dict] = None


class ChunkResult(BaseModel):
    filepath: str
    title: str
    folder: str
    heading: str
    content: str
    score: float
    chunk_index: int


class SearchResponse(BaseModel):
    question: str
    results: list[ChunkResult]


class AskResponse(BaseModel):
    question: str
    answer: str
    references: list[ChunkResult]


class HealthResponse(BaseModel):
    status: str
    qdrant_connected: bool
    model_loaded: bool
    deepseek_configured: bool


class StatsResponse(BaseModel):
    total_points: int
    collections: list[str]
    embedding_model: str
    deepseek_model: str

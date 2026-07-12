"""Generate embeddings using a local Sentence-Transformer model."""

from functools import lru_cache
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL, EMBEDDING_DIM


@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer(EMBEDDING_MODEL, trust_remote_code=True)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for a list of text strings."""
    model = get_model()
    embeddings = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
    return embeddings.tolist()


def embed_text(text: str) -> list[float]:
    """Generate embedding for a single text string."""
    return embed_texts([text])[0]

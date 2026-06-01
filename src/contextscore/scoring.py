import numpy as np
from sentence_transformers import SentenceTransformer
from typing import cast


def embed(
    texts: list[str],
    # all-MiniLM-L6-v2: lightweight & fast model (384-dim), good balance of speed/quality
    model_name: str = "all-MiniLM-L6-v2",
) -> np.ndarray:
    """Encode texts into dense vector embeddings for semantic similarity scoring.

    Args:
        texts: List of input strings to embed.
        model_name: SentenceTransformer model name.

    Returns:
        Array of embedding vectors of shape (n_texts, embedding_dim).
    """
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, convert_to_numpy=True)
    # Tell mypy encode is returning a numpy array
    embeddings = cast(np.ndarray, embeddings)
    return embeddings

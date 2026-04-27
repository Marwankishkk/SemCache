"""Semantic cache: embed queries, match similar past queries, return cached responses."""

from .cache import Cache
from .embeddings import EmbeddingModel
from .storage import Storage

__all__ = ["Cache", "EmbeddingModel", "Storage"]
__version__ = "0.1.0"

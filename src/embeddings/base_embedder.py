from abc import ABC, abstractmethod
from typing import List, Tuple
from langchain_core.documents import Document

class BaseEmbedder(ABC):
    """Abstract Embedder class for all embedding models."""

    @abstractmethod
    def embed_documents(self, documents: List[Document]) -> List[List[float]]:
        """Return embeddings for list of LangChain documents."""
        pass

    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """Embedding for a single query."""
        pass

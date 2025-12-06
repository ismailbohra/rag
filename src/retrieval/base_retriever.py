from abc import ABC, abstractmethod
from typing import List, Tuple
from langchain_core.documents import Document

class BaseRetriever(ABC):
    """Abstract retriever interface."""

    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[Document, float]]:
        """Return list of (Document, score)."""
        pass

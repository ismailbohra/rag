from abc import ABC, abstractmethod
from typing import List, Tuple
from langchain_core.documents import Document

class BaseVectorStore(ABC):

    @abstractmethod
    def create_collection(self):
        """Create table/schema if not exists."""
        pass

    @abstractmethod
    def upsert(
        self,
        docs: List[Document],
        embeddings: List[List[float]],
    ):
        """Insert or update stored embeddings."""
        pass

    @abstractmethod
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5
    ) -> List[Tuple[Document, float]]:
        """Return (Document, score) results."""
        pass

    @abstractmethod
    def delete(self, doc_id: str):
        """Delete document by id."""
        pass

from typing import List, Tuple
from langchain_core.documents import Document
from ..embeddings.embedder_factory import EmbedderFactory
from ..vectorstore.base_store import BaseVectorStore
from .base_retriever import BaseRetriever

class VectorRetriever(BaseRetriever):

    def __init__(
        self,
        vector_store: BaseVectorStore,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        self.vector_store = vector_store
        self.embedder = EmbedderFactory.get_embedder(model_name)

    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[Document, float]]:
        # 1. Embed query
        query_emb = self.embedder.embed_query(query)

        # 2. Run vector database search
        results = self.vector_store.search(query_emb, top_k=top_k)

        # 'results' is List[(Document, score)]
        return results

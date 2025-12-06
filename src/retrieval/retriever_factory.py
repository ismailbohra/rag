from .vector_retriever import VectorRetriever
from ..vectorstore.base_store import BaseVectorStore

class RetrieverFactory:

    @staticmethod
    def get_retriever(
        retriever_type: str,
        vector_store: BaseVectorStore,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):

        if retriever_type == "vector":
            return VectorRetriever(vector_store, model_name)

        raise ValueError(f"Unknown retriever type: {retriever_type}")

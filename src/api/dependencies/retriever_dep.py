from src.retrieval.retriever_factory import RetrieverFactory
from .vector_store_dep import get_vector_store

def get_retriever():
    store = get_vector_store()
    return RetrieverFactory.get_retriever(
        retriever_type="vector",
        vector_store=store,
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

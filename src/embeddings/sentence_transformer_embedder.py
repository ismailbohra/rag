from typing import List
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer
from .base_embedder import BaseEmbedder

class SentenceTransformerEmbedder(BaseEmbedder):

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, documents: List[Document]) -> List[List[float]]:
        texts = [doc.page_content for doc in documents]
        embeddings = self.model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        emb = self.model.encode([text], show_progress_bar=False)[0]
        return emb.tolist()

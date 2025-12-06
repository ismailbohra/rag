from typing import List, Tuple
from langchain_core.documents import Document
from .embedder_factory import EmbedderFactory
from .chunker import Chunker

class EmbeddingPipeline:

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ):
        self.embedder = EmbedderFactory.get_embedder(model_name)
        self.chunker = Chunker(chunk_size, chunk_overlap)

    def process(self, documents: List[Document]) -> Tuple[List[Document], List[List[float]]]:
        """Chunk -> Embed -> Return"""
        
        # Step 1: Chunk documents
        chunked_docs = self.chunker.chunk_documents(documents)

        # Step 2: Generate embeddings
        embeddings = self.embedder.embed_documents(chunked_docs)

        return chunked_docs, embeddings

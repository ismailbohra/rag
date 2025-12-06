from src.embeddings.embedder_factory import EmbedderFactory

def get_embedder():
    return EmbedderFactory.get_embedder(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

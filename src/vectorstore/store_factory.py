from .pgvector_store import PGVectorStore

class VectorStoreFactory:

    @staticmethod
    def get_store(
        db_type: str = "pgvector",
        conn_str: str = None,
        embedding_dim: int = 768
    ):
        if db_type == "pgvector":
            return PGVectorStore(
                conn_str=conn_str,
                embedding_dim=embedding_dim
            )

        raise ValueError(f"Unsupported vector store: {db_type}")

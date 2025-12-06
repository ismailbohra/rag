from src.vectorstore.store_factory import VectorStoreFactory

def get_vector_store():
    return VectorStoreFactory.get_store(
        db_type="pgvector",
        conn_str="postgresql://default:FqGEiXoH6jO2@ep-billowing-butterfly-a4sdj7jq-pooler.us-east-1.aws.neon.tech/vectordb?sslmode=require&channel_binding=require",
        embedding_dim=384,
    )

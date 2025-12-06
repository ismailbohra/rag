from fastapi import APIRouter, Depends
from src.api.schemas.ingest_schema import IngestRequest
from src.ingestion.pipeline import IngestionPipeline
from src.embeddings.pipeline import EmbeddingPipeline
from src.api.dependencies.vector_store_dep import get_vector_store

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

@router.post("/")
def ingest_docs(
    payload: IngestRequest,
    store = Depends(get_vector_store)
):
    path = payload.file_path

    # 1. Load docs
    docs = IngestionPipeline().load(path)

    # 2. Chunk + embed
    embed_pipeline = EmbeddingPipeline(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        chunk_size=350,
        chunk_overlap=50
    )
    chunked_docs, embeddings = embed_pipeline.process(docs)

    # 3. Store in vector DB
    store.create_collection()
    store.upsert(chunked_docs, embeddings)

    return {
        "status": "success",
        "chunks_indexed": len(chunked_docs)
    }

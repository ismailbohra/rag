from fastapi import FastAPI
from .routers.ingest_router import router as ingest_router
from .routers.query_router import router as query_router

app = FastAPI(
    title="Modular RAG API",
    version="1.0",
    description="Production RAG architecture with FastAPI"
)

app.include_router(ingest_router)
app.include_router(query_router)

@app.get("/")
def root():
    return {"status": "RAG API running"}

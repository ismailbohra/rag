from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from typing import List
import shutil
import os
from pathlib import Path
from src.api.schemas.ingest_schema import IngestRequest, IngestFileResponse
from src.ingestion.pipeline import IngestionPipeline
from src.embeddings.pipeline import EmbeddingPipeline
from src.api.dependencies.vector_store_dep import get_vector_store

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

# Ensure data folder exists
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


@router.post("/", response_model=dict)
def ingest_docs(
    payload: IngestRequest,
    store = Depends(get_vector_store)
):
    """Ingest documents using file_path (backward compatible)"""
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


@router.post("/upload", response_model=List[IngestFileResponse])
async def ingest_files(
    files: List[UploadFile] = File(...),
    store = Depends(get_vector_store)
):
    """
    Upload and ingest multiple PDF files.
    - Files are saved to data/ folder
    - File paths are stored in metadata
    - Returns success/error for each file
    """
    results = []
    
    for file in files:
        try:
            # 1. Validate file type
            if not file.filename:
                results.append({
                    "status": "error",
                    "filename": "unknown",
                    "file_path": "",
                    "chunks_indexed": 0,
                    "error": "No filename provided"
                })
                continue
            
            if not file.filename.lower().endswith('.pdf'):
                results.append({
                    "status": "error",
                    "filename": file.filename,
                    "file_path": "",
                    "chunks_indexed": 0,
                    "error": "Only PDF files are supported"
                })
                continue
            
            # 2. Save file to data folder
            file_path = DATA_DIR / file.filename
            
            # If file exists, create a unique name
            if file_path.exists():
                name, ext = os.path.splitext(file.filename)
                counter = 1
                while (DATA_DIR / f"{name}_{counter}{ext}").exists():
                    counter += 1
                file_path = DATA_DIR / f"{name}_{counter}{ext}"
            
            # Write uploaded file to disk
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # 3. Load and process documents
            docs = IngestionPipeline().load(str(file_path))
            
            if not docs:
                results.append({
                    "status": "error",
                    "filename": file.filename,
                    "file_path": str(file_path),
                    "chunks_indexed": 0,
                    "error": "No content extracted from PDF"
                })
                continue
            
            # 4. Chunk + embed
            embed_pipeline = EmbeddingPipeline(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                chunk_size=350,
                chunk_overlap=50
            )
            chunked_docs, embeddings = embed_pipeline.process(docs)
            
            # 5. Store in vector DB
            store.create_collection()
            store.upsert(chunked_docs, embeddings)
            
            # 6. Return success
            results.append({
                "status": "success",
                "filename": file.filename,
                "file_path": str(file_path),
                "chunks_indexed": len(chunked_docs),
                "embeddings": embeddings
            })
            
        except Exception as e:
            results.append({
                "status": "error",
                "filename": file.filename if file.filename else "unknown",
                "file_path": "",
                "chunks_indexed": 0,
                "error": str(e)
            })
    
    return results


@router.get("/files/{filename}")
async def get_file(filename: str):
    """
    Serve uploaded PDF files for download/viewing.
    Prevents directory traversal attacks.
    """
    # Sanitize filename (prevent directory traversal)
    if "/" in filename or "\\" in filename or filename.startswith("."):
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    file_path = DATA_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    if not file_path.is_file():
        raise HTTPException(status_code=400, detail="Invalid file path")
    
    # Return file
    from fastapi.responses import FileResponse
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=filename
    )

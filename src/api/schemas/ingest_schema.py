from pydantic import BaseModel
from typing import Optional, Dict

class IngestRequest(BaseModel):
    file_path: str
    metadata: Optional[Dict] = None


class IngestFileResponse(BaseModel):
    status: str
    filename: str
    file_path: str
    chunks_indexed: int

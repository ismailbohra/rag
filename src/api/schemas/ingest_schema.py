from pydantic import BaseModel
from typing import Optional, Dict

class IngestRequest(BaseModel):
    file_path: str
    metadata: Optional[Dict] = None

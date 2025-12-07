"""Pydantic schemas for chat sessions and messages."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class CreateSessionReq(BaseModel):
    """Schema for creating a new chat session."""
    title: Optional[str] = Field(None, max_length=255)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Questions about RAG"
            }
        }


class SessionOut(BaseModel):
    """Schema for chat session response."""
    id: int
    title: Optional[str]
    created_at: str
    last_activity: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Questions about RAG",
                "created_at": "2025-12-06T10:00:00",
                "last_activity": "2025-12-06T11:30:00"
            }
        }


class ChatMessageIn(BaseModel):
    """Schema for incoming chat message."""
    content: str = Field(..., min_length=1)
    role: str = Field("user", pattern="^(user|assistant|system)$")

    class Config:
        json_schema_extra = {
            "example": {
                "content": "What is retrieval augmented generation?",
                "role": "user"
            }
        }


class ChatMessageOut(BaseModel):
    """Schema for chat message response."""
    id: int
    session_id: int
    user_id: int
    role: str
    content: str
    citations: Optional[List[Dict]] = None
    created_at: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "session_id": 1,
                "user_id": 1,
                "role": "user",
                "content": "What is RAG?",
                "citations": None,
                "created_at": "2025-12-06T10:00:00"
            }
        }


class QueryPayload(BaseModel):
    """Schema for query/chat endpoint request."""
    query: str = Field(..., min_length=1)
    session_id: Optional[int] = None
    top_k: Optional[int] = Field(5, ge=1, le=50)
    stream: Optional[bool] = False

    class Config:
        json_schema_extra = {
            "example": {
                "query": "Explain retrieval augmented generation",
                "session_id": 1,
                "top_k": 5,
                "stream": False
            }
        }


class QueryResponse(BaseModel):
    """Schema for query/chat endpoint response."""
    session_id: int
    response: dict

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": 1,
                "response": "Retrieval augmented generation (RAG) is..."
            }
        }

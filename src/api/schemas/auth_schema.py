"""Pydantic schemas for authentication endpoints."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreate(BaseModel):
    """Schema for user registration."""
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[str] = None
    password: str = Field(..., min_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "secure_password_123"
            }
        }


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "secure_password_123"
            }
        }


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class UserOut(BaseModel):
    """Schema for user response (without password)."""
    id: int
    username: str
    email: Optional[str]
    created_at: str

    class Config:
        from_attributes = True

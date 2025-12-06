"""Authentication dependency for FastAPI."""
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from src.api.utils.auth import decode_access_token
from src.models.base import SessionLocal
from src.models.tables import User
from typing import Optional


def get_db():
    """Get database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Extract and validate JWT token from Authorization header.
    Returns the authenticated user.
    
    Expected header format: Authorization: Bearer <token>
    """
    # Check if authorization header is provided
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )
    
    # Extract token from header
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header format. Expected: Bearer <token>"
        )
    
    token = authorization.split(" ", 1)[1]
    
    # Decode and validate token
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token or expired"
        )
    
    # Get user from database
    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    return user

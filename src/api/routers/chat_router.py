"""Chat sessions and messages router."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.api.dependencies.auth_dep import get_current_user, get_db
from src.models.tables import ChatSession, Chat, User
from src.api.schemas.chat_schema import (
    CreateSessionReq,
    SessionOut,
    ChatMessageOut
)
from src.api.utils.api_logging import log_api_call

router = APIRouter(prefix="/chats", tags=["chats"])


def to_session_out(s: ChatSession) -> SessionOut:
    """Convert ChatSession ORM to Pydantic response model."""
    return SessionOut(
        id=s.id,
        title=s.title,
        created_at=s.created_at.isoformat(),
        last_activity=s.last_activity.isoformat()
    )


def to_message_out(m: Chat) -> ChatMessageOut:
    """Convert Chat ORM to Pydantic response model."""
    return ChatMessageOut(
        id=m.id,
        session_id=m.session_id,
        user_id=m.user_id,
        role=m.role,
        content=m.content,
        citations=m.citations if m.citations else None,
        created_at=m.created_at.isoformat()
    )


@router.get("/sessions", response_model=List[SessionOut])
@log_api_call("get_user_sessions")
def get_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all chat sessions for the current user, ordered by last activity."""
    sessions = (
        db.query(ChatSession)
        .filter(ChatSession.user_id == current_user.id)
        .order_by(ChatSession.last_activity.desc())
        .all()
    )
    return [to_session_out(s) for s in sessions]


@router.post("/sessions", response_model=SessionOut)
@log_api_call("create_chat_session")
def create_session(
    payload: CreateSessionReq,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new chat session for the current user."""
    session = ChatSession(
        user_id=current_user.id,
        title=payload.title or "New chat"
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return to_session_out(session)


@router.get("/sessions/{session_id}", response_model=List[ChatMessageOut])
@log_api_call("get_session_messages")
def get_session_messages(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all messages for a specific chat session."""
    # Verify session belongs to current user
    session = (
        db.query(ChatSession)
        .filter(
            ChatSession.id == session_id,
            ChatSession.user_id == current_user.id
        )
        .first()
    )
    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    # Fetch all messages in chronological order
    messages = (
        db.query(Chat)
        .filter(Chat.session_id == session_id)
        .order_by(Chat.created_at.asc())
        .all()
    )
    return [to_message_out(m) for m in messages]


@router.delete("/sessions/{session_id}")
@log_api_call("delete_chat_session")
def delete_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a chat session and all its messages."""
    session = (
        db.query(ChatSession)
        .filter(
            ChatSession.id == session_id,
            ChatSession.user_id == current_user.id
        )
        .first()
    )
    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    db.delete(session)
    db.commit()
    return {"detail": "Session deleted successfully"}

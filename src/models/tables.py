"""SQLAlchemy ORM models for users, chat sessions, and messages."""
from sqlalchemy import (
    Column, Integer, BigInteger, Text, TIMESTAMP, 
    ForeignKey, JSON, func, Index, TypeDecorator, String
)
from sqlalchemy.dialects.postgresql import TIMESTAMP as PG_TS
from sqlalchemy.orm import relationship
from .base import Base


class Vector(TypeDecorator):
    """Custom type for pgvector."""
    impl = String
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(String())
        return dialect.type_descriptor(String())


class User(Base):
    """User account model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, unique=True, nullable=False, index=True)
    email = Column(Text, unique=True, nullable=True)
    hashed_password = Column(Text, nullable=False)
    created_at = Column(
        PG_TS(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Relationships
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
    chats = relationship("Chat", back_populates="user", cascade="all, delete-orphan")


class ChatSession(Base):
    """Chat session (conversation thread) model."""
    __tablename__ = "chat_sessions"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    title = Column(Text, nullable=True)
    created_at = Column(
        PG_TS(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    last_activity = Column(
        PG_TS(timezone=True),
        server_default=func.now(),
        nullable=False,
        onupdate=func.now()
    )

    # Relationships
    user = relationship("User", back_populates="chat_sessions")
    chats = relationship("Chat", back_populates="session", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_chat_sessions_user_id', 'user_id'),
    )


class Chat(Base):
    """Chat message model."""
    __tablename__ = "chats"

    id = Column(BigInteger, primary_key=True, index=True)
    session_id = Column(
        BigInteger,
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    role = Column(Text, nullable=False)  # 'user' | 'assistant' | 'system'
    content = Column(Text, nullable=False)
    citations = Column(JSON, server_default="[]")
    chat_metadata = Column(JSON, server_default="{}")
    created_at = Column(
        PG_TS(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Relationships
    session = relationship("ChatSession", back_populates="chats")
    user = relationship("User", back_populates="chats")
    embedding = relationship("ChatEmbedding", back_populates="chat", uselist=False, cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_chats_session_id', 'session_id'),
        Index('idx_chats_user_id', 'user_id'),
        Index('idx_chats_created_at', 'created_at'),
    )


class ChatEmbedding(Base):
    """Chat message embedding model (pgvector)."""
    __tablename__ = "chat_embeddings"

    chat_id = Column(
        BigInteger,
        ForeignKey("chats.id", ondelete="CASCADE"),
        primary_key=True
    )
    embedding = Column(Vector, nullable=True)
    chat_metadata = Column(JSON, server_default="{}")

    # Relationships
    chat = relationship("Chat", back_populates="embedding")

"""Database configuration and session management."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read from environment or use default for development
DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# Base class for models
Base = declarative_base()

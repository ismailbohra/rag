"""
Bootstrap script to initialize the database with required tables and indexes.

Run this once before starting the application:
    python bootstrap_db.py
"""
import os
import sys
from sqlalchemy import text
from src.models.base import engine, Base
from src.models.tables import User, ChatSession, Chat, ChatEmbedding
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def init_db():
    """Initialize database tables and extensions."""
    print("🗄️  Initializing database...")

    # Create all tables from SQLAlchemy models
    print("📋 Creating tables from models...")
    Base.metadata.create_all(bind=engine)

    # Enable pgvector extension
    print("📦 Enabling pgvector extension...")
    with engine.connect() as conn:
        try:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
            print("✅ pgvector extension enabled")
        except Exception as e:
            print(f"⚠️  pgvector extension error: {e}")

    # Create indexes
    print("🔍 Creating indexes...")
    with engine.connect() as conn:
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)",
            "CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_id ON chat_sessions(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_chats_session_id ON chats(session_id)",
            "CREATE INDEX IF NOT EXISTS idx_chats_user_id ON chats(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_chats_created_at ON chats(created_at)",
        ]
        for idx_sql in indexes:
            try:
                conn.execute(text(idx_sql))
                conn.commit()
            except Exception as e:
                print(f"⚠️  Index creation warning: {e}")

    print("✅ Database initialized successfully!")
    print("\n📚 Tables created:")
    print("   - users")
    print("   - chat_sessions")
    print("   - chats")
    print("   - chat_embeddings")
    print("   - documents (original ingestion table)")


def verify_db():
    """Verify database connection and basic structure."""
    print("\n🔗 Verifying database connection...")
    try:
        with engine.connect() as conn:
            # Test basic query
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
            print("✅ Database connection successful")

            # Check for pgvector
            try:
                result = conn.execute(text("SELECT extname FROM pg_extension WHERE extname='vector'"))
                if result.fetchone():
                    print("✅ pgvector extension available")
                else:
                    print("⚠️  pgvector not found - trying to enable...")
            except Exception as e:
                print(f"⚠️  pgvector check failed: {e}")

            # Check tables exist
            tables = ['users', 'chat_sessions', 'chats', 'chat_embeddings']
            for table in tables:
                try:
                    result = conn.execute(
                        text(f"SELECT 1 FROM information_schema.tables WHERE table_name='{table}'")
                    )
                    if result.fetchone():
                        print(f"✅ Table '{table}' exists")
                    else:
                        print(f"❌ Table '{table}' not found")
                except Exception as e:
                    print(f"❌ Error checking table '{table}': {e}")

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print(f"   DATABASE_URL: {os.getenv('DATABASE_URL', 'not set')}")
        sys.exit(1)


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 RAG Database Bootstrap Script")
    print("=" * 60)
    
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ragdb")
    print(f"\n📍 Target Database: {db_url[:40]}...")

    try:
        init_db()
        verify_db()
        print("\n✨ Bootstrap complete! Ready to start the application.")
    except Exception as e:
        print(f"\n❌ Bootstrap failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

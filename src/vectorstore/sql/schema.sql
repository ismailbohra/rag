-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Original documents table for ingestion
CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    content TEXT,
    metadata JSONB,
    embedding vector(768) -- adjust dimension based on your model
);

-- Users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Chat sessions (conversation threads per user)
CREATE TABLE IF NOT EXISTS chat_sessions (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    last_activity TIMESTAMPTZ DEFAULT now()
);

-- Chat messages (ordered messages within a session)
CREATE TABLE IF NOT EXISTS chats (
    id BIGSERIAL PRIMARY KEY,
    session_id BIGINT NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    chat_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Chat embeddings (vector embeddings for chat messages)
CREATE TABLE IF NOT EXISTS chat_embeddings (
    chat_id BIGINT PRIMARY KEY REFERENCES chats(id) ON DELETE CASCADE,
    embedding vector(384),
    chat_metadata JSONB DEFAULT '{}'::jsonb
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_id ON chat_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_chats_session_id ON chats(session_id);
CREATE INDEX IF NOT EXISTS idx_chats_user_id ON chats(user_id);
CREATE INDEX IF NOT EXISTS idx_chats_created_at ON chats(created_at);

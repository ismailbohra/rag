CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    content TEXT,
    metadata JSONB,
    embedding vector(768) -- adjust dimension based on your model
);

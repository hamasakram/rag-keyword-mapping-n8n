-- Initialize pgvector extension for vector operations
CREATE EXTENSION IF NOT EXISTS vector;

-- Create keywords table for storing keyword embeddings
CREATE TABLE IF NOT EXISTS keywords (
    id SERIAL PRIMARY KEY,
    keyword TEXT NOT NULL,
    embedding VECTOR(1536), -- matches Gemini embedding size
    used BOOLEAN DEFAULT FALSE
);

-- Add index on the embedding column for efficient similarity searches
CREATE INDEX IF NOT EXISTS idx_keywords_embedding ON keywords USING ivfflat (embedding vector_cosine_ops);

-- Add index on the keyword column for text searches
CREATE INDEX IF NOT EXISTS idx_keywords_keyword ON keywords (keyword);

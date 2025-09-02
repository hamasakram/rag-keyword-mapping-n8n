-- Initialize pgvector extension for vector operations
CREATE EXTENSION IF NOT EXISTS vector;

-- Enable UUID generation extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Create keywords table for storing keyword embeddings
CREATE TABLE IF NOT EXISTS keywords (
    id SERIAL PRIMARY KEY,
    keyword TEXT NOT NULL,
    embedding VECTOR(768), -- matches Gemini embedding size (768)
    used BOOLEAN DEFAULT FALSE
);

-- Add new metadata columns if they don't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'keywords' AND column_name = 'source_file'
    ) THEN
        ALTER TABLE keywords ADD COLUMN source_file TEXT;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'keywords' AND column_name = 'ingestion_batch_id'
    ) THEN
        ALTER TABLE keywords ADD COLUMN ingestion_batch_id UUID DEFAULT gen_random_uuid();
    END IF;
END $$;

-- Indexes
-- Add index on the embedding column for efficient similarity searches
CREATE INDEX IF NOT EXISTS idx_keywords_embedding ON keywords USING ivfflat (embedding vector_cosine_ops);

-- Add index on the keyword column for text searches
CREATE INDEX IF NOT EXISTS idx_keywords_keyword ON keywords (keyword);

-- Add index on ingestion_batch_id for faster filtering
CREATE INDEX IF NOT EXISTS idx_keywords_ingestion_batch_id ON keywords (ingestion_batch_id);

-- Create table to store product image descriptions and embeddings
CREATE TABLE IF NOT EXISTS product_descriptions (
    id SERIAL PRIMARY KEY,
    image_name TEXT,
    description TEXT,
    embedding VECTOR(768),
    meta JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for vector similarity search
CREATE INDEX IF NOT EXISTS idx_product_descriptions_embedding
ON product_descriptions USING ivfflat (embedding vector_cosine_ops);

-- Simple created_at index for recency queries
CREATE INDEX IF NOT EXISTS idx_product_descriptions_created_at
ON product_descriptions (created_at DESC);


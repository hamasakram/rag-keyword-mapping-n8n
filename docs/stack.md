# Tech Stack & Infrastructure

## Overview
RAG (Retrieval-Augmented Generation) Keyword Mapping System using n8n workflows and vector database technology.

## Core Infrastructure

### Database
- **PostgreSQL 15+** with **pgvector** extension
  - Vector similarity search capabilities
  - Optimized for 768-dimensional embeddings (Gemini API compatible)
  - Containerized deployment via Docker

### Database Schema
```sql
-- Keywords table structure
CREATE TABLE keywords (
    id SERIAL PRIMARY KEY,
    keyword TEXT NOT NULL UNIQUE,
    embedding VECTOR(768), -- matches Gemini embedding size (768)
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_file TEXT,
    ingestion_batch_id UUID DEFAULT gen_random_uuid(),
    meta JSONB
);

-- Performance indexes
CREATE INDEX idx_keywords_embedding ON keywords USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_keywords_keyword ON keywords (keyword);
CREATE INDEX idx_keywords_used ON keywords (used);
CREATE INDEX idx_keywords_ingestion_batch_id ON keywords (ingestion_batch_id);
```

### Vector Database Features
- **pgvector** extension for vector operations
- **IVFFlat** indexing for fast similarity searches
- **Cosine similarity** calculations
- **768-dimensional** embedding support (Gemini API standard)
- **UUID generation** via uuid-ossp extension
- **Cryptographic functions** via pgcrypto extension

## Development Environment

### Docker Services
- **PostgreSQL + pgvector**: `localhost:5432`
- **Adminer**: `localhost:8080` (Database administration interface)

### Environment Variables
```bash
# Database Configuration
PGHOST=localhost
PGPORT=5432
PGDATABASE=rag_keywords
PGUSER=postgres
PGPASSWORD=postgres

# Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# App
ENV=development
```

## AI & Embeddings

### Google Gemini API
- **Model**: `gemini-pro` for text generation
- **Embeddings**: `models/embedding-001` for vector generation
- **Vector Dimensions**: 768 (standard for Gemini embeddings)
- **API Integration**: Secure key management via environment variables

### Embedding Process
1. Keyword text input from CSV files
2. Gemini API embedding generation (768-dim vectors)
3. Vector storage in PostgreSQL with pgvector
4. Metadata storage in JSONB format
5. Similarity search capabilities

## Data Processing

### CSV Integration
- **Source**: `data/keywords.csv` with keyword and meta columns
- **Format**: Handles unquoted JSON in meta column
- **Processing**: Custom parser for CSV with embedded JSON
- **Batch Processing**: 51 keywords successfully processed

### Metadata Structure
```json
{
  "sv": 24000,        // Search volume
  "note": "electronics" // Category/note
}
```

## Workflow Automation

### n8n Platform
- **Purpose**: Orchestrate RAG keyword mapping workflows
- **Integration**: Connect database operations with AI services
- **Automation**: Streamline keyword processing and retrieval

## Project Structure
```
rag-keyword-mapping-n8n/
├── docker-compose.yml          # Database services
├── .env                        # Environment variables
├── infra/sql/
│   └── 001_init_keywords.sql  # Database initialization
├── data/
│   └── keywords.csv           # Keyword data with metadata
├── scripts/
│   └── embed_and_upsert.py    # Embedding generation script
├── docs/
│   └── stack.md               # This file
├── n8n/                       # n8n workflows
└── workflows/                 # Workflow definitions
```

## Key Features Implemented

### ✅ Phase 1: Infrastructure Setup
- Database infrastructure with pgvector
- Keywords table schema with proper indexing
- Docker containerization
- Database administration interface (Adminer)
- SQL initialization scripts
- Environment variable management

### ✅ Phase 2: Data Integration & Embeddings
- **51 keywords processed** with 768-dimensional embeddings
- **Gemini API integration** for vector generation
- **CSV data import** with metadata parsing
- **JSONB metadata storage** with search volume and categories
- **Batch processing script** (`embed_and_upsert.py`)
- **Vector similarity indexing** for fast searches
- **Source tracking** via source_file and ingestion_batch_id
- **UUID generation** for batch identification

### 🚧 Phase 3: Workflow Automation (Next)
- n8n workflow setup
- Keyword similarity search implementation
- RAG query system development
- Usage tracking and management
- API endpoints for keyword operations

## Performance Considerations

### Database Optimization
- **IVFFlat Index**: Fast approximate nearest neighbor search
- **Cosine Similarity**: Efficient vector comparison
- **Connection Pooling**: Optimized database connections
- **Batch Operations**: Support for bulk keyword processing
- **JSONB Indexing**: Fast metadata queries

### Scalability
- **Vector Dimensions**: 768-dimensional embeddings
- **Index Strategy**: IVFFlat for large-scale similarity search
- **Containerization**: Easy horizontal scaling
- **Stateless Design**: Workflow-based architecture
- **Batch Processing**: Efficient bulk operations

## Security & Best Practices

### Database Security
- **Environment Variables**: Secure credential management
- **Connection Encryption**: PostgreSQL SSL support
- **Access Control**: User-based permissions
- **UUID Generation**: Secure batch identification

### API Security
- **API Key Management**: Secure Gemini API access via .env
- **Input Validation**: Keyword sanitization
- **Rate Limiting**: API usage controls
- **Error Handling**: Comprehensive error management

## Monitoring & Logging

### Database Monitoring
- **Health Checks**: Container health monitoring
- **Performance Metrics**: Query execution times
- **Error Logging**: Comprehensive error tracking
- **Data Validation**: Row counts and embedding verification

### Application Logging
- **Structured Logging**: Detailed operation tracking
- **Progress Indicators**: Real-time processing feedback
- **Error Tracking**: Detailed error context
- **Success Metrics**: Processing completion statistics

## Deployment

### Local Development
```bash
# Start services
docker-compose up -d

# Set environment variables
export GEMINI_API_KEY=your_key_here

# Run embedding script
python scripts/embed_and_upsert.py

# Access services
# Database: localhost:5432
# Adminer: http://localhost:8080
```

### Production Considerations
- **Environment Variables**: Secure configuration management
- **Database Backups**: Automated backup strategies
- **Monitoring**: Production-grade monitoring and alerting
- **Scaling**: Horizontal scaling strategies
- **API Rate Limits**: Gemini API usage monitoring

## Current Status

### 🎯 **Phase 2 Complete: Data Integration & Embeddings**
- ✅ **51 keywords** with 768-dimensional embeddings stored
- ✅ **Metadata integration** with search volume and categories
- ✅ **Vector similarity search** ready for implementation
- ✅ **Batch processing** system operational
- ✅ **Database schema** optimized for RAG operations

### 📊 **Data Statistics**
- **Total Keywords**: 51
- **Embeddings Generated**: 51 (100%)
- **Vector Dimension**: 768
- **Categories**: electronics, furniture, wearables, photography, fitness, sportswear, nutrition, mobility, home_appliances, kitchen, music, home_decor, personal_care, beauty, baby_products, kids, outdoors, fashion
- **Search Volume Range**: 4,500 - 30,000

### 🚀 **Phase 3 In Progress: Image → Description → Embedding**
We now support a full image understanding path using Gemini vision + embeddings. See the Phase 3 section in the project `README.md` for usage, and a sample run using `data/Images/OIP.jpg` including Top‑K keyword retrieval.

High-level flow:
- Input: product image (e.g., `data/Images/OIP.jpg`)
- Vision caption: Gemini 1.5 Pro generates a concise description
- Embedding: `models/embedding-001` (768D) for parity with `keywords`
- Optional store: persist to `product_descriptions`
- Retrieval: cosine similarity against `keywords.embedding`
- Output: JSON with `description`, `embedding_dim`, optional `stored_id`, and `topk_keywords`


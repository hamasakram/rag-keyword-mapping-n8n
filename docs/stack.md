# Tech Stack & Infrastructure

## Overview
RAG (Retrieval-Augmented Generation) Keyword Mapping System using n8n workflows and vector database technology.

## Core Infrastructure

### Database
- **PostgreSQL 15+** with **pgvector** extension
  - Vector similarity search capabilities
  - Optimized for 1536-dimensional embeddings (Gemini API compatible)
  - Containerized deployment via Docker

### Database Schema
```sql
-- Keywords table structure
CREATE TABLE keywords (
    id SERIAL PRIMARY KEY,
    keyword TEXT NOT NULL UNIQUE,
    embedding VECTOR(1536),
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance indexes
CREATE INDEX idx_keywords_embedding ON keywords USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_keywords_keyword ON keywords (keyword);
CREATE INDEX idx_keywords_used ON keywords (used);
```

### Vector Database Features
- **pgvector** extension for vector operations
- **IVFFlat** indexing for fast similarity searches
- **Cosine similarity** calculations
- **1536-dimensional** embedding support (Gemini API standard)

## Development Environment

### Docker Services
- **PostgreSQL + pgvector**: `localhost:5432`
- **Adminer**: `localhost:8080` (Database administration interface)

### Environment Variables
```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=rag_keywords
DB_USER=postgres
DB_PASSWORD=postgres

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
```

## AI & Embeddings

### Google Gemini API
- **Model**: `gemini-pro` for text generation
- **Embeddings**: `models/embedding-001` for vector generation
- **Vector Dimensions**: 1536 (standard for Gemini embeddings)

### Embedding Process
1. Keyword text input
2. Gemini API embedding generation
3. Vector storage in PostgreSQL
4. Similarity search capabilities

## Workflow Automation

### n8n Platform
- **Purpose**: Orchestrate RAG keyword mapping workflows
- **Integration**: Connect database operations with AI services
- **Automation**: Streamline keyword processing and retrieval

## Project Structure
```
rag-keyword-mapping-n8n/
├── docker-compose.yml          # Database services
├── infra/sql/
│   └── 001_init_keywords.sql  # Database initialization
├── docs/
│   └── stack.md               # This file
├── n8n/                       # n8n workflows
├── scripts/                    # Utility scripts
└── workflows/                 # Workflow definitions
```

## Key Features Implemented

### ✅ Completed
- Database infrastructure with pgvector
- Keywords table schema with proper indexing
- Docker containerization
- Database administration interface (Adminer)
- SQL initialization scripts

### 🚧 In Progress
- n8n workflow setup
- Keyword embedding generation
- RAG query system

### 📋 Planned
- n8n workflow automation
- Keyword similarity search
- Usage tracking and management
- API endpoints for keyword operations

## Performance Considerations

### Database Optimization
- **IVFFlat Index**: Fast approximate nearest neighbor search
- **Cosine Similarity**: Efficient vector comparison
- **Connection Pooling**: Optimized database connections
- **Batch Operations**: Support for bulk keyword processing

### Scalability
- **Vector Dimensions**: 1536-dimensional embeddings
- **Index Strategy**: IVFFlat for large-scale similarity search
- **Containerization**: Easy horizontal scaling
- **Stateless Design**: Workflow-based architecture

## Security & Best Practices

### Database Security
- **Environment Variables**: Secure credential management
- **Connection Encryption**: PostgreSQL SSL support
- **Access Control**: User-based permissions

### API Security
- **API Key Management**: Secure Gemini API access
- **Input Validation**: Keyword sanitization
- **Rate Limiting**: API usage controls

## Monitoring & Logging

### Database Monitoring
- **Health Checks**: Container health monitoring
- **Performance Metrics**: Query execution times
- **Error Logging**: Comprehensive error tracking

### Application Logging
- **Structured Logging**: JSON-formatted log output
- **Log Levels**: Configurable logging verbosity
- **Error Tracking**: Detailed error context

## Deployment

### Local Development
```bash
# Start services
docker-compose up -d

# Access services
# Database: localhost:5432
# Adminer: http://localhost:8080
```

### Production Considerations
- **Environment Variables**: Secure configuration management
- **Database Backups**: Automated backup strategies
- **Monitoring**: Production-grade monitoring and alerting
- **Scaling**: Horizontal scaling strategies

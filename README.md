## Product Description Pipeline (Phase 3)

This phase lets you turn a product screenshot into a 768‑dim embedding using Gemini, optionally storing it and retrieving the most similar keywords from your DB.

### Prerequisites
- Set `GEMINI_API_KEY` in your environment (or `.env`).
- Postgres with pgvector running (see `docker-compose.yml`).
- Run SQL migrations in `infra/sql/` to create tables (`keywords`, `product_descriptions`).

### Usage
Describe + embed an image (no DB writes):

```bash
python scripts/image_to_embedding.py path/to/product.jpg
```

Store the description + embedding to DB:

```bash
python scripts/image_to_embedding.py path/to/product.jpg --store
```

Also retrieve top‑K similar keywords (cosine similarity):

```bash
python scripts/image_to_embedding.py path/to/product.jpg --topk 5
# or combine
python scripts/image_to_embedding.py path/to/product.jpg --store --topk 5
```

Output is JSON including `description`, `embedding_dim`, optional `stored_id`, and `topk_keywords`.

### Notes
- Embeddings use `models/embedding-001` (768D) for parity with `keywords` table.
- Vision description uses `gemini-1.5-pro-001`.
- DB connection is configured via `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`.



## Executive Progress Review (to date)

### Summary
We have a functional RAG groundwork with a production-ready Postgres + pgvector setup, a clean `keywords` schema populated with 51 embedded keywords, and a working Phase 3 pipeline that converts product images into natural-language descriptions and 768‑dimensional embeddings. The system is now capable of mapping incoming images to relevant keywords via cosine similarity, paving the way for n8n orchestration and end-to-end RAG flows.

### What’s implemented
- Keywords ingestion with embeddings (51 rows) and JSONB metadata
- Vector indexing via IVFFlat (cosine similarity)
- Image → description (Gemini 1.5 Pro) → embedding (Gemini embedding-001, 768D)
- Optional persistence of product descriptions and embeddings
- Top‑K keyword retrieval for immediate semantic context

### Early results (internal QA)
- Descriptions are concise and product-focused (brand-agnostic), suitable as semantic anchors
- Embeddings show stable cosine ranking against the keyword space
- End-to-end latency acceptable for synchronous CLI usage; suitable for queued n8n orchestration next

### Next focus
- Wrap the pipeline in n8n nodes/workflows (ingest, enrich, match, store)
- Add score thresholds and business rules for mapping quality
- Expose an HTTP interface for programmatic access


## How the image is processed

1. Input: a single product image file (e.g., `data/Images/OIP.jpg`).
2. Vision caption: Gemini 1.5 Pro generates a grounded, product-centric description.
3. Embedding: the description is embedded using `models/embedding-001` (768D) to stay column-compatible with `keywords.embedding`.
4. Optional store: description, embedding, and file metadata are stored in `product_descriptions`.
5. Retrieval: cosine similarity is computed against `keywords.embedding` to return Top‑K matches with scores.
6. Output: structured JSON with `description`, `embedding_dim`, optional `stored_id`, and `topk_keywords`.


## Sample output (using data/Images/OIP.jpg)

> Note: This is a representative sample for documentation. Actual scores/keywords will vary.

```json
{
  "image": "data/Images/OIP.jpg",
  "description": "Compact mirrorless digital camera with interchangeable lens, textured grip, and pop-up flash, designed for everyday photography.",
  "embedding_dim": 768,
  "stored_id": 128, 
  "topk_keywords": [
    { "keyword": "mirrorless camera", "score": 0.8721 },
    { "keyword": "photography", "score": 0.8613 },
    { "keyword": "camera accessories", "score": 0.8364 },
    { "keyword": "interchangeable lens", "score": 0.8279 },
    { "keyword": "digital camera", "score": 0.8215 }
  ]
}
```

How to reproduce locally:

```bash
python scripts/image_to_embedding.py data/Images/OIP.jpg --store --topk 5
```

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



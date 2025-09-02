import os
import csv
import json
import psycopg2
from psycopg2.extras import Json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("🚀 Starting keyword embedding script...")

# Configure Gemini client
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ Error: GEMINI_API_KEY environment variable not set")
    exit(1)

print(f"✅ Gemini API key configured: {api_key[:10]}...")
genai.configure(api_key=api_key)

# Database connection
print("🔌 Connecting to database...")
conn = psycopg2.connect(
    dbname=os.getenv("PGDATABASE", "rag_keywords"),
    user=os.getenv("PGUSER", "postgres"),
    password=os.getenv("PGPASSWORD", "postgres"),
    host=os.getenv("PGHOST", "localhost"),
    port=os.getenv("PGPORT", 5432),
)
cur = conn.cursor()
print("✅ Database connected successfully")

# Load CSV file
csv_path = os.path.join(os.path.dirname(__file__), "../data/keywords.csv")
print(f"📁 Loading CSV from: {csv_path}")

if not os.path.exists(csv_path):
    print(f"❌ Error: CSV file not found at {csv_path}")
    exit(1)

# Read file line by line to handle unquoted JSON
rows = []
with open(csv_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
    # Skip header
    for line in lines[1:]:
        line = line.strip()
        if line:
            # Split on first comma only
            parts = line.split(',', 1)
            if len(parts) == 2:
                keyword = parts[0].strip()
                meta_raw = parts[1].strip()
                rows.append({"keyword": keyword, "meta": meta_raw})
            else:
                print(f"⚠️ Skipping malformed line: {line}")

print(f"📊 Found {len(rows)} keywords to process")

for i, row in enumerate(rows):
    keyword = row["keyword"]
    meta_raw = row["meta"]
    
    print(f"🔄 Processing {i+1}/{len(rows)}: {keyword}")

    # Parse meta as JSON if present, else None
    try:
        meta = json.loads(meta_raw) if meta_raw else None
        if meta:
            print(f"  📋 Meta: {meta}")
    except json.JSONDecodeError:
        print(f"⚠️ Skipping invalid meta for keyword: {keyword}")
        meta = None

    # Check if keyword already exists
    cur.execute("SELECT id FROM keywords WHERE keyword = %s", (keyword,))
    existing = cur.fetchone()
    
    if existing:
        # Update existing record with meta
        try:
            cur.execute(
                "UPDATE keywords SET meta = %s WHERE keyword = %s",
                (Json(meta) if meta else None, keyword)
            )
            print(f"  ✅ Updated meta for existing keyword: {keyword}")
        except Exception as e:
            print(f"  ❌ Failed to update meta for {keyword}: {e}")
    else:
        # Generate embedding and insert new record
        try:
            response = genai.embed_content(
                model="models/embedding-001",  # Gemini embedding model
                content=keyword
            )
            embedding = response['embedding']  # Returns 768-dim vector
            print(f"  ✅ Generated embedding for: {keyword}")
            
            cur.execute(
                "INSERT INTO keywords (keyword, embedding, source_file, meta) VALUES (%s, %s, %s, %s)",
                (keyword, embedding, "keywords.csv", Json(meta) if meta else None)
            )
            print(f"  ✅ Inserted new keyword: {keyword}")
        except Exception as e:
            print(f"  ❌ Failed to process {keyword}: {e}")
            continue

print("💾 Committing changes...")
conn.commit()
cur.close()
conn.close()
print("🎉 Script completed successfully!")

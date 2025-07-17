import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from tqdm import tqdm
import os

tqdm.pandas()

DATA_PATH = "data/processed/movies_enriched.csv"
OUTPUT_PATH = "data/processed/movie_embeddings.npz"

print("🔍 Loading movie metadata...")
df = pd.read_csv(DATA_PATH)
df = df.dropna(subset=["overview"])
df["release_year"] = pd.to_datetime(df["release_date"], errors='coerce').dt.year
print(f"✅ Loaded {len(df)} movies with valid overviews.")

# Load Sentence-BERT model
print("🧠 Loading Sentence-BERT model (all-MiniLM-L6-v2)...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings with progress bar
print("⚙️ Generating semantic embeddings...")
# overviews = df["overview"].tolist()
def build_embedding_text(row):
    genres = row.get("genres", "")
    try:
        genre_names = ", ".join([g["name"] for g in eval(genres)]) if isinstance(genres, str) else ""
    except:
        genre_names = ""

    return f"{row['Title']} ({row['release_year']}) — {genre_names}. {row['overview']}"

texts = df.apply(build_embedding_text, axis=1).tolist()

print(texts[:5])

# embeddings = []
# for emb in tqdm(model.encode(texts, batch_size=32, show_progress_bar=False), total=len(texts), desc="📈 Encoding"):
#     embeddings.append(emb)

# embeddings = np.array(embeddings)

# # Save embeddings and metadata
# print("💾 Saving embeddings and metadata...")
# np.savez_compressed(OUTPUT_PATH,
#                     embeddings=embeddings,
#                     titles=df["Title"].tolist(),
#                     movie_ids=df["MovieID"].tolist())

# print("✅ Done! Embeddings saved to:", OUTPUT_PATH)

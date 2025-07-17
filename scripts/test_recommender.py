import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load metadata and embeddings
df = pd.read_csv("data/processed/movies_enriched.csv")
df.columns = df.columns.str.strip().str.lower()

embeddings_data = np.load("data/processed/movie_embeddings.npz")
embeddings = embeddings_data['embeddings']

# Create lowercase title lookup
titles = df['title'].dropna().tolist()
titles_lower = [t.lower() for t in titles]
title_to_idx = {t.lower(): i for i, t in enumerate(titles)}

# Ask user for input
query = input("🎬 Enter movie title: ").strip().lower()

# Try exact match first
idx = title_to_idx.get(query, None)

# If exact match fails, do partial search
if idx is None:
    partial_matches = [i for i, t in enumerate(titles_lower) if query in t]
    if not partial_matches:
        print(f"❌ Movie not found: {query}")
        exit()
    print(f"🔍 Using partial match: {titles[partial_matches[0]]}")
    idx = partial_matches[0]

# Compute similarity and recommend
query_vec = embeddings[idx].reshape(1, -1)
sims = cosine_similarity(query_vec, embeddings)[0]
top_indices = sims.argsort()[::-1][1:6]

print(f"\n🎬 Recommended for '{titles[idx]}':\n")
for i in top_indices:
    print(f"• {titles[i]} (score: {sims[i]:.4f})")

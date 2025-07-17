# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity

# # Load saved data
# DATA_PATH = "data/processed/movie_embeddings.npz"
# data = np.load(DATA_PATH, allow_pickle=True)

# embeddings = data["embeddings"]
# titles = data["titles"]
# movie_ids = data["movie_ids"]

# # Helper: recommend similar movies
# def get_similar_movies(query_title, top_k=5):
#     query_title = query_title.lower()
    
#     # Find index of query movie
#     try:
#         index = [title.lower() for title in titles].index(query_title)
#     except ValueError:
#         print(f"❌ Movie not found: {query_title}")
#         return []
    
#     query_vec = embeddings[index].reshape(1, -1)
    
#     # Compute cosine similarity
#     similarities = cosine_similarity(query_vec, embeddings).flatten()
#     similar_indices = similarities.argsort()[::-1][1:top_k+1]  # exclude itself

#     results = [(titles[i], similarities[i]) for i in similar_indices]
#     return results

# scripts/recommender.py

import difflib
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util

def load_data():
    movies = pd.read_csv("data/processed/movies_enriched.csv")
    data = np.load("data/processed/movie_embeddings.npz")
    embeddings = data["embeddings"]
    return movies, embeddings

def recommend_movies(movie_title, movies_df, embeddings, top_k=5):
    if not isinstance(movie_title, str):
        movie_title = str(movie_title).strip().lower()
    movie_title = movie_title.strip().lower()

    # Title matching
    all_titles = movies_df["matched_title"].fillna("").astype(str).tolist()
    match = difflib.get_close_matches(movie_title, all_titles, n=1, cutoff=0.6)

    if not match:
        return None

    matched_title = match[0]
    idx = movies_df[movies_df["matched_title"] == matched_title].index[0]

    # Now instead of comparing embeddings[idx] vs others (which may be weak),
    # encode the *user input* itself
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_text = movie_title
    query_vec = model.encode(query_text, convert_to_tensor=True)

    scores = util.cos_sim(query_vec, embeddings)[0].cpu().numpy()
    top_indices = scores.argsort()[::-1][:top_k]

    results = []
    for i in top_indices:
        row = movies_df.iloc[i]
        genres_str = ", ".join([g["name"] for g in row["genres"]]) if isinstance(row["genres"], list) else row["genres"]
        poster_url = f"https://image.tmdb.org/t/p/w500{row['poster_path']}" if pd.notna(row["poster_path"]) else None
        results.append({
            "title": row["Title"],
            "genres": genres_str,
            "overview": row["overview"],
            "poster_path": poster_url,
            "release_year": row["release_date"][:4] if pd.notna(row["release_date"]) else "Unknown",
            "score": float(scores[i])
        })

    return {
        "input_title": movies_df.iloc[idx]["Title"],
        "results": results
    }

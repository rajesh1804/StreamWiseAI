import pandas as pd
from fuzzywuzzy import fuzz
from tqdm import tqdm
import os

ml_path = "data/processed/movies.csv"
tmdb_path = "data/raw/tmdb/movies_metadata.csv"
out_path = "data/processed/movies_enriched.csv"

tqdm.pandas()

# Load MovieLens
ml = pd.read_csv(ml_path)
ml["CleanTitle"] = ml["Title"].str.extract(r"^(.*)\s\(\d{4}\)", expand=False).str.strip()

# Load TMDb metadata
tmdb = pd.read_csv(tmdb_path, low_memory=False)
tmdb = tmdb.dropna(subset=["title", "overview"])
tmdb["title_clean"] = tmdb["title"].str.lower().str.strip()

# Function to find best fuzzy match
def get_best_match(title, choices):
    scores = [(choice, fuzz.token_sort_ratio(str(title).lower(), choice)) for choice in choices]
    best = max(scores, key=lambda x: x[1])
    return best if best[1] > 80 else (None, 0)  # threshold

# Apply fuzzy matching
matches = ml["CleanTitle"].progress_apply(lambda x: get_best_match(x, tmdb["title_clean"].tolist()))
ml["matched_title"] = matches.apply(lambda x: x[0])
ml["match_score"] = matches.apply(lambda x: x[1])

# Merge on matched title
merged = ml.merge(tmdb, left_on="matched_title", right_on="title_clean", how="left")

# Keep relevant columns
keep_cols = [
    "MovieID", "Title", "Genres",
    "overview", "genres", "release_date", "poster_path", "matched_title", "match_score"
]
final = merged[keep_cols]
final.to_csv(out_path, index=False)

print("✅ Enriched metadata saved to:", out_path)

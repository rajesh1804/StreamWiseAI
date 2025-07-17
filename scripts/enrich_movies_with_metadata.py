import pandas as pd
from fuzzywuzzy import fuzz
from tqdm import tqdm
import ast

ml_path = "data/processed/movies.csv"
tmdb_path = "data/raw/tmdb/movies_metadata.csv"
out_path = "data/processed/movies_enriched2.csv"

tqdm.pandas()

# Load MovieLens
ml = pd.read_csv(ml_path)
ml["CleanTitle"] = ml["Title"].str.extract(r"^(.*)\s\(\d{4}\)", expand=False).str.strip()
ml.dropna(subset=['CleanTitle'], inplace=True)
ml['Year'] = ml['Title'].str.extract(r"\((\d{4})\)", expand=False)
ml['Genres'] = ml['Genres'].str.replace('|', ', ', regex=False)
ml['CleanTitle'] = ml['CleanTitle'].str.replace(r"\s*\(.*?\)", "", regex=True).str.strip()

# Load TMDb metadata
tmdb = pd.read_csv(tmdb_path, low_memory=False)
tmdb = tmdb.dropna(subset=["title", "overview"])
tmdb["title_clean"] = tmdb["title"].str.lower().str.strip()
tmdb['release_year'] = tmdb['release_date'].str[:4]
tmdb['genres'] = tmdb['genres'].apply(
    lambda x: ', '.join(d['name'] for d in ast.literal_eval(x) if 'name' in d)
)

# Function to find best fuzzy match
def get_best_match(title, year):
    choices = tmdb["title_clean"][tmdb["release_year"].astype(str)==year].tolist()
    scores = [(choice, fuzz.token_sort_ratio(str(title).lower(), choice)) for choice in choices]
    best = max(scores, key=lambda x: x[1])
    return best if best[1] > 80 else (None, 0)  # threshold


# Apply fuzzy matching
matches = ml[["CleanTitle", "Year"]].progress_apply(
    lambda x: get_best_match(
        x['CleanTitle'], 
        x['Year']
        ), 
    axis=1)
ml["matched_title"] = matches.apply(lambda x: x[0])
ml["match_score"] = matches.apply(lambda x: x[1])
ml.dropna(subset=['matched_title'], inplace=True)

# Merge on matched title
merged = ml.merge(tmdb, left_on="matched_title", right_on="title_clean", how="left")

def merge_unique_genres(col1, col2):
    # Split by comma and strip whitespace
    list1 = [x.strip() for x in col1.split(',')] if pd.notna(col1) else []
    list2 = [x.strip() for x in col2.split(',')] if pd.notna(col2) else []

    # Combine while preserving order and removing duplicates
    seen = set()
    merged = []
    for item in list1 + list2:
        if item not in seen:
            seen.add(item)
            merged.append(item)
    return ', '.join(merged)

merged['genres'] = merged.apply(lambda row: merge_unique_genres(row['Genres'], row['genres']), axis=1)


# Keep relevant columns
keep_cols = [
    "MovieID", "Title", "Genres", "CleanTitle",
    "overview", "genres", "release_date", "release_year", "poster_path", "matched_title", "match_score"
]
final = merged[keep_cols]
final.to_csv(out_path, index=False)

print("✅ Enriched metadata saved to:", out_path)

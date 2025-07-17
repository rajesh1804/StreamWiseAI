import pandas as pd
import os

RAW_DIR = "data/raw/movielens/ml-1m"
PROCESSED_DIR = "data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Read .dat files using correct encoding and separator
users = pd.read_csv(f"{RAW_DIR}/users.dat", sep="::", engine="python", encoding="latin-1",
                    names=["UserID", "Gender", "Age", "Occupation", "Zip-code"])

movies = pd.read_csv(f"{RAW_DIR}/movies.dat", sep="::", engine="python", encoding="latin-1",
                     names=["MovieID", "Title", "Genres"])

ratings = pd.read_csv(f"{RAW_DIR}/ratings.dat", sep="::", engine="python", encoding="latin-1",
                      names=["UserID", "MovieID", "Rating", "Timestamp"])

# Save cleaned CSVs
users.to_csv(f"{PROCESSED_DIR}/users.csv", index=False)
movies.to_csv(f"{PROCESSED_DIR}/movies.csv", index=False)
ratings.to_csv(f"{PROCESSED_DIR}/ratings.csv", index=False)

print("✅ Preprocessing complete. Cleaned CSVs saved to:", PROCESSED_DIR)

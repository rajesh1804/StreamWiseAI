import os
import zipfile
import urllib.request

DATA_DIR = "data/raw/movielens"
URL = "https://files.grouplens.org/datasets/movielens/ml-1m.zip"
ZIP_PATH = "data/raw/movielens/ml-1m.zip"

os.makedirs(DATA_DIR, exist_ok=True)

print("Downloading MovieLens 1M...")
urllib.request.urlretrieve(URL, ZIP_PATH)

with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
    zip_ref.extractall(DATA_DIR)

print("✅ Download complete. Extracted to:", DATA_DIR)

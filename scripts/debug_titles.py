import pandas as pd

df = pd.read_csv("data/processed/movies_enriched.csv")
df.columns = df.columns.str.strip().str.lower()

titles = df['title'].dropna().unique()
titles_lower = [t.lower() for t in titles]

# Search for 'toy story' match
matches = [t for t in titles_lower if 'toy story' in t]

print("Matching titles:")
print(matches if matches else "❌ No matches found for 'toy story'")

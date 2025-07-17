import streamlit as st
from scripts.recommender import load_data, recommend_movies
import ast

st.set_page_config(page_title="StreamWiseAI", layout="wide")
st.title("🎬 StreamWiseAI – Movie Recommender")

# Load data
movies, embeddings = load_data()

# Search input
movie_input = st.text_input("Enter a movie you liked", placeholder="e.g. Toy Story")

if movie_input:
    recommendations = recommend_movies(movie_input, movies, embeddings)
    
    if not recommendations:
        st.error("Movie not found. Please try another title.")
    else:
        st.subheader(f"📽️ Recommendations for **{recommendations['input_title']}**:")
        cols = st.columns(2)
        
        for idx, rec in enumerate(recommendations["results"]):
            with cols[idx % 2]:
                st.markdown(f"**{rec['title']}** ({rec['release_year']})")
                st.image(f"https://image.tmdb.org/t/p/w200{rec['poster_path']}", width=120)

                # Parse genre string and extract names
                genres = []
                try:
                    genre_list = ast.literal_eval(rec["genres"])
                    if isinstance(genre_list, list):
                        genres = [g["name"] for g in genre_list if isinstance(g, dict) and "name" in g]
                except (ValueError, SyntaxError):
                    pass
                genre_text = " / ".join(genres) if genres else "Unknown genre"
                st.markdown(f"*Genre(s): {genre_text}*")

                st.markdown(f"_{rec['overview']}_")
                st.markdown("---")

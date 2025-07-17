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

                st.markdown(f"*Genre(s): {rec['genres']}*")

                st.markdown(f"_{rec['overview']}_")
                st.markdown("---")

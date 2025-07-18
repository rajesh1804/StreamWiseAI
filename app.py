import streamlit as st
from scripts.recommender import load_data, recommend_movies
from agent import generate_retention_tip

st.set_page_config(page_title="StreamWiseAI", layout="wide")
st.title("🎬 StreamWiseAI – Movie Recommender")

# Load data
movies, embeddings = load_data()

# Search input
movie_input = st.text_input("Enter a movie you liked", placeholder="e.g. Toy Story")
show_tip = st.checkbox("💡 Show retention insight from AI coach?", value=True)

if movie_input:
    with st.spinner("Finding great recommendations..."):
        recommendations = recommend_movies(movie_input, movies, embeddings)

        if not recommendations:
            st.error("❌ Movie not found. Please try another title.")
        else:
            st.subheader(f"📽️ Recommendations for **{movie_input}**")

            cols = st.columns(2)

            for idx, rec in enumerate(recommendations["results"]):
                with cols[idx % 2]:
                    with st.container():
                        st.markdown("#### 🎬 " + rec['title'] + f" ({rec['release_year']})")

                        # Fallback-safe image
                        if rec['poster_path']:
                            st.image(f"https://image.tmdb.org/t/p/w200{rec['poster_path']}", width=150)
                        else:
                            st.image("https://via.placeholder.com/150x225.png?text=No+Image", width=150)

                        st.markdown(f"**🎭 Genre(s):** {rec['genres']}")
                        st.markdown(f"**🧠 Similarity Score:** {rec['similarity']:.2f}")
                        
                        # Truncate overview if too long
                        short_overview = rec['overview']
                        if len(short_overview) > 250:
                            short_overview = short_overview[:250] + "..."
                        st.markdown(f"_{short_overview}_")

                        st.markdown("---")

            if show_tip:
                with st.spinner("🧠 Generating retention insight..."):
                    tip = generate_retention_tip(movie_input, recommendations["results"])
                    if tip and not tip.startswith("⚠️"):
                        st.markdown("### 💡 Retention Coach Tip")
                        st.info(tip)
                    else:
                        st.warning("Couldn't generate tip at the moment.")


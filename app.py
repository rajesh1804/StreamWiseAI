import streamlit as st
from scripts.recommender import load_data, recommend_movies
from agent import generate_retention_tip

st.set_page_config(page_title="StreamWiseAI", layout="wide")
st.title("🎬 StreamWiseAI – Personalized Movie Recommender & Retention Coach")
st.caption("🤖 Powered by AI Agents · 🎯 Smart Search · 🧠 AI Insights")


# Load data
movies, embeddings = load_data()

# Initialize watch history
if "watch_history" not in st.session_state:
    st.session_state["watch_history"] = []

# Search input
movie_input = st.text_input("Enter a movie you liked", placeholder="e.g. Toy Story")
show_tip = st.checkbox("💡 Show retention insight from AI coach?", value=True)

if movie_input:
    with st.spinner("Finding great recommendations..."):
        recommendations = recommend_movies(movie_input, movies, embeddings)

        if not recommendations:
            st.error("❌ Movie not found. Please try another title.")
        else:
            st.subheader(f"📽️ Recommendations for **{recommendations['input_title']}**")

            if recommendations["input_title"] not in st.session_state["watch_history"]:
                st.session_state["watch_history"].append(recommendations["input_title"])

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
                with st.spinner("🤖 Retention Coach is analyzing your taste..."):
                    tip = generate_retention_tip(movie_input, recommendations["results"], st.session_state.get("watch_history", []))
                    if tip and not tip.startswith("⚠️"):
                        st.markdown("### 💡 Retention Coach Suggests:")
                        st.markdown(f"""
                        <div style="background-color:#f0f8ff; padding:15px; border-radius:10px; border-left:5px solid #1f77b4;">
                            <span style="font-size:16px;">{tip}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("Couldn't generate tip at the moment.")

with st.sidebar:
    st.markdown("## 🎬 **About StreamWiseAI**")
    
    st.markdown("""
<span style='color:#6c63ff'><strong>StreamWiseAI</strong></span> is a personalized movie discovery engine designed for modern streaming platforms.

Built to impress recruiters and mimic real-world production use cases, it features:
    
🔍 <span style='color:#FFA500'><strong>Semantic Search</strong></span> — understands meaning, not just keywords  
🧠 <span style='color:#00BFFF'><strong>AI Retention Coach</strong></span> — LLM agent gives viewing tips  
🗂️ <span style='color:#32CD32'><strong>Watch History Memory</strong></span> — tracks user session dynamically  
🚀 <span style='color:#FF69B4'><strong>Built for Showcase</strong></span> — Fast, deployable & recruiter-friendly  

---

<small><i>Tech stack: Sentence Transformers · Streamlit · OpenRouter LLM API · Fuzzy Matching · npz Vector Index</i></small>
""", unsafe_allow_html=True)


if st.session_state["watch_history"]:
    st.markdown("---")
    with st.expander("👀 View your recently searched movies"):
        st.markdown("\n".join(f"- {title}" for title in st.session_state["watch_history"]))

st.markdown("---")
st.markdown(
    "<small>🚀 Built by Rajesh Marudhachalam</small>",
    unsafe_allow_html=True
)
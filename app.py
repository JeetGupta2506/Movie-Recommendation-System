import streamlit as st
import pickle
import pandas as pd
import os
from PIL import Image
import requests
from io import BytesIO

# Page Configuration
st.set_page_config(
    page_title="🎬 Movie Recommender",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .movie-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    .recommendation-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 2rem;
    }
    
    .sidebar-content {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Check if files exist before loading
@st.cache_data
def load_data():
    if not os.path.exists("movies.pkl") or not os.path.exists("similarity.pkl"):
        st.error("🔴 Error: Required data files (`movies.pkl`, `similarity.pkl`) are missing!")
        st.info("""
        **To use this app, you need:**
        1. `movies.pkl` - DataFrame with movie data including 'movie_name' and optionally 'Poster_URL'
        2. `similarity.pkl` - Similarity matrix for movie recommendations
        
        **Sample data structure:**
        - movies.pkl should contain a DataFrame with columns: ['movie_name', 'Poster_URL', 'genre', 'year', 'rating']
        - similarity.pkl should contain a 2D numpy array with similarity scores
        """)
        st.stop()
    
    try:
        df = pickle.load(open("movies.pkl", "rb"))
        similarity = pickle.load(open("similarity.pkl", "rb"))
        return df, similarity
    except Exception as e:
        st.error(f"Error loading data files: {str(e)}")
        st.stop()

# Load data
df, similarity = load_data()

# Default poster URL
DEFAULT_POSTER_URL = "https://via.placeholder.com/300x450/667eea/white?text=No+Poster"

# Function to fetch and display movie poster
def fetch_poster(movie_name):
    """Fetch movie poster URL from the dataset"""
    if "Poster_URL" not in df.columns:
        return DEFAULT_POSTER_URL
    
    filtered_df = df[df["movie_name"] == movie_name]
    if not filtered_df.empty and pd.notna(filtered_df["Poster_URL"].values[0]):
        return filtered_df["Poster_URL"].values[0]
    return DEFAULT_POSTER_URL

def get_movie_details(movie_name):
    """Get additional movie details if available"""
    movie_data = df[df["movie_name"] == movie_name]
    if not movie_data.empty:
        details = {}
        if "genre" in df.columns:
            details["genre"] = movie_data["genre"].values[0] if pd.notna(movie_data["genre"].values[0]) else "N/A"
        if "year" in df.columns:
            details["year"] = movie_data["year"].values[0] if pd.notna(movie_data["year"].values[0]) else "N/A"
        if "rating" in df.columns:
            details["rating"] = movie_data["rating"].values[0] if pd.notna(movie_data["rating"].values[0]) else "N/A"
        return details
    return {}

# Function to recommend movies
def recommend(movie):
    """Generate movie recommendations based on similarity"""
    if movie not in df["movie_name"].values:
        return [], []

    index_list = df.index[df["movie_name"] == movie].tolist()
    if not index_list:
        return [], []

    index = index_list[0]
    distances = sorted(enumerate(similarity[index]), key=lambda x: x[1], reverse=True)

    recommended_movies = [df.iloc[i[0]]["movie_name"] for i in distances[1:6]]
    recommended_posters = [fetch_poster(movie) for movie in recommended_movies]

    return recommended_movies, recommended_posters

# Main App Header
st.markdown("""
<div class="main-header">
    <h1>🎬 Indian Movie Recommender System</h1>
    <p>Discover your next favorite movie with AI-powered recommendations!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.title("🔍 Movie Search")
    st.write("Select a movie to get personalized recommendations")
    
    # Search functionality
    search_term = st.text_input("🔎 Search movies:", placeholder="Type to search...")
    
    # Filter movies based on search
    if search_term:
        filtered_movies = df[df["movie_name"].str.contains(search_term, case=False, na=False)]["movie_name"].values
        if len(filtered_movies) == 0:
            st.warning("No movies found matching your search!")
            filtered_movies = df["movie_name"].values
    else:
        filtered_movies = df["movie_name"].values
    
    # Movie selection
    movie_name = st.selectbox("🎥 Choose a movie:", filtered_movies, key="movie_select")
    
    # ... sidebar content continues (dataset info removed)
    st.markdown('</div>', unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 🎭 Selected Movie")
    if movie_name:
        # Display selected movie poster
        poster_url = fetch_poster(movie_name)
        try:
            st.image(poster_url, width=250, caption=movie_name)
        except:
            st.image(DEFAULT_POSTER_URL, width=250, caption=movie_name)
        
        # Display movie details if available
        details = get_movie_details(movie_name)
        if details:
            st.markdown("**Movie Details:**")
            for key, value in details.items():
                st.write(f"**{key.title()}:** {value}")

with col2:
    st.markdown("### 🎯 Get Recommendations")
    
    # Recommendation button
    if st.button("🚀 Find Similar Movies", type="primary", use_container_width=True):
        with st.spinner("🔎 Analyzing movie preferences and finding similar movies..."):
            recommendations, posters = recommend(movie_name)
            
            if not recommendations:
                st.error("❌ No recommendations found. Please try another movie.")
            else:
                st.success(f"✅ Found {len(recommendations)} similar movies!")
                
                # Display recommendations in a grid
                st.markdown("### 🎬 Recommended Movies")
                
                # Create columns for recommendations
                cols = st.columns(len(recommendations))
                
                for i, (movie, poster) in enumerate(zip(recommendations, posters)):
                    with cols[i]:
                        try:
                            st.image(poster if poster else DEFAULT_POSTER_URL, 
                                   use_container_width=True, 
                                   caption=f"#{i+1}")
                            st.markdown(f"**{movie}**")
                            
                            # Add movie details if available
                            movie_details = get_movie_details(movie)
                            if movie_details:
                                if "rating" in movie_details and movie_details["rating"] != "N/A":
                                    st.markdown(f"⭐ {movie_details['rating']}")
                                if "year" in movie_details and movie_details["year"] != "N/A":
                                    st.markdown(f"📅 {movie_details['year']}")
                        except Exception as e:
                            st.image(DEFAULT_POSTER_URL, use_container_width=True)
                            st.markdown(f"**{movie}**")
                            st.caption("Poster unavailable")


import streamlit as st
import pickle
import pandas as pd
import os

# Check if files exist before loading
if not os.path.exists("movies.pkl") or not os.path.exists("similarity.pkl"):
    st.error("🔴 Error: Required data files (`movies.pkl`, `similarity.pkl`) are missing!")
    st.stop()

# Load Pickle Files
df = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# ✅ Corrected Default Poster Image (Valid Direct Link)
DEFAULT_POSTER_URL = "https://www.indieactivity.com/wp-content/uploads/2022/03/File-Not-Found-Poster.png"

# Function to Fetch Movie Poster
def fetch_poster(movie_name):
    if "Poster_URL" not in df.columns:
        st.warning("⚠️ Warning: 'Poster_URL' column not found in dataset!")
        return None
    
    filtered_df = df[df["movie_name"] == movie_name]
    if not filtered_df.empty and pd.notna(filtered_df["Poster_URL"].values[0]):
        return filtered_df["Poster_URL"].values[0]
    return None  # Return None if poster not found

# Function to Recommend Movies
def recommend(movie):
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

# Streamlit UI
st.title("🎬 Indian Movie Recommender System")
st.write("Find movies similar to your favorite! 🚀")

# Sidebar
st.sidebar.title("🔍 Search & Filter")
st.sidebar.write("Use the dropdown to select a movie and find recommendations.")

# Movie Selection Dropdown
movie_name = st.selectbox("🎥 Choose a movie", df["movie_name"].values)

# Recommendation Button with Spinner
if st.button("Recommend"):
    with st.spinner("🔎 Finding similar movies..."):
        recommendations, posters = recommend(movie_name)
        
        if not recommendations:
            st.error("❌ Movie not found. Please try another.")
        else:
            st.write("### 🎬 Recommended Movies:")
            
            cols = st.columns(5)  # Create 5 columns for images
            for i in range(len(recommendations)):
                with cols[i]:  # Place each movie in a separate column
                    st.image(posters[i] if posters[i] else DEFAULT_POSTER_URL, use_container_width=True)
                    st.write(f"✅ {recommendations[i]}")



# 🎬 Indian Movie Recommendation System

A modern, interactive web app built with Streamlit that recommends Indian movies based on your selection. Powered by a similarity matrix and a curated movie dataset, it helps you discover your next favorite film with ease.

## Features
- Search and filter movies by name
- Get AI-powered recommendations for similar movies
- View movie posters and details (genre, year, rating)
- Responsive, user-friendly UI with sidebar controls
- No coding required — just run and explore!

## Demo
![App Screenshot](https://via.placeholder.com/800x300?text=Movie+Recommender+Demo)

## Getting Started

### 1. Clone the repository
```powershell
git clone <your-repo-url>
cd Movie-Recommendation-System
```

### 2. Install dependencies
Make sure you have Python 3.8+ installed. Then run:
```powershell
pip install streamlit pandas pillow requests
```

### 3. Prepare the data
Place the following files in the project root:
- `movies.pkl` — a pickled pandas DataFrame with columns:
    - `movie_name` (str): Movie title
    - `Poster_URL` (str, optional): URL to poster image
    - `genre` (str, optional): e.g. "Action, Drama"
    - `year` (int/str, optional): Release year
    - `rating` (float/str, optional): Movie rating
- `similarity.pkl` — a pickled 2D numpy array (similarity matrix)

> **Tip:** You can use the provided `IMDB-Movie-Dataset(2023-1951).csv` as a starting point and preprocess it to create `movies.pkl` and `similarity.pkl`.

### 4. Run the app
```powershell
streamlit run app.py
```
The app will open in your browser at http://localhost:8501

## Usage
- Use the sidebar to search for a movie.
- Select a movie to see its poster and details.
- Click "Find Similar Movies" to get recommendations.
- Click on a recommended movie to view its details.

## File Structure
```
Movie-Recommendation-System/
├── app.py                  # Main Streamlit app
├── fill.py                 # (Optional) Data preparation script
├── movies.pkl              # Movie DataFrame (required)
├── similarity.pkl          # Similarity matrix (required)
├── IMDB-Movie-Dataset...   # Raw CSV dataset
├── Updated_Movie_Dataset...# Processed CSVs
├── README.md               # This file
```

## Customization
- To change the look and feel, edit the CSS in `app.py`.
- To use a different dataset, update `movies.pkl` and `similarity.pkl`.

## License
This project is for educational and personal use. Please credit the original dataset sources if you share or deploy it.

---
Made with ❤️ using Streamlit.

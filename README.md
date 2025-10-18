# 🎬 Indian Movie Recommender System  

Discover your next favorite movie with AI-powered recommendations!
Built with Streamlit, Python, and Machine Learning, this interactive web app helps users find movies similar to their favorites based on content similarity.

## 🚀 Features 

- **AI-Powered Recommendations** — Suggests top 5 similar movies using pre-trained similarity matrices.  
- **Interactive UI** — Beautiful and responsive layout built with Streamlit and custom CSS.  
- **Poster Previews** — Displays movie posters dynamically (or a fallback image if unavailable).  
- **Detailed Movie Info** — Shows genre, year, and rating where available.  
- **Search Functionality** — Easily search and filter movies from the dataset.  
- **Error Handling** — Gracefully handles missing files or data issues.  

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 
- **ML/Data**: Pandas, Pickle (for loading data), NumPy (via similarity matrix)
- **Other**: PIL (for images), Requests 


## 📸 ScreenShots

![Landing page](<screenshots/Landing.png>)
![Report](<screenshots/report.png>)
![Chatbot](<screenshots/chatbot.jpg>)

## 💡 How It Works

- The user selects or searches for a movie.

- The app finds the corresponding index in the similarity matrix.

- It computes similarity scores and fetches the top 5 similar movies.

- The results are displayed with posters and movie details in a responsive grid layout.

## 🚀 How to Run the App Locally

1. **Clone the Repository**: 

   ```bash
   git clone https://github.com/JeetGupta2506/Movie-Recommendation-System
   cd Movie-Recommender-System
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**:

   ```bash
   streamlit run app.py
   ```


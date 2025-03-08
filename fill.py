import pandas as pd
import requests
import time

# Load the dataset
df = pd.read_csv("Updated_Movie_Dataset.csv")

# OMDb API configuration
API_KEY = "your_omdb_api_key"  # Replace with your OMDb API key
API_URL = "http://www.omdbapi.com/"

# Function to fetch poster URL from OMDb
def fetch_poster_url(movie_name, year):
    params = {"t": movie_name, "y": year, "apikey": API_KEY}
    try:
        response = requests.get(API_URL, params=params)
        data = response.json()
        if data.get("Response") == "True":
            return data.get("Poster")
    except Exception as e:
        print(f"Error fetching poster for {movie_name}: {e}")
    return None

# Iterate over the dataset and fetch missing poster URLs
for index, row in df.iterrows():
    if pd.isna(row["Poster_URL"]):
        poster_url = fetch_poster_url(row["movie_name"], row["year"])
        if poster_url:
            df.at[index, "Poster_URL"] = poster_url
        time.sleep(1)  # Delay to avoid hitting API limits

# Save the updated dataset
df.to_csv("Updated_Movie_Dataset_With_Posters.csv", index=False)
print("✅ Dataset updated successfully!")

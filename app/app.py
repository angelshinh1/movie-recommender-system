import streamlit as st
import pickle
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct full paths to the pickle files
movies_list_path = os.path.join(script_dir, "extracted_movies.pkl")
similarity_path = os.path.join(script_dir, "similarity.pkl")

# Try to load pickle files with error handling
try:
    with open(movies_list_path, "rb") as f:
        movies_list = pickle.load(f)

    with open(similarity_path, "rb") as f:
        similarity = pickle.load(f)
except FileNotFoundError as e:
    st.error(f"Error loading data files: {e}")
    st.error(f"Current script directory: {script_dir}")
    st.error(f"Attempted to load from: {movies_list_path} and {similarity_path}")
    st.stop()  # Stop the app from running further


def recommend_movie(movie):
    # get the index of the movie
    idx = movies_list[movies_list["title"] == movie].index[0]

    distances = similarity[idx]

    result = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
        1:6
    ]  # get the top 5 similar movies
    recommended_movies = []
    for i in result:
        recommended_movies.append(movies_list.iloc[i[0]].title)

    return recommended_movies


st.title("My Movie Recommender App")

# Check if movies_list is loaded before creating selectbox
if "movies_list" in locals():
    option = st.selectbox("Please select a movie", movies_list["title"].values)

    if st.button("Give suggestion"):
        suggestions = recommend_movie(option)
        for i in suggestions:
            st.write(i)
else:
    st.error("Failed to load movie data. Please check the data files.")

st.markdown(
    """
<a href="https://github.com/angelshinh1/movie-recommender-system" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-Repo-blue?logo=github" alt="GitHub Repo">
</a>
<a href="https://github.com/angelshinh1" target="_blank">
    <img src="https://img.shields.io/badge/Follow--me-black?style=social&logo=github" alt="Follow Me">
</a>
""",
    unsafe_allow_html=True,
)

import streamlit as st
import pickle
import os
import sys
import pandas as pd

# Determine the base directory for the app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct full paths to the pickle files
MOVIES_LIST_PATH = os.path.join(BASE_DIR, "extracted_movies.pkl")
SIMILARITY_PATH = os.path.join(BASE_DIR, "similarity.pkl")


def load_pickle_file(file_path):
    """
    Safely load a pickle file with comprehensive error handling
    """
    try:
        with open(file_path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        st.error(f"Error loading pickle file {file_path}: {e}")
        st.error(f"Full file path: {os.path.abspath(file_path)}")
        st.error(f"File exists: {os.path.exists(file_path)}")
        st.error(f"Current working directory: {os.getcwd()}")
        st.error(f"Base directory: {BASE_DIR}")
        return None


# Load pickle files
try:
    movies_list = load_pickle_file(MOVIES_LIST_PATH)
    similarity = load_pickle_file(SIMILARITY_PATH)

    # Validate loaded data
    if movies_list is None or similarity is None:
        st.error("Failed to load required data files.")
        st.stop()

    # Ensure movies_list is a DataFrame
    if not isinstance(movies_list, pd.DataFrame):
        st.error(f"Expected DataFrame, got {type(movies_list)}")
        st.stop()

except Exception as e:
    st.error(f"Unexpected error during data loading: {e}")
    st.stop()


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

# Movie selection and recommendation
option = st.selectbox("Please select a movie", movies_list["title"].values)

if st.button("Give suggestion"):
    suggestions = recommend_movie(option)
    for i in suggestions:
        st.write(i)

# Additional information section
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

# Debug information (optional, can be removed in production)
with st.expander("Debug Information"):
    st.write("### Pickle File Details")
    st.write(f"Movies List Path: {MOVIES_LIST_PATH}")
    st.write(f"Movies List Path Exists: {os.path.exists(MOVIES_LIST_PATH)}")
    st.write(f"Similarity Path: {SIMILARITY_PATH}")
    st.write(f"Similarity Path Exists: {os.path.exists(SIMILARITY_PATH)}")
    st.write(f"Base Directory: {BASE_DIR}")
    st.write(f"Current Working Directory: {os.getcwd()}")

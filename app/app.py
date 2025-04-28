import streamlit as st
import pickle

movies_list = pickle.load(open("extracted_movies.pkl", "rb"))

similarity = pickle.load(open("similarity.pkl", "rb"))

def recommend_movie(movie):
    # get the index of the movie
    idx = movies_list[movies_list['title'] == movie].index[0]
    
    distances = similarity[idx]

    result = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6] # get the top 5 similar movies
    recommended_movies = []
    for i in result:
        recommended_movies.append(movies_list.iloc[i[0]].title) 
    
    return recommended_movies

st.title("My movie recommender app")

option = st.selectbox(
    "Please select a movie",
    movies_list['title'].values
) 

if st.button('Give suggestion'):
    suggestions = recommend_movie(option)
    for i in suggestions:
        st.write(i)

import streamlit as st
import pickle
import pandas as pd

def fetch_img(idx):
    data = final.iloc[idx]['poster_path']
    return "https://image.tmdb.org/t/p/w500/" + data

def recommend(movie):
    movie_index = final[final['title_x'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:9]
    recommended_movies = []
    posters = []
    for i in movie_list:
        movie_id = i[0]
        recommended_movies.append(final.iloc[movie_id].title_x)
        posters.append(fetch_img(movie_id))
    return recommended_movies, posters

# Load data
final_data = pickle.load(open('movie_dict.pkl', 'rb'))
final = pd.DataFrame(final_data)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Page config
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# Title
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>Movie Recommender System 🍿</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Find movies similar to your favorite one — instantly!</p>", unsafe_allow_html=True)

# Dropdown
option = st.selectbox(
    'Choose a movie to get recommendations:',
    final['title_x'].values
)

# Button
if st.button('Show Recommendations'):
    names, posters = recommend(option)

    # Show recommendations in 2 rows of 4
    for i in range(0, 8, 4):
        cols = st.columns(4)
        for idx, col in enumerate(cols):
            if i + idx < len(names):
                with col:
                    st.image(posters[i + idx], use_container_width=True)
                    st.markdown(f"<p style='text-align: center; font-weight: bold;'>{names[i + idx]}</p>", unsafe_allow_html=True)

# Footer
st.markdown("---")

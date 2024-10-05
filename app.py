import streamlit as st
import pickle
import pandas as pd
import requests

def fetc_mov(movie_id):
    res = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=380f074ced27d70293b987341d0467a7&language=en-US'.format(movie_id))
    data = res.json()

    #st.text(data)
    #st.text('https://api.themoviedb.org/3/movie/{}?api_key=380f074ced27d70293b987341d0467a7&language=en-US'.format(movie_id))

    return "https://image.tmdb.org/t/p/w92/" + data['poster_path']

# Load movie data and similarity matrix
movies_dict = pickle.load(open('moviesdict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Recommendation function
def Recommendd(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    rec_movies = []
    rec_movies_pos = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        rec_movies.append(movies.iloc[i[0]].title)
        rec_movies_pos.append(fetc_mov(movie_id))
    return rec_movies, rec_movies_pos

# Debugging line


# Selectbox for movie selection
selected_movie_name = st.selectbox(
    'Select a movie for recommendations:',
    movies['title'].values
)

# Display the selected movie for debugging
st.write(f"You selected: {selected_movie_name}")

# Button to trigger recommendation
if st.button('Recommend'):
    recommendations, posters = Recommendd(selected_movie_name)

    col1, col2, col3,col4,col5 = st.columns(5)  # Changed from st.beta_columns to st.columns
    with col1:
        st.text(recommendations[0])
        st.image(posters[0])

    with col2:
        st.text(recommendations[1])
        st.image(posters[1])

    with col3:
        st.text(recommendations[2])
        st.image(posters[2])

    with col4:
        st.text(recommendations[3])
        st.image(posters[3])

    with col5:
        st.text(recommendations[4])
        st.image(posters[4])


import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path', '')
    full_path = "http://image.tmdb.org/t/p/w500" + poster_path
    return full_path

def recommend(movie_df):
    index = movies[movies['title'] == movie_df].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_name = []
    recommended_movie_poster = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_poster.append(fetch_poster(movie_id))
        recommended_movie_name.append(movies.iloc[i[0]].title)
    return recommended_movie_name, recommended_movie_poster

# Initialize or load recommendation history
if 'history_names' not in st.session_state:
    st.session_state.history_names = []
if 'history_posters' not in st.session_state:
    st.session_state.history_posters = []

st.header("Movie Recommendation System Using Machine Learning")

try:
    with open('artificats/movie_list.pkl', 'rb') as f:
        movies = pickle.load(f)
    with open('artificats/similary.pkl', 'rb') as f:
        similarity = pickle.load(f)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

movie_list = movies['title'].values
selected_movie = st.selectbox('Type or select a movie to get recommendation', movie_list)

# Initialize filtered_movie_name to avoid errors
filtered_movie_name = []
filtered_movie_poster = []

if st.button('Show recommendation'):
    recommended_movie_name, recommended_movie_poster = recommend(selected_movie)

    # Filter out movies that are already in the history from the current recommendations
    for name, poster in zip(recommended_movie_name, recommended_movie_poster):
        if name not in st.session_state.history_names:
            filtered_movie_name.append(name)
            filtered_movie_poster.append(poster)

    # Add only the newly recommended movies to history
    st.session_state.history_names.extend(filtered_movie_name)
    st.session_state.history_posters.extend(filtered_movie_poster)

    # Limit history to the last 15 movies
    st.session_state.history_names = st.session_state.history_names[-15:]
    st.session_state.history_posters = st.session_state.history_posters[-15:]

# Display current recommendations (those not in history)
if filtered_movie_name:
    st.subheader("Current Recommendations")
    cols = st.columns(5)  # Create 5 columns for layout
    for col, name, poster in zip(cols, filtered_movie_name, filtered_movie_poster):
        with col:
            # Display the movie name as a button
            if st.button(name):  
                st.write(f"You selected {name}!")  # You can replace this with any other action
            st.image(poster)  # Display the movie poster

# Display movie recommendation history (up to 15 movies), excluding movies in current recommendations
if st.session_state.history_names:
    st.subheader("Recommendation History")
    
    # Filter out current recommendations from history
    history_filtered_names = [name for name in st.session_state.history_names if name not in filtered_movie_name]
    history_filtered_posters = [poster for name, poster in zip(st.session_state.history_names, st.session_state.history_posters) if name not in filtered_movie_name]
    
    if history_filtered_names:
        cols = st.columns(5)
        for col, name, poster in zip(cols * 3, history_filtered_names, history_filtered_posters):
            with col:
                st.text(name)
                st.image(poster)

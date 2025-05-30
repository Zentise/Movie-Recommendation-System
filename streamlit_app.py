import streamlit as st
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------- Data Preprocessing (same as before) --------

@st.cache_data
def load_data():
    movies_df = pd.read_csv("data/tmdb_5000_movies.csv")
    credits_df = pd.read_csv("data/tmdb_5000_credits.csv")
    movies_df = movies_df.merge(credits_df, on='title')
    movies_df = movies_df[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    
    def convert(obj):
        try:
            return [i['name'] for i in ast.literal_eval(obj)]
        except:
            return []

    def get_director(obj):
        try:
            return [i['name'] for i in ast.literal_eval(obj) if i['job'] == 'Director']
        except:
            return []

    def collapse(L):
        return " ".join(L)

    movies_df.dropna(inplace=True)
    movies_df['genres'] = movies_df['genres'].apply(convert)
    movies_df['keywords'] = movies_df['keywords'].apply(convert)
    movies_df['cast'] = movies_df['cast'].apply(lambda x: convert(x)[:3])
    movies_df['crew'] = movies_df['crew'].apply(get_director)
    movies_df['overview'] = movies_df['overview'].apply(lambda x: x.split())
    movies_df['tags'] = movies_df['overview'] + movies_df['genres'] + movies_df['keywords'] + movies_df['cast'] + movies_df['crew']
    movies_df['tags'] = movies_df['tags'].apply(collapse)

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies_df['tags']).toarray()
    similarity = cosine_similarity(vectors)

    return movies_df, similarity

movies_df, similarity = load_data()

# -------- UI Layout --------

st.title("🎬 Movie Recommender System")
st.write("Enter a movie name below to get 5 similar movie recommendations:")

movie_list = movies_df['title'].values
selected_movie = st.selectbox("Choose a movie", movie_list)

if st.button("Recommend"):
    movie = selected_movie
    idx = movies_df[movies_df['title'] == movie].index[0]
    distances = list(enumerate(similarity[idx]))
    sorted_movies = sorted(distances, reverse=True, key=lambda x: x[1])[1:6]

    st.subheader("Top 5 Recommendations:")
    for i in sorted_movies:
        st.write(f"🎥 {movies_df.iloc[i[0]]['title']}")

import streamlit as st
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------- Function to preprocess data and calculate similarity --------
@st.cache_data
def load_data():
    # Load data
    movies_df = pd.read_csv("data/tmdb_5000_movies.csv")
    credits_df = pd.read_csv("data/tmdb_5000_credits.csv")

    # Merge datasets
    movies_df = movies_df.merge(credits_df, on='title')
    movies_df = movies_df[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

    # Helper functions to process columns
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

    # Process features
    movies_df.dropna(inplace=True)
    movies_df['genres'] = movies_df['genres'].apply(convert)
    movies_df['keywords'] = movies_df['keywords'].apply(convert)
    movies_df['cast'] = movies_df['cast'].apply(lambda x: convert(x)[:3])
    movies_df['crew'] = movies_df['crew'].apply(get_director)
    movies_df['overview'] = movies_df['overview'].apply(lambda x: x.split())
    movies_df['tags'] = movies_df['overview'] + movies_df['genres'] + movies_df['keywords'] + movies_df['cast'] + movies_df['crew']
    movies_df['tags'] = movies_df['tags'].apply(collapse)

    # Vectorize tags
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies_df['tags']).toarray()

    # Similarity matrix
    similarity = cosine_similarity(vectors)

    return movies_df[['title']], similarity

# Load processed data
movies_df, similarity = load_data()

# -------- Streamlit UI --------
st.title("🎬 Movie Recommender System")
st.write("Get 5 similar movie recommendations based on content.")

movie_list = movies_df['title'].values
selected_movie = st.selectbox("Choose a movie", movie_list)

if st.button("Recommend"):
    idx = movies_df[movies_df['title'] == selected_movie].index[0]
    distances = list(enumerate(similarity[idx]))
    sorted_movies = sorted(distances, reverse=True, key=lambda x: x[1])[1:6]

    st.subheader("Top 5 Recommendations:")
    for i in sorted_movies:
        st.write(f"🎥 {movies_df.iloc[i[0]]['title']}")
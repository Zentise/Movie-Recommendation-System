import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
movies_df = pd.read_csv("data/tmdb_5000_movies.csv")
credits_df = pd.read_csv("data/tmdb_5000_credits.csv")

# Merge on title
movies_df = movies_df.merge(credits_df, left_on='title', right_on='title')

# Select features
movies_df = movies_df[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

import ast

def convert(obj):
    try:
        L = []
        for i in ast.literal_eval(obj):
            L.append(i['name'])
        return L
    except:
        return []

def get_director(obj):
    try:
        L = []
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                L.append(i['name'])
        return L
    except:
        return []

def collapse(L):
    return " ".join(L)

# Clean and transform
movies_df.dropna(inplace=True)
movies_df['genres'] = movies_df['genres'].apply(convert)
movies_df['keywords'] = movies_df['keywords'].apply(convert)
movies_df['cast'] = movies_df['cast'].apply(lambda x: convert(x)[:3])  # top 3 cast only
movies_df['crew'] = movies_df['crew'].apply(get_director)

movies_df['overview'] = movies_df['overview'].apply(lambda x: x.split())
movies_df['tags'] = movies_df['overview'] + movies_df['genres'] + movies_df['keywords'] + movies_df['cast'] + movies_df['crew']

movies_df['tags'] = movies_df['tags'].apply(collapse)

# Vectorize
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies_df['tags']).toarray()

# Similarity matrix
similarity = cosine_similarity(vectors)

# Recommend function
def recommend(movie):
    movie = movie.lower()
    if movie not in movies_df['title'].str.lower().values:
        print("Movie not found.")
        return
    idx = movies_df[movies_df['title'].str.lower() == movie].index[0]
    distances = list(enumerate(similarity[idx]))
    sorted_movies = sorted(distances, reverse=True, key=lambda x: x[1])[1:6]
    print("Top 5 Recommendations:")
    for i in sorted_movies:
        print(movies_df.iloc[i[0]]['title'])

# Example
if __name__ == "__main__":
    movie_name = input("Enter a movie name: ")
    recommend(movie_name)

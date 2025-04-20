import pandas as pd
from imdb import IMDb
from sklearn.preprocessing import MultiLabelBinarizer

def load_imdb_data():
    ia = IMDb()
    
    # Example: get top 250 movies
    top250 = ia.get_top250_movies()
    movies = []
    for movie in top250:
        ia.update(movie)
        movies.append({
            'movie_id': movie.movieID if hasattr(movie, 'movieID') else None,
            'title': movie.get('title', None),
            'year': movie.get('year', None),
            'genres': movie.get('genres', []),
            'rating': movie.get('rating', None),
            'votes': movie.get('votes', None),
            'plot': movie.get('plot outline', None)
        })
    df = pd.DataFrame(movies)
    print("Columns in dataframe:", df.columns)
    print("Sample data:\n", df.head())
    return df

def preprocess_data(df):
    # Drop rows with missing values in important columns
    df = df.dropna(subset=['title', 'genres', 'rating'])
    # Convert genres list to one-hot encoding
    mlb = MultiLabelBinarizer()
    genre_dummies = pd.DataFrame(mlb.fit_transform(df['genres']),
                                 columns=mlb.classes_,
                                 index=df.index)
    df = pd.concat([df, genre_dummies], axis=1)
    return df

if __name__ == "__main__":
    df = load_imdb_data()
    df_clean = preprocess_data(df)
    df_clean.to_csv('../data/processed_movies.csv', index=False)
    print("Data preprocessing completed and saved to data/processed_movies.csv")

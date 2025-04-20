import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD

class CollaborativeFilteringRecommender:
    def __init__(self, data_path):
        self.data_path = data_path
        self.user_item_matrix = None
        self.svd = TruncatedSVD(n_components=20, random_state=42)
        self.user_factors = None
        self.item_factors = None
        self.movie_titles = None

    def load_data(self):
        df = pd.read_csv(self.data_path)
        # Create user-item matrix
        self.user_item_matrix = df.pivot(index='user_id', columns='movie_id', values='rating').fillna(0)
        self.movie_titles = df[['movie_id', 'title']].drop_duplicates().set_index('movie_id')

    def train(self):
        self.user_factors = self.svd.fit_transform(self.user_item_matrix)
        self.item_factors = self.svd.components_

    def recommend(self, user_id, top_n=10):
        if user_id not in self.user_item_matrix.index:
            return pd.DataFrame(columns=['movie_id', 'title', 'estimated_rating'])
        user_idx = self.user_item_matrix.index.get_loc(user_id)
        user_ratings = self.user_factors[user_idx, :].dot(self.item_factors)
        # Get movies already rated by user
        rated_movies = self.user_item_matrix.loc[user_id]
        unrated_indices = rated_movies[rated_movies == 0].index
        # Predict ratings for unrated movies
        predicted_ratings = pd.Series(user_ratings, index=self.user_item_matrix.columns)
        predicted_ratings = predicted_ratings.loc[unrated_indices]
        top_movies = predicted_ratings.sort_values(ascending=False).head(top_n)
        recommendations = self.movie_titles.loc[top_movies.index].copy()
        recommendations['estimated_rating'] = top_movies.values
        recommendations.reset_index(inplace=True)
        return recommendations[['movie_id', 'title', 'estimated_rating']]

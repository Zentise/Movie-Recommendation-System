import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)

class MovieRecommender:
    def __init__(self):
        logger.info("Initializing MovieRecommender...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.movies_df = pd.read_csv('data/movies.csv')
        self.movie_embeddings = None
        self.initialize_embeddings()

    def initialize_embeddings(self):
        # Create embeddings for movie titles
        movie_titles = self.movies_df['title'].tolist()
        self.movie_embeddings = self.model.encode(movie_titles)

    def get_recommendations(self, movie_title, n_recommendations=5):
        # Find the movie in our dataset
        movie_idx = self.movies_df[self.movies_df['title'].str.lower() == movie_title.lower()].index
        
        if len(movie_idx) == 0:
            # If exact match not found, find closest match
            movie_embedding = self.model.encode([movie_title])
            similarities = cosine_similarity(movie_embedding, self.movie_embeddings)[0]
            movie_idx = [np.argmax(similarities)]

        if len(movie_idx) == 0:
            return []

        # Get the embedding for our movie
        movie_embedding = self.movie_embeddings[movie_idx[0]].reshape(1, -1)
        
        # Calculate similarities
        similarities = cosine_similarity(movie_embedding, self.movie_embeddings)[0]
        
        # Get indices of most similar movies (excluding the input movie)
        similar_movie_indices = np.argsort(similarities)[::-1][1:n_recommendations+1]
        
        # Get the recommended movies
        recommendations = self.movies_df.iloc[similar_movie_indices]
        
        return recommendations.to_dict('records')

    def get_all_movies(self):
        return self.movies_df['title'].tolist()

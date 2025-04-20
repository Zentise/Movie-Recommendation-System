import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ContentBasedRecommender:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.tfidf_matrix = None
        self.cosine_sim = None
        self.indices = pd.Series(self.data.index, index=self.data['title']).drop_duplicates()

    def fit(self):
        # Use genres and plot combined as text features
        self.data['combined_features'] = self.data['genres'].fillna('') + ' ' + self.data['plot'].fillna('')
        tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = tfidf.fit_transform(self.data['combined_features'])
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def recommend(self, title, top_n=10):
        if title not in self.indices:
            return []
        idx = self.indices[title]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]
        movie_indices = [i[0] for i in sim_scores]
        return self.data.iloc[movie_indices][['title', 'year', 'rating']]

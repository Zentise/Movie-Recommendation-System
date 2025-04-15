from flask import Blueprint, render_template, request, jsonify
from app.models import MovieRecommender
import os
import logging

logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)
recommender = MovieRecommender()
logger.info("MovieRecommender instance created in routes")

@main.route('/')
def index():
    logger.info("Serving index page")
    return render_template('index.html')

@main.route('/recommend', methods=['POST'])
def recommend():
    logger.info("Received recommendation request")
    data = request.get_json()
    movie_title = data.get('movie_title', '')
    logger.info(f"Searching for recommendations for movie: {movie_title}")
    
    if not movie_title:
        return jsonify({'error': 'No movie title provided'}), 400
    
    try:
        recommendations = recommender.get_recommendations(movie_title)
        return jsonify({'recommendations': recommendations})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/movies')
def get_movies():
    try:
        movies = recommender.get_all_movies()
        return jsonify({'movies': movies})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

document.addEventListener('DOMContentLoaded', () => {
    fetchMoviesList();
});

function fetchMoviesList() {
    fetch('/movies')
        .then(response => response.json())
        .then(data => {
            const moviesList = document.getElementById('moviesList');
            moviesList.innerHTML = '';
            if (data.movies) {
                data.movies.forEach(movie => {
                    const option = document.createElement('option');
                    option.value = movie;
                    moviesList.appendChild(option);
                });
            }
        })
        .catch(error => {
            console.error('Error fetching movies list:', error);
        });
}

function getRecommendations() {
    const movieInput = document.getElementById('movieSearch');
    const movieTitle = movieInput.value.trim();
    const recommendationsContainer = document.getElementById('recommendationsContainer');
    const recommendationsList = document.getElementById('recommendationsList');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const errorMessage = document.getElementById('errorMessage');

    recommendationsContainer.style.display = 'none';
    errorMessage.style.display = 'none';

    if (!movieTitle) {
        errorMessage.textContent = 'Please enter a movie title.';
        errorMessage.style.display = 'block';
        return;
    }

    loadingSpinner.style.display = 'block';

    fetch('/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ movie_title: movieTitle })
    })
    .then(response => response.json())
    .then(data => {
        loadingSpinner.style.display = 'none';

        if (data.error) {
            errorMessage.textContent = data.error;
            errorMessage.style.display = 'block';
            return;
        }

        const recommendations = data.recommendations;
        if (recommendations.length === 0) {
            errorMessage.textContent = 'No recommendations found.';
            errorMessage.style.display = 'block';
            return;
        }

        recommendationsList.innerHTML = '';
        recommendations.forEach(movie => {
            const col = document.createElement('div');
            col.className = 'col-md-4 recommendation-item';

            const card = document.createElement('div');
            card.className = 'card movie-card';

            const cardBody = document.createElement('div');
            cardBody.className = 'card-body';

            const title = document.createElement('h5');
            title.className = 'movie-title';
            title.textContent = movie.title;

            cardBody.appendChild(title);
            card.appendChild(cardBody);
            col.appendChild(card);
            recommendationsList.appendChild(col);
        });

        recommendationsContainer.style.display = 'block';
    })
    .catch(error => {
        loadingSpinner.style.display = 'none';
        errorMessage.textContent = 'An error occurred while fetching recommendations.';
        errorMessage.style.display = 'block';
        console.error('Error:', error);
    });
}

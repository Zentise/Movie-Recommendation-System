# Movie Recommender

This project contains a movie recommendation system using IMDbPY data.

## Project Structure

- `data/`: Raw and processed data
- `notebooks/`: EDA and experiments
- `models/`: Recommendation models (content-based and collaborative filtering)
- `app/`: Streamlit app for user interface
- `utils/`: Helper functions including data preprocessing

## Installation

Install dependencies using:

```
pip install -r requirements.txt
```

## Usage

1. Preprocess data:

```bash
python utils/data_preprocessing.py
```

2. Run the Streamlit app:

```bash
streamlit run app/app.py
```

## Features

- Content-Based Filtering using TF-IDF and cosine similarity
- Collaborative Filtering using matrix factorization (SVD) with Surprise library
- Easy-to-use Streamlit interface for recommendations

## Evaluation

Evaluation scripts and notebooks can be added for model performance analysis.

## Future Work

- Add deep learning models for recommendations
- Add more comprehensive evaluation metrics and visualizations
- Expand UI with Gradio option

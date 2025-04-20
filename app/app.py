import streamlit as st
import pandas as pd
from models.content_based import ContentBasedRecommender
from models.collaborative_filtering import CollaborativeFilteringRecommender

@st.cache(allow_output_mutation=True)
def load_content_model():
    model = ContentBasedRecommender('../data/processed_movies.csv')
    model.fit()
    return model

@st.cache(allow_output_mutation=True)
def load_collab_model():
    model = CollaborativeFilteringRecommender('../data/ratings.csv')
    model.load_data()
    model.train()
    return model

def main():
    st.title("Movie Recommendation System")

    menu = ["Content-Based Filtering", "Collaborative Filtering"]
    choice = st.sidebar.selectbox("Select Recommendation Model", menu)

    if choice == "Content-Based Filtering":
        st.subheader("Content-Based Movie Recommendations")
        model = load_content_model()
        movie_title = st.text_input("Enter a movie title you like:")
        if st.button("Recommend"):
            recommendations = model.recommend(movie_title)
            if recommendations.empty:
                st.write("No recommendations found. Please check the movie title.")
            else:
                st.write(recommendations)

    elif choice == "Collaborative Filtering":
        st.subheader("Collaborative Filtering Recommendations")
        model = load_collab_model()
        user_id = st.number_input("Enter your user ID:", min_value=1, step=1)
        if st.button("Recommend"):
            recommendations = model.recommend(user_id)
            if recommendations.empty:
                st.write("No recommendations found for this user.")
            else:
                st.write(recommendations)

if __name__ == "__main__":
    main()

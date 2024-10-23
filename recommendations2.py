import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# Load the dataset
events_df = pd.read_csv('events.csv')

# Filter only movies
movies_df = events_df[events_df['category'] == 'Movies']

# Function to recommend movies based on genre and watched movies
def recommend_movies(watched_movies, genre_interest, top_n=3):
    # Filter movies based on genre of interest
    genre_movies = movies_df[movies_df['category'] == 'Movies']
    genre_movies = genre_movies[genre_movies['event_name'].isin(watched_movies) | (genre_movies['category'] == genre_interest)]
    
    if len(genre_movies) == 0:
        return "No recommendations available for the selected genre."
    
    # Combine features for comparison
    genre_movies['features'] = genre_movies[['event_name', 'category']].apply(lambda x: ' '.join(x), axis=1)
    
    # Create a count vectorizer to convert text to numerical form
    count_vectorizer = CountVectorizer(stop_words='english')
    count_matrix = count_vectorizer.fit_transform(genre_movies['features'])
    
    # Calculate cosine similarity between the movies
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    
    # Get index of the first movie in the list of watched movies
    watched_idx = genre_movies[genre_movies['event_name'].isin(watched_movies)].index[0]
    
    # Get similarity scores for all movies
    sim_scores = list(enumerate(cosine_sim[watched_idx]))
    
    # Sort movies based on similarity score
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the top N recommendations excluding the watched movie itself
    movie_indices = [i[0] for i in sim_scores if i[0] != watched_idx][:top_n]
    
    return genre_movies.iloc[movie_indices][['event_name', 'category', 'price']]

# Example usage
watched_movies = ['Movie B', 'Movie E']  # Example movies watched by the user
genre_interest = 'Movies'

recommended_movies = recommend_movies(watched_movies, genre_interest, top_n=3)
print(recommended_movies)

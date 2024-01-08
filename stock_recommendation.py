import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

df = pd.read_csv("ticker_history.csv")
print(df.head)
print(df.columns)
# Combine relevant features into a single string
df['Features'] = df[['open', 'high', 'low', 'close', 'ticker']].astype(str).agg(' '.join, axis=1)
# Vectorize these features using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['Features'])

# Function to get item recommendations based on user input (date)
def get_recommendations(date, ticker):
    #Finds the index of the first row where the user input date matches in the column Date
    index = df[(df['date'] == date) & (df['ticker'] == ticker)].index[0]
    #Calculate the similarity between items represented by their TF-IDF vectors
    similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)
    cosine_scores = similarities[index]
    print(cosine_scores)
    # Get the indices of items with highest similarity scores
    indices = cosine_scores.argsort()[:-4:-1]

    # Return recommended items
    recommendations = df['date'].iloc[indices].tolist()
    return recommendations

def display_recommended_dates(recommendations, ticker):
    for i in recommendations:
        print(df[(df['date'] == f"{i}") & (df['ticker'] == ticker)])

# Example usage
user_input_date = '2024-01-02'
ticker ="AAPL"
recommendations = get_recommendations(user_input_date, ticker)

print(f"User Input Date and Ticker: {user_input_date}, {ticker}")
print(f"Recommended Dates: {recommendations}")
print(display_recommended_dates(recommendations, ticker))
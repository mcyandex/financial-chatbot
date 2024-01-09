import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import streamlit as st
 
df = pd.read_csv("./Data/ticker_history.csv", delimiter=';')
st.write(df.head)
st.write(df.columns)
# Combine relevant features into a single string
df['Features'] = df[['open', 'high', 'low', 'close','ticker']].astype(str).agg(' '.join, axis=1)
# Vectorize these features using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['Features'])
 
# Function to get item recommendations based on user input (date)
def get_recommendations(date, ticker):
    #Finds the index of the first row where the user input date matches in the column Date
    filtered_df = df[(df['date'] == date) & (df['ticker'] == ticker)]
 
    if not filtered_df.empty:
        index = filtered_df.index[0]
 
        #Calculate the similarity between items represented by their TF-IDF vectors
        similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)
        cosine_scores = similarities[index]
        st.write(cosine_scores)
        # Get the 3 indices of items with highest similarity scores
        indices = cosine_scores.argsort()[:-4:-1]
        # Return recommended items
        recommendations = df['date'].iloc[indices].tolist()
        return recommendations
    else:
        st.write(f"No data found for date {date} and ticker {ticker}")
 
#Display the details on each recommended date
def display_recommended_dates(recommendations, ticker):
    if recommendations != None:
        for i in recommendations:
            st.write(df[(df['date'] == f"{i}") & (df['ticker'] == ticker)])
    else :
        st.write(f"No data found for recommendations {recommendations}")
 
#Example :
#'08/12/2023'
#"aapl"
def chatbot():
    while True:
        st.write("Please enter a date (MM/DD/YYYY) : ")
        user_input_date = st.text_input()
        st.write("Please enter a ticker : ")
        ticker = input().upper()
        recommendations = get_recommendations(user_input_date, ticker)
        st.write(f"User Input Date and Ticker: {user_input_date}, {ticker}")
        st.write(f"Recommended Dates: {recommendations}")
        st.write(display_recommended_dates(recommendations, ticker))
        st.write("Do you want to continue? (yes/no): ")
        response = input().lower()
        if response != 'yes':
            break
chatbot()        
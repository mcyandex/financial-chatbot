import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
  
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
def get_stock_recommendation():
    global df
    df = pd.read_csv("./Data/ticker_history.csv", delimiter=';')
    # Combine relevant features into a single string
    df['Features'] = df[['open', 'high', 'low', 'close','ticker']].astype(str).agg(' '.join, axis=1)
    # Vectorize these features using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    global tfidf_matrix
    tfidf_matrix = vectorizer.fit_transform(df['Features'])

    exit_conditions = ("q", "quit", "exit")
    print("Type q / quit / exit to exit the program.")
    print("Chatbot: Welcome to the stock recommendation module !")

    while True:
        print("\nChatbot: Please enter a date (MM/DD/YYYY)\n")
        user_input_date = input("User: ")
        if user_input_date in exit_conditions :
            print("ATTENTION : QUITTING STOCK RECOMMENDATION !!")
            return 
        else :
            print("\nChatbot: Please enter a ticker\n")
            ticker = input("User: ").upper()
            if ticker in exit_conditions:
                print("ATTENTION : QUITTING STOCK RECOMMENDATION !!")
                return 
        recommendations = get_recommendations(user_input_date, ticker)
        st.write(f"\nUser Input Date and Ticker: {user_input_date}, {ticker}")
        st.write(f"\nRecommended Dates: {recommendations}")
        st.write(display_recommended_dates(recommendations, ticker))
        st.write("\nChatbot: Do you want to continue? (yes/no): \n")
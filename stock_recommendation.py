import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
  
# Function to get item recommendations based on user st.text_input (date)
def get_recommendations(date, ticker):
    #Finds the index of the first row where the user st.text_input date matches in the column Date
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
    input_count=0
    restart = True
    date=""
    while restart:
        global df
        df = pd.read_csv("./Data/ticker_history.csv", delimiter=';')
        # Combine relevant features into a single string
        df['Features'] = df[['open', 'high', 'low', 'close','ticker']].astype(str).agg(' '.join, axis=1)
        # Vectorize these features using TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english')
        global tfidf_matrix
        tfidf_matrix = vectorizer.fit_transform(df['Features'])

        exit_conditions = ("q", "quit", "exit")
        #st.write("Type q / quit / exit to exit the program.")
        st.write("Chatbot: Welcome to the stock recommendation module !")

        questions= ["Chatbot: Please enter a date (MM/DD/YYYY)", "Chatbot: Please enter a ticker"]
        for question in questions:
            st.write(question)
            user_response = st.text_input(label="\n User :",key=f"user{input_count}")
            input_count+=1
            if user_response in exit_conditions:
                st.write("ATTENTION : QUITTING STOCK RECOMMENDATION !!")
                return 
            elif "/" in user_response :
                date = user_response
            else:
                ticker = user_response.upper()
        recommendations = get_recommendations(date, ticker)
        st.write(f"\nUser print Date and Ticker: {date}, {ticker}")
        st.write(f"\nRecommended Dates: {recommendations}")
        st.write(display_recommended_dates(recommendations, ticker))
        st.write("\nChatbot: Do you want to continue? (yes/no): \n")
        response = st.text_input(label="\n User :",key=f"continue{input_count}").lower()
        if response != "yes":
            restart = False
    
#get_stock_recommendation()

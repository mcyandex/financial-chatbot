import pandas as pd
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
        print(cosine_scores)
        # Get the 3 indices of items with highest similarity scores
        indices = cosine_scores.argsort()[:-4:-1]
        # Return recommended items
        recommendations = df['date'].iloc[indices].tolist()
        return recommendations
    else:
        print(f"No data found for date {date} and ticker {ticker}")
 
#Display the details on each recommended date
def display_recommended_dates(recommendations, ticker):
    if recommendations != None:
        for i in recommendations:
            print(df[(df['date'] == f"{i}") & (df['ticker'] == ticker)])
    else :
        print(f"No data found for recommendations {recommendations}")
 
#Example :
#'08/12/2023'
#"aapl"
def get_stock_recommendation(): 
    restart = True
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
        print("Type q / quit / exit to exit the program.")
        print("Chatbot: Welcome to the stock recommendation module !")

        questions= ["Chatbot: Please enter a date (MM/DD/YYYY)", "Chatbot: Please enter a ticker"]
        for question in questions:
            print(question)
            user_response = input("User: ")
            if user_response in exit_conditions:
                print("ATTENTION : QUITTING STOCK RECOMMENDATION !!")
                return 
            elif "/" in user_response :
                date = user_response
            else:
                ticker = user_response.upper()
        recommendations = get_recommendations(date, ticker)
        print(f"\nUser Input Date and Ticker: {date}, {ticker}")
        print(f"\nRecommended Dates: {recommendations}")
        print(display_recommended_dates(recommendations, ticker))
        print("\nChatbot: Do you want to continue? (yes/no): \n")
        response = input().lower()
        if response != "yes":
            restart = False
    
#get_stock_recommendation()
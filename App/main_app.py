import random
from App.stocks_consulting_app import *
from App.yahoo_articles_app import *
from App.personal_finance_app import *
from App.stock_recommendation_app import *
import streamlit as st
import nltk
import random
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

responses = {
    "hello": [
        "Hello! How can I assist you today?",
        "Hi there! How can I help you?",
        "Good morning! How can I help you start your day?",
    ],
    "hi": [
        "Hello! How can I assist you today?",
        "Hi there! How can I help you?",
        "Good morning! How can I help you start your day?",
    ],
    "good morning": [
        "Hello! How can I assist you today?",
        "Hi there! How can I help you?",
        "Good morning! How can I help you start your day?",
    ],
    "how are you": [
        "I'm just a program, but thanks for asking!",
        "I'm here and ready to help. What can I do for you today?",
    ],
    "who are you": [
        "I am your Financial Advisor Bot, designed to provide information and assistance on personal finance.",
        "I am a virtual assistant focused on helping you with financial advice.",
    ],
    "what can you do": [
        "I can provide guidance on budgeting, investments, retirement planning, and more. Feel free to ask me any questions related to personal finance!",
        "You can ask me about budgeting strategies, investment tips, and retirement planning. How can I assist you today?",
    ],
    "stocks consulting": ["http://localhost:8501/Stocks_consulting"],
    "personal finance" : ["http://localhost:8501/2_Personal-Finance"],
    "stock recommendation": ["http://localhost:8501/Yahoo-articles"],
    "yahoo advice articles" : ["http://localhost:8501/Stock-Recommentation"],

    "default" : "I don't understand. Can you rephrase your question?"
    ,
}

def clean_text(text):
    # Remove symbols and digits
    clean_text = re.sub('[^a-zA-Z]', ' ', text)   
    # Replace multiple spaces with a single space
    clean_text = re.sub('\[.*?\]', ' ', clean_text)
    return clean_text

def preprocess_text(text):
    text = clean_text(text)
    stoplist = set(stopwords.words('english')+ list(punctuation))
    #Word Tokenize
    tokens = word_tokenize(text.lower())
    #filter the list of tokens that are not in stoplist
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stoplist]
    #Lemmatization
    lemmatizer = WordNetLemmatizer()
    #lemmatize each token
    filtered_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    #recreate a phrase with the preprocessed tokens 
    return ' '.join(filtered_tokens)
 
def generate_response(user_input):
    preprocessed_input = preprocess_text(user_input)
    
    vectorizer = TfidfVectorizer()
    #for each key in the responses dictionary, compute preprocessing and stock them in a list
    key_vectors = [preprocess_text(key) for key in responses.keys()]
    #add the preprocessed user input into this list of keys
    key_vectors.append(preprocessed_input)
 
    #create the tfidf matrix of these keys
    tfidf_matrix = vectorizer.fit_transform(key_vectors)
    #compute the similarity of the keys with the last element of the list (user input)
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]
    #print(similarity_scores)
    #get the best score from the list
    best_match_index = similarity_scores.argmax()  
    #find the key of the dict that is the closest to the user input  
    matched_key = list(responses.keys())[best_match_index % len(responses)]

    #if the score is greater than 0.1 get the matched response
    if similarity_scores[best_match_index] > 0.1:
        response = responses[matched_key]
        #if the response is a function, call it
        if callable(response):
            response()
        else : 
            response = random.choice(responses[matched_key])
    #if the score is very bad, the program returns a default message
    else:
        response = responses["default"]
    return response

def start_chat():
    st.write(
        "\nChatbot: Hello, I am your Financial Advisor Bot. Feel free to ask me any questions related to personal finance:"
    )

    
    if st.session_state.get("messages") is None:
        st.session_state.messages = []
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        
        if prompt.lower() in ['exit', 'bye', 'quit']:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = "Goodbye! Until next time."
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

        #Generate response
        bot_response = generate_response(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = bot_response
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            

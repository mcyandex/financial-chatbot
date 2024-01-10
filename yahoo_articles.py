import requests
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import streamlit as st

responses = {
    "budgeting": [
        "Budgeting is crucial for financial success. Have you set up a budget before?",
        "Sure, let's talk about budgeting. Where would you like to start?",
        "Budgeting is a key aspect of financial planning. How can I assist you with it?",
    ],
    "investment": [
        "Investing can help grow your wealth. What specific questions do you have about investments?",
        "Sure, let's discuss investments. What aspects are you interested in?",
        "Investing wisely is important for financial goals. How can I guide you through it?",
    ],
    "retirement planning": [
        "Retirement planning is essential for a secure future. What do you want to know about retirement planning?",
        "Certainly, let's talk about retirement planning. What specific information are you looking for?",
        "Planning for retirement is a smart move. How can I assist you in this process?",
    ],
    "default" : [
        "I don't understand. Can you rephrase your question?"
    ],
}

def get_yahoo_finance_articles(base_url, count=26):
    """
    Retrieves Yahoo Finance articles from the specified base URL.

    Parameters:
    - base_url (str): The base URL to fetch articles from.
    - count (int): Number of articles to retrieve.

    Returns:
    - list: List of dictionaries containing article titles and links.
    """
    response = requests.get(base_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('li', class_='js-stream-content')

        result = []
        for i, article in enumerate(articles[:count]):
            title = article.find('h3').get_text(strip=True)
            link = article.find('a')['href']
            result.append({"title": title, "link": link})

        return result
    else:
        return None

def print_articles(articles):
  if articles:
    for i, article in enumerate(articles):
        st.write(f"\nArticle {i + 1}:")
        st.write(f"Titre: {article['title']}")
        st.write(f"Liens: {article['link']}")
  else:
      st.write("Aucun article trouvé.")

def get_titles(articles):
  titles = []
  for i, article in enumerate(articles):
    titles.append(article['title'])
  return titles

def get_links(articles):
  links = []
  for i, article in enumerate(articles):
    if not article['link'].startswith('http'):
      article['link'] = 'https://finance.yahoo.com' + article['link']
    links.append(article['link'])
  return links

def get_paragraphs_text(soup):
   paragraphs = soup.find_all('p')
   return [paragraph.text.lower() for paragraph in paragraphs]

def extract_text_from_article(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = get_paragraphs_text(soup)
    return text

def parse_all_articles(links):
  return ['.'.join(extract_text_from_article(link)) for link in links]

def data_preprocessing(bdd):
  preprocessed_bdd = []
  for doc in bdd:
    tokens = sent_tokenize(doc)
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    preprocessed_bdd.append(' '.join(lemmatized_tokens))
  return preprocessed_bdd

def get_best_article(user_input):
  """
    Finds the most similar preprocessed article to the user input.

    Parameters:
    - user_input (str): User's input.

    Returns:
    - str: The most similar preprocessed article or an error message.
    """
  preprocessed_bdd.append(user_input)

  vectorizer = TfidfVectorizer(stop_words='english')
  tfidf_matrix = vectorizer.fit_transform(preprocessed_bdd)

  cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
  most_similar_index = np.argmax(cosine_sim)

  # Check if the cosine similarity is less than 1 (indicating some similarity) and greater than 0.1 (considering a minimum threshold for similarity).
  if cosine_sim[0][most_similar_index] < 1 and cosine_sim[0][most_similar_index] > 0.1:
      return preprocessed_bdd[most_similar_index]
  else:
      return "I am sorry, I could not understand you."
  
def get_following_sentences(user_input, best_article, num_following_sentences=5):
    """
    Finds the N most similar sentences following the best article.

    Parameters:
    - user_input (str): User's input.
    - best_article (str): The most similar preprocessed article.
    - num_following_sentences (int): Number of following sentences to retrieve.

    Returns:
    - str: The capitalized N most similar sentences or an error message.
    """
    best_article = best_article.split('.') 
    best_article.append(user_input)

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(best_article)

    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    most_similar_index = np.argmax(cosine_sim)

    following_indices = np.argsort(cosine_sim[0])[:-num_following_sentences-1:-1][1:]

    following_sentences = [best_article[i] for i in following_indices]

    # Check if the cosine similarity is less than 1 (indicating some similarity) and greater than 0.1 (considering a minimum threshold for similarity).
    if cosine_sim[0][most_similar_index] < 1 and cosine_sim[0][most_similar_index] > 0.1:
        capitalized_sentences = [sentence.capitalize() for sentence in following_sentences]
        return '. '.join(capitalized_sentences) + '.'
    else:
        return "I am sorry, I could not understand you."

def start_chatbot_yahoo():
   exit_conditions = ("q", "quit", "exit", 'bye')
   while True:
       query = st.text_input("\nUser: ")
       if query in exit_conditions:
           break
       else:
           best_article = get_best_article(query)
           best_sentence = get_following_sentences(query, best_article)
           st.write(f"\nChatbot: {best_sentence}")
           preprocessed_bdd.pop()

def get_financial_advices():
  articles = get_yahoo_finance_articles("https://finance.yahoo.com/topic/personal-finance-news/") + get_yahoo_finance_articles("https://finance.yahoo.com/") + get_yahoo_finance_articles("https://finance.yahoo.com/calendar/") + get_yahoo_finance_articles("https://finance.yahoo.com/topic/stock-market-news/")
  urls = get_links(articles)
  global bdd
  bdd = parse_all_articles(urls)
  global preprocessed_bdd
  preprocessed_bdd = data_preprocessing(bdd)
  start_chatbot_yahoo()
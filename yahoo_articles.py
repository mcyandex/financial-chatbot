import requests
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import torch
from transformers import BertForQuestionAnswering, BertTokenizer

model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

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
        print(f"\nArticle {i + 1}:")
        print(f"Titre: {article['title']}")
        print(f"Liens: {article['link']}")
  else:
      print("Aucun article trouvé.")

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
       query = input("\nUser: ")
       if query in exit_conditions:
           break
       else:
           best_article = get_best_article(query)
           best_sentence = get_following_sentences(query, best_article)
           print(f"\nChatbot: {best_sentence}")
           preprocessed_bdd.pop()
  
def get_best_context(question, articles):
    #append question to the bdd
    articles.append(question)
    
    #create instance of tfidf vectorizer
    vectorizer = TfidfVectorizer()
    #compute the tfidf matrix
    tfidf_matrix = vectorizer.fit_transform(articles)
    
    #compute cos sim between the question and articles
    similarities = cosine_similarity(tfidf_matrix[-1] , tfidf_matrix[:-1])
    #get the best index of the answer that has the best cos sim
    best_index = similarities.argmax()

    #pop the question out of the bdd
    articles.pop()

    #retrieve the best answer
    best_answer = articles[best_index]
    return best_answer

def generate_answer_bert(question, context, model, tokenizer):
    #tokenize question and context with bert's tokenizer
    inputs = tokenizer(question, context, return_tensors = 'pt', max_length = 512, truncation = True) #'pt' to return pytorch tensors. max length and trucation to control the input size
    outputs = model(**inputs) #pass the input to the model to get start/end positions' probability
    
    start_scores = outputs.start_logits #extract the predictions for the start position
    end_scores = outputs.end_logits #extract the predictions for the start position

    answer_start = torch.argmax(start_scores) #retrieve the max arg of the start position where the proba is the highest
    answer_end = torch.argmax(end_scores) + 1 #retrieve the max arg of the end position where the proba is the highest
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end])) #extract the answer with these positions

    cleaned_answer = answer.replace("[CLS]" , "").replace("[SEP]" , "").strip() #remove some tokens used by bert

    return cleaned_answer

def get_final_answer(question , bdd):
   best_context = get_best_context(question , bdd)
   bert_answer = generate_answer_bert(question, best_context, model, tokenizer)

   return bert_answer

def get_financial_advices():
  print("Type q / quit / exit to exit the program.")
  print("Chatbot: Welcome to the yahoo articles module !")
  articles = get_yahoo_finance_articles("https://finance.yahoo.com/topic/personal-finance-news/") + get_yahoo_finance_articles("https://finance.yahoo.com/") + get_yahoo_finance_articles("https://finance.yahoo.com/calendar/") + get_yahoo_finance_articles("https://finance.yahoo.com/topic/stock-market-news/")
  urls = get_links(articles)
  global bdd
  bdd = parse_all_articles(urls)
  global preprocessed_bdd
  preprocessed_bdd = data_preprocessing(bdd)
  start_chatbot_yahoo()
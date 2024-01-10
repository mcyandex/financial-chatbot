import random
import streamlit as st
from stocks_consulting import *
from stocks_consulting import *
from yahoo_articles import *
from personal_finance import *
from stock_recommendation import *
import importlib

# Assuming the page files are in the "pages" folder and have the same name as the page function
pages_folder = "pages"

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
}

exits = ["q", "quit", "exit", "bye"]


def get_options():
    st.write("\nChatbot: Here some of my functionalities")
    st.write("\nSelect the service that you want")
    st.write("1) [Stocks consulting](Stocks_consulting)")
    st.write("2) [Personal Finance](Personal_Finance)")
    st.write("3) [Yahoo articles](Yahoo_articles)")
    st.write("4) [Stock Recommendation](Stock_Recommendation)")





def get_help():
    st.write("\nChatbot: Here list of commands you can use")
    for k in responses.keys():
        st.write("- " + k)
    st.write("- options")
    st.write("- help")
def load_page(page_name):
    module = importlib.import_module(f"{pages_folder}.{page_name}")
    return module.page

def start_chat():
    st.write(
        "\nChatbot: Hello, I am your Financial Advisor Bot. Feel free to ask me any questions related to personal finance:"
    )
    st.write("\n(Use the command 'help' to see all the possible commands)")

    if st.session_state.get("messages") is None:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.expander(message["role"].capitalize()):
            st.markdown(message["content"])

    # Accept user input
    user_input = st.chat_input("\nYou: ")
    
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        # Display user message in chat message container
        with st.expander("User"):
            st.markdown(user_input)

        # Handle user input and generate assistant response
        handle_user_input(user_input.lower())


def handle_user_input(user_input):
    if user_input in responses:
        st.write("\nChatbot: " + random.choice(responses[user_input]))
    elif user_input == "options":
        get_options()
    elif user_input == "1":
        get_stocks_report()
    elif user_input == "2":
        get_personal_finance()
    elif user_input == "3":
        get_financial_advices()
    elif user_input == "4":
        get_stock_recommendation()
    elif user_input == "help":
        get_help()
    elif user_input in exits:
        st.write("\nChatbot: Goodbye! Until next time.")
    else:
        st.write("\nChatbot: I don't understand. Can you rephrase your question?")




import random
import streamlit as st
from stocks_consulting import *
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
    st.write(
        "\n(Use the command 'help' to see all the possible command)" 
    )

    user_inputs = []  # List to store user inputs
    input_counter = 0

    user_input = st.text_input(f"{input_counter + 1}. \nYou: ")

    ask_button = st.button("Ask")

    if ask_button and user_input:
        input_counter += 1
        user_inputs.append(user_input.lower())  # Convert input to lowercase
        st.write(input_counter)

        for i, (input_text, output_text) in enumerate(zip(user_inputs, responses.get(user_input, []))):
            st.write(f"\nYou {i + 1}: {input_text}")
            st.write(f"Chatbot {i + 1}: {output_text}")

        user_input_lower = user_input.lower()
        if user_input_lower in responses:
            st.write("\nChatbot: " + random.choice(responses[user_input_lower]))
        elif user_input_lower == "options":
            get_options()
        elif user_input_lower == "1":
            # Change the page based on user input
            selected_page_name = "1_Stocks consulting"
            selected_page = load_page(selected_page_name)
            selected_page()
        elif user_input_lower == "help":
            get_help()
        elif user_input_lower in exits:
            st.write("\nChatbot: Goodbye! Until next time.")
        else:
            st.write("\nChatbot: I don't understand. Can you rephrase your question?")

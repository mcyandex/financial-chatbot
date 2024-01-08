import streamlit as st
from transformers import pipeline
import random
import streamlit as st
from stocks_consulting import *


# Load the chatbot model (you can use any chatbot model of your choice)
chatbot_model = pipeline("conversational")



# Home Page
def home():
    st.title("Home Page")
    st.write("Welcome to the Chatbot Interface!")
# Stocks Consulting Page
def stocks_page():
    st.title("Stocks Consulting")
    st.write("Welcome to the Stocks Consulting page!")
    # Add your content for Stocks Consulting here

# Budget Recommendation Page
def budget_page():
    st.title("Budget Recommendation")
    st.write("Welcome to the Budget Recommendation page!")
    # Add your content for Budget Recommendation here

# Personal Finance Advice Page
def personal_finance_page():
    st.title("Personal Finance Advice")
    st.write("Welcome to the Personal Finance Advice page!")
    # Add your content for Personal Finance Advice here

# Investing Recommendation Page
def investing_page():
    st.title("Investing Recommendation")
    st.write("Welcome to the Investing Recommendation page!")
    # Add your content for Investing Recommendation here
# Chatbot Page
def chatbot():
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
        st.write("\nChatbot: Here are some of my functionalities")
        st.write("1) [Stocks consulting](#stocks-consulting)")
        st.write("2) [Budget Recommendation](#budget-recommendation)")
        st.write("3) [Personal Finance Advice](#personal-finance-advice)")
        st.write("4) [Investing Recommendation](#investing-recommendation)")


    def get_help():
        st.write("\nChatbot: Here list of commands you can use")
        for k in responses.keys():
            st.write("- " + k)
        st.write("- options")
        st.write("- help")


    def start_chat():
        st.write(
            "\nChatbot: Hello, I am your Financial Advisor Bot. Feel free to ask me any questions related to personal finance:"
        )
        get_options()



        user_input = st.text_input(f"{input_counter + 1}. \nYou: ").lower()

        ask_button = st.button("Ask")
            # Parameters
        user_inputs = []  # List to store user inputs
        input_counter = 0

        if ask_button and user_input:
            input_counter += 1
            user_inputs.append(user_input)
            st.write(input_counter)

            for i, (input_text, output_text) in enumerate(zip(user_inputs, responses.get(user_input, []))):
                st.write(f"\nYou {i + 1}: {input_text}")
                st.write(f"Chatbot {i + 1}: {output_text}")

            if user_input in responses:
                st.write("\nChatbot: " + random.choice(responses[user_input]))
            elif user_input == "options":
                get_options()
            elif user_input == "2":
                get_stocks_report()
            elif user_input == "help":
                get_help()
            elif user_input in exits:
                st.write("\nChatbot: Goodbye! Until next time.")
            else:
                st.write("\nChatbot: I don't understand. Can you rephrase your question?")

    start_chat()

# About Page
def about():
    st.title("About")
    st.write("This is a simple Streamlit app with a multi-page interface.")

# Navigation
pages = {
    "Home": home,
    "Chatbot": chatbot,
    "Stocks Consulting": stocks_page,
    "Budget Recommendation": budget_page,
    "Personal Finance Advice": personal_finance_page,
    "Investing Recommendation": investing_page,
    "About": about,
}

# Sidebar
selected_page = st.sidebar.radio("Select a page", list(pages.keys()))

# Display the selected page
pages[selected_page]()

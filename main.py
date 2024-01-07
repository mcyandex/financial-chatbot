import random
from stocks_consulting import *

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
    print("\nChatbot: Here some of my functionalities")
    print("1) Stocks consulting")
    print("2) Budget Recommendation")
    print("3) Personal Finance Advice")
    print("4) Investing Recommendation")


def get_help():
    print("\nChatbot: Here list of commands you can use")
    for k in responses.keys():
        print("- " + k)
    print("- options")
    print("- help")


def start_chat():
    print(
        "\nChatbot: Hello, I am your Financial Advisor Bot. Feel free to ask me any questions related to personal finance:"
    )
    get_options()

    while True:
        user_input = input("\nYou: ").lower()
        if user_input in responses:
            print("\nChatbot: " + random.choice(responses[user_input]))
        elif user_input == "options":
            get_options()
        elif user_input == "2":
            get_stocks_report()
        elif user_input == "help":
            get_help()
        elif user_input in exits:
            print("\nChatbot: Goodbye! Until next time.")
            break
        else:
            print("\nChatbot: I don't understand. Can you rephrase your question?")

start_chat()
import streamlit as st
from transformers import pipeline
from main_app import start_chat

# Load the chatbot model (you can use any chatbot model of your choice)
chatbot_model = pipeline("conversational")

# Home Page
def home():
    st.title("Home Page")
    st.write("Welcome to the Chatbot Interface!")

# Chatbot Page
def chatbot():
    start_chat()

# About Page
def about():
    st.title("About")
    st.write("This is a simple Streamlit app with a multi-page interface.")

# Navigation
pages = {
    "Home": home,
    "Chatbot": chatbot,
    "About": about,
}

# Sidebar
selected_page = st.sidebar.radio("Select a page", list(pages.keys()))

# Display the selected page
pages[selected_page]()

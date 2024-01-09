import streamlit as st
from transformers import pipeline
from stocks_consulting import *


# Load the chatbot model (you can use any chatbot model of your choice)
chatbot_model = pipeline("conversational")

st.title("Stocks Consulting")
st.write("Welcome to the Stocks Consulting page!")

get_stocks_report()
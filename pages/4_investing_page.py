import streamlit as st
from transformers import pipeline
import random
from stocks_consulting import *


# Load the chatbot model (you can use any chatbot model of your choice)
chatbot_model = pipeline("conversational")

st.title("Investing Recommendation")
st.write("Welcome to the Investing Recommendation page!")
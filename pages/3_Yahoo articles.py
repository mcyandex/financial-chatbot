import streamlit as st
from transformers import pipeline
import random
from yahoo_articles import *


# Load the chatbot model (you can use any chatbot model of your choice)
chatbot_model = pipeline("conversational")

st.title("Personal Finance Advice")
st.write("Welcome to the Personal Finance Advice page!")

get_financial_advices()
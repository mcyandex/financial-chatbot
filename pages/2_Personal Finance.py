import streamlit as st
from transformers import pipeline
import random
from personal_finance import *


# Load the chatbot model (you can use any chatbot model of your choice)
chatbot_model = pipeline("conversational")

st.title("Budget Recommendation")
st.write("Welcome to the Budget Recommendation page!")

get_personal_finance()
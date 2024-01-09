import streamlit as st
from transformers import pipeline
import random
import streamlit as st
from stocks_consulting import *
from main_app import *


# Load the chatbot model (you can use any chatbot model of your choice)
chatbot_model = pipeline("conversational")



start_chat()

st.write("--------------------------------------------------------")
st.write("For faster navigation")

st.write("\nSelect the service that you want")
st.write("1) [Stocks consulting](Stocks_consulting)")
st.write("2) [Personal Finance](Personal_Finance)")
st.write("3) [Yahoo articles](Yahoo_articles)")
st.write("4) [Stock Recommendation](Stock_Recommendation)")

import streamlit as st
from transformers import pipeline
from App.stocks_consulting_app import *

st.title("Stocks Consulting")
st.write("Welcome to the Stocks Consulting page!")
st.write("This page consist of having some indicators or informations on some company about their stocks ")
st.write("--------------------------------------------------------")

get_stocks_report()
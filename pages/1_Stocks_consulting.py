import streamlit as st
from transformers import pipeline
from stocks_consulting import *

st.title("Stocks Consulting")
st.write("Welcome to the Stocks Consulting page!")

get_stocks_report()
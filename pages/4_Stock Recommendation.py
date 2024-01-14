import streamlit as st
from transformers import pipeline
import random
from App.stock_recommendation_app import *


st.title("Investing Recommendation")
st.write("Welcome to the Investing Recommendation page!")
st.write("This page consist of having giving you dates of a company where the features are really near ")

st.write("To test this you can set the date to 08/12/2023 with aapl as the ticker\n")
st.write("--------------------------------------------------------")

get_stock_recommendation()
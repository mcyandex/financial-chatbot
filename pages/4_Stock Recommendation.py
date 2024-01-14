import streamlit as st
from transformers import pipeline
import random
from App.stock_recommendation_app import *


st.title("Investing Recommendation")
st.write("Welcome to the Investing Recommendation page!")

get_stock_recommendation()
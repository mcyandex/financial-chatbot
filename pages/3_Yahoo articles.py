import streamlit as st
from transformers import pipeline
import random
from App.yahoo_articles_app import *


st.title("Personal Finance Advice")
st.write("Welcome to the Personal Finance Advice page!")
st.write("This page consist of giving an answer or informations on the question that you want")
st.write("--------------------------------------------------------")

get_financial_advices()
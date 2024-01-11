import streamlit as st
from transformers import pipeline
import random
from yahoo_articles import *


st.title("Personal Finance Advice")
st.write("Welcome to the Personal Finance Advice page!")

get_financial_advices()
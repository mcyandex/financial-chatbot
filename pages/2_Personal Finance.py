import streamlit as st
from transformers import pipeline
import random
from App.personal_finance_app import *


st.title("Personal Finance")
st.write("Welcome to the Personal Finance page!")
st.write("This page consist of having some indicators or informations about all your investisment ")
st.write("")

st.write("if your answer is 'yes' in this question 'Do you have any variable costs this year?', accept your input by pressing 'enter' to have the other cells")
st.write("--------------------------------------------------------")

get_personal_finance()
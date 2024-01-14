import streamlit as st
from transformers import pipeline
import random
from personal_finance_app import *


st.title("Budget Recommendation")
st.write("Welcome to the Budget Recommendation page!")

get_personal_finance()
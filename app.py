import streamlit as st
from transformers import pipeline
import random
import streamlit as st
from stocks_consulting import *
from main_app import *


# Load the chatbot model (you can use any chatbot model of your choice)
chatbot_model = pipeline("conversational")



start_chat()

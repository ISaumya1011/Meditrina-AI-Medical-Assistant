# old api key : AIzaSyDx85a8cs7oeF0yXR3mngoUa2szwPdx7Qs
# setx GOOGLE_API_KEY "AIzaSyA_MRzinC7fI9_OwTGJX04CFvcR7jr62tE"
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai
import numpy as np
import pandas as pd
import PIL
from PIL import Image

GOOGLE_API_KEY = 'GOOGLE_API_KEY'
genai.configure(api_key="GOOGLE_API_KEY")

# Fn to load gemini pro model n get response
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
def get_gemini_response(question):
    response=chat.send_message(question,stream=True)
    return response

# Initialize our streamlit app
st.set_page_config(page_title="Hey, I'm Meditrina!")

st.title("Hello, I'm Meditrina : Your AI Medical Assistant!")
st.markdown("## 👩‍⚕️ How can I help you? ")
with st.chat_message("user"):
    st.write("Hello 👋")
with st.chat_message("assistant"):
    st.write("Hello human")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input=st.text_input("Prompt: ",key="input")
submit=st.button("Ask the question")

if submit and input:
    response=get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is ")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))
if st.button(" Chat History 🗨️ "):
    st.subheader("The Chat History is ")
    
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")



# streamlit run app1.py

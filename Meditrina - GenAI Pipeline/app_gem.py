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

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

def get_gemini_response(question, prompt):
    # Incorporate the custom prompt into the chat history
    chat.send_message(prompt)
    response = chat.send_message(question, stream=True)
    return response

# Initialize our streamlit app
st.set_page_config(page_title="Hey, I'm Meditrina!")

st.sidebar.title("👩‍⚕️ I'm Meditrina ")
st.sidebar.markdown("# Here is how I can help you. ")
st.sidebar.markdown("### - I efficiently predict disease based on symptoms you experience")
st.sidebar.markdown("### - Suggest precautions based on predictions")
st.sidebar.markdown("### - Help you with Treatment plans")
st.sidebar.markdown("### - Provide list of home remedies")

st.title("Hello, I'm Meditrina : Your AI Medical Assistant!")
st.markdown("## 🩺 How can I help you? ")
with st.chat_message("user"):
    st.write("Hello 👋")
with st.chat_message("assistant"):
    st.write("Hello!")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Defining age and gender of the user
gender = st.radio("What is your gender : ",('Female','Male'), key="gender")
age = st.number_input("Please enter your age : ", step=1, min_value=0, max_value=125, key="age")

# Custom prompt for the medical assistant :: Using formatted string to insert age and gender of user for custom output
medical_assistant_prompt = """You are Meditrina, an AI Medical Assistant. You are a friendly, helpful and compassionate medical expert.
You are a knowledgeable and kind medical expert.
You provide a one stop platform for the patient and satisfy the user.Be caring and responsible like a doctor.
You act as an AI doctor and help the patient by providing them 
disease predictions, precautions, treatment plan or when to seek medical advice.
You provide efficient analysis of symptoms and disease.
You should provide accurate and helpful information to users 
about health conditions, symptoms, treatments, and preventive care."""+ f"For customised plan, age of the user is {age} and the gender of the user is {gender}."
medical_assistant_prompt = medical_assistant_prompt + """ 
Answer to user's illness or symptoms in the following order :
1. List down the possible predicted conditions or diseases based on symptom given. Explain their specific symptoms or detail in brief and Mention the no. of days user could have felt ill according to corresponding predicted disease.
2. List the precautionas that the user should take to resolve the symptoms and possible disease
3. Suggest some home remedies that user can follow
4. Give user additional tips
5. Tell when to necessarily seek medical advice
At end, suggest users to consult with a healthcare professional for best diagnosis and treatment."""

input = st.text_input("Prompt: ", key="input")
input = input
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input, medical_assistant_prompt)
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

# streamlit run app_gem.py
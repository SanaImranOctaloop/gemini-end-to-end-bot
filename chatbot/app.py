from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Function for Gemini Pro Model and get Response
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize our streamlit app
st.set_page_config("GEMINI CHATBOT")
st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

inp = st.text_input("Input: ", key='input')
submit = st.button("Ask the Question")

if submit and inp:
    response = get_gemini_response(inp)
    
    # Add user query and response to session chat
    st.session_state['chat_history'].append(("You:  ", inp))
    st.subheader("The response is: ")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot:  ", chunk.text))
        
st.subheader("The Chat history is: ")

for role, text in st.session_state["chat_history"]:
    st.write(f"{role} {text}")

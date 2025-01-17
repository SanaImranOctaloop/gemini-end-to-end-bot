from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import time  # Import time for adding delay

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Function for Gemini Pro Model and get Response
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


def get_gemini_response_streaming(question):
    # Generator function to yield characters one-by-one with a delay
    response = chat.send_message(question, stream=True)  # Stream response
    for chunk in response:
        for char in chunk.text:
            yield char  # Yield one character at a time


# Initialize our streamlit app
st.set_page_config("GEMINI CHATBOT")
st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

inp = st.text_input("Input: ", key='input')
submit = st.button("Ask the Question")

if submit and inp:
    # Add user query to session chat
    st.session_state['chat_history'].append(("You:  ", inp))
    st.subheader("The response is: ")
    
    # Get streaming response
    response_gen = get_gemini_response_streaming(inp)
    response_text = ""

    # Stream response character by character
    response_placeholder = st.empty()  # Placeholder for streaming content
    for char in response_gen:
        response_text += char  # Build response incrementally
        response_placeholder.write(response_text)  # Update UI
        time.sleep(0.05)  # Delay of 0.05 seconds per character
    
    # Add the full bot response to session history
    st.session_state['chat_history'].append(("Bot:  ", response_text))

# Display Chat History
st.subheader("The Chat history is: ")
for role, text in st.session_state["chat_history"]:
    st.write(f"{role} {text}")

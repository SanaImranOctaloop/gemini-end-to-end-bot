# Importing Libraries
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Loading virtual environment, environment variables
load_dotenv()

# Accessing environment variables
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
APP_NAME = os.getenv("APP_NAME")
PORT = int(os.getenv("PORT", 8001)) 

# Initializing Model
model = genai.GenerativeModel("gemini-pro")

# Initializing FastAPI app
app = FastAPI(title=APP_NAME)

# A dictionary to hold the chat history per session/user
chat_history = []

# Start a new chat instance (global in this example)
chat = model.start_chat(history=[])

# Defining a request model
class ChatRequest(BaseModel):
    question: str


# Accessing root directory, home page 
@app.get("/")
async def root():
    return {"message": f"Welcome to {APP_NAME}!"}



# POST method to send a question to the chatbot and get a response.
@app.post("/ask")
async def ask_chatbot(request: ChatRequest):
    try:
        response_stream = chat.send_message(request.question, stream=True)

        response_text = "".join(chunk.text for chunk in response_stream)
        # Add to chat history
        chat_history.append({"user": request.question, "bot": response_text})

        return {"user": request.question, "bot": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# GET method to retrieve the chat history.
@app.get("/chat-history")
async def get_chat_history():
    return {"history": chat_history}



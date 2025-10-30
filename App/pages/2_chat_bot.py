import streamlit as st
from dotenv import load_dotenv
import os
from groq import Groq

# Load the GROQ_API_KEY from .env file
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Streamlit setup
st.set_page_config(page_title="Groq Chatbot ⚡", page_icon="🤖")
st.title("🤖 Simple Chatbot (Powered by Groq)")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hey there! I'm your Groq-powered chatbot. How can I help you today?"}
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input field
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response using Groq model
    response = client.chat.completions.create(
        model="openai/gpt-oss-safeguard-20b",  # You can use 'llama3-70b-8192' too
        messages=st.session_state.messages
    )

    bot_reply = response.choices[0].message.content

    # Show assistant message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

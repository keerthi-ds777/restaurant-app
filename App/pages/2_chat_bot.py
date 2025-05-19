from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="BiteFinder - Chatbot",
    page_icon="🤖",
    layout="wide"
)
# Get the API key from the environment variable
api_key = os.getenv("GOOGLE_GENAI_API_KEY")
if not api_key:
    st.error("🔐 API key missing! Create a `.env` file with `GOOGLE_GENAI_API_KEY`")
    st.stop()  # Halt app if no key

# Configure the Google Generative AI client
genai.configure(api_key=api_key)

def get_chat_response(prompt):
    """Get AI response with error handling using Google Generative AI"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def chatbot_page():
    st.title("💬 Chatbot Page")
    st.markdown("Ask the BiteFinder Bot anything!")

    # Initialize chat
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Ask me about restaurent or recipe ?"}]

    # Display chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Handle user input
    if prompt := st.chat_input("Type your question here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        try:
            with st.spinner("🧠 Thinking..."):
                response = get_chat_response(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"API Error: {str(e)}")
            st.session_state.messages.append({"role": "assistant", "content": "⚠️ Sorry, I encountered an error."})
        st.rerun()



chatbot_page()


import os
from dotenv import load_dotenv
import streamlit as st

from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.schema import HumanMessage, AIMessage

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
        st.error("🔑 Please set GROQ_API_KEY in .env")
        st.stop()

st.set_page_config(page_title="Cooking Guide Chatbot", page_icon="🍳", layout="wide")
st.title("🍲 ChefGroq — Your Cooking Assistant")

    # Initialize the Groq chat model via LangChain
llm = ChatGroq(
        model="llama-3.1-8b-instant",  # or whichever model you prefer
        temperature=0.7,
        api_key=groq_key    )

    # Use memory to retain conversation
if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(return_messages=True)

if "conversation" not in st.session_state:
        st.session_state.conversation = ConversationChain(
            llm=llm,
            memory=st.session_state.memory
        )

    # Input from user

    
    # Display conversation history
st.markdown("### Conversation")
for msg in st.session_state.memory.chat_memory.messages:
        if isinstance(msg, HumanMessage):
            st.markdown(f"**You:** {msg.content}")
        else:
            st.markdown(f"**ChefGroq:** {msg.content}")
        st.markdown("---")

    # Input from user at the bottom
user_input = st.chat_input("Ask me about cooking, recipes, tips…")
if user_input:
        with st.spinner("Thinking …"):
            response = st.session_state.conversation.run(user_input)
            st.session_state.memory.chat_memory.add_message(HumanMessage(content=user_input))
            st.session_state.memory.chat_memory.add_message(AIMessage(content=response))


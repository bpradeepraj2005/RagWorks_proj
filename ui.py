import streamlit as st
import os
from dotenv import load_dotenv

# Ensure environment is loaded
load_dotenv()

# Must import agent after dotenv loads
from agent_framework.multi_agent import run_agent_system

# Configure Streamlit page
st.set_page_config(page_title="AI Shopping Assistant", page_icon="🛍️", layout="centered")

st.title("🛍️ Personal AI Shopping Assistant")
st.markdown("""
Welcome! I am powered by a Multi-Agent framework using **Groq** and **LangChain**. 
I have access to live budgets, a local database, and store policy RAG context.
""")

# Check for API key before proceeding
if not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "dummy_key_to_prevent_crash":
    st.warning("⚠️ Warning: GROQ_API_KEY is missing from your .env file. The agent will not be able to process queries.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history on rerun
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input block
if prompt := st.chat_input("Ask me to buy something or check a policy..."):
    # Add user message to state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing request and executing tools..."):
            try:
                response = run_agent_system(prompt)
                
                # Check if response caught a rate limit exception from the framework string
                if "429" in response and "rate_limit_exceeded" in response:
                    st.error("🚀 Whoa there! The free Groq API Rate Limit was exceeded. Please wait a minute before sending another message.")
                    st.session_state.messages.append({"role": "assistant", "content": "*(Rate Limit Error - Try again shortly)*"})
                else:
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
            except Exception as e:
                st.error(f"System Crash: {e}")

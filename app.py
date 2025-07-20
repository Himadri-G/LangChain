import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import ConversationChain

st.set_page_config(page_title="Chatbot", page_icon="💬")
st.title("My LangChain Chatbot")

# Maintain session state
if "history" not in st.session_state:
    st.session_state.history = []

prompt = st.chat_input("Type your message...")
if prompt:
    # Add user message to chat
    st.session_state.history.append({"role": "user", "content": prompt})

    # LangChain call (simple version)
    llm = OpenAI()
    response = llm(prompt)
    st.session_state.history.append({"role": "assistant", "content": response})

for msg in st.session_state.history:
    st.chat_message(msg['role']).markdown(msg['content'])



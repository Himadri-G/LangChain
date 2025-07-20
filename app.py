import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Your prompt template
template = """
Answer the question below based on our conversation history.

Conversation History:
{context}

Question:
{question}

Answer:
"""

# Initialize the model
model = OllamaLLM(model="llama3")

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Streamlit UI
st.set_page_config(page_title="Llama3 Ollama Chatbot")
st.header("💬 AI Chatbot (Llama3+Ollama)")

# Session state to remember conversation
if "history" not in st.session_state:
    st.session_state.history = "The conversation has just begun."
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input box at bottom
user_input = st.chat_input("Type your message and press Enter")

if user_input:
    context = st.session_state.history
    with st.spinner("Llama3 is thinking..."):
        try:
            result = chain.invoke({"context": context, "question": user_input})
            st.session_state.messages.append(("User", user_input))
            st.session_state.messages.append(("Llama3", result.strip()))
            st.session_state.history += f"\nUser: {user_input}\nAI: {result.strip()}"
        except Exception as e:
            st.session_state.messages.append(("Llama3", f"Sorry, I encountered an error: {e}"))

# Display chat
for sender, message in st.session_state.messages:
    if sender == "User":
        st.chat_message("user").markdown(message)
    else:
        st.chat_message("assistant").markdown(message)

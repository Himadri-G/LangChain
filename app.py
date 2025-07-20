import streamlit as st
<<<<<<< HEAD
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
=======
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
>>>>>>> 62d5f9c (Your commit message here)

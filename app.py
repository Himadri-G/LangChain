import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import time
from datetime import datetime

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
@st.cache_resource
def load_model():
    return OllamaLLM(model="llama3")

model = load_model()
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Enhanced Streamlit UI with custom styling
st.set_page_config(
    page_title="AI Assistant", 
    page_icon="🤖", 
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 800px;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: #f0f0f0;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Header
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Assistant</h1>
    <p>Powered by Llama3 & Ollama | Chat with intelligence</p>
</div>
""", unsafe_allow_html=True)

# Session state initialization
if "history" not in st.session_state:
    st.session_state.history = "The conversation has just begun."
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat button in main area
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.history = "The conversation has just begun."
        st.rerun()

# Main chat area
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display welcome message if no messages
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #666;">
        <h3>👋 Welcome to AI Assistant!</h3>
        <p>I'm here to help you with any questions. Start a conversation below!</p>
        <p><em>💡 Try asking me about:</em></p>
        <p>• General knowledge questions</p>
        <p>• Problem solving</p>
        <p>• Creative writing</p>
        <p>• Code explanations</p>
    </div>
    """, unsafe_allow_html=True)

# Display chat messages
for i, (sender, message) in enumerate(st.session_state.messages):
    if sender == "User":
        with st.chat_message("user", avatar="👤"):
            st.markdown(f"**You:** {message}")
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(f"**AI:** {message}")

st.markdown('</div>', unsafe_allow_html=True)

# Enhanced chat input
st.markdown("### 💬 Send a Message")
user_input = st.chat_input("Type your message here... 🚀", key="chat_input")

# Process user input
if user_input:
    # Add user message immediately
    st.session_state.messages.append(("User", user_input))
    
    # Show user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(f"**You:** {user_input}")
    
    # Show AI response with typing effect
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🤔 AI is thinking..."):
            try:
                context = st.session_state.history
                result = chain.invoke({"context": context, "question": user_input})
                
                # Clean up the result
                clean_result = result.strip()
                
                # Add to session state
                st.session_state.messages.append(("Llama3", clean_result))
                st.session_state.history += f"\nUser: {user_input}\nAI: {clean_result}"
                
                # Display AI response
                st.markdown(f"**AI:** {clean_result}")
                
                # Auto-scroll to bottom (rerun to show new messages)
                time.sleep(0.5)
                st.rerun()
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.session_state.messages.append(("Llama3", error_msg))
                st.error(error_msg)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🚀 Built with Streamlit, LangChain & Ollama | Created by Himadri Goswami</p>
</div>
""", unsafe_allow_html=True)

from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# # Define a prompt template for the chatbot
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

# Create the prompt template
prompt = ChatPromptTemplate.from_template(template)

# Combine prompt and model into a chain
chain = prompt | model

def handle_conversation():
    context = "The conversation has just begun."
    print("\n--- AI Chatbot (Powered by Llama3) ---")
    print("Ask me anything! Type 'exit' to quit.")
    print("--------------------------------------")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("\nLlama3: Goodbye! Thanks for chatting.")
            break
        print("Llama3: Thinking...")
        try:
            result = chain.invoke({"context": context, "question": user_input})
            print(f"Llama3: {result.strip()}")
            context += f"\nUser: {user_input}\nAI: {result.strip()}"
        except Exception as e:
            print(f"Llama3: Sorry, I encountered an error: {e}")

if __name__ == "__main__":
    handle_conversation()

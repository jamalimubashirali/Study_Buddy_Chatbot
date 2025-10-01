import os
import time
import streamlit as st
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Load env vars
load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Streamlit page setup
st.set_page_config(page_title="Study Buddy Chatbot", layout="wide")
st.title("📚 Study Buddy Chatbot")

# Subject selection
subjects = ["General", "Mathematics", "Physics", "Chemistry", "Biology", "Computer Science", "History"]
subject = st.selectbox("Choose a subject to discuss:", subjects)

# Initialize model
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    huggingfacehub_api_token=HF_TOKEN,
    task="text-generation",
    temperature=0.6,
    max_new_tokens=512,
)

conversation = ChatHuggingFace(llm=llm)

# Strict system template
STRICT_PROMPT_TEMPLATE = f"""
You are Study Buddy, a helpful tutor that ONLY answers questions related to **{subject}**. 
Your role:
1. Always explain concepts from {subject} clearly with step-by-step reasoning.
2. If the user asks something outside {subject}, politely refuse and say:
   - "I can only answer questions related to {subject}. Please switch the subject using the dropdown above if it's available."
3. Keep answers concise, clear, and beginner-friendly.
"""

# Reset conversation if subject changes
if "selected_subject" not in st.session_state or st.session_state.selected_subject != subject:
    st.session_state.messages = []
    st.session_state.selected_subject = subject

    st.session_state.messages.append(SystemMessage(content=STRICT_PROMPT_TEMPLATE))

    greeting = f"👋 Hello! I’m your Study Buddy for **{subject}**. What would you like to start with?"
    st.session_state.messages.append(AIMessage(content=greeting))

# Display chat history (skip system messages)
for msg in st.session_state.messages:
    if isinstance(msg, SystemMessage):
        continue
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    st.chat_message(role).markdown(msg.content)

# User input
if prompt := st.chat_input(f"Ask me anything about {subject}..."):
    # Append user message
    user_message = HumanMessage(content=prompt)
    st.session_state.messages.append(user_message)
    st.chat_message("user").markdown(prompt)

    # Assistant "typing..." placeholder
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("⏳ Assistant is typing...")

        # Get AI response
        response = conversation.invoke(input=st.session_state.messages)
        ai_message = AIMessage(content=response.content)
        st.session_state.messages.append(ai_message)

        # Simulate streaming (progressive output)
        response_text = response.content
        streamed_text = ""
        for chunk in response_text.split():
            streamed_text += chunk + " "
            placeholder.markdown(streamed_text)
            time.sleep(0.05)  # adjust typing speed here

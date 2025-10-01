import os
import time
import streamlit as st
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate

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
   "❌ I can only answer questions related to {subject}. Please switch the subject using the dropdown above if it's available."
3. Keep answers concise, clear, and beginner-friendly.
"""

# Prompt template to enforce system message
prompt_template = ChatPromptTemplate.from_messages([
    ("system", STRICT_PROMPT_TEMPLATE),
    ("user", "{question}")
])

# Reset session when subject changes
if "selected_subject" not in st.session_state or st.session_state.selected_subject != subject:
    st.session_state.messages = []
    st.session_state.selected_subject = subject

    greeting = f"👋 Hello! I’m your Study Buddy for **{subject}**. What would you like to start with?"
    st.session_state.messages.append(AIMessage(content=greeting))

# Display past chat history
for msg in st.session_state.messages:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    st.chat_message(role).markdown(msg.content)

# Guardrails: simple keyword check for subject mismatch
subject_keywords = {
    "Physics": ["force", "energy", "motion", "quantum", "gravity", "optics", "thermodynamics"],
    "Biology": ["cell", "dna", "plant", "animal", "organism", "reproduction", "evolution"],
    "Chemistry": ["molecule", "atom", "reaction", "bond", "compound", "periodic"],
    "Mathematics": ["algebra", "calculus", "geometry", "equation", "integral", "derivative"],
    "Computer Science": ["algorithm", "data", "programming", "machine learning", "AI", "database"],
    "History": ["war", "revolution", "empire", "ancient", "civilization", "king", "colony"]
}

if prompt := st.chat_input(f"Ask me anything about {subject}..."):
    # Show user input
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append(HumanMessage(content=prompt))

    # Guardrail check
    if subject != "General":
        # Look for obvious mismatch keywords
        other_subjects = [s for s in subject_keywords if s != subject]
        if any(word in prompt.lower() for s in other_subjects for word in subject_keywords[s]):
            response_text = f"❌ I can only answer questions related to **{subject}**. Please switch the subject using the dropdown above if it's available."
            st.session_state.messages.append(AIMessage(content=response_text))
            st.chat_message("assistant").markdown(response_text)
        else:
            # Generate response with strict prompt
            formatted_prompt = prompt_template.format_messages(question=prompt)
            response = conversation.invoke(input=formatted_prompt)
            response_text = response.content

            # Stream output
            with st.chat_message("assistant"):
                placeholder = st.empty()
                streamed_text = ""
                for chunk in response_text.split():
                    streamed_text += chunk + " "
                    placeholder.markdown(streamed_text)
                    time.sleep(0.05)
            st.session_state.messages.append(AIMessage(content=response_text))
    else:
        # General subject (no restrictions)
        formatted_prompt = prompt_template.format_messages(question=prompt)
        response = conversation.invoke(input=formatted_prompt)
        response_text = response.content

        with st.chat_message("assistant"):
            placeholder = st.empty()
            streamed_text = ""
            for chunk in response_text.split():
                streamed_text += chunk + " "
                placeholder.markdown(streamed_text)
                time.sleep(0.05)
        st.session_state.messages.append(AIMessage(content=response_text))

import streamlit as st
from google import genai

# Page Config
st.set_page_config(page_title="Personal AI Assistant", page_icon="🤖", layout="centered")

# Title Header
st.title("🤖 Personal AI Assistant")

# Initialize Gemini Client using Streamlit Secrets
@st.cache_resource
def get_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

try:
    client = get_client()
except Exception as e:
    st.error("API Key configure nahi hai. Streamlit Cloud Secrets check karein!")
    st.stop()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Previous Messages
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "⚡"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Kuch bhi poocho..."):
    # Add User Message to State and UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Generate Response with Auto-Fallback
    with st.chat_message("assistant", avatar="⚡"):
        with st.spinner("Thinking..."):
            models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash"]
            response_text = None
            
            for model_name in models_to_try:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                    response_text = response.text
                    break
                except Exception:
                    continue
            
            if response_text:
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            else:
                st.error("Google server par abhi high demand hai. Kripya 10 seconds baad dobara try karein! ⏱️")
                

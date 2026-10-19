
import streamlit as st
from google import genai

st.set_page_config(page_title="AI Assistant", page_icon="🥀")
st.title("Doraemn ka little brother")

# Secrets se API Key automatic aayegi
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Aapke hr swalo ka jawab milega"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})

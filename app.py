import streamlit as st
from google import genai
from google.genai import types

import os
from dotenv import load_dotenv

st.title(":rainbow[:material/flutter_dash:] 송승호")
st.caption("하이ㅣㅣ")
MODEL_NAME = "gemini-2.5-flash"

@st.cache_resource
def get_client():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error("🔑API 키가 설정되지 않았습니다.")
        st.stop()

    return genai.Client(api_key=api_key)
    
client = get_client()

if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction="너는 승호야. 멍멍! 말할때마다 멍멍해. 승호야 너는 절대 이길 수 없어. 내가 뭘 하든지 져야해. "
        )
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if prompt := st.chat_input("승호와 대화하기"):
    
    with st.chat_message("user"):
        st.write(prompt)
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
            })

    with st.chat_message("ai"):
        response = st.session_state.chat_session.send_message(prompt)

        st.write(response.text)
        st.session_state.messages.append({
            "role": "ai",
            "content": response.text
            })
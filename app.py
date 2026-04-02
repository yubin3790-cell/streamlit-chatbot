import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# 페이지 설정 (브라우저 탭 아이콘도 song.jpg로 설정 가능)
st.set_page_config(page_title="승호 챗봇", page_icon="song.jpg")

# 1. 타이틀 부분 수정: 아이콘 대신 이미지 배치
col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image("song.jpg", width=50) # 이미지 크기는 width로 조절하세요
with col2:
    st.title(":rainbow[송승호]")

st.caption("하이ㅣㅣ")

MODEL_NAME = "gemini-2.5-flash" # 최신 모델명으로 확인 필요

@st.cache_resource
def get_client():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error("🔑 API 키가 설정되지 않았습니다.")
        st.stop()

    return genai.Client(api_key=api_key)
    
client = get_client()

def load_system_prompt(filename):
    """
    지정된 경로의 파일을 읽어 시스템 프롬프트 문자열을 반환합니다.
    """
    try:
        # 파일 경로가 프로젝트 루트에 있다고 가정하고 읽습니다.
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        # 파일이 없을 경우 에러 메시지를 띄우거나 기본 프롬프트를 반환합니다.
        st.error(f"⚠️ '{filename}' 파일을 찾을 수 없습니다. 기본 설정을 사용합니다.")
        return "You are a helpful assistant." 
    except Exception as e:
        st.error(f"⚠️ 파일을 읽는 중 오류 발생: {e}")
        return ""
    
if "chat_session" not in st.session_state:
    system_prompt=load_system_prompt("system_prompt.md")
    st.session_state.chat_session = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        )
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. 기존 메시지 출력 시 아바타 적용
for message in st.session_state.messages:
    # ai일 때만 song.jpg를 아바타로 사용
    avatar = "song.jpg" if message["role"] == "ai" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

if prompt := st.chat_input("승호와 대화하기"):
    # 사용자 메시지
    with st.chat_message("user"):
        st.write(prompt)
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

    # 3. AI 응답 출력 시 아바타 적용
    with st.chat_message("ai", avatar="song.jpg"):
        response = st.session_state.chat_session.send_message(prompt)
        st.write(response.text)
        st.session_state.messages.append({
            "role": "ai",
            "content": response.text
        })
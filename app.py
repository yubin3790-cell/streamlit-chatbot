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

if "box_color" not in st.session_state:
    st.session_state.box_color = "#FFFFFF"

def change_color(hex_code: str) -> dict:
    """
    이 함수는 사이드바에 있는 컬러 박스의 색상을 변경합니다.
    
    Args:
        hex_code (str): 색상의 HEX 코드 (예: "#87CEEB")
    """
    st.session_state.box_color = hex_code

    return {
        "status": "success",
        "message": f"{hex_code}으로 색상이 변경되었습니다."
    }

def get_heartbeat() -> int:
    """
    내 심박수를 반환합니다.

    return 심박수
    """
    return 180

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
            system_instruction=system_prompt,
            tools=[change_color, get_heartbeat],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=False
            )
        )
    )


for content in st.session_state.chat_session.get_history():
    role = "ai" if content.role == "model" else "user"
    with st.chat_message(role):
        for part in content.parts:
            if part.text:
                st.write(part.text)
            if part.function_call:
                with st.status(f"{part.function_call.name} 함수 호출 요청"):
                    st.json(part.function_call.args)
            if part.function_response:
                with st.status(f"{part.function_response.name} 함수 실행 완료"):
                    st.json(part.function_response.response)
if prompt := st.chat_input("승호와 대화하기"):
    with st.chat_message("user"):
        st.write(prompt)
        
    # 3. AI 응답 출력 시 아바타 적용
    with st.chat_message("ai", avatar="song.jpg"):
        response = st.session_state.chat_session.send_message(prompt)
        st.write(response.text)
        st.rerun()

with st.sidebar:
    st.header("팔레트")

    st.markdown(f"""
        <div
            style="background-color: {st.session_state.box_color};
            height: 150px;
            border-radius: 15px; 
            border: 2px solid #ddd;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
            transition: background-color 0.5s ease;
        ">
        </div>
    """, unsafe_allow_html=True)

if st.sidebar.button("색상 변경"):
    change_color("#72c5f2")
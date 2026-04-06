import streamlit as st
import serial
import json

st.title("NeoPixel")


port = st.text_input("포트", value="COM3")

@st.cache_resource
def get_ser(port):
    try:
        return serial.Serial(port, 115200, timeout=1)
    except Exception as e:
        st.write(e)
        return None

ser = get_ser(port)

if ser is not None:
    st.success(f"{port} 연결 성공!")
else:
    st.error(f"{port}를 찾을 수 없습니다.")

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)

    return (r, g, b)

if color := st.color_picker("색상"):
    r,g,b = hex_to_rgb(color)

    payload = {
        "type": "pixel",
        "r": r,
        "g": g,
        "b": b
    }

    st.json(payload)

    if ser and ser.is_open:
        message = json.dumps(payload)
        ser.write(message.encode())
import streamlit as st
import requests
import json

# 페이지 설정
st.set_page_config(layout="wide", page_title="Chat Doc")

# config.json에서 API URL 및 API KEY 가져오기
with open('config.json') as config_file:
    config = json.load(config_file)

API_KEY = config["API_KEY"]
LAAS_PRESET_HASH = config["LAAS_PRESET_HASH"]

# LaaS Preset API 호출 함수 (POST 요청, chat/completions)
def get_chat_completions(messages):
    try:
        url = 'https://api-laas.wanted.co.kr/api/preset/v2/chat/completions'
        headers = {
            "project": "PROMPTHON_PRJ_385",
            "apiKey": API_KEY,
            "Content-Type": "application/json; charset=utf-8"
        }
        data = {
            "hash": LAAS_PRESET_HASH,
            "messages": [{"role": "user", "content": messages}],
            "params": {"task": "guide_generation", "contents": " "}
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            response_data = response.json()
            choices = response_data.get("choices", [])
            if choices:
                return choices[0]["message"]["content"]
            else:
                return "No result found."
        else:
            return f"LaaS API 호출 오류: {response.status_code}, {response.text}"
    except Exception as e:
        return f"LaaS API 호출 중 예외 발생: {e}"

# 제목
st.title("Chat Doc")
st.write("Input your messenger conversations and get them organized into concise guides.")

# 화면을 두 개의 열로 분할
left_column, right_column = st.columns(2)

# 왼쪽 열: 입력 섹션
with left_column:
    st.header("Input")
    user_input = st.text_area("Please enter the conversation:", height=300)
    if st.button("Generate Guide"):
        if user_input:
            with st.spinner("Generating guide..."):
                guide = get_chat_completions(user_input)
            # 오른쪽 열에 결과 표시
            with right_column:
                st.header("Generated Guide")
                st.write(guide)
        else:
            st.warning("Please enter a conversation")

# 오른쪽 열: 결과 섹션 (초기 상태)
with right_column:
    st.header("Generated Guide")
    st.write("The generated guide will appear here after you input a conversation and click 'Generate Guide'.")

# 스타일 적용
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
    }
    .stTextArea>div>div>textarea {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)


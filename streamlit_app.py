import streamlit as st
import requests
import json

# 페이지 설정
st.set_page_config(layout="wide", page_title="Chat Doc")

# CSS 스타일 정의
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .title {
        font-size: 50px;
        color: #4a4a4a;
        text-align: center;
        padding: 20px 0;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .subtitle {
        font-size: 18px;
        color: #666;
        text-align: center;
        margin-bottom: 30px;
        line-height: 1.5;
    }
    .stColumn {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .left-column {
        background-color: #e6e6e6;
    }
</style>
""", unsafe_allow_html=True)

# config.json에서 API URL 및 API KEY 가져오기
with open('config.json') as config_file:
    config = json.load(config_file)

API_KEY = config["API_KEY"]
LAAS_PRESET_HASH = config["LAAS_PRESET_HASH"]

# 제목 및 부제목
st.markdown('<h1 class="title">Chat Doc</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">I\'ll create a work guide to help you stay on task.<br>Please enter your Messenger conversations and I\'ll organize them into a task guide.</p>', unsafe_allow_html=True)


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


# 화면을 두 개의 열로 분할
left_column, right_column = st.columns([1, 1])

# 왼쪽 열: 입력 섹션
with left_column:
    st.markdown('<div class="stColumn left-column">', unsafe_allow_html=True)
    st.subheader("Input")
    user_input = st.text_area("Please enter the conversation:", height=300)
    if st.button("Generate Guide"):
        if user_input:
            with st.spinner("Generating guide..."):
                guide = get_chat_completions(user_input)
            # 오른쪽 열에 결과 표시
            with right_column:
                st.markdown('<div class="stColumn">', unsafe_allow_html=True)
                st.subheader("Generated Guide")
                st.write(guide)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Please enter a conversation")
    st.markdown('</div>', unsafe_allow_html=True)

# 오른쪽 열: 결과 섹션 (초기 상태)
with right_column:
    st.markdown('<div class="stColumn">', unsafe_allow_html=True)
    st.subheader("Generated Guide")
    st.write("The generated guide will appear here after you input a conversation and click 'Generate Guide'.")
    st.markdown('</div>', unsafe_allow_html=True)


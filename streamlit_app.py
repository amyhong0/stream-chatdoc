import streamlit as st
import requests
import json

# LaaS API 호출 함수
def get_chat_completions(messages):
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        api_key = config['API_KEY']
        laas_preset_hash = config['LAAS_PRESET_HASH']

        url = 'https://api-laas.wanted.co.kr/api/preset/v2/chat/completions'
        headers = {
            "project": "PROMPTHON_PRJ_385",
            "apiKey": api_key,
            "Content-Type": "application/json; charset=utf-8"
        }
        data = {
            "hash": laas_preset_hash,
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

# CSS 스타일 적용
st.markdown("""
    <style>
    body {
        background-color: black;
        color: white;
        font-family: Arial, sans-serif;
    }
    .title-section {
        text-align: center;
        padding: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
    }
    .title-section h1 {
        font-size: 3rem;
        color: white;
        font-weight: bold;
        text-shadow: 4px 4px 6px rgba(0, 0, 0, 0.7);
    }
    .title-section img {
        width: 60px;
        height: 60px;
    }
    .left-section, .right-section {
        background-color: #333333;
        padding: 20px;
        border-radius: 10px;
        margin: 10px;
        color: white;
    }
    .left-section {
        background-color: #4f4f4f;
    }
    .right-section {
        background-color: #333333;
    }
    h2 {
        font-size: 1.5rem;
        color: white;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
    }
    .stColumn > div {
        flex: 1;
        padding: 10px;
        max-width: 100%;
    }
    .stColumn {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 20px;
    }
    @media (min-width: 1000px) {
        .stColumn > div {
            max-width: 70%;
        }
    }
    @media (min-width: 1400px) {
        .stColumn > div {
            max-width: 45%;
        }
    }
    </style>
""", unsafe_allow_html=True)

# 메인 타이틀과 아이콘 함께 표시
st.markdown("""
    <div class="title-section">
        <img src="chatdoc_icon.png" alt="Chat Doc Icon">
        <h1>Chat Doc</h1>
    </div>
    <p style="text-align: center;">I'll create a work guide to help you stay on task. Please enter your Messenger conversations and I'll organize them into a task guide.</p>
""", unsafe_allow_html=True)

# Streamlit 레이아웃 설정 (두 개의 컬럼을 사용하여 좌우 섹션 나누기)
left_column, right_column = st.columns(2)

# 왼쪽 섹션: Conversation 입력
with left_column:
    st.markdown("""
    <div class="left-section">
        <h2>Conversation</h2>
        <p>Please enter the conversation:</p>
    """, unsafe_allow_html=True)
    conversation_input = st.text_area("", height=200)

    # Generate Guide 버튼: 입력창 아래에 배치
    if st.button('Generate Guide', key="generate_button"):
        if conversation_input:
            generated_guide = get_chat_completions(conversation_input)
            # 오른쪽 섹션에 마크다운 형식으로 결과 표시
            with right_column:
                st.markdown("""
                <div class="right-section">
                    <h2>Generated Guide</h2>
                    <p>The generated guide will appear here after you input a conversation and click 'Generate Guide'.</p>
                """, unsafe_allow_html=True)
                st.markdown(generated_guide, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 오른쪽 섹션: Generated Guide - 기본 화면에서 비어 있을 때 표시
if 'generated_guide' not in locals():
    with right_column:
        st.markdown("""
        <div class="right-section">
            <h2>Generated Guide</h2>
            <p>The generated guide will appear here after you input a conversation and click 'Generate Guide'.</p>
        </div>
        """, unsafe_allow_html=True)

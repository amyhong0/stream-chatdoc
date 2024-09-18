import streamlit as st
import requests
import json
import streamlit.components.v1 as components

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
        color: white;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit 레이아웃 설정 (두 개의 컬럼을 사용하여 좌우 섹션 나누기)
left_column, right_column = st.columns(2)

# 왼쪽 섹션: Conversation 입력
with left_column:
    st.markdown("""
    <div class="left-section">
        <h2>Conversation</h2>
        <p>Please enter the conversation:</p>
    </div>
    """, unsafe_allow_html=True)
    conversation_input = st.text_area("", height=200)

# 오른쪽 섹션: Generated Guide
with right_column:
    st.markdown("""
    <div class="right-section">
        <h2>Generated Guide</h2>
        <p>The generated guide will appear here after you input a conversation and click 'Generate Guide'.</p>
    </div>
    """, unsafe_allow_html=True)

    # Generate Guide 버튼
    if st.button('Generate Guide'):
        if conversation_input:
            generated_guide = get_chat_completions(conversation_input)
            st.text_area("Generated Guide", value=generated_guide, height=200)

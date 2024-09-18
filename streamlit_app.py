import streamlit as st
import requests
import json
import streamlit.components.v1 as components  # HTML을 렌더링하기 위한 모듈

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

# HTML 파일을 로드하는 함수
def load_html(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        html_content = f.read()
    return html_content

# Streamlit에서 HTML 파일 렌더링 (st.components.v1.html 사용)
components.html(load_html('layout.html'), height=200)  # 타이틀 섹션만 렌더링

# Streamlit 레이아웃 설정 (두 개의 컬럼을 사용하여 좌우 섹션 나누기)
left_column, right_column = st.columns(2)

# 왼쪽 섹션: Conversation 입력
with left_column:
    st.markdown("## Conversation")
    conversation_input = st.text_area("Please enter the conversation:", height=200)

    # Generate Guide 버튼
    if st.button('Generate Guide', key="generate_button"):
        if conversation_input:
            generated_guide = get_chat_completions(conversation_input)
            right_column.text_area("Generated Guide", value=generated_guide, height=200)

# 오른쪽 섹션: Generated Guide
with right_column:
    st.markdown("## Generated Guide")
    st.write("The generated guide will appear here after you input a conversation and click 'Generate Guide'.")

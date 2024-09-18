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

# Streamlit에서 HTML 파일 렌더링 (st.markdown 대신 st.components.v1.html 사용)
components.html(load_html('layout.html'), height=600)

# Streamlit 위젯 추가 (텍스트 입력 및 버튼)
st.write("### Conversation Input")
conversation_input = st.text_area("Enter your conversation here", height=200)
if st.button('Generate Guide'):
    if conversation_input:
        generated_guide = get_chat_completions(conversation_input)
        st.write("### Generated Guide")
        st.text_area("Generated Guide", value=generated_guide, height=200)

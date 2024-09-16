import streamlit as st
import requests
import json

# 페이지 설정을 최상단에 배치
st.set_page_config(page_title="Chat Doc", layout="wide")

# config.json 파일에서 API 키와 Hash값 불러오기
with open('config.json', 'r') as f:
    config = json.load(f)

API_KEY = config['API_KEY']
LAAS_PRESET_HASH = config['LAAS_PRESET_HASH']

# LaaS Preset API 호출 함수
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

# 스타일 시트 연결
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 타이틀과 아이콘
st.markdown("<h1 class='title'>Chat Doc</h1>", unsafe_allow_html=True)
st.markdown("<p class='description'>I'll create a work guide to help you stay on task.<br>"
            "Please enter your Messenger conversations and I'll organize them into a task guide.</p>",
            unsafe_allow_html=True)

# 2개의 섹션 레이아웃 정의
col1, col2 = st.columns(2)

# 왼쪽 섹션 (Conversation 입력)
with col1:
    with st.container():
        st.markdown("<div class='section-left'>", unsafe_allow_html=True)  # 섹션 전체를 감싸는 div 시작
        st.markdown("<h2 class='section-title'>Conversation</h2>", unsafe_allow_html=True)
        st.markdown("<p class='section-description'>Please enter the conversation:</p>", unsafe_allow_html=True)

        # 텍스트 입력 및 버튼 생성
        conversation_input = st.text_area("Enter your conversation here", height=300)
        if st.button("Generate Guide"):
            # LaaS API에 메시지를 보냄
            generated_guide = get_chat_completions(conversation_input)
        st.markdown("</div>", unsafe_allow_html=True)  # 섹션 전체를 감싸는 div 끝

# 오른쪽 섹션 (Generated Guide 표시)
with col2:
    with st.container():
        st.markdown("<div class='section-right'>", unsafe_allow_html=True)  # 섹션 전체를 감싸는 div 시작
        st.markdown("<h2 class='section-title'>Generated Guide</h2>", unsafe_allow_html=True)
        st.markdown("<p class='section-description'>The generated guide will appear here after you input a conversation and click 'Generate Guide'.</p>", unsafe_allow_html=True)

        # 챗봇 응답 출력
        if 'generated_guide' in locals():
            st.text_area("Generated Guide", value=generated_guide, height=300)
        st.markdown("</div>", unsafe_allow_html=True)  # 섹션 전체를 감싸는 div 끝



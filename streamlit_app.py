import streamlit as st
import requests
import json

# 스타일 시트 연결
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 페이지 설정
st.set_page_config(page_title="Chat Doc", layout="wide")

# 타이틀과 아이콘
st.markdown("<h1 class='title'>Chat Doc</h1>", unsafe_allow_html=True)
st.markdown("<p class='description'>I'll create a work guide to help you stay on task.<br>"
            "Please enter your Messenger conversations and I'll organize them into a task guide.</p>",
            unsafe_allow_html=True)

# 2개의 섹션 레이아웃 정의
col1, col2 = st.columns(2)

# 왼쪽 섹션 (Conversation 입력)
with col1:
    st.markdown("<h2 class='section-title'>Conversation</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-description'>Please enter the conversation:</p>", unsafe_allow_html=True)
    
    # 텍스트 입력 및 버튼 생성
    conversation_input = st.text_area("Enter your conversation here", height=300)
    if st.button("Generate Guide"):
        # LaaS API에 메시지를 보냄
        api_url = "https://api-laas.wanted.co.kr/api/preset/v2/chat/completions/"  # 실제 LaaS API 엔드포인트로 교체
        headers = {"Content-Type": "application/json"}
        data = {"message": conversation_input}
        
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            generated_guide = response.json().get("assistant", "Error: No response from the bot")
        else:
            generated_guide = "Error: Failed to connect to the bot."

# 오른쪽 섹션 (Generated Guide 표시)
with col2:
    st.markdown("<h2 class='section-title'>Generated Guide</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-description'>The generated guide will appear here after you input a conversation and click 'Generate Guide'.</p>", unsafe_allow_html=True)
    
    # 챗봇 응답 출력
    if 'generated_guide' in locals():
        st.text_area("Generated Guide", value=generated_guide, height=300)

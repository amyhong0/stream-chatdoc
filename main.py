import streamlit as st
import requests
import json

# 페이지 설정: 기본 타이틀 제거 및 레이아웃 설정
st.set_page_config(page_title="Chat Doc", layout="wide", initial_sidebar_state="collapsed")

# CSS를 사용하여 전체 배경을 블랙으로 설정
st.markdown(
    """
    <style>
    /* 전체 앱의 배경을 블랙으로 설정 */
    .stApp {
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
    h2 {
        font-size: 1.5rem;
        color: white;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 메인 타이틀과 아이콘 표시
st.markdown(
    """
    <div class="title-section">
        <img src="https://raw.githubusercontent.com/amyhong0/stream-chatdoc/main/chatdoc_icon.png" alt="Chat Doc Icon" width="60" height="60">
        <h1>Chat Doc</h1>
    </div>
    <p style="text-align:center;">I'll create a work guide to help you stay on task. Please enter your Messenger conversations and I'll organize them into a task guide.</p>
    """,
    unsafe_allow_html=True
)

# 좌우 섹션 나누기 (Streamlit의 columns 기능 사용)
left_column, right_column = st.columns(2)

# 왼쪽 섹션 (대화 입력)
with left_column:
    st.markdown(
        """
        <div class="left-section">
            <h2>Conversation</h2>
            <p>Please enter the conversation:</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # 대화 입력창 (Streamlit의 text_area 사용)
    conversation_input = st.text_area("Enter conversation:", height=200)

# 오른쪽 섹션 (생성된 가이드)
with right_column:
    st.markdown(
        """
        <div class="right-section">
            <h2>Generated Guide</h2>
            <p>The generated guide will appear here after you input a conversation and click 'Generate Guide'.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# 버튼 클릭 시 동작
if st.button('Generate Guide'):
    
    if conversation_input.strip() == "":
        st.error("Please enter a conversation.")
    
    else:
        
        # LaaS API 호출 함수 정의
        def get_chat_completions(messages):
            try:
                # config.json 파일에서 API 키와 해시값을 읽어옴
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

                # API 호출
                response = requests.post(url, headers=headers, json=data)

                # 상태 코드 확인
                if response.status_code == 200:
                    try:
                        # 응답을 JSON으로 파싱
                        response_data = response.json()
                        choices = response_data.get("choices", [])
                        if choices:
                            return choices[0]["message"]["content"]
                        else:
                            return "No result found."
                    except ValueError as e:
                        # JSON 파싱 오류 처리
                        return f"JSON 파싱 오류: {e}, 응답 내용: {response.text}"
                else:
                    # 상태 코드가 200이 아닌 경우 오류 메시지 출력
                    return f"LaaS API 호출 오류: {response.status_code}, {response.text}"

            except Exception as e:
                return f"LaaS API 호출 중 예외 발생: {e}"

        
        # API 호출 및 결과 표시
        generated_guide = get_chat_completions(conversation_input)
        
        with right_column:
            st.markdown(
                f"""
                <div class="right-section">
                    <h2>Generated Guide</h2>
                    <p>{generated_guide}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

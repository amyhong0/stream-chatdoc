import streamlit as st
import requests
import json
import os
from fpdf import FPDF

# 페이지 설정: 기본 타이틀 제거 및 레이아웃 설정
st.set_page_config(page_title="Chat Doc", layout="wide", initial_sidebar_state="collapsed")

# CSS를 사용하여 Nanum Gothic 웹폰트를 참조
st.markdown(
    """
    <style>
    /* Nanum Gothic 웹폰트 추가 */
    @import url('https://hangeul.pstatic.net/hangeul_static/css/nanum-gothic.css');

    /* 전체 앱의 배경을 블랙으로 설정 */
    .stApp {
        background-color: black;
        color: white;
        font-family: 'Nanum Gothic', sans-serif;
    }

    /* "Enter conversation:" 글씨를 흰색으로 설정 */
    .stTextArea label {
        color: white !important;
    }

    /* 버튼 스타일: 코랄 배경에 흰색 글씨 */
    .stButton > button {
        background-color: coral;
        color: white;
        padding: 10px 20px;
        font-size: 1rem;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        cursor: pointer;
    }

    /* PDF 저장 버튼 스타일: 진한 올리브 배경에 흰색 글씨 */
    .stDownloadButton > button, .stDownloadButton > button:hover {
        background-color: #8FBD24; /* 연두색 */
        color: white !important;
        padding: 10px 20px;
        font-size: 1rem;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        cursor: pointer;
    }

    /* 버튼 hover 시 색상 변경 */
    .stButton > button:hover {
        background-color: #DC7660; /* darker coral */
        color: white;
    }

    .stDownloadButton > button:hover {
        background-color: #356300; /* 짙은 연두색 */
        color: white;
    }
    .stButton > button:active, .stDownloadButton > button:active {
        opacity: 0.8;
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

    .right-section {
        display: flex;
        flex-direction: column;
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
   conversation_input = st.text_area("Enter conversation:", height=200, width=500)


# 현재 스크립트 파일이 위치한 경로
current_dir = os.path.dirname(os.path.abspath(__file__))

# NanumGothic.ttf 폰트 파일의 절대 경로 설정
font_path = os.path.join(current_dir, "NanumGothic.ttf")

# PDF 생성 함수 정의
def create_pdf(content, filename):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()

    # 나눔고딕 폰트 추가
    try:
        pdf.add_font('NanumGothic', '', font_path, uni=True)
        pdf.set_font('NanumGothic', size=12)
    except Exception as e:
        print(f"Font loading error: {e}")
        return

    # 여러 줄 텍스트를 PDF로 저장
    pdf.multi_cell(0, 10, txt=content)

    pdf.output(filename)

# 상태 변수로 generated_guide를 유지하기 위해 session state 사용
if 'generated_guide' not in st.session_state:
   st.session_state.generated_guide = ""

# 버튼 클릭 시 동작
if st.button('Generate Guide', key='generate_button', use_container_width=False, width=500):
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
                       return f"JSON 파싱 오류 {e}, 응답 내용 {response.text}"
               else:
                   return f"LaaS API 호출 오류 {response.status_code}: {response.text}"

           except Exception as e:
               return f"LaaS API 호출 중 예외 발생 {e}"

       # API 호출 및 결과를 session_state에 저장하여 유지
       st.session_state.generated_guide = get_chat_completions(conversation_input)

# 오른쪽 섹션 (생성된 가이드가 여기에 표시됨)
with right_column:
   st.markdown(
       f"""
       <div class="right-section">
           <h2>Generated Guide</h2>
           {st.session_state.generated_guide}
       </div>
       """,
       unsafe_allow_html=True,
   )

   # PDF 저장 버튼 추가 (오른쪽 아래에 배치)
   if st.session_state.generated_guide.strip():
       if create_pdf(st.session_state.generated_guide, 'generated_guide.pdf'):
           st.error("PDF creation failed. Please check font file.")
       else:
           with open('generated_guide.pdf', 'rb') as pdf_file:
               st.download_button(
                   'Save as PDF', 
                   pdf_file,
                   file_name='generated_guide.pdf', use_container_width=False, width=500,
                   key='download_button'
               )


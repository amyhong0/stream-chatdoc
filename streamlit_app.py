import streamlit as st
from PIL import Image
import base64
from io import BytesIO  # Import BytesIO

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
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        text-align: center;
        padding: 20px;
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
    .right-section {
        background-color: #333333;
    }
    h2 {
        font-size: 1.5rem;
        color: white;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
    }
    </style>
""", unsafe_allow_html=True)

# 메인 타이틀과 아이콘 함께 표시
icon_image = Image.open('chatdoc_icon.png')

# 아이콘을 base64로 인코딩하여 HTML에 삽입
buffered = BytesIO()
icon_image.save(buffered, format="PNG")
icon_base64 = base64.b64encode(buffered.getvalue()).decode()

st.markdown(f"""
<div class="title-section">
    <img src="data:image/png;base64,{icon_base64}" alt="Chat Doc Icon" style="width:60px;height:60px;">
    <h1>Chat Doc</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style="text-align:center;">I'll create a work guide to help you stay on task. Please enter your Messenger conversations and I'll organize them into a task guide.</p>
""", unsafe_allow_html=True)

# Streamlit 레이아웃 설정 (두 개의 컬럼을 사용하여 좌우 섹션 나누기)
left_column, right_column = st.columns(2)

# 왼쪽 섹션: Conversation 입력
with left_column:
    st.markdown("""
    <div class="left-section">

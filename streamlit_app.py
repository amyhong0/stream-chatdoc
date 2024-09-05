import streamlit as st
import requests
import json

# config.json에서 API URL 및 API KEY 가져오기
with open('config.json') as config_file:
    config = json.load(config_file)

API_KEY = config["API_KEY"]
LAAS_PRESET_HASH = config["LAAS_PRESET_HASH"]

st.title("Chat Doc")
st.write(
    "Input your messenger conversations and get them organized into concise guides."
)

# 사용자 입력
user_input = st.text_area("Please enter the conversation:", height=200)

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
            "params": {"task": "guide_generation", "contents": " "}  # API 문서에서 요구하는 작업 파라미터
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            response_data = response.json()
            # 응답에서 필요한 부분 추출
            choices = response_data.get("choices", [])
            if choices:
                return choices[0]["message"]["content"]
            else:
                return "No result found."
        else:
            return f"LaaS API 호출 오류: {response.status_code}, {response.text}"
    except Exception as e:
        return f"LaaS API 호출 중 예외 발생: {e}"

# 버튼 클릭 시 API 호출 및 결과 출력
if st.button("Generate Guide"):
    if user_input:
        guide = get_chat_completions(user_input)
        st.write(guide)
    else:
        st.write("Please enter a conversation")

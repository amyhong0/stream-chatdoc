import streamlit as st
import streamlit.components.v1 as components

# HTML 파일 로드 함수
def load_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Streamlit 앱 시작
st.title("Chat Doc - Streamlit Deployment")

# HTML 파일 로드 및 표시
html_content = load_html("index.html")
components.html(html_content, height=800, scrolling=True)

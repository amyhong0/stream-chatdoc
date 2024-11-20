import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정: 기본 타이틀 제거 및 레이아웃 설정
st.set_page_config(page_title=None, layout="wide", initial_sidebar_state="collapsed")

# HTML 파일 로드 함수
def load_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# HTML 파일 로드 및 표시
html_content = load_html("index.html")

# 전체 페이지에 HTML 삽입 (unsafe_allow_html=True로 Streamlit의 기본 스타일 무시)
components.html(html_content, height=800, scrolling=True)

import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정: 기본 타이틀 제거 및 레이아웃 설정
st.set_page_config(page_title=None, layout="wide", initial_sidebar_state="collapsed")

# HTML 코드 직접 삽입
html_content = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Chat Doc</title>
    <style>
      /* 전체 화면을 덮는 스타일 */
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
        background-color: black; /* 전체 배경색을 검정색으로 설정 */
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
      .title-section img {
        width: 60px;
        height: 60px;
      }
      .left-section,
      .right-section {
        background-color: #333333;
        padding: 20px;
        border-radius: 10px;
        margin: 10px;
        color: white;
        width: calc(50% - 40px); /* 두 섹션의 너비를 같게 설정 */
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
      .container {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 20px; /* 좌우 섹션 간의 간격 */
      }
      /* 화면 높이를 채우기 위한 추가 스타일 */
      .full-height {
          min-height: calc(100vh - 40px); /* 화면 높이를 채우도록 설정 */
          display: flex;
          flex-direction: column;
          justify-content: center; /* 세로 중앙 정렬 */
          align-items: center; /* 가로 중앙 정렬 */
          padding-bottom: 20px; /* 아래쪽 여백 추가 */
      }
    </style>
  </head>
  
  <body>
    <div class="full-height">
      <!-- 메인 타이틀과 아이콘 -->
      <div class="title-section">
        <img
          src="https://raw.githubusercontent.com/amyhong0/stream-chatdoc/main/chatdoc_icon.png"
          alt="Chat Doc Icon"
        />
        <!-- 아이콘 경로가 제대로 설정되어 있는지 확인 -->
        <h1>Chat Doc</h1>
      </div>
      
      <p style="text-align: center">
        I'll create a work guide to help you stay on task. Please enter your
        Messenger conversations and I'll organize them into a task guide.
      </p>

      <!-- 좌우 섹션을 나누는 컨테이너 -->
      <div class="container">
        
        <!-- 왼쪽 섹션 (대화 입력) -->
        <div class="left-section">
          <h2>Conversation</h2>
          <p>Please enter the conversation:</p>
          <textarea
            id="conversation_input"
            rows="10"
            style="border-radius: 10px; width: 100%"
          ></textarea>

          <!-- Generate Guide 버튼 스타일 추가 -->
          <button
            id="generate_button"
            style="
              margin-top: 10px;
              padding: 15px 30px;
              font-size: 1.2rem;
              font-weight: bold;
              background-color: coral;
              color: white;
              border: none;
              border-radius: 5px;
              cursor: pointer;
            "
          >
            Generate Guide
          </button>
        </div>

        <!-- 오른쪽 섹션 (생성된 가이드) -->
        <div class="right-section" id="generated_guide_section">
          <h2>Generated Guide</h2>
          <p>
            The generated guide will appear here after you input a conversation
            and click 'Generate Guide'.
          </p>
        </div>
        
      </div> <!-- container 끝 -->
      
    </div> <!-- full-height 끝 -->

    <!-- JavaScript 코드 -->
    <script>
      document
        .getElementById("generate_button")
        .addEventListener("click", async function () {
          // 대화 입력값 가져오기
          const conversation =
            document.getElementById("conversation_input").value;

          if (conversation.trim() === "") {
            alert("Please enter a conversation.");
            return;
          }

          try {
            // config.json 파일에서 API 키와 해시값을 가져오는 함수
            const configResponse = await fetch("config.json");
            const config = await configResponse.json();
            const apiKey = config.API_KEY;
            const laasPresetHash = config.LAAS_PRESET_HASH;

            // LaaS API 호출
            const response = await fetch(
              "https://api-laas.wanted.co.kr/api/preset/v2/chat/completions",
              {
                method: "POST",
                headers: {
                  project: "PROMPTHON_PRJ_385",
                  apiKey,
                  "Content-Type": "application/json; charset=utf-8",
                },
                body: JSON.stringify({
                  hash: laasPresetHash,
                  messages: [{ role: "user", content: conversation }],
                  params: { task: "guide_generation", contents: " " },
                }),
              }
            );

            if (response.ok) {
              const responseData = await response.json();
              const choices = responseData.choices || [];

              // 가이드가 성공적으로 생성되었을 경우
              if (choices.length > 0) {
                document.getElementById("generated_guide_section").innerHTML = `
                            <h2>Generated Guide</h2>
                            <p>${choices[0].message.content}</p>
                        `;
              } else {
                document.getElementById("generated_guide_section").innerHTML = `
                            <h2>Generated Guide</h2>
                            <p>No result found.</p>
                        `;
              }
            } else {
              // API 호출 오류 처리
              document.getElementById("generated_guide_section").innerHTML = `
                        <h2>Generated Guide</h2>
                        <p>LaaS API 호출 오류 ${response.status}: ${await response.text()}</p>`;
            }
          } catch (error) {
            // 예외 처리
            document.getElementById("generated_guide_section").innerHTML = `
                    <h2>Generated Guide</h2>
                    <p>LaaS API 호출 중 예외 발생 ${error.message}</p>`;
          }
        });
    </script>

  </body>
</html>
"""

# Streamlit에 HTML 삽입 (unsafe_allow_html=True로 Streamlit의 기본 스타일 무시)
components.html(html_content, height=800, scrolling=True)

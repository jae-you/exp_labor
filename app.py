import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="AI Workflow Design Experiment", layout="wide")

# 2. 스타일 설정
st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer { display: none !important; }
        #MainMenu { visibility: hidden; }
        .stApp { background-color: #1e1e1e; }
    </style>
""", unsafe_allow_html=True)

# 3. HTML/JS 소스코드
html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <style>
        /* --- CORE THEME --- */
        :root {
            --bg-color: #1e1e1e;
            --sidebar-width: 50px; 
            --editor-width: 38%;
            --chat-width: 62%;
            --text-color: #d4d4d4;
            --accent-color: #3794ff;
            --user-msg-bg: #2b313a;
            --ai-msg-bg: #1e1e1e;
            --input-bg: #2d2d2d;
        }
        body {
            margin: 0; padding: 0;
            font-family: 'Consolas', 'Pretendard', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            height: 100vh;
            display: flex; flex-direction: column; overflow: hidden;
        }
        
        .hidden { display: none !important; }
        .btn {
            background-color: var(--accent-color); color: white; border: none;
            padding: 12px 24px; cursor: pointer; font-size: 14px; border-radius: 6px;
            transition: opacity 0.2s;
        }
        .btn:hover { opacity: 0.9; }

        /* INTRO SCREEN */
        #intro-screen {
            display: flex; justify-content: center; align-items: center;
            height: 100%; background: radial-gradient(circle at center, #2a2a2a 0%, #000 100%);
        }
        .mail-window {
            width: 700px; background-color: #181818; border: 1px solid #333;
            border-radius: 12px; padding: 40px; box-shadow: 0 20px 50px rgba(0,0,0,0.7);
        }
        .req-list { background: #252526; padding: 20px; border-radius: 8px; border-left

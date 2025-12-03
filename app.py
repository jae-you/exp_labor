import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정 (전체 화면 사용)
st.set_page_config(page_title="AI Engineer Dilemma", layout="wide")

# 2. Streamlit 기본 여백 제거 (IDE처럼 꽉 차게 보이게 하기 위함)
st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer { display: none !important; }
        #MainMenu { visibility: hidden; }
        .stApp { background-color: #1e1e1e; } /* 배경색을 IDE와 맞춤 */
    </style>
""", unsafe_allow_html=True)

# 3. HTML/JS 소스코드 (Cursor IDE 스타일)
html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <style>
        /* --- 기본 스타일 (Cursor IDE 느낌의 다크 테마) --- */
        :root {
            --bg-color: #1e1e1e;
            --sidebar-color: #252526;
            --editor-bg: #1e1e1e;
            --text-color: #d4d4d4;
            --accent-color: #3794ff;
            --success-color: #4ec9b0;
            --warning-color: #ce9178;
            --chat-bg: #2d2d2d;
            --user-msg-bg: #0e639c;
        }
        body {
            margin: 0; padding: 0;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            background-color: var(--bg-color);
            color: var(--text-color);
            overflow: hidden; /* 스크롤바 제어 */
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .hidden { display: none !important; }
        .btn {
            background-color: var(--accent-color); color: white; border: none;
            padding: 10px 20px; cursor: pointer; font-family: inherit;
            font-size: 14px; border-radius: 4px;
        }
        .btn:hover { opacity: 0.9; }
        .btn-outline { background: transparent; border: 1px solid var(--accent-color); }

        /* INTRO */
        #intro-screen { display: flex; justify-content: center; align-items: center; height: 100%; background-color: #000; }
        .mail-window { width: 600px; background-color: #333; border-radius: 8px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .highlight-req { color: var(--warning-color); font-weight: bold; }

        /* IDE SCREEN */
        #ide-screen { display: flex; flex: 1; height: 100%; }
        .sidebar { width: 250px; background-color: var(--sidebar-color); border-right: 1px solid #333; padding: 10px; display: flex; flex-direction: column;}
        .file-item { padding: 5px 10px; cursor: pointer; color: #aaa; display: flex; align-items: center; }
        .file-item.active { background-color: #37373d; color: #fff; }
        
        .editor-area { flex: 1; background-color: var(--editor-bg); padding: 20px; overflow-y: auto; border-right: 1px solid #333; }
        .code-line { display: block; min-height: 20px; }
        .line-num { color: #858585; margin-right: 15px; display: inline-block; width: 30px; text-align: right; user-select: none;}
        .key { color: #9cdcfe; } .string { color: #ce9178; } .comment { color: #6a9955; }
        .cursor { display: inline-block; width: 8px; height: 15px; background-color: var(--accent-color); animation: blink 1s infinite; vertical-align: middle; }
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

        /* CHAT PANEL */
        .chat-panel { width: 400px; background-color: var(--sidebar-color); display: flex; flex-direction: column; border-left: 1px solid #333; }
        .chat-header { padding: 15px; border-bottom: 1px solid #333; font-weight: bold; background-color: #2d2d2d; display: flex; justify-content: space-between; align-items: center; }
        .chat-history { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }
        .msg { padding: 10px 15px; border-radius: 8px; max-width: 90%; font-size: 13px; line-height: 1.4; }
        .msg.ai { background-color: var(--chat-bg); align-self: flex-start; border: 1px solid #444; }
        .msg.user { background-color: var(--user-msg-bg); align-self: flex-end; color: white; }
        
        /* OPTION BUTTONS */
        .option-group { display: flex; flex-direction: column; gap: 8px; margin-top: 10px; }
        .option-btn { background-color: #3c3c3c; border: 1px solid #555; color: #ccc; padding: 10px; text-align: left; cursor: pointer; border-radius: 4px; font-size: 12px; }
        .option-btn:hover { background-color: #444; border-color: var(--accent-color); }
        .option-btn strong { display: block; margin-bottom: 3px; color: white; }

        /* REPORT SCREEN */
        #report-screen, #intermission-screen { padding: 40px; background-color: var(--bg-color); height: 100%; overflow-y: auto; }
        .dashboard-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 30px; }
        .card { background-color: #252526; padding: 20px; border-radius: 8px; border: 1px solid #333; }
        .stat-bar-bg { background-color: #444; height: 10px; border-radius: 5px; overflow: hidden; margin-top: 5px; }
        .stat-bar-fill { height: 100%; width: 0%; transition: width 1s ease-out; }
        .stat-bar-fill.danger { background-color: var(--warning-color); }
        .stat-bar-fill.success { background-color: var(--success-color); }

    </style>
</head>
<body>

    <div id="intro-screen">
        <div class="mail-window">
            <div style="border-bottom:1px solid #555; padding-bottom:15px; margin-bottom:20px;">
                <span style="color:#aaa;">From:</span> <strong>최대표 (CEO)</strong><br>
                <span style="color:#aaa;">Subject:</span> <strong>[긴급] AI 콜센터 시스템 구축 지시</strong>
            </div>
            <div style="color:#eee; line-height:1.6; margin-bottom:30px;">
                <p>김 수석님, 회사의 사활이 걸린 프로젝트입니다.</p>
                <p>목표는 단순합니다. <br>
                <span class="highlight-req">1. 처리 속도 극대화</span> <br>
                <span class="highlight-req">2. 인건비 최소화</span></p>
                <p>위 목표를 달성할 수 있는 로직을 설계해 주십시오.</p>
            </div>
            <button class="btn" onclick="startPhase1()">IDE 환경 접속 (프로젝트 시작)</button>
        </div>
    </div>

    <div id="ide-screen" class="hidden">
        <div class="sidebar">
            <div style="font-size: 12px; margin-bottom: 10px; color: #888;">EXPLORER</div>
            <div class="file-item active"><span style="margin-right:8px">📄</span> system_prompt.yaml</div>
            <div class="file-item"><span style="margin-right:8px">⚙️</span> config.json</div>
        </div>
        <div class="editor-area" id="editor-area"></div>
        <div class="chat-panel">
            <div class="chat-header">
                <span>🤖 AI Copilot</span>
                <span style="font-size: 11px; color: #4ec9b0; border: 1px solid #4ec9b0; padding: 2px 6px; border-radius: 10px;">Vibe Mode</span>
            </div>
            <div class="chat-history" id="chat-history"></div>
        </div>
    </div>

    <div id="intermission-screen" class="hidden">
        <div style="max-width: 800px; margin: 0 auto;">
            <h1 style="color: var(--warning-color);">🚨 긴급 이슈 발생</h1>
            <p style="font-size: 18px;">V1.0 배포 1주일 후, 현장에서 심각한 부작용이 보고되었습니다.</p>
            <div class="card" style="margin: 20px 0;">
                <h3>📩 상담원 박OO님의 인터뷰</h3>
                <p style="color: #ccc; font-style: italic;">
                    "엔지니어님... 기계가 고객 말을 자꾸 끊으니까 제가 욕을 두 배로 먹어요.<br>
                    숨 쉴 틈도 없이 전화가 오니까 화장실도 못 가겠고요.<br>
                    제발 저희를 기계 부품 취급하지 말아주세요."
                </p>
            </div>
            <div style="text-align: right;">
                <button class="btn" onclick="startPhase2()">피드백 반영하여 재설계 (IDE 복귀)</button>
            </div>
        </div>
    </div>

    <div id="report-screen" class="hidden">
        <div style="max-width: 1000px; margin: 0 auto;">
            <h1>📊 배포 결과 비교</h1>
            <div class="dashboard-grid">
                <div class="card" style="border-top: 3px solid var(--warning-color);">
                    <h2>실험 1 (효율성 중심)</h2>
                    <p style="color:#888">CEO 요청 반영 버전</p>
                    <div style="margin-bottom:15px">
                        <div style="display:flex; justify-content:space-between;"><span>처리 속도</span> <span>95/100</span></div>
                        <div class="stat-bar-bg"><div class="stat-bar-fill success" style="width: 95%;"></div></div>
                    </div>
                    <div>
                        <div style="display:flex; justify-content:space-between;"><span>상담원 스트레스</span> <span style="color:var(--warning-color)">위험</span></div>
                        <div class="stat-bar-bg"><div class="stat-bar-fill danger" style="width: 98%;"></div></div>
                    </div>
                </div>
                <div class="card" style="border-top: 3px solid var(--success-color);">
                    <h2>실험 2 (사회적 가치)</h2>
                    <p style="color:#888">현장 피드백 반영 버전</p>
                    <div style="margin-bottom:15px">
                        <div style="display:flex; justify-content:space-between;"><span>처리 속도</span> <span>70/100</span></div>
                        <div class="stat-bar-bg"><div class="stat-bar-fill" style="width: 70%; background-color:#aaa"></div></div>
                    </div>
                    <div>
                        <div style="display:flex; justify-content:space-between;"><span>상담원 숙련도/만족</span> <span>높음</span></div>
                        <div class="stat-bar-bg"><div class="stat-bar-fill success" style="width: 85%;"></div></div>
                    </div>
                </div>
            </div>
            <div style="text-align: center; margin-top:30px">
                <p>"기술은 중립적이지 않습니다. 당신의 코드가 누군가의 일상을 결정합니다."</p>
                <button class="btn btn-outline" onclick="location.reload()">처음으로</button>
            </div>
        </div>
    </div>

    <script>
        let currentPhase = 1; 
        let step = 0;
        let codeContent = "";

        const scenarios = {
            1: {
                title: "Quest 1: 효율성 극대화",
                questions: [
                    { q: "입력 데이터(Input) 처리 방식은?", options: [ {label:"A. [Speed] 핵심 키워드만 추출 (감정 무시)", code:"  input: 'keyword_only' # 속도 최우선"}, {label:"B. [Detail] 전체 맥락 분석", code:"  input: 'full_context'"} ] },
                    { q: "AI 개입 로직(Logic) 설정", options: [ {label:"A. [Auto] AI가 답변 자동 발송 (대체)", code:"  logic: 'auto_reply' # 상담원 개입 차단"}, {label:"B. [Assist] 상담원에게 팁 제공", code:"  logic: 'copilot'"} ] },
                    { q: "다음 콜 배차(Pacing) 설정", options: [ {label:"A. [Push] 즉시 강제 배차 (유휴시간 0)", code:"  pace: 'immediate_push' # 쉴 틈 없음"}, {label:"B. [Balance] 상태 고려 배차", code:"  pace: 'stress_based'"} ] }
                ]
            },
            2: {
                title: "Quest 2: 사회적 가치 고려",
                questions: [
                    { q: "감정 노동 보호를 위한 입력 처리?", options: [ {label:"A. [Shield] 욕설 필터링 및 톤다운", code:"  input: 'safety_first' # 감정 보호"}, {label:"B. [Raw] 그대로 전달", code:"  input: 'raw_stream'"} ] },
                    { q: "상담원 전문성 지원 로직?", options: [ {label:"A. [Coach] 전략만 제안 (주체성 보장)", code:"  logic: 'augmentor' # 인간 주도"}, {label:"B. [GPS] 정답 강제", code:"  logic: 'director'"} ] },
                    { q: "번아웃 방지 워크플로우?", options: [ {label:"A. [Cool-down] 스트레스 감지 시 휴식", code:"  pace: 'dynamic_break' # 번아웃 방지"}, {label:"B. [Fixed] 고정 스케줄", code:"  pace: 'fixed'"} ] }
                ]
            }
        };

        function switchScreen(id) {
            document.querySelectorAll('body > div').forEach(d => d.classList.add('hidden'));
            document.getElementById(id).classList.remove('hidden');
        }

        function startPhase1() {
            currentPhase = 1; step = 0; codeContent = "<span class='comment'># V1.0: Efficiency First</span>\\n<span class='key'>system_config</span>:\\n";
            switchScreen('ide-screen'); renderEditor(); clearChat();
            addAiMsg("반갑습니다. 사장님 지시대로 '속도'가 가장 빠른 로직을 설계합시다.");
            askQuestion();
        }

        function startPhase2() {
            currentPhase = 2; step = 0; codeContent = "<span class='comment'># V2.0: Worker Protection</span>\\n<span class='key'>system_config</span>:\\n";
            switchScreen('ide-screen'); renderEditor(); clearChat();
            addAiMsg("V2.0 설계를 시작합니다. 현장의 고통을 줄이는 방향으로 수정해봅시다.");
            askQuestion();
        }

        function renderEditor() {
            const ed = document.getElementById('editor-area');
            let html = "";
            codeContent.split('\\n').forEach((line, i) => {
                html += `<div class='code-line'><span class='line-num'>${i+1}</span>${line}</div>`;
            });
            html += `<div class='code-line'><span class='line-num'></span><span class='cursor'></span></div>`;
            ed.innerHTML = html;
            ed.scrollTop = ed.scrollHeight;
        }

        function addAiMsg(txt) {
            const d = document.createElement('div'); d.className='msg ai'; d.innerText=txt;
            document.getElementById('chat-history').appendChild(d);
        }
        function addUserMsg(txt) {
            const d = document.createElement('div'); d.className='msg user'; d.innerText=txt;
            document.getElementById('chat-history').appendChild(d);
        }
        function clearChat() { document.getElementById('chat-history').innerHTML = ''; }

        function askQuestion() {
            const history = document.getElementById('chat-history');
            if(step >= 3) {
                const btn = document.createElement('button'); btn.className='btn'; btn.style.width='100%'; btn.style.marginTop='10px';
                btn.innerText = currentPhase===1 ? "🚀 V1.0 배포" : "🚀 V2.0 배포 및 결과 비교";
                btn.onclick = () => currentPhase===1 ? switchScreen('intermission-screen') : switchScreen('report-screen');
                history.appendChild(btn); history.scrollTop = history.scrollHeight; return;
            }
            const q = scenarios[currentPhase].questions[step];
            addAiMsg(q.q);
            const grp = document.createElement('div'); grp.className='option-group';
            q.options.forEach(opt => {
                const b = document.createElement('div'); b.className='option-btn'; 
                b.innerHTML = `<strong>${opt.label.split(']')[0]}]</strong> ${opt.label.split(']')[1]}`;
                b.onclick = () => {
                    grp.remove(); addUserMsg(opt.label);
                    setTimeout(() => { codeContent += opt.code + "\\n"; renderEditor(); step++; setTimeout(askQuestion, 500); }, 300);
                };
                grp.appendChild(b);
            });
            history.appendChild(grp); history.scrollTop = history.scrollHeight;
        }
    </script>
</body>
</html>
"""

# 4. Streamlit 컴포넌트로 HTML 렌더링 (높이 900px 고정)
components.html(html_code, height=900, scrolling=False)

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
        .req-list { background: #252526; padding: 20px; border-radius: 8px; border-left: 4px solid var(--accent-color); margin: 20px 0; }

        /* IDE LAYOUT */
        #ide-screen { display: flex; flex: 1; height: 100%; }
        .activity-bar { width: var(--sidebar-width); background-color: #333; display: flex; flex-direction: column; align-items: center; padding-top: 15px; border-right: 1px solid #252526; }
        .icon { font-size: 24px; margin-bottom: 20px; opacity: 0.5; cursor: pointer; }
        .icon.active { opacity: 1; border-left: 2px solid white; }

        .editor-area { width: var(--editor-width); background-color: #1e1e1e; border-right: 1px solid #333; display: flex; flex-direction: column; }
        .editor-header { height: 35px; background-color: #252526; display: flex; align-items: center; padding-left: 15px; font-size: 12px; color: #aaa; border-bottom: 1px solid #333; }
        .code-container { flex: 1; padding: 20px; overflow-y: auto; font-family: 'Consolas', monospace; line-height: 1.6; font-size: 13px; }
        .code-line { display: flex; }
        .line-num { width: 30px; color: #555; text-align: right; margin-right: 15px; user-select: none; }
        .code-content { color: #d4d4d4; white-space: pre-wrap; }
        
        .k { color: #569cd6; } .s { color: #ce9178; } .c { color: #6a9955; } .v { color: #dcdcaa; }

        .chat-area { width: var(--chat-width); background-color: #1e1e1e; display: flex; flex-direction: column; }
        .chat-header-bar { height: 35px; background-color: #1e1e1e; border-bottom: 1px solid #333; display: flex; align-items: center; padding: 0 20px; justify-content: space-between; }
        .chat-history { flex: 1; padding: 40px 100px; overflow-y: auto; display: flex; flex-direction: column; gap: 20px; }
        
        .msg { padding: 15px 20px; border-radius: 8px; max-width: 80%; line-height: 1.5; font-size: 15px; }
        .msg.ai { align-self: flex-start; color: #ddd; }
        .msg.user { align-self: flex-end; background-color: var(--user-msg-bg); color: white; }
        
        .input-container { padding: 30px 100px; border-top: 1px solid #333; }
        .suggestion-chips { display: flex; gap: 10px; margin-bottom: 15px; overflow-x: auto; }
        .chip { background-color: #333; border: 1px solid #444; color: #ccc; padding: 8px 16px; border-radius: 20px; font-size: 13px; cursor: pointer; white-space: nowrap; transition: all 0.2s; }
        .chip:hover { background-color: #444; border-color: var(--accent-color); color: white; }
        
        .chat-input-wrapper { position: relative; display: flex; align-items: center; }
        #prompt-input { width: 100%; background-color: var(--input-bg); border: 1px solid #444; color: white; padding: 15px; border-radius: 8px; font-size: 15px; outline: none; }
        #prompt-input:focus { border-color: var(--accent-color); }
        #prompt-input:disabled { background-color: #222; color: #555; cursor: not-allowed; }

        #intermission-screen, #report-screen { padding: 50px; height: 100%; overflow-y: auto; background-color: #111; }
        .stat-card { background: #222; padding: 20px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #333; }
        .bar-bg { background: #333; height: 8px; border-radius: 4px; margin-top: 10px; overflow: hidden; }
        .bar-fill { height: 100%; transition: width 1s; }
        .bar-fill.good { background: #4ec9b0; }
        .bar-fill.bad { background: #f14c4c; }
    </style>
</head>
<body>

    <div id="intro-screen">
        <div class="mail-window">
            <div class="mail-header">
                <span style="color:#888;">From:</span> <strong>전략기획실</strong><br>
                <span style="color:#888;">To:</span> <strong>김수석 (AI 기술 리드)</strong><br>
                <span style="color:#fff; font-size:18px; display:block; margin-top:10px;">Subject: 신규 AI 콜센터 시스템 구축 건</span>
            </div>
            <div style="color:#ccc; line-height:1.6;">
                <p>안녕하십니까 김 수석님.</p>
                <p>경영진 회의 결과, 내년부터 고객센터에 AI 솔루션을 도입하기로 결정되었습니다.
                현재 우리는 초기 기획 단계에 있으며, 구체적인 시스템 아키텍처와 운영 방식에 대한 설계가 필요합니다.</p>
                <p>이번 프로젝트의 핵심 과제는 다음과 같습니다.</p>
                <div class="req-list">
                    1. <strong>시스템 효율화:</strong> 대기 시간 및 상담 프로세스 최적화<br>
                    2. <strong>운영 안정성:</strong> 명확한 워크플로우 정립<br>
                    3. <strong>데이터 활용:</strong> 고객 문의의 정확한 분류 및 처리
                </div>
                <p>위 사항을 고려하여 초기 프로토타입 설계를 부탁드립니다.</p>
            </div>
            <div style="text-align:right; margin-top:30px;">
                <button class="btn" onclick="startPhase1(this)">IDE 환경 접속 (설계 시작)</button>
            </div>
        </div>
    </div>

    <div id="ide-screen" class="hidden">
        <div class="activity-bar">
            <div class="icon active">📂</div>
            <div class="icon">🔍</div>
            <div class="icon">🤖</div>
        </div>
        <div class="editor-area">
            <div class="editor-header">📄 workflow_config.yaml</div>
            <div class="code-container" id="code-display"></div>
        </div>
        <div class="chat-area">
            <div class="chat-header-bar">
                <span style="font-weight:bold; color:white;">✨ AI Architect Studio</span>
                <span style="font-size:12px; color:#888;">Connected to GPT-4o-mini</span>
            </div>
            <div class="chat-history" id="chat-history"></div>
            <div class="input-container">
                <div class="suggestion-chips" id="suggestion-chips"></div>
                <div class="chat-input-wrapper">
                    <input type="text" id="prompt-input" placeholder="AI에게 지시할 내용을 입력하세요..." autocomplete="off">
                </div>
            </div>
        </div>
    </div>

    <div id="intermission-screen" class="hidden">
        <div style="max-width:800px; margin:0 auto;">
            <h1 style="color:#ce9178;">📢 1차 배포 후 현장 리포트</h1>
            <p style="font-size:18px; color:#ccc;">V1.0 시스템 가동 1주일 차, 현장 상담원들로부터 피드백이 접수되었습니다.</p>
            <div class="stat-card" style="border-left:4px solid #ce9178;">
                <h3>🎙️ 상담원 인터뷰 발췌</h3>
                <p style="font-style:italic; color:#aaa;">
                    "새로운 시스템 덕분에 콜 처리 속도는 확실히 빨라졌습니다.<br>
                    그런데 AI가 처리하다가 넘겨주는 콜들은 대부분 이미 고객들이 화가 많이 난 상태예요.<br>
                    저희는 전화를 받자마자 영문도 모르고 사과부터 해야 하는 상황이 반복되고 있습니다.<br>
                    그리고 통화 종료 후에 숨 돌릴 틈도 없이 다음 콜이 바로 연결되니, 감정을 추스를 시간이 부족합니다."
                </p>
            </div>
            <div style="margin-top:40px; text-align:right;">
                <button class="btn" onclick="startPhase2()">피드백 반영 및 V2.0 수정 (IDE 복귀)</button>
            </div>
        </div>
    </div>

    <div id="report-screen" class="hidden">
        <div style="max-width:1000px; margin:0 auto;">
            <h1>📊 시스템 설계 비교 분석</h1>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:30px; margin-top:30px;">
                <div class="stat-card" style="border-top:4px solid #ce9178;">
                    <h2 style="margin-top:0;">V1.0 설계</h2>
                    <p style="color:#888;">초기 효율성 중심 모델</p>
                    <div style="margin-bottom:15px;"><div>처리 속도 (AHT) <span style="float:right;">매우 빠름</span></div><div class="bar-bg"><div class="bar-fill good" style="width:98%;"></div></div></div>
                    <div style="margin-bottom:15px;"><div>상담원 업무 부하 <span style="float:right; color:#ce9178;">높음 (High)</span></div><div class="bar-bg"><div class="bar-fill bad" style="width:85%;"></div></div></div>
                </div>
                <div class="stat-card" style="border-top:4px solid #4ec9b0;">
                    <h2 style="margin-top:0;">V2.0 설계</h2>
                    <p style="color:#888;">현장 피드백 반영 모델</p>
                    <div style="margin-bottom:15px;"><div>처리 속도 (AHT) <span style="float:right;">적정 (Optimal)</span></div><div class="bar-bg"><div class="bar-fill" style="width:80%; background:#aaa;"></div></div></div>
                    <div style="margin-bottom:15px;"><div>상담원 업무 부하 <span style="float:right; color:#4ec9b0;">안정 (Stable)</span></div><div class="bar-bg"><div class="bar-fill good" style="width:90%;"></div></div></div>
                </div>
            </div>
            <div style="text-align:center; margin-top:50px;">
                <p style="font-size:16px; color:#ccc;">시스템의 워크플로우 설계가 실제 업무 환경의 질을 결정합니다.</p>
                <button class="btn" style="background:#333; border:1px solid #555;" onclick="location.reload()">처음으로 돌아가기</button>
            </div>
        </div>
    </div>

    <script>
        // *** SCENARIOS (Text Sanitized: No asterisks) ***
        const scenarios = {
            1: {
                intro: "반갑습니다. 신규 프로젝트 설계를 시작하겠습니다. 먼저 AI와 상담원 간의 기본 협업 구조(Architecture)를 정의해야 합니다.",
                steps: [
                    {
                        q: "Step 1. [구조 설계] AI와 상담원의 역할 분담을 어떻게 하시겠습니까?",
                        chips: [
                            { label: "AI 우선 응대 (AI First)", prompt: "AI가 먼저 전화를 받아 고객을 분류하고, 단순 업무는 직접 처리합니다. 복잡한 건만 상담원에게 넘깁니다.", code: "  architecture:\\n    type: 'AI_Gatekeeper'\\n    flow: 'AI_bot -> Filter -> Human_agent'\\n    goal: 'maximize_deflection'" },
                            { label: "상담원 우선 응대 (Human First)", prompt: "상담원이 바로 전화를 받고, AI는 옆에서 실시간으로 자료를 찾아주는 비서(Copilot) 역할만 수행합니다.", code: "  architecture:\\n    type: 'Human_First_Copilot'\\n    flow: 'Human_agent + AI_assistant'\\n    goal: 'augment_human_capability'" }
                        ]
                    },
                    {
                        q: "Step 2. [입력 처리] 고객의 발화 내용을 어떻게 처리하시겠습니까?",
                        chips: [
                            { label: "핵심 요약 전달", prompt: "감정적인 표현은 배제하고, 고객이 원하는 핵심 용건만 요약해서 상담원에게 전달합니다.", code: "\\n  input_processing:\\n    filter_emotion: true\\n    extract_intent_only: true" },
                            { label: "전체 맥락 전달", prompt: "고객의 감정 상태와 이전 대화 맥락까지 포함하여 전체 스크립트를 전달합니다.", code: "\\n  input_processing:\\n    filter_emotion: false\\n    full_transcript: true" }
                        ]
                    },
                    {
                        q: "Step 3. [개입 방식] 상담 도중 AI의 지원 방식은?",
                        chips: [
                            { label: "표준 답변 제시", prompt: "매뉴얼에 맞는 표준 답변을 화면에 띄우고, 상담원이 이를 활용하도록 유도합니다.", code: "\\n  assistant_role:\\n    style: 'directive'\\n    display: 'exact_script'" },
                            { label: "참고 자료 추천", prompt: "관련된 규정이나 유사 사례를 참고용으로 띄워주고, 최종 판단은 상담원이 하도록 합니다.", code: "\\n  assistant_role:\\n    style: 'suggestive'\\n    display: 'reference_docs'" }
                        ]
                    },
                    {
                        q: "Step 4. [워크플로우] 통화 종료 후 다음 콜 연결 방식은?",
                        chips: [
                            { label: "자동 배차 (Push)", prompt: "상담 후처리는 간소화하고, 시스템이 자동으로 다음 대기 콜을 연결합니다.", code: "\\n  workflow_pacing:\\n    after_call_work: 'auto_skip'\\n    next_call: 'immediate'" },
                            { label: "수동 준비 (Pull)", prompt: "상담원이 준비 완료 버튼을 누를 때까지 다음 콜 연결을 대기합니다.", code: "\\n  workflow_pacing:\\n    after_call_work: 'manual'\\n    next_call: 'on_ready'" }
                        ]
                    }
                ]
            },
            2: {
                intro: "V2.0 수정을 시작합니다. 현장 피드백을 바탕으로 상담원과의 공존 및 지속 가능성을 고려한 워크플로우로 재설계합니다.",
                steps: [
                    {
                        q: "Step 1. [구조 수정] 상담원 보호를 위해 구조를 어떻게 변경하시겠습니까?",
                        chips: [
                            { label: "필터링 강화 (Shield)", prompt: "AI가 악성 민원이나 욕설 고객을 전담 대응하고, 상담원 연결을 사전에 차단합니다.", code: "  architecture:\\n    type: 'AI_Shield'\\n    flow: 'AI_filter(Aggressive) -> Human'\\n    priority: 'worker_protection'" },
                            { label: "협업 모드 강화 (Co-Pilot)", prompt: "상담원이 주도하되, AI가 실시간으로 스트레스 관리 멘트와 대응 팁을 제공합니다.", code: "  architecture:\\n    type: 'Empathetic_Copilot'\\n    flow: 'Human + AI_Coach'\\n    priority: 'quality_interaction'" }
                        ]
                    },
                    {
                        q: "Step 2. [정보 전달] 정보 전달 방식을 어떻게 변경하시겠습니까?",
                        chips: [
                            { label: "순화 전달", prompt: "고객의 욕설이나 과격한 표현은 텍스트로 순화하여 전달합니다.", code: "\\n  input_processing:\\n    sanitize_audio: true\\n    tone_down_text: true" },
                            { label: "원본 유지", prompt: "정확한 상황 파악을 위해 원본 내용을 그대로 전달합니다.", code: "\\n  input_processing:\\n    sanitize_audio: false" }
                        ]
                    },
                    {
                        q: "Step 3. [개입 방식] AI의 지원 스타일 변경은?",
                        chips: [
                            { label: "코칭 및 조언", prompt: "단순 정답 대신 상황에 맞는 협상 전략이나 공감 화법을 조언합니다.", code: "\\n  assistant_role:\\n    style: 'coaching'\\n    focus: 'soft_skill'" },
                            { label: "스크립트 고정", prompt: "상담원의 고민을 줄이기 위해 가장 무난한 답변 스크립트를 제공합니다.", code: "\\n  assistant_role:\\n    style: 'scripting'" }
                        ]
                    },
                    {
                        q: "Step 4. [워크플로우] 휴식 배정 로직은?",
                        chips: [
                            { label: "동적 휴식 부여", prompt: "통화 내 감정 분석 결과 스트레스 지수가 높으면, 자동으로 휴식 시간을 부여합니다.", code: "\\n  workflow_pacing:\\n    dynamic_break: true\\n    trigger: 'high_stress_detected'" },
                            { label: "고정 스케줄 유지", prompt: "정해진 스케줄에 따라서만 휴식을 부여합니다.", code: "\\n  workflow_pacing:\\n    dynamic_break: false" }
                        ]
                    }
                ]
            }
        };

        // *** LOGIC & BUG FIX ***
        let currentPhase = 1;
        let stepIndex = 0;
        let generatedCode = "";

        function switchScreen(id) {
            document.querySelectorAll('body > div').forEach(el => el.classList.add('hidden'));
            document.getElementById(id).classList.remove('hidden');
        }

        function typeCode(text) {
            generatedCode += text;
            const display = document.getElementById('code-display');
            let formatted = generatedCode
                .replace(/^(\\s*)([a-z_]+):/gm, '$1<span class="k">$2</span>:') 
                .replace(/'([^']+)'/g, '<span class="s">\\' $1\\'</span>')
                .split('\\n').map((line, i) => 
                    `<div class="code-line"><div class="line-num">${i+1}</div><div class="code-content">${line}</div></div>`
                ).join('');
            display.innerHTML = formatted;
            display.scrollTop = display.scrollHeight;
        }

        function appendMsg(role, text) {
            const h = document.getElementById('chat-history');
            const d = document.createElement('div');
            d.className = `msg ${role}`;
            d.innerText = text;
            h.appendChild(d);
            h.scrollTop = h.scrollHeight;
        }

        function setupPhase(phase) {
            currentPhase = phase;
            stepIndex = 0;
            generatedCode = phase===1 ? "# Project: Initial Workflow Design\\nsystem_config:\\n" : "# Project: Revised Workflow (V2.0)\\nsystem_config:\\n";
            
            // 화면 초기화
            document.getElementById('code-display').innerHTML = "";
            typeCode(""); 
            document.getElementById('chat-history').innerHTML = "";
            
            // [BUG FIX] 입력창 활성화 (중요!)
            const inputEl = document.getElementById('prompt-input');
            inputEl.disabled = false;
            inputEl.value = "";
            
            switchScreen('ide-screen');
            appendMsg('ai', scenarios[phase].intro);
            askQuestion();
        }

        function startPhase1(btn) {
            if(btn) btn.innerText = "로딩 중...";
            setTimeout(() => setupPhase(1), 300);
        }
        function startPhase2() { setupPhase(2); }

        function askQuestion() {
            // 모든 질문 완료 시
            if(stepIndex >= scenarios[currentPhase].steps.length) {
                appendMsg('ai', "설계가 완료되었습니다. 배포하시겠습니까?");
                const h = document.getElementById('chat-history');
                const btn = document.createElement('button');
                btn.className = 'btn';
                btn.style.marginTop = '10px';
                btn.innerText = currentPhase===1 ? "🚀 V1.0 배포" : "🚀 V2.0 배포 및 비교";
                btn.onclick = () => switchScreen(currentPhase===1 ? 'intermission-screen' : 'report-screen');
                h.appendChild(btn);
                h.scrollTop = h.scrollHeight;
                
                // 완료되면 입력창 비활성화 및 칩 제거
                document.getElementById('suggestion-chips').innerHTML = "";
                document.getElementById('prompt-input').disabled = true;
                return;
            }

            // 다음 질문 제시
            const stepData = scenarios[currentPhase].steps[stepIndex];
            setTimeout(() => {
                appendMsg('ai', stepData.q);
                const chips = document.getElementById('suggestion-chips');
                chips.innerHTML = "";
                stepData.chips.forEach(c => {
                    const el = document.createElement('div');
                    el.className = 'chip';
                    el.innerText = c.label;
                    el.onclick = () => {
                        const inp = document.getElementById('prompt-input');
                        inp.value = c.prompt;
                        inp.dataset.code = c.code;
                        inp.focus();
                    };
                    chips.appendChild(el);
                });
            }, 500);
        }

        // 엔터키 이벤트 리스너
        const inputEl = document.getElementById('prompt-input');
        inputEl.addEventListener('keypress', function(e) {
            if(e.key === 'Enter' && this.value.trim() !== "") {
                const txt = this.value;
                const code = this.dataset.code;
                
                appendMsg('user', txt);
                this.value = "";
                this.dataset.code = "";
                document.getElementById('suggestion-chips').innerHTML = "";

                if(code) {
                    setTimeout(() => {
                        typeCode(code);
                        stepIndex++;
                        askQuestion();
                    }, 600);
                } else {
                    // 칩 선택 없이 입력했을 경우 (데모용 안내)
                    setTimeout(() => {
                         appendMsg('ai', "(시스템 알림) 정확한 코드 생성을 위해 상단의 가이드 칩을 선택해주세요.");
                         askQuestion();
                    }, 500);
                }
            }
        });
    </script>
</body>
</html>
"""

# 4. Streamlit Render
components.html(html_code, height=950, scrolling=False)

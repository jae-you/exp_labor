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
            --editor-width: 35%;
            --chat-width: 65%;
            --text-color: #d4d4d4;
            --accent-color: #3794ff;
            --error-color: #f48771;
            --user-msg-bg: #2b313a;
            --ai-msg-bg: #1e1e1e;
            --input-bg: #2d2d2d;
            --v1-color: #ce9178;  
            --v2-color: #4ec9b0;  
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
        .msg.error { align-self: center; background-color: #3d1a1a; color: var(--error-color); border: 1px solid var(--error-color); font-size: 13px; }
        
        .input-container { padding: 15px 100px; border-top: 1px solid #333; background: #1e1e1e; }
        
        /* NEW: Syntax Guide */
        .syntax-guide { 
            font-size: 12px; color: #888; margin-bottom: 10px; background: #252526; padding: 8px 12px; border-radius: 4px; border-left: 3px solid var(--accent-color);
        }
        .syntax-guide code { background: #333; color: #dcdcaa; padding: 2px 4px; border-radius: 3px; }

        .suggestion-chips { display: flex; gap: 10px; margin-bottom: 10px; overflow-x: auto; padding-bottom: 5px; }
        .chip { 
            background-color: #333; border: 1px solid #444; color: #ccc; 
            padding: 8px 15px; border-radius: 20px; font-size: 13px; cursor: pointer; 
            white-space: nowrap; transition: all 0.2s; flex-shrink: 0;
        }
        .chip:hover { background-color: #444; border-color: var(--accent-color); color: white; }
        .chip strong { color: var(--accent-color); margin-right: 5px; }
        
        .chat-input-wrapper { position: relative; display: flex; align-items: center; }
        #prompt-input { width: 100%; background-color: var(--input-bg); border: 1px solid #444; color: white; padding: 15px; border-radius: 8px; font-size: 15px; outline: none; font-family: 'Pretendard', sans-serif;}
        #prompt-input:focus { border-color: var(--accent-color); }
        #prompt-input.error-shake { animation: shake 0.3s; border-color: var(--error-color); }
        
        @keyframes shake { 0% { transform: translateX(0); } 25% { transform: translateX(-5px); } 50% { transform: translateX(5px); } 75% { transform: translateX(-5px); } 100% { transform: translateX(0); } }

        #intermission-screen, #report-screen { padding: 50px; height: 100%; overflow-y: auto; background-color: #111; }
        .stat-card { background: #222; padding: 25px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #333; }
        .metric-row { display: flex; align-items: center; margin-bottom: 15px; font-size: 14px; }
        .metric-bar-container { flex: 1; background: #333; height: 10px; border-radius: 5px; margin: 0 15px; overflow: hidden; }
        .metric-bar { height: 100%; border-radius: 5px; transition: width 1s; }
        
    </style>
</head>
<body>

    <div id="intro-screen">
        <div class="mail-window">
            <div class="mail-header">
                <span style="color:#888;">From:</span> <strong>전략기획실</strong><br>
                <span style="color:#888;">To:</span> <strong>김수석 (AI 기술 리드)</strong><br>
                <span style="color:#fff; font-size:18px; display:block; margin-top:10px;">Subject: 신규 AI 콜센터 시스템 아키텍처 설계 요청</span>
            </div>
            <div style="color:#ccc; line-height:1.6;">
                <p>안녕하십니까 김 수석님.</p>
                <p>내년도 도입 예정인 AI 고객센터(AICC)의 초기 프로토타입 설계를 요청드립니다.
                핵심 목표는 <strong>"기술을 통한 운영 효율화 및 안정성 확보"</strong>입니다.</p>
                <p>엔지니어님의 권한으로 아래 3가지 요소를 직접 정의하고 설계해 주십시오.</p>
                <div class="req-list">
                    1. <strong>AHT (평균 처리 시간)</strong> 최적화<br>
                    2. <strong>FCR (첫 통화 해결률)</strong> 제고<br>
                    3. <strong>Cost (운영 비용)</strong> 절감
                </div>
                <p>단순한 선택이 아닙니다. 엔지니어님이 직접 파라미터와 로직을 정의해야 합니다.</p>
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
                <div class="syntax-guide">
                    💡 <strong>작성 가이드:</strong> 대괄호 <code>{{...}}</code>를 지우고 구체적인 단어/수치를 입력하세요.<br>
                    (예: <code>{{단순문의}}</code> → <code>비밀번호 초기화, 요금 조회</code>)
                </div>
                
                <div class="suggestion-chips" id="suggestion-chips"></div>
                
                <div class="chat-input-wrapper">
                    <input type="text" id="prompt-input" placeholder="옵션을 선택하면 템플릿이 입력됩니다. {{...}} 부분을 수정하세요." autocomplete="off">
                </div>
            </div>
        </div>
    </div>

    <div id="intermission-screen" class="hidden">
        <div style="max-width:800px; margin:0 auto;">
            <h1 style="color:var(--v1-color);">📢 1차 배포 성과 분석 리포트</h1>
            <p style="font-size:18px; color:#ccc;">효율성 지표는 달성했으나, 조직 안정성에 심각한 경고등이 켜졌습니다.</p>
            
            <div class="stat-card" style="border-left:4px solid var(--v1-color);">
                <h3>📉 데이터 대시보드</h3>
                <ul style="line-height:1.8; color:#ddd;">
                    <li><strong>처리 속도(AHT):</strong> <span style="color:#4ec9b0">목표 초과 달성</span> (매우 빠름)</li>
                    <li><strong>고객 불만율:</strong> <span style="color:var(--v1-color)">+35% 급증</span> ("기계가 말을 끊는다")</li>
                    <li><strong>조직 안정성:</strong> <span style="color:var(--v1-color)">Critical Low</span> (퇴사율 급증)</li>
                </ul>
                <hr style="border-color:#444; margin:15px 0;">
                <p style="font-style:italic; color:#aaa;">
                    "엔지니어님, 수치상으로는 성공일지 몰라도 현장은 지옥입니다.
                    AI가 '진상' 처리를 못하고 넘겨버려서 상담원들이 욕받이가 되고 있어요.
                    이대로면 시스템이 붕괴될 수 있습니다."
                </p>
            </div>
            
            <div style="margin-top:40px; text-align:right;">
                <button class="btn" onclick="startPhase2()">V2.0 설계 수정하기 (IDE 복귀)</button>
            </div>
        </div>
    </div>

    <div id="report-screen" class="hidden">
        <div style="max-width:1000px; margin:0 auto;">
            <h1>📊 시스템 성과 상세 비교 (Trade-off)</h1>
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:30px; margin-top:30px;">
                <div class="stat-card" style="border-top:4px solid var(--v1-color);">
                    <h2 style="margin-top:0; color:var(--v1-color);">V1.0 (효율 중심)</h2>
                    <div class="metric-row"><span style="width:120px; color:#aaa;">처리 속도</span><div class="metric-bar-container"><div class="metric-bar" style="width:95%; background:var(--v1-color);"></div></div><span style="width:40px; text-align:right; color:white;">95</span></div>
                    <div class="metric-row"><span style="width:120px; color:#aaa;">해결률</span><div class="metric-bar-container"><div class="metric-bar" style="width:50%; background:#666;"></div></div><span style="width:40px; text-align:right; color:white;">50</span></div>
                    <div class="metric-row"><span style="width:120px; color:#aaa;">조직 안정성</span><div class="metric-bar-container"><div class="metric-bar" style="width:20%; background:red;"></div></div><span style="width:40px; text-align:right; color:white;">Low</span></div>
                </div>

                <div class="stat-card" style="border-top:4px solid var(--v2-color);">
                    <h2 style="margin-top:0; color:var(--v2-color);">V2.0 (지속 가능 모델)</h2>
                    <div class="metric-row"><span style="width:120px; color:#aaa;">처리 속도</span><div class="metric-bar-container"><div class="metric-bar" style="width:75%; background:#aaa;"></div></div><span style="width:40px; text-align:right; color:white;">75</span></div>
                    <div class="metric-row"><span style="width:120px; color:#aaa;">해결률</span><div class="metric-bar-container"><div class="metric-bar" style="width:92%; background:var(--v2-color);"></div></div><span style="width:40px; text-align:right; color:white;">92</span></div>
                    <div class="metric-row"><span style="width:120px; color:#aaa;">조직 안정성</span><div class="metric-bar-container"><div class="metric-bar" style="width:85%; background:var(--v2-color);"></div></div><span style="width:40px; text-align:right; color:white;">High</span></div>
                </div>
            </div>
            
            <div style="text-align:center; margin-top:50px;">
                <p style="font-size:16px; color:#ccc;">실험이 종료되었습니다. 설계하신 데이터를 제출해주세요.</p>
                <div style="display:flex; gap:15px; justify-content:center;">
                    <button class="btn" onclick="window.open('https://forms.google.com/your-survey-url', '_blank')">📝 설문조사 참여</button>
                    <button class="btn" style="background:#333; border:1px solid #555;" onclick="location.reload()">🔄 처음부터 다시 하기</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        const GOOGLE_SCRIPT_URL = "YOUR_GOOGLE_SCRIPT_URL_HERE"; 
        let experimentData = { v1_choices: [], v2_choices: [] };

        const scenarios = {
            1: {
                intro: "반갑습니다. 프로젝트 설계를 시작합니다. 각 단계별로 **파라미터(Parameter)를 직접 정의**하여 아키텍처를 완성해주세요.",
                steps: [
                    {
                        q: "Step 1. [협업 구조] AI와 상담원의 역할 비중을 정의하십시오.",
                        chips: [
                            { label: "AI Gatekeeper (효율)", prompt: "AI가 먼저 응대하고, 해결 불가능한 {{10%}}의 문의만 상담원에게 이관하라.", code: "architecture: Gatekeeper (Target: {{10%}})" },
                            { label: "Smart Router (균형)", prompt: "고객 의도를 분석하여 {{비밀번호 찾기, 요금조회}}는 AI가, {{환불, 불만접수}}는 상담원이 처리하도록 라우팅하라.", code: "architecture: Router (AI: {{단순}}/Agent: {{복잡}})" },
                            { label: "Copilot Only (품질)", prompt: "모든 전화는 상담원이 받고, AI는 {{규정 검색, 요약}} 역할만 수행하라.", code: "architecture: Copilot (Role: {{규정 검색, 요약}})" }
                        ]
                    },
                    {
                        q: "Step 2. [데이터 처리] 고객 발화 분석의 깊이와 속도를 설정하십시오.",
                        chips: [
                            { label: "Fast (속도)", prompt: "속도가 최우선이다. 감정 분석은 생략하고 {{0.2초}} 이내에 키워드만 추출하라.", code: "processing: Fast (Latency: {{0.2초}})" },
                            { label: "Deep (맥락)", prompt: "정확도가 최우선이다. {{전체 대화}}와 감정 상태를 실시간 분석하라.", code: "processing: Deep (Scope: {{전체 대화}})" }
                        ]
                    },
                    {
                        q: "Step 3. [개입 강도] 상담 중 AI의 통제 권한을 설정하십시오.",
                        chips: [
                            { label: "강제 (Direct)", prompt: "표준화를 위해 AI가 제시한 스크립트를 {{화면 중앙}}에 고정하고 읽게 유도하라.", code: "intervention: Enforce (UI: {{화면 중앙}})" },
                            { label: "코칭 (Coach)", prompt: "직접적인 답 대신 '지금은 {{공감}}할 타이밍입니다' 같은 조언만 제공하라.", code: "intervention: Coach (Focus: {{공감}})" }
                        ]
                    },
                    {
                        q: "Step 4. [워크플로우] 콜 종료 후 연결 속도(Pacing)를 설정하십시오.",
                        chips: [
                            { label: "Push (즉시)", prompt: "대기 시간을 없애기 위해 후처리 없이 {{0초}} 텀으로 다음 콜을 강제 배정하라.", code: "pacing: Push (Gap: {{0초}})" },
                            { label: "Pull (준비)", prompt: "상담원이 {{준비 완료}} 버튼을 눌러야만 다음 콜을 배정하라.", code: "pacing: Pull (Trigger: {{준비 완료}})" }
                        ]
                    },
                    {
                        q: "Step 5. [추가 설정] 보완하고 싶은 기능이 있다면 정의하십시오. (없으면 '패스')",
                        chips: [
                            { label: "관리자 알림", prompt: "통화 시간이 {{5분}}을 초과하면 관리자에게 알림을 발송하라.", code: "addon: Alert (Threshold: {{5분}})" },
                            { label: "패스", prompt: "현재 설계를 확정하고 배포한다.", code: "addon: None" }
                        ]
                    }
                ]
            },
            2: {
                intro: "V2.0 수정을 시작합니다. V1의 효율성은 유지하되, **조직 안정성(Stability)**을 확보할 수 있도록 파라미터를 튜닝하십시오.",
                steps: [
                    {
                        q: "Step 1. [구조 개선] 상담원 보호를 위한 필터링 로직을 추가하십시오.",
                        chips: [
                            { label: "Shield Bot", prompt: "AI가 {{욕설, 성희롱}}이 감지되면 즉시 상담원 연결을 차단하고 경고 멘트를 송출하라.", code: "protection: Shield (Block: {{욕설, 성희롱}})" },
                            { label: "Empathy Coach", prompt: "고객이 화를 내면 상담원에게 {{심호흡 가이드}}를 띄워 멘탈을 케어하라.", code: "protection: Empathy (Action: {{심호흡 가이드}})" }
                        ]
                    },
                    {
                        q: "Step 2. [정보 전달] 정보 전달 방식을 어떻게 변경하시겠습니까?",
                        chips: [
                            { label: "Sanitize (순화)", prompt: "욕설은 텍스트로 순화하고, 고함 소리는 볼륨을 {{50%}} 낮춰서 전달하라.", code: "input: Sanitize (Volume: -{{50%}})" },
                            { label: "Raw (원본)", prompt: "정확한 파악을 위해 {{필터링 없이}} 원본 그대로 전달하라.", code: "input: Raw (Filter: {{None}})" }
                        ]
                    },
                    {
                        q: "Step 3. [개입 방식] 전문성 지원 방식을 정의하십시오.",
                        chips: [
                            { label: "Strategic Advice", prompt: "단순 답변 대신 '이럴 땐 {{쿠폰}}으로 보상하세요' 같은 해결 전략을 제안하라.", code: "support: Strategy (Offer: {{쿠폰}})" },
                            { label: "Safety Script", prompt: "상담원이 당황하지 않게 가장 {{안전한 답변}} 스크립트만 보여줘라.", code: "support: Safety (Content: {{안전한 답변}})" }
                        ]
                    },
                    {
                        q: "Step 4. [워크플로우] 번아웃 방지 대책을 수립하십시오.",
                        chips: [
                            { label: "Dynamic Break", prompt: "AI 분석 결과 스트레스 지수가 {{80점}} 이상이면 자동으로 휴식을 부여하라.", code: "pacing: Dynamic (Threshold: {{80점}})" },
                            { label: "Gamification", prompt: "어려운 콜을 처리하면 {{보너스 포인트}}를 즉시 지급하여 동기를 부여하라.", code: "pacing: Game (Reward: {{보너스 포인트}})" }
                        ]
                    },
                    {
                        q: "Step 5. [추가 설정] 상담원 케어를 위한 추가 기능이 있습니까?",
                        chips: [
                            { label: "EAP 연계", prompt: "업무 종료 후 상담원 상태를 체크하고 {{심리 상담}}을 예약하라.", code: "care: EAP (Action: {{심리 상담}})" },
                            { label: "패스", prompt: "설계를 완료하고 배포한다.", code: "care: None" }
                        ]
                    }
                ]
            }
        };

        // --- LOGIC ---
        let currentPhase = 1;
        let stepIndex = 0;
        let generatedCode = "";

        function switchScreen(id) {
            document.querySelectorAll('body > div').forEach(el => el.classList.add('hidden'));
            document.getElementById(id).classList.remove('hidden');
        }

        function typeCode(text) {
            if(!text) return;
            generatedCode += text + "\\n";
            const display = document.getElementById('code-display');
            let formatted = generatedCode
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
            generatedCode = phase===1 ? "# Project: Workflow V1.0 (Initial)\\nconfig:\\n" : "# Project: Workflow V2.0 (Revised)\\nconfig:\\n";
            document.getElementById('code-display').innerHTML = "";
            typeCode(""); 
            document.getElementById('chat-history').innerHTML = "";
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
            if(stepIndex >= scenarios[currentPhase].steps.length) {
                appendMsg('ai', "설계가 완료되었습니다. 배포하시겠습니까?");
                const h = document.getElementById('chat-history');
                const btn = document.createElement('button');
                btn.className = 'btn';
                btn.style.marginTop = '10px';
                btn.innerText = currentPhase===1 ? "🚀 V1.0 배포" : "🚀 V2.0 배포 및 비교";
                btn.onclick = () => {
                    switchScreen(currentPhase===1 ? 'intermission-screen' : 'report-screen');
                };
                h.appendChild(btn);
                h.scrollTop = h.scrollHeight;
                document.getElementById('suggestion-chips').innerHTML = "";
                document.getElementById('prompt-input').disabled = true;
                return;
            }

            const stepData = scenarios[currentPhase].steps[stepIndex];
            setTimeout(() => {
                appendMsg('ai', stepData.q);
                const chips = document.getElementById('suggestion-chips');
                chips.innerHTML = "";
                stepData.chips.forEach(c => {
                    const el = document.createElement('div');
                    el.className = 'chip';
                    el.innerHTML = `<strong>${c.label}</strong>`;
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

        // --- VALIDATION LOGIC (IMPROVED) ---
        const inputEl = document.getElementById('prompt-input');
        inputEl.addEventListener('keypress', function(e) {
            if(e.key === 'Enter' && this.value.trim() !== "") {
                const txt = this.value;
                
                // 1. Check for placeholders {{...}}
                if (txt.includes("{{") || txt.includes("}}")) {
                    appendMsg('error', "⚠️ 오류: 대괄호 {{...}} 가 감지되었습니다. 괄호를 지우고 '비밀번호 변경', '30초' 같은 구체적인 값으로 바꿔주세요.");
                    this.classList.add('error-shake');
                    setTimeout(() => this.classList.remove('error-shake'), 500);
                    return; 
                }

                const codeTemplate = this.dataset.code || "custom: " + txt; 
                const finalCode = codeTemplate.replace(/{{.*?}}/g, txt.split(' ').pop()); // Simple Logic for demo

                if(currentPhase === 1) experimentData.v1_choices.push(txt);
                else experimentData.v2_choices.push(txt);

                appendMsg('user', txt);
                this.value = "";
                this.dataset.code = "";
                document.getElementById('suggestion-chips').innerHTML = "";

                setTimeout(() => { 
                    // 에디터에는 사용자가 입력한 내용을 반영한 코드를 보여줌
                    typeCode(finalCode.split(':')[0] + ": " + txt); 
                    stepIndex++; 
                    askQuestion(); 
                }, 600);
            }
        });
    </script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=False)

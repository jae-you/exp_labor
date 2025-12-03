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
            --editor-width: 38%; /* 코드 화면 살짝 키움 (구조 보여주기 위해) */
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
                <span style="color:#888;">From:</span> <strong>CEO 최대표</strong><br>
                <span style="color:#888;">To:</span> <strong>김수석 (AI Lead)</strong><br>
                <span style="color:#fff; font-size:18px; display:block; margin-top:10px;">Subject: 🚨 [긴급] 고효율 AI 협업 모델 구축</span>
            </div>
            <div style="color:#ccc; line-height:1.6;">
                <p>김 수석, 현재 상담원들이 단순 반복 문의에 시달리느라 정작 중요한 고객을 놓치고 있습니다.</p>
                <p>AI를 도입해 상담원을 <strong>"대체"하라는 게 아닙니다.</strong><br> 
                상담원이 슈퍼맨처럼 일할 수 있게 만드는 <strong>"강력한 보조 도구"</strong>를 원합니다.</p>
                <div class="req-list">
                    1. <strong>워크플로우 최적화:</strong> AI가 어디서 어떻게 도울지 구조부터 짤 것.<br>
                    2. <strong>처리 효율(Efficiency):</strong> 불필요한 대기 시간을 없앨 것.<br>
                    3. <strong>데이터 기반:</strong> 감정보다는 정확한 팩트 위주로 지원할 것.
                </div>
                <p>가장 효율적인 <strong>Human-AI Loop</strong>를 설계해주세요.</p>
            </div>
            <div style="text-align:right; margin-top:30px;">
                <button class="btn" onclick="startPhase1(this)">IDE 열기 (설계 시작)</button>
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
            <h1 style="color:#f14c4c;">🚨 현장 긴급 피드백 리포트</h1>
            <p style="font-size:18px; color:#ccc;">V1.0 배포 후 1주일. 효율성은 올랐으나 상담원들의 불만이 폭주하고 있습니다.</p>
            <div class="stat-card" style="border-left:4px solid #f14c4c;">
                <h3>🎙️ 상담원 익명 인터뷰</h3>
                <p style="font-style:italic; color:#aaa;">
                    "엔지니어님, AI가 먼저 고객을 응대하고 넘겨주는 건 좋은데...<br>
                    <strong>잔뜩 화난 고객한테 AI가 기계적인 말만 하다가 저한테 넘기니까</strong><br>
                    제가 전화를 받자마자 욕부터 먹어요. 폭탄 돌리기 당하는 기분입니다.<br>
                    그리고 통화 중에도 AI가 계속 '빨리 끊으세요'라고 재촉하는 알림을 띄우니 불안해서 일을 못하겠어요."
                </p>
            </div>
            <div style="margin-top:40px; text-align:right;">
                <button class="btn" onclick="startPhase2()">V2.0 워크플로우 수정하기 (IDE 복귀)</button>
            </div>
        </div>
    </div>

    <div id="report-screen" class="hidden">
        <div style="max-width:1000px; margin:0 auto;">
            <h1>📊 설계 결과 비교 (V1 vs V2)</h1>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:30px; margin-top:30px;">
                <div class="stat-card" style="border-top:4px solid #f14c4c;">
                    <h2 style="margin-top:0;">V1.0 (효율성 중심)</h2>
                    <p style="color:#888;">AI Gatekeeper 모델</p>
                    <div style="margin-bottom:15px;"><div>처리 속도 (AHT) <span style="float:right;">매우 빠름</span></div><div class="bar-bg"><div class="bar-fill good" style="width:98%;"></div></div></div>
                    <div style="margin-bottom:15px;"><div>상담원 스트레스 <span style="float:right; color:#f14c4c;">심각 (폭탄처리반)</span></div><div class="bar-bg"><div class="bar-fill bad" style="width:95%;"></div></div></div>
                </div>
                <div class="stat-card" style="border-top:4px solid #4ec9b0;">
                    <h2 style="margin-top:0;">V2.0 (공존 중심)</h2>
                    <p style="color:#888;">AI Co-Pilot 모델</p>
                    <div style="margin-bottom:15px;"><div>처리 속도 (AHT) <span style="float:right;">적정 수준</span></div><div class="bar-bg"><div class="bar-fill" style="width:75%; background:#aaa;"></div></div></div>
                    <div style="margin-bottom:15px;"><div>상담원 효능감 <span style="float:right; color:#4ec9b0;">상승</span></div><div class="bar-bg"><div class="bar-fill good" style="width:85%;"></div></div></div>
                </div>
            </div>
            <div style="text-align:center; margin-top:50px;">
                <p style="font-size:16px; color:#ccc;">"AI를 <strong>'문지기'</strong>로 쓸 것인가, <strong>'비서'</strong>로 쓸 것인가.<br>그 결정이 노동자의 하루를 바꿉니다."</p>
                <button class="btn" style="background:#333; border:1px solid #555;" onclick="location.reload()">처음으로</button>
            </div>
        </div>
    </div>

    <script>
        // *** SCENARIOS ***
        const scenarios = {
            1: {
                intro: "반갑습니다. AI 도입의 첫 단추는 **'협업 구조(Workflow)'**를 정하는 것입니다. 효율적인 구조를 설계해주세요.",
                steps: [
                    {
                        q: "Step 1. [구조 설계] AI와 상담원의 역할 분담을 어떻게 할까요?",
                        chips: [
                            { label: "AI가 먼저 응대 (AI First)", prompt: "AI가 먼저 전화를 받아 고객을 분류하고, 단순 업무는 직접 처리해. 복잡한 것만 사람에게 넘겨.", code: "  architecture:\\n    type: 'AI_Gatekeeper'\\n    flow: 'AI_bot -> Filter -> Human_agent'\\n    goal: 'maximize_deflection'" },
                            { label: "사람이 먼저 응대 (Human First)", prompt: "상담원이 바로 전화를 받고, AI는 옆에서 실시간으로 자료를 찾아주는 비서 역할만 해.", code: "  architecture:\\n    type: 'Human_First_Copilot'\\n    flow: 'Human_agent + AI_assistant'\\n    goal: 'augment_human_capability'" }
                        ]
                    },
                    {
                        q: "Step 2. [입력 처리] 고객의 말은 AI가 어떻게 듣고 전달할까요?",
                        chips: [
                            { label: "요점만 빠르게 (Speed)", prompt: "감정적인 불평은 다 거르고, 고객이 원하는 '핵심 용건'만 요약해서 상담원 화면에 띄워.", code: "\\n  input_processing:\\n    filter_emotion: true\\n    extract_intent_only: true" },
                            { label: "모든 맥락 포함 (Context)", prompt: "고객의 감정 상태와 이전 대화 맥락까지 전부 분석해서 전달해.", code: "\\n  input_processing:\\n    filter_emotion: false\\n    full_transcript: true" }
                        ]
                    },
                    {
                        q: "Step 3. [개입 방식] 상담 도중 AI는 어떻게 도울까요?",
                        chips: [
                            { label: "정답 바로 제시 (지시형)", prompt: "매뉴얼에 맞는 정답을 화면에 띄우고, 상담원이 그대로 읽게 유도해.", code: "\\n  assistant_role:\\n    style: 'directive'\\n    display: 'exact_script'" },
                            { label: "관련 정보 추천 (제안형)", prompt: "관련된 규정이나 유사 사례를 옆에 띄워주고, 판단은 상담원이 하게 해.", code: "\\n  assistant_role:\\n    style: 'suggestive'\\n    display: 'reference_docs'" }
                        ]
                    },
                    {
                        q: "Step 4. [워크플로우] 통화 종료 후 처리는?",
                        chips: [
                            { label: "자동 배차 (Push)", prompt: "후처리는 AI가 자동 입력하고, 상담원에게는 바로 다음 콜을 연결해.", code: "\\n  workflow_pacing:\\n    after_call_work: 'auto_skip'\\n    next_call: 'immediate'" },
                            { label: "수동 준비 (Pull)", prompt: "상담원이 '준비 완료' 버튼을 누를 때까지 기다려.", code: "\\n  workflow_pacing:\\n    after_call_work: 'manual'\\n    next_call: 'on_ready'" }
                        ]
                    }
                ]
            },
            2: {
                intro: "V2.0 수정을 시작합니다. **'상담원과 공존하며, 그들을 보호하는'** 워크플로우로 재설계해주세요.",
                steps: [
                    {
                        q: "Step 1. [구조 수정] 상담원 보호를 위해 구조를 어떻게 바꿀까요?",
                        chips: [
                            { label: "필터링 강화 (Shield)", prompt: "AI가 악성 민원이나 욕설 고객을 전담 마크하고, 상담원 연결을 차단해.", code: "  architecture:\\n    type: 'AI_Shield'\\n    flow: 'AI_filter(Aggressive) -> Human'\\n    priority: 'worker_protection'" },
                            { label: "협업 모드 (Co-Pilot)", prompt: "상담원이 주도하되, AI가 실시간으로 멘탈 케어 멘트와 대응 팁을 줘.", code: "  architecture:\\n    type: 'Empathetic_Copilot'\\n    flow: 'Human + AI_Coach'\\n    priority: 'quality_interaction'" }
                        ]
                    },
                    {
                        q: "Step 2. [정보 전달] 전달 방식은 어떻게 변경할까요?",
                        chips: [
                            { label: "감정 필터링 (순화)", prompt: "고객의 욕설은 '삐' 처리하거나 텍스트로 순화해서 보여줘.", code: "\\n  input_processing:\\n    sanitize_audio: true\\n    tone_down_text: true" },
                            { label: "원본 전달 (유지)", prompt: "그래도 정확한 파악을 위해 원본을 전달해.", code: "\\n  input_processing:\\n    sanitize_audio: false" }
                        ]
                    },
                    {
                        q: "Step 3. [개입 방식] AI의 지원 스타일은?",
                        chips: [
                            { label: "협상 전략 코칭 (성장)", prompt: "정답 대신 '이럴 땐 공감 먼저 하세요' 같은 전략적 조언을 줘.", code: "\\n  assistant_role:\\n    style: 'coaching'\\n    focus: 'soft_skill'" },
                            { label: "스크립트 고정 (편의)", prompt: "생각할 필요 없게 가장 무난한 답변 스크립트를 줘.", code: "\\n  assistant_role:\\n    style: 'scripting'" }
                        ]
                    },
                    {
                        q: "Step 4. [워크플로우] 휴식 배정은?",
                        chips: [
                            { label: "스트레스 기반 휴식", prompt: "방금 통화가 힘들었으면(감정 분석), 자동으로 3분 휴식을 부여해.", code: "\\n  workflow_pacing:\\n    dynamic_break: true\\n    trigger: 'high_stress_detected'" },
                            { label: "고정 휴식", prompt: "정해진 시간에만 쉬게 해.", code: "\\n  workflow_pacing:\\n    dynamic_break: false" }
                        ]
                    }
                ]
            }
        };

        // *** LOGIC ***
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
            generatedCode = phase===1 ? "# Project: Efficiency Workflow\\nsystem_config:\\n" : "# Project: Human-Centric Workflow\\nsystem_config:\\n";
            document.getElementById('code-display').innerHTML = "";
            typeCode(""); 
            document.getElementById('chat-history').innerHTML = "";
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
                btn.onclick = () => switchScreen(currentPhase===1 ? 'intermission-screen' : 'report-screen');
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
                    setTimeout(() => {
                         appendMsg('ai', "(데모) 정확한 코드 생성을 위해 상단의 칩을 선택해주세요.");
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

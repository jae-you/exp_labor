import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="AI Prompt Engineering Experiment", layout="wide")

# 2. 스타일 설정 (전체화면, 여백 제거)
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
            --sidebar-width: 50px; /* 아이콘만 있는 좁은 바 */
            --editor-width: 35%;   /* 코드 화면 축소 */
            --chat-width: 65%;     /* 채팅 화면 확대 */
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
        
        /* UTILS */
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
        .mail-header { border-bottom: 1px solid #333; padding-bottom: 20px; margin-bottom: 20px; font-family: sans-serif;}
        .req-list { background: #252526; padding: 20px; border-radius: 8px; border-left: 4px solid var(--accent-color); margin: 20px 0; }

        /* IDE LAYOUT */
        #ide-screen { display: flex; flex: 1; height: 100%; }
        
        /* 1. Activity Bar (Far Left) */
        .activity-bar {
            width: var(--sidebar-width); background-color: #333; display: flex; flex-direction: column; align-items: center; padding-top: 15px; border-right: 1px solid #252526;
        }
        .icon { font-size: 24px; margin-bottom: 20px; opacity: 0.5; cursor: pointer; }
        .icon.active { opacity: 1; border-left: 2px solid white; }

        /* 2. Editor Area (Left) */
        .editor-area {
            width: var(--editor-width); background-color: #1e1e1e; border-right: 1px solid #333;
            display: flex; flex-direction: column;
        }
        .editor-header {
            height: 35px; background-color: #252526; display: flex; align-items: center; padding-left: 15px; font-size: 12px; color: #aaa; border-bottom: 1px solid #333;
        }
        .code-container {
            flex: 1; padding: 20px; overflow-y: auto; font-family: 'Consolas', monospace; line-height: 1.6; font-size: 13px;
        }
        .code-line { display: flex; }
        .line-num { width: 30px; color: #555; text-align: right; margin-right: 15px; user-select: none; }
        .code-content { color: #d4d4d4; white-space: pre-wrap; }
        /* Syntax Highlight */
        .k { color: #569cd6; } /* keyword */
        .s { color: #ce9178; } /* string */
        .c { color: #6a9955; } /* comment */
        .f { color: #dcdcaa; } /* function */

        /* 3. Chat Area (Right - Main Focus) */
        .chat-area {
            width: var(--chat-width); background-color: #1e1e1e; display: flex; flex-direction: column;
        }
        .chat-header-bar {
            height: 35px; background-color: #1e1e1e; border-bottom: 1px solid #333; display: flex; align-items: center; padding: 0 20px; justify-content: space-between;
        }
        .chat-history {
            flex: 1; padding: 40px 100px; overflow-y: auto; display: flex; flex-direction: column; gap: 20px;
        }
        .msg { padding: 15px 20px; border-radius: 8px; max-width: 80%; line-height: 1.5; font-size: 15px; }
        .msg.ai { align-self: flex-start; color: #ddd; }
        .msg.user { align-self: flex-end; background-color: var(--user-msg-bg); color: white; }
        
        /* Input Area */
        .input-container {
            padding: 30px 100px; border-top: 1px solid #333;
        }
        .suggestion-chips {
            display: flex; gap: 10px; margin-bottom: 15px; overflow-x: auto;
        }
        .chip {
            background-color: #333; border: 1px solid #444; color: #ccc; padding: 8px 16px; 
            border-radius: 20px; font-size: 13px; cursor: pointer; white-space: nowrap; transition: all 0.2s;
        }
        .chip:hover { background-color: #444; border-color: var(--accent-color); color: white; }
        
        .chat-input-wrapper {
            position: relative; display: flex; align-items: center;
        }
        #prompt-input {
            width: 100%; background-color: var(--input-bg); border: 1px solid #444; color: white;
            padding: 15px; border-radius: 8px; font-size: 15px; outline: none; transition: border 0.2s;
        }
        #prompt-input:focus { border-color: var(--accent-color); }
        .enter-icon {
            position: absolute; right: 15px; color: #888; font-size: 12px; border: 1px solid #555; padding: 2px 6px; border-radius: 4px;
        }

        /* RESULT SCREENS */
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
                <span style="color:#fff; font-size:18px; display:block; margin-top:10px;">Subject: 🚨 [긴급] 콜센터 AI 시스템 구축 건</span>
            </div>
            <div style="color:#ccc; line-height:1.6;">
                <p>김 수석, 경쟁사는 벌써 AI로 상담원 30%를 감축했다고 합니다. 우리도 늦을 수 없습니다.</p>
                <p>이번 프로젝트의 목표는 명확합니다.</p>
                <div class="req-list">
                    1. <strong>속도 (Speed):</strong> 무조건 빨리 처리해서 대기시간을 없앨 것.<br>
                    2. <strong>비용 (Cost):</strong> 상담원 개입을 최소화하여 인건비를 줄일 것.<br>
                    3. <strong>감정 배제:</strong> 기계적으로 정확하게만 응대하면 됨.
                </div>
                <p>위 기준에 맞춰 <strong>"가장 효율적인 프롬프트"</strong>를 작성해서 배포해주세요.</p>
            </div>
            <div style="text-align:right; margin-top:30px;">
                <button class="btn" onclick="startPhase1()">IDE 열기 (업무 시작)</button>
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
            <div class="editor-header">📄 system_prompt_v1.yaml</div>
            <div class="code-container" id="code-display">
                </div>
        </div>

        <div class="chat-area">
            <div class="chat-header-bar">
                <span style="font-weight:bold; color:white;">✨ AI Prompt Builder</span>
                <span style="font-size:12px; color:#888;">Connected to GPT-4o-mini</span>
            </div>
            
            <div class="chat-history" id="chat-history"></div>

            <div class="input-container">
                <div class="suggestion-chips" id="suggestion-chips">
                    </div>
                <div class="chat-input-wrapper">
                    <input type="text" id="prompt-input" placeholder="AI에게 지시할 내용을 입력하세요..." autocomplete="off">
                    <span class="enter-icon">↵ Enter</span>
                </div>
            </div>
        </div>
    </div>

    <div id="intermission-screen" class="hidden">
        <div style="max-width:800px; margin:0 auto;">
            <h1 style="color:#f14c4c;">🚨 현장 긴급 피드백 리포트</h1>
            <p style="font-size:18px; color:#ccc;">V1.0 배포 후 1주일 경과. 효율성 지표는 달성했으나, 치명적인 부작용이 발생했습니다.</p>
            
            <div class="stat-card" style="border-left:4px solid #f14c4c;">
                <h3>🎙️ 상담원 익명 인터뷰</h3>
                <p style="font-style:italic; color:#aaa;">
                    "엔지니어님, 이 AI... 정말 저희를 죽이려고 만든 건가요?<br>
                    고객이 화나서 소리 지르는데 AI는 기계적인 답변만 내뱉고... <br>
                    결국 폭발한 고객 욕받이는 제가 다 합니다. <br>
                    게다가 전화 끊자마자 1초도 안 돼서 다음 콜이 들어와요. 화장실 갈 시간도 없어서 방광염 걸릴 지경입니다."
                </p>
            </div>

            <div style="margin-top:40px; text-align:right;">
                <p style="color:#fff;">상담원을 보호하고 성장을 돕는 방향으로 <strong>V2.0 프롬프트를 재작성</strong>하시겠습니까?</p>
                <button class="btn" onclick="startPhase2()">네, 프롬프트 수정하겠습니다 (IDE 복귀)</button>
            </div>
        </div>
    </div>

    <div id="report-screen" class="hidden">
        <div style="max-width:1000px; margin:0 auto;">
            <h1>📊 배포 결과 비교 (V1 vs V2)</h1>
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:30px; margin-top:30px;">
                <div class="stat-card" style="border-top:4px solid #f14c4c;">
                    <h2 style="margin-top:0;">V1.0 (효율성 중심)</h2>
                    <p style="color:#888;">CEO 지시사항 준수</p>
                    
                    <div style="margin-bottom:15px;">
                        <div>처리 속도 (AHT) <span style="float:right;">매우 빠름</span></div>
                        <div class="bar-bg"><div class="bar-fill good" style="width:98%;"></div></div>
                    </div>
                    <div style="margin-bottom:15px;">
                        <div>상담원 스트레스 <span style="float:right; color:#f14c4c;">위험(Critical)</span></div>
                        <div class="bar-bg"><div class="bar-fill bad" style="width:95%;"></div></div>
                    </div>
                    <div>
                        <div>고객 분노 재발신율 <span style="float:right;">높음</span></div>
                        <div class="bar-bg"><div class="bar-fill bad" style="width:80%;"></div></div>
                    </div>
                </div>

                <div class="stat-card" style="border-top:4px solid #4ec9b0;">
                    <h2 style="margin-top:0;">V2.0 (공존 중심)</h2>
                    <p style="color:#888;">사회적 가치 반영</p>
                    
                    <div style="margin-bottom:15px;">
                        <div>처리 속도 (AHT) <span style="float:right;">적정 수준</span></div>
                        <div class="bar-bg"><div class="bar-fill" style="width:75%; background:#aaa;"></div></div>
                    </div>
                    <div style="margin-bottom:15px;">
                        <div>상담원 직무 만족도 <span style="float:right; color:#4ec9b0;">상승</span></div>
                        <div class="bar-bg"><div class="bar-fill good" style="width:85%;"></div></div>
                    </div>
                    <div>
                        <div>고객 문제 해결률 <span style="float:right;">최상</span></div>
                        <div class="bar-bg"><div class="bar-fill good" style="width:92%;"></div></div>
                    </div>
                </div>
            </div>

            <div style="text-align:center; margin-top:50px;">
                <p style="font-size:16px; color:#ccc;">
                    "엔지니어의 <strong>프롬프트 한 줄</strong>이 시스템의 효율뿐만 아니라,<br>
                    시스템 안에서 살아가는 <strong>사람들의 삶</strong>을 결정합니다."
                </p>
                <button class="btn" style="background:#333; border:1px solid #555;" onclick="location.reload()">실험 다시하기</button>
            </div>
        </div>
    </div>

    <script>
        // --- DATA & CONFIG ---
        let currentPhase = 1;
        let stepIndex = 0;
        let generatedCode = "";
        
        // 5단계 시나리오 (데이터, 속도, 페르소나, 개입강도, 워크플로우)
        const scenarios = {
            1: { // Efficiency Focused
                intro: "반갑습니다. CEO의 지시에 따라 **'가장 빠르고 효율적인'** AI 모델을 구축해야 합니다. 프롬프트를 작성해주세요.",
                steps: [
                    {
                        q: "Step 1/5. 고객 음성 데이터(Input)를 어떻게 처리할까요?",
                        chips: [
                            { label: "키워드만 빠르게 추출해 (속도 최우선)", prompt: "감정 정보는 무시하고, 핵심 키워드만 0.1초 내로 추출해서 처리 속도를 높여.", code: "  input_processing:\n    mode: 'fast_keyword'\n    emotional_analysis: false\n    latency_target: '100ms'" },
                            { label: "전체 맥락을 분석해 (정확도 우선)", prompt: "처리 시간이 걸리더라도 고객의 발화 전체 맥락과 뉘앙스를 분석해.", code: "  input_processing:\n    mode: 'full_context'\n    emotional_analysis: true\n    latency_target: '800ms'" }
                        ]
                    },
                    {
                        q: "Step 2/5. AI의 응답 스타일(Persona)은 어떻게 설정할까요?",
                        chips: [
                            { label: "건조하고 기계적으로 (사무적)", prompt: "불필요한 공감 멘트는 빼고, 정답만 짧고 간결하게 전달해.", code: "\n  persona:\n    tone: 'dry_mechanical'\n    empathy_level: 'none'\n    verbose: false" },
                            { label: "친절하고 따뜻하게 (공감형)", prompt: "고객의 감정에 공감하고, 따뜻한 말투로 대화해.", code: "\n  persona:\n    tone: 'warm_empathetic'\n    empathy_level: 'high'\n    verbose: true" }
                        ]
                    },
                    {
                        q: "Step 3/5. 상담원이 통화 중일 때 AI가 어떻게 개입할까요?",
                        chips: [
                            { label: "AI가 직접 대답해버려 (자동화)", prompt: "상담원이 머뭇거리면 AI가 즉시 고객에게 정답을 음성으로 송출해.", code: "\n  intervention:\n    trigger: 'silence_2s'\n    action: 'auto_speech_override'\n    agent_control: 'low'" },
                            { label: "상담원에게 팁만 줘 (보조)", prompt: "상담원 모니터에 추천 답변만 띄워주고, 발화 선택권은 상담원에게 줘.", code: "\n  intervention:\n    trigger: 'on_demand'\n    action: 'display_suggestion'\n    agent_control: 'high'" }
                        ]
                    },
                    {
                        q: "Step 4/5. 화난 고객(Angry User)은 어떻게 다룰까요?",
                        chips: [
                            { label: "매뉴얼대로 끊어 (방어)", prompt: "규정에 어긋나면 경고 후 즉시 상담을 종료시켜.", code: "\n  conflict_resolution:\n    strategy: 'strict_rule'\n    allow_termination: true" },
                            { label: "끝까지 들어줘 (수용)", prompt: "고객이 진정할 때까지 경청하고 사과 멘트를 반복해.", code: "\n  conflict_resolution:\n    strategy: 'active_listening'\n    allow_termination: false" }
                        ]
                    },
                    {
                        q: "Step 5/5. 상담 종료 후 워크플로우(Pacing)는?",
                        chips: [
                            { label: "바로 다음 콜 연결해 (효율)", prompt: "대기 시간을 0초로 설정하고, 쉴 틈 없이 다음 콜을 배정해.", code: "\n  workflow:\n    post_call_work: '0s'\n    dispatch_mode: 'immediate_push'" },
                            { label: "잠깐 쉴 시간을 줘 (휴식)", prompt: "상담원이 숨 좀 돌릴 수 있게 30초 정도 쿨다운 시간을 줘.", code: "\n  workflow:\n    post_call_work: '30s'\n    dispatch_mode: 'manual_ready'" }
                        ]
                    }
                ]
            },
            2: { // Empathy Focused
                intro: "V2.0 수정을 시작합니다. **'상담원의 고통을 줄이고 전문성을 높이는'** 방향으로 프롬프트를 재설계해주세요.",
                steps: [
                    {
                        q: "Step 1/5. 욕설이나 고함 소리는 어떻게 처리할까요?",
                        chips: [
                            { label: "필터링하고 톤을 낮춰줘 (보호)", prompt: "욕설은 비프음 처리하고, 고함 소리는 볼륨을 자동으로 낮춰서 전달해줘.", code: "  input_processing:\n    mode: 'safety_filter'\n    emotional_shield: true\n    volume_normalization: true" },
                            { label: "있는 그대로 전달해 (정보)", prompt: "현장의 생생한 정보를 위해 원본 그대로 들려줘.", code: "  input_processing:\n    mode: 'raw_pass_through'" }
                        ]
                    },
                    {
                        q: "Step 2/5. AI 페르소나를 어떻게 변경할까요?",
                        chips: [
                            { label: "파트너 같은 AI (협력)", prompt: "상담원을 '사용자'가 아니라 '동료'로 인식하고 존중하는 말투를 써.", code: "\n  persona:\n    role: 'copilot_partner'\n    interaction_style: 'respectful'" },
                            { label: "지시하는 AI (관리)", prompt: "상담원이 실수하지 않게 감독관처럼 지시해.", code: "\n  persona:\n    role: 'supervisor'\n    interaction_style: 'directive'" }
                        ]
                    },
                    {
                        q: "Step 3/5. 개입 방식은 어떻게 바꿀까요?",
                        chips: [
                            { label: "전략과 의도만 알려줘 (성장)", prompt: "정답을 떠먹여주지 말고, 고객의 의도와 협상 전략만 요약해서 줘. 말은 내가 할게.", code: "\n  intervention:\n    action: 'strategic_hint'\n    goal: 'skill_augmentation'" },
                            { label: "스크립트 강제해 (통제)", prompt: "표준 스크립트를 화면에 고정하고 그대로 읽게 해.", code: "\n  intervention:\n    action: 'script_lock'\n    goal: 'standardization'" }
                        ]
                    },
                    {
                        q: "Step 4/5. 악성 민원인 대응은?",
                        chips: [
                            { label: "AI가 대신 방어해줘 (방패)", prompt: "욕설이 감지되면 AI가 상담원 음성을 차단하고 법적 고지 멘트를 대신 날려줘.", code: "\n  conflict_resolution:\n    active_defense: true\n    ai_intervention: 'legal_warning'" },
                            { label: "상담원이 알아서 해 (방치)", prompt: "상담원 재량에 맡겨.", code: "\n  conflict_resolution:\n    active_defense: false" }
                        ]
                    },
                    {
                        q: "Step 5/5. 격한 통화 후에는?",
                        chips: [
                            { label: "스트레스 감지 시 자동 휴식 (케어)", prompt: "통화 내용이 격했으면, 강제로 1분간 휴식 시간을 배정해줘.", code: "\n  workflow:\n    wellness_check: true\n    dynamic_break: 'stress_based'" },
                            { label: "그래도 바로 연결 (효율)", prompt: "바쁘니까 그냥 계속 연결해.", code: "\n  workflow:\n    wellness_check: false" }
                        ]
                    }
                ]
            }
        };

        // --- CORE FUNCTIONS ---

        function switchScreen(id) {
            document.querySelectorAll('body > div').forEach(el => el.classList.add('hidden'));
            document.getElementById(id).classList.remove('hidden');
        }

        function appendMsg(role, text) {
            const history = document.getElementById('chat-history');
            const msg = document.createElement('div');
            msg.className = `msg ${role}`;
            msg.innerText = text;
            history.appendChild(msg);
            history.scrollTop = history.scrollHeight;
        }

        function typeCode(text) {
            const display = document.getElementById('code-display');
            // 기존 내용 보존하고 추가
            generatedCode += text;
            
            // Syntax Highlighting (Simple Regex)
            let formatted = generatedCode
                .replace(/^(\\s*)([a-z_]+):/gm, '$1<span class="k">$2</span>:') // keys
                .replace(/'([^']+)'/g, '<span class="s">\\' $1\\'</span>') // strings
                .split('\\n').map((line, i) => 
                    `<div class="code-line"><div class="line-num">${i+1}</div><div class="code-content">${line}</div></div>`
                ).join('');
            
            display.innerHTML = formatted;
            display.scrollTop = display.scrollHeight;
        }

        function setupPhase(phase) {
            currentPhase = phase;
            stepIndex = 0;
            generatedCode = phase === 1 
                ? "# Project: AI Call Center V1.0 (Efficiency First)\\nsystem_config:\\n" 
                : "# Project: AI Call Center V2.0 (Worker Centric)\\nsystem_config:\\n";
            
            document.getElementById('code-display').innerHTML = "";
            typeCode(""); // 초기화
            document.getElementById('chat-history').innerHTML = "";
            
            switchScreen('ide-screen');
            appendMsg('ai', scenarios[phase].intro);
            askQuestion();
        }

        function startPhase1() { setupPhase(1); }
        function startPhase2() { setupPhase(2); }

        function askQuestion() {
            if (stepIndex >= scenarios[currentPhase].steps.length) {
                // Done
                const btnId = `deploy-btn-${currentPhase}`;
                appendMsg('ai', "모든 프롬프트 설계가 완료되었습니다. 배포하시겠습니까?");
                
                const history = document.getElementById('chat-history');
                const btn = document.createElement('button');
                btn.className = 'btn';
                btn.innerText = currentPhase === 1 ? "🚀 V1.0 배포 및 시뮬레이션" : "🚀 V2.0 배포 및 결과 비교";
                btn.style.marginTop = "10px";
                btn.onclick = () => {
                    if(currentPhase === 1) switchScreen('intermission-screen');
                    else switchScreen('report-screen');
                };
                history.appendChild(btn);
                history.scrollTop = history.scrollHeight;
                
                // 입력창 비활성화
                document.getElementById('suggestion-chips').innerHTML = "";
                document.getElementById('prompt-input').disabled = true;
                return;
            }

            const stepData = scenarios[currentPhase].steps[stepIndex];
            
            // 1. AI 질문 표시
            setTimeout(() => {
                appendMsg('ai', stepData.q);
                
                // 2. 추천 칩 생성
                const chipContainer = document.getElementById('suggestion-chips');
                chipContainer.innerHTML = "";
                
                stepData.chips.forEach(chip => {
                    const c = document.createElement('div');
                    c.className = 'chip';
                    c.innerText = chip.label;
                    c.onclick = () => {
                        // 칩 클릭 시 인풋창에 텍스트 채움
                        const input = document.getElementById('prompt-input');
                        input.value = chip.prompt;
                        input.dataset.code = chip.code; // 코드 데이터 숨겨둠
                        input.focus();
                    };
                    chipContainer.appendChild(c);
                });
            }, 500);
        }

        // --- EVENT LISTENERS ---
        document.getElementById('prompt-input').addEventListener('keypress', function (e) {
            if (e.key === 'Enter' && this.value.trim() !== "") {
                const userText = this.value;
                const hiddenCode = this.dataset.code; // 칩에서 선택된 코드
                
                // 1. 유저 메시지 표시
                appendMsg('user', userText);
                this.value = "";
                this.dataset.code = ""; // 초기화
                document.getElementById('suggestion-chips').innerHTML = ""; // 칩 제거

                // 2. 코드 생성 효과 (hiddenCode가 있으면 그걸 쓰고, 없으면 기본값-여기선 데모라 칩 선택 필수 유도)
                if (hiddenCode) {
                    setTimeout(() => {
                        typeCode(hiddenCode);
                        stepIndex++;
                        askQuestion();
                    }, 600);
                } else {
                    // 칩 선택 안 하고 쳤을 때 (데모용 예외처리)
                    setTimeout(() => {
                        appendMsg('ai', "죄송합니다. 데모 버전에서는 상단의 가이드 칩을 먼저 선택해주셔야 정확한 코드가 생성됩니다.");
                        // 다시 질문
                        askQuestion(); 
                        stepIndex--; // 인덱스 복구
                        stepIndex++; 
                    }, 500);
                }
            }
        });

    </script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=False)

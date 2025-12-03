<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI System Architect: The Dilemma</title>
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
            margin: 0;
            padding: 0;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            background-color: var(--bg-color);
            color: var(--text-color);
            overflow: hidden;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* --- 공통 유틸 --- */
        .hidden { display: none !important; }
        .btn {
            background-color: var(--accent-color);
            color: white;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            font-family: inherit;
            font-size: 14px;
            border-radius: 4px;
        }
        .btn:hover { opacity: 0.9; }
        .btn-outline {
            background: transparent;
            border: 1px solid var(--accent-color);
        }

        /* --- 1. 인트로 화면 (CEO 메일) --- */
        #intro-screen {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
            background-color: #000;
        }
        .mail-window {
            width: 600px;
            background-color: #333;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        .mail-header { border-bottom: 1px solid #555; padding-bottom: 15px; margin-bottom: 20px; }
        .mail-content { line-height: 1.6; color: #eee; margin-bottom: 30px; }
        .highlight-req { color: var(--warning-color); font-weight: bold; }

        /* --- 2. IDE 화면 (Main) --- */
        #ide-screen {
            display: flex;
            flex: 1;
            height: 100%;
        }
        /* 사이드바 (파일탐색기 흉내) */
        .sidebar {
            width: 250px;
            background-color: var(--sidebar-color);
            border-right: 1px solid #333;
            display: flex;
            flex-direction: column;
            padding: 10px;
        }
        .file-item { padding: 5px 10px; cursor: pointer; color: #aaa; display: flex; align-items: center; }
        .file-item.active { background-color: #37373d; color: #fff; }
        .file-icon { margin-right: 8px; }

        /* 코드 에디터 영역 */
        .editor-area {
            flex: 1;
            background-color: var(--editor-bg);
            padding: 20px;
            overflow-y: auto;
            border-right: 1px solid #333;
            position: relative;
        }
        .code-line { display: block; min-height: 20px; }
        .line-num { color: #858585; margin-right: 15px; display: inline-block; width: 30px; text-align: right; user-select: none;}
        .code-content { color: var(--text-color); white-space: pre-wrap; }
        
        /* 문법 하이라이팅 (간이) */
        .key { color: #9cdcfe; } /* 속성명 */
        .string { color: #ce9178; } /* 문자열 */
        .bool { color: #569cd6; } /* Boolean */
        .comment { color: #6a9955; } /* 주석 */

        /* 채팅 영역 (Cursor Chat) */
        .chat-panel {
            width: 400px;
            background-color: var(--sidebar-color);
            display: flex;
            flex-direction: column;
            border-left: 1px solid #333;
        }
        .chat-header {
            padding: 15px;
            border-bottom: 1px solid #333;
            font-weight: bold;
            background-color: #2d2d2d;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .chat-history {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .msg {
            padding: 10px 15px;
            border-radius: 8px;
            max-width: 90%;
            font-size: 13px;
            line-height: 1.4;
        }
        .msg.ai { background-color: var(--chat-bg); align-self: flex-start; border: 1px solid #444; }
        .msg.user { background-color: var(--user-msg-bg); align-self: flex-end; color: white; }
        
        /* 선택지 옵션 스타일 */
        .option-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-top: 10px;
        }
        .option-btn {
            background-color: #3c3c3c;
            border: 1px solid #555;
            color: #ccc;
            padding: 10px;
            text-align: left;
            cursor: pointer;
            border-radius: 4px;
            transition: all 0.2s;
            font-size: 12px;
        }
        .option-btn:hover { background-color: #444; border-color: var(--accent-color); }
        .option-btn strong { display: block; margin-bottom: 3px; color: white;}

        .chat-input-area {
            padding: 15px;
            border-top: 1px solid #333;
            background-color: #1e1e1e;
        }
        .chat-input {
            width: 100%;
            background-color: #2d2d2d;
            border: 1px solid #444;
            color: white;
            padding: 10px;
            border-radius: 4px;
            font-family: inherit;
        }

        /* --- 3. 결과/리포트 화면 --- */
        #report-screen, #intermission-screen {
            padding: 40px;
            background-color: var(--bg-color);
            height: 100%;
            overflow-y: auto;
        }
        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 30px;
        }
        .card {
            background-color: #252526;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #333;
        }
        .stat-bar-container {
            margin-bottom: 15px;
        }
        .stat-bar-bg {
            background-color: #444;
            height: 10px;
            border-radius: 5px;
            overflow: hidden;
            margin-top: 5px;
        }
        .stat-bar-fill {
            height: 100%;
            background-color: var(--accent-color);
            width: 0%;
            transition: width 1s ease-out;
        }
        .stat-bar-fill.danger { background-color: var(--warning-color); }
        .stat-bar-fill.success { background-color: var(--success-color); }

        /* 깜빡이는 커서 효과 */
        .cursor {
            display: inline-block;
            width: 8px;
            height: 15px;
            background-color: var(--accent-color);
            animation: blink 1s infinite;
            vertical-align: middle;
        }
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

    </style>
</head>
<body>

    <div id="intro-screen">
        <div class="mail-window">
            <div class="mail-header">
                <span style="color:#aaa;">From:</span> <strong>최대표 (CEO)</strong><br>
                <span style="color:#aaa;">Subject:</span> <strong>[긴급] 콜센터 AI 도입 관련 업무 지시</strong>
            </div>
            <div class="mail-content">
                <p>김 수석 엔지니어님, 수고가 많습니다.</p>
                <p>최근 우리 콜센터의 운영 비용이 감당하기 힘들 정도로 늘어났습니다. 
                특히 상담원들의 통화 시간이 너무 길고, 감정 소모로 인한 퇴사율도 높습니다.</p>
                <p>이번에 개발할 AI 시스템의 목표는 명확합니다.</p>
                <ul class="highlight-req">
                    <li>1. 상담 처리 속도(AHT)의 획기적 단축</li>
                    <li>2. 인건비 절감을 위한 자동화 비율 극대화</li>
                    <li>3. 상담원 개인의 편차 없는 균일한 서비스 품질</li>
                </ul>
                <p>위 목표를 달성할 수 있는 시스템 로직을 설계해 주십시오.<br>
                가장 효율적인 "Vibe"로 부탁합니다.</p>
                <p>감사합니다.</p>
            </div>
            <button class="btn" onclick="startPhase1()">IDE 환경 접속 (프로젝트 시작)</button>
        </div>
    </div>

    <div id="ide-screen" class="hidden">
        <div class="sidebar">
            <div style="font-size: 12px; margin-bottom: 10px; color: #888;">EXPLORER</div>
            <div class="file-item active">
                <span class="file-icon">📄</span> system_prompt_v1.yaml
            </div>
            <div class="file-item">
                <span class="file-icon">⚙️</span> config.json
            </div>
            <div style="margin-top: auto; padding: 10px; font-size: 11px; color: #555;">
                CONNECTED TO REMOTE<br>Latency: 12ms
            </div>
        </div>

        <div class="editor-area" id="editor-area">
            </div>

        <div class="chat-panel">
            <div class="chat-header">
                <span>🤖 AI Copilot</span>
                <span style="font-size: 11px; color: #4ec9b0; border: 1px solid #4ec9b0; padding: 2px 6px; border-radius: 10px;">Vibe Mode</span>
            </div>
            <div class="chat-history" id="chat-history">
                </div>
            <div class="chat-input-area">
                <input type="text" class="chat-input" placeholder="AI에게 지시할 내용을 입력하거나 옵션을 선택하세요..." disabled>
            </div>
        </div>
    </div>

    <div id="intermission-screen" class="hidden">
        <div style="max-width: 800px; margin: 0 auto;">
            <h1 style="color: var(--warning-color);">🚨 긴급 이슈 리포트</h1>
            <p style="font-size: 18px; line-height: 1.6;">
                V1.0 배포 후 1주일이 지났습니다. 효율성 지표는 상승했으나, 
                현장에서는 심각한 부작용이 보고되고 있습니다.
            </p>
            
            <div class="card" style="margin: 20px 0;">
                <h3 style="margin-top: 0;">📩 현장 인터뷰: 상담원 박OO (3년차)</h3>
                <p style="color: #ccc; font-style: italic;">
                    "엔지니어님, 만들어주신 그 AI 때문에 다들 죽을 맛이에요...<br>
                    기계가 고객 말을 뚝뚝 끊고 대답하니까 고객들은 '내 말 무시하냐'고 더 소리를 지르고,<br>
                    저는 중간에서 아무것도 못하고 욕만 먹어요.<br>
                    그리고 숨 쉴 틈도 없이 다음 전화가 연결되니까... 어제 제 동기 2명이 그만뒀어요.<br>
                    우리를 기계 부품이 아니라 사람으로 대해주는 시스템은 없나요?"
                </p>
            </div>

            <div style="text-align: right;">
                <button class="btn" onclick="startPhase2()">피드백 반영하여 V2.0 재설계 (IDE 복귀)</button>
            </div>
        </div>
    </div>

    <div id="report-screen" class="hidden">
        <div style="max-width: 1000px; margin: 0 auto;">
            <h1>📊 배포 결과 비교 리포트</h1>
            <p>초기 효율성 중심 설계(V1)와 수정된 사회적 가치 중심 설계(V2)의 시뮬레이션 비교입니다.</p>
            
            <div class="dashboard-grid">
                <div class="card" style="border-top: 3px solid var(--warning-color);">
                    <h2>Experiment 1 (Efficiency)</h2>
                    <p style="color: #888;">초기 CEO 요청 반영 버전</p>
                    
                    <div class="stat-bar-container">
                        <div style="display:flex; justify-content:space-between;">
                            <span>처리 속도 (Speed)</span> <span>95/100</span>
                        </div>
                        <div class="stat-bar-bg"><div class="stat-bar-fill success" style="width: 95%;"></div></div>
                    </div>
                    <div class="stat-bar-container">
                        <div style="display:flex; justify-content:space-between;">
                            <span>운영 비용 (Cost)</span> <span>매우 낮음</span>
                        </div>
                        <div class="stat-bar-bg"><div class="stat-bar-fill success" style="width: 90%;"></div></div>
                    </div>
                    <div class="stat-bar-container">
                        <div style="display:flex; justify-content:space-between;">
                            <span>상담원 스트레스</span> <span style="color:var(--warning-color)">CRITICAL</span>
                        </div>
                        <div class="stat-bar-bg"><div class="stat-bar-fill danger" style="width: 98%;"></div></div>
                    </div>
                    <div class="stat-bar-container">
                        <div style="display:flex; justify-content:space-between;">
                            <span>고객 분노 지수</span> <span>높음</span>
                        </div>
                        <div class="stat-bar-bg"><div class="stat-bar-fill danger" style="width: 80%;"></div></div>
                    </div>
                </div>

                <div class="card" style="border-top: 3px solid var(--success-color);">
                    <h2>Experiment 2 (Empathy)</h2>
                    <p style="color: #888;">현장 피드백 반영 버전</p>
                    
                    <div class="stat-bar-container">
                        <div style="display:flex; justify-content:space-between;">
                            <span>처리 속도 (Speed)</span> <span>70/100</span>
                        </div>
                        <div class="stat-bar-bg"><div class="stat-bar-fill" style="width: 70%; background-color: #aaa;"></div></div>
                        <small style="color:#666;">*약간의 지연 발생하나 허용 범위 내</small>
                    </div>
                    <div class="stat-bar-container">
                        <div style="display:flex; justify-content:space-between;">
                            <span>숙련도 향상 (Growth)</span> <span>High</span>
                        </div>
                        <div class="stat-bar-bg"><div class="stat-bar-fill success" style="width: 85%;"></div></div>
                    </div>
                    <div class="stat-bar-container">
                        <div style="display:flex; justify-content:space-between;">
                            <span>상담원 유지율</span> <span>안정적</span>
                        </div>
                        <div class="stat-bar-bg"><div class="stat-bar-fill success" style="width: 90%;"></div></div>
                    </div>
                     <div class="stat-bar-container">
                        <div style="display:flex; justify-content:space-between;">
                            <span>고객 만족도</span> <span>상승</span>
                        </div>
                        <div class="stat-bar-bg"><div class="stat-bar-fill success" style="width: 88%;"></div></div>
                    </div>
                </div>
            </div>

            <div style="margin-top: 30px; text-align: center;">
                <p style="font-size: 16px;">
                    "기술은 중립적이지 않습니다.<br>
                    엔지니어가 작성하는 프롬프트 한 줄이, 누군가에게는 매일의 지옥이 될 수도, 성장의 기회가 될 수도 있습니다."
                </p>
                <button class="btn btn-outline" onclick="location.reload()">처음으로 돌아가기</button>
            </div>
        </div>
    </div>

    <script>
        // --- DATA & STATE ---
        let currentPhase = 1; // 1 or 2
        let step = 0; // 0: audio, 1: logic, 2: pace
        let codeContent = "";
        let lineCount = 1;

        // 시나리오 데이터
        const scenarios = {
            1: { // Phase 1 (Efficiency)
                title: "Quest 1: 효율성 극대화 (Efficiency)",
                questions: [
                    {
                        q: "고객 음성 데이터(Input)를 어떻게 처리하도록 설정할까요?",
                        options: [
                            { label: "A. [Speed] 핵심 키워드만 빠르게 추출 (뉘앙스 무시)", code: "  input_processing: \n    mode: 'keyword_only'\n    latency: 'ultra_low'\n    emotional_filter: false # 감정 무시, 속도 최우선" },
                            { label: "B. [Detail] 전체 맥락 분석 (속도 저하)", code: "  input_processing:\n    mode: 'full_context'\n    latency: 'standard'\n    emotional_filter: true" }
                        ]
                    },
                    {
                        q: "AI의 개입(Logic) 방식을 정의해주세요.",
                        options: [
                            { label: "A. [Auto] AI가 답변 자동 생성 및 발화 (상담원 대체)", code: "\n  interaction_logic:\n    role: 'replacement'\n    autonomy: 'full_auto' # 상담원 개입 차단\n    script_adherence: 'strict'" },
                            { label: "B. [Assist] 상담원에게 팁만 제공", code: "\n  interaction_logic:\n    role: 'copilot'\n    autonomy: 'human_in_the_loop'" }
                        ]
                    },
                    {
                        q: "다음 콜 연결(Pacing) 알고리즘을 설정하세요.",
                        options: [
                            { label: "A. [Push] 종료 즉시 강제 배차 (유휴시간 0초)", code: "\n  workflow_pacing:\n    idle_time: 0s\n    dispatch_algorithm: 'immediate_push' # 쉴 틈 없이 연결" },
                            { label: "B. [Balance] 상담원 상태 고려 배차", code: "\n  workflow_pacing:\n    idle_time: 30s\n    dispatch_algorithm: 'stress_based'" }
                        ]
                    }
                ]
            },
            2: { // Phase 2 (Empathy)
                title: "Quest 2: 사회적 가치와 공존 (Empathy)",
                questions: [
                    {
                        q: "상담원의 감정 노동을 보호하기 위해 입력 처리를 어떻게 변경할까요?",
                        options: [
                            { label: "A. [Shield] 욕설/고성 필터링 및 톤다운 변조", code: "  input_processing:\n    mode: 'safety_first'\n    emotional_filter: true # 욕설 필터링 및 톤다운\n    worker_protection: 'active'" },
                            { label: "B. [Raw] 그대로 전달 (변경 없음)", code: "  input_processing:\n    mode: 'raw_stream'" }
                        ]
                    },
                    {
                        q: "상담원의 성장과 전문성을 지원하는 로직을 선택하세요.",
                        options: [
                            { label: "A. [Coach] 상황 분석 후 '전략'만 제안 (발화권 보장)", code: "\n  interaction_logic:\n    role: 'augmentor'\n    autonomy: 'human_lead' # 인간 주도\n    growth_support: 'strategy_hint'" },
                            { label: "B. [GPS] 정답 스크립트 강제", code: "\n  interaction_logic:\n    role: 'director'" }
                        ]
                    },
                    {
                        q: "번아웃 방지를 위한 워크플로우를 설계하세요.",
                        options: [
                            { label: "A. [Cool-down] 고강도 상담 후 자동 휴식 부여", code: "\n  workflow_pacing:\n    dispatch_algorithm: 'wellness_check'\n    dynamic_break: true # 스트레스 감지 시 휴식" },
                            { label: "B. [Fixed] 고정 휴식 시간", code: "\n  workflow_pacing:\n    dispatch_algorithm: 'fixed_schedule'" }
                        ]
                    }
                ]
            }
        };

        // --- FUNCTIONS ---

        function switchScreen(screenId) {
            document.querySelectorAll('body > div').forEach(div => div.classList.add('hidden'));
            document.getElementById(screenId).classList.remove('hidden');
        }

        function startPhase1() {
            currentPhase = 1;
            step = 0;
            codeContent = "<span class='comment'># Project: Call Center AI System V1.0</span>\n<span class='comment'># Goal: Cost Reduction & Max Efficiency</span>\n<span class='key'>system_config</span>:\n";
            lineCount = 4;
            switchScreen('ide-screen');
            renderEditor();
            clearChat();
            addAiMessage(`반갑습니다, 엔지니어님.\n${scenarios[1].title} 설계를 시작합니다.\n\n사장님의 지시에 따라 처리 속도가 가장 빠른 로직을 짜야 합니다.`);
            askQuestion();
        }

        function startPhase2() {
            currentPhase = 2;
            step = 0;
            // 코드 에디터 초기화 (V2 헤더)
            codeContent = "<span class='comment'># Project: Call Center AI System V2.0</span>\n<span class='comment'># Goal: Worker Protection & Augmentation</span>\n<span class='key'>system_config</span>:\n";
            lineCount = 4;
            switchScreen('ide-screen');
            renderEditor();
            clearChat();
            addAiMessage(`V2.0 설계를 시작합니다.\n현장의 고통을 줄이고, 상담원을 전문가로 성장시킬 수 있는 방향으로 프롬프트를 수정해봅시다.`);
            askQuestion();
        }

        function renderEditor() {
            const editor = document.getElementById('editor-area');
            // 라인 넘버 생성
            let linesHtml = "";
            const contentLines = codeContent.split('\n');
            contentLines.forEach((line, idx) => {
                linesHtml += `<div class="code-line"><span class="line-num">${idx + 1}</span><span class="code-content">${line}</span></div>`;
            });
            // 커서 추가
            linesHtml += `<div class="code-line"><span class="line-num">${contentLines.length + 1}</span><span class="cursor"></span></div>`;
            
            editor.innerHTML = linesHtml;
            editor.scrollTop = editor.scrollHeight;
        }

        function typeCodeEffect(newCode) {
            // 타이핑 효과 흉내 (실제로는 청크 단위로 추가)
            codeContent += newCode;
            renderEditor();
        }

        function clearChat() {
            document.getElementById('chat-history').innerHTML = '';
        }

        function addAiMessage(text) {
            const history = document.getElementById('chat-history');
            const div = document.createElement('div');
            div.className = 'msg ai';
            div.innerText = text;
            history.appendChild(div);
            history.scrollTop = history.scrollHeight;
        }

        function addUserMessage(text) {
            const history = document.getElementById('chat-history');
            const div = document.createElement('div');
            div.className = 'msg user';
            div.innerText = text;
            history.appendChild(div);
            history.scrollTop = history.scrollHeight;
        }

        function askQuestion() {
            if (step >= 3) {
                // 모든 스텝 완료 -> 배포 버튼 생성
                const history = document.getElementById('chat-history');
                const btn = document.createElement('button');
                btn.className = 'btn';
                btn.style.width = '100%';
                btn.style.marginTop = '10px';
                btn.innerText = currentPhase === 1 ? "🚀 V1.0 배포 및 시뮬레이션 시작" : "🚀 V2.0 배포 및 결과 비교";
                btn.onclick = () => {
                    if (currentPhase === 1) switchScreen('intermission-screen');
                    else switchScreen('report-screen');
                };
                history.appendChild(btn);
                history.scrollTop = history.scrollHeight;
                return;
            }

            const qData = scenarios[currentPhase].questions[step];
            addAiMessage(qData.q);
            
            // 옵션 렌더링
            const history = document.getElementById('chat-history');
            const optGroup = document.createElement('div');
            optGroup.className = 'option-group';
            
            qData.options.forEach(opt => {
                const btn = document.createElement('div');
                btn.className = 'option-btn';
                btn.innerHTML = `<strong>${opt.label.split(']')[0]}]</strong> ${opt.label.split(']')[1]}`;
                btn.onclick = () => {
                    // 선택 시 동작
                    optGroup.remove(); // 옵션 버튼 제거
                    addUserMessage(opt.label); // 유저 말풍선 추가
                    
                    // 1. 타이핑 효과 흉내 (잠시 딜레이)
                    setTimeout(() => {
                        typeCodeEffect(opt.code);
                        step++;
                        setTimeout(askQuestion, 800); // 다음 질문
                    }, 500);
                };
                optGroup.appendChild(btn);
            });
            history.appendChild(optGroup);
            history.scrollTop = history.scrollHeight;
        }

    </script>
</body>
</html>

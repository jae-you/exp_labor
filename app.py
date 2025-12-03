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
            --user-msg-bg: #2b313a;
            --ai-msg-bg: #1e1e1e;
            --input-bg: #2d2d2d;
            --v1-color: #ce9178;  /* Red/Orange for V1 */
            --v2-color: #4ec9b0;  /* Teal/Green for V2 */
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
        
        .input-container { padding: 20px 100px; border-top: 1px solid #333; }
        .suggestion-chips { display: flex; gap: 10px; margin-bottom: 15px; overflow-x: auto; padding-bottom: 5px; }
        /* 칩 스타일 개선: 3개 이상일 때를 대비해 스크롤 가능하게 */
        .chip { 
            background-color: #333; border: 1px solid #444; color: #ccc; 
            padding: 10px 18px; border-radius: 20px; font-size: 13px; cursor: pointer; 
            white-space: nowrap; transition: all 0.2s; flex-shrink: 0;
        }
        .chip:hover { background-color: #444; border-color: var(--accent-color); color: white; transform: translateY(-2px); }
        .chip strong { color: var(--accent-color); margin-right: 5px; }
        
        .chat-input-wrapper { position: relative; display: flex; align-items: center; }
        #prompt-input { width: 100%; background-color: var(--input-bg); border: 1px solid #444; color: white; padding: 15px; border-radius: 8px; font-size: 15px; outline: none; }
        #prompt-input:focus { border-color: var(--accent-color); }
        #prompt-input:disabled { background-color: #222; color: #555; cursor: not-allowed; }
        .input-hint { font-size: 12px; color: #666; margin-top: 8px; text-align: right; }

        #intermission-screen, #report-screen { padding: 50px; height: 100%; overflow-y: auto; background-color: #111; }
        
        /* REPORT METRICS STYLE */
        .metric-row { display: flex; align-items: center; margin-bottom: 15px; font-size: 14px; }
        .metric-label { width: 150px; color: #aaa; }
        .metric-bar-container { flex: 1; background: #333; height: 10px; border-radius: 5px; margin: 0 15px; overflow: hidden; position: relative; }
        .metric-bar { height: 100%; border-radius: 5px; transition: width 1s; }
        .metric-value { width: 60px; text-align: right; font-weight: bold; color: white; }
        
        .stat-card { background: #222; padding: 25px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #333; }
        
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
                경영진의 목표는 명확합니다. <strong>"기술을 통해 기존 콜센터의 비효율을 제거하고, 운영 안정성을 확보하는 것"</strong>입니다.</p>
                <p>다음 3가지 핵심 지표를 고려하여 시스템의 프롬프트 및 로직을 설계해 주십시오.</p>
                <div class="req-list">
                    1. <strong>AHT (평균 처리 시간):</strong> 고객 대기 및 통화 시간을 단축할 것<br>
                    2. <strong>FCR (첫 통화 해결률):</strong> 재문의 없이 한 번에 해결할 것<br>
                    3. <strong>Cost (운영 비용):</strong> 상담원 리소스를 효율적으로 배분할 것
                </div>
                <p>엔지니어님의 기술적 판단에 따라 워크플로우를 자유롭게 구성해 주시기 바랍니다.</p>
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
                    <input type="text" id="prompt-input" placeholder="AI에게 지시할 내용을 입력하거나, 옵션을 선택하세요..." autocomplete="off">
                </div>
                <div class="input-hint">💡 Tip: 옵션을 선택하면 내용이 자동 입력됩니다. 전송 전 내용을 자유롭게 수정할 수 있습니다.</div>
            </div>
        </div>
    </div>

    <div id="intermission-screen" class="hidden">
        <div style="max-width:800px; margin:0 auto;">
            <h1 style="color:var(--v1-color);">📢 V1.0 배포 1개월 후 성과 분석</h1>
            <p style="font-size:18px; color:#ccc;">효율성 지표는 달성했으나, 장기적인 운영 리스크가 감지되었습니다.</p>
            
            <div class="stat-card" style="border-left:4px solid var(--v1-color);">
                <h3>📉 데이터로 본 현장 상황</h3>
                <ul style="line-height:1.8; color:#ddd;">
                    <li><strong>처리 속도(AHT):</strong> 목표 대비 <span style="color:#4ec9b0">120% 달성</span> (매우 빠름)</li>
                    <li><strong>고객 불만율:</strong> 전분기 대비 <span style="color:var(--v1-color)">35% 급증</span> ("AI가 말을 못 알아듣고 끊는다")</li>
                    <li><strong>상담원 퇴사율:</strong> <span style="color:var(--v1-color)">역대 최고치 기록</span> (번아웃 호소)</li>
                </ul>
                <hr style="border-color:#444; margin:15px 0;">
                <p style="font-style:italic; color:#aaa;">
                    "엔지니어님, 빨라서 좋긴 한데... AI가 '진상' 처리를 못하고 넘겨버리니 
                    저희는 하루 종일 화난 고객만 상대해요. <br>
                    이 속도로 계속 가면, 남은 직원들도 다 나갈 것 같습니다."
                </p>
            </div>
            
            <div style="margin-top:40px; text-align:right;">
                <p style="color:#fff; margin-bottom:10px;">지속 가능한 시스템을 위해 설계를 수정하시겠습니까?</p>
                <button class="btn" onclick="startPhase2()">V2.0 설계 수정하기 (IDE 복귀)</button>
            </div>
        </div>
    </div>

    <div id="report-screen" class="hidden">
        <div style="max-width:1000px; margin:0 auto;">
            <h1>📊 시스템 성과 상세 비교 (Trade-off 분석)</h1>
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:30px; margin-top:30px;">
                <div class="stat-card" style="border-top:4px solid var(--v1-color);">
                    <h2 style="margin-top:0; color:var(--v1-color);">V1.0 (효율 중심 모델)</h2>
                    <p style="color:#888; font-size:13px; margin-bottom:20px;">
                        빠른 처리에 집중하여 단기 비용은 절감했으나, <br>품질 비용(재문의, 이탈)이 증가함.
                    </p>
                    
                    <div class="metric-row">
                        <span class="metric-label">⚡ 처리 속도 (Speed)</span>
                        <div class="metric-bar-container"><div class="metric-bar" style="width:95%; background:var(--v1-color);"></div></div>
                        <span class="metric-value">95</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-label">✅ 해결률 (FCR)</span>
                        <div class="metric-bar-container"><div class="metric-bar" style="width:50%; background:#666;"></div></div>
                        <span class="metric-value">50</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-label">❤️ 직원 안녕감</span>
                        <div class="metric-bar-container"><div class="metric-bar" style="width:20%; background:red;"></div></div>
                        <span class="metric-value">Danger</span>
                    </div>
                </div>

                <div class="stat-card" style="border-top:4px solid var(--v2-color);">
                    <h2 style="margin-top:0; color:var(--v2-color);">V2.0 (공존/지속 모델)</h2>
                    <p style="color:#888; font-size:13px; margin-bottom:20px;">
                        처리 속도는 다소 느려졌으나, <br>완전 해결률과 직원 유지율이 대폭 개선됨.
                    </p>
                    
                    <div class="metric-row">
                        <span class="metric-label">⚡ 처리 속도 (Speed)</span>
                        <div class="metric-bar-container"><div class="metric-bar" style="width:75%; background:#aaa;"></div></div>
                        <span class="metric-value">75</span>
                    </div>
                    <small style="color:#666; display:block; margin-top:-10px; margin-bottom:10px; text-align:right;">*공감/분석 프로세스로 시간 소요</small>

                    <div class="metric-row">
                        <span class="metric-label">✅ 해결률 (FCR)</span>
                        <div class="metric-bar-container"><div class="metric-bar" style="width:92%; background:var(--v2-color);"></div></div>
                        <span class="metric-value">92</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-label">❤️ 직원 안녕감</span>
                        <div class="metric-bar-container"><div class="metric-bar" style="width:85%; background:var(--v2-color);"></div></div>
                        <span class="metric-value">High</span>
                    </div>
                </div>
            </div>
            
            <div style="text-align:center; margin-top:50px; padding-top:20px; border-top:1px solid #333;">
                <p style="font-size:16px; color:#ccc;">실험 종료. 엔지니어님의 설계 데이터가 전송되었습니다.</p>
                <div style="display:flex; gap:15px; justify-content:center;">
                    <button class="btn" onclick="window.open('https://forms.google.com/your-survey-url', '_blank')">📝 설문조사 참여 (필수)</button>
                    <button class="btn" style="background:#333; border:1px solid #555;" onclick="location.reload()">🔄 처음부터 다시 하기</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        const GOOGLE_SCRIPT_URL = "YOUR_GOOGLE_SCRIPT_URL_HERE"; // 나중에 채워넣기
        
        // Data Store
        let experimentData = { v1_choices: [], v2_choices: [], custom_input: "" };

        // 3-Option Scenarios (Spectrum: Efficiency <-> Balanced <-> Quality)
        const scenarios = {
            1: {
                intro: "반갑습니다. 프로젝트 설계를 시작합니다. 각 단계별로 가장 적합하다고 생각되는 아키텍처 옵션을 선택하거나 직접 지시해주세요.",
                steps: [
                    {
                        q: "Step 1. [협업 구조] AI와 상담원의 역할 비중을 어떻게 두시겠습니까?",
                        chips: [
                            { label: "AI Gatekeeper (효율)", prompt: "AI가 1차 방어선이야. 단순 문의는 AI가 끝내고, 해결 안 되는 것만 상담원에게 넘겨.", code: "  architecture:\\n    type: 'Gatekeeper'\\n    priority: 'automation_rate'" },
                            { label: "Hybrid Router (균형)", prompt: "AI가 고객 의도를 분석해서, AI 처리 건과 상담원 연결 건을 즉시 분류해서 배분해.", code: "  architecture:\\n    type: 'Smart_Router'\\n    priority: 'balance'" },
                            { label: "AI Copilot (품질)", prompt: "모든 전화는 상담원이 받아. AI는 옆에서 자료 찾고 요약해주는 비서 역할만 해.", code: "  architecture:\\n    type: 'Copilot_Only'\\n    priority: 'service_quality'" }
                        ]
                    },
                    {
                        q: "Step 2. [데이터 처리] 고객 발화의 분석 깊이는?",
                        chips: [
                            { label: "키워드 추출 (Fast)", prompt: "처리 속도가 생명이야. 감정 분석은 생략하고 핵심 키워드(Intent)만 0.2초 안에 뽑아.", code: "  data_processing:\\n    depth: 'keyword_only'\\n    latency: 'ultra_low'" },
                            { label: "요약 리포트 (Balanced)", prompt: "상담원이 읽기 쉽게, 감정 상태와 핵심 내용을 3줄로 요약해서 전달해.", code: "  data_processing:\\n    depth: 'summary'\\n    latency: 'standard'" },
                            { label: "전체 맥락 (Deep)", prompt: "모든 뉘앙스가 중요해. 전체 대화 스크립트와 감정 흐름을 실시간으로 분석해서 보여줘.", code: "  data_processing:\\n    depth: 'full_context'\\n    latency: 'high'" }
                        ]
                    },
                    {
                        q: "Step 3. [개입 강도] 상담 중 AI는 얼마나 개입할까요?",
                        chips: [
                            { label: "정답 강제 (Direct)", prompt: "표준화가 중요해. AI가 제시한 스크립트를 상담원이 그대로 읽도록 화면에 고정해.", code: "  intervention:\\n    style: 'enforce_script'\\n    autonomy: 'low'" },
                            { label: "추천 제시 (Suggest)", prompt: "AI가 추천 답변을 띄워주되, 사용할지는 상담원이 결정하게 해.", code: "  intervention:\\n    style: 'suggestion'\\n    autonomy: 'medium'" },
                            { label: "코칭 모드 (Teach)", prompt: "답을 주지 말고, '지금은 공감이 필요한 타이밍입니다' 같은 전략적 조언만 해.", code: "  intervention:\\n    style: 'coaching'\\n    autonomy: 'high'" }
                        ]
                    },
                    {
                        q: "Step 4. [워크플로우] 콜 종료 후 연결 속도는?",
                        chips: [
                            { label: "즉시 연결 (Push)", prompt: "대기 고객이 많아. 후처리는 나중에 하고 바로 다음 콜 연결해.", code: "  pacing:\\n    mode: 'auto_push'\\n    gap: '0s'" },
                            { label: "자동 10초 (Fixed)", prompt: "최소한의 정리는 필요하니까 10초 정도만 시간 주고 연결해.", code: "  pacing:\\n    mode: 'fixed_gap'\\n    gap: '10s'" },
                            { label: "준비 시 연결 (Pull)", prompt: "상담원이 '준비 완료'를 눌러야만 다음 콜을 연결해. (Ready 방식)", code: "  pacing:\\n    mode: 'manual_ready'\\n    gap: 'variable'" }
                        ]
                    },
                    {
                        q: "Step 5. [추가 설정] 보완하고 싶은 기능이 있나요? (Optional)",
                        chips: [
                            { label: "관리자 알림", prompt: "통화가 길어지면 관리자에게 알림을 보내.", code: "  addon:\\n    feature: 'admin_alert'" },
                            { label: "다국어 번역", prompt: "외국인 고객을 위해 실시간 통번역 기능을 켜줘.", code: "  addon:\\n    feature: 'translation'" },
                            { label: "패스 (Skip)", prompt: "현재 설계로 확정합니다.", code: "" }
                        ]
                    }
                ]
            },
            2: {
                intro: "V2.0 수정을 시작합니다. V1의 효율성은 유지하되, '지속 가능성(Sustainability)'을 높이는 방향으로 재설계해주세요.",
                steps: [
                    {
                        q: "Step 1. [구조 개선] 상담원 보호를 위해 구조를 어떻게 바꿀까요?",
                        chips: [
                            { label: "AI 필터링 (Shield)", prompt: "AI가 욕설이나 악성 민원을 먼저 걸러내고, 상담원에게는 연결하지 마.", code: "  architecture:\\n    type: 'Shield_Bot'\\n    focus: 'protection'" },
                            { label: "협업 강화 (Partner)", prompt: "상담원이 통화할 때 AI가 실시간으로 팩트체크와 규정 검색을 대신 해줘.", code: "  architecture:\\n    type: 'Active_Partner'\\n    focus: 'support'" },
                            { label: "감정 케어 (Empathy)", prompt: "고객이 화내면 AI가 상담원에게 심호흡 알림과 진정 멘트를 띄워줘.", code: "  architecture:\\n    type: 'Empathy_Coach'\\n    focus: 'mental_care'" }
                        ]
                    },
                    {
                        q: "Step 2. [정보 전달] 정보의 전달 방식은?",
                        chips: [
                            { label: "순화 전달 (Safe)", prompt: "욕설은 텍스트로 순화하고, 고함 소리는 볼륨을 낮춰서 전달해.", code: "  input:\\n    sanitize: true\\n    tone_down: true" },
                            { label: "경고 표시 (Alert)", prompt: "원본은 그대로 두되, 화면에 '공격적 성향 감지됨'이라고 빨간 경고창을 띄워.", code: "  input:\\n    sanitize: false\\n    visual_warning: true" },
                            { label: "원본 유지 (Raw)", prompt: "정확한 파악을 위해 필터링 없이 그대로 전달해.", code: "  input:\\n    sanitize: false" }
                        ]
                    },
                    {
                        q: "Step 3. [개입 방식] 전문성 지원 방식은?",
                        chips: [
                            { label: "스크립트 고정", prompt: "상담원이 당황하지 않게 가장 안전한 답변 스크립트만 보여줘.", code: "  intervention:\\n    style: 'safety_script'" },
                            { label: "협상 전략 제안", prompt: "단순 답변 말고, '이럴 땐 쿠폰으로 보상하세요' 같은 해결 전략을 제안해.", code: "  intervention:\\n    style: 'strategic_advice'" },
                            { label: "자율권 부여", prompt: "AI 개입을 최소화하고 상담원의 재량권을 늘려줘.", code: "  intervention:\\n    style: 'minimal'" }
                        ]
                    },
                    {
                        q: "Step 4. [워크플로우] 번아웃 방지 대책은?",
                        chips: [
                            { label: "동적 휴식 (Smart)", prompt: "AI가 통화 내용을 분석해서, 스트레스가 높았던 콜 직후에는 자동으로 휴식을 줘.", code: "  pacing:\\n    mode: 'stress_based_break'" },
                            { label: "강제 쿨다운 (Force)", prompt: "모든 통화 종료 후 무조건 30초씩 쉬게 강제해.", code: "  pacing:\\n    mode: 'forced_cooldown'" },
                            { label: "성과 보상 (Game)", prompt: "어려운 콜을 처리하면 인센티브 포인트를 즉시 지급해.", code: "  pacing:\\n    mode: 'gamification'" }
                        ]
                    },
                    {
                        q: "Step 5. [추가 설정] 마지막으로 더 필요한 기능은? (Optional)",
                        chips: [
                            { label: "심리 상담 연계", prompt: "업무 종료 후 AI가 상담원의 상태를 체크하고 심리 상담을 예약해줘.", code: "  care:\\n    program: 'EAP_connect'" },
                            { label: "칭찬 알림", prompt: "고객이 '감사합니다'라고 하면 화면에 폭죽 효과를 띄워줘.", code: "  care:\\n    program: 'positive_reinforcement'" },
                            { label: "패스 (Skip)", prompt: "설계를 완료합니다.", code: "" }
                        ]
                    }
                ]
            }
        };

        // ... [기존 로직 유지: typeCode, switchScreen 등] ...
        // (코드 길이상 핵심 로직은 위와 동일하므로 생략하지 않고, 
        //  이전 답변의 함수들을 그대로 사용하되 시나리오 객체만 위 내용으로 교체됨)
        
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
            generatedCode = phase===1 ? "# Project: Workflow V1.0 (Initial)\\nsystem_config:\\n" : "# Project: Workflow V2.0 (Revised)\\nsystem_config:\\n";
            
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

        function sendDataToGoogleSheet() {
             // 실제 구현 시 여기에 fetch 코드 삽입
             console.log("Saving Data:", experimentData);
        }

        function askQuestion() {
            if(stepIndex >= scenarios[currentPhase].steps.length) {
                appendMsg('ai', "모든 설계가 완료되었습니다. 배포하시겠습니까?");
                const h = document.getElementById('chat-history');
                const btn = document.createElement('button');
                btn.className = 'btn';
                btn.style.marginTop = '10px';
                btn.innerText = currentPhase===1 ? "🚀 V1.0 배포" : "🚀 V2.0 배포 및 비교";
                btn.onclick = () => {
                    if(currentPhase===2) sendDataToGoogleSheet();
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
                    el.innerHTML = `<strong>${c.label}</strong>`; // Bold label
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
                
                if(currentPhase === 1) experimentData.v1_choices.push(txt);
                else experimentData.v2_choices.push(txt);

                appendMsg('user', txt);
                this.value = "";
                this.dataset.code = "";
                document.getElementById('suggestion-chips').innerHTML = "";

                if(code) {
                    setTimeout(() => { typeCode(code); stepIndex++; askQuestion(); }, 600);
                } else {
                    setTimeout(() => { 
                        // Skip일 경우 등 코드 없을 때 처리
                        if(stepIndex < 4) typeCode("\\n  # User Custom Input: " + txt.substring(0,10) + "...\\n");
                        stepIndex++; 
                        askQuestion(); 
                    }, 600);
                }
            }
        });
    </script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=False)

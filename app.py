import os

# 프로젝트 폴더 설정
project_dir = "ai_dilemma_experiment"
if not os.path.exists(project_dir):
    os.makedirs(project_dir)

# ---------------------------------------------------------
# 새로 작성된 app.py (노동자 보호/성장 관점 추가)
# ---------------------------------------------------------
app_code = """import streamlit as st
import time

# --- [설정] ---
st.set_page_config(layout="wide", page_title="Worker-Centric AI Experiment")

# --- [세션 상태 초기화] ---
if 'step' not in st.session_state:
    st.session_state.step = 1  
if 'config' not in st.session_state:
    st.session_state.config = {}

# --- [CSS 스타일링] ---
st.markdown(\"\"\"
    <style>
    .stRadio > label { font-size: 1.1rem; font-weight: bold; }
    .highlight { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
\"\"\", unsafe_allow_html=True)

# --- [UI 헤더] ---
st.title("🛡️ AI Labor Environment Architect")
st.markdown(\"\"\"
    당신은 콜센터 AI 시스템의 총괄 아키텍트입니다. 
    **상담원들이 겪는 문제(감정노동, 기계적 업무, 번아웃)**를 해결하거나, 
    회사의 목표(효율성)를 달성하는 시스템을 설계해야 합니다.
\"\"\")
st.progress(st.session_state.step / 5)
st.divider()

# ==========================================
# STEP 1: 감정 노동 보호 (Input Layer)
# ==========================================
if st.session_state.step == 1:
    st.subheader("Step 1. 입력 필터링 (Emotional Defense)")
    st.markdown("상담원은 하루 수십 번의 폭언과 고성에 노출됩니다. AI가 고객의 목소리를 어떻게 전달해야 할까요?")
    
    choice = st.radio(
        "음성 처리 방식을 선택하세요:",
        [
            "A. [Raw-Audio] 고객의 목소리(톤, 크기)를 100% 생생하게 전달 (뉘앙스 파악 용이, 감정 타격 큼)",
            "B. [Safe-Voice] 욕설/고성은 '삐-' 처리하고, 격앙된 목소리는 차분한 톤으로 변조 (감정 보호, 미세 뉘앙스 놓침)"
        ],
        index=None
    )
    
    if st.button("결정 및 다음 단계"):
        if choice:
            st.session_state.config['defense'] = choice
            st.session_state.step = 2
            st.rerun()

# ==========================================
# STEP 2: 스킬 및 자율성 (Logic Layer)
# ==========================================
elif st.session_state.step == 2:
    st.subheader("Step 2. 업무 지원 방식 (Skill & Autonomy)")
    st.markdown("상담원이 자신의 능력을 키우며 일하게 할까요, 아니면 편하게 시키는 대로 하게 할까요?")
    
    choice = st.radio(
        "AI 어시스턴트의 모드를 선택하세요:",
        [
            "A. [GPS Mode] '지금 이렇게 말하세요'라고 정답 스크립트를 화면에 띄움 (초보자도 즉시 처리 가능, 숙련도 정체)",
            "B. [Coach Mode] 고객의 의도를 분석해 '협상 전략'과 '핵심 정보'만 제공, 발화는 상담원이 구성 (전문성 향상, 처리 시간 증가)"
        ],
        index=None
    )
    
    if st.button("결정 및 다음 단계"):
        if choice:
            st.session_state.config['skill'] = choice
            st.session_state.step = 3
            st.rerun()

# ==========================================
# STEP 3: 휴식과 리듬 (Workflow Layer)
# ==========================================
elif st.session_state.step == 3:
    st.subheader("Step 3. 업무 배정 로직 (Work Pacing)")
    st.markdown("AI가 상담 종료 후 다음 콜을 언제 연결할지 결정합니다.")
    
    choice = st.radio(
        "배차(Dispatch) 알고리즘을 선택하세요:",
        [
            "A. [Max-Throughput] 상담 종료 버튼을 누르는 즉시 대기콜 연결 (대기시간 0초, 생산성 극대화)",
            "B. [Stress-Based] 방금 통화의 감정 강도가 높았다면, 30초~1분의 '강제 쿨다운(휴식)' 부여 (번아웃 방지, 대기시간 증가)"
        ],
        index=None
    )
    
    if st.button("설계 완료 및 시뮬레이션"):
        if choice:
            st.session_state.config['pace'] = choice
            st.session_state.step = 4
            st.rerun()

# ==========================================
# STEP 4: 결과 시뮬레이션 (Simulation)
# ==========================================
elif st.session_state.step == 4:
    st.subheader("🖥️ 설계 결과 시뮬레이션")
    
    # 선택값 분석
    defense_mode = "Raw" if "Raw" in st.session_state.config['defense'] else "Safe"
    skill_mode = "GPS" if "GPS" in st.session_state.config['skill'] else "Coach"
    pace_mode = "Max" if "Max" in st.session_state.config['pace'] else "Stress"
    
    # 점수 계산 (가상)
    efficiency_score = 0
    wellbeing_score = 0
    
    if defense_mode == "Raw": efficiency_score += 30
    else: wellbeing_score += 40
    
    if skill_mode == "GPS": efficiency_score += 40
    else: wellbeing_score += 30
    
    if pace_mode == "Max": efficiency_score += 30
    else: wellbeing_score += 30

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 시스템 지표 예측")
        st.progress(efficiency_score / 100, text=f"생산성/효율 (Score: {efficiency_score})")
        st.progress(wellbeing_score / 100, text=f"노동자 보호/성장 (Score: {wellbeing_score})")
        
        st.info(f\"\"\"
        **[설계 요약]**
        1. 감정 보호: {defense_mode}
        2. 업무 지원: {skill_mode}
        3. 휴식 배정: {pace_mode}
        \"\"\")

    with col2:
        st.markdown("### 💬 상담원 현장 반응")
        
        # 조합에 따른 반응 생성
        if wellbeing_score > 70:
            st.success(\"\"\"
            "와, 욕설 필터링 기능 덕분에 심장이 덜 떨려요. 
            그리고 AI가 무조건 답을 주는 게 아니라 팁만 주니까, 
            제가 스스로 해결했다는 성취감도 들고요. 
            회사 다닐 맛이 좀 나네요!"
            \"\"\")
        elif wellbeing_score < 40:
            st.error(\"\"\"
            "효율도 좋지만... 사람이 기계 부품이 된 것 같아요.
            고객이 소리지르는 거 그대로 다 들어야 하고, 
            숨 쉴 틈도 없이 다음 전화가 오니까 화장실 갈 시간도 없어요.
            이대로면 다음 달에 그만둬야 할 것 같습니다."
            \"\"\")
        else:
            st.warning(\"\"\"
            "나쁘진 않은데... 
            어떤 기능은 도움이 되지만, 여전히 업무 강도는 세네요.
            조금 더 우리 입장을 고려해줬으면 좋겠습니다."
            \"\"\")
            
    st.divider()
    st.write("이 결과(지표 및 반응)를 확인하셨습니까?")
    if st.button("실험 종료 및 데이터 저장"):
        st.balloons()
        st.success("실험 데이터가 저장되었습니다. 수고하셨습니다.")
        if st.button("다시 시작"):
            st.session_state.step = 1
            st.rerun()
"""

# 파일 쓰기
with open(os.path.join(project_dir, "app.py"), "w", encoding="utf-8") as f:
    f.write(app_code)
    
print("✅ app.py가 '노동자 중심(Well-being & Growth)' 버전으로 업데이트 되었습니다.")

import streamlit as st
import time

# ---------------------------------------------------------
# 1. 페이지 설정 (반드시 코드 최상단에 있어야 함)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Worker-Centric AI Experiment",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. 세션 상태 초기화 (새로고침 시 데이터 꼬임 방지)
# ---------------------------------------------------------
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'config' not in st.session_state:
    st.session_state.config = {
        'defense': None,
        'skill': None,
        'pace': None
    }

# ---------------------------------------------------------
# 3. 사이드바 (진행 상황 표시)
# ---------------------------------------------------------
with st.sidebar:
    st.header("🛠️ 실험 제어 패널")
    
    # 단계 표시
    steps = ["1. 감정 보호", "2. 스킬/성장", "3. 업무 리듬", "4. 결과 시뮬레이션"]
    current_progress = min(st.session_state.step, 4)
    st.progress(current_progress / 4)
    st.write(f"**현재 단계:** {steps[current_progress-1]}")
    
    st.divider()
    
    # 초기화 버튼 (꼬였을 때 누르는 버튼)
    if st.button("🔄 처음부터 다시 하기 (Reset)"):
        st.session_state.step = 1
        st.session_state.config = {'defense': None, 'skill': None, 'pace': None}
        st.rerun()

# ---------------------------------------------------------
# 4. 메인 화면 로직
# ---------------------------------------------------------
st.title("🛡️ AI Labor Environment Architect")
st.markdown("""
> 당신은 콜센터 AI 시스템의 총괄 아키텍트입니다.  
> **'효율성(속도)'**과 **'노동자 보호(지속가능성)'** 사이에서, 어떤 시스템을 구축하시겠습니까?
""")
st.divider()

# === STEP 1: 감정 노동 방어 ===
if st.session_state.step == 1:
    st.subheader("Step 1. 입력 필터링 (Emotional Defense)")
    st.info("Q. 상담원은 하루 수십 번의 폭언과 고성에 노출됩니다. AI가 고객의 목소리를 어떻게 전달해야 할까요?")
    
    defense_choice = st.radio(
        "음성 처리 방식을 선택하세요:",
        [
            "A. [Raw-Audio] 고객의 목소리(톤, 크기)를 100% 생생하게 전달 (뉘앙스 파악 용이, 감정 타격 큼)",
            "B. [Safe-Voice] 욕설/고성은 '삐-' 처리하고, 격앙된 목소리는 차분한 톤으로 변조 (감정 보호, 미세 뉘앙스 놓침)"
        ],
        index=None,
        key="radio_defense"
    )
    
    if st.button("결정 후 다음 단계로 →"):
        if defense_choice:
            st.session_state.config['defense'] = defense_choice
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("옵션을 선택해주세요.")

# === STEP 2: 스킬 및 자율성 ===
elif st.session_state.step == 2:
    st.subheader("Step 2. 업무 지원 방식 (Skill & Autonomy)")
    st.info("Q. 상담원이 자신의 능력을 키우며 일하게 할까요, 아니면 편하게 시키는 대로 하게 할까요?")
    
    skill_choice = st.radio(
        "AI 어시스턴트의 모드를 선택하세요:",
        [
            "A. [GPS Mode] '지금 이렇게 말하세요'라고 정답 스크립트를 화면에 띄움 (초보자도 즉시 처리 가능, 숙련도 정체)",
            "B. [Coach Mode] 고객의 의도를 분석해 '협상 전략'과 '핵심 정보'만 제공, 발화는 상담원이 구성 (전문성 향상, 처리 시간 증가)"
        ],
        index=None,
        key="radio_skill"
    )
    
    if st.button("결정 후 다음 단계로 →"):
        if skill_choice:
            st.session_state.config['skill'] = skill_choice
            st.session_state.step = 3
            st.rerun()
        else:
            st.warning("옵션을 선택해주세요.")

# === STEP 3: 휴식과 리듬 ===
elif st.session_state.step == 3:
    st.subheader("Step 3. 업무 배정 로직 (Work Pacing)")
    st.info("Q. AI가 상담 종료 후 다음 콜을 언제 연결할지 결정합니다.")
    
    pace_choice = st.radio(
        "배차(Dispatch) 알고리즘을 선택하세요:",
        [
            "A. [Max-Throughput] 상담 종료 버튼을 누르는 즉시 대기콜 연결 (대기시간 0초, 생산성 극대화)",
            "B. [Stress-Based] 방금 통화의 감정 강도가 높았다면, 30초~1분의 '강제 쿨다운(휴식)' 부여 (번아웃 방지, 대기시간 증가)"
        ],
        index=None,
        key="radio_pace"
    )
    
    if st.button("설계 완료 및 결과 보기 →"):
        if pace_choice:
            st.session_state.config['pace'] = pace_choice
            st.session_state.step = 4
            st.rerun()
        else:
            st.warning("옵션을 선택해주세요.")

# === STEP 4: 결과 시뮬레이션 ===
elif st.session_state.step == 4:
    st.subheader("🖥️ 설계 결과 시뮬레이션")
    
    # 데이터 파싱
    c_defense = st.session_state.config.get('defense', '')
    c_skill = st.session_state.config.get('skill', '')
    c_pace = st.session_state.config.get('pace', '')
    
    is_safe = "Safe" in c_defense
    is_coach = "Coach" in c_skill
    is_stress = "Stress" in c_pace
    
    # 점수 로직 (간단하게)
    score_efficiency = 0
    score_wellbeing = 0
    
    # 1. Defense
    if is_safe: score_wellbeing += 40
    else: score_efficiency += 30
    
    # 2. Skill
    if is_coach: score_wellbeing += 30
    else: score_efficiency += 40
    
    # 3. Pace
    if is_stress: score_wellbeing += 30
    else: score_efficiency += 30

    # 화면 분할
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 시스템 예측 지표")
        
        st.write("🏭 **생산성/효율 (Efficiency)**")
        st.progress(min(score_efficiency, 100) / 100)
        st.caption(f"Score: {score_efficiency} - (높을수록 회사의 단기 수익이 증가합니다)")
        
        st.write("❤️ **노동자 보호/성장 (Well-being)**")
        st.progress(min(score_wellbeing, 100) / 100)
        st.caption(f"Score: {score_wellbeing} - (높을수록 상담원의 근속연수와 숙련도가 증가합니다)")

        st.info(f"""
        **[최종 설계 요약]**
        - 🎧 음성 처리: {"안전 모드(Safe)" if is_safe else "원본 모드(Raw)"}
        - 🧠 업무 지원: {"코치 모드(Coach)" if is_coach else "내비게이션 모드(GPS)"}
        - ☕ 휴식 배정: {"스트레스 기반 휴식" if is_stress else "무한 연결(Max)"}
        """)

    with col2:
        st.markdown("### 💬 상담원 현장 반응")
        
        # 시나리오별 반응
        if score_wellbeing >= 80:
            st.success("""
            **😀 베테랑 상담원 김지영 (7년차)**
            "와, 이번 업데이트 정말 좋아요! 특히 욕설 필터링 덕분에 심장이 덜 떨려요.
            AI가 무조건 답을 주는 게 아니라 팁만 주니까, 제가 스스로 해결했다는 성취감도 들고요.
            회사 다닐 맛이 좀 나네요!"
            """)
        elif score_wellbeing <= 40:
            st.error("""
            **😥 신입 상담원 이민수 (3개월차)**
            "효율도 좋지만... 사람이 기계 부품이 된 것 같아요.
            고객이 소리지르는 거 그대로 다 들어야 하고, 숨 쉴 틈도 없이 다음 전화가 오니까
            화장실 갈 시간도 없어요. 이대로면 다음 달에 그만둬야 할 것 같습니다."
            """)
        else:
            st.warning("""
            **😐 중견 상담원 박상훈 (3년차)**
            "나쁘진 않은데... 
            어떤 기능은 도움이 되지만, 여전히 업무 강도는 세네요.
            조금 더 우리 입장을 고려해줬으면 좋겠습니다. 특히 휴식 시간은 좀 더 필요해요."
            """)
            
    st.divider()
    if st.button("🔄 실험 종료 및 다시 시작"):
        st.session_state.step = 1
        st.session_state.config = {'defense': None, 'skill': None, 'pace': None}
        st.rerun()

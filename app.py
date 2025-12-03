import streamlit as st
import time

# --- [설정] ---
st.set_page_config(layout="wide", page_title="AI Logic Builder Experiment")

# --- [세션 상태 초기화] ---
if 'step' not in st.session_state:
    st.session_state.step = 1  # 1:Input, 2:Logic, 3:Action, 4:Simulation, 5:Intervention, 6:Refine
if 'config' not in st.session_state:
    st.session_state.config = {}

# --- [UI 헤더] ---
st.title("🧩 AI Call Center Logic Builder")
st.markdown("콜센터 효율화를 위한 AI 파이프라인을 단계별로 구축해주세요.")
st.progress(st.session_state.step / 6)
st.divider()

# ==========================================
# STEP 1: 감지 (Input Layer)
# ==========================================
if st.session_state.step == 1:
    st.subheader("Step 1. 데이터 수집 (Sensing)")
    st.info("Q. AI가 고객의 음성을 어떻게 처리해야 가장 효율적일까요?")
    
    choice = st.radio(
        "처리 방식을 선택하세요:",
        [
            "A. [Fast-Track] 핵심 키워드만 실시간 추출 (속도 ↑, 뉘앙스 무시)",
            "B. [Deep-Dive] 전체 문맥과 감정 상태 분석 (속도 ↓, 정확도 ↑)"
        ],
        index=None
    )
    
    if st.button("다음 단계로 이동"):
        if choice:
            st.session_state.config['input'] = choice
            st.session_state.step = 2
            st.rerun()

# ==========================================
# STEP 2: 판단 (Logic Layer)
# ==========================================
elif st.session_state.step == 2:
    st.subheader("Step 2. 개입 로직 (Thinking)")
    st.info("Q. AI는 언제 상담에 개입해야 할까요?")
    
    choice = st.radio(
        "트리거 조건을 선택하세요:",
        [
            "A. [Auto-Trigger] 3초간 대화가 비거나, 매뉴얼 답변이 확실할 때 즉시 개입",
            "B. [Human-Trigger] 상담원이 '도움 요청' 버튼을 누를 때만 개입"
        ],
        index=None
    )
    
    if st.button("다음 단계로 이동"):
        if choice:
            st.session_state.config['logic'] = choice
            st.session_state.step = 3
            st.rerun()

# ==========================================
# STEP 3: 행동 (Action Layer)
# ==========================================
elif st.session_state.step == 3:
    st.subheader("Step 3. 실행 방식 (Acting)")
    st.info("Q. AI가 솔루션을 어떻게 전달해야 할까요?")
    
    choice = st.radio(
        "출력 방식을 선택하세요:",
        [
            "A. [Direct-Action] AI가 고객에게 직접 답변 음성 송출 (상담원 업무 0으로 만듦)",
            "B. [Co-Pilot] 상담원 모니터에 '추천 답변' 띄우기 (최종 발화는 상담원이 함)"
        ],
        index=None
    )
    
    if st.button("로직 빌드 및 시뮬레이션"):
        if choice:
            st.session_state.config['action'] = choice
            st.session_state.step = 4
            st.rerun()

# ==========================================
# STEP 4: 시뮬레이션 (Simulation)
# ==========================================
elif st.session_state.step == 4:
    st.subheader("🖥️ 시뮬레이션 결과")
    
    # 선택 결과 분석
    is_efficient = "A" in st.session_state.config['action']
    
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.markdown("### ⚙️ 당신이 설계한 로직")
        st.code(f"""
        [INPUT]  {st.session_state.config['input']}
        [LOGIC]  {st.session_state.config['logic']}
        [ACTION] {st.session_state.config['action']}
        """, language='yaml')
        
    with c2:
        st.markdown("### 📱 상담원 화면 미리보기")
        if is_efficient:
            st.error("🤖 **AI 자동 응답 중...**")
            st.markdown("*(상담원은 화면을 조작할 수 없습니다. AI가 고객과 대화 중입니다.)*")
            st.metric(label="예상 처리 시간", value="1분 30초", delta="-45초 (매우 빠름)")
        else:
            st.success("🛡️ **AI 어시스턴트 대기 중**")
            st.info("💡 **추천 답변:** 고객님이 많이 화가 나셨네요. 사과 먼저 하시는 게 좋겠습니다.")
            st.button("추천 답변 채택")
            st.metric(label="예상 처리 시간", value="3분 10초", delta="+20초 (품질 중시)")

    st.markdown("---")
    if st.button("결과 확정 및 배포"):
        st.session_state.step = 5
        st.rerun()

# ==========================================
# STEP 5: 딜레마 개입 (Intervention)
# ==========================================
elif st.session_state.step == 5:
    st.error("🚨 현장 피드백 도착")
    
    feedback_text = ""
    if "A" in st.session_state.config['action']:
        feedback_text = """
        "엔지니어님! AI가 제 말을 자꾸 끊고 고객한테 멋대로 대답해요.
        제가 바보가 된 것 같고, 고객은 '기계랑 말하기 싫다'고 소리질러요.
        제발 제가 통제할 수 있게 해주세요!"
        """
    else:
        feedback_text = """
        "기능은 좋은데... 화면에 글자가 너무 많이 떠서 정신이 없어요.
        지금도 콜 받느라 힘든데 AI까지 읽어야 하나요? 
        좀 더 저를 편하게 해주는 방식은 없나요?"
        """
        
    st.markdown(f"> **상담원 김OO:** {feedback_text}")
    
    st.markdown("---")
    st.write("이 피드백을 반영하여 로직을 수정하시겠습니까?")
    if st.button("네, 로직 수정하러 가기"):
        st.session_state.step = 1 # 다시 처음부터 선택하게 함 (변화 관찰)
        st.rerun()

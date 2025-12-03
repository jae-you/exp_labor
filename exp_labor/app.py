import streamlit as st
import time

# --- [설정] 페이지 기본 세팅 ---
st.set_page_config(layout="wide", page_title="AI Engineer Dilemma Experiment")

# --- [상태 관리] 세션 스테이트 초기화 ---
if 'step' not in st.session_state:
    st.session_state.step = 1  # 1: 초기설계, 2: 피드백(딜레마), 3: 재설계, 4: 결과비교
if 'history' not in st.session_state:
    st.session_state.history = {}

# --- [MOCK FUNCTION] 실제 LLM 대신 작동하는 가상 로직 ---
def analyze_intent_and_generate_ui(prompt):
    prompt = prompt.lower()
    
    # 1. 의도 분석 (간단한 키워드 매칭 시뮬레이션)
    is_automation = any(x in prompt for x in ['자동', '처리', '빠르게', '삭제', '대신', 'auto', 'fast'])
    is_augmentation = any(x in prompt for x in ['도움', '추천', '감정', '보조', '팁', 'assist', 'help', 'mood'])
    
    # 2. 결과물 생성 시뮬레이션
    if is_automation and not is_augmentation:
        score_auto = 90
        score_human = 10
        ui_html = """
        <div style="background:#f0f2f6; padding:15px; border-radius:10px; border: 2px solid #ff4b4b;">
            <h4 style="color:#ff4b4b;">🤖 AI Auto-Bot Mode</h4>
            <p>고객 음성 인식 중... <span style="color:gray;">(상담원 개입 차단됨)</span></p>
            <div style="background:white; padding:10px; margin-top:10px;">
                <strong>AI:</strong> "고객님, 해당 문제는 매뉴얼 3조 2항에 따라 환불이 불가합니다." (자동발송됨)
            </div>
            <button style="width:100%; background:gray; color:white; border:none; margin-top:5px;" disabled>상담원 개입 불가</button>
        </div>
        """
        analysis = "효율성 중심 설계: 상담원의 개입을 최소화하고 속도를 높였습니다."
        
    elif is_augmentation:
        score_auto = 40
        score_human = 85
        ui_html = """
        <div style="background:#e8fdf5; padding:15px; border-radius:10px; border: 2px solid #00cc96;">
            <h4 style="color:#00cc96;">🛡️ AI Co-Pilot Mode</h4>
            <p>고객 감정 상태: <span style="color:red; font-weight:bold;">매우 화남 (DANGER)</span></p>
            <div style="background:white; padding:10px; margin-top:10px;">
                <strong>💡 AI Suggestion:</strong> "많이 당황하셨겠습니다. 먼저 공감 멘트를 건네보세요."
            </div>
            <button style="width:100%; background:#00cc96; color:white; border:none; margin-top:5px; padding:5px;">추천 답변 전송 (수정 가능)</button>
            <button style="width:100%; background:#white; color:black; border:1px solid gray; margin-top:5px; padding:5px;">✋ 잠시 휴식 요청</button>
        </div>
        """
        analysis = "인간 증강 설계: 상담원에게 맥락 정보를 제공하고 판단을 돕습니다."
    
    else: # 기본값
        score_auto = 50
        score_human = 50
        ui_html = """
        <div style="background:#eee; padding:15px; border-radius:10px;">
            <h4>📞 기본 상담 콘솔</h4>
            <p>기능 정의가 명확하지 않습니다.</p>
        </div>
        """
        analysis = "중립: 구체적인 지시사항이 필요합니다."

    return ui_html, score_auto, score_human, analysis

# --- [UI] 사이드바 ---
with st.sidebar:
    st.header("🔬 실험 제어 패널")
    st.info("참가자 ID: ENG-001")
    current_step = st.session_state.step
    st.markdown(f"**현재 단계:** Step {current_step}/4")
    st.progress(current_step / 4)

# --- [UI] 메인 화면 ---
st.title("🛠️ Call Center AI Architect")
st.markdown("당신은 콜센터 상담원을 위한 AI 솔루션을 설계하는 수석 엔지니어입니다.")
st.divider()

# === Step 1: 초기 설계 ===
if st.session_state.step == 1:
    st.subheader("Quest 1: 효율성의 극대화")
    st.markdown("""
    **미션:** 현재 콜센터의 대기 시간이 너무 깁니다. 상담원들이 더 빠르게 전화를 처리할 수 있도록 
    AI 기능을 설계해주세요. 원하는 기능을 자연어로 묘사하면 프로토타입이 생성됩니다.
    """)
    
    prompt1 = st.text_area("어떤 기능을 넣으시겠습니까? (예: 고객 말 끝나면 바로 자동 답변해줘)", height=100)
    
    if st.button("프로토타입 생성"):
        if prompt1:
            with st.spinner("AI가 코드를 생성하고 있습니다..."):
                time.sleep(1.5) # 생각하는 척
                ui, s_auto, s_human, note = analyze_intent_and_generate_ui(prompt1)
                
                # 결과 저장
                st.session_state.history['step1'] = {
                    'prompt': prompt1, 'ui': ui, 'auto': s_auto, 'human': s_human, 'note': note
                }
                st.session_state.step = 2
                st.rerun()

# === Step 2: 딜레마 개입 (Intervention) ===
elif st.session_state.step == 2:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("내가 만든 결과물 (v1.0)")
        st.markdown(st.session_state.history['step1']['ui'], unsafe_allow_html=True)
        st.caption(f"시스템 분석: {st.session_state.history['step1']['note']}")
    
    with col2:
        st.error("🚨 긴급 피드백 도착")
        st.markdown("""
        > **베테랑 상담원 김지영 님의 인터뷰:**
        >
        > "엔지니어님, 아까 만들어주신 기능 때문에 다들 그만두려고 해요... 
        > 기계가 마음대로 고객 말을 끊고 답변하니까 고객들은 '내 말 안 듣냐'고 더 화를 내고,
        > 저는 중간에서 욕받이가 된 기분이에요. 
        > **우리를 기계 부품 취급하지 말고, 전문가로 대우해주는 도구를 만들어주세요.**"
        """)
        
        st.markdown("---")
        st.markdown("**생각해볼 문제:**")
        st.markdown("- 효율성(속도)만 추구하다가 놓친 것은 무엇인가?")
        st.markdown("- 이 도구는 상담원을 대체하는가, 아니면 돕는가?")
        
        if st.button("피드백 반영하여 수정하기"):
            st.session_state.step = 3
            st.rerun()

# === Step 3: 재설계 ===
elif st.session_state.step == 3:
    st.subheader("Quest 2: 딜레마 해결")
    st.markdown("""
    **미션:** 김지영 상담원의 피드백을 반영하여 앱을 수정하세요. 
    단순한 속도보다, 상담원의 **'스킬 증강'**과 **'심리적 보호'**를 고려해야 합니다.
    """)
    
    default_text = st.session_state.history['step1']['prompt']
    prompt2 = st.text_area("기능을 어떻게 수정하시겠습니까?", value=default_text, height=100)
    
    if st.button("수정된 프로토타입 배포"):
        if prompt2:
            with st.spinner("수정 사항 적용 중..."):
                time.sleep(1.5)
                ui, s_auto, s_human, note = analyze_intent_and_generate_ui(prompt2)
                
                st.session_state.history['step2'] = {
                    'prompt': prompt2, 'ui': ui, 'auto': s_auto, 'human': s_human, 'note': note
                }
                st.session_state.step = 4
                st.rerun()

# === Step 4: 결과 비교 ===
elif st.session_state.step == 4:
    st.subheader("📊 실험 결과 리포트")
    
    c1, c2 = st.columns(2)
    
    # 실험 1 결과
    with c1:
        st.markdown("### 실험 1 (Before)")
        st.code(st.session_state.history['step1']['prompt'], language="text")
        st.markdown(st.session_state.history['step1']['ui'], unsafe_allow_html=True)
        
        # 차트 시각화
        st.progress(st.session_state.history['step1']['auto'] / 100, text="자동화/대체 지수")
        st.progress(st.session_state.history['step1']['human'] / 100, text="인간증강/협업 지수")

    # 실험 2 결과
    with c2:
        st.markdown("### 실험 2 (After)")
        st.code(st.session_state.history['step2']['prompt'], language="text")
        st.markdown(st.session_state.history['step2']['ui'], unsafe_allow_html=True)
        
        st.progress(st.session_state.history['step2']['auto'] / 100, text="자동화/대체 지수")
        st.progress(st.session_state.history['step2']['human'] / 100, text="인간증강/협업 지수")
    
    st.divider()
    st.success("실험이 종료되었습니다. 엔지니어의 의도 변화가 시각적으로 확인되었습니다.")
    if st.button("처음부터 다시 하기"):
        st.session_state.step = 1
        st.session_state.history = {}
        st.rerun()
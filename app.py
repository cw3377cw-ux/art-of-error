import streamlit as st
from openai import OpenAI

# 1. 페이지 설정 및 아카데믹 그린 디자인
st.set_page_config(page_title="위풍당당 실수 연구소", page_icon="🎓", layout="centered")

st.markdown("""
    <style>
    .main-title { font-size: 34px; font-weight: bold; color: #1E3D2F; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 15px; color: #557A67; text-align: center; margin-bottom: 30px; }
    .cert-box { border: 5px double #2E5A44; padding: 30px; background-color: #FAFBFB; border-radius: 10px; text-align: center; margin-top: 20px; }
    .cert-title { font-size: 24px; font-weight: bold; color: #1E3D2F; margin-bottom: 20px; letter-spacing: 2px; }
    .quest-box { background-color: #EEF7F2; border: 1px solid #CCE7D9; padding: 20px; border-radius: 8px; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎓 위풍당당 실수 연구소</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">나의 실수를 당당하게 긍정하고(Amor Fati), 자신만의 성장 경로(Rhizome)를 탐색하는 교실</div>', unsafe_allow_html=True)

# 2. 사이드바 설정 (금고에 키가 없을 때를 대비한 백업용 유지)
with st.sidebar:
    st.header("🔑 시스템 설정")
    st.success("시스템 API Key가 안전하게 연동되어 있습니다.")

# 3. 세션 상태 초기화 (인터랙티브 화면 전환용 치트키)
if "step" not in st.session_state:
    st.session_state.step = 1
if "ai_analysis" not in st.session_state:
    st.session_state.ai_analysis = ""
if "choices" not in st.session_state:
    st.session_state.choices = []
if "philosophical_question" not in st.session_state:
    st.session_state.philosophical_question = ""

# ----------------- [STEP 1: 입력 화면] -----------------
if st.session_state.step == 1:
    st.subheader("📝 오늘의 실수 등록하기")
    student_name = st.text_input("당신의 멋진 이름(또는 별명)을 적어주세요!", placeholder="예: 홍길동")

    category_choice = st.selectbox(
        "오늘 교실이나 공부 중에 어떤 실수를 마주했나요?",
        ["수학/연산 실수", "국어/지문 오해", "사회/과학 개념 혼동", "수행평가 및 조별 과제 중 아쉬운 실수", "친구 관계 및 학급 생활 속 행동 실수", "기타 (직접 입력)"]
)

    if category_choice == "기타 (직접 입력)":
        category = st.text_input("어떤 종류의 실수인지 간단하게 써주세요", placeholder="여기에 실수의 종류를 입력하세요")
    else:
        category = category_choice

    error_details = st.text_area(
        "저지른 실수나 당시의 상황을 솔직하게 나누어 주세요.",
        placeholder="예시: 수학 단원평가 풀다가 더하기를 빼기로 잘못 보고 풀어서 틀렸어요. 너무 속상해요."
)

    submit_btn = st.button("실수 연구소에 가치 분석 요청하기 🚀")

    if submit_btn:
        if not student_name or not error_details:
            st.warning("이름이랑 실수를 마주한 상황을 빈칸 없이 입력해줘!")
        else:
            with st.spinner("연구소장 AI가 당신의 실수를 위대한 자산으로 재해석하는 중..."):
                try:
                    client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=st.secrets["GROQ_API_KEY"])
                    
# 100% 자연스러운 초등 맞춤형 동적 생성 시스템 프롬프트
                system_prompt = """
                너는 초등학생들이 학교생활과 공부 중에 저지른 '실수'를 성장의 비타민으로 바꿔주는 다정하고 유쾌한 '위풍당당 실수 연구소장 AI'야.
                
                [핵심 가치 지도 철학 (주의: '아모르 파티', '리좀' 이라는 단어는 답변에 절대 직접 노출하지 말 것)]
                1. 운명애의 관점: 아이가 실수를 부끄러워하거나 숨기지 않고, "이 실수가 나를 더 단단하게 성장시킬 멋진 계기야!"라며 스스로를 당당하게 긍정하도록 마음을 촉촉하게 어루만져줘.
                2. 다양성과 탈중심화 관점: 학교가 정한 '단 하나의 정답 경로'에서 미끄러진 아이의 실수를 절대 '틀린 것'이나 '실패'로 규정하지 말고, '생각이 사방으로 자유롭게 뻗어 나가는 창의적인 오작동이자 가치 있는 탐험'으로 따뜻하게 재해석해 주어야 해.
                
                [답변 작성 규칙 - 부자연스러운 말투 전면 수정]
                1. 대상 독자: 초등학교 3~6학년 어린이가 읽고 바로 감동받거나 웃을 수 있도록 친근하고 다정하면서도 칭찬을 아끼지 않는 격려조를 유지해줘.
                2. 금지 사항: "~하는 대신 ~해라", "~하지 말고 ~하자" 같은 번역기 말투나 앞뒤 문맥이 꼬이는 문장은 절대 금지. "~야", "~해보는 건 어떨까?", "~해보자!" 같은 자연스러운 구어체로 작성할 것. "이채운아, 넌~" 처럼 기계적으로 이름을 반복하며 훈계하지 마.
                3. 필수 포함 요소 (구조를 명확히 나누어 줄바꿈할 것):
                   - [실수의 반전 가치]: 아이가 입력한 구체적인 실수를 바탕으로, 왜 그 행동이 '뇌가 엄청 열심히 새로운 길을 탐험하다 생긴 멋진 발자국'인지 인문학적으로 칭찬 및 해석해줘.
                   - [나만의 행동 지침 3가지]: 아이가 입력한 실수 내용(수학, 국어, 친구 관계 등)에 100% 매칭되는 독창적인 해결책 3가지를 제안해줘. 고정된 예시를 쓰지 말고, 아이의 구체적인 상황을 바탕으로 아래 3가지 성향에 맞는 기발한 이름을 실시간으로 작명해서 자연스러운 행동 요령을 적어줘.
                     * 🔵 [정면 돌파형 기사] (실수를 정면으로 부딪쳐 해결하는 멋진 미션 제안)
                     * 🟢 [침착한 마법사] (마음을 가라앉히고 풀이 과정이나 감정을 다스리는 조용한 미션 제안)
                     * 🟣 [생각 돋보기 탐험가] (실수를 통해 발견한 새로운 생각이나 재미를 즐기는 창의적 미션 제안)
                """
                    
                    user_content = f"이름: {student_name}\n분류: {category}\n실수 기술: {error_details}"
                    
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_content}],
                        temperature=0.7
                    )
                    
                    raw_text = response.choices[0].message.content
                    
                    # 간단한 텍스트 파싱 처리로 데이터를 세션에 저장
                    st.session_state.ai_analysis = raw_text
                    st.session_state.student_name = student_name
                    st.session_state.category = category
                    st.session_state.step = 2
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"에러 발생! Secrets 설정을 확인해봐, 어이: {e}")

# ----------------- [STEP 2: 인터랙티브 선택 화면] -----------------
elif st.session_state.step == 2:
    st.subheader(f"🎓 {st.session_state.student_name} 연구원님을 위한 맞춤형 분석 완료!")
    
    # 1단계 AI 분석 리포트 보여주기
    st.markdown(f"""
    <div class="cert-box" style="text-align: left;">
        <div class="cert-title" style="text-align: center;">🔬 실수의 인문학적 재해석</div>
        <p style="line-height: 1.7; color: #2C3E50; white-space: pre-wrap;">{st.session_state.ai_analysis}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="quest-box"><b>🧭 소장님의 퀘스트:</b> 자, 이 실수의 무대 위에서 당신은 이제 어떤 생각의 갈래를 선택해 개척해 나가겠습니까? 아래에서 마음에 드는 성장의 길을 하나 선택해 보세요!</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔵 갈래 A 선택"):
            st.session_state.final_choice = "용기 있게 정면으로 부딪히며 탐험하는 길"
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("🟢 갈래 B 선택"):
            st.session_state.final_choice = "침착하게 멈춰 서서 나를 돌아보는 깊은 샘물의 길"
            st.session_state.step = 3
            st.rerun()
    with col3:
        if st.button("🟡 갈래 C 선택"):
            st.session_state.final_choice = "친구들과 지혜를 나누며 함께 발을 맞춰 걷는 길"
            st.session_state.step = 3
            st.rerun()

# ----------------- [STEP 3: 최종 인증서 발행 및 철학 질문 발급] -----------------
elif st.session_state.step == 3:
    st.success("축하합니다! 자신만의 주체적인 성장 경로를 결정하셨습니다.")
    
    cert_html = f"""
<div class="cert-box">
    <div class="cert-title">📜 위풍당당 실수 분석 인증서</div>
    <p><b>연구원 성명:</b> {st.session_state.student_name} 어린이</p>
    <p><b>선택한 성장의 갈래:</b> ✨ {st.session_state.final_choice} ✨</p>
    <hr style="border: 1px dashed #2E5A44;">
    <div style="text-align: left; line-height: 1.7; color: #2C3E50; padding: 10px;">
        당신은 타인이 정해준 획일적인 정답에 의존하지 않고, 스스로 사유하여 자신만의 독창적인 해결 경로를 개척해 냈습니다. 이에 위풍당당 연구소는 당신의 위대한 실수가 빛나는 자산이 되었음을 공식 인증합니다.
    </div>
    <hr style="border: 1px dashed #2E5A44;">
    <p style="font-weight: bold; color: #E67E22; font-size: 13pt; margin-top: 15px;">"실수는 틀린 것이 아니라, 새로운 길을 발견한 것입니다."</p>
    <p style="font-size: 13px; color: #7F8C8D; margin-top: 5px;">위풍당당 실수 연구소 | 소장 AI 배상</p>
</div>
"""
    st.markdown(cert_html, unsafe_allow_html=True)
    st.balloons()
    
    if st.button("처음으로 돌아가기 🔄"):
        st.session_state.step = 1
        st.rerun()

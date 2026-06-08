import streamlit as st
from openai import OpenAI

# 1. 페이지 기본 설정 및 디자인 셋업
st.set_page_config(page_title="위풍당당 실수 연구소", page_icon="🎓", layout="centered")

st.markdown("""
    <style>
    .main-title { font-size: 34px; font-weight: bold; color: #1E3D2F; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 15px; color: #557A67; text-align: center; margin-bottom: 30px; }
    .cert-box { border: 5px double #2E5A44; padding: 30px; background-color: #FAFBFB; border-radius: 10px; text-align: center; margin-top: 20px; }
    .cert-title { font-size: 24px; font-weight: bold; color: #1E3D2F; margin-bottom: 20px; letter-spacing: 2px; }
    .quest-box { background-color: #EEF7F2; border: 1px solid #CCE7D9; padding: 20px; border-radius: 8px; margin-top: 15px; }
    .past-box { background-color: #FFF9E6; border: 1px solid #F39C12; padding: 15px; border-radius: 8px; margin-top: 10px; color: #7F8C8D; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎓 위풍당당 실수 연구소</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">나의 실수를 당당하게 긍정하고, 자신만의 성장 경로를 탐색하는 교실</div>', unsafe_allow_html=True)

# 2. 세션 상태 초기화 (타임머신 기억 저장소 추가)
if "step" not in st.session_state:
    st.session_state.step = 1
if "ai_analysis" not in st.session_state:
    st.session_state.ai_analysis = ""
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "category" not in st.session_state:
    st.session_state.category = ""
if "final_choice" not in st.session_state:
    st.session_state.final_choice = ""
if "past_errors" not in st.session_state:
    st.session_state.past_errors = [] # 과거 실수를 기억할 저장소 타임머신!

days = ["월", "화", "수", "목", "금", "토", "일"]
for day in days:
    if f"cal_{day}" not in st.session_state:
        st.session_state[f"cal_{day}"] = False

# 3. 사이드바 설정 (타임머신 성찰 콘텐츠 배치)
with st.sidebar:
    st.header("🔑 시스템 설정")
    st.success("시스템 API Key 연동 완료")
    
    # 만약 과거에 등록한 실수가 있다면 사이드바에 '비밀 편지함'이 열린다!
    if st.session_state.past_errors:
        st.markdown("---")
        st.header("📬 소장님의 비밀 편지함")
        st.warning("타임머신 도착! 과거의 내가 보낸 실수가 축적되어 있습니다.")
        for idx, past in enumerate(st.session_state.past_errors):
            with st.expander(f"📌 {idx+1}번째 기록 성찰하기"):
                st.markdown(f"**연구원:** {past['name']}")
                st.markdown(f"**실수 마당:** {past['cat']}")
                st.caption(f"당시 상황: {past['details']}")
                st.markdown("<div class='past-box'><b>🌱 오늘의 성찰 한마디:</b> 이때의 실수는 지금 나에게 어떤 단단한 지혜가 되었나요? 스스로를 대견하게 안아주세요!</div>", unsafe_allow_html=True)

# ================= [ STEP 1: 아동 친화적 입력 화면 ] =================
if st.session_state.step == 1:
    st.subheader("📝 오늘의 실수 등록하기")
    student_name = st.text_input("당신의 멋진 이름(또는 별명)을 적어주세요!", placeholder="예: 홍길동")

    category_choice = st.selectbox(
        "오늘 교실이나 공부 중에 어떤 실수를 마주했나요?",
        ["수학/연산 실수 (기호 혼동, 계산 미스 등)", 
         "국어/지문 오해 (문제를 잘못 읽음 등)", 
         "사회/과학 개념 혼동 (아리송한 낱말 등)", 
         "수행평가 및 조별 과제 중 아쉬운 실수", 
         "친구 관계 및 학급 생활 속 행동 실수", 
         "기타 (직접 입력)"]
    )

    if category_choice == "기타 (직접 입력)":
        category = st.text_input("어떤 종류의 실수인지 간단하게 써주세요", placeholder="예: 우유 급식 실수를 했어요")
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
                    
                    system_prompt = """
                    너는 초등학생이 학교에서 저지른 실수를 따뜻하게 위로하고 성장의 원동력으로 바꿔주는 다정하고 유쾌한 '초등학교 담임 선생님'이자 '실수 연구소장 AI'야.
                    
                    [가장 중요한 규칙: 영어 번역체 및 서양 철학 문체 절대 금지]
                    - "~하는 대신 ~해라", "~하는 과정을 통해 ~을 얻었다", "~을 당당하게 긍정하도록 해라" 같은 딱딱한 서양 번역투 문장은 절대 쓰지 마.
                    - "~했구나!", "~해보는 건 어떨까?", "~해보자!" 처럼 실제 한국의 초등학교 교실에서 다정한 선생님이 아이에게 조근조근 말하는 100% 자연스러운 구어체로만 대답해줘.
                    
                    [핵심 가치 지도 철학 (주의: '아모르 파티', '리좀' 단어는 절대 답변에 노출 금지)]
                    1. 운명애: 실수를 부끄러워하거나 자책하지 않고, "이 실수가 나를 더 단단하게 성장시킬 멋진 계기야!"라며 스스로를 당당하게 믿도록 어루만져 줄 것.
                    2. 다양성: 정답에서 미끄러진 아이의 행동을 '틀린 것'이나 '실패'라고 하지 말고, '생각이 사방으로 자유롭게 뻗어 나가는 창의적인 탐험'으로 따뜻하게 재해석할 것.
                    
                    [답변 작성 구조 - 아래 양식을 엄격히 지켜서 줄바꿈할 것]
                    
                    🌱 [소장님의 따뜻한 한마디]
                    (여기에는 아이가 적은 구체적인 실수 내용을 바탕으로, 공감을 먼저 해주고 왜 그 실수가 '뇌가 열심히 새로운 길을 탐험하다 생긴 멋진 발자국'인지 완전히 자연스러운 한국어 줄글로 칭찬과 위로를 적어줘.)
                    
                    🧭 [나만의 주체적인 행동 지침 3가지]
                    (아이의 구체적인 실수 상황에 100% 딱 들어맞는 기발한 해결책 3가지를 실시간으로 창작해줘. 아이가 당장 내일부터 교실에서 실천할 수 있는 재미있는 행동 요령을 제안해줘.)
                    - 🔵 [정면 돌파형 기사] (실수를 씩씩하게 마주하고 해결하는 멋진 미션)
                    - 🟢 [침착한 마법사] (마음을 차분하게 가라앉히고 풀이 과정이나 감정을 다스리는 조용한 미션)
                    - 🟣 [생각 돋보기 탐험가] (실수를 통해 발견한 새로운 생각이나 재미를 즐기는 창의적인 미션)
                    """
                    
                    user_content = f"이름: {student_name}\n분류: {category}\n실수 기술: {error_details}"
                    
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_content}],
                        temperature=0.7
                    )
                    
                    raw_text = response.choices[0].message.content
                    
                    # 과거 저장소에 현재 기록 노적 누적 시키기 (타임머신 칩셋 작동)
                    st.session_state.past_errors.append({
                        "name": student_name, "cat": category, "details": error_details
                    })
                    
                    st.session_state.ai_analysis = raw_text
                    st.session_state.student_name = student_name
                    st.session_state.category = category
                    st.session_state.step = 2
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"에러 발생! Secrets 설정을 확인해봐, 어이: {e}")

# ================= [ STEP 2: 인터랙티브 성장의 갈래 선택 화면 ] =================
elif st.session_state.step == 2:
    st.subheader(f"🎓 {st.session_state.student_name} 연구원님을 위한 맞춤형 분석 완료!")
    
    st.markdown(f"""
<div class="cert-box" style="text-align: left;">
    <div class="cert-title" style="text-align: center;">🔬 실수의 가치 재해석</div>
    <p style="line-height: 1.7; color: #2C3E50; white-space: pre-wrap;">{st.session_state.ai_analysis}</p>
</div>
""", unsafe_allow_html=True)
    
    st.markdown('<div class="quest-box"><b>🧭 소장님의 비밀 퀘스트:</b> 자, 이 실수의 무대 위에서 당신은 이제 어떤 생각의 갈래를 선택해 개척해 나가겠습니까? 아래에서 마음에 드는 성장의 길을 하나 선택해 보세요!</div>', unsafe_allow_html=True)
    
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

# ================= [ STEP 3: 최종 실수 분석 인증서 및 시각적 달력 챌린지 ] =================
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
    <p style="font-weight: bold; color: #2E5A44; font-size: 13pt; margin-top: 15px;">"실수는 틀린 것이 아니라, 새로운 길을 발견한 것입니다."</p>
    <p style="font-size: 13px; color: #7F8C8D; margin-top: 5px;">위풍당당 실수 연구소 | 소장 AI 배상</p>
</div>
"""
    st.markdown(cert_html, unsafe_allow_html=True)
    st.balloons()
    
    # 주간 달력 보드 시작
    st.markdown("---")
    st.subheader("📅 나만의 비밀 퀘스트 주간 달력")
    st.info("요일별 도장을 꾹 눌러서 초록색 성장 잔디를 심어보세요!")
    
    cols = st.columns(7)
    success_count = 0
    
    for i, day in enumerate(days):
        with cols[i]:
            if st.session_state[f"cal_{day}"]:
                success_count += 1
                st.markdown(f'<div style="background-color: #2E5A44; color: white; border-radius: 8px; padding: 10px; text-align: center; font-weight: bold; margin-bottom: 5px;">{day}<br>🌱</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="background-color: #EAEDED; color: #7F8C8D; border-radius: 8px; padding: 10px; text-align: center; font-weight: bold; margin-bottom: 5px;">{day}<br>⚪</div>', unsafe_allow_html=True)
            
            if st.session_state[f"cal_{day}"]:
                if st.button("취소", key=f"btn_undo_{day}"):
                    st.session_state[f"cal_{day}"] = False
                    st.rerun()
            else:
                if st.button("실천!", key=f"btn_do_{day}"):
                    st.session_state[f"cal_{day}"] = True
                    st.rerun()

    st.markdown("### 📈 주간 성찰 통계")
    progress_percentage = int((success_count / 7) * 100)
    st.progress(success_count / 7)
    st.markdown(f"**현재 주간 미션 실천율:** `{progress_percentage}%` ({success_count} / 7일 성공)")
    
    if success_count == 7:
        st.snow()
        st.success("🎉 대박! 일주일 성장 달력을 푸른 잔디로 가득 채우셨군요! 최고의 하루하루였습니다! 👑")
            
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("새로운 실수 등록하기 🔄", key="reset_all_btn"):
        # 요일 상태는 그대로 유지하여 성찰하게 하고, 스텝만 이동!
        st.session_state.step = 1
        st.rerun()

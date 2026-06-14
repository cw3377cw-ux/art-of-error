import streamlit as st
from openai import OpenAI
import random

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="위풍당당 실수 연구소", page_icon="🎓", layout="centered")

st.markdown("""
    <style>
    .main-title { font-size: 36px; font-weight: bold; color: #1E3D2F; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 16px; color: #557A67; text-align: center; margin-bottom: 30px; }
    .cert-box { border: 5px double #2E5A44; padding: 30px; background-color: #FAFBFB; border-radius: 12px; text-align: center; margin-top: 20px; }
    .cert-title { font-size: 26px; font-weight: bold; color: #1E3D2F; margin-bottom: 20px; letter-spacing: 2px; }
    .quest-box { background-color: #EEF7F2; border: 1px solid #CCE7D9; padding: 20px; border-radius: 10px; margin-top: 15px; }
    .level-badge { background-color: #2E5A44; color: white; padding: 5px 15px; border-radius: 20px; font-size: 14px; font-weight: bold; }
    .teacher-notice { background-color: #FFF9E6; border-left: 6px solid #F1C40F; padding: 15px; margin-bottom: 20px; border-radius: 5px; font-weight: bold; color: #7D6608; }
    .quote-box { font-style: italic; color: #566573; margin-top: 15px; font-size: 14px; border-top: 1px solid #D5DBDB; padding-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# 2. 세션 상태 초기화 (데이터베이스 역할)
if "step" not in st.session_state: st.session_state.step = 1
if "past_errors" not in st.session_state: st.session_state.past_errors = []
if "teacher_messages" not in st.session_state: st.session_state.teacher_messages = []
if "class_notice" not in st.session_state: st.session_state.class_notice = "오늘도 실수를 통해 멋지게 자라나는 여러분을 응원합니다! (선생님 올림)"

days = ["월", "화", "수", "목", "금", "토", "일"]
for day in days:
    if f"cal_{day}" not in st.session_state: st.session_state[f"cal_{day}"] = False

# 3. 사이드바: 모드 전환 및 관리자 대시보드
with st.sidebar:
    st.header("⚙️ 연구소 설정")
    mode = st.radio("사용자 유형", ["학생 모드 🎒", "교사용 관리 모드 👩‍🏫"])
    
    if mode == "교사용 관리 모드 👩‍🏫":
        st.markdown("---")
        st.subheader("👩‍🏫 교수님 전용 대시보드")
        
        # [소통 강화] 전체 공지사항 수정 기능
        new_notice = st.text_area("📢 학급 전체 공지 적기", value=st.session_state.class_notice)
        if st.button("공지사항 업데이트"):
            st.session_state.class_notice = new_notice
            st.success("학급 전체 전광판에 메시지가 등록되었습니다.")
            
        st.markdown("---")
        st.subheader("📊 학급 실수 데이터")
        if st.session_state.past_errors:
            cats = [p['cat'] for p in st.session_state.past_errors]
            for c in set(cats):
                st.write(f"• {c}: {cats.count(c)}건")
                st.progress(cats.count(c) / len(cats))
            
            st.subheader("📬 도착한 비밀 상담")
            for msg in st.session_state.teacher_messages:
                st.info(f"**{msg['name']}**: {msg['msg']}\n\n*(원인: {msg['cat']})*")
        else:
            st.write("누적된 데이터가 없습니다.")

# 4. 학생 모드 메인 화면
if mode == "학생 모드 🎒":
    # [소통 강화] 선생님의 실시간 전광판 노출
    st.markdown(f'<div class="teacher-notice">📢 선생님의 한마디: {st.session_state.class_notice}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="main-title">🎓 위풍당당 실수 연구소</div>', unsafe_allow_html=True)
    
    # [레벨 시스템] 성장 시각화
    error_count = len(st.session_state.past_errors)
    if error_count < 2: level, icon, l_name = "Lv.1", "🌱", "실수 씨앗"
    elif error_count < 4: level, icon, l_name = "Lv.2", "🌿", "생각 새싹"
    elif error_count < 6: level, icon, l_name = "Lv.3", "🌳", "지혜 나무"
    else: level, icon, l_name = "Lv.Max", "🌲", "성장 숲의 주인"
    
    st.markdown(f'<p style="text-align:center;"><span class="level-badge">{level} {icon} {l_name}</span></p>', unsafe_allow_html=True)

    # ----------------- [ STEP 1: 입력 ] -----------------
    if st.session_state.step == 1:
        st.subheader("📝 오늘의 실수 등록")
        name = st.text_input("연구원 이름", placeholder="이름을 입력하세요")
        cat = st.selectbox("어떤 실수인가요?", ["수학/연산", "국어/이해", "사회/과학", "조별과제/수행", "친구관계", "기타"])
        details = st.text_area("상황 설명", placeholder="어떤 일이 있었나요?")
        
        if st.button("분석 요청 🚀"):
            if name and details:
                with st.spinner("소장님이 분석 중..."):
                    try:
                        client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=st.secrets["GROQ_API_KEY"])
                        prompt = """초등학생의 실수를 따뜻하게 위로하는 담임 선생님 말투로 대답해줘. [규칙: 번역체 금지, 구어체 사용, 아모르 파티/리좀 단어 노출 금지] 
                        구성: 🌱[소장님의 따뜻한 한마디], 🧭[나만의 주체적인 행동 지침 3가지(🔵기사, 🟢마법사, 🟣탐험가 성향별 작명)]"""
                        
                        response = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"이름:{name}, 분류:{cat}, 내용:{details}"}]
                        )
                        st.session_state.ai_analysis = response.choices[0].message.content
                        st.session_state.student_name, st.session_state.category, st.session_state.details = name, cat, details
                        st.session_state.past_errors.append({"name":name, "cat":cat, "details":details})
                        st.session_state.step = 2
                        st.rerun()
                    except: st.error("연결 에러!")
            else: st.warning("빈칸을 채워줘!")

    # ----------------- [ STEP 2: 선택 ] -----------------
    elif st.session_state.step == 2:
        st.markdown(f'<div class="cert-box" style="text-align:left;">{st.session_state.ai_analysis}</div>', unsafe_allow_html=True)
        st.markdown('<div class="quest-box"><b>🧭 소장님의 퀘스트:</b> 어떤 성장의 길을 개척해볼까요?</div>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: 
            if st.button("🔵 갈래 A"): st.session_state.final_choice = "정면 돌파의 길"; st.session_state.step = 3; st.rerun()
        with c2: 
            if st.button("🟢 갈래 B"): st.session_state.final_choice = "침착한 성찰의 길"; st.session_state.step = 3; st.rerun()
        with c3: 
            if st.button("🟡 갈래 C"): st.session_state.final_choice = "지혜로운 나눔의 길"; st.session_state.step = 3; st.rerun()

    # ----------------- [ STEP 3: 인증서 & 통계 ] -----------------
    elif st.session_state.step == 3:
        # [인문학적 장치] 철학 한 스푼 랜덤 생성
        quotes = [
            "니체 아저씨가 말했어요. '나를 쓰러뜨리지 못하는 시련은 나를 더 강하게 만든다!' 오늘의 실수도 널 강하게 만들 거야.",
            "들뢰즈 선생님은 '인생은 정해진 길이 아니라 내가 뻗어 나가는 모든 곳이 길이다'라고 했어. 네 실수는 새로운 길이란다.",
            "운명을 사랑하라는 말은, 지금 이 모습 그대로의 너를 가장 아껴주라는 뜻이야. 실수한 너도 참 소중해.",
            "생각은 뿌리처럼 뻗어 나가는 거야. 정답이 아니어도 네 생각은 이미 멋진 숲을 이루고 있어."
        ]
        
        st.markdown(f"""
        <div class="cert-box">
            <div class="cert-title">📜 위풍당당 실수 분석 인증서</div>
            <p><b>연구원:</b> {st.session_state.student_name} | <b>선택:</b> {st.session_state.final_choice}</p>
            <hr>
            <p>"실수는 새로운 길을 발견한 것입니다."</p>
            <div class="quote-box">💡 <b>소장님의 철학 한 스푼:</b><br>{random.choice(quotes)}</div>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
        
        # 주간 달력
        st.markdown("---")
        st.subheader("📅 주간 성장 잔디 심기")
        cols = st.columns(7)
        sc = 0
        for i, d in enumerate(days):
            with cols[i]:
                if st.session_state[f"cal_{d}"]:
                    sc += 1
                    st.markdown(f'<div style="background-color:#2E5A44;color:white;border-radius:5px;text-align:center;padding:5px;">{d}<br>🌱</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="background-color:#F2F3F4;border-radius:5px;text-align:center;padding:5px;">{d}<br>⚪</div>', unsafe_allow_html=True)
                if st.button("실천", key=f"d_{d}"): st.session_state[f"cal_{d}"] = not st.session_state[f"cal_{d}"]; st.rerun()
        st.progress(sc/7); st.write(f"주간 실천율: {int(sc/7*100)}%")

        # [소통 강화] 교사에게 메시지
        st.markdown("---")
        msg = st.text_input("💌 선생님께 보낼 비밀 편지", placeholder="선생님께 하고 싶은 말을 적어보세요.")
        if st.button("편지 보내기"):
            st.session_state.teacher_messages.append({"name":st.session_state.student_name, "cat":st.session_state.category, "msg":msg})
            st.success("선생님께 편지가 전달되었습니다!")

        if st.button("새로운 실수 등록하기 🔄"): 
            st.session_state.step = 1; st.rerun()

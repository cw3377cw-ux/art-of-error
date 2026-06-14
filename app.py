import streamlit as st
from openai import OpenAI
import random

# 1. 페이지 기본 설정 및 디자인 셋업 (영문 타이틀 완벽 제거)
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
    .teacher-box { background-color: #F4F6F7; border-left: 5px solid #2E5A44; padding: 15px; margin-bottom: 10px; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# 2. 세션 상태 데이터 저장소 초기화
if "step" not in st.session_state: st.session_state.step = 1
if "ai_analysis" not in st.session_state: st.session_state.ai_analysis = ""
if "student_name" not in st.session_state: st.session_state.student_name = ""
if "category" not in st.session_state: st.session_state.category = ""
if "final_choice" not in st.session_state: st.session_state.final_choice = ""
if "past_errors" not in st.session_state: st.session_state.past_errors = []
if "teacher_messages" not in st.session_state: st.session_state.teacher_messages = []
if "class_notice" not in st.session_state: st.session_state.class_notice = "오늘도 실수를 통해 멋지게 자라나는 여러분을 응원합니다! (선생님 올림)"

days = ["월", "화", "수", "목", "금", "토", "일"]
for day in days:
    if f"cal_{day}" not in st.session_state:
        st.session_state[f"cal_{day}"] = False

# 3. 사이드바: 사용자 모드 전환 및 교사용 대시보드
with st.sidebar:
    st.header("⚙️ 연구소 설정")
    mode = st.radio("사용자 유형을 선택하세요", ["학생 모드 🎒", "교사용 관리 모드 👩‍🏫"])
    
    if mode == "학생 모드 🎒":
        if st.session_state.past_errors:
            st.markdown("---")
            st.header("📬 소장님의 비밀 편지함")
            for idx, past in enumerate(st.session_state.past_errors):
                with st.expander(f"📌 {idx+1}번째 기록 성찰하기"):
                    st.markdown(f"**연구원:** {past['name']}")
                    st.markdown(f"**실수 마당:** {past['cat']}")
                    st.caption(f"당시 상황: {past['details']}")
                    st.markdown("<div class='past-box'><b>🌱 오늘의 성찰:</b> 이때의 실수는 지금 나에게 어떤 지혜가 되었나요? 대견한 나를 칭찬해 줍시다!</div>", unsafe_allow_html=True)
                    
    elif mode == "교사용 관리 모드 👩‍🏫":
        st.markdown("---")
        st.subheader("👩‍🏫 교수님 전용 대시보드")
        
        # 전체 학급 공지사항 제어 기능
        new_notice = st.text_area("📢 학급 전체 공지 업데이트", value=st.session_state.class_notice)
        if st.button("공지사항 반영하기"):
            st.session_state.class_notice = new_notice
            st.success("학급 전광판에 등록되었습니다.")
            
        st.markdown("---")
        st.subheader("📊 실시간 누적 실수 통계")
        if st.session_state.past_errors:
            cats = [p['cat'] for p in st.session_state.past_errors]
            for c in set(cats):
                st.write(f"• {c}: {cats.count(c)}건 발생")
                st.progress(cats.count(c) / len(cats))
            
            st.subheader("📬 도착한 비밀 상담 우체통")
            for msg in st.session_state.teacher_messages:
                st.markdown(f"""
                <div class="teacher-box">
                    <b>👤 {msg['name']} 어린이</b> ({msg['cat']})<br>
                    <b>💬 메시지:</b> {msg['msg']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("누적된 학급 실수 데이터가 아직 없습니다.")

# 4. 학생 모드 메인 화면 구동
if mode == "학생 모드 🎒":
    # 교사의 실시간 안내 전광판 상단 노출
    st.markdown(f'<div class="teacher-notice">📢 선생님의 한마디: {st.session_state.class_notice}</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">🎓 위풍당당 실수 연구소</div>', unsafe_allow_html=True)
    
    # 생각의 나무 레벨 시스템 시각화
    error_count = len(st.session_state.past_errors)
    if error_count < 2: level, icon, l_name = "Lv.1", "🌱", "실수 씨앗"
    elif error_count < 4: level, icon, l_name = "Lv.2", "🌿", "생각 새싹"
    elif error_count < 6: level, icon, l_name = "Lv.3", "🌳", "지혜 나무"
    else: level, icon, l_name = "Lv.Max", "🌲", "성장 숲의 주인"
    
    st.markdown(f'<p style="text-align:center;"><span class="level-badge">{level} {icon} {l_name}</span></p>', unsafe_allow_html=True)

    # ----------------- [ STEP 1: 아동 친화적 입력 화면 ] -----------------
    if st.session_state.step == 1:
        st.subheader("📝 오늘의 실수 등록하기")
        name = st.text_input("당신의 멋진 이름(또는 별명)을 적어주세요!", placeholder="예: 홍길동")
        cat = st.selectbox("오늘 교실이나 공부 중에 어떤 실수를 마주했나요?", ["수학/연산 실수", "국어/지문 오해", "사회/과학 개념 혼동", "수행평가 및 조별 과제 중 아쉬운 실수", "친구 관계 및 학급 생활 속 행동 실수", "기타 (직접 입력)"])
        details = st.text_area("저지른 실수나 당시의 상황을 솔직하게 나누어 주세요.", placeholder="예시: 수학 단원평가 풀다가 더하기를 빼기로 잘못 보고 풀어서 틀렸어요.")
        
        if st.button("실수 연구소에 가치 분석 요청하기 🚀"):
            if name and details:
                with st.spinner("연구소장 AI가 당신의 실수를 위대한 자산으로 재해석하는 중..."):
                    try:
                        client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=st.secrets["GROQ_API_KEY"])
                        
                        # 고정된 타이틀 탈피, 실수 연계형 동적 제목 작명 지침 셋업
                        system_prompt = """
                        너는 초등학생이 학교에서 저지른 실수를 따뜻하게 위로하고 성장의 원동력으로 바꿔주는 다정하고 유쾌한 '초등학교 담임 선생님'이자 '실수 연구소장 AI'야.
                        
                        [가장 중요한 규칙: 영어 번역체 및 서양 철학 문체 절대 금지]
                        - "~하는 대신 ~해라", "~하는 과정을 통해 ~을 얻었다" 같은 딱딱한 번역투는 절대 쓰지 마.
                        - "~했구나!", "~해보는 건 어떨까?", "~해보자!" 처럼 실제 다정한 선생님이 아이에게 조근조근 말하는 100% 자연스러운 한국어 구어체로만 대답해줘.
                        - '아모르 파티', '리좀' 단어는 절대 답변에 직접 노출하지 마.
                        
                        [답변 작성 구조 - 아래 양식을 엄격히 지켜서 출력할 것]
                        
                        🌱 [소장님의 따뜻한 한마디]
                        (아이가 적은 구체적 실수를 바탕으로 공감해 주고, 왜 그 행동이 '뇌가 열심히 새로운 길을 탐험하다 생긴 멋진 발자국'인지 따뜻하게 격려해줘.)
                        
                        🧭 [나만의 주체적인 행동 지침 3가지]
                        (아이가 입력한 구체적인 실수 상황을 완벽하게 반영하여, 다음부터 실천할 수 있는 해결책 3가지를 기발하게 창작해줘. 
                        주의: '정면 돌파형 기사', '침착한 마법사' 같은 상투적이고 고정된 타이틀 수식어는 절대 쓰지 마! 
                        대신 아이가 겪은 구체적 실수 내용에 따라 핵심 해결책을 직관적으로 축약한 기발하고 재미있는 순우리말/초등 눈높이의 동적 제목을 3가지 실시간으로 작명하여 제안해줘.)
                        - 🔵 [실수 상황 맞춤형으로 요약한 톡톡 튀는 해결책 제목 A] (행동 요령 설명)
                        - 🟢 [실수 상황 맞춤형으로 요약한 톡톡 튀는 해결책 제목 B] (행동 요령 설명)
                        - 🟣 [실수 상황 맞춤형으로 요약한 톡톡 튀는 해결책 제목 C] (행동 요령 설명)
                        """
                        
                        response = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": f"이름:{name}, 분류:{cat}, 내용:{details}"}],
                            temperature=0.7
                        )
                        st.session_state.ai_analysis = response.choices[0].message.content
                        st.session_state.student_name, st.session_state.category, st.session_state.details = name, cat, details
                        
                        # 타임머신용 과거 저장소에 누적
                        st.session_state.past_errors.append({"name": name, "cat": cat, "details": details})
                        st.session_state.step = 2
                        st.rerun()
                    except: 
                        st.error("AI 서버 연결 에러! Secrets 설정을 확인해봐, 어이!")
            else: 
                st.warning("이름이랑 상황을 빈칸 없이 적어줘!")

    # ----------------- [ STEP 2: 인터랙티브 생각의 갈래 선택 ] -----------------
    elif st.session_state.step == 2:
        st.markdown(f'<div class="cert-box" style="text-align:left;">{st.session_state.ai_analysis}</div>', unsafe_allow_html=True)
        st.markdown('<div class="quest-box"><b>🧭 소장님의 비밀 퀘스트:</b> 자, 이 실수의 무대 위에서 당신은 이제 어떤 생각의 갈래를 선택해 개척해 나가겠습니까?</div>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: 
            if st.button("🔵 갈래 A 선택"): st.session_state.final_choice = "용기 있게 정면으로 부딪히며 탐험하는 길"; st.session_state.step = 3; st.rerun()
        with c2: 
            if st.button("🟢 갈래 B 선택"): st.session_state.final_choice = "침착하게 멈춰 서서 나를 돌아보는 깊은 샘물의 길"; st.session_state.step = 3; st.rerun()
        with c3: 
            if st.button("🟡 갈래 C 선택"): st.session_state.final_choice = "친구들과 지혜를 나누며 함께 발을 맞춰 걷는 길"; st.session_state.step = 3; st.rerun()

    # ----------------- [ STEP 3: 최종 인증서 발행 및 잔디 달력 + 소통 ] -----------------
    elif st.session_state.step == 3:
        quotes = [
            "니체 아저씨가 말했어요. '나를 쓰러뜨리지 못하는 시련은 나를 더 강하게 만든다!' 오늘의 실수도 널 단단하게 만들어 줄 거야.",
            "들뢰즈 선생님은 '인생은 정해진 하나의 길이 아니라 내가 사방으로 뻗어 나가는 모든 곳이 길이다'라고 했어. 네 실수는 새로운 개척지란다.",
            "나의 운명을 기꺼이 사랑하라는 말은, 실수한 모습 그대로의 너도 가장 소중하게 아껴주라는 뜻이야.",
            "생각은 생각의 뿌리를 타고 자유롭게 자란단다. 정답이 아니어도 네 사고 회로는 이미 멋진 성장의 숲을 이루고 있어."
        ]
        
        st.markdown(f"""
        <div class="cert-box">
            <div class="cert-title">📜 위풍당당 실수 분석 인증서</div>
            <p><b>연구원 성명:</b> {st.session_state.student_name} 어린이</p>
            <p><b>선택한 성장의 갈래:</b> ✨ {st.session_state.final_choice} ✨</p>
            <hr style="border: 1px dashed #2E5A44;">
            <p style="font-weight: bold; color: #2E5A44; font-size: 13pt;">"실수는 틀린 것이 아니라, 새로운 길을 발견한 것입니다."</p>
            <div class="quote-box">💡 <b>소장님의 철학 한 스푼:</b><br>{random.choice(quotes)}</div>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
        
        # 명시적 시각화 주간 잔디 달력 보드
        st.markdown("---")
        st.subheader("📅 나만의 비밀 퀘스트 주간 달력")
        st.info("요일별 도장을 꾹 눌러서 초록색 성장 잔디를 심어보세요!")
        
        cols = st.columns(7)
        sc = 0
        for i, d in enumerate(days):
            with cols[i]:
                if st.session_state[f"cal_{d}"]:
                    sc += 1
                    st.markdown(f'<div style="background-color:#2E5A44;color:white;border-radius:8px;text-align:center;padding:10px;font-weight:bold;margin-bottom:5px;">{d}<br>🌱</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="background-color:#EAEDED;color:#7F8C8D;border-radius:8px;text-align:center;padding:10px;font-weight:bold;margin-bottom:5px;">{d}<br>⚪</div>', unsafe_allow_html=True)
                
                if st.button("실천!", key=f"d_btn_{d}"): 
                    st.session_state[f"cal_{d}"] = not st.session_state[f"cal_{d}"]
                    st.rerun()
                    
        st.progress(sc/7)
        st.markdown(f"**현재 주간 미션 실천율:** `{int(sc/7*100)}%` ({sc} / 7일 성공)")
        
        # 양방향 소통 창구 연동 (교사용 대시보드로 실시간 다이렉트 전송)
        st.markdown("---")
        st.subheader("💌 담임 선생님께 비밀 상담 편지 보내기")
        student_msg = st.text_input("선생님께만 전하고 싶은 각오나 마음:", placeholder="예: 선생님, 저 내일부터 뺄셈 함정 조심하기 미션 꼭 실천해 볼게요!")
        if st.button("비밀 편지 발송하기 📮"):
            if student_msg:
                st.session_state.teacher_messages.append({"name": st.session_state.student_name, "cat": st.session_state.category, "msg": student_msg})
                st.success("선생님 대시보드로 안전하게 전송되었습니다! (사이드바 교사 모드에서 즉시 확인 가능)")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("새로운 실수 등록하기 🔄", key="final_reset"):
            st.session_state.step = 1
            st.rerun()

# 교사용 모드 대기 상태 안내문
elif mode == "교사용 전용 관리 모드 👩‍🏫":
    st.subheader("👩‍🏫 교사용 실시간 관리자 화면")
    st.info("← 왼쪽 사이드바 메뉴를 보시면 현재 학생들이 등록한 실시간 실수 유형 통계 그래프와 학생들이 전송한 비밀 상담 편지를 즉각 확인하실 수 있습니다.")

import streamlit as st
import requests
import json
import random

# 1. 화면 기본 설정 및 꾸미기 (순우리말 한국어 정서 정돈)
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

st.markdown('<div class="main-title">🎓 위풍당당 실수 연구소</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">나의 실수를 당당하게 반겨주고, 나만의 새로운 성장 길을 찾아가는 교실</div>', unsafe_allow_html=True)

# 2. 기억 저장소 초기화 (개인 화면 기억용 세션 유지)
if "step" not in st.session_state: st.session_state.step = 1
if "ai_analysis" not in st.session_state: st.session_state.ai_analysis = ""
if "student_name" not in st.session_state: st.session_state.student_name = ""
if "category" not in st.session_state: st.session_state.category = ""
if "final_choice" not in st.session_state: st.session_state.final_choice = ""
if "past_errors" not in st.session_state: st.session_state.past_errors = []
if "teacher_messages" not in st.session_state: st.session_state.teacher_messages = []
if "class_notice" not in st.session_state: st.session_state.class_notice = "오늘도 실수를 통해 멋지게 자라나는 여러분을 응원합니다! (선생님 씀)"

days = ["월", "화", "수", "목", "금", "토", "일"]
for day in days:
    if f"cal_{day}" not in st.session_state:
        st.session_state[f"cal_{day}"] = False

# 3. 옆구리 메뉴창: 모드 변경 및 교사용 모음판
with st.sidebar:
    st.header("⚙️ 연구소 설정")
    mode = st.radio("누구인가요?", ["학생 마당 🎒", "선생님 전용 관리 마당 👩‍🏫"])
    
    if mode == "학생 마당 🎒":
        if st.session_state.past_errors:
            st.markdown("---")
            st.header("📬 소장님의 비밀 편지함")
            for idx, past in enumerate(st.session_state.past_errors):
                with st.expander(f"📌 {idx+1}번째 성장 기록 성찰하기"):
                    st.markdown(f"**연구원 이름:** {past['name']}")
                    st.markdown(f"**실수 종류:** {past['cat']}")
                    st.caption(f"겪은 상황: {past['details']}")
                    st.markdown("<div class='past-box'><b>🌱 오늘의 돌아보기:</b> 이때의 실수는 지금 나에게 어떤 단단한 지혜가 되었나요? 대견한 나를 듬뿍 칭찬해 줍시다!</div>", unsafe_allow_html=True)
                    
    elif mode == "선생님 전용 관리 마당 👩‍🏫":
        st.markdown("---")
        st.subheader("👩‍🏫 교수님 전용 모음판")
        
        new_notice = st.text_area("📢 학급 전체 알림판 글 적기", value=st.session_state.class_notice)
        if st.button("알림판 글 바꾸기"):
            st.session_state.class_notice = new_notice
            st.success("학급 전광판에 잘 등록되었습니다.")
            
        st.markdown("---")
        st.subheader("📊 실시간 누적 실수 통계 게이지")
        if st.session_state.past_errors:
            cats = [p['cat'] for p in st.session_state.past_errors]
            for c in set(cats):
                count = cats.count(c)
                st.write(f"• {c}: {count}번 일어남")
                st.progress(count / len(cats))
            
            st.subheader("📬 도착한 비밀 상담 우체통")
            for msg in st.session_state.teacher_messages:
                st.markdown(f"""
                <div class="teacher-box">
                    <b>👤 {msg['name']} 어린이</b> ({msg['cat']})<br>
                    <b>💬 보낸 메시지:</b> {msg['msg']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("쌓인 학급 실수 자료가 아직 없습니다.")

# 4. 학생 모드 메인 화면 구동
if mode == "학생 마당 🎒":
    st.markdown(f'<div class="teacher-notice">📢 선생님의 한마디: {st.session_state.class_notice}</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">🎓 위풍당당 실수 연구소</div>', unsafe_allow_html=True)
    
    error_count = len(st.session_state.past_errors)
    if error_count < 2: level, icon, l_name = "1단계", "🌱", "실수 씨앗"
    elif error_count < 4: level, icon, l_name = "2단계", "🌿", "생각 새싹"
    elif error_count < 6: level, icon, l_name = "3단계", "🌳", "지혜 나무"
    else: level, icon, l_name = "최고 단계", "🌲", "성장 숲의 주인"
    
    st.markdown(f'<p style="text-align:center;"><span class="level-badge">{level} {icon} {l_name}</span></p>', unsafe_allow_html=True)

    # ----------------- [ 1단계: 입력 화면 ] -----------------
    if st.session_state.step == 1:
        st.subheader("📝 오늘의 실수 등록하기")
        name = st.text_input("당신의 멋진 이름(또는 별명)을 적어주세요!", placeholder="예: 홍길동")
        cat = st.selectbox("오늘 교실이나 공부 중에 어떤 실수를 마주했나요?", ["수학 계산 실수", "국어 글 고쳐 읽기 실수", "사회나 과학 개념 혼동", "모둠 과제 중 아쉬운 실수", "친구 관계나 학급 생활 속 말실수", "기타 직접 적기"])
        details = st.text_area("겪었던 실수나 당시 상황을 솔직하게 나누어 주세요.", placeholder="예시: 수학 문제를 풀다가 더하기를 빼기로 잘못 보고 풀어서 틀렸어요.")
        
        if st.button("실수 연구소에 가치 분석 요청하기 🚀"):
            if name and details:
                with st.spinner("실수를 멋진 자산으로 재해석하는 중..."):
                    
                    backup_responses = {
                        "수학 계산 실수": """🌱 [소장님의 따뜻한 한마디]
틀린 연산 기호나 숫자는 결코 부끄러운 게 아니란다! 우리 뇌가 엄청나게 빠른 속도로 문제를 해결하려다 잠깐 발을 헛디딘 것뿐이야. 오히려 이런 사소한 틈새를 찾아내는 과정에서 수학적 사고력이 훨씬 더 깊고 단단해진단다!

🧭 [나만의 행동 지침 3가지]
- 🔵 [돋보기 기호 탐정 작전] 앞으로 문제를 읽을 때 연산 기호에 초록색 동그라미를 크게 치고 시작해 보는 건 어떨까?
- 🟢 [숨고르기 삼초 마법] 답을 다 적고 나서 딱 삼 초 동안만 검토하는 침착한 시간을 가져보자.
- 🟣 [오답 보물 상자 만들기] 틀린 식을 나만의 공책에 비밀스럽게 기록해 두는 멋진 탐험을 시작해보자.""",
                        
                        "국어 글 고쳐 읽기 실수": """🌱 [소장님의 따뜻한 한마디]
글자나 문맥을 잠깐 착각한 건 네가 글을 대충 읽어서가 아니라, 네 뇌가 더 창의적이고 풍부한 이야기를 상상하느라 찰나의 틈이 생긴 거란다! 고쳐 읽는 발자국마다 네 어휘력과 상상력은 무럭무럭 자라나고 있어.

🧭 [나만의 행동 지침 3가지]
- 🔵 [손가락 징검다리 걷기] 글을 읽을 때 손가락 끝으로 글자를 하나하나 짚으며 디딤돌처럼 따라가 보자.
- 🟢 [마음의 낭독회 열기] 마음속으로 아주 다정하고 부드러운 목소리로 글을 소리 내어 읽는 상상을 해보는 건 어떨까?
- 🟣 [숨은 글자 사냥꾼] 문장 속에 숨어있는 진짜 핵심 단어를 찾아 동그라미 치는 보물찾기 퀘스트를 해보자.""",
                        
                        "사회나 과학 개념 혼동": """🌱 [소장님의 따뜻한 한마디]
방대한 개념들이 머릿속에서 얽히고설키는 건 당연한 성장통이란다! 뇌가 복잡한 지식의 지도를 새롭게 그리느라 교통정리를 하는 중이거든. 헷갈렸던 개념을 바로잡을 때 지식의 뿌리가 훨씬 깊숙이 내려앉는단다.

🧭 [나만의 행동 지침 3가지]
- 🔵 [마인드맵 거미줄 그리기] 공책에 중심 단어를 적고 뿌리처럼 사방으로 연상되는 개념을 이어나가 보자.
- 🟢 [어린이 선생님 놀이] 인형이나 거울을 보고 방금 배운 개념을 아주 쉽게 설명해 주는 마법의 교실을 열어보자.
- 🟣 [개념 짝꿍 카드 찾기] 단어와 뜻을 카드로 쪼개어 맞춰보는 재미있는 놀이판을 만들어 실천해보자.""",
                        
                        "모둠 과제 중 아쉬운 실수": """🌱 [소장님의 따뜻한 한마디]
여랫이 함께 조화를 이루며 걸어갈 때 삐걱거리는 발소리가 나는 건 너무나 자연스러운 일이야! 서로 다른 생각의 조각들이 맞물려 거대한 그림을 완성하는 멋진 과정이거든. 이 아쉬움이 다음 협력의 훌륭한 나침반이 될 거란다.

🧭 [나만의 행동 지침 3가지]
- 🔵 [마음 경청 확성기 켜기] 친구가 이야기를 할 때 고개를 세 번 끄덕이며 끝까지 들어주는 미션을 수행해보자.
- 🟢 [따뜻한 칭찬 배달원] 모둠원의 멋진 아이디어를 발견할 때마다 "그 생각 진짜 멋지다!"라고 먼저 말해보자.
- 🟣 [역할 톱니바퀴 맞추기] 내가 맡은 작은 임무를 책임감 있게 끝마치며 조용히 동료를 돕는 기쁨을 찾아보자.""",
                        
                        "친구 관계나 학급 생활 속 말실수": """🌱 [소장님의 따뜻한 한마디]
말 한마디가 아쉽게 툭 튀어나왔을 때 속상해하는 그 마음 자체만으로도 너는 이미 엄청나게 따뜻하고 예쁜 성품을 가진 아이란다! 상처를 솔직하게 인정하고 먼저 손 내밀 수 있는 용기가 너를 가장 멋진 친구로 만들어 줄 거야.

🧭 [나만의 행동 지침 3가지]
- 🔵 [용기 퐁퐁 사과 편지] 속상했을 친구에게 "아까는 내 마음과 다르게 말이 나왔어, 미안해"라고 진심을 전해보자.
- 🟢 [신호등 입술 필터] 말이 입 밖으로 나오기 전에 '빨간불'을 켜고 잠깐 생각한 뒤 말하는 연습을 해보자.
- 🟣 [비밀 정서 우체통] 내 감정을 글이나 일기로 적으며 마음의 호수를 잔잔하게 다스려보는 시간을 가져보자."""
                    }
                    
                    default_backup = """🌱 [소장님의 따뜻한 한마디]
실수를 솔직하게 마주한 것 자체만으로도 너는 이미 엄청나게 멋진 어린이 연구원이야! 실수는 틀린 게 아니라 새로운 길을 발견하는 지도란다. 오늘의 성찰을 통해 한 뼘 더 단단하게 자라날 너를 소장님이 언제나 응원할게!

🧭 [나만의 행동 지침 3가지]
- 🔵 [씩씩한 발걸음 작전] 아쉬움은 훌훌 털어버리고 내일 교실 문을 열 때 밝게 웃으며 인사하기 미션을 수행해보자.
- 🟢 [생각 정돈 일기장] 오늘 있었던 일 중에 가장 대견했던 점 하나를 찾아 일기에 꾹꾹 눌러 적어보자.
- 🟣 [지혜의 나침반 세우기] 다음번에 비슷한 상황이 오면 삼 초만 멈춰 서서 생각하기로 나 자신과 약속해보자."""

                    try:
                        api_key = st.secrets["GEMINI_API_KEY"]
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                        
                        headers = {'Content-Type': 'application/json'}
                        payload = {
                            "contents": [{
                                "parts": [{"text": f"초등학교 담임 선생님 말투로 어린이 이름 {name}이 겪은 실수 [{details}]를 위로하는 따뜻한 줄글 한마디와, 상투적이지 않고 구체적인 상황을 요약한 한글 제목 지침 3가지를 친근한 구어체로 작성해줘. 한자어나 영어 단어, 리좀, 아모르파티는 절대 금지야."}]
                            }]
                        }
                        
                        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=5)
                        response_json = response.json()
                        
                        if 'candidates' in response_json:
                            ai_text = response_json['candidates'][0]['content']['parts'][0]['text']
                        else:
                            ai_text = backup_responses.get(cat, default_backup)
                            
                    except:
                        ai_text = backup_responses.get(cat, default_backup)
                    
                    st.session_state.ai_analysis = ai_text
                    st.session_state.student_name, st.session_state.category, st.session_state.details = name, cat, details
                    st.session_state.past_errors.append({"name": name, "cat": cat, "details": details})
                    st.session_state.step = 2
                    st.rerun()

    # ----------------- [ 2단계: 생각의 갈래 선택 ] -----------------
    elif st.session_state.step == 2:
        st.markdown(f'<div class="cert-box" style="text-align:left;">{st.session_state.ai_analysis}</div>', unsafe_allow_html=True)
        st.markdown('<div class="quest-box"><b>🧭 소장님의 비밀 퀘스트:</b> 자, 이 실수의 무대 위에서 당신은 이제 어떤 생각의 갈래를 선택해 개척해 나가겠습니까?</div>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: 
            if st.button("🔵 갈래 첫 번째 선택"): st.session_state.final_choice = "용기 있게 정면으로 부딪히며 탐험하는 길"; st.session_state.step = 3; st.rerun()
        with c2: 
            if st.button("🟢 갈래 두 번째 선택"): st.session_state.final_choice = "침착하게 멈춰 서서 나를 돌아보는 깊은 샘물의 길"; st.session_state.step = 3; st.rerun()
        with c3: 
            if st.button("🟡 갈래 세 번째 선택"): st.session_state.final_choice = "친구들과 지혜를 나누며 함께 발을 맞춰 걷는 길"; st.session_state.step = 3; st.rerun()

    # ----------------- [ 3단계: 최종 인증서 발행 및 잔디 달력 ] -----------------
    elif st.session_state.step == 3:
        quotes = [
            "위대한 철학자 니체 아저씨가 말했어요. '나를 쓰러뜨리지 못하는 시련은 나를 더 강하게 만든다!' 오늘의 실수도 널 단단하게 만들어 줄 거야.",
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
        
        st.markdown("---")
        # [오류 해결 패치 완료]: 최신 파이썬 규격에 맞춰 불순한 HTML 태그를 제거하고 올바른 마크다운 구조로 전면 수정함!
        st.subheader("💌 담임 선생님께 비밀 상담 편지 보내기")
        student_msg = st.text_input("선생님께만 전하고 싶은 각오나 마음:", placeholder="예: 선생님, 저 내일부터 뺄셈 함정 조심하기 미션 꼭 실천해 볼게요!")
        if st.button("비밀 편지 발송하기 📮"):
            if student_msg:
                st.session_state.teacher_messages.append({"name": st.session_state.student_name, "cat": st.session_state.category, "msg": student_msg})
                st.success("선생님 전용 모음판으로 안전하게 전송되었습니다! (사이드바 메뉴에서 즉시 확인 가능)")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("새로운 실수 등록하기 🔄", key="final_reset"):
            st.session_state.step = 1
            st.rerun()

elif mode == "선생님 전용 관리 마당 👩‍🏫":
    st.subheader("👩‍🏫 선생님 전용 실시간 화면")
    st.info("← 왼쪽 사이드바 메뉴를 보시면 현재 학생들이 등록한 실시간 실수 종류 통계 게이지와 학생들이 전송한 비밀 상담 편지를 즉각 확인하실 수 있습니다.")

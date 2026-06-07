import streamlit as st
from openai import OpenAI

# 1. 페이지 기본 설정 및 아카데믹 그린 스타일 셋업
st.set_page_config(page_title="위풍당당 실수 연구소", page_icon="🎓", layout="centered")

st.markdown("""
    <style>
    .main-title { font-size: 34px; font-weight: bold; color: #1E3D2F; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 15px; color: #557A67; text-align: center; margin-bottom: 30px; }
    .cert-box { border: 5px double #2E5A44; padding: 30px; background-color: #FAFBFB; border-radius: 10px; text-align: center; margin-top: 20px; }
    .cert-title { font-size: 24px; font-weight: bold; color: #1E3D2F; margin-bottom: 20px; letter-spacing: 2px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎓 위풍당당 실수 연구소</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">나의 실수를 당당하게 긍정하고, 나만의 성장 경로를 탐색하는 교실</div>', unsafe_allow_html=True)
# 2. 사이드바 API 키 입력 설정 (이제 키 입력창을 없애고 설명만 남긴다!)
with st.sidebar:
    st.header("🔑 시스템 설정")
    st.success("시스템 API Key가 안전하게 연동되어 있습니다.")
    st.info("이 프로그램은 완전히 무료인 Llama-3.1 모델을 기반으로 구동됩니다.")

# 3. 학생 친화적 입력 폼 인터페이스
st.subheader("📝 오늘의 실수 등록하기")
student_name = st.text_input("당신의 멋진 이름(또는 별명)을 적어주세요!", placeholder="예: 홍길동")

# 선택지에 '기타 (직접 입력)'를 추가했다
category_choice = st.selectbox(
    "오늘 교실이나 공부 중에 어떤 실수를 마주했나요?",
    ["수학/연산 실수 (기호 혼동, 계산 미스 등)", 
     "국어/지문 오해 (문제를 잘못 읽음 등)", 
     "사회/과학 개념 혼동 (아리송한 낱말 등)", 
     "수행평가 및 조별 과제 중 아쉬운 실수", 
     "친구 관계 및 학급 생활 속 행동 실수",
     "기타 (직접 입력)"]
)

# 사용자가 '기타 (직접 입력)'를 선택했을 때만 입력창이 나타나는 마법!
if category_choice == "기타 (직접 입력)":
    category = st.text_input("어떤 종류의 실수인지 간단하게 써주세요 (예: 청소 시간 실수, 준비물 깜빡 등)", placeholder="여기에 실수의 종류를 입력하세요")
else:
    category = category_choice

error_details = st.text_area(
    "저지른 실수나 당시의 상황을 솔직하게 나누어 주세요.",
    placeholder="예시: 수학 단원평가 풀다가 더하기를 빼기로 잘못 보고 풀어서 틀렸어요. 너무 속상해요."
)

submit_btn = st.button("실수 연구소에 가치 분석 요청하기 🚀")

# 4. 인문학적 프롬프트 연동 및 생성 로직
if submit_btn:
    if not student_name or not error_details:
        st.warning("이름이랑 실수를 마주한 상황을 빈칸 없이 입력해줘!")
    else:
        with st.spinner("연구소장 AI가 당신의 실수를 위대한 자산으로 재해석하는 중..."):
            try:
                # 사이드바 입력창 대신 streamlit의 비밀 금고(secrets)에서 키를 자동으로 꺼내온다!
                client = OpenAI(
                    base_url="https://api.groq.com/openai/v1",
                    api_key=st.secrets["GROQ_API_KEY"]
                )
                
                # '실수' 콘셉트 중심의 고도화된 시스템 프롬프트 (이 긴 내용이 들어가야 작동한다!)
                system_prompt = """
                너는 초등학생들이 학교생활과 공부 중에 저지른 '실수'를 성장의 비타민으로 바꿔주는 '위풍당당 실수 연구소장 AI'야.
                
                니체의 '아모르 파티(Amor Fati)' 정신에 따라, 아이가 자신의 실수를 부끄러워하거나 숨기지 않고 "이 실수가 나를 더 강하게 만들 거야!"라며 당당하게 긍정하도록 유도해줘.
                또한 들뢰즈의 '리좀(Rhizome)' 관점을 적용해서, 학교가 정한 '단 하나의 정답 경로'에서 미끄러진 아이의 실수를 '생각이 사방으로 뻗어 나가는 창의적인 오작동이자 새로운 탐험'으로 재해석해 주어야 해.
                
                [답변 작성 규칙]
                1. 대상 독자: 초등학교 3~6학년 어린이가 읽고 바로 이해할 수 있도록 친근하고 다정하면서도 유머러스한 격려조를 유지할 것.
                2. 금지 사항: 절대로 꼰대처럼 훈계하거나, "다음엔 조심해야지?" 같은 죄책감을 주는 주입식 멘트는 절대 금지. 니체의 아모르 파티, 들뢰즈의 리좀 용어를 직접적으로 언급 절대 금지.
                3. 필수 포함 요소 (줄글 형태로 자연스럽게 연결해서 작성):
                   - [실수의 반전 가치]: 아이가 입력한 실수가 왜 '바보 같은 짓'이 아니라 '뇌가 열심히 일하다가 생긴 멋진 탐험 흔적'인지 철학적으로 칭찬 및 해석.
                   - [나만의 행동 지침 3가지]: 아이가 앞으로 같은 상황에서 주체적으로 실천할 수 있는 재미있고 독창적인 이름의 해결책을 3가지 제안. 이때, 이 해결책은 실수에 걸맞게 대응되어야 하며, 구체적인 행동을 필수적으로 유도할 것. 
                
                user_content = f"이름: {student_name}\n분류: {category}\n실수 기술: {error_details}"
                
                # 무료 고성능 모델인 llama-3.1-8b-instant로 호출!
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content}
                    ],
                    temperature=0.7
                )
                
                ai_analysis = response.choices[0].message.content
                
                # 5. 연구소 분석 인증서 피드백 출력
                st.success("분석 완료! 당신의 실수는 성장의 시작점입니다.")
                
                st.markdown(f"""
                    <div class="cert-box">
                        <div class="cert-title">📜 위풍당당 실수 분석 인증서</div>
                        <p><b>연구원 성명:</b> {student_name} 어린이</p>
                        <p><b>등록된 실수 마당:</b> {category}</p>
                        <hr style="border: 1px dashed #2E5A44;">
                        <div style="text-align: left; white-space: pre-wrap; line-height: 1.7; color: #2C3E50; padding: 10px 5px;">
                            {ai_analysis}
                        </div>
                        <hr style="border: 1px dashed #2E5A44;">
                        <p style="margin-top: 20px; font-weight: bold; color: #2E5A44; font-size: 13pt;">"실수는 틀린 것이 아니라, 새로운 길을 발견한 것입니다."</p>
                        <p style="font-size: 13px; color: #7F8C8D; margin-top: 8px;">위풍당당 실수 연구소 | 소장 AI 배상</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.balloons()
                
            except Exception as e:
                st.error(f"에러 발생! Secrets 설정이나 API 키를 확인해봐: {e}")

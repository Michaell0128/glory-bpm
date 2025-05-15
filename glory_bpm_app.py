import streamlit as st
import datetime
import requests

# 웹훅 URL (메이크 Webhook1 주소)
WEBHOOK_URL = "https://hook.eu2.make.com/spsrabuk655kpqb8hckd1dtt7v7a7nio"

st.set_page_config(page_title="Glory BPM", page_icon="🚀", layout="centered")

# 세션 스테이트 초기화
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'task_counter' not in st.session_state:
    st.session_state.task_counter = 1

# 휴일 리스트 (예시)
holidays = []

# 세부업무 추천 매칭표
subtask_suggestions = {
    "콘텐츠": ["목차 작성", "경쟁사 분석", "타겟 설정"],
    "촬영": ["촬영 리스트 작성", "소품 준비", "숏폼 영상 촬영", "롱폼 영상 촬영", "제품 사진 촬영", "제품 홍보영상 촬영"],
    "디자인": ["로고 디자인", "패키지 디자인", "상세페이지 디자인", "명함 디자인", "렌딩페이지 디자인", "카드뉴스 디자인"],
    "인스타그램": ["숏폼 촬영", "카드뉴스 기획"],
    "유튜브": ["컨텐츠 기획", "영상 업로드"],
    "IR": ["기획", "제안서작성", "경쟁사 분석", "타겟 분석"]
}

# 기한 계산 함수
def calculate_due_date(days):
    if not days:
        return "기한 없음"
    today = datetime.date.today()
    delta = datetime.timedelta(days=1)
    while days > 0:
        today += delta
        if today.weekday() < 5 and today not in holidays:
            days -= 1
    return today.strftime('%Y-%m-%d (%a)')

# 업무 담당자 배정 함수
def assign_task(task_name):
    task_name = task_name.lower()
    if any(keyword in task_name for keyword in ["콘텐츠", "기획", "촬영 준비", "레시피", "sns", "마케팅", "분석", "보고서"]):
        return "이윤성"
    elif any(keyword in task_name for keyword in ["제품", "상품", "패키지", "촬영 세팅", "디자인", "편집", "영상"]):
        return "권희용"
    else:
        if len(task_name) <= 15:
            return "이윤성"
        else:
            return "권희용"

# 메인 앱 시작
st.title("Glory BPM - 업무 입력")

st.subheader("업무 추가")

for i in range(st.session_state.task_counter):
    with st.form(key=f"form_{i}"):
        st.markdown(f"### 업무 {i+1}")

        cols = st.columns([3, 1])  # 업무명:기한 입력창 비율 설정

        with cols[0]:
            task_name = st.text_input("업무명 입력", key=f"task_{i}")
            st.caption("(자유로운 문장으로 작성)")

        with cols[1]:
            due_days = st.text_input("기한 입력", key=f"due_{i}")
            st.caption("(X일, 공백='기한 없음')")
            due_preview = calculate_due_date(int(due_days)) if due_days.isdigit() else "기한 없음"
            st.caption(f"예상 기한: {due_preview}")

        suggested = []
        if task_name:
            for keyword, suggestions in subtask_suggestions.items():
                if keyword in task_name:
                    suggested = st.multiselect("추가 제안 업무 선택", suggestions, key=f"sub_{i}")
                    break

        # 업무 저장 버튼
        submitted = st.form_submit_button("업무 저장")
        if submitted:
            assigned_to = assign_task(task_name)
            task_data = {
                "task_name": task_name,
                "due_date": due_preview,
                "sub_tasks": suggested,
                "assigned_to": assigned_to,
                "status": "pending",
                "created_at": datetime.datetime.now().isoformat()
            }
            st.session_state.tasks.append(task_data)
            st.success(f"업무 '{task_name}' 저장 완료! 담당자: {assigned_to}")

# 추가 업무 입력 버튼
if st.button("+ 추가 업무 입력"):
    st.session_state.task_counter += 1

st.divider()

# 🟡 수정된 핵심 부분
if st.button("업무배정 실행"):
    if not st.session_state.tasks:
        st.error("입력된 업무가 없습니다.")
    else:
        # 전체 업무 리스트를 한번에 Webhook1으로 전송
        payload = {
            "tasks": st.session_state.tasks
        }
        response = requests.post(WEBHOOK_URL, json=payload)

        if response.status_code == 200:
            st.success(f"총 {len(st.session_state.tasks)}건의 업무가 성공적으로 전송되었습니다!")
        else:
            st.error(f"전송 실패: {response.status_code}")

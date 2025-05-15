import streamlit as st
import datetime
import requests

# Streamlit page config
st.set_page_config(page_title="Glory BPM", page_icon="🚀", layout="centered")

# Webhook URL (Make)
WEBHOOK_URL = "https://hook.eu2.make.com/spsrabuk655kpqb8hckd1dtt7v7a7nio"

# 휴일 리스트 (예시)
holidays = []

# 세부 업무 추천 매칭표
subtask_suggestions = {
    "컨텐츠": ["목차 작성", "경쟁사 분석", "타겟 설정"],
    "촬영": ["촬영 리스트 작성", "소품 준비", "숏폼 영상 촬영", "롱폼 영상 촬영", "제품 사진 촬영", "제품 홍보영상 촬영"],
    "디자인": ["로고 디자인", "패키지 디자인", "상세페이지 디자인", "명함 디자인", "렌딩페이지 디자인", "카드뉴스 디자인"],
    "인스타그램": ["숏폼 촬영", "카드뉴스 기획"],
    "유튜브": ["컨텐츠 기획", "영상 업로드"],
    "IR": ["기획", "제안서 작성", "경쟁사 분석", "타겟 분석"]
}

# 기한 계산 함수
def calculate_due_date(days):
    if not days:
        return "ASAP"
    today = datetime.date.today()
    delta = datetime.timedelta(days=1)
    while days > 0:
        today += delta
        if today.weekday() < 5 and today not in holidays:
            days -= 1
    return today.strftime('%Y-%m-%d (%a)')

# 담당자 자동배정 함수
def assign_task(task_name):
    task_name = task_name.lower()
    if any(keyword in task_name for keyword in ["콘텐츠", "기획", "촬영", "레시피", "sns", "마케팅", "분석", "보고서"]):
        return "이윤성"
    elif any(keyword in task_name for keyword in ["제품", "상품", "패키지", "촬영 세팅", "디자인", "편집", "영상"]):
        return "권희용"
    else:
        if len(task_name) <= 15:
            return "이윤성"
        else:
            return "권희용"

# Streamlit 메인 함수
def main():
    st.title("Glory BPM - 업무 입력")

    if 'tasks' not in st.session_state:
        st.session_state.tasks = []

    if 'task_counter' not in st.session_state:
        st.session_state.task_counter = 1

    st.subheader("업무 추가")

    for i in range(st.session_state.task_counter):
        with st.form(key=f"form_{i}"):
            st.markdown(f"### 업무 {i+1}")

            cols = st.columns([2, 1])
            with cols[0]:
                task_name = st.text_input("업무명 입력", key=f"task_{i}")
                st.caption("(자유로운 문장으로 작성)")
            with cols[1]:
                due_days = st.text_input("기한 입력", key=f"due_{i}")
                st.caption("(X일, 공백=기한 없음)")
                due_preview = calculate_due_date(int(due_days)) if due_days.isdigit() else "ASAP"
                st.caption(f"예상 기한: {due_preview}")

            suggested = []
            if task_name:
                for keyword, suggestions in subtask_suggestions.items():
                    if keyword in task_name:
                        if st.button("확인", key=f"confirm_{i}"):
                            suggested = st.multiselect("추가 제안 업무 선택", suggestions, key=f"sub_{i}")
                        break

            submitted = st.form_submit_button("업무 저장")

            if submitted:
                assigned_to = assign_task(task_name)
                sub_tasks = st.session_state.get(f"sub_{i}", [])
                task_data = {
                    "task_name": task_name,
                    "due_date": due_preview,
                    "sub_tasks": sub_tasks,
                    "assigned_to": assigned_to,
                    "status": "pending",
                    "created_at": datetime.datetime.now().isoformat()
                }
                st.session_state.tasks.append(task_data)
                st.success(f"업무 '{task_name}' 저장 완료! 담당자: {assigned_to}")

    st.button("+ 추가 업무 입력", on_click=lambda: st.session_state.update(task_counter=st.session_state.task_counter + 1))

    st.divider()

    if st.button("업무배정 실행"):
        if not st.session_state.tasks:
            st.error("입력된 업무가 없습니다.")
        else:
            try:
                payload = {"tasks": st.session_state.tasks}
                response = requests.post(WEBHOOK_URL, json=payload)
                if response.status_code == 200:
                    st.success(f"총 {len(st.session_state.tasks)}건의 업무가 메이크로 전송되었습니다.")
                else:
                    st.error(f"메이크 전송 실패: {response.status_code}")
            except Exception as e:
                st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()

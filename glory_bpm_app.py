import streamlit as st
import datetime

st.set_page_config(page_title="Glory BPM", page_icon="🚀", layout="wide")

# 휴일 리스트 (예시)
holidays = []

# 세부 업무 추천 매칭표
subtask_suggestions = {
    "콘텐츠": ["목차 작성", "경쟁사 분석", "타겟 설정"],
    "촬영": ["촬영 리스트 작성", "소품 준비", "숏폼 영상 촬영", "롱폼 영상 촬영", "제품 사진 촬영", "제품 홍보영상 촬영"],
    "디자인": ["로고 디자인", "패키지 디자인", "상세페이지 디자인", "명함 디자인", "렌딩페이지 디자인", "카드뉴스 디자인"],
    "인스타그램": ["숏폼 촬영", "카드뉴스 기획"],
    "유튜브": ["컨텐츠 기획", "영상 업로드"],
    "IR": ["기획", "제안서작성", "경쟁사 분석", "타켓 분석"]
}

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

def main():
    st.title("Glory BPM - 업무 입력")

    if 'tasks' not in st.session_state:
        st.session_state.tasks = []

    st.subheader("업무 추가")

    if 'task_counter' not in st.session_state:
        st.session_state.task_counter = 1

    for i in range(st.session_state.task_counter):
        with st.form(key=f"form_{i}"):
            st.markdown(f"### 업무 {i+1}")

            # 🔵 1. 업무명 입력
            task_name = st.text_input("업무명 입력", key=f"task_{i}")

            # 🔵 2. 기한 입력
            due_days = st.text_input("기한 입력 (X일, 비우면 기한 없음)", key=f"due_{i}")
            due_preview = calculate_due_date(int(due_days)) if due_days.isdigit() else "기한 없음"
            st.caption(f"예상 기한: {due_preview}")

            # 🔵 3. (수정된 부분) task_name이 입력된 경우에만 추가업무 제안
            suggested = []
            if task_name:
                for keyword, suggestions in subtask_suggestions.items():
                    if keyword in task_name:
                        suggested = st.multiselect("추가 제안 업무 선택", suggestions, key=f"sub_{i}")
                        break

            # 🔵 4. 저장 버튼
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

    # 업무 추가 버튼
    st.button("+ 추가 업무 입력", on_click=lambda: st.session_state.update(task_counter=st.session_state.task_counter + 1))

    st.divider()

    # 업무배정 실행 버튼
    if st.button("업무배정 실행"):
        if not st.session_state.tasks:
            st.error("입력된 업무가 없습니다.")
        else:
            st.success(f"총 {len(st.session_state.tasks)}건의 업무가 저장되었습니다.")
            for task in st.session_state.tasks:
                st.write(f"업무명: {task['task_name']}")
                st.write(f"담당자: {task['assigned_to']}")
                st.write(f"기한: {task['due_date']}")
                if task['sub_tasks']:
                    st.write(f"세부 업무: {', '.join(task['sub_tasks'])}")
                else:
                    st.write("세부 업무: (없음)")
                st.divider()

import streamlit as st
import datetime
import requests

st.set_page_config(page_title="Glory BPM", page_icon="🚀", layout="wide")

# 휴일 리스트
holidays = []

# 세부 업무 추천 매칭표
subtask_suggestions = {
    "콘텐츠": ["목차 작성", "경쟁사 분석", "타겟 설정"],
    "사진": ["사진 찍기", "소품 준비"],
    "사진카드": ["화려한 카드 포인트", "사진 카드 포인트"]
}

# 기한계산

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

# 업무 분할

def assign_task(task_name):
    task_name = task_name.lower()
    if any(keyword in task_name for keyword in ["콘텐츠", "계획", "사진", "sns", "링크"]):
        return "이윤성"
    else:
        return "권희용"

# 메이크 전송 함수

def send_to_webhook(task_data):
    webhook_url = "https://hook.eu2.make.com/spsrabuk655kpqb8hckd1dtt7v7a7nio"
    payload = {"tasks": task_data}
    headers = {"Content-Type": "application/json"}
    requests.post(webhook_url, json=payload, headers=headers)

# 메인

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

            cols = st.columns([3, 1])
            with cols[0]:
                task_name = st.text_input("업무명 입력", key=f"task_{i}")
                st.caption("(자유로운 문장으로 작성)")
            with cols[1]:
                due_days = st.text_input("기한 입력", key=f"due_{i}")
                st.caption("(X일, 공백=기한 없음)")

            due_preview = calculate_due_date(int(due_days)) if due_days.isdigit() else "ASAP"
            st.caption(f"예상 기한: {due_preview}")

            button_cols = st.columns([1, 1])

            confirm_clicked = button_cols[0].form_submit_button("확인")
            save_clicked = button_cols[1].form_submit_button("업무 저장")

            suggested = []
            if confirm_clicked:
                if task_name:
                    for keyword, suggestions in subtask_suggestions.items():
                        if keyword in task_name:
                            suggested = st.multiselect("추가 제안 업무 선택", suggestions, key=f"sub_{i}")
                            break

            if save_clicked:
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
                st.success(f"'{task_name}' 업무 저장 완료")

    if st.button("추가 업무 입력"):
        st.session_state.task_counter += 1

    st.divider()

    if st.button("업무배정 실행"):
        if not st.session_state.tasks:
            st.error("입력된 업무가 없습니다.")
        else:
            st.success(f"총 {len(st.session_state.tasks)}개 업무가 저장되었습니다.")
            for task in st.session_state.tasks:
                st.write(f"업무명: {task['task_name']}")
                st.write(f"담당자: {task['assigned_to']}")
                st.write(f"기한: {task['due_date']}")
                if task['sub_tasks']:
                    st.write(f"세부 업무: {', '.join(task['sub_tasks'])}")
                else:
                    st.write("세부 업무: (없음)")
                st.divider()
            send_to_webhook(st.session_state.tasks)

if __name__ == "__main__":
    main()

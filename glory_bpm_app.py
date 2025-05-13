import streamlit as st
import datetime

st.set_page_config(page_title="Glory BPM", page_icon="🚀", layout="wide")

# --- 기존 함수/코드들 유지 ---

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
            task_name = st.text_input("업무명 입력", key=f"task_{i}")
            due_days = st.text_input("기한 입력 (X일, 비우면 기한 없음)", key=f"due_{i}")
            due_preview = calculate_due_date(int(due_days)) if due_days.isdigit() else "기한 없음"
            st.caption(f"예상 기한: {due_preview}")

            suggested = []
            for keyword, suggestions in subtask_suggestions.items():
                if keyword in task_name:
                    suggested = st.multiselect("추가 제안 업무 선택", suggestions, key=f"sub_{i}")
                    break

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

    st.button("+ 추가 업무 입력", on_click=lambda: st.session_state.update(task_counter=st.session_state.task_counter + 1))

    st.divider()

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

import streamlit as st
import datetime
import requests

st.set_page_config(page_title="Glory BPM", page_icon="🚀", layout="centered")

# 휴일 리스트 (필요시 추가)
holidays = []

# 세부 업무 추천 매칭표
subtask_suggestions = {
    "콘텐츠": ["목차 작성", "경쟁사 분석", "타겟 설정"],
    "촬영": ["촬영 리스트 작성", "소품 준비", "숏폼 영상 촬영", "롱폼 영상 촬영", "제품 사진 촬영", "제품 홍보영상 촬영"],
    "디자인": ["로고 디자인", "패키지 디자인", "상세페이지 디자인", "명함 디자인", "랜딩페이지 디자인", "카드뉴스 디자인"],
    "인스타그램": ["숏폼 촬영", "카드뉴스 기획"],
    "유튜브": ["컨텐츠 기획", "영상 업로드"],
    "IR": ["기획", "제안서작성", "경쟁사 분석", "타겟 분석"]
}

# 메이크 Webhook URL
make_webhook_url = "https://hook.eu2.make.com/spsrabuk655kpqb8hckd1dtt7v7a7nio"

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

# 담당자 배정 함수
def assign_task(task_name):
    task_name = task_name.lower()
    if any(keyword in task_name for keyword in ["콘텐츠", "기획", "촬영 준비", "레시피", "sns", "마케팅", "분석", "보고서"]):
        return "이윤성"
    elif any(keyword in task_name for keyword in ["제품", "상품", "패키지", "촬영 세팅", "디자인", "편집", "영상"]):
        return "권희용"
    else:
        return "이윤성" if len(task_name) <= 15 else "권희용"

# 앱 메인
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
                        if st.form_submit_button("확인", key=f"confirm_{i}"):
                            suggested = st.multiselect("추가 제안 업무 선택", suggestions, key=f"sub_{i}")
                        break

            # 저장 버튼
            if st.form_submit_button("업무 저장", key=f"save_{i}"):
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

    if st.button("+ 추가 업무 입력"):
        st.session_state.task_counter += 1

    st.divider()

    if st.button("업무배정 실행"):
        if not st.session_state.tasks:
            st.error("입력된 업무가 없습니다.")
        else:
            payload = {"tasks": st.session_state.tasks}
            try:
                response = requests.post(make_webhook_url, json=payload)
                if response.status_code == 200:
                    st.success(f"총 {len(st.session_state.tasks)}건의 업무가 저장되어 전송되었습니다.")
                    for task in st.session_state.tasks:
                        st.write(f"**업무명:** {task['task_name']}")
                        st.write(f"**담당자:** {task['assigned_to']}")
                        st.write(f"**기한:** {task['due_date']}")
                        st.write(f"**세부 업무:** {', '.join(task['sub_tasks']) if task['sub_tasks'] else '(없음)'}")
                        st.divider()
                    st.session_state.tasks.clear()
                else:
                    st.error(f"전송 실패: {response.status_code} {response.text}")
            except Exception as e:
                st.error(f"에러 발생: {e}")

if __name__ == "__main__":
    main()

import streamlit as st
import json

# 세션 상태 초기화
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'jsonl_data' not in st.session_state:
    st.session_state['jsonl_data'] = ""
if 'current_index' not in st.session_state:
    st.session_state['current_index'] = 1  # 현재 항목 번호

def add_message_area(index):
    st.markdown(f"### {st.session_state['current_index']}번째 항목")  # 현재 항목 번호 출력
    with st.container():
        role = st.selectbox("Role", ["system", "assistant", "user"], key=f"role_{index}")
        content = st.text_area("Content", key=f"content_{index}")
        st.session_state['messages'][index] = {"role": role, "content": content}

st.title("JSONL Message Creator")

# '+' 버튼으로 메시지 입력 영역 추가
if st.button("Adding the prompt"):
    st.session_state['messages'].append({})

# 동적으로 메시지 입력 영역 생성
for i in range(len(st.session_state['messages'])):
    add_message_area(i)

# '저장' 버튼
if st.button("Save"):
    # 현재까지의 메시지를 JSON 형태로 화면에 표시
    current_json = {"messages": [message for message in st.session_state['messages'] if message]}
    st.json(current_json)

    # JSONL 파일 업데이트
    new_jsonl = json.dumps(current_json, ensure_ascii=False)
    st.session_state['jsonl_data'] += new_jsonl + "\n"

# '다음' 버튼
if st.button("Next"):
    # 현재 항목 번호 증가
    st.session_state['current_index'] += 1

    # 메시지 초기화 및 페이지 상단으로 스크롤
    st.session_state['messages'] = []
    st.experimental_rerun()

# 'Download JSONL' 버튼
if st.button("작업 완료"):
    st.download_button(label="Download JSONL", data=st.session_state['jsonl_data'], file_name="messages.jsonl", mime="text/plain")

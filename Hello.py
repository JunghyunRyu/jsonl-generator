import streamlit as st
import json

# 세션 상태 초기화
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'jsonl_data' not in st.session_state:
    st.session_state['jsonl_data'] = ""

def add_message_area(index):
    with st.container():
        role_key = f"role_{index}"
        content_key = f"content_{index}"

        role = st.selectbox("Role", ["system", "user", "assistant"], key=role_key)
        content = st.text_area("Content", key=content_key)

        st.session_state['messages'][index] = {"role": role, "content": content}

st.title("JSONL Message Creator")

if st.button("Adding the prompt"):
    st.session_state['messages'].append({})

for i in range(len(st.session_state['messages'])):
    add_message_area(i)

if st.button("Save"):
    # 현재 메시지를 JSONL 형식으로 저장
    current_json = {"messages": [message for message in st.session_state['messages'] if message]}
    new_jsonl = json.dumps(current_json, ensure_ascii=False)
    st.session_state['jsonl_data'] += new_jsonl + "\n"

    # UI 초기화
    st.session_state['messages'] = []
    st.rerun()

# 'Download JSONL' 버튼
if st.button("작업 완료"):
    st.download_button(label="Download JSONL", data=st.session_state['jsonl_data'], file_name="messages.jsonl", mime="text/plain")

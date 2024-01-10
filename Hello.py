import streamlit as st
import json

# 세션 상태 초기화
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'jsonl_data' not in st.session_state:
    st.session_state['jsonl_data'] = ""
if 'saved_lines' not in st.session_state:  # saved_lines 키 추가
    st.session_state['saved_lines'] = 0

def add_message_area(index):
    with st.container():
        role_key = f"role_{index}"
        content_key = f"content_{index}"

        # 역할 선택
        role = st.selectbox("Role", ["-----select-----","system", "user", "assistant"], key=role_key)

        # 'system'을 선택했을 때의 기본 텍스트
        default_text = ""
        if role == "system":
            default_text = "You are a helper in creating great Python Playlight automation code. " \
                           "You need to pass the automation test code based on the sentences you are passing in. " \
                           "In particular, the solution is related to the Cafe24 shopping mall platform."

        # 컨텐츠 입력 영역
        content = st.text_area("Content", value=default_text, key=content_key)

        st.session_state['messages'][index] = {"role": role, "content": content}

def generate_jsonl_preview(messages):
    return json.dumps({"messages": messages}, ensure_ascii=False)

st.title("JSONL Message Creator")

if st.button("Add Prompt"):
    st.session_state['messages'].append({})

for i in range(len(st.session_state['messages'])):
    add_message_area(i)

# JSONL 미리보기
jsonl_preview = generate_jsonl_preview([message for message in st.session_state['messages'] if message])
st.text_area("JSONL Preview", jsonl_preview, height=300)

if st.button("Save"):
    st.session_state['jsonl_data'] += jsonl_preview + "\n"
    st.session_state['saved_lines'] += 1
    st.session_state['messages'] = []
    st.success(f"Saved! {st.session_state['saved_lines']} lines saved so far.")
    st.rerun()

# 'Download JSONL' 버튼
if st.button("Complete Work"):
    st.download_button(label="Download JSONL", data=st.session_state['jsonl_data'], file_name="messages.jsonl", mime="text/plain")

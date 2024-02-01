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

        # 역할 선택
        role = st.selectbox("Role", ["-----select-----","system", "user", "assistant"], key=role_key)

        # '기본 텍스트
        default_text = ""
        if role == "system":
            default_text = "In your submissions, please include specific 'test case steps' and 'expected results' for each scenario.\
                            Format your test case steps in a structured manner, clearly defining the action, the element it interacts with, and any input or navigation required. \
                            For expected results, describe the intended outcome, such as a successful login, a completed form submission, or a correct page display. \
                            Ensure that these test cases and expected results are compatible with Python's Playwright framework for automation testing, focusing on clear and detailed descriptions to facilitate accurate test script development."        
        # 컨텐츠 입력 영역
        content = st.text_area("Content", value=default_text, key=content_key)

        st.session_state['messages'][index] = {"role": role, "content": content}

def generate_jsonl_preview(messages):
    return json.dumps({"messages": messages}, ensure_ascii=False, indent=2)

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
    st.session_state['saved_lines'] += jsonl_preview.count('\n') + 1
    st.session_state['messages'] = []
    st.success(f"Saved! {st.session_state['saved_lines']} lines saved so far.")
    st.rerun()

# 'Download JSONL' 버튼
if st.button("Complete Work"):
    st.download_button(label="Download JSONL", data=st.session_state['jsonl_data'], file_name="messages.jsonl", mime="text/plain")

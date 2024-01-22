import streamlit as st
import json

# 세션 상태 초기화
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'jsonl_data' not in st.session_state:
    st.session_state['jsonl_data'] = ""
if 'saved_lines' not in st.session_state:  # saved_lines 키 추가
    st.session_state['saved_lines'] = 0

def add_message_area(index,default_role="-----select-----"):
    with st.container():
        role_key = f"role_{index}"
        content_key = f"content_{index}"

        # 역할 선택
        #role = st.selectbox("Role", ["-----select-----","system", "user", "assistant"], key=role_key)
        # 역할 선택 (디폴트 값 설정)
        role = st.selectbox("Role", ["-----select-----", "system", "user", "assistant"], 
                            index=["-----select-----", "system", "user", "assistant"].index(default_role), 
                            key=role_key)        

        # 'system'을 선택했을 때의 기본 텍스트
        default_text = ""
        if role == "system":
            default_text = "You are currently engaged in a web page automation testing process using Python's Playwright framework. " \
                           "Your task is to comprehend the requirements presented to you and provide the corresponding Python Playwright code snippets as a solution." \
                           "The response should strictly consist of Python Playwright code fragments that fulfill the specific automation tasks requested."

        # 컨텐츠 입력 영역
        content = st.text_area("Content", value=default_text, key=content_key)

        st.session_state['messages'][index] = {"role": role, "content": content}

def generate_jsonl_preview(messages):
    return json.dumps({"messages": messages}, ensure_ascii=False)

# 특정 역할의 단일 메시지 추가 함수
def add_single_message(role):
    st.session_state['messages'].append({"role": role, "content": ""})

# 사이드바에 버튼 배치
with st.sidebar:
    st.title("Add Prompts")
    if st.button("Add Prompt"):
        st.session_state['messages'].append({"role": "system", "content": ""})
        st.session_state['messages'].append({"role": "user", "content": ""})
        st.session_state['messages'].append({"role": "assistant", "content": ""})
        #st.session_state['messages'].append({})
    if st.button("Add Single System Prompt"):
        add_single_message("system")
    if st.button("Add Single User Prompt"):
        add_single_message("user")
    if st.button("Add Single Assistant Prompt"):
        add_single_message("assistant")


st.title("JSONL Message Creator")

for i, message in enumerate(st.session_state['messages']):
    add_message_area(i, default_role=message.get("role", "-----select-----"))

# for i in range(len(st.session_state['messages'])):
#     add_message_area(i)

# JSONL 미리보기
jsonl_preview = generate_jsonl_preview([message for message in st.session_state['messages'] if message])
st.text_area("JSONL Preview", jsonl_preview, height=300)
# 사이드바에 버튼 배치
with st.sidebar:
    if st.button("Save"):
        st.session_state['jsonl_data'] += jsonl_preview + "\n"
        st.session_state['saved_lines'] += 1
        st.session_state['messages'] = []
        st.success(f"Saved! {st.session_state['saved_lines']} lines saved so far.")
        st.rerun()
    # 'Download JSONL' 버튼
    if st.button("Complete Work"):
        st.download_button(label="Download JSONL", data=st.session_state['jsonl_data'], file_name="messages.jsonl", mime="text/plain")




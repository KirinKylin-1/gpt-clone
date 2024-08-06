import streamlit as st
from langchain.memory import ConversationBufferMemory

from chater_utils import get_chat_response

st.markdown("<h1 style='text-align: center;'>💬 谈天说地</h1>", unsafe_allow_html=True)

with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API Key：", type="password")
    st.markdown("[获取OpenAI API key](https://platform.openai.com/account/api-keys)")

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    st.session_state["messages"] = [{"role": "ai",
                                     "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}]

# 定义一个用于放置按钮的容器
button_container = st.empty()

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()
if prompt:
    if not openai_api_key:
        st.info("请输入你的OpenAI API Key")
        st.stop()
    st.session_state["messages"].append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    with st.spinner("AI正在思考中，请稍等..."):
        response = get_chat_response(prompt, st.session_state["memory"],
                                     openai_api_key)
    msg = {"role": "ai", "content": response}
    st.session_state["messages"].append(msg)
    st.chat_message("ai").write(response)

# 在按钮容器中创建并放置'清空聊天记录'按钮
clear_button = button_container.button("清空聊天记录", key='clear_button')
if clear_button:
    st.session_state["messages"] = [{"role": "ai",
                                     "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}]
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    # 使用 st.rerun() 替代
    st.rerun()
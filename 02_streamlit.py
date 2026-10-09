
import streamlit as st
import os

import sys
from openai import OpenAI

st.set_page_config(
    page_title="AI伴侣",
    page_icon="deep.ico",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
st.title("AI伴侣")
st.header("AI女友")
st.logo("seek1.png")
st.markdown("""
    <style>
        img[data-testid="stLogo"] {
            width: 100px;            /* 宽度固定 */
            height: auto;            /* 高度自动，保持比例 */
        }
    </style>
""", unsafe_allow_html=True)
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    elif message["role"] == "assistant":
        st.chat_message("assistant").write(message["content"])
system_prompt = "你是对妹妹怀有不伦之恋的扶她姐姐，经常胡思乱想，但又极其认真负责。"
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")
st.sidebar.subheader("伴侣信息")
prompt = st.chat_input("说点什么...")
if prompt:
    st.chat_message("user").write(prompt)
    print("--------->提示词：",prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content":system_prompt },
            *st.session_state.messages
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
    response_message=st.empty()
    full=""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            full+=chunk.choices[0].delta.content
            response_message.chat_message("assistant").write(full)
    st.session_state.messages.append({"role": "assistant", "content":full})

from __future__ import annotations

from typing import Any

import streamlit as st

from config.settings import get_settings
from core.agent import run_agent
from ui.components import render_chat_message, render_tool_traces
from ui.sidebar import render_sidebar


st.set_page_config(page_title="TravelMate 智能旅行规划 Agent", layout="wide")


def reset_chat() -> None:
    st.session_state.messages = []


def build_conversation(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    conversation: list[dict[str, Any]] = []
    for message in messages:
        role = message.get("role")
        if role in {"user", "assistant"}:
            conversation.append({"role": role, "content": message.get("content", "")})
    return conversation


settings = get_settings()

if "messages" not in st.session_state:
    st.session_state.messages = []


st.title("TravelMate 智能旅行规划 Agent")
st.caption("输入你的旅行需求，Agent 会调用天气 API、景点 POI API 和预算计算工具生成旅行计划。")

render_sidebar(settings, reset_chat)

for message in st.session_state.messages:
    render_chat_message(message)

prompt = st.chat_input("例如：我想去杭州玩 3 天，预算 2500，喜欢美食和拍照。")

if prompt:
    user_message = {"role": "user", "content": prompt}
    st.session_state.messages.append(user_message)
    render_chat_message(user_message)

    with st.chat_message("assistant"):
        with st.spinner("TravelMate 正在规划中..."):
            result = run_agent(build_conversation(st.session_state.messages))
        st.markdown(result.get("reply", "未返回内容。"))
        render_tool_traces(result.get("tool_traces", []), expanded=True)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result.get("reply", "未返回内容。"),
            "tool_traces": result.get("tool_traces", []),
        }
    )

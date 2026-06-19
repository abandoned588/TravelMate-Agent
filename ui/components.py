from __future__ import annotations

import json
from typing import Any

import streamlit as st


def render_tool_traces(tool_traces: list[dict[str, Any]], expanded: bool = False) -> None:
    if not tool_traces:
        return

    with st.expander("查看本轮工具调用记录", expanded=expanded):
        for trace in tool_traces:
            st.markdown(f"**Tool:** `{trace.get('tool_name', 'unknown')}`")
            st.code(
                json.dumps(trace.get("arguments", {}), ensure_ascii=False, indent=2),
                language="json",
            )
            st.write(f"Result Summary: {trace.get('result_summary', '无摘要')}")
            preview = trace.get("raw_result_preview")
            if preview:
                st.caption(preview)


def render_chat_message(message: dict[str, Any]) -> None:
    role = message.get("role", "assistant")
    with st.chat_message(role):
        st.markdown(message.get("content", ""))
        render_tool_traces(message.get("tool_traces", []), expanded=False)


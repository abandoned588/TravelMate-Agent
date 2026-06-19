from __future__ import annotations

import streamlit as st

from config.settings import Settings


EXAMPLE_PROMPTS = [
    "我从郑州出发，想去杭州玩 3 天，预算 2500 元，喜欢美食、拍照，不想太累，帮我规划一下。",
    "我想去成都玩 2 天，预算 1200，喜欢美食和历史文化，帮我安排轻松一点的路线。",
    "帮我把刚才的行程保存下来。",
]


def render_sidebar(settings: Settings, on_clear) -> None:
    with st.sidebar:
        st.subheader("运行状态")
        st.write(f"模型名称：`{settings.model_name}`")
        st.write("LLM 配置：" + ("已配置" if settings.has_llm_credentials else "未配置"))
        st.write("高德 POI Key：" + ("已配置" if settings.has_amap_key else "未配置"))
        st.write("Geoapify Key：" + ("已配置" if settings.has_geoapify_key else "未配置"))

        if not settings.has_llm_credentials:
            st.warning("请先在 `.env` 中配置 OPENAI_API_KEY、OPENAI_BASE_URL 和 MODEL_NAME。")
        elif not settings.has_amap_key:
            st.info("未配置 AMAP_API_KEY 时，景点查询会如实返回错误，不会伪造结果。")

        st.markdown("**示例输入**")
        for prompt in EXAMPLE_PROMPTS:
            st.code(prompt)

        st.button("清空对话", on_click=on_clear, use_container_width=True)


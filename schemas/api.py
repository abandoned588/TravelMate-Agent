from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ChatMessageInput(BaseModel):
    role: Literal["user", "assistant"] = Field(..., description="消息角色，网页侧通常只传 user 或 assistant。")
    content: str = Field(..., description="消息文本内容。")


class ChatRequest(BaseModel):
    messages: list[ChatMessageInput] = Field(..., description="当前会话的消息列表。")


class ChatResponse(BaseModel):
    success: bool = Field(..., description="是否成功完成本次对话调用。")
    reply: str = Field(..., description="Agent 返回给前端的最终回复。")
    tool_traces: list[dict[str, Any]] = Field(default_factory=list, description="本轮工具调用记录。")


class SaveItineraryRequest(BaseModel):
    title: str = Field(..., description="行程标题。")
    content: str = Field(..., description="完整 Markdown 行程内容。")


class ApiResponse(BaseModel):
    success: bool = Field(..., description="接口是否成功。")
    message: str | None = Field(default=None, description="接口附加说明。")
    data: dict[str, Any] | list[dict[str, Any]] | None = Field(default=None, description="接口返回数据。")


from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class ToolTrace(BaseModel):
    timestamp: datetime = Field(..., description="When the tool call happened.")
    tool_name: str = Field(..., description="Tool name.")
    arguments: dict[str, Any] = Field(default_factory=dict, description="Tool call arguments.")
    success: bool = Field(..., description="Whether the tool call succeeded.")
    result_summary: str = Field(..., description="Summary of the tool result.")
    raw_result_preview: str | None = Field(default=None, description="Short preview of the raw tool result.")


class ChatTurn(BaseModel):
    role: Literal["system", "user", "assistant", "tool"] = Field(..., description="Message role.")
    content: str = Field(..., description="Message content.")
    tool_name: str | None = Field(default=None, description="Tool name when role is tool.")
    tool_call_id: str | None = Field(default=None, description="OpenAI tool call id.")


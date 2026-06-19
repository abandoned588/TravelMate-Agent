from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ToolResult(BaseModel):
    success: bool = Field(..., description="工具执行是否成功")
    data: dict[str, Any] | list[dict[str, Any]] | None = Field(default=None, description="工具返回的数据主体")
    summary: str | None = Field(default=None, description="工具返回摘要")
    error: str | None = Field(default=None, description="工具失败时的错误说明")


class WeatherForecastOutput(ToolResult):
    data: dict[str, Any] | None = Field(default=None, description="天气查询结果")


class AttractionSearchOutput(ToolResult):
    data: dict[str, Any] | None = Field(default=None, description="景点与 POI 查询结果")


class BudgetOutput(ToolResult):
    data: dict[str, Any] | None = Field(default=None, description="预算计算结果")


class SaveItineraryOutput(ToolResult):
    data: dict[str, Any] | None = Field(default=None, description="行程保存结果")


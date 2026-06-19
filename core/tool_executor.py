from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from config.settings import TOOL_TRACE_PATH, ensure_project_directories
from core.exceptions import ToolExecutionError
from schemas.chat import ToolTrace
from tools.registry import execute_tool
from tools.utils import compact_preview, summarize_tool_result


def _model_dump(instance: Any) -> dict[str, Any]:
    if hasattr(instance, "model_dump"):
        return instance.model_dump(mode="json")
    return instance.dict()


def log_tool_trace(trace: ToolTrace) -> None:
    ensure_project_directories()
    with TOOL_TRACE_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(_model_dump(trace), ensure_ascii=False) + "\n")


def run_tool_call(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    try:
        result = execute_tool(tool_name, arguments)
    except Exception as exc:
        raise ToolExecutionError(f"Unhandled tool execution error: {exc}") from exc

    summary = summarize_tool_result(result)
    trace = ToolTrace(
        timestamp=datetime.now(),
        tool_name=tool_name,
        arguments=arguments,
        success=bool(result.get("success", False)),
        result_summary=summary,
        raw_result_preview=compact_preview(result),
    )
    log_tool_trace(trace)
    return {
        "success": bool(result.get("success", False)),
        "tool_name": tool_name,
        "result": result,
        "summary": summary,
        "trace": _model_dump(trace),
    }


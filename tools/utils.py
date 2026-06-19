from __future__ import annotations

import json
from typing import Any


WEATHER_CODE_LABELS = {
    0: "晴朗",
    1: "大体晴",
    2: "多云",
    3: "阴天",
    45: "有雾",
    48: "雾凇",
    51: "小毛毛雨",
    53: "毛毛雨",
    55: "较强毛毛雨",
    61: "小雨",
    63: "中雨",
    65: "大雨",
    71: "小雪",
    73: "中雪",
    75: "大雪",
    80: "阵雨",
    81: "较强阵雨",
    82: "暴雨阵雨",
    95: "雷暴",
}


def summarize_tool_result(result: dict[str, Any]) -> str:
    if result.get("summary"):
        return str(result["summary"])
    if not result.get("success", False):
        return str(result.get("error", "Tool call failed"))

    data = result.get("data")
    if isinstance(data, list):
        return f"Returned {len(data)} records."
    if isinstance(data, dict):
        if "pois" in data and isinstance(data["pois"], list):
            return f"Returned {len(data['pois'])} POIs."
        if "forecast" in data and isinstance(data["forecast"], list):
            return f"Returned {len(data['forecast'])} forecast days."
        return "Tool call succeeded."
    return "Tool call succeeded."


def safe_get(data: dict[str, Any] | None, key: str, default: Any = None) -> Any:
    if not isinstance(data, dict):
        return default
    return data.get(key, default)


def deduplicate_pois(pois: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    deduplicated: list[dict[str, Any]] = []
    for poi in pois:
        unique_key = str(poi.get("id") or f"{poi.get('name')}_{poi.get('address')}_{poi.get('location')}")
        if unique_key in seen:
            continue
        seen.add(unique_key)
        deduplicated.append(poi)
    return deduplicated


def compact_preview(result: dict[str, Any], limit: int = 300) -> str:
    try:
        text = json.dumps(result, ensure_ascii=False)
    except TypeError:
        text = str(result)
    return text if len(text) <= limit else text[: limit - 3] + "..."


from __future__ import annotations

from typing import Any

from config.settings import get_settings


def search_places(city: str, categories: list[str], limit: int) -> dict[str, Any]:
    settings = get_settings()
    if not settings.has_geoapify_key:
        return {"success": False, "error": "缺少 GEOAPIFY_API_KEY，当前未启用 Geoapify 备用查询。"}

    return {
        "success": False,
        "error": f"Geoapify 备用查询尚未启用。城市: {city}，分类: {', '.join(categories)}，limit: {limit}",
    }

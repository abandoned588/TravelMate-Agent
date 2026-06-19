from __future__ import annotations

from typing import Any

import requests

from config.settings import get_settings


AMAP_POI_URL = "https://restapi.amap.com/v3/place/text"


def search_poi(city: str, keyword: str, limit: int) -> dict[str, Any]:
    settings = get_settings()
    if not settings.has_amap_key:
        return {"success": False, "error": "缺少 AMAP_API_KEY，无法调用高德 POI API。"}

    try:
        response = requests.get(
            AMAP_POI_URL,
            params={
                "key": settings.amap_api_key,
                "keywords": keyword,
                "city": city,
                "citylimit": "true",
                "output": "json",
                "offset": limit,
            },
            timeout=settings.request_timeout,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        return {"success": False, "error": f"高德 POI 请求失败: {exc}"}
    except ValueError as exc:
        return {"success": False, "error": f"高德 POI 接口返回了无效 JSON: {exc}"}

    if payload.get("status") != "1":
        return {"success": False, "error": f"高德 POI API 返回失败: {payload.get('info', '未知错误')}"}

    pois = payload.get("pois") or []
    return {
        "success": True,
        "data": {"city": city, "keyword": keyword, "pois": pois},
        "summary": f"关键词“{keyword}”检索到 {len(pois)} 个 POI。",
    }


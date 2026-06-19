from __future__ import annotations

from typing import Any

from config.constants import DEFAULT_POI_LIMIT
from services.amap_client import search_poi
from services.cache_service import read_cache, write_cache
from tools.utils import deduplicate_pois


INTEREST_KEYWORDS: dict[str, list[str]] = {
    "美食": ["美食街", "小吃", "餐厅"],
    "拍照": ["景点", "公园", "地标"],
    "历史": ["博物馆", "古街", "寺庙", "历史建筑"],
    "历史文化": ["博物馆", "古街", "寺庙", "历史建筑"],
    "自然风景": ["公园", "湖", "山", "风景区"],
    "购物": ["商场", "步行街", "商圈"],
    "亲子": ["动物园", "科技馆", "亲子乐园"],
    "轻松路线": ["公园", "步行街", "咖啡馆"],
}


def _keywords_from_interests(interests: list[str]) -> list[str]:
    keywords: list[str] = []
    for interest in interests:
        keywords.extend(INTEREST_KEYWORDS.get(interest, [interest]))
    return list(dict.fromkeys(keywords))


def _normalize_poi(poi: dict[str, Any], keyword: str) -> dict[str, Any]:
    return {
        "id": poi.get("id"),
        "name": poi.get("name"),
        "type": poi.get("type"),
        "address": poi.get("address"),
        "location": poi.get("location"),
        "cityname": poi.get("cityname"),
        "adname": poi.get("adname"),
        "source": "AMap",
        "matched_keyword": keyword,
    }


def search_attractions(city: str, interests: list[str], limit: int = DEFAULT_POI_LIMIT) -> dict[str, Any]:
    """Search attractions and POIs from AMap according to the user's interests."""
    cache_key = f"{city}_{'-'.join(interests)}_{limit}"
    cached = read_cache("poi_cache", cache_key)
    if cached is not None:
        return {
            "success": True,
            "data": cached,
            "summary": cached.get("summary", f"已读取 {city} 的 POI 缓存。"),
        }

    keywords = _keywords_from_interests(interests)
    merged_pois: list[dict[str, Any]] = []
    for keyword in keywords:
        poi_result = search_poi(city, keyword, limit)
        if not poi_result.get("success"):
            return poi_result

        for poi in poi_result["data"].get("pois", []):
            merged_pois.append(_normalize_poi(poi, keyword))

    deduplicated = deduplicate_pois(merged_pois)[:limit]
    summary = f"{city} 共检索到 {len(deduplicated)} 个相关地点。"
    result_data = {
        "city": city,
        "interests": interests,
        "keywords": keywords,
        "pois": deduplicated,
        "summary": summary,
    }
    write_cache("poi_cache", cache_key, result_data)
    return {"success": True, "data": result_data, "summary": summary}


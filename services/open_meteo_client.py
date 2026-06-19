from __future__ import annotations

from typing import Any

import requests

from config.settings import get_settings


GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def geocode_city(city: str) -> dict[str, Any]:
    settings = get_settings()
    try:
        response = requests.get(
            GEOCODE_URL,
            params={"name": city, "count": 1, "language": "zh", "format": "json"},
            timeout=settings.request_timeout,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        return {"success": False, "error": f"Open-Meteo 地理编码请求失败: {exc}"}
    except ValueError as exc:
        return {"success": False, "error": f"Open-Meteo 地理编码返回了无效 JSON: {exc}"}

    results = payload.get("results") or []
    if not results:
        return {"success": False, "error": f"未能解析城市“{city}”的地理信息。"}

    item = results[0]
    return {
        "success": True,
        "data": {
            "name": item.get("name", city),
            "country": item.get("country"),
            "timezone": item.get("timezone"),
            "latitude": item.get("latitude"),
            "longitude": item.get("longitude"),
        },
        "summary": f"已解析 {city} 的经纬度信息。",
    }


def fetch_weather(latitude: float, longitude: float, days: int) -> dict[str, Any]:
    settings = get_settings()
    try:
        response = requests.get(
            FORECAST_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
                "forecast_days": days,
                "timezone": "auto",
            },
            timeout=settings.request_timeout,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        return {"success": False, "error": f"Open-Meteo 天气请求失败: {exc}"}
    except ValueError as exc:
        return {"success": False, "error": f"Open-Meteo 天气接口返回了无效 JSON: {exc}"}

    daily = payload.get("daily")
    if not isinstance(daily, dict):
        return {"success": False, "error": "Open-Meteo 天气接口未返回 daily 预报数据。"}

    return {
        "success": True,
        "data": {
            "timezone": payload.get("timezone"),
            "daily": daily,
        },
        "summary": f"已获取未来 {days} 天的天气预报。",
    }


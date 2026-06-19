from __future__ import annotations

from typing import Any

from services.cache_service import read_cache, write_cache
from services.open_meteo_client import fetch_weather, geocode_city
from tools.utils import WEATHER_CODE_LABELS


def get_weather_forecast(city: str, days: int) -> dict[str, Any]:
    """Query Open-Meteo geocoding and forecast APIs for a city's weather."""
    cache_key = f"{city}_{days}"
    cached = read_cache("weather_cache", cache_key)
    if cached is not None:
        return {
            "success": True,
            "data": cached,
            "summary": cached.get("summary", f"已读取 {city} 的天气缓存。"),
        }

    geocode_result = geocode_city(city)
    if not geocode_result.get("success"):
        return geocode_result

    geo = geocode_result["data"]
    weather_result = fetch_weather(geo["latitude"], geo["longitude"], days)
    if not weather_result.get("success"):
        return weather_result

    daily = weather_result["data"]["daily"]
    forecast: list[dict[str, Any]] = []
    for index, date in enumerate(daily.get("time", [])):
        code = daily.get("weather_code", [None])[index]
        forecast.append(
            {
                "date": date,
                "weather_code": code,
                "weather_text": WEATHER_CODE_LABELS.get(code, "未知天气"),
                "temperature_max": daily.get("temperature_2m_max", [None])[index],
                "temperature_min": daily.get("temperature_2m_min", [None])[index],
                "precipitation_probability_max": daily.get("precipitation_probability_max", [None])[index],
            }
        )

    result_data = {
        "city": geo["name"],
        "country": geo.get("country"),
        "timezone": geo.get("timezone") or weather_result["data"].get("timezone"),
        "latitude": geo["latitude"],
        "longitude": geo["longitude"],
        "forecast": forecast,
    }
    summary = f"{geo['name']}未来 {days} 天天气查询成功，共返回 {len(forecast)} 天预报。"
    result_data["summary"] = summary
    write_cache("weather_cache", cache_key, result_data)
    return {"success": True, "data": result_data, "summary": summary}


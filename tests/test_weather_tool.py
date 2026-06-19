import tools.weather as weather_module


def test_get_weather_forecast_formats_response(monkeypatch) -> None:
    monkeypatch.setattr(weather_module, "read_cache", lambda *args, **kwargs: None)
    monkeypatch.setattr(weather_module, "write_cache", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        weather_module,
        "geocode_city",
        lambda city: {
            "success": True,
            "data": {
                "name": city,
                "country": "China",
                "timezone": "Asia/Shanghai",
                "latitude": 30.2741,
                "longitude": 120.1551,
            },
        },
    )
    monkeypatch.setattr(
        weather_module,
        "fetch_weather",
        lambda latitude, longitude, days: {
            "success": True,
            "data": {
                "timezone": "Asia/Shanghai",
                "daily": {
                    "time": ["2026-06-12", "2026-06-13"],
                    "weather_code": [0, 2],
                    "temperature_2m_max": [30, 29],
                    "temperature_2m_min": [22, 21],
                    "precipitation_probability_max": [10, 20],
                },
            },
        },
    )

    result = weather_module.get_weather_forecast("Hangzhou", 2)

    assert result["success"] is True
    assert result["data"]["city"] == "Hangzhou"
    assert len(result["data"]["forecast"]) == 2
    assert result["data"]["forecast"][0]["weather_text"] == "晴朗"


def test_get_weather_forecast_bubbles_service_error(monkeypatch) -> None:
    monkeypatch.setattr(weather_module, "read_cache", lambda *args, **kwargs: None)
    monkeypatch.setattr(weather_module, "geocode_city", lambda city: {"success": False, "error": "lookup failed"})

    result = weather_module.get_weather_forecast("Nowhere", 2)

    assert result["success"] is False
    assert result["error"] == "lookup failed"


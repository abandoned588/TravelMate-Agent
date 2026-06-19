import tools.attractions as attractions_module


def test_search_attractions_merges_and_deduplicates(monkeypatch) -> None:
    monkeypatch.setattr(attractions_module, "read_cache", lambda *args, **kwargs: None)
    monkeypatch.setattr(attractions_module, "write_cache", lambda *args, **kwargs: None)

    def fake_search_poi(city: str, keyword: str, limit: int) -> dict:
        return {
            "success": True,
            "data": {
                "pois": [
                    {
                        "id": "poi-1",
                        "name": "West Lake",
                        "type": "scenic",
                        "address": "Hangzhou",
                        "location": "120.1,30.2",
                        "cityname": city,
                        "adname": "Xihu",
                    },
                    {
                        "id": "poi-1",
                        "name": "West Lake",
                        "type": "scenic",
                        "address": "Hangzhou",
                        "location": "120.1,30.2",
                        "cityname": city,
                        "adname": "Xihu",
                    },
                ]
            },
            "summary": f"{keyword} ok",
        }

    monkeypatch.setattr(attractions_module, "search_poi", fake_search_poi)

    result = attractions_module.search_attractions("Hangzhou", ["美食", "拍照"], limit=10)

    assert result["success"] is True
    assert result["data"]["city"] == "Hangzhou"
    assert len(result["data"]["pois"]) == 1


def test_search_attractions_returns_clear_error_when_amap_fails(monkeypatch) -> None:
    monkeypatch.setattr(attractions_module, "read_cache", lambda *args, **kwargs: None)
    monkeypatch.setattr(attractions_module, "write_cache", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        attractions_module,
        "search_poi",
        lambda city, keyword, limit: {"success": False, "error": "Missing AMAP_API_KEY"},
    )

    result = attractions_module.search_attractions("Hangzhou", ["美食"], limit=5)

    assert result["success"] is False
    assert "AMAP_API_KEY" in result["error"]


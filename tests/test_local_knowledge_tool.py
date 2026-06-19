from tools.local_knowledge import search_local_knowledge


def test_search_local_knowledge_returns_city_results() -> None:
    result = search_local_knowledge("Hangzhou", ["attraction", "food"], limit=4)

    assert result["success"] is True
    assert result["data"]["city"] == "Hangzhou"
    assert len(result["data"]["results"]) >= 2
    names = {row["name"] for row in result["data"]["results"]}
    assert "West Lake" in names


def test_search_local_knowledge_filters_by_query() -> None:
    result = search_local_knowledge("Zhengzhou", ["food"], query="night", limit=5)

    assert result["success"] is True
    assert any("Night Market" in row["name"] for row in result["data"]["results"])

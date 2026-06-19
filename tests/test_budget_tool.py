from tools.budget import calculate_budget


def test_calculate_budget_returns_expected_fields() -> None:
    result = calculate_budget(days=3, user_budget=2500, transport_cost=300)

    assert result["success"] is True
    assert result["data"]["hotel_total"] == 500
    assert result["data"]["food_total"] == 360
    assert result["data"]["total_cost"] == 1360
    assert "summary" in result


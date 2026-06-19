from __future__ import annotations

import json

from config.settings import get_settings
from tools.registry import execute_tool, get_tool_schemas


def main() -> None:
    settings = get_settings()
    print("TravelMate quick tool check")
    print("=" * 32)
    print(f"Model configured: {settings.has_llm_credentials}")
    print(f"AMap configured: {settings.has_amap_key}")
    print(f"Geoapify configured: {settings.has_geoapify_key}")
    print(f"Registered tools: {len(get_tool_schemas())}")

    budget_result = execute_tool(
        "calculate_budget",
        {"days": 3, "user_budget": 2500, "transport_cost": 300},
    )
    print("\n[Budget Tool]")
    print(json.dumps(budget_result, ensure_ascii=False, indent=2))

    save_result = execute_tool(
        "save_itinerary",
        {"title": "Quick Test Trip", "content": "## Day 1\n- Demo itinerary item"},
    )
    print("\n[Save Tool]")
    print(json.dumps(save_result, ensure_ascii=False, indent=2))

    if settings.has_amap_key:
        attractions_result = execute_tool(
            "search_attractions",
            {"city": "杭州", "interests": ["美食", "拍照"], "limit": 5},
        )
        print("\n[Attractions Tool]")
        print(json.dumps(attractions_result, ensure_ascii=False, indent=2))
    else:
        print("\n[Attractions Tool]")
        print("Skipped because AMAP_API_KEY is not configured.")

    print("\n[Weather Tool]")
    print("Run through the UI or a live script when network access is available.")


if __name__ == "__main__":
    main()


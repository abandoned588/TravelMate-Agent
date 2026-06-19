from __future__ import annotations

from typing import Any

from schemas.tool_inputs import (
    AttractionSearchInput,
    BudgetInput,
    LocalKnowledgeSearchInput,
    SaveItineraryInput,
    WeatherForecastInput,
)
from tools.attractions import search_attractions
from tools.budget import calculate_budget
from tools.itinerary import save_itinerary
from tools.local_knowledge import search_local_knowledge
from tools.weather import get_weather_forecast


TOOL_REGISTRY = {
    "get_weather_forecast": {
        "description": "Query upcoming weather for a city using Open-Meteo.",
        "input_model": WeatherForecastInput,
        "handler": get_weather_forecast,
    },
    "search_attractions": {
        "description": "Search attractions, food areas, and POIs for a city using AMap.",
        "input_model": AttractionSearchInput,
        "handler": search_attractions,
    },
    "search_local_knowledge": {
        "description": "Search the local CSV knowledge base for famous attractions and foods in a city. Use this before itinerary writing so the final plan reflects curated local knowledge.",
        "input_model": LocalKnowledgeSearchInput,
        "handler": search_local_knowledge,
    },
    "calculate_budget": {
        "description": "Estimate a trip budget and determine whether it exceeds the user's budget.",
        "input_model": BudgetInput,
        "handler": calculate_budget,
    },
    "save_itinerary": {
        "description": "Save the final itinerary as storage/outputs/itinerary.md.",
        "input_model": SaveItineraryInput,
        "handler": save_itinerary,
    },
}


def _model_schema(model: Any) -> dict[str, Any]:
    if hasattr(model, "model_json_schema"):
        return model.model_json_schema()
    return model.schema()


def _model_dump(instance: Any) -> dict[str, Any]:
    if hasattr(instance, "model_dump"):
        return instance.model_dump()
    return instance.dict()


def get_tool_schemas() -> list[dict[str, Any]]:
    schemas: list[dict[str, Any]] = []
    for tool_name, entry in TOOL_REGISTRY.items():
        schemas.append(
            {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": entry["description"],
                    "parameters": _model_schema(entry["input_model"]),
                },
            }
        )
    return schemas


def get_tool_mapping() -> dict[str, Any]:
    return {tool_name: entry["handler"] for tool_name, entry in TOOL_REGISTRY.items()}


def execute_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    entry = TOOL_REGISTRY.get(tool_name)
    if entry is None:
        return {"success": False, "error": f"Unknown tool: {tool_name}"}

    model = entry["input_model"]
    try:
        validated = model.model_validate(arguments) if hasattr(model, "model_validate") else model.parse_obj(arguments)
    except Exception as exc:
        return {"success": False, "error": f"Tool argument validation failed: {exc}"}

    payload = _model_dump(validated)
    return entry["handler"](**payload)

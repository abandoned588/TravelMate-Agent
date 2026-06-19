# Tool Design

## Overview

TravelMate exposes four tools to the LLM. Each tool returns a structured `dict` with at least:

- `success`
- `data` on success
- `summary`
- `error` on failure

## Weather Tool

- Entry point: `tools/weather.py`
- Name: `get_weather_forecast`
- Dependencies: `services/open_meteo_client.py`, `services/cache_service.py`

Responsibilities:

- Resolve city coordinates with Open-Meteo geocoding
- Fetch multi-day forecast data
- Normalize weather codes into readable labels
- Cache successful results

## Attractions Tool

- Entry point: `tools/attractions.py`
- Name: `search_attractions`
- Dependencies: `services/amap_client.py`, `services/cache_service.py`

Responsibilities:

- Map user interests into search keywords
- Query AMap POI search for each keyword
- Merge and deduplicate POI results
- Return a concise POI list with source metadata

## Budget Tool

- Entry point: `tools/budget.py`
- Name: `calculate_budget`

Responsibilities:

- Estimate hotel, food, ticket, and transport cost
- Compare total cost to user budget
- Provide simple advice based on remaining budget

## Itinerary Tool

- Entry point: `tools/itinerary.py`
- Name: `save_itinerary`

Responsibilities:

- Create the output directory if needed
- Save a Markdown itinerary
- Return the absolute saved path

## Registry

`tools/registry.py` is the single place that:

- registers tool schemas for the LLM
- maps tool names to Python handlers
- validates arguments with Pydantic models


# TravelMate-Agent

TravelMate is a course-demo travel planning agent built around DeepSeek's OpenAI-compatible function calling. It reads a user's travel request, calls external APIs for weather and POIs, estimates budget, saves the final itinerary to a local Markdown file, and also exposes a FastAPI backend for a future web frontend.

## Project Overview

- `app.py` provides a Streamlit chat interface.
- `api/app.py` provides an HTTP API layer for a future web frontend.
- `core/` handles model calls, tool execution, and tool-call logging.
- `services/` wraps external APIs such as Open-Meteo and AMap.
- `tools/` contains the business tools exposed to the LLM.
- `storage/logs/tool_trace.jsonl` records every tool call.
- `storage/outputs/itinerary.md` stores the saved itinerary.

## BYOA Requirements Mapping

This project covers the three BYOA must-haves:

1. Tool Use / Skills
   It implements four callable tools: weather lookup, attraction lookup, budget calculation, and itinerary saving.
2. Context Integration
   It connects the LLM with Open-Meteo, AMap, and the local filesystem through function calling.
3. Vibe Coding
   The project structure, schemas, API wrappers, tools, and Streamlit UI are AI-assisted, while the system prompt and orchestration rules are explicitly designed.

## Architecture

- `config/`
  Centralizes environment loading, paths, and constants.
- `schemas/`
  Defines Pydantic input and output models for tool calling and chat trace data.
- `services/`
  Wraps raw HTTP requests and cache access.
- `tools/`
  Converts external service data into stable tool outputs for the agent.
- `core/`
  Runs the DeepSeek-compatible chat loop, dispatches tools, and writes logs.
- `ui/`
  Renders sidebar, chat messages, and tool trace panels.

## Tool List

- `get_weather_forecast(city, days)`
  Uses Open-Meteo geocoding and forecast APIs.
- `search_attractions(city, interests, limit=10)`
  Uses the AMap POI API to search for attractions, food spots, and related places.
- `calculate_budget(days, user_budget, ...)`
  Estimates travel cost and checks whether the plan exceeds budget.
- `save_itinerary(title, content)`
  Saves a Markdown itinerary to `storage/outputs/itinerary.md`.

## Installation

1. Use Python 3.10 or 3.11 if possible. The current workspace is using Python 3.13, which may still work, but 3.10/3.11 is closer to the assignment target.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill in the required keys.

## Environment Variables

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL_NAME=deepseek-chat

AMAP_API_KEY=your_amap_api_key
GEOAPIFY_API_KEY=your_geoapify_api_key_optional
```

- `DEEPSEEK_API_KEY`, `DEEPSEEK_BASE_URL`, and `DEEPSEEK_MODEL_NAME` are required for the LLM.
- `AMAP_API_KEY` is required for attraction lookup.
- Open-Meteo does not require a key.
- `GEOAPIFY_API_KEY` is reserved for the optional fallback client.

## Run Commands

Start the Streamlit UI:

```bash
streamlit run app.py
```

Start the FastAPI backend:

```bash
uvicorn api.app:app --reload
```

Quick local tool check:

```bash
python scripts/quick_tool_test.py
```

Run tests:

```bash
pytest
```

API contract:

- See `docs/api.md`

## Example Inputs

Example 1:

```text
我从郑州出发，想去杭州玩 3 天，预算 2500 元，喜欢美食、拍照，不想太累，帮我规划一下。
```

Expected tool usage:

```text
get_weather_forecast(city="杭州", days=3)
search_attractions(city="杭州", interests=["美食", "拍照", "轻松路线"], limit=10)
calculate_budget(days=3, user_budget=2500, ...)
optional save_itinerary(...)
```

Example 2:

```text
我想去成都玩 2 天，预算 1200，喜欢美食和历史文化，帮我安排轻松一点的路线。
```

Example 3:

```text
帮我把刚才的行程保存下来。
```

Expected tool usage:

```text
save_itinerary(title=..., content=...)
```

## Screenshot Suggestions

- Sidebar showing model status and API-key status
- A full chat example with the final itinerary reply
- Expanded tool trace panel for one turn
- `storage/logs/tool_trace.jsonl`
- `storage/outputs/itinerary.md`

## Known Limitations

- Without a valid DeepSeek API key, the agent cannot produce model-driven travel plans.
- Without `AMAP_API_KEY`, the attraction tool returns a real error instead of fake POIs.
- The budget tool uses rule-based estimates rather than live transport or hotel pricing.
- The optional Geoapify client is reserved but not enabled as the default path.
.\.venv\Scripts\python.exe -m uvicorn api.app:app --reload

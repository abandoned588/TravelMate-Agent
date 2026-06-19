# TravelMate Agent Rules

## Project Overview

TravelMate is a focused travel-planning agent for coursework demos. It uses a DeepSeek-compatible model plus tool calling to combine weather, POI search, budget estimation, and itinerary saving.

## Build and Run Commands

- Install dependencies: `pip install -r requirements.txt`
- Configure `.env` from `.env.example`
- Run Streamlit UI: `streamlit run app.py`
- Run FastAPI backend: `uvicorn api.app:app --reload`
- Run tests: `pytest`
- Run local smoke check: `python scripts/quick_tool_test.py`

## Code Style

- Use clear, small modules with single responsibility.
- Keep UI logic in `app.py` and `ui/`.
- Keep HTTP API logic in `api/`.
- Keep orchestration in `core/`.
- Keep API calls in `services/`.
- Keep LLM-exposed tools in `tools/`.
- Return structured `dict` results from every tool.
- Set a timeout on every HTTP request.

## Tool Calling Rules

- Do not hardcode weather or attraction data in the codebase.
- Weather-related answers must call `get_weather_forecast`.
- Attraction or POI-related answers must call `search_attractions`.
- Budget judgments must call `calculate_budget`.
- Save/export requests must call `save_itinerary`.
- If an API fails, return the real error and do not fabricate data.

## Security Considerations

- Never commit real API keys.
- Read all runtime secrets from `.env`.
- Do not replace external API data with mock production results.
- Keep tool logs in `storage/logs/tool_trace.jsonl` for traceability.

## Testing Checklist

- `calculate_budget` returns a structured success payload.
- `save_itinerary` writes a Markdown file to `storage/outputs/itinerary.md`.
- `search_attractions` reports a clear error when `AMAP_API_KEY` is missing.
- `get_weather_forecast` can be tested with mocked service responses.
- `core/tool_executor.py` writes tool-call traces to `storage/logs/tool_trace.jsonl`.
- `streamlit run app.py` starts after dependencies are installed.

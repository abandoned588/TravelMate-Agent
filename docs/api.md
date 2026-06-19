# API Design

This document defines the HTTP API that the future web frontend should call. The browser should only call these endpoints and should never call OpenAI, Open-Meteo, or AMap directly.

## Base Rule

- Frontend -> TravelMate API
- TravelMate API -> `core/agent.py`
- `core/agent.py` -> `tools/`
- `tools/` -> `services/`
- `services/` -> external APIs

## 1. Health Check

`GET /api/health`

Purpose:

- check whether the backend is running
- expose basic configuration status for the frontend

Response example:

```json
{
  "success": true,
  "message": "TravelMate API is ready.",
  "data": {
    "model_name": "gpt-4o-mini",
    "llm_configured": true,
    "amap_configured": true,
    "geoapify_configured": false
  }
}
```

## 2. Chat Planning

`POST /api/chat`

Purpose:

- send the current conversation to the agent
- receive the final reply plus the tool traces from this round

Request body:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "我从郑州出发，想去杭州玩 3 天，预算 2500 元，喜欢美食、拍照，不想太累，帮我规划一下。"
    }
  ]
}
```

Response example:

```json
{
  "success": true,
  "reply": "这里是规划结果……",
  "tool_traces": [
    {
      "timestamp": "2026-06-19T10:00:00",
      "tool_name": "get_weather_forecast",
      "arguments": {
        "city": "杭州",
        "days": 3
      },
      "success": true,
      "result_summary": "杭州未来 3 天天气查询成功，共返回 3 天预报。",
      "raw_result_preview": "{...}"
    }
  ]
}
```

## 3. Save Itinerary

`POST /api/save-itinerary`

Purpose:

- save an itinerary directly from the web UI

Request body:

```json
{
  "title": "杭州 3 日轻松游",
  "content": "# 杭州 3 日轻松游\n\n## Day 1\n- 西湖散步"
}
```

## 4. Read Tool Traces

`GET /api/tool-traces?limit=20`

Purpose:

- show the latest tool calls in the web debug panel
- support report screenshots and observability

## 5. Read Current Itinerary

`GET /api/itinerary`

Purpose:

- let the frontend view the latest saved Markdown itinerary

## Frontend Integration Notes

- Keep API keys only on the backend.
- Frontend should use `fetch` or Axios against these `/api/*` endpoints.
- The tool trace panel in the web UI should read `tool_traces` from `/api/chat` first, and optionally use `/api/tool-traces` for a history view.


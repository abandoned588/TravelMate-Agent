from __future__ import annotations

import json
from typing import Any, Iterator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from config.settings import ITINERARY_PATH, TOOL_TRACE_PATH, WEB_DIR, get_settings
from core.agent import run_agent, stream_agent
from schemas.api import ApiResponse, ChatRequest, ChatResponse, SaveItineraryRequest
from tools.itinerary import save_itinerary


def _read_latest_tool_traces(limit: int = 20) -> list[dict[str, Any]]:
    if not TOOL_TRACE_PATH.exists():
        return []

    lines = [line.strip() for line in TOOL_TRACE_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    records: list[dict[str, Any]] = []
    for line in lines[-limit:]:
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            records.append(payload)
    return records


def _read_itinerary_markdown() -> str:
    if not ITINERARY_PATH.exists():
        return ""
    return ITINERARY_PATH.read_text(encoding="utf-8")


def _ndjson_line(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False) + "\n"


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="TravelMate API",
        version="0.1.0",
        description="HTTP API wrapper for the TravelMate planning agent.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/health", response_model=ApiResponse)
    def health() -> ApiResponse:
        return ApiResponse(
            success=True,
            message="TravelMate API is ready.",
            data={
                "llm_provider": "DeepSeek-compatible",
                "model_name": settings.model_name,
                "llm_configured": settings.has_llm_credentials,
                "amap_configured": settings.has_amap_key,
                "geoapify_configured": settings.has_geoapify_key,
            },
        )

    @app.post("/api/chat", response_model=ChatResponse)
    def chat(request: ChatRequest) -> ChatResponse:
        conversation = [message.model_dump() for message in request.messages]
        result = run_agent(conversation)
        return ChatResponse(
            success=bool(result.get("success", False)),
            reply=str(result.get("reply", "")),
            tool_traces=result.get("tool_traces", []),
        )

    @app.post("/api/chat/stream")
    def chat_stream(request: ChatRequest) -> StreamingResponse:
        conversation = [message.model_dump() for message in request.messages]

        def event_stream() -> Iterator[str]:
            for event in stream_agent(conversation):
                yield _ndjson_line(event)

        return StreamingResponse(event_stream(), media_type="application/x-ndjson")

    @app.post("/api/save-itinerary", response_model=ApiResponse)
    def save_itinerary_endpoint(request: SaveItineraryRequest) -> ApiResponse:
        result = save_itinerary(request.title, request.content)
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to save itinerary."))
        return ApiResponse(success=True, message=result.get("summary"), data=result.get("data"))

    @app.get("/api/tool-traces", response_model=ApiResponse)
    def tool_traces(limit: int = 20) -> ApiResponse:
        safe_limit = max(1, min(limit, 100))
        return ApiResponse(
            success=True,
            message=f"Returned up to {safe_limit} latest tool traces.",
            data=_read_latest_tool_traces(limit=safe_limit),
        )

    @app.get("/api/itinerary", response_model=ApiResponse)
    def itinerary() -> ApiResponse:
        markdown = _read_itinerary_markdown()
        return ApiResponse(
            success=True,
            message="Current itinerary file loaded.",
            data={"path": str(ITINERARY_PATH), "content": markdown},
        )

    @app.get("/", include_in_schema=False)
    def index() -> FileResponse:
        return FileResponse(WEB_DIR / "index.html")

    app.mount("/web", StaticFiles(directory=WEB_DIR), name="web")

    return app


app = create_app()
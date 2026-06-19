# Architecture

## Goal

TravelMate is designed as a small but traceable agent project for BYOA coursework. The system separates UI, orchestration, tools, and external service access so that each layer can be tested and explained independently.

## Layered Design

- `app.py` and `ui/`
  Render the Streamlit interface, manage session-state chat history, and display tool traces.
- `core/`
  Owns the OpenAI-compatible function-calling loop, tool dispatch, and log writing.
- `tools/`
  Exposes stable business tools that the LLM can call directly.
- `services/`
  Encapsulates HTTP calls and cache operations.
- `schemas/`
  Defines structured tool input, output, and tool-trace models.
- `config/`
  Centralizes paths, environment variables, and constants.
- `storage/`
  Persists cache, logs, and generated itinerary output.

## Runtime Flow

1. User submits a request in Streamlit.
2. `core/agent.py` prepends the system prompt and sends the conversation to the LLM.
3. If the model emits `tool_calls`, `core/tool_executor.py` validates and executes them.
4. Each tool result is appended back to the conversation as a tool message.
5. The model receives updated context and generates the final answer.
6. The UI displays both the answer and the tool trace records.

## Traceability

- Every tool call is logged to `storage/logs/tool_trace.jsonl`.
- Saved itineraries are written to `storage/outputs/itinerary.md`.
- Cache is stored in `storage/cache/` to reduce repeated API calls.
- `api/app.py` provides a web-facing API layer so the browser can call TravelMate without exposing secrets.

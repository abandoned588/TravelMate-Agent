from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator

from config.settings import PROMPTS_DIR
from core.exceptions import ConfigurationError, LLMClientError
from core.llm_client import LLMCompatibleClient
from core.tool_executor import run_tool_call
from tools.registry import get_tool_schemas


SYSTEM_PROMPT_PATH = PROMPTS_DIR / "system_prompt.md"


def _read_system_prompt() -> str:
    if SYSTEM_PROMPT_PATH.exists():
        content = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()
        if content:
            return content
    return "You are TravelMate, a travel planning agent."


def _assistant_tool_calls(message: Any) -> list[dict[str, Any]]:
    tool_calls: list[dict[str, Any]] = []
    for tool_call in message.tool_calls or []:
        tool_calls.append(
            {
                "id": tool_call.id,
                "type": tool_call.type,
                "function": {
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments,
                },
            }
        )
    return tool_calls


class TravelMateAgent:
    """Main agent loop for OpenAI-compatible function calling."""

    def __init__(self) -> None:
        self.system_prompt = _read_system_prompt()
        self.client = LLMCompatibleClient()
        self.tool_schemas = get_tool_schemas()

    def _build_messages(self, conversation: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [{"role": "system", "content": self.system_prompt}, *conversation]

    def _parse_tool_arguments(self, text: str) -> dict[str, Any]:
        try:
            payload = json.loads(text or "{}")
        except json.JSONDecodeError:
            return {}
        return payload if isinstance(payload, dict) else {}

    def _create_completion(self, messages: list[dict[str, Any]], use_tools: bool = True, stream: bool = False) -> Any:
        return self.client.create_chat_completion(
            messages=messages,
            tools=self.tool_schemas if use_tools else None,
            tool_choice="auto" if use_tools else "auto",
            stream=stream,
        )

    def _stream_final_text(
        self,
        messages: list[dict[str, Any]],
        tool_traces: list[dict[str, Any]],
    ) -> Iterator[dict[str, Any]]:
        stream = self._create_completion(messages, use_tools=False, stream=True)
        accumulated_text = ""

        yield {
            "type": "status",
            "stage": "drafting",
            "message": "工具已完成，正在实时整理最终行程。",
        }

        for chunk in stream:
            choice = chunk.choices[0]
            delta = choice.delta
            content = getattr(delta, "content", None) or ""
            if content:
                accumulated_text += content
                yield {
                    "type": "token",
                    "delta": content,
                    "reply_so_far": accumulated_text,
                }

        yield {
            "type": "final",
            "success": True,
            "reply": accumulated_text or "The model returned no text response.",
            "tool_traces": tool_traces,
        }

    def iter_reply(self, conversation: list[dict[str, Any]]) -> Iterator[dict[str, Any]]:
        messages = self._build_messages(conversation)
        tool_traces: list[dict[str, Any]] = []

        yield {
            "type": "status",
            "stage": "queued",
            "message": "已收到需求，正在分析旅行偏好。",
        }

        try:
            for round_index in range(6):
                yield {
                    "type": "status",
                    "stage": "thinking",
                    "message": "正在判断下一步是否需要调用工具。",
                    "round": round_index + 1,
                }

                response = self._create_completion(messages, use_tools=True, stream=False)
                message = response.choices[0].message

                if message.tool_calls:
                    messages.append(
                        {
                            "role": "assistant",
                            "content": message.content or "",
                            "tool_calls": _assistant_tool_calls(message),
                        }
                    )

                    for tool_call in message.tool_calls:
                        arguments = self._parse_tool_arguments(tool_call.function.arguments)
                        yield {
                            "type": "tool_start",
                            "tool_name": tool_call.function.name,
                            "arguments": arguments,
                            "message": f"正在调用工具 {tool_call.function.name}...",
                        }
                        tool_result = run_tool_call(tool_call.function.name, arguments)
                        tool_traces.append(tool_result["trace"])
                        yield {
                            "type": "tool_finish",
                            "tool_name": tool_call.function.name,
                            "summary": tool_result["summary"],
                            "trace": tool_result["trace"],
                        }
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps(tool_result["result"], ensure_ascii=False),
                            }
                        )

                    yield {
                        "type": "status",
                        "stage": "tool_complete",
                        "message": "工具结果已返回，正在继续规划。",
                    }
                    continue

                if tool_traces:
                    yield from self._stream_final_text(messages, tool_traces)
                    return

                direct_reply = message.content or "The model returned no text response."
                yield {
                    "type": "token",
                    "delta": direct_reply,
                    "reply_so_far": direct_reply,
                }
                yield {
                    "type": "final",
                    "success": True,
                    "reply": direct_reply,
                    "tool_traces": tool_traces,
                }
                return

            yield {
                "type": "final",
                "success": False,
                "reply": "Too many tool-calling rounds. Please try a simpler request.",
                "tool_traces": tool_traces,
            }
        except (ConfigurationError, LLMClientError) as exc:
            yield {"type": "final", "success": False, "reply": str(exc), "tool_traces": tool_traces}
        except Exception as exc:
            yield {
                "type": "final",
                "success": False,
                "reply": f"Agent run failed: {exc}",
                "tool_traces": tool_traces,
            }

    def reply(self, conversation: list[dict[str, Any]]) -> dict[str, Any]:
        final_result = {
            "success": False,
            "reply": "The agent produced no final response.",
            "tool_traces": [],
        }
        collected_reply = ""
        for event in self.iter_reply(conversation):
            if event.get("type") == "token":
                collected_reply = str(event.get("reply_so_far", collected_reply))
            if event.get("type") == "final":
                final_result = {
                    "success": bool(event.get("success", False)),
                    "reply": str(event.get("reply", "")) or collected_reply,
                    "tool_traces": event.get("tool_traces", []),
                }
        return final_result


def run_agent(conversation: list[dict[str, Any]]) -> dict[str, Any]:
    agent = TravelMateAgent()
    return agent.reply(conversation)


def stream_agent(conversation: list[dict[str, Any]]) -> Iterator[dict[str, Any]]:
    agent = TravelMateAgent()
    yield from agent.iter_reply(conversation)
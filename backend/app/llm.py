"""LLM provider abstraction and validated structured output.

Any OpenAI-compatible API works (DeepSeek by default). The rest of the app only depends on
the `LLMProvider` protocol, so swapping providers does not touch the triage logic.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any, Protocol

from pydantic import BaseModel, ValidationError

from app.schemas import Usage

log = logging.getLogger("triage.llm")


class LLMError(RuntimeError):
    """The provider failed or never returned a valid structured answer."""


@dataclass
class LLMResult:
    content: str
    usage: Usage


class LLMProvider(Protocol):
    model: str

    def complete_json(self, messages: list[dict[str, str]], max_tokens: int) -> LLMResult: ...


class OpenAICompatibleProvider:
    """Chat Completions client with JSON mode (DeepSeek, OpenAI, Groq, ...)."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        temperature: float = 0.2,
        timeout: float = 30.0,
        extra_body: dict[str, Any] | None = None,
    ) -> None:
        from openai import OpenAI

        self.model = model
        self._temperature = temperature
        self._extra_body = extra_body or {}
        self._client = OpenAI(api_key=api_key, base_url=base_url, timeout=timeout, max_retries=1)

    def complete_json(self, messages: list[dict[str, str]], max_tokens: int) -> LLMResult:
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore[arg-type]
                response_format={"type": "json_object"},
                max_tokens=max_tokens,
                temperature=self._temperature,
                extra_body=self._extra_body or None,
            )
        except Exception as exc:  # network, auth, quota... never leak details to the client
            raise LLMError(f"provider call failed: {type(exc).__name__}") from exc
        choice = response.choices[0]
        usage = response.usage
        return LLMResult(
            content=choice.message.content or "",
            usage=Usage(
                prompt_tokens=getattr(usage, "prompt_tokens", 0) or 0,
                completion_tokens=getattr(usage, "completion_tokens", 0) or 0,
                total_tokens=getattr(usage, "total_tokens", 0) or 0,
            ),
        )


def parse_json_object(content: str) -> dict[str, Any]:
    """Parse a JSON object, tolerating Markdown fences some models add despite JSON mode."""
    text = content.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text.removeprefix("json").strip()
    if not text:
        raise ValueError("empty response")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("response is not a JSON object")
    return data


def complete_structured[T: BaseModel](
    provider: LLMProvider,
    messages: list[dict[str, str]],
    schema: type[T],
    max_tokens: int,
    max_attempts: int = 2,
) -> tuple[T, Usage, int]:
    """Call the model and validate its JSON against `schema`.

    On malformed or invalid JSON the error is sent back to the model and it gets one more try.
    Returns the parsed object, the summed token usage and the number of attempts.
    """
    total = Usage()
    conversation = list(messages)
    last_error = ""
    for attempt in range(1, max_attempts + 1):
        result = provider.complete_json(conversation, max_tokens=max_tokens)
        total = Usage(
            prompt_tokens=total.prompt_tokens + result.usage.prompt_tokens,
            completion_tokens=total.completion_tokens + result.usage.completion_tokens,
            total_tokens=total.total_tokens + result.usage.total_tokens,
        )
        try:
            return schema.model_validate(parse_json_object(result.content)), total, attempt
        except (ValueError, ValidationError) as exc:
            last_error = str(exc)[:500]
            log.warning("invalid structured output (attempt %s): %s", attempt, last_error)
            conversation = [
                *messages,
                {"role": "assistant", "content": result.content[:2000]},
                {
                    "role": "user",
                    "content": "Your previous answer was not valid JSON for the required schema. "
                    f"Error: {last_error}\nReturn only the corrected JSON object.",
                },
            ]
    raise LLMError(f"invalid structured output after {max_attempts} attempts: {last_error}")

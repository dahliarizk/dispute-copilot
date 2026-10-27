import json
from dataclasses import dataclass
from typing import Any

import anthropic
from pydantic import BaseModel

from app.config import settings
from app.prompts._shared.loader import LoadedPrompt


@dataclass(frozen=True)
class LLMResult[T: BaseModel]:
    """The parsed structured output of one LLM call, plus token usage."""

    output: T
    model: str
    input_tokens: int
    output_tokens: int


def _render_examples(examples: list[dict[str, Any]]) -> str:
    if not examples:
        return ""
    blocks = [
        "Input: "
        + json.dumps(ex["input"], ensure_ascii=False)
        + "\nOutput: "
        + json.dumps(ex["output"], ensure_ascii=False)
        for ex in examples
    ]
    return "Examples:\n\n" + "\n\n".join(blocks) + "\n\n---\n\n"


def _client() -> anthropic.Anthropic:
    if not settings.anthropic_api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set. Add it to backend/.env before making LLM calls."
        )
    return anthropic.Anthropic(
        api_key=settings.anthropic_api_key,
        max_retries=3,
        timeout=60.0,
    )


def call[T: BaseModel](prompt: LoadedPrompt, output_model: type[T]) -> LLMResult[T]:
    """Call the bundle's model and parse the result into output_model."""
    client = _client()
    user_content = _render_examples(prompt.examples) + prompt.user
    max_tokens = int(prompt.config.get("max_tokens", 1024))

    parsed = client.messages.parse(
        model=prompt.model,
        max_tokens=max_tokens,
        system=prompt.system,
        messages=[{"role": "user", "content": user_content}],
        output_format=output_model,
    )

    output: T | None = None
    for block in parsed.content:
        candidate = getattr(block, "parsed_output", None)
        if candidate is not None:
            output = candidate
            break
    if output is None:
        raise RuntimeError("Model returned no parsed output")

    return LLMResult(
        output=output,
        model=prompt.model,
        input_tokens=parsed.usage.input_tokens,
        output_tokens=parsed.usage.output_tokens,
    )

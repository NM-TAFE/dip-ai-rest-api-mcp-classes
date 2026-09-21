from __future__ import annotations

from typing import List
from fastmcp.prompts import Message


def explain_conversion_prompt(
    input_value: str,
    input_unit: str,
    target_unit: str,
) -> List[Message]:
    """Render a tutoring-style explanation for a specific conversion."""

    return [
        Message(
            role="assistant",
            content=(
                "You are a clear, encouraging tutor helping a learner understand unit conversions. "
                "Show the formula, substitute the numbers, and provide the result. Keep it to 5 steps max."
            ),
        ),
        Message(
            role="user",
            content=(
                f"Explain how to convert {input_value} {input_unit} to {target_unit}. "
                "Return both the math and the final number."
            ),
        ),
    ]


def api_usage_prompt(operation: str) -> List[Message]:
    """Produce a single curl example for a chosen operation."""

    return [
        Message(
            role="system",
            content=(
                "You write concise API usage snippets. Show a single curl example that calls the correct "
                "endpoint on http://localhost:8003. Include JSON body and a short explanation line."
            ),
        ),
        Message(
            role="user",
            content=f"Give me a curl example for the {operation} endpoint.",
        ),
    ]


PROMPT_DEFINITIONS = [
    {
        "name": "explain_conversion",
        "description": "Guide a learner through the math for a specific conversion.",
        "func": explain_conversion_prompt,
    },
    {
        "name": "api_usage",
        "description": "Produce a ready-to-run curl snippet for one conversion endpoint.",
        "func": api_usage_prompt,
    },
]

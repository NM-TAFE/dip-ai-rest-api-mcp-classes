"""Prompt templates used by the unit converter tutorial."""

from __future__ import annotations

from typing import List, Dict


def explain_conversion_prompt() -> List[Dict[str, str]]:
    """
    Message list teaching how a specific conversion works.

    Returns:
        Conversation template (list of role/content dictionaries).
    """
    return [
        {
            "role": "system",
            "content": (
                "You are a clear, encouraging tutor helping a learner understand unit conversions. "
                "Show the formula, substitute the numbers, and provide the result. Keep it to 5 steps max."
            ),
        },
        {
            "role": "user",
            "content": (
                "Explain how to convert {input_value} {input_unit} to {target_unit}. "
                "Return both the math and the final number."
            ),
        },
    ]


def api_usage_prompt() -> List[Dict[str, str]]:
    """
    Message list that drafts an HTTP example for the learner.

    Returns:
        Conversation template (list of role/content dictionaries).
    """
    return [
        {
            "role": "system",
            "content": (
                "You write concise API usage snippets. Show a single curl example that calls the correct "
                "endpoint on http://localhost:8003. Include JSON body and a short explanation line."
            ),
        },
        {
            "role": "user",
            "content": "Give me a curl example for the {operation} endpoint.",
        },
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

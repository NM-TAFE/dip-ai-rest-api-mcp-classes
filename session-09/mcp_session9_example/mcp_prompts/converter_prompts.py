from __future__ import annotations
from typing import List

from fastmcp.prompts import Message


def explain_conversion_prompt(
    input_value: str,
    input_unit: str,
    target_unit: str,
) -> List[Message]:
    """Creates a tutoring-style system + user prompt for unit conversion explanations."""

    instructions = (
        "You are a clear, patient, and encouraging tutor helping students learn unit conversions. "
        "Always follow these rules:\n"
        "1. Show the conversion formula clearly.\n"
        "2. Substitute the given values into the formula.\n"
        "3. Show the calculation step-by-step.\n"
        "4. Give the final answer with the correct unit.\n"
        "5. Keep your entire response to a maximum of 5 steps.\n"
        "Use simple language suitable for beginners."
    )

    user_prompt = (
        f"Explain how to convert {input_value} {input_unit} to {target_unit}. "
        "Return both the step-by-step math and the final numerical result."
    )

    return [
        Message(role="assistant", content=instructions),
        Message(role="user", content=user_prompt),
    ]


def api_usage_prompt(
    operation: str,
    resource_text: str | None = None,
) -> List[Message]:
    """Produce a single curl example for a chosen operation.
    
    Optionally embeds a resource (e.g. API reference, endpoint list, or notes)
    to help the student get more accurate and consistent results.
    """

    instructions = (
        "You are a helpful teaching assistant that shows clean API usage examples.\n"
        "Rules:\n"
        "1. Show only ONE curl command per response.\n"
        "2. Use the base URL: http://localhost:8003\n"
        "3. Include the full JSON body when needed.\n"
        "4. Add one short, clear explanation line after the curl command.\n"
        "5. Keep the entire response short and beginner-friendly."
    )

    user_prompt = f"Give me a curl example for the {operation} endpoint."

    # Embed the resource if provided (makes it much easier for the student)
    if resource_text:
        resource_block = {
            "type": "resource",
            "resource": {
                "uri": "resource://api-reference",
                "mimeType": "text/plain",
                "text": resource_text.strip()
            }
        }
        
        user_prompt += (
            "\n\nHere is a helpful reference to use:\n"
            f"{resource_block}"
        )

    return [
        Message(role="assistant", content=instructions),
        Message(role="user", content=user_prompt),
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
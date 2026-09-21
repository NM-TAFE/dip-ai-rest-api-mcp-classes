"""Reusable MCP resources for the unit converter tutorial."""

from __future__ import annotations

from typing import Any, Dict


def unit_reference() -> Dict[str, Any]:
    """
    JSON cheatsheet of supported conversions, formulas, and sample IO.

    Returns:
        Dictionary describing conversions, formulas, and examples.
    """
    return {
        "id": "unit-converter-cheatsheet",
        "title": "Unit Converter Cheatsheet",
        "supported": {
            "temperature": {
                "celsius_to_fahrenheit": {"formula": "(°C × 9/5) + 32", "example": {"input": 25, "output": 77}},
                "fahrenheit_to_celsius": {"formula": "(°F − 32) × 5/9", "example": {"input": 86, "output": 30}},
            },
            "distance": {
                "kilometers_to_miles": {"formula": "km × 0.621371", "example": {"input": 5, "output": 3.106855}},
                "miles_to_kilometers": {"formula": "mi ÷ 0.621371", "example": {"input": 3.1, "output": 4.98895}},
            },
        },
        "notes": [
            "Negative distances are rejected to keep results meaningful.",
            "Temperature conversions accept any real number.",
        ],
    }


def troubleshooting_guide() -> str:
    """
    Plain‑text quick answers for common mistakes.

    Returns:
        Multi-line string with troubleshooting tips.
    """
    return "\n".join(
        [
            "Troubleshooting tips:",
            "- Check you are using the correct unit for the endpoint.",
            "- For miles_to_kilometers, distances must be >= 0.",
            "- Precision: results use floating point math; round if needed.",
            "- HTTP docs live at /docs once the server is running.",
        ]
    )


# How would we scope this?
RESOURCE_DEFINITIONS = [
    {
        "name": "unit_reference",
        "display_name": "Unit Converter Cheatsheet",
        "description": "JSON cheatsheet covering formulas and sample conversions.",
        "mime_type": "application/json",
        "func": unit_reference,
    },
    {
        "name": "troubleshooting_guide",
        "display_name": "Troubleshooting Guide",
        "description": "Plain text tips for common conversion mistakes.",
        "mime_type": "text/plain",
        "func": troubleshooting_guide,
    },
]

# Conversion logic and HTTP endpoints are defined here so they can be reused
# by both the FastAPI app and the MCP tool registrations.

from fastapi import APIRouter

router = APIRouter(prefix="", tags=["unit-conversion"])


# --- Core conversion helpers -------------------------------------------------

#Executes
def celsius_to_fahrenheit_value(celsius: float) -> float:
    """
    Convert Celsius to Fahrenheit using (°C × 9/5) + 32.

    Args:
        celsius: Temperature in Celsius.

    Returns:
        The Fahrenheit temperature.
    """
    return (celsius * 9 / 5) + 32


def fahrenheit_to_celsius_value(fahrenheit: float) -> float:
    """
    Convert Fahrenheit to Celsius using (°F − 32) × 5/9.

    Args:
        fahrenheit: Temperature in Fahrenheit.

    Returns:
        The Celsius temperature.
    """
    return (fahrenheit - 32) * 5 / 9


def kilometers_to_miles_value(kilometers: float) -> float:
    """
    Convert kilometers to miles with the 0.621371 factor.

    Args:
        kilometers: Distance in kilometers.

    Returns:
        The distance in miles.
    """
    return kilometers * 0.621371

# --- FastAPI endpoints -------------------------------------------------------

@router.post("/celsius-to-fahrenheit")
def celsius_to_fahrenheit(celsius: float):
    """
    HTTP endpoint: convert Celsius to Fahrenheit.

    Args:
        celsius: Temperature in Celsius.

    Returns:
        JSON dict with the result and operation name.
    """
    result = celsius_to_fahrenheit_value(celsius)
    return {"result": result, "operation": "celsius_to_fahrenheit"}


@router.post("/fahrenheit-to-celsius")
def fahrenheit_to_celsius(fahrenheit: float):
    """
    HTTP endpoint: convert Fahrenheit to Celsius.

    Args:
        fahrenheit: Temperature in Fahrenheit.

    Returns:
        JSON dict with the result and operation name.
    """
    result = fahrenheit_to_celsius_value(fahrenheit)
    return {"result": result, "operation": "fahrenheit_to_celsius"}


@router.post("/kilometers-to-miles")
def kilometers_to_miles(kilometers: float):
    """
    HTTP endpoint: convert kilometers to miles.

    Args:
        kilometers: Distance in kilometers.

    Returns:
        JSON dict with the result and operation name.
    """
    result = kilometers_to_miles_value(kilometers)
    return {"result": result, "operation": "kilometers_to_miles"}

# --- Metadata for MCP tool registration ----

TOOL_DEFINITIONS = [
    {
        "name": "celsius_to_fahrenheit",
        "description": "Convert Celsius temperature to Fahrenheit",
        "func": celsius_to_fahrenheit_value,
        "tags": {"temperature", "conversion"},
    },
    {
        "name": "fahrenheit_to_celsius",
        "description": "Convert Fahrenheit temperature to Celsius",
        "func": fahrenheit_to_celsius_value,
        "tags": {"temperature", "conversion"},
    },
    {
        "name": "kilometers_to_miles",
        "description": "Convert kilometers to miles",
        "func": kilometers_to_miles_value,
        "tags": {"distance", "conversion"},
    }
]

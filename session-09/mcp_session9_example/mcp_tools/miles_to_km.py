from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel, Field
from utils.get_principal import Principal, get_current_principal
from utils.enforce_permissions import enforce_permissions
import math, time

router = APIRouter(prefix="", tags=["unit-conversion"])

# --- Request/Response models for clarity ---
class ConversionRequest(BaseModel):
    """Request model for miles to kilometers conversion, with validation.
    Attributes: ge=0 ensures non-negative input, and description provides API documentation."""
    miles: float = Field(..., ge=0, description="Distance in miles (>= 0)")

class ConversionResponse(BaseModel):
    """Response model for miles to kilometers conversion.
    Attributes: result is the converted distance, operation indicates the conversion type, and audited_at is a timestamp for auditing."""
    result: float
    operation: str
    audited_at: float

def miles_to_kilometers_value(miles: float) -> float:
    """
    Convert miles to kilometers, rejecting negative inputs.

    Args:
        miles: Distance in miles.

    Returns:
        The distance in kilometers.

    Raises:
        ValueError: If a negative distance is provided.
    """
    if miles is None or math.isnan(miles):
        raise ValueError("Miles must be a valid number.")
    if miles < 0:
        raise ValueError("Distance cannot be negative")
    return miles / 0.621371

@router.post("/miles-to-kilometers")
# def miles_to_kilometers(miles: float):
def miles_to_kilometers(
        body: ConversionRequest,     
        principal: Principal = Depends(get_current_principal),
        ) -> ConversionResponse:
    """
    HTTP endpoint: convert miles to kilometers with input validation.

    Args:
        miles: Distance in miles.

    Returns:
        JSON dict with the result and operation name, or an error message.
    """
    # import logging
    # logging.info(f"Endpoint called by user_id={principal.user_id}, roles={principal.roles}, scopes={principal.scopes}, input_miles={body.miles}")

    enforce_permissions(principal)
    # logging.info(f"Permissions check passed for user_id={principal.user_id}")

    try:
        result = miles_to_kilometers_value(body.miles)
        return ConversionResponse(
            result=result,
            operation="miles_to_kilometers",
            audited_at=time.time(),
        )
    except ValueError as exc:  # Keep HTTP response friendly
        raise HTTPException(status_code=400, detail=str(exc))

TOOL_DEFINITION = [
    {
        "name": "miles_to_kilometers",
        "description": "Convert miles to kilometers (validates non‑negative input)",
        "func": miles_to_kilometers_value,
        "tags": {"distance", "conversion"},
    },
]
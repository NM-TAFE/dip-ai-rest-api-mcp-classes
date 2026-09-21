### Review the original

- Read `mcp_tools/converter_tools.py`; find:
  - Pure function `miles_to_kilometers_value`.
  - HTTP route `@router.post("/miles-to-kilometers")`.
  - Tool metadata `miles_to_kilometers_tool`.
- List gaps: no auth, no Pydantic models, ad‑hoc error handling, no audit fields.

### Phase 1 — New module scaffold

1. Create `miles_to_km.py` alongside the existing files.
2. Add imports you will need:
   - `from fastapi import FastAPI, Depends, HTTPException, Header`
   - `from pydantic import BaseModel, Field`
   - `from typing import Optional, Set`
   - `import math, time`

### Phase 2 — Roles, structure + permissions

4. Define a `Principal` Pydantic model with `user_id: str`, `roles: Set[str] = set()`, `scopes: Set[str] = set()`.
5. Add constants:
   - `REQUIRED_ROLES = {"utility.read", "conversion.run"}`
   - `REQUIRED_SCOPES = {"miles:convert"}`
6. Implement `get_current_principal(authorisation: Optional[str] = Header(..., alias="Authorisation")) -> Principal`:
   - If header missing or not `Bearer ...`, raise `HTTPException(401, "Missing or invalid token")`.
   - Parse token (demo rule: if token contains `"demo-token"`, grant both required roles/scopes; else empty sets).
7. Implement `enforce_permissions(principal: Principal)`:
   - Compute missing roles/scopes; if any → raise `HTTPException(403, detail={"error": "forbidden", "missing_roles": sorted(...), "missing_scopes": sorted(...)})`.

### Phase 3 — Duplicate and compare

8. Reuse the logic but make it stricter:
   - `def miles_to_kilometers_value(miles: float) -> float:`
   - Error if `miles is None` or `math.isnan(miles)` → `ValueError("Miles must be a valid number.")`.
   - Error if `miles < 0` → `ValueError("Miles must be non-negative.")`.
   - Return `miles * 1.609344` (factor choice; keep consistent).

### Phase 4 — Add request/response schemas

9. Add `class ConversionRequest(BaseModel): miles: float = Field(..., ge=0, description="Distance in miles (>= 0)")`.
10. Add `class ConversionResponse(BaseModel): result: float; operation: str; audited_at: float`.

### Phase 5 — Finalise the HTTP endpoint

11. Define route:

```python
@app.post("/miles-to-kilometers", response_model=ConversionResponse)
def miles_to_kilometers(body: ConversionRequest, principal: Principal = Depends(get_current_principal)):
    enforce_permissions(principal)
    try:
        result = miles_to_kilometers_value(body.miles)
        return ConversionResponse(result=result, operation="miles_to_kilometers", audited_at=time.time())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
```

- Note: `response_model` keeps OpenAPI accurate.

### Phase 6 — MCP tool metadata (mirror the route)

12. Create a dictionary `miles_to_kilometers_tool` (do **not** overwrite the original file):

- `name`: `"miles_to_kilometers"`
- `description`: same as before.
- `input_schema`: object with required `miles` number, `minimum: 0`.
- `output_schema`: object with `result` (number), `operation` (const `"miles_to_kilometers"`), `audited_at` (number).
- `func`: `miles_to_kilometers_value`.
- `tags`: `{"distance", "conversion"}`.
- `meta.permissions`: `required_roles`, `required_scopes`, `policy: "deny-by-default"`, `reason: "..."`
- `rate_limit` and `audit.log_fields` mirroring the example in `converter_tools.py`.

### Phase 7 — Manually test

13. Run server: `python -m converter_streamable_http_server`.
14. Test cases via cURL & MCP Inspector:

- Valid: Authorization `Bearer demo-token` + `{"miles": 5}` → 200, `result ≈ 8.04672`.
- Missing token → 401.
- Token without roles/scopes (e.g., `Bearer other`) → 403 with `missing_roles`, `missing_scopes`.
- `{"miles": -1}` or `{"miles": "nan"}` → 400 with validation message.

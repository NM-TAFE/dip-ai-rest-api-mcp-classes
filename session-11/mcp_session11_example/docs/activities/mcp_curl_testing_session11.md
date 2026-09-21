# Testing MCP Tools with curl

### Converter Tools Error‑Handling

Use these commands against the running MCP/HTTP server started with:

```bash
python calculator_api_tutorial.py
```

(Default base URL: `http://localhost:8003`)

The MCP endpoints do **not** require authentication.  
The plain HTTP conversion routes can optionally accept an:

    Authorization: Bearer <token>

---

## URL structure (important)

- MCP JSON‑RPC endpoint
  - `POST http://localhost:8003/mcp/`
- Plain FastAPI HTTP routes
  - `/celsius-to-fahrenheit-celsius-to-fahrenheit-post`
  - `/fahrenheit-to-celsius-fahrenheit-to-celsius-post`
  - `/kilometers_to_miles_kilometers_to_miles_post`

---

## curl flag cheat sheet

- `-s` Silent mode (hide progress/errors)
- `-D -` Write response headers to stdout (used to capture `mcp-session-id`)
- `-o /dev/null` Discard response body while keeping headers
- `-v` Verbose connection/debug output
- `-L` Follow redirects (helpful if you forget `/mcp/`)

---

## Optional environment helpers

```bash
BASE="http://localhost:8003" && MCP="$BASE/mcp/" && AUTH="Authorization: Bearer 143f4a46d74fee0d7918b2857577868cb3daf9e6e50ee91c2f7975ba26fdb8f7" && ACCEPT="Accept: application/json, text/event-stream" && PROTO="MCP-Protocol-Version: 2025-06-18"
```

---

## Quick connectivity + MCP session capture (run first)

```bash
SESSION=$(curl -sD - -o /dev/null "$MCP" -H "Content-Type: application/json, text/event-stream" -H "$ACCEPT" -H "$PROTO" -d '{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"curl","version":"1.0"}}}' | awk 'BEGIN{IGNORECASE=1} /^mcp-session-id:/ {sub(/\r$/,""); print $2}')
echo "SESSION=$SESSION"
```

If `SESSION` is empty, rerun without `-s` or add `-v`.

---

## 1️. MCP handshake

```bash
curl -s "$MCP" -H "Content-Type: application/json, text/event-stream" -H "$ACCEPT" -H "$PROTO" -H "Mcp-Session-Id: $SESSION" -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{"roots":{"listChanged":true}},"clientInfo":{"name":"curl","version":"1.0"}}}'
```

---

## 2️. List available tools

```bash
curl -s "$MCP" -H "Content-Type: application/json, text/event-stream" -H "$ACCEPT" -H "$PROTO" -H "Mcp-Session-Id: $SESSION" -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
```

Expected tools:

- `/celsius_to_fahrenheit_celsius_to_fahrenheit_post`
- `/fahrenheit_to_celsius_fahrenheit_to_celsius_post`
- `/kilometers_to_miles_kilometers_to_miles_post`

---

## 3️. Happy path — valid MCP tool call

```bash
curl -s "$MCP" -H "Content-Type: application/json" -H "$ACCEPT" -H "$PROTO" -H "Mcp-Session-Id: $SESSION" -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"fahrenheit_to_celsius_fahrenheit_to_celsius_post","arguments":{"fahrenheit":77}}}'
```

Baseline — always test this first.

---

## 4️. Protocol error — unknown tool name

```bash
curl -s "$MCP" -H "Content-Type: application/json, text/event-stream" -H "$ACCEPT" -H "$PROTO" -H "Mcp-Session-Id: $SESSION" -d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"rankine_to_celsius","arguments":{"value":100}}}'
```

Fails at the **protocol layer** (`method not found`).

---

## 5️. Protocol / schema error — wrong argument name

```bash
curl -s "$MCP" -H "Content-Type: application/json, text/event-stream, text/event-stream" -H "$ACCEPT" -H "$PROTO" -H "Mcp-Session-Id: $SESSION" -d '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"kilometers_to_miles_kilometers_to_miles_post","arguments":{"distance":10}}}'
```

Fails because `distance` is not a valid parameter name.

---

## 6. Domain logic bug — negative values are accepted (HTTP)

This section **intentionally exposes a bug** in the current implementation.

### Current HTTP endpoint (BUGGY)

```python
@router.post("/kilometers-to-miles")
def kilometers_to_miles(kilometers: float):
    result = kilometers_to_miles_value(kilometers)
    return {"result": result, "operation": "kilometers_to_miles"}
```

### Input that currently succeeds when it should not

```bash
curl -s "$MCP" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION" \
  -d '{
    "jsonrpc": "2.0",
    "id": 200,
    "method": "tools/call",
    "params": {
      "name": "kilometers_to_miles_kilometers_to_miles_post",
      "arguments": {
        "kilometers": -10
      }
    }
  }'
```

```json
{
  "result": -6.21371,
  "operation": "kilometers_to_miles"
}
```

### Where is this bug

- Transport NO
- FastAPI parsing NO
- Type validation NO
- Result is mathematically correct but meaningless

> This is **function logic problem**.

---

## Option A — Tool‑logic validation (explicit domain rule)

Add a guard inside the route or core function:

```python
from fastapi import HTTPException

@router.post("/kilometers-to-miles")
def kilometers_to_miles(kilometers: float):
    if kilometers < 0:
        raise HTTPException(
            status_code=422,
            detail="Distance must be zero or greater"
        )

    result = kilometers_to_miles_value(kilometers)
    return {"result": result, "operation": "kilometers_to_miles"}
```

### Retest after fix

Now fails with a clear validation error.

---

## Fix option B — FastAPI / Pydantic validation (preferred)

Push validation to the outer boundary of the API using a request model.

```python
from pydantic import BaseModel, Field

class KilometersRequest(BaseModel):
    kilometers: float = Field(..., ge=0, description="Distance in kilometers (>= 0)")

@router.post("/kilometers-to-miles")
def kilometers_to_miles(payload: KilometersRequest):
    result = kilometers_to_miles_value(payload.kilometers)
    return {"result": result, "operation": "kilometers_to_miles"}
```

### Retest after fix

Rejected before the tool logic runs.

---

## 7️. FastAPI validation error — wrong type

```bash
curl -s "$BASE/celsius-to-fahrenheit" -H "Content-Type: application/json, text/event-stream" -H "$AUTH" -d '{"celsius":"warm"}'
```

Rejected by Pydantic type validation.

---

## 88. FastAPI validation error — missing field

```bash
curl -s "$BASE/kilometers-to-miles" -H "Content-Type: application/json, text/event-stream" -d '{}'
```

Rejected due to missing required input.

---

## 9. Transport error — broken JSON

```bash
curl -X POST "$MCP" -H "Content-Type: application/json, text/event-stream" -d '{"jsonrpc":"2.0","method":"tools/call",'
```

Fails at the HTTP parser before MCP or tool logic.

---

## Testing prompts and resources

These are tested using with the **same MCP session and JSON‑RPC**.

---

## 1. Prompt example — `explain_conversion`

### What this tests

- Prompt lookup by name
- Argument passing
- Prompt rendering (no execution logic yet)

### curl command

```bash
curl -s "$MCP" -H "Content-Type: application/json, text/event-stream" -H "$ACCEPT" -H "$PROTO" -H "Mcp-Session-Id: $SESSION" -d '{"jsonrpc":"2.0","id":11,"method":"prompts/get","params":{"name":"explain_conersion","arguments":{"input_value":"10","input_unit":"kilometers","target_unit":"miles"}}}'
```

### Notes

- This is **not** a protocol error if the prompt exists
- This does **not** perform the conversion — it generates an explanation
- The output is a **structured prompt** (system + user messages)
- If the prompt name were wrong, this would become a **protocol‑level error**
  - Note the code this is intentional and useful.

---

## 1. Resource example — `unit_reference`

### What this tests

- Resource URI lookup
- MIME type handling
- Read‑only reference access

### curl command

```bash
curl -s "$MCP" -H "Content-Type: application/json, text/event-stream" -H "$ACCEPT" -H "$PROTO" -H "Mcp-Session-Id: $SESSION" -d '{"jsonrpc":"2.0","id":12,"method":"resources/read","params":{"uri":"resource://unit_reference"}}'
```

## List the resources

```bash
curl -s "$MCP" \
  -H "Content-Type: application/json, text/event-stream" \
  -H "$ACCEPT" \
  -H "$PROTO" \
  -H "Mcp-Session-Id: $SESSION" \
  -d '{"jsonrpc":"2.0","id":21,"method":"resources/read","params":{"uri":"resource://converter/unit_reference"}}'
```

Replace the correct URI from the reponse into the initial command

### Notes

- Resources are **data**, not actions
- No arguments are required here
- If the resource URI is wrong, MCP returns a **protocol error**
- Resources are ideal for:
  - API reference data
  - Cheatsheets
  - Troubleshooting guides
  - Shared context for prompts

---

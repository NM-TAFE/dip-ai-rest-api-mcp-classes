# Unit Converter API + MCP Tutorial

Hands-on material for showing students how FastAPI endpoints become MCP tools, plus how to expose resources and prompts, using `fastmcp`. Everything needed lives in this folder.

## What’s here

- `calculator_api_tutorial.py` – builds the FastAPI app, wraps it with FastMCP, mounts MCP HTTP/SSE endpoints, registers resources and prompts, and starts uvicorn.
- `converter_tools.py` – conversion logic plus FastAPI routes (these routes become MCP tools automatically).
- `converter_resources.py` / `converter_prompts.py` – resource content and prompt templates that are registered with FastMCP.
- `requirements.txt` – Python dependencies.

## Prerequisites

- Python 3.10+ (tested with 3.11).
- Virtual environment recommended.
- Optional: an MCP-capable client (VS Code MCP extension, `mcp-remote`, or the npm inspector below).

## Setup

```bash
# from this folder
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the HTTP + MCP server

```bash
# start the server
python calculator_api_tutorial.py
```

You’ll see:

- Swagger UI: http://localhost:8003/docs
- ReDoc: http://localhost:8003/redoc
- MCP endpoints served by FastMCP:
  - streamable-http: http://localhost:8003/mcp
  - SSE: http://localhost:8003/sse

## Try the HTTP endpoints (curl)

```bash
# Without pydantic
curl -X POST "http://localhost:8003/miles-to-kilometers?miles=3.1" \
  -H "Authorization: Bearer 143f4a46d74fee0d7918b2857577868cb3daf9e6e50ee91c2f7975ba26fdb8f7"

# If we use pydantic models
curl -X POST "http://localhost:8003/miles-to-kilometers" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer Y658139cf61948208ed76a4b36122b9552ec5c3f6da5e02f7c5d85d995dede17dE" \
  -d "3.1"
```

- Celsius → Fahrenheit

```bash
curl -X POST "http://localhost:8003/celsius-to-fahrenheit" \
  -H "Content-Type: application/json" \
  -d "25"
```

- Fahrenheit → Celsius

```bash
curl -X POST "http://localhost:8003/fahrenheit-to-celsius" \
  -H "Content-Type: application/json" \
  -d "86"
```

- Kilometers → Miles

```bash
curl -X POST "http://localhost:8003/kilometers-to-miles" \
  -H "Content-Type: application/json" \
  -d "5"
```

- Miles → Kilometers (rejects negative values)

```bash
curl -X POST "http://localhost:8003/miles-to-kilometers" \
  -H "Content-Type: application/json" \
  -d "3.1"
```

Each endpoint returns JSON like `{ "result": <number>, "operation": "..." }` or `{ "error": "..." }` for invalid input.

## Use with MCP

1. Start the server as above.
2. Point your MCP client to the process. Example VS Code `.vscode/mcp.json` entry:
   ```json
   {
     "servers": {
       "UnitConverter": {
         "command": "python",
         "args": ["calculator_api_tutorial.py"]
       }
     }
   }
   ```
3. From the MCP client, list artifacts. You should see:
   - Tools: `celsius_to_fahrenheit`, `fahrenheit_to_celsius`, `kilometers_to_miles`, `miles_to_kilometers`
   - Resources: `resource://unit_reference`, `resource://troubleshooting_guide`
   - Prompts: `explain_conversion`, `api_usage`

## Inspect with the npm MCP Inspector

Explore everything (tools, resources, prompts) in a browser.

```bash
# with the server already running on http://localhost:8220
# Prefer HTTP transport:
npx @modelcontextprotocol/inspector@latest -e DUMMY=1 --url http://localhost:8003/mcp --transport http

# If you need SSE:
npx @modelcontextprotocol/inspector@latest -e DUMMY=1  --url http://localhost:8003/sse --transport sse

# If env error appears
npx @modelcontextprotocol/inspector@latest -e DUMMY=1 --url http://localhost:8003/mcp --transport streamable-http
```

- UI runs on localhost:5173 by default.
- Change UI port if needed: `CLIENT_PORT=8080 npx @modelcontextprotocol/inspector --url http://localhost:8003/mcp --transport http`
- Add headers if required: `--header "Authorization: Bearer TOKEN"`.

# Unit Converter API + MCP Tutorial

Hands-on material for showing students how FastAPI endpoints become MCP tools, plus how to expose resources and prompts, using `fastmcp`. Everything needed lives in this folder.

## What’s here

- `calculator_api_tutorial.py` – builds the FastAPI app, wraps it with FastMCP, mounts MCP HTTP/SSE endpoints, registers resources and prompts, and starts uvicorn.
- `converter_tools.py` – conversion logic plus FastAPI routes (these routes become MCP tools automatically).
- `converter_resources.py` / `converter_prompts.py` – resource content and prompt templates that are registered with FastMCP.
- `requirements.txt` – Python dependencies.

## Prerequisites

- Python 3.10+ (tested with 3.11).
- Virtual environment recommended.
- Optional: an MCP-capable client (VS Code MCP extension, `mcp-remote`, or the npm inspector below).

## Setup

```bash
# from this folder
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the HTTP + MCP server

```bash
python calculator_api_tutorial.py
```

You’ll see:

- Swagger UI: http://localhost:8003/docs
- ReDoc: http://localhost:8003/redoc
- MCP endpoints served by FastMCP:
  - streamable-http: http://localhost:8003/mcp
  - SSE: http://localhost:8003/sse
    "$SESSION

## Try the HTTP endpoints (curl)

```bash
# Without pydantic
curl -X POST "http://localhost:8003/miles-to-kilometers?miles=3.1" \

# If we use pydantic models
curl -X POST 'http://localhost:8003/celsius-to-fahrenheit?celsius=20' -H 'accept: application/json' -d ''
```

- Celsius → Fahrenheit
- Fahrenheit → Celsius
- Kilometers → Miles
- Miles → Kilometers (rejects negative values)

Each endpoint returns JSON like `{ "result": <number>, "operation": "..." }` or `{ "error": "..." }` for invalid input.

## Use with MCP

1. Start the server as above.
2. Point your MCP client to the process. Example VS Code `.vscode/mcp.json` entry:
   ```json
   {
     "servers": {
       "UnitConverter": {
         "command": "python",
         "args": ["calculator_api_tutorial.py"]
       }
     }
   }
   ```
3. From the MCP Inspector client, list artifacts. You should see:
   - Tools: `celsius_to_fahrenheit`, `fahrenheit_to_celsius`, `kilometers_to_miles`, `miles_to_kilometers`
   - Resources: `resource://unit_reference`, `resource://troubleshooting_guide`
   - Prompts: `explain_conversion`, `api_usage`

## Inspect with the npm MCP Inspector

Explore everything (tools, resources, prompts) in a browser.

```bash
# with the server already running on http://localhost:8220
# Prefer HTTP transport:
npx @modelcontextprotocol/inspector@latest -e DUMMY=1 --url http://localhost:8003/mcp --transport http

# If you need SSE:
npx @modelcontextprotocol/inspector@latest -e DUMMY=1  --url http://localhost:8003/sse --transport sse

# If env error appears
npx @modelcontextprotocol/inspector@latest -e DUMMY=1 --url http://localhost:8003/mcp --transport streamable-http
```

- UI runs on localhost:5173 by default.
- Change UI port if needed: `CLIENT_PORT=8080 npx @modelcontextprotocol/inspector --url http://localhost:8003/mcp --transport http`
- Add headers if required: `--header "Authorization: Bearer TOKEN"`.

## Headers & Auth (common to all)

```bash
# Add JSON content type (and optionally your auth token)
-H "Content-Type: application/json" \
-H "Authorization: Bearer <TOKEN>"
```

> If your server doesn’t require auth, omit the `Authorization` header.

---

## 1) List all prompts

```bash
curl -s -X POST <SERVER_URL> \
-H "Content-Type: application/json" \
-d '{"jsonrpc":"2.0","method":"prompts/list","params":{},"id":1}'
```

**Expected response (shape varies by server):**

```json
{
  "jsonrpc": "2.0",
  "result": { "prompts": [{ "name": "summarize" }, { "name": "explain" }] },
  "id": 1
}
```

---

## 2) Get a specific prompt (including its template/metadata)

```bash
curl -s -X POST <SERVER_URL> \
-H "Content-Type: application/json" \
-d '{"jsonrpc":"2.0","method":"prompts/get","params":{"name":"summarize"},"id":2}'
```

**Optional params commonly supported:**

- `"version": "v2"` (if your server versions prompts)
- `"locale": "en-AU"` (if prompts are localized)

---

## 3) Render/execute a prompt with variables

If your prompt has placeholders (e.g., `{{text}}`), pass them as `input` or `variables`:

```bash
curl -s -X POST <SERVER_URL> \
-H "Content-Type: application/json" \
-d '{"jsonrpc":"2.0","method":"prompts/render","params":{"name":"summarize","variables":{"text":"This is the content to summarize","tone":"neutral"}},"id":3}'
```

Some servers use `"input"` instead of `"variables"`:

```bash
-d '{"jsonrpc":"2.0","method":"prompts/render","params":{"name":"summarize","input":{"text":"...","tone":"neutral"}},"id":3}'
```

---

## 4) List available resources

Resources are typically files, URLs, or data blobs the MCP server exposes.

```bash
curl -s -X POST <SERVER_URL> \
-H "Content-Type: application/json" \
-d '{"jsonrpc":"2.0","method":"resources/list","params":{},"id":4}'
```

**Example result:**

```json
{
  "jsonrpc": "2.0",
  "result": {
    "resources": [
      { "uri": "file:///data/report.pdf" },
      { "uri": "s3://bucket/logs/" }
    ]
  },
  "id": 4
}
```

---

## 5) Read a resource by URI

```bash
curl -s -X POST <SERVER_URL> \
-H "Content-Type: application/json" \
-d '{"jsonrpc":"2.0","method":"resources/read","params":{"uri":"file:///data/report.pdf"},"id":5}'
```

**If the resource supports ranges or formats:**

```bash
-d '{"jsonrpc":"2.0","method":"resources/read","params":{"uri":"file:///data/report.pdf","options":{"range":{"start":0,"end":4096},"as":"text"}},"id":5}'
```

---

## 6) Search resources (if supported)

```bash
curl -s -X POST <SERVER_URL> \
-H "Content-Type: application/json" \
-d '{"jsonrpc":"2.0","method":"resources/search","params":{"query":"error OR exception","limit":50},"id":6}'
```

---

## Handling errors

If something goes wrong, the server returns an **error object**:

- **Parse error (-32700):** Your JSON is malformed.
- **Invalid request (-32600):** Missing `"jsonrpc":"2.0"` or `"method"`.
- **Method not found (-32601):** You called a method the server doesn’t implement (e.g., typo in `"prompts/render"`).
- **Invalid params (-32602):** Wrong/missing fields in `"params"`.
- **Internal error (-32603):** Server crashed while handling your request.

Example failing call (typo in method):

```bash
curl -s -X POST <SERVER_URL> -H "Content-Type: application/json" \
-d '{"jsonrpc":"2.0","method":"prompts/rendr","params":{"name":"summarize"},"id":7}'
```

Response:

```json
{
  "jsonrpc": "2.0",
  "error": { "code": -32601, "message": "Method not found" },
  "id": 7
}
```

---

### macOS/Linux (bash/zsh)

- The examples above will work as‑is.

### Windows PowerShell

- Use single quotes around the JSON, or escape double quotes:

```powershell
curl -Method POST <SERVER_URL> `
  -Headers @{ "Content-Type"="application/json" } `
  -Body '{"jsonrpc":"2.0","method":"prompts/list","params":{},"id":1}'
```

### Windows CMD

```cmd
curl -s -X POST <SERVER_URL> -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"prompts/list\",\"params\":{},\"id\":1}"
```

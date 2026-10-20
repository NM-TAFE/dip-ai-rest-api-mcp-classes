# Dynamic Resource Routing

Use these steps to switch the converter resources from hard-coded decorators to dynamic registration. The end result lets you add a new resource by editing `mcp_resources/converter_resources.py` only—no server wiring changes required.

## Steps

1. Resource metadata lives in `mcp_resources/converter_resources.py` inside `RESOURCE_DEFINITIONS`. Each entry needs `name`, optional `display_name`, `description`, `mime_type`, and `func`.
2. The dynamic registrar now lives in `utils/resource_utils.py` as `register_resources`. It registers a single dynamic template `resource://converter/{name}` that resolves resources by URI parameter.
3. In `converter_streamable_http_server.py`, import both:
   ```python
   from mcp_resources.converter_resources import RESOURCE_DEFINITIONS
   from utils.resource_utils import register_resources
   ```
4. Remove the manual `@mcp.resource` functions and call `register_resources(mcp, RESOURCE_DEFINITIONS)` right after the `FastMCP.from_fastapi(...)` block. This wires every definition automatically behind a parameterized URI.
5. Start the server and verify the MCP resources list shows the template `resource://converter/{name}`. Read a resource by supplying the path param, e.g. `resource://converter/unit_reference` or `resource://converter/troubleshooting_guide`. Example one-liner curls (set env vars first):

```bash
BASE="http://localhost:8003"; MCP="$BASE/mcp/"; ACCEPT="Accept: application/json, text/event-stream"; PROTO="MCP-Protocol-Version: 2025-06-18"
SESSION=$(curl -sD - -o /dev/null "$MCP" -H "Content-Type: application/json" -H "$ACCEPT" -H "$PROTO" -d '{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"curl","version":"1.0"}}}' | awk 'BEGIN{IGNORECASE=1} /^mcp-session-id:/ {sub(/\r$/,""); print $2}')
curl -s "$MCP" -H "Content-Type: application/json" -H "$ACCEPT" -H "$PROTO" -H "Mcp-Session-Id: $SESSION" -d '{"jsonrpc":"2.0","id":5,"method":"resources/list","params":{}}'
curl -s "$MCP" -H "Content-Type: application/json" -H "$ACCEPT" -H "$PROTO" -H "Mcp-Session-Id: $SESSION" -d '{"jsonrpc":"2.0","id":6,"method":"resources/read","params":{"uri":"resource://converter/unit_reference"}}'
```

6. Add a new resource by appending to `RESOURCE_DEFINITIONS`; no further code changes are needed. Restart the server and the new name works immediately at `resource://converter/<new_name>`.

## STDIO test (no HTTP)

With the stdio server running (`python converter_stdio_server.py`), send each line as a separate JSON message (newline terminated):

```powershell
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"cli","version":"1.0"}}}
{"jsonrpc":"2.0","id":2,"method":"resources/list","params":{}}
{"jsonrpc":"2.0","id":3,"method":"resources/read","params":{"uri":"resource://converter/unit_reference"}}
```

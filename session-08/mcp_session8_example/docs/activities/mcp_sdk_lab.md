## 1. Create & activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python --version            # expect 3.12.x
```

## 2. Install requirements one by one

Read `requirements.txt`, then install line-by-line, checking each.

```bash
python -m pip install --upgrade pip
pip install fastapi
pip install uvicorn
pip install fastmcp
pip install pydantic
```

Quick checks after installs (regular REPL is fine for these):

```python
python -m asyncio  # or plain python
>>> from fastapi import FastAPI
>>> from fastmcp import FastMCP
>>> import uvicorn, pydantic
```

## 3. Start the server (no reload in sandboxed envs)

Run this **in the shell, not inside the Python REPL**. If you’re in a `>>>` prompt, type `exit()` or press `Ctrl+D` first.

```bash
uvicorn converter_streamable_http_server:app --host 127.0.0.1 --port 8000
```

- If `--reload` throws “Operation not permitted”, omit it.
- Open http://127.0.0.1:8000/docs and http://127.0.0.1:8000/mcp/docs.

## 4. Explore FastAPI in an async-friendly REPL

Use `python -m asyncio` so `await` works at top level.

```bash
python -m asyncio
>>> from fastapi import FastAPI
>>> app = FastAPI(title="Unit Converter MCP Server", version="1.2.1")
>>> dir(app)[:10]             # sample of attributes
>>> app.title
>>> app.version
>>> app.servers               # []
>>> app.openapi_url           # "/openapi.json"
```

## 5. Explore FastMCP surface

```python
>>> from fastmcp import FastMCP
>>> mcp = FastMCP.from_fastapi(app,
...     name="Unit Converter MCP Server",
...     instructions="Unit conversion tools with supporting resources and prompts.")
>>> dir(mcp)[:15]
>>> mcp.name
>>> mcp.instructions
>>> mcp.local_provider
>>> await mcp.list_tools()    # works here because async REPL
```

## 6. Inspect the real project app & tools

```python
>>> import converter_streamable_http_server as srv
>>> real_app = srv.app
>>> dir(real_app)[:15]
>>> real_app.title, real_app.version
>>> len(real_app.routes)

>>> from mcp_tools.converter_tools import kilometers_to_miles
>>> kilometers_to_miles(5)

>>> mcp2 = FastMCP.from_fastapi(real_app,
...     name="Unit Converter MCP Server",
...     instructions="Unit conversion tools with supporting resources and prompts.")
>>> await mcp2.list_tools()                 # should include "kilometers_to_miles"
>>> await mcp2.get_tool("kilometers_to_miles")
```

**If you see `AttributeError: 'FastMCPOpenAPI' object has no attribute 'list_tools'`:**

- The project constructs MCP via `FastMCP.from_fastapi(real_app, ...)` in `converter_streamable_http_server.py`. Recreate it the same way in your REPL:
  ```python
  >>> from converter_streamable_http_server import app
  >>> from fastmcp import FastMCP
  >>> mcp = FastMCP.from_fastapi(app,
  ...     name="Unit Converter MCP Server",
  ...     instructions="Unit conversion tools with supporting resources and prompts.")
  >>> await mcp.list_tools()
  ```
- Don’t call `list_tools` on `mcp.http_app` or on `FastMCP.from_openapi(...)`; those return the OpenAPI adapter that lacks tool methods.

## 7. System health route

The project now ships with a built-in `/health` route (defined in `converter_streamable_http_server.py`). You can just start the server and hit it:

```bash
curl http://127.0.0.1:8000/health | jq
```

If you want to recreate it manually in the REPL instead, use:

```python
>>> from fastapi import APIRouter
>>> import platform, datetime, os, time  # stdlib only
>>> router = APIRouter(prefix="", tags=["system"])
>>> started_at = time.time()
>>> @router.get("/health")
... def health():
...     return {
...         "status": "ok",
...         "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
...         "python": platform.python_version(),
...         "platform": platform.platform(),
...         "pid": os.getpid(),
...         "cwd": os.getcwd(),
...         "uptime_seconds": round(time.time() - started_at, 2),
...     }
<press Enter on a blank line to finish the function block>
>>> real_app.include_router(router)
```

If you still get `SyntaxError` at the decorator, you likely typed extra `...` yourself. Let the REPL supply the `...` prompts automatically—only type the code shown after them.

## 8. Tear-down

- Stop uvicorn with `Ctrl+C`.
- `deactivate` to leave the venv.

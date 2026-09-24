# MCP SDK / FastMCP REPL Lab

## 1. Create & activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python --version            # expect 3.12.x
```

## 2. Install requirements one by one

Read `requirements.txt`, then install the required packages line-by-line, checking each installation.

```bash
python -m pip install --upgrade pip
pip install fastapi
pip install uvicorn
pip install fastmcp
pip install pydantic
```

> **Version note:** FastMCP changes quickly. This exercise assumes the FastMCP version used by the supplied project. If the project pins package versions in `requirements.txt`, use those versions.

Quick checks after installs:

```bash
python -m asyncio
>>> from fastapi import FastAPI
>>> from fastmcp import FastMCP
>>> import uvicorn, pydantic
```

`python -m asyncio` is useful for this lab because it allows `await` to be used directly at the prompt.

## 3. Start the server

Run this **in the shell, not inside the Python REPL**. If you are at a `>>>` prompt, type `exit()` or press `Ctrl+D` first.

```bash
uvicorn converter_streamable_http_server:app --host 127.0.0.1 --port 8000
```

- If `--reload` throws `Operation not permitted`, omit it.
- Open the FastAPI documentation at:

```text
http://127.0.0.1:8000/docs
```

- The MCP Streamable HTTP endpoint is mounted at:

```text
http://127.0.0.1:8000/mcp/
```

The MCP endpoint is for MCP clients rather than a Swagger documentation page.

## 4. Explore FastAPI in an async-friendly REPL

Open another terminal, activate the virtual environment, then start the asyncio REPL:

```bash
python -m asyncio
```

Explore a small FastAPI application:

```python
>>> from fastapi import FastAPI
>>> app = FastAPI(title="Unit Converter MCP Server", version="1.2.1")
>>> dir(app)[:10]             # sample of attributes
>>> app.title
>>> app.version
>>> app.servers               # []
>>> app.openapi_url           # "/openapi.json"
```

## 5. Explore the FastMCP surface

Create a FastMCP server from the FastAPI application:

```python
>>> from fastmcp import FastMCP
>>> mcp = FastMCP.from_fastapi(app,
...     name="Unit Converter MCP Server",
...     instructions="Unit conversion tools with supporting resources and prompts.")
>>> dir(mcp)[:15]
>>> mcp.name
>>> mcp.instructions
>>> mcp.local_provider
>>> await mcp.list_tools()
```

`await` works here because the lab is using the asyncio REPL.

> **FastMCP version note:** Internal OpenAPI/provider classes have changed between FastMCP versions. For this exercise, work with the `FastMCP` object returned by `FastMCP.from_fastapi()` rather than trying to interact directly with internal adapter classes.

## 6. Inspect the real project app & tools

Import the actual application used by the project:

```python
>>> import converter_streamable_http_server as srv
>>> real_app = srv.app
>>> dir(real_app)[:15]
>>> real_app.title, real_app.version
>>> len(real_app.routes)
```

Now inspect and call one of the project's Python conversion functions directly:

```python
>>> from mcp_tools.converter_tools import kilometers_to_miles
>>> kilometers_to_miles(5)
```

Next, create a new FastMCP server from the real FastAPI application:

```python
>>> mcp2 = FastMCP.from_fastapi(real_app,
...     name="Unit Converter MCP Server",
...     instructions="Unit conversion tools with supporting resources and prompts.")
>>> tools = await mcp2.list_tools()
>>> tools
>>> [tool.name for tool in tools]
```

Look for tools generated from the application's FastAPI/OpenAPI conversion routes.

> **Important:** The supplied application also manually registers an MCP tool named `kilometers_to_miles`. Creating a new `FastMCP` instance with `FastMCP.from_fastapi(real_app)` reproduces tools generated from the FastAPI/OpenAPI routes, but it does not automatically repeat every manual MCP registration performed elsewhere in `converter_streamable_http_server.py`.

If a tool name from the list looks useful, inspect it using that exact name:

```python
>>> await mcp2.get_tool("<tool-name-from-the-list>")
```

Do not assume the generated name will always be exactly `kilometers_to_miles`; generated names can depend on the route and operation metadata.

## 7. System health route

The project ships with a built-in `/health` route defined in `converter_streamable_http_server.py`.

With the server running, test it from another terminal:

```bash
curl http://127.0.0.1:8000/health
```

If `jq` is installed, you can optionally pretty-print the response:

```bash
curl http://127.0.0.1:8000/health | jq
```

If you want to recreate a similar route manually in the REPL for exploration, use:

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
```

Press **Enter on a blank line** to finish the function block, then add the router to the real application:

```python
>>> real_app.include_router(router)
```

If you get a `SyntaxError` at the decorator, you may have typed the `...` prompts yourself. Let the REPL generate `...` automatically and type only the code after the prompt.

## 8. Tear-down

- Stop Uvicorn with `Ctrl+C`.
- Run `deactivate` to leave the virtual environment.

### Step 1: Run both servers

Terminal 1 – HTTP server

```bash
python converter_streamable_http_server.py
```

Terminal 2 – STDIO + Inspector

```bash
npx @modelcontextprotocol/inspector python converter_stdio_server.py
```

Open in browser:

- http://localhost:8003/docs
- http://localhost:8003/mcp

Keep the inspector tab open.

### Step 2: Understand logging

Open `logging_utils.py`

Investigate:

- What handler class creates the rotating log files?
- What is the default maximum size per log file?
- How many backup files are kept?
- What happens if you set `console=False`?
- What is the difference between the `root` logger level and the level given to named loggers (e.g. `"fastmcp"`, `"uvicorn"`)?
- Look in both server files to see where `build_log_config` is called and where `configure_logging` / `LOG_CONFIG` is used.

### Step 3: Logging experiments

Do these one at a time → restart server → observe console + log files after each change.

1. Silence console in stdio server only  
   `converter_stdio_server.py` → set `console=False`

2. Make HTTP server very verbose  
   `converter_streamable_http_server.py`

```python
root_level="DEBUG"
# and
uvicorn.run(..., log_level="debug", ...)
```

3. Give fastmcp its own logger (file only)  
   In **both** server files, add to `logger_handlers`:

```python
"fastmcp": ["rotating_file"],
```

4. Central control logging file size
   In `logging_utils.py` temporarily change  
   `"maxBytes": 1 * 1024 * 1024,` (1 MB)

### Step 4: Intentionally break things

Add one error per component:

`converter_tools.py`

```python
def celsius_to_fahrenheit_value(celsius: float) -> float:
    if celsius < -273.15:
        raise ValueError("Physically impossible: below absolute zero!")
    return (celsius * 9 / 5) + 32
```

`converter_resources.py`

```python
def unit_reference() -> Dict[str, Any]:
    raise RuntimeError("Cheatsheet service temporarily unavailable")
    # rest of function...
```

`converter_prompts.py`

```python
def explain_conversion_prompt() -> List[Dict[str, str]]:
    1 / 0   # ZeroDivisionError on purpose
    return [ ... ]   # original code
```

Save & restart both servers.

### Step 5: Debug using Inspector + log files

In the **MCP Inspector** (try both stdio connection and streamable-http):

- Call tool: `celsius_to_fahrenheit` with input `-300`
- Fetch resource: `resource://unit_reference`
- Use prompt: `explain_conversion`

Note:

- How errors are shown in the UI
- Full stack traces
- Which file + line is highlighted

Then open the two log files:

- `logs/http_....log`
- `logs/stdio_....log`

Search for `ValueError`, `RuntimeError`, `ZeroDivisionError`

Why do the tracebacks look almost the same in both transports / log files?

### Step 6: Logging clean-up

- Remove or comment out the three lines you added that raise exceptions
- Revert any logging experiments you want to reset (console=True, levels back to INFO, etc.)
- Restart servers & confirm normal operation again

### Step 7: Clean Up & Investigate Libraries

1. Make sure the three `raise` / `1/0` lines are removed or commented out.
2. Restart both servers & verify that tools, resources and prompts work normally again.

**Framework library exploration** (do it in a Python shell, Jupyter, or even at the bottom of any .py file):

**FastAPI**

```python
import fastapi
help(fastapi.FastAPI)
# or just see where it lives:
print(fastapi.__file__)
```

**FastMCP**

```python
import fastmcp
help(fastmcp.FastMCP)
print(fastmcp.__file__)
```

**Final questions**

1. What is the **main class** that turns a normal FastAPI application into an MCP server?
2. In the HTTP server file, which transport is mounted at the `/mcp` path?

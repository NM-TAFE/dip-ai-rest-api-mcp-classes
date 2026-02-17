# Tutorial: Unit Converter API + MCP (tools, resources, prompts)
# Uses FastAPI for HTTP routes and FastMCP to expose tools/resources/prompts over HTTP/SSE transports.

from fastapi import FastAPI
from fastmcp import FastMCP

from converter_tools import router as converter_router
from converter_resources import unit_reference, troubleshooting_guide
from converter_prompts import explain_conversion_prompt, api_usage_prompt

from pathlib import Path
import uvicorn

PORT = 8003  # adjust as needed

# Use a raw string for Windows paths or Path for robustness
# LOG_FILE = Path(r"C:\ProgramData\Laragon\www\repos\REST-API\Material\session3\mcp_session3_example\logs\mcp_log_v1.log")
LOG_FILE = Path(r".\logs\mcp_log_v1.log")

# 1) Ensure the directory exists
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# 2) Build a valid dictConfig
LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        "access": {
            "format": '%(asctime)s [%(levelname)s] %(client_addr)s - "%(request_line)s" %(status_code)s'
        },
    },
    "handlers": {
        "rotating_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": str(LOG_FILE),
            "maxBytes": 10 * 1024 * 1024,  # 10 MB
            "backupCount": 3,
            "encoding": "utf-8",
            "delay": True,  # open file lazily to avoid early open during config
        },
        # Optional: also mirror to console while you debug
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "uvicorn":         {"level": "DEBUG", "handlers": ["rotating_file", "console"], "propagate": False},
        "uvicorn.error":   {"level": "DEBUG", "handlers": ["rotating_file", "console"], "propagate": False},
        "uvicorn.access":  {"level": "DEBUG", "handlers": ["rotating_file"], "propagate": False},
    },
    "root": {"level": "INFO", "handlers": ["rotating_file", "console"]},
}

# FastAPI app for plain HTTP
app = FastAPI(
    title="Unit Converter API Tutorial",
    description="FastAPI endpoints auto-exposed as MCP tools via FastMCP, with resources and prompts.",
    version="1.2.1",
)
app.include_router(converter_router)

# FastMCP server generated from FastAPI OpenAPI (tools) plus manual resources/prompts
mcp = FastMCP.from_fastapi(
    app,
    name="Unit Converter API with MCP",
    instructions="Unit conversion tools with supporting resources and prompts.",
)


# Resources
@mcp.resource("resource://unit_reference", name="Unit Converter Cheatsheet", mime_type="application/json")
def _resource_unit_reference():
    return unit_reference()


@mcp.resource("resource://troubleshooting_guide", name="Troubleshooting Guide", mime_type="text/plain")
def _resource_troubleshooting():
    return troubleshooting_guide()


# Prompts
@mcp.prompt(name="explain_conversion", description="Guide a learner through the math for a conversion.")
def _prompt_explain_conversion():
    return explain_conversion_prompt()


@mcp.prompt(name="api_usage", description="Produce a curl example for a conversion endpoint.")
def _prompt_api_usage():
    return api_usage_prompt()


# Build MCP sub-apps (need lifespan) and mount onto FastAPI
mcp_http_app = mcp.http_app(path="/", transport="streamable-http")
mcp_sse_app = mcp.http_app(path="/", transport="sse")
# Ensure FastAPI runs the MCP lifespan so streamable-http task group initializes
app.router.lifespan_context = mcp_http_app.lifespan

app.mount("/mcp", mcp_http_app)
app.mount("/sse", mcp_sse_app)


if __name__ == "__main__":
    import uvicorn
    PORT = 8003 # avoid conflicts/permissions on lower ports
    print("Starting the Unit Converter API server (HTTP + MCP tools/resources/prompts)...")
    print(f"HTTP docs:      http://localhost:{PORT}/docs")
    print(f"HTTP redoc:     http://localhost:{PORT}/redoc")
    print(f"MCP endpoint:   http://localhost:{PORT}/mcp (HTTP)")
    print(f"MCP endpoint:   http://localhost:{PORT}/sse (SSE)")
    # uvicorn.run(app, host="localhost", port=PORT, log_level="trace", log_config={"handler": "file_handler", "level": "TRACE", "filename": './log/mcp_log_v1.log'})

    
    uvicorn.run(
        app,
        host="localhost",
        port=PORT,
        log_level="trace",   # Uvicorn internal level
        log_config=LOG_CONFIG,
    )


# Try it out!
# 1) Run: python calculator_api_tutorial.py
# 2) Visit the docs above to exercise the HTTP endpoints.
# 3) Use MCP clients (mcp-remote or inspector) against /mcp (http) or /sse (sse) to list tools/resources/prompts.

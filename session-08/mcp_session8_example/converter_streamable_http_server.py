# Unit Converter API + MCP (tools, resources, prompts)
# Uses FastAPI for HTTP routes and FastMCP to expose tools/resources/prompts over HTTP/SSE transports.
from fastapi import FastAPI, APIRouter
from fastmcp import FastMCP

from mcp_tools.converter_tools import router as converter_router
from mcp_tools.miles_to_km import router as mile_to_km
from mcp_prompts.converter_prompts import explain_conversion_prompt, api_usage_prompt
from mcp_resources.converter_resources import RESOURCE_DEFINITIONS
from utils.resource_utils import register_resources

from utils.logging_utils import build_log_config
import platform
import datetime
import os
import time
from pathlib import Path
import uvicorn

# Set up your logging preferences 
# LOG_FILE = Path(r".\logs\mcp_log_streamable_http.log")(use forward slashes on mac/Linux too)
LOG_FILE = Path("logs/mcp_log_streamable_http.log")

LOG_CONFIG = build_log_config(
    LOG_FILE,
    logger_handlers={
        "uvicorn": ["rotating_file", "console"],
        "uvicorn.error": ["rotating_file", "console"],
        "uvicorn.access": ["rotating_file"],
    },
    root_level="INFO",
    logger_level="DEBUG",
)

# FastAPI app for plain HTTP
app = FastAPI(
    title="Unit Converter MCP Server",
    description="FastAPI endpoints auto-exposed as MCP tools via FastMCP, with resources and prompts.",
    version="1.2.1",
)

# --- Register Prompts ---
app.include_router(converter_router)
app.include_router(mile_to_km)

# --- Register System ---
system_router = APIRouter(prefix="", tags=["system"])
started_at = time.time()

@system_router.get("/health")
def health():
    return {
        "status": "ok",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "python": platform.python_version(),
        "platform": platform.platform(),
        "pid": os.getpid(),
        "cwd": os.getcwd(),
        "uptime_seconds": round(time.time() - started_at, 2),
    }

app.include_router(system_router)

# FastMCP server generated from FastAPI OpenAPI (tools) plus manual resources/prompts
mcp = FastMCP.from_fastapi(
    app,
    name="Unit Converter MCP Server",
    instructions="Unit conversion tools with supporting resources and prompts.",
)

# --- Register Resources --- dynamically via URI template
register_resources(mcp, RESOURCE_DEFINITIONS)

# Prompts
@mcp.prompt(name="explain_conversion", description="Guide a learner through the math for a conversion.")
def _prompt_explain_conversion():
    return explain_conversion_prompt()


@mcp.prompt(name="api_usage", description="Produce a curl example for a conversion endpoint.")
def _prompt_api_usage():
    return api_usage_prompt()

# Build MCP sub-application and mount onto FastAPI
mcp_http_app = mcp.http_app(path="/", transport="streamable-http")

# Ensure FastAPI runs the MCP lifespan so streamable-http initialises properly
app.router.lifespan_context = mcp_http_app.lifespan

app.mount("/mcp", mcp_http_app)

if __name__ == "__main__":
    import uvicorn

    PORT = 8003

    print("Starting the Unit Converter API server (HTTP + MCP tools/resources/prompts)...")
    print(f"HTTP docs:      http://localhost:{PORT}/docs")
    print(f"HTTP redoc:     http://localhost:{PORT}/redoc")
    print(f"MCP endpoint:   http://localhost:{PORT}/mcp (HTTP)")

    uvicorn.run(
        app,
        host="localhost",
        port=PORT,
        log_level="trace",   # Uvicorn internal logging
        log_config=LOG_CONFIG,
    )
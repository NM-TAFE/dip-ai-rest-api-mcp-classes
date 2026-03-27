from pathlib import Path

from fastmcp import FastMCP

from mcp_tools.converter_tools import TOOL_DEFINITIONS
from mcp_resources.converter_resources import RESOURCE_DEFINITIONS
from mcp_prompts.converter_prompts import PROMPT_DEFINITIONS
from utils.resource_utils import register_resources

from utils.logging_utils import build_log_config, configure_logging

# Set up your logging preferences
LOG_FILE = Path("./logs/mcp_log_stdio.log")
configure_logging(
    build_log_config(
        LOG_FILE,
        console=True,
        logger_handlers={
            "fastmcp": ["rotating_file", "console"],
        },
        root_level="INFO",
        logger_level="DEBUG",
    )
)

mcp = FastMCP("Unit Converter (STDIO)")

# --- Register tools ---
for tool in TOOL_DEFINITIONS:
    mcp.tool(
        name=tool["name"],
        description=tool.get("description", tool["name"])
    )(tool["func"])

# --- Register resources (dynamic template: resource://converter/{name}) ---
register_resources(mcp, RESOURCE_DEFINITIONS)

# --- Register prompt templates ---
for prompt in PROMPT_DEFINITIONS:
    print(prompt)
    name = prompt["name"]
    desc= prompt.get("description", name)
    prompt_function = prompt["func"]

    # Register the prompt function as-is (it returns a list[dict])
    mcp.prompt(name=name, description=desc)(prompt_function)

if __name__ == "__main__":
    mcp.run()

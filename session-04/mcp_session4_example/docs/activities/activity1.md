## Setup

```bash
# from this folder
python -m venv .venv
# Mac or Gitbash
source .venv/bin/activate
# Windows powershell:
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

---

## 2. start the STDIO server with **MCP Inspector** (Windows)

**Important**: Inspector **launches your STDIO server as a child process**. Do **not** start the server manually first.

### Step 2.2 — Launch MCP Inspector + your STDIO server

Use the Python launcher:

```powershell
npx @modelcontextprotocol/inspector python converter_stdio_server.py
```

Or call your venv’s Python:

```powershell
# Use this command
npx @modelcontextprotocol/inspector python converter_stdio_server.py
npx @modelcontextprotocol/inspector .\venv\Scripts\python.exe converter_stdio_server.py
```

**What you should see in the Inspector UI**

- **Tools**: `celsius_to_fahrenheit`, `fahrenheit_to_celsius`, `kilometers_to_miles`, `miles_to_kilometers`
- **Resources**: `resource://unit_reference`, `resource://troubleshooting_guide`  
  You can invoke tools and preview resources directly in the UI. citeturn11search41

---

## 3. Test the STDIO server from the **Windows command line (no UI)**

Two Windows‑friendly approaches are shown below.

### Option A Raw JSON‑RPC over STDIO (advanced)

MCP STDIO uses **newline‑delimited JSON‑RPC**; you can interact manually to see protocol flow.

1. Open two terminals: one to run the server, one to paste JSON into stdin.

```powershell
.\venv\Scripts\python.exe converter_stdio_server.py
```

2. Paste messages in order (one line each):

```json
{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"windows-shell","version":"0.1"}},"id":1}
{"jsonrpc":"2.0","method":"notifications/initialized"}
{"jsonrpc":"2.0","method":"tools/list","id":2}
{"jsonrpc":"2.0","method":"tools/call","params":{"name":"celsius_to_fahrenheit","arguments":{"celsius":25}},"id":3}
```

> That sequence demonstrates the MCP lifecycle and basic tool invocation.

3. Troubleshooting (Windows)

- **JSON quoting in PowerShell**: Use escaped double quotes inside the `--params` string, e.g. `"{\"miles\": 3.1}"`.
- **Inspector fails to run your Python**: Use the full venv path:  
  `npx @modelcontextprotocol/inspector .\venv\Scripts\python.exe converter_stdio_server.py`
- **STDIO environment isolation**: If your tools require env vars (API keys), remember STDIO‑launched servers **don’t inherit** your shell env; pass env explicitly via Inspector flags or CLI.
- **Keep Inspector updated**: Ensure version ≥ **0.14.1** (patched).

---

4. Out of class task

- Add a new conversion tool (e.g., meters +
  to/from feet) via `TOOL_DEFINITIONS`; re‑run the activity.
- Trigger a validation error (e.g., negative distance) and observe the JSON‑RPC error in Inspector.
- Later, try **Streamable HTTP** for networked/production deployments.

---

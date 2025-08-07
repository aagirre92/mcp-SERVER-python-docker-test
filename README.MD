## MCP Python Docker Test

This project demonstrates a minimal Model Context Protocol (MCP) server implemented in Python, designed to run inside a Docker container. It provides a set of simple mathematical tools (add, subtract, multiply, divide, and distance calculations) that can be exposed to LLM agents and Copilot Studio for programmatic use.

### Project Intent
- **Showcase** how to build and expose Python functions as MCP tools for agent frameworks.
- **Test** compatibility with Copilot Studio and similar LLM agent platforms.
- **Demonstrate** the difference in tool visibility when using simple types vs. Pydantic models as function arguments.

### Key Features
- Implements basic math operations as MCP tools.
- Includes two distance calculation tools:
  - `coordinates_distance`: Uses a Pydantic model (not visible to Copilot Studio agents).
  - `coordinates_distance_simple_types`: Uses only primitive types (visible to Copilot Studio agents).
- Ready to run in Docker or locally.

### Tool Visibility Limitation
> **Note:** MCP tools that use Pydantic models as arguments (e.g., `coordinates_distance`) are **not supported by Microsoft Copilot Studio** and will not appear in the agent toolset. Use only primitive types for maximum compatibility.

### Usage

**Good old Docker:**
   ```sh
   docker build -t mcp-python-docker-test .
   docker run -p 8080:8080 mcp-python-docker-test
   ```

### File Overview
- `server.py` — Main MCP server and tool definitions
- `pyproject.toml` — Project metadata and dependencies
- `Dockerfile` — Containerization instructions
- `test_server.py` — (Optional) Tests for the server
- `uv.lock` — Dependency lock file

### How to share it outside localhost

Use [devtunnel](https://learn.microsoft.com/en-us/azure/developer/dev-tunnels/get-started?tabs=windows#install) tool and these commands

```powershell
devtunnel user login
devtunnel create test-mcp -a --host-header unchanged
devtunnel port create test-mcp -p 8080
devtunnel host test-mcp
```

This tunnel will give you a public url that you may use in copilot connector as host

### IMPORTANT:

* **MS Copilot MCP - Custom Connector definition**: For some reason, in the copilot studio connector definition, you must put `/mcp/` (notice the final slash). This is the :

```yaml
swagger: '2.0'
info:
  title: GCP-MCP
  description: ''
  version: '1.0'
host: 9jx97sr1-5000.uks1.devtunnels.ms
basePath: /
schemes:
  - https
paths:
  /mcp/:
    post:
      summary: Andoni test GCP Cloud Run
      x-ms-agentic-protocol: mcp-streamable-1.0
      operationId: InvokeMCP
      responses:
        '200':
          description: Success
securityDefinitions: {}
```


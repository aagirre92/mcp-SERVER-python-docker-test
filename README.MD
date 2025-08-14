# MCP Python Docker Test

This project demonstrates a minimal Model Context Protocol (MCP) server in Python, designed to run inside a Docker container and expose simple mathematical tools for use with LLM agents and Microsoft Copilot Studio.

## GCP Cloud Run
This repository is connected to GCP Cloud run `mcp-server`

## Main Script

**`mcp-server-oauth-gcp-cloudRun.py`** is the main entry point.  
It starts an MCP server with OAuth2 authentication using Google Cloud credentials. The script:
- Verifies Google OAuth2 access tokens and restricts access to allowed emails.
- Exposes math tools (`add`, `subtract`, `multiply`, `divide`, and distance calculations) as MCP tools.
- Supports both primitive-type and Pydantic model arguments (**⚠️: only primitive-type tools are visible to Copilot Studio agents. Those tools that have non-primitive types as INPUT are not shown in Copilot Studio Agents**).

## Quick Start

**Build and run with Docker:**
```sh
docker build -t mcp-python-docker-test .
docker run -p 8080:8080 mcp-python-docker-test
```

## Copilot Studio Integration

- Use a public URL (e.g., via [devtunnel](https://learn.microsoft.com/en-us/azure/developer/dev-tunnels/get-started?tabs=windows#install)) as the host.
- In the Copilot Studio connector definition, set the path to `/mcp/` (with the trailing slash). **⚠️ When using FastMCP with `from fastmcp import FastMCP` I had to put the final slash, but when using it with from mcp.server.fastmcp import FastMCP I did not put! This is very important**

**Example Swagger:**
```yaml
swagger: '2.0'
info:
  title: GCP-MCP
  version: '1.0'
host: <your-public-url>
basePath: /
schemes:
  - https
paths:
  /mcp/:
    post:
      summary: MCP endpoint
      x-ms-agentic-protocol: mcp-streamable-1.0
      operationId: InvokeMCP
      responses:
        '200':
          description: Success
securityDefinitions: {}
```

## Files

- `mcp-server-oauth-gcp-cloudRun.py` — Main MCP server with Google OAuth2
- `Dockerfile` — Containerization instructions
- `pyproject.toml` — Project dependencies
- `server.py` — (Alternative) MCP server without
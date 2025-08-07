import asyncio
import httpx

from fastmcp import Client

async def test_server():
    # Test the MCP server using streamable-http transport.
    # Use "/sse" endpoint if using sse transport.
    #cliente = "https://mcp-server-xq6erlxn4a-uc.a.run.app/mcp"
    cliente = "https://9jx97sr1-5000.uks1.devtunnels.ms/mcp/"  # For local testing
    print(f">>> Connecting to MCP server at {cliente}")
    async with Client(cliente) as client:
        # List available tools
        tools = await client.list_tools()
        for tool in tools:
            print(f">>> Tool found: {tool.name}")
        # Call add tool
        print(">>>  Calling add tool for 1 + 2")
        result = await client.call_tool("add", {"a": 1, "b": 2})
        print(f"Result for add tool: {result.data}")
        # Call subtract tool
        print(">>>  Calling subtract tool for 10 - 3")
        result = await client.call_tool("subtract", {"a": 10, "b": 3})
        print(f"Result for subtract tool: {result.data}")

if __name__ == "__main__":
    asyncio.run(test_server())

import asyncio
import logging
import os
from pydantic import BaseModel,Field

from fastmcp import FastMCP 

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)



mcp = FastMCP("MCP Server on Cloud Run")

class Coordinates(BaseModel):
    """Coordinates for a point in 2D space."""
    x: float = Field(description="X coordinate")
    y: float = Field(description="Y coordinate")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Use this to add two numbers together.
    
    Args:
        a: The first number.
        b: The second number.
    
    Returns:
        The sum of the two numbers.
    """
    logger.info(f">>> Tool: 'add' called with numbers '{a}' and '{b}'")
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Use this to subtract two numbers.
    
    Args:
        a: The first number.
        b: The second number.
    
    Returns:
        The difference of the two numbers.
    """
    logger.info(f">>> Tool: 'subtract' called with numbers '{a}' and '{b}'")
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Use this to multiply two numbers.
    
    Args:
        a: The first number.
        b: The second number.
    
    Returns:
        The product of the two numbers.
    """
    logger.info(f">>> Tool: 'multiply' called with numbers '{a}' and '{b}'")
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> float:
    """Use this to divide two numbers.
    
    Args:
        a: The numerator.
        b: The denominator.
    
    Returns:
        The quotient of the two numbers.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    logger.info(f">>> Tool: 'divide' called with numbers '{a}' and '{b}'")
    return a / b

@mcp.tool()
def coordinates_distance(coord1: Coordinates, coord2: Coordinates) -> float:
    """Calculate the distance between two points in 2D space. THIS TOOL IS NOT VISIBLE FOR COPILOT STUDIO AGENTS,
      AS IT USES A Pydantic MODEL.
    
    Args:
        coord1: The first point's coordinates.
        coord2: The second point's coordinates.
    
    Returns:
        The Euclidean distance between the two points.
    """
    logger.info(f">>> Tool: 'coordinates_distance' called with coordinates '{coord1}' and '{coord2}'")
    return ((coord1.x - coord2.x) ** 2 + (coord1.y - coord2.y) ** 2) ** 0.5

@mcp.tool()
def coordinates_distance_simple_types(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate the distance between two points in 2D space.
    This tool uses simple types instead of a Pydantic model (THEREFORE IT IS VISIBLE FOR COPILOT STUDIO AGENTS).

    Args:
        x1: X coordinate of the first point.
        y1: Y coordinate of the first point.
        x2: X coordinate of the second point.
        y2: Y coordinate of the second point.

    Returns:
        The Euclidean distance between the two points.
    """
    logger.info(f">>> Tool: 'coordinates_distance' called with coordinates ({x1}, {y1}) and ({x2}, {y2})")
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

if __name__ == "__main__":
    logger.info(f" MCP server started on port {os.getenv('PORT', 8080)}")
    # Could also use 'sse' transport, host="0.0.0.0" required for Cloud Run.
    asyncio.run(
        mcp.run_async(
            transport="streamable-http", 
            host="0.0.0.0", 
            port=os.getenv("PORT", 8080),
        )
    )

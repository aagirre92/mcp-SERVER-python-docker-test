"""
Run from the repository root:
    uv run examples/snippets/servers/oauth_server.py
"""
import os
import logging
from pydantic import AnyHttpUrl,BaseModel, Field
import requests
from dotenv import load_dotenv
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import FastMCP
# from fastmcp import FastMCP  # Ensure you have the correct import for FastMCP
# Load environment variables from .env file
load_dotenv()

# -- Setup logging --
logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

# --- Oauth settings ---

GOOGLE_ISSUER = "https://accounts.google.com"
GCP_OAUTH_CLIENT_ID = os.getenv("GCP_OAUTH_CLIENT_ID")  # Must match your OAuth client ID

class SimpleTokenVerifier(TokenVerifier):
    """Simple token verifier for demonstration.
    Docu url: https://gofastmcp.com/python-sdk/fastmcp-server-auth-providers-in_memory#verify-token
    """

    async def verify_token(self, token: str) -> AccessToken | None:
        print(f"Verifying token: {token}")
        gcp_access_token_verification_url = f"https://oauth2.googleapis.com/tokeninfo?access_token={token}"
        response = requests.get(gcp_access_token_verification_url)
        #response.raise_for_status()
        token_info = response.json()

        if token_info.get("error") == "invalid_token":
            print("🚨 Invalid token received from Google OAuth.")
            return None
        
        if token_info.get("aud") == os.getenv("GCP_OAUTH_CLIENT_ID") and token_info.get("email") in os.getenv("GCP_OAUTH_ALLOWED_EMAILS", "").split(","):
            access_token = AccessToken(
                token=token,
                client_id=token_info.get("aud"),
                scopes=token_info.get("scope", "").split(), # split function splits scopes by space (default)
                expires_at=token_info.get("exp"),
            )
            print(f"✅Token verified successfully: {access_token}")
            # Return the access token if verification is successful
        
            return access_token
        else:
            print("Invalid token or audience mismatch.")
            return None
        # Here you would implement the actual token verification logic
        pass  # This is where you would implement actual token validation


# Create FastMCP instance as a Resource Server (with from mcp.server.fastmcp import FastMCP)

# ------- FastMCP instance -------
mcp = FastMCP(
    name="Basic Math Toolset Andoni",
    host="0.0.0.0",
    port=int(os.getenv("PORT", 8000)),  # Default to 8000 if PORT is not set
    # Token verifier for authentication
    token_verifier=SimpleTokenVerifier(),
    # Auth settings for RFC 9728 Protected Resource Metadata
    auth=AuthSettings(
        issuer_url=AnyHttpUrl(GOOGLE_ISSUER),  # Authorization Server URL
        resource_server_url=AnyHttpUrl(f"http://localhost:{os.getenv('PORT', 8000)}"),  # This server's URL
        required_scopes=["openid"],
    ),
)

# -------------------- Tools --------------------
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
    mcp.run(transport="streamable-http")